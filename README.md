# OpenWebUI JobSpy Job Search Tool

Multi-board job search tool for OpenWebUI that aggregates listings from LinkedIn, Indeed, ZipRecruiter, Glassdoor, Google, and more.

**Version:** 1.0.0  
**Author:** Beau D'Amore ([www.damore.ai](https://www.damore.ai))  
**Library Credit:** [python-jobspy](https://pypi.org/project/python-jobspy/)

## Features

- **Multi-Board Search**: Simultaneously search across 8+ job boards:
  - LinkedIn Jobs
  - Indeed
  - ZipRecruiter
  - Glassdoor
  - Google Jobs
  - Bayt (Middle East)
  - Naukri (India)
  - BDJobs (Bangladesh)

- **Rich Job Details**: 
  - Job title, company, and location
  - Remote status and job type (full-time, part-time, contract, internship)
  - Salary ranges (when available)
  - Posting dates
  - Job description previews
  - Direct links to applications

- **Smart Filtering**:
  - Location-based search with distance radius
  - Job type filters
  - Remote work options
  - Recency filters (last 24 hours, week, month)
  - Salary range filters

- **Intelligent Defaults**: Configure site preferences, default locations, and search parameters

- **Formatted Results**: Clean, emoji-enhanced output with clickable links and organized information

## Installation

### Requirements

```bash
pip install python-jobspy pandas
```

### Setup in OpenWebUI

1. Upload `tool/jobspy_search_tool.py` to OpenWebUI
2. Configure the valves (optional) for your preferred defaults:
   - Default job sites
   - Default location and country
   - Search radius
   - Results limit

## Usage

### Basic Examples

```
"Find software engineering jobs in San Francisco"
"Search for remote Python developer positions"
"Show me marketing jobs within 25 miles of Chicago"
"Find engineering jobs posted in the last 24 hours"
"Look for contract UX designer positions"
```

### Configuration (Valves)

- **default_sites**: Comma-separated list of job boards (default: `linkedin,indeed,zip_recruiter`)
- **default_location**: Default search location (e.g., `San Francisco, CA`)
- **default_country**: Country code for Indeed/Glassdoor (default: `USA`)
- **default_distance**: Search radius in miles (default: 50)
- **default_results_wanted**: Maximum results per board (default: 10)
- **default_hours_old**: Maximum age of listings (default: 720 hours/30 days)
- **enable_debug**: Show search parameters in results

See [docs/USAGE.md](docs/USAGE.md) for complete configuration options and detailed usage guide.

## Documentation

- [Complete Usage Guide](docs/USAGE.md)
- [System Prompt](prompt/jobspy-prompt.md)

## License

MIT License - See individual repository for details

## Author

**Beau D'Amore**  
[www.damore.ai](https://www.damore.ai)
