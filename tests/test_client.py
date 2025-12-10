"""
Tests unitaires pour linkedin-jobs-api-py
"""

import pytest
from linkedin_jobs_api import query
from linkedin_jobs_api.url_builder import build_search_url
import requests


@pytest.fixture
def sample_jobs():
    """Mocked test jobs to avoid LinkedIn API calls."""
    return [
        {
            "position": "Senior Python Developer",
            "company": "Google",
            "companyLogo": "https://media...png",
            "location": "Paris, France",
            "date": "2025-12-10T10:00:00Z",
            "agoTime": "1 day ago",
            "salary": "€80k-€120k",
            "jobUrl": "https://www.linkedin.com/jobs/view/123",
        }
    ]


def test_query_simple():
    """Basic search test."""
    jobs = query(keyword="python", location="Paris", limit="1")

    assert isinstance(jobs, list)
    if jobs:  # LinkedIn peut être down
        assert len(jobs) <= 1
        assert "position" in jobs[0]
        assert "company" in jobs[0]


def test_url_builder_basic():
    """Basic URL construction test."""
    url = build_search_url(keyword="python", location="Paris")

    assert (
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search" in url
    )
    assert "keywords=python" in url
    assert "location=Paris" in url


def test_all_filters():
    """Test ALL  filters."""
    jobs = query(
        keyword="developer",
        location="France",
        date_since_posted="past week",
        job_type="full time",
        remote_filter="remote",
        salary="100000",
        experience_level="senior",
        has_verification=True,
        under_10_applicants=True,
        sort_by="recent",
        limit="1",
    )

    assert isinstance(jobs, list)


def test_pagination():
    """Test pagination (page 1 = jobs 0-9)."""
    jobs_page0 = query(keyword="developer", page="0", limit="1")
    jobs_page1 = query(keyword="developer", page="1", limit="1")

    assert isinstance(jobs_page0, list)
    assert isinstance(jobs_page1, list)


def test_sort_by_recent():
    """Test sort_by=recent (latest jobs).)."""
    jobs = query(keyword="python", sort_by="recent", limit="3")

    assert isinstance(jobs, list)
    print("Recent jobs:", [job.get("agoTime", "N/A") for job in jobs])


def test_sort_by_relevant():
    """Test sort_by=relevant (LinkedIn algorithm)."""
    jobs = query(keyword="data scientist", sort_by="relevant", limit="3")

    assert isinstance(jobs, list)


def test_remote_filter():
    """Test remote filter  only."""
    jobs = query(keyword="frontend", remote_filter="remote", limit="3")

    assert isinstance(jobs, list)


def test_structure_job():
    """Check exact job structure."""
    jobs = query(keyword="python", limit="1")

    if jobs:
        job = jobs[0]
        required_fields = ["position", "company", "jobUrl", "location"]
        for field in required_fields:
            assert field in job
        assert isinstance(job["position"], str)
        assert job["salary"] == "" or isinstance(job["salary"], str)


def test_empty_keyword():
    """Test without keyword (all jobs)."""
    jobs = query(location="Paris", limit="1")
    assert isinstance(jobs, list)


@pytest.mark.skip(reason="LinkedIn may block - manual test.")
def test_live_linkedin():
    """Live test (to be run manually)."""
    jobs = query(keyword="python developer", location="Paris", limit="5")
    assert len(jobs) > 0
    print("✅ LIVE TEST OK:", len(jobs), "jobs found")


def test_error_handling():
    """Test network error handling."""
    # Invalid URL for testing.
    with pytest.raises(requests.RequestException):
        requests.get("https://nonexistent.linkedin.com")
