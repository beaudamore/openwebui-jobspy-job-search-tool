# JobSpy Job Search Tool - Usage Guide

## Overview

The JobSpy Job Search Tool enables AI assistants to search for jobs across multiple job boards including LinkedIn, Indeed, ZipRecruiter, Glassdoor, Google, and more. It aggregates results from various sources and presents them in a clean, formatted manner.

**Version:** 1.0.0  
**Author:** Beau D'Amore (www.damore.ai)  
**Library Credit:** [python-jobspy](https://pypi.org/project/python-jobspy/)

---

## Requirements

Before using this tool, ensure the following Python packages are installed:

```bash
pip install python-jobspy pandas
```

---

## User Expectations

### What This Tool Does

- **Multi-Board Search**: Searches across multiple job boards simultaneously (LinkedIn, Indeed, ZipRecruiter, Glassdoor, Google, Bayt, Naukri, BDJobs)
- **Aggregated Results**: Combines results from all selected job boards into a single, unified view
- **Rich Job Details**: Provides comprehensive information including:
  - Job title and company
  - Location and remote status
  - Job type (full-time, part-time, contract, internship)
  - Salary range (when available)
  - Posting date
  - Job description preview
  - Direct link to job posting
- **Customizable Filters**: Filter by location, job type, remote status, recency, and distance
- **Smart Defaults**: Uses configured defaults for consistent searching behavior

### Expected Workflow

1. **User Request**: User asks the AI assistant to search for jobs (e.g., "Find me software engineering jobs in San Francisco")
2. **Tool Execution**: The tool searches the configured job boards with specified or default parameters
3. **Status Updates**: Real-time status updates show search progress
4. **Formatted Results**: Results are displayed with clear formatting, emoji indicators, and clickable links
5. **Debug Information** (optional): Shows the exact search parameters used

### Typical Use Cases

- **Job Discovery**: "Find data analyst jobs in New York"
- **Remote Work Search**: "Search for remote Python developer positions"
- **Location-Based**: "Show me marketing jobs within 25 miles of Chicago"
- **Recent Postings**: "Find engineering jobs posted in the last 24 hours"
- **Specific Job Types**: "Look for contract UX designer positions"
- **Multi-Criteria**: "Search for full-time remote data science jobs with salaries over $100k"

---

## Valve Configuration Options

Valves allow you to configure default behavior for the job search tool. These settings are used when specific parameters aren't provided in the search request.

### Available Valves

#### `default_sites`
- **Type**: String
- **Default**: `"linkedin,indeed,zip_recruiter"`
- **Description**: Comma-separated list of job sites to search
- **Options**: 
  - `linkedin` - LinkedIn Jobs
  - `indeed` - Indeed
  - `zip_recruiter` - ZipRecruiter
  - `glassdoor` - Glassdoor
  - `google` - Google Jobs
  - `bayt` - Bayt (Middle East)
  - `naukri` - Naukri (India)
  - `bdjobs` - BDJobs (Bangladesh)
- **Example**: `"linkedin,indeed,glassdoor,google"`

#### `default_location`
- **Type**: String
- **Default**: `""` (empty)
- **Description**: Default location for job searches
- **Format**: City, State or City, Country
- **Examples**: 
  - `"San Francisco, CA"`
  - `"New York, NY"`
  - `"London, UK"`
  - `"Remote"`
  - Leave empty for no location filter

#### `default_country`
- **Type**: String
- **Default**: `"USA"`
- **Description**: Default country for Indeed and Glassdoor searches
- **Options**: `"USA"`, `"Canada"`, `"UK"`, `"India"`, etc.
- **Note**: Country codes affect Indeed and Glassdoor search results

#### `default_distance`
- **Type**: Integer
- **Default**: `50`
- **Description**: Default search radius in miles from the specified location
- **Range**: 1-100 miles (typical)
- **Examples**: 
  - `10` - 10 miles
  - `25` - 25 miles
  - `50` - 50 miles

#### `default_results_wanted`
- **Type**: Integer
- **Default**: `15`
- **Description**: Number of job results to retrieve per job board
- **Range**: 1-50 (recommended)
- **Note**: Higher numbers may take longer to retrieve
- **Examples**:
  - `10` - Quick searches
  - `15` - Balanced
  - `30` - Comprehensive searches

#### `default_hours_old`
- **Type**: Integer
- **Default**: `72`
- **Description**: Filter for jobs posted within the last X hours
- **Special Values**: `0` = no time filter (any posting date)
- **Examples**:
  - `24` - Last 24 hours
  - `48` - Last 2 days
  - `72` - Last 3 days
  - `168` - Last week
  - `0` - Any time

#### `default_is_remote`
- **Type**: Boolean
- **Default**: `false`
- **Description**: Default filter for remote jobs only
- **Values**: 
  - `true` - Only show remote jobs
  - `false` - Show all jobs (remote and on-site)

#### `default_job_type`
- **Type**: String
- **Default**: `""` (empty - all types)
- **Description**: Default job type filter
- **Options**:
  - `"fulltime"` - Full-time positions
  - `"parttime"` - Part-time positions
  - `"internship"` - Internship positions
  - `"contract"` - Contract positions
  - `""` - All types (leave empty)

#### `enable_debug_output`
- **Type**: Boolean
- **Default**: `true`
- **Description**: Include debug information in search results
- **Values**:
  - `true` - Show search parameters and debug info
  - `false` - Hide debug information
- **Use Cases**: 
  - Enable for troubleshooting
  - Disable for cleaner output in production

---

## Method: `search_jobs()`

This is the **only method** the AI assistant should call to perform job searches.

### Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `search_term` | String | **Yes** | Job title or keywords to search for | `"software engineer"`, `"data analyst"` |
| `location` | String | No | Location to search in (overrides default) | `"San Francisco, CA"`, `"Remote"` |
| `site_name` | String | No | Comma-separated list of job sites (overrides default) | `"linkedin,indeed"` |
| `job_type` | String | No | Job type filter | `"fulltime"`, `"parttime"`, `"internship"`, `"contract"` |
| `is_remote` | Boolean | No | Remote job filter | `true`, `false` |
| `results_wanted` | Integer | No | Number of results per site | `10`, `20`, `30` |
| `hours_old` | Integer | No | Filter for recent postings (hours) | `24`, `48`, `72` |
| `distance` | Integer | No | Search radius in miles | `10`, `25`, `50` |

### Return Value

Returns a formatted string containing:
- Debug information (if enabled)
- Search summary (search term, location, sites searched, result count)
- Detailed job listings with:
  - Job title and company
  - Location
  - Site source
  - Job type
  - Salary information
  - Posting date
  - Remote status
  - Direct URL
  - Description preview

### Usage Examples

#### Basic Search (Uses All Defaults)
```python
search_jobs(search_term="python developer")
```

#### Search with Location
```python
search_jobs(
    search_term="data scientist",
    location="New York, NY"
)
```

#### Remote Jobs Only
```python
search_jobs(
    search_term="software engineer",
    is_remote=true
)
```

#### Recent Postings
```python
search_jobs(
    search_term="marketing manager",
    location="Chicago, IL",
    hours_old=24  # Last 24 hours only
)
```

#### Custom Job Boards
```python
search_jobs(
    search_term="UX designer",
    location="San Francisco, CA",
    site_name="linkedin,glassdoor,google"
)
```

#### Comprehensive Search
```python
search_jobs(
    search_term="full stack developer",
    location="Austin, TX",
    site_name="linkedin,indeed,zip_recruiter",
    job_type="fulltime",
    is_remote=false,
    results_wanted=20,
    hours_old=48,
    distance=25
)
```

---

## Configuration Recommendations

### For General Job Searching
```
default_sites: "linkedin,indeed,zip_recruiter"
default_location: ""
default_country: "USA"
default_distance: 50
default_results_wanted: 15
default_hours_old: 72
default_is_remote: false
default_job_type: ""
enable_debug_output: true
```

### For Remote-First Organizations
```
default_sites: "linkedin,indeed,zip_recruiter,google"
default_location: "Remote"
default_is_remote: true
default_results_wanted: 20
default_hours_old: 168
enable_debug_output: false
```

### For Local Hiring (Small Radius)
```
default_distance: 15
default_location: "Your City, ST"
default_results_wanted: 10
default_hours_old: 72
```

### For High-Volume Recruiting
```
default_sites: "linkedin,indeed,zip_recruiter,glassdoor,google"
default_results_wanted: 30
default_hours_old: 168
enable_debug_output: false
```

---

## Troubleshooting

### Common Issues

**Issue**: "JobSpy library not installed"
- **Solution**: Install required packages: `pip install python-jobspy pandas`

**Issue**: No results returned
- **Causes**: 
  - Search term too specific
  - Location too restrictive
  - `hours_old` filter too narrow
  - Job type filter excluding all results
- **Solution**: Broaden search criteria or use default values

**Issue**: Search takes too long
- **Causes**: 
  - Too many sites selected
  - `results_wanted` set too high
  - Network connectivity issues
- **Solution**: Reduce number of sites or results per site

**Issue**: Results not relevant
- **Causes**: 
  - Search term too broad
  - Location not specified
- **Solution**: Use more specific search terms and include location

---

## Best Practices

1. **Start Broad**: Begin with general search terms and narrow down if needed
2. **Use Location**: Always specify location when searching for on-site positions
3. **Balance Speed vs. Coverage**: More sites = more results but slower searches
4. **Recent Posts**: Use `hours_old` filter to find fresh opportunities
5. **Remote Clarity**: Explicitly set `is_remote=true` when searching remote jobs
6. **Debug Mode**: Keep `enable_debug_output=true` during initial setup and testing
7. **Site Selection**: Choose sites relevant to your industry (e.g., LinkedIn for tech, Indeed for general)
8. **Results Limit**: Use 10-20 results per site for best balance of speed and coverage

---

## Output Format

Results are formatted with emojis for easy scanning:
- 🔍 Search summary
- 🏢 Company name
- 📍 Location
- 🌐 Job site source
- 💼 Job type
- 💰 Salary information
- 📅 Posting date
- 🏠 Remote indicator
- 🔗 Direct URL
- 📝 Description preview

---

## Support

For issues or questions:
- **Tool Author**: Beau D'Amore - www.damore.ai
- **Library Documentation**: https://pypi.org/project/python-jobspy/
- **Library GitHub**: Check PyPI page for repository link

---

## Version History

- **v1.0.0** - Initial release with multi-board search, comprehensive filtering, and configurable defaults
