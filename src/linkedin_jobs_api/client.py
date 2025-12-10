"""
Main client with reinforced anti-bot headers.
"""

from typing import Any, Optional

import requests

from .url_builder import build_search_url
from .parser import parse_jobs_html


def query(
    keyword: str = "",
    location: str = "",
    date_since_posted: Optional[str] = None,
    job_type: Optional[str] = None,
    remote_filter: Optional[str] = None,
    salary: Optional[str] = None,
    experience_level: Optional[str] = None,
    limit: str = "10",
    page: str = "0",
    sort_by: Optional[str] = None,
    has_verification: bool = False,
    under_10_applicants: bool = False,
) -> list[dict[str, Any]]:
    """Query LinkedIn Jobs API with comprehensive search parameters and anti-bot protection.

        This method performs a complete search operation by building the appropriate URL,
        making HTTP requests with reinforced anti-bot headers, and parsing the HTML response
        into normalized job objects. It handles pagination.

        Args:
            keyword (str, optional): Search keywords or job title. Defaults to "".
            location (str, optional): Geographic location for jobs. Defaults to "".
            date_since_posted (Optional[str], optional): Time frame for postings
                (e.g., "1", "7", "30" for days). Defaults to None.
            job_type (Optional[str], optional): Job type filter
                (e.g., "F", "C", "P", "T" for Full time, Contract, etc.). Defaults to None.
            remote_filter (Optional[str], optional): Remote work options
                (e.g., "1", "2", "3" for Remote, Hybrid, On-site). Defaults to None.
            salary (Optional[str], optional): Salary range filter. Defaults to None.
            experience_level (Optional[str], optional): Experience level
                (e.g., "1", "2", "3", "4", "5" for Internship to Executive). Defaults to None.
            limit (str, optional): Number of results per page. Defaults to "10" Max.
            page (str, optional): Results page number (0-indexed). Defaults to "0" Min 999 Max.
            sort_by (Optional[str], optional): Sort order
                (e.g., "R", "DD" for Relevant or Date Posted). Defaults to None.
            has_verification (bool, optional): Filter for verified companies. Defaults to False.
            under_10_applicants (bool, optional): Filter for jobs with under 10 applicants.
                Defaults to False.

        Returns:
            list[dict[str, Any]]: List of normalized job dictionaries with structure:
                - position: str - Job title
                - company: str - Company name
                - companyLogo: str - Company logo
                - location: str - Job location
                - jobUrl: str - Direct link to job posting
                - date_posted: str - Posting date in ISO format
                - salary: str - Salary range text
                - agoTime: str - Job ago time


        Example:
            >>> jobs = query(
            ...     keyword="python developer",
            ...     location="Remote",
            ...     limit="10",
            ...     remote_filter="remote"
            ... )
            >>> len(jobs)
            10
            >>> jobs[0]['title']
            'Senior Python Developer'
            >>> all('python' in job['title'].lower() for job in jobs)
            True
        """
    url = build_search_url(
        keyword=keyword,
        location=location,
        date_since_posted=date_since_posted,
        job_type=job_type,
        remote_filter=remote_filter,
        salary=salary,
        experience_level=experience_level,
        page=page,
        sort_by=sort_by,
        has_verification=has_verification,
        under_10_applicants=under_10_applicants,
    )

    # HEADERS
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.linkedin.com/jobs",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    # Session avec cookies persistants
    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, timeout=30)

        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}")
            return []

        jobs = parse_jobs_html(response.text)

        return jobs[: int(limit)]

    except requests.RequestException as e:
        print(f"🌐 Error network: {e}")
        return []
