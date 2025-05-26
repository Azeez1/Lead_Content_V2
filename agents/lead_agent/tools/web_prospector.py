"""Simple website prospector used by the lead agent."""

import requests
from bs4 import BeautifulSoup


def prospect_website(url: str) -> dict:
    """Extract basic lead information from a website.

    Parameters
    ----------
    url:
        The HTTP or HTTPS URL to inspect.

    Returns
    -------
    dict
        Dictionary containing the web page title and any e-mail addresses
        discovered.  The dict always contains ``status`` which is ``"success"``
        when scraping succeeds or ``"failure"`` otherwise.
    """

    try:
        # ------------------------------------------------------------------
        # Fetch the page and parse it
        # ------------------------------------------------------------------
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for non-200 responses
        soup = BeautifulSoup(response.content, "html.parser")

        # ------------------------------------------------------------------
        # Gather all email addresses from "mailto:" links
        # ------------------------------------------------------------------
        emails_found: set[str] = set()
        for link in soup.find_all("a", href=True):
            if link["href"].startswith("mailto:"):
                emails_found.add(link["href"][7:])  # strip the mailto: prefix

        # Page title is useful for context about the company
        title = soup.title.string if soup.title else "No title found"

        return {
            "url": url,
            "title": title.strip(),
            "emails": list(emails_found),
            "status": "success",
        }
    except requests.RequestException as e:
        # Network-related or HTTP errors are captured here
        return {"url": url, "error": str(e), "status": "failure"}
    except Exception as e:  # pragma: no cover - catch unexpected parsing errors
        return {
            "url": url,
            "error": f"An unexpected error occurred: {str(e)}",
            "status": "failure",
        }

