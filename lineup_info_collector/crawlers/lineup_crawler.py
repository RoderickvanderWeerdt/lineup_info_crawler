import requests
from bs4 import BeautifulSoup, Tag

from lineup_info_collector import constants


def _get_soup(url: str) -> BeautifulSoup:
    """Gets the soup from a given URL.

    Args:
        url: The URL to get the soup from.

    Returns:
        A BeautifulSoup object representing the parsed HTML of the page.

    Raises:
        ConnectionError: If the request to the URL fails.
    """
    try:
        response = requests.get(url, headers=constants.HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to get response from website {url}") from e
    return BeautifulSoup(response.text, "html.parser")


def _dtrh_crawler(params: dict[str, str]) -> list[dict[str, str]]:
    """Crawls the Down the Rabbit Hole website for artists.

    Args:
        params: A dictionary containing the URL of the festival.

    Returns:
        A list of dictionaries, where each dictionary represents an artist
        and contains the artist's name and a link to their page.

    Raises:
        ValueError: If no artist elements are found on the page.
    """
    soup = _get_soup(params["URL"])
    artists: list[dict[str, str]] = []
    artist_elements = soup.findAll("a", {"class": "group"})
    if not artist_elements:
        raise ValueError(
            "No artist elements found on DTRH page. HTML structure may have changed."
        )
    for div in artist_elements:
        if isinstance(div, Tag):
            artists.append({"name": div.attrs["title"], "link": div.attrs["href"]})
    return artists


def _pinkpop_crawler(params: dict[str, str]) -> list[dict[str, str]]:
    """Crawls the Pinkpop website for artists.

    Args:
        params: A dictionary containing the URL of the festival.

    Returns:
        A list of dictionaries, where each dictionary represents an artist
        and contains the artist's name, a link to their page, and the day
        they are performing.

    Raises:
        ValueError: If no artist elements are found on the page.
    """
    soup = _get_soup(params["URL"])
    artists: list[dict[str, str]] = []
    artist_elements = soup.findAll("a", {"data-day": ["friday", "saturday", "sunday"]})
    if not artist_elements:
        raise ValueError(
            "No artist elements found on Pinkpop page. HTML structure may have changed."
        )
    for div in artist_elements:
        if isinstance(div, Tag):
            artist_name = " ".join(div.text.strip().split(" ")[:-3])
            artist_day = div.text.strip().split(" ")[-3]
            artists.append(
                {"name": artist_name, "link": div.attrs["href"], "day": artist_day}
            )
    return artists


def _ooto_crawler(params: dict[str, str]) -> list[dict[str, str]]:
    """Crawls the Out of the Ordinary website for artists.

    Args:
        params: A dictionary containing the URL of the festival.

    Returns:
        A list of dictionaries, where each dictionary represents an artist
        and contains the artist's name and a placeholder link.

    Raises:
        ValueError: If no artist elements are found on the page.
    """
    soup = _get_soup(params["URL"])
    artists: list[dict[str, str]] = []
    artist_elements = soup.find_all("h3")
    if not artist_elements:
        raise ValueError(
            "No artist elements found on OOTO page. HTML structure may have changed."
        )
    for div in artist_elements:
        if isinstance(div, Tag):
            artists.append({"name": div.text.strip(), "link": "~"})
    return artists


def _prettypissed_crawler(params: dict[str, str]) -> list[dict[str, str]]:
    """Crawls the Pretty Pissed website for artists.

    Args:
        params: A dictionary containing the URL of the festival.

    Returns:
        A list of dictionaries, where each dictionary represents an artist
        and contains the artist's name and a link to their page.

    Raises:
        ValueError: If no artist elements are found on the page.
    """
    soup = _get_soup(params["URL"])
    artists: list[dict[str, str]] = []
    artist_elements = soup.findAll(
        "a", {"class": "styles_page-preview-medium__link__Biqrh"}
    )
    if not artist_elements:
        raise ValueError(
            "No artist elements found on Pretty Pissed page. HTML structure may have changed."
        )
    for div in artist_elements:
        if isinstance(div, Tag):
            artists.append(
                {
                    "name": div.text.strip(),
                    "link": "https://www.melkweg.nl" + div.attrs["href"],
                }
            )
    return artists


def _lowlands_crawler(params: dict[str, str]) -> list[dict[str, str]]:
    """Crawls the Lowlands website for artists.

    This function first collects all the act page URLs from the main lineup
    page and then visits each URL to get the artist's name.

    Args:
        params: A dictionary containing the URL of the festival.

    Returns:
        A list of dictionaries, where each dictionary represents an artist
        and contains the artist's name and a link to their page.

    Raises:
        ValueError: If no act pages are found on the main lineup page.
    """
    soup = _get_soup(params["URL"])
    urls: list[str] = []
    artists: list[dict[str, str]] = []
    # first collect all the act pages
    act_pages = soup.findAll("a", {"class": "act-list-item__button"})
    if not act_pages:
        raise ValueError(
            "No act pages found on Lowlands page. HTML structure may have changed."
        )
    for div in act_pages:
        if isinstance(div, Tag):
            urls.append("https://lowlands.nl" + div.attrs["href"])

    # now get the act names from each url page
    for url in urls:
        soup = _get_soup(url)
        div = soup.find("h1", {"class": "detail-header__heading--large"})
        if div is None:
            print(f"Act url not working: {url}")
            continue
        name = div.text.replace(",", ";")
        artists.append({"name": name, "link": url})
    return artists


def _get_lowlands_styles(url):
    soup = _get_soup(url)
    div = soup.find("h2", {"class": "act-detail__subtitle"})
    if div is None:
        print(f"Act url not working: {url}")
        return ""
    return div.text.strip()


def _lowlands_crawler2(params):
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.findAll("a", {"class": "act-list-item__button"}):
        href = "https://www.lowlands.nl" + div.attrs["href"]
        artists.append(
            {
                "name": div.text.strip(),
                "link": href,
                "backup_styles": _get_lowlands_styles(href),
            }
        )
    return artists


def lineup_crawler(params: dict[str, str]) -> list[dict[str, str]]:
    """Crawls the lineup for a given festival.

    This function acts as a dispatcher, calling the appropriate crawler based
    on the festival name provided in the params.

    Args:
        params: A dictionary containing the festival name and other parameters.

    Returns:
        A list of dictionaries, where each dictionary represents an artist.

    Raises:
        ValueError: If the festival name is unknown.
    """
    festival_name = params.get("FESTIVAL")
    if festival_name == "DTRH":
        return _dtrh_crawler(params)
    if festival_name == "lowlands":
        return _lowlands_crawler(params)
    if festival_name == "pinkpop":
        return _pinkpop_crawler(params)
    if festival_name == "ooto":
        return _ooto_crawler(params)
    if festival_name == "prettypissed":
        return _prettypissed_crawler(params)
    raise ValueError(
        f"Unknown festival {festival_name}. "
        "Currently accepted are: ['DTRH', 'lowlands', 'pinkpop', 'ooto', 'prettypissed']"
    )
