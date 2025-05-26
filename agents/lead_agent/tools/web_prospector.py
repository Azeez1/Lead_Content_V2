# agents/lead_agent/tools/web_prospector.py
import requests
from bs4 import BeautifulSoup


def prospect_website(url: str) -> dict:
    """
    Scrapes a given URL for potential lead information (e.g., contact details, company info).
    This is a very basic example. Real-world scraping is much more complex.
    Args:
        url: The URL of the website to scrape.
    Returns:
        A dictionary containing extracted information or an error message.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        emails_found = set()
        for link in soup.find_all('a', href=True):
            if link['href'].startswith('mailto:'):
                emails_found.add(link['href'][7:])

        title = soup.title.string if soup.title else "No title found"

        return {
            "url": url,
            "title": title.strip(),
            "emails": list(emails_found),
            "status": "success"
        }
    except requests.RequestException as e:
        return {"url": url, "error": str(e), "status": "failure"}
    except Exception as e:
        return {"url": url, "error": f"An unexpected error occurred: {str(e)}", "status": "failure"}
