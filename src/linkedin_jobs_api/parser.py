"""
LinkedIn Jobs HTML parser -> normalized Job objects.
"""

from typing import Any
from selectolax.parser import HTMLParser


def parse_jobs_html(html: str) -> list[dict[str, Any]]:
    """ Parse LinkedIn Jobs HTML content into normalized job objects.

        This function extracts job listings from LinkedIn's HTML response and
        converts them into a standardized dictionary format structure.

        Args:
            html (str): Raw HTML content from LinkedIn Jobs search results

        Returns:
            list[dict[str, Any]]: List of normalized job dictionaries with keys:
                                - position: str - Job title
                                -  company: str - Company name
                                -  companyLogo: str - Company logo
                                -  location: str - Job location
                                -  jobUrl: str - Direct link to job posting
                                -  date: str - Posting date in ISO format
                                - salary: str - Job salary
                            - agoTime: str - Job ago time"""
    parser = HTMLParser(html)
    jobs = []

    # $("li")
    job_cards = parser.css("li")

    for card in job_cards:
        try:
            # SELECTORS
            position = card.css_first(".base-search-card__title")
            company = card.css_first(".base-search-card__subtitle")

            if not position or not company:  #  check
                continue

            position = position.text().strip()
            company = company.text().strip()


            location = (
                card.css_first(".job-search-card__location").text().strip()
                if card.css_first(".job-search-card__location")
                else ""
            )
            date_elem = card.css_first("time")
            date = date_elem.attributes.get("datetime", "") if date_elem else ""
            salary_elem = card.css_first(".job-search-card__salary-info")
            salary = (
                salary_elem.text().strip().replace("\n", " ") if salary_elem else ""
            )
            job_url_elem = card.css_first(".base-card__full-link")
            job_url = job_url_elem.attributes.get("href", "") if job_url_elem else ""
            logo_elem = card.css_first(".artdeco-entity-image")
            company_logo = (
                logo_elem.attributes.get("data-delayed-url", "") if logo_elem else ""
            )
            ago_time = (
                card.css_first(".job-search-card__listdate--new, .job-search-card__listdate").text().strip()
                if card.css_first(".job-search-card__listdate--new, .job-search-card__listdate")
                else ""
            )

            jobs.append(
                {
                    "position": position,
                    "company": company,
                    "companyLogo": company_logo,
                    "location": location,
                    "date": date,
                    "agoTime": ago_time,
                    "salary": salary or "Not specified",
                    "jobUrl": job_url,
                }
            )

        except Exception:
            continue

    return jobs
