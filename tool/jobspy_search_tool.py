"""
title: JobSpy Job Search Tool
author: Beau D'Amore www.damore.ai
version: 1.0.0
description: Search for jobs across multiple job boards (LinkedIn, Indeed, ZipRecruiter, Glassdoor, Google, etc.) using the JobSpy library. Configure default search parameters and get aggregated job results.
requirements: python-jobspy, pandas

This tool uses the python-jobspy library for job searching.
Credit: python-jobspy - https://pypi.org/project/python-jobspy/
"""

import asyncio
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


def _format_job_results(jobs_df, search_params: Dict[str, Any]) -> str:
    """INTERNAL ONLY - Format job search results for display in tabular format with expandable details"""
    if jobs_df.empty:
        return "❌ No jobs found matching your criteria"

    result_count = len(jobs_df)
    output = f"🔍 **Job Search Results**\n"
    output += f"**Search Term:** {search_params.get('search_term', 'N/A')}\n"
    output += f"**Location:** {search_params.get('location', 'N/A')}\n"
    output += f"**Sites Searched:** {search_params.get('sites', 'N/A')}\n"
    output += f"**Results Found:** {result_count}\n\n"

    # Create table header
    output += "| # | Job Title | Company | Location | Type | Salary | Posted | Source | Apply |\n"
    output += "|---|-----------|---------|----------|------|--------|--------|--------|-------|\n"

    # Iterate through jobs and format each row
    for idx, job in jobs_df.iterrows():
        # Job number
        row = f"| {idx + 1} | "
        
        # Job title
        title = job.get('title', 'N/A')
        row += f"{title} | "
        
        # Company
        company = job.get('company', 'N/A')
        row += f"{company} | "
        
        # Location with remote indicator
        location = job.get('location', 'N/A')
        if job.get('is_remote'):
            location += " 🏠"
        row += f"{location} | "
        
        # Job type
        job_type = job.get('job_type', '-')
        if job_type and job_type != '-':
            job_type = str(job_type).title()
        else:
            job_type = '-'
        row += f"{job_type} | "
        
        # Salary information
        salary = ""
        if job.get('min_amount') or job.get('max_amount'):
            if job.get('min_amount') and job.get('max_amount'):
                salary = f"${job.get('min_amount'):,.0f}-${job.get('max_amount'):,.0f}"
            elif job.get('min_amount'):
                salary = f"${job.get('min_amount'):,.0f}+"
            elif job.get('max_amount'):
                salary = f"Up to ${job.get('max_amount'):,.0f}"
            
            if job.get('interval'):
                interval_val = str(job.get('interval', ''))
                interval_short = interval_val.replace('yearly', '/yr').replace('monthly', '/mo').replace('hourly', '/hr').replace('weekly', '/wk')
                salary += f" {interval_short}"
        else:
            salary = '-'
        row += f"{salary} | "
        
        # Date posted
        date_posted = job.get('date_posted', '-')
        if date_posted and date_posted != '-':
            # Try to format date more concisely
            try:
                from datetime import datetime
                date_posted = str(date_posted)
                if isinstance(date_posted, str):
                    date_posted = date_posted.split()[0]  # Get just the date part if datetime
            except:
                pass
        row += f"{str(date_posted)} | "
        
        # Source site
        site = job.get('site', '-')
        if site and site != '-':
            site = str(site).title().replace('_', ' ')
        else:
            site = '-'
        row += f"{site} | "
        
        # Apply link
        job_url = job.get('job_url', '')
        if job_url:
            row += f"[Apply]({job_url}) |"
        else:
            row += "- |"
        
        output += row + "\n"

    # Add expandable details section for each job
    output += "\n---\n\n## 📋 Detailed Job Information\n\n"
    
    for idx, job in jobs_df.iterrows():
        job_num = idx + 1
        title = job.get('title', 'N/A')
        company = job.get('company', 'N/A')
        
        output += f"<details>\n<summary><strong>Job #{job_num}: {title} at {company}</strong></summary>\n\n"
        
        # Basic Information
        output += "### 📌 Overview\n\n"
        output += f"- **Position:** {job.get('title', 'N/A')}\n"
        output += f"- **Company:** {job.get('company', 'N/A')}\n"
        output += f"- **Location:** {job.get('location', 'N/A')}\n"
        
        if job.get('is_remote'):
            output += f"- **Remote Work:** ✅ Yes\n"
        
        if job.get('job_type'):
            output += f"- **Job Type:** {str(job.get('job_type', '')).title()}\n"
        
        site_val = str(job.get('site', 'N/A'))
        output += f"- **Source:** {site_val.replace('_', ' ').title()}\n"
        output += f"- **Date Posted:** {str(job.get('date_posted', 'N/A'))}\n"
        
        # Compensation
        if job.get('min_amount') or job.get('max_amount') or job.get('currency'):
            output += "\n### 💰 Compensation\n\n"
            
            if job.get('min_amount') or job.get('max_amount'):
                if job.get('min_amount') and job.get('max_amount'):
                    output += f"- **Salary Range:** ${job.get('min_amount'):,.0f} - ${job.get('max_amount'):,.0f}\n"
                elif job.get('min_amount'):
                    output += f"- **Minimum Salary:** ${job.get('min_amount'):,.0f}\n"
                elif job.get('max_amount'):
                    output += f"- **Maximum Salary:** ${job.get('max_amount'):,.0f}\n"
            
            if job.get('interval'):
                output += f"- **Payment Interval:** {str(job.get('interval', '')).title()}\n"
            
            if job.get('currency'):
                output += f"- **Currency:** {job.get('currency')}\n"
        
        # Additional Details
        if job.get('emails') or job.get('num_urgent_words') or job.get('benefits'):
            output += "\n### ℹ️ Additional Information\n\n"
            
            if job.get('emails'):
                output += f"- **Contact Email:** {job.get('emails')}\n"
            
            if job.get('num_urgent_words'):
                output += f"- **Urgency Indicators:** {job.get('num_urgent_words')}\n"
            
            if job.get('benefits'):
                output += f"- **Benefits:** {job.get('benefits')}\n"
        
        # Job Description
        if job.get('description'):
            output += "\n### 📝 Job Description\n\n"
            description = str(job.get('description', ''))
            # Clean up description
            description = description.strip()
            output += f"{description}\n"
        
        # Application Link
        output += "\n### 🔗 Apply Now\n\n"
        if job.get('job_url'):
            output += f"**[→ Click here to apply for this position]({job.get('job_url')})**\n"
        else:
            output += "*No application link available*\n"
        
        output += "\n</details>\n\n"

    return output


class Tools:
    @staticmethod
    async def emit_status(eventer, msg: str, done: bool = False, hidden: bool = False):
        """Emit status update to OpenWebUI interface"""
        await eventer(
            {
                "type": "status",
                "data": {
                    "description": msg,
                    "done": done,
                    "hidden": hidden,
                },
            }
        )

    @staticmethod
    async def emit_error(eventer, msg: str, done: bool = True, hidden: bool = False):
        """Emit error message to OpenWebUI interface"""
        await eventer(
            {
                "type": "error",
                "data": {
                    "description": msg,
                    "done": done,
                    "hidden": hidden,
                },
            }
        )

    @staticmethod
    async def emit_result(
        eventer, content: str, done: bool = True, hidden: bool = False
    ):
        """Emit final result to OpenWebUI interface"""
        await eventer(
            {
                "type": "result",
                "data": {
                    "description": content,
                    "done": done,
                    "hidden": hidden,
                },
            }
        )

    class Valves(BaseModel):
        """Configuration parameters for the job search tool"""

        default_sites: str = Field(
            default="linkedin,indeed,zip_recruiter",
            description="Comma-separated list of job sites to search. Options: linkedin, indeed, zip_recruiter, glassdoor, google, bayt, naukri, bdjobs",
        )
        default_location: str = Field(
            default="",
            description="Default location for job searches (e.g., 'San Francisco, CA', 'New York, NY')",
        )
        default_country: str = Field(
            default="USA",
            description="Default country for Indeed/Glassdoor searches (e.g., 'USA', 'Canada', 'UK')",
        )
        default_distance: int = Field(
            default=50,
            description="Default search radius in miles",
        )
        default_results_wanted: int = Field(
            default=15,
            description="Default number of job results to retrieve per site",
        )
        default_hours_old: int = Field(
            default=72,
            description="Default filter for jobs posted within X hours (0 = no filter)",
        )
        default_is_remote: bool = Field(
            default=False,
            description="Default remote job filter",
        )
        default_job_type: str = Field(
            default="",
            description="Default job type filter. Options: fulltime, parttime, internship, contract (leave empty for all)",
        )
        enable_debug_output: bool = Field(
            default=True,
            description="Include debug information in responses",
        )

    def __init__(self):
        self.valves = self.Valves()

    async def search_jobs(
        self,
        search_term: str,
        location: Optional[str] = None,
        site_name: Optional[str] = None,
        job_type: Optional[str] = None,
        is_remote: Optional[bool] = None,
        results_wanted: Optional[int] = None,
        hours_old: Optional[int] = None,
        distance: Optional[int] = None,
        __event_emitter__=None,
    ) -> str:
        """
        Search for jobs across multiple job boards using JobSpy library.
        
        **THIS IS THE ONLY METHOD YOU SHOULD CALL.**
        
        Args:
            search_term: Job title or keywords to search for (e.g., "software engineer", "data analyst")
            location: Optional location to search in (e.g., "San Francisco, CA", "Remote"). Uses default if not provided.
            site_name: Optional comma-separated list of job sites (e.g., "linkedin,indeed"). Uses default if not provided.
            job_type: Optional job type filter ("fulltime", "parttime", "internship", "contract")
            is_remote: Optional remote job filter (True/False)
            results_wanted: Optional number of results per site (uses default if not provided)
            hours_old: Optional filter for jobs posted within X hours
            distance: Optional search radius in miles
            
        Returns:
            Formatted job search results with title, company, location, salary, and links
            
        Example:
            search_jobs(search_term="python developer", location="New York, NY", is_remote=True)
        """
        # Setup event emitter
        eventer = __event_emitter__ or (lambda *args, **kwargs: asyncio.sleep(0))

        # Use provided values or fall back to defaults
        location = location or self.valves.default_location
        site_name = site_name or self.valves.default_sites
        job_type = job_type or self.valves.default_job_type or None
        is_remote = is_remote if is_remote is not None else self.valves.default_is_remote
        results_wanted = results_wanted or self.valves.default_results_wanted
        hours_old = hours_old if hours_old is not None else self.valves.default_hours_old
        distance = distance or self.valves.default_distance

        # Convert hours_old to None if 0
        if hours_old == 0:
            hours_old = None

        # Parse site names
        sites_list = [s.strip() for s in site_name.split(",") if s.strip()]

        debug_info = ""
        if self.valves.enable_debug_output:
            debug_info = f"""🔧 **Debug Information**:
- Search Term: '{search_term}'
- Location: '{location}'
- Sites: {sites_list}
- Job Type: {job_type or 'All'}
- Remote Only: {is_remote}
- Results per Site: {results_wanted}
- Hours Old: {hours_old or 'Any time'}
- Distance: {distance} miles
- Country: {self.valves.default_country}

"""

        try:
            await self.emit_status(eventer, f"Initializing job search for '{search_term}'...")

            # Import jobspy here to avoid startup delays
            from jobspy import scrape_jobs

            await self.emit_status(eventer, f"Searching {len(sites_list)} job board(s)...")

            # Perform the job search
            jobs_df = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: scrape_jobs(
                    site_name=sites_list,
                    search_term=search_term,
                    location=location if location else None,
                    distance=distance,
                    is_remote=is_remote,
                    job_type=job_type if job_type else None,
                    results_wanted=results_wanted,
                    country_indeed=self.valves.default_country,
                    hours_old=hours_old,
                    description_format="markdown",
                    verbose=0,  # Suppress jobspy logs
                ),
            )

            await self.emit_status(eventer, "Processing results...")

            # Format the results
            search_params = {
                "search_term": search_term,
                "location": location or "N/A",
                "sites": ", ".join(sites_list),
            }
            results = _format_job_results(jobs_df, search_params)

            final_output = debug_info + results

            await self.emit_result(eventer, final_output)
            await self.emit_status(eventer, "Search complete", done=True)

            return final_output

        except ImportError:
            error_msg = "JobSpy library not installed. Please install it with: pip install python-jobspy pandas"
            await self.emit_error(eventer, error_msg)
            return debug_info + f"❌ {error_msg}"
        except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
            error_msg = f"Job search failed: {str(e)}"
            await self.emit_error(eventer, error_msg)
            return debug_info + f"❌ {error_msg}"
        except Exception as e:
            # Catch any unexpected errors
            error_msg = f"Unexpected error during job search: {str(e)}"
            await self.emit_error(eventer, error_msg)
            return debug_info + f"❌ {error_msg}"
