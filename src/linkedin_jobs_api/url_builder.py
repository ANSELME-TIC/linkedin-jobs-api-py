"""
Construction of LinkedIn Jobs search URLs with all filters.
"""

from typing import Optional
from urllib.parse import urlencode


def build_search_url(
    keyword: str = "",
    location: str = "",
    date_since_posted: Optional[str] = None,
    job_type: Optional[str] = None,
    remote_filter: Optional[str] = None,
    salary: Optional[str] = None,
    experience_level: Optional[str] = None,
    page: str = "0",
    sort_by: Optional[str] = None,
    has_verification: bool = False,
    under_10_applicants: bool = False,
) -> str:
    """Build a LinkedIn Jobs search URL with comprehensive filtering options.

        Constructs a complete LinkedIn Jobs search URL by combining base parameters
        with optional filters for date, job type, remote work, salary, experience level,
        and other advanced search criteria.

        Args:
            keyword (str, optional): Search keywords or job title. Defaults to "".
            location (str, optional): Geographic location for jobs. Defaults to "".
            date_since_posted (Optional[str], optional): Time frame for postings
                (e.g., "1hr", "24hr", "past week", "past month"). Defaults to None.
            job_type (Optional[str], optional): Job type filter
                (e.g., "F", "C", "P", "T" for Full time, Contract,Part time etc.). Defaults to None.
            remote_filter (Optional[str], optional): Remote work options
                (e.g., "1", "2", "3" for On-site, Hybrid,Remote ). Defaults to None.
            salary (Optional[str], optional): Salary range filter. Defaults to None.
            experience_level (Optional[str], optional): Experience level
                (e.g., "1", "2", "3", "4", "5" for Internship to Executive). Defaults to None.
            page (str, optional): Results page number (0-indexed). Defaults to "0".
            sort_by (Optional[str], optional): Sort order
                (e.g., "R", "DD" for Relevant or Date Posted). Defaults to None.
            has_verification (bool, optional): Filter for verified companies. Defaults to False.
            under_10_applicants (bool, optional): Filter for jobs with under 10 applicants.
                Defaults to False.

        Returns:
            str: Complete LinkedIn Jobs search URL with all specified parameters.

        """

    params = {}

    if keyword:
        params["keywords"] = keyword.replace(" ", "+")
    if location:
        params["location"] = location.replace(" ", "+")
    if date_since_posted:
        params["f_TPR"] = _map_date_since_posted(date_since_posted)
    if salary:
        params["f_SB2"] = _map_salary(salary)
    if experience_level:
        params["f_E"] = _map_experience_level(experience_level)
    if remote_filter:
        params["f_WT"] = _map_remote_filter(remote_filter)
    if job_type:
        params["f_JT"] = _map_job_type(job_type)
    if has_verification:
        params["f_VJ"] = "true"
    if under_10_applicants:
        params["f_EA"] = "true"

    params["start"] = str(int(page) * 10)

    if sort_by == "recent":
        params["sortBy"] = "DD"
    elif sort_by == "relevant":
        params["sortBy"] = "R"

    query_string = urlencode(params)
    return f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{query_string}"


# MAPPINGS
def _map_date_since_posted(value):
    return {
        "1hr": "r3600",
        "24hr": "r86400",
        "past week": "r604800",
        "past month": "r2592000",
    }.get(value)


def _map_salary(value):
    return {"40000": "1", "60000": "2", "80000": "3", "100000": "4", "120000": "5"}.get(
        value
    )


def _map_experience_level(value):
    return {
        "internship": "1",
        "entry level": "2",
        "associate": "3",
        "senior": "4",
        "director": "5",
        "executive": "6",
    }.get(value.lower())


def _map_remote_filter(value):
    return {"on site": "1", "remote": "2", "hybrid": "3"}.get(value.lower())


def _map_job_type(value):
    return {
        "full time": "F",
        "part time": "P",
        "contract": "C",
        "temporary": "T",
        "internship": "I",
        "volunteer": "V",
    }.get(value.lower())
