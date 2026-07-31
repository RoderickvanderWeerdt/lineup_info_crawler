from bs4 import BeautifulSoup
import requests

from lineup_info_collector import constants


def _get_soup(url: str):
    """Fetch a URL and parse the response body as HTML.

    Args:
        url: The URL to fetch.

    Returns:
        A `BeautifulSoup` object parsed from the response body.

    Raises:
        SystemExit: If the request fails.
    """
    try:
        response = requests.get(url, headers=constants.HEADERS)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(f"ERROR: failed to get response from website {url}")
        raise SystemExit(e)
    return BeautifulSoup(response.text, "html.parser")
