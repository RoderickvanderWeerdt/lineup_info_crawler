import requests
from bs4 import BeautifulSoup, Tag
from unidecode import unidecode

from lineup_info_collector import constants


def _find_info_url(artist: str) -> str:
    """Finds the AllMusic URL for a given artist.

    This function searches for an artist on AllMusic and returns the URL to their
    main page.

    Args:
        artist (str): The name of the artist to search for.

    Returns:
        str | None: The AllMusic URL for the artist if found, otherwise None.

    Raises:
        ConnectionError: If the HTTP request to AllMusic fails.
    """
    try:
        response = requests.get(
            f"https://www.allmusic.com/search/artists/{artist}",
            headers=constants.HEADERS,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(
            f"Failed to fetch search results for {artist}: {e}"
        ) from e

    soup = BeautifulSoup(response.text, features="lxml")
    artist_div = soup.find("div", {"class": "artist"})

    if isinstance(artist_div, Tag) and artist_div.a and "href" in artist_div.a.attrs:
        url = artist_div.a["href"]
        if isinstance(url, str):
            return url
        elif isinstance(url, list):
            return url[0]

    print(f"INFO: No AllMusic URL found for {artist}")
    return ""


def _compare_names(line_up_name: str, info_name: str) -> bool:
    """Compares two artist names for equality, ignoring case and accents.

    This function normalizes both names by converting them to lowercase and
    removing any accent marks before comparison.

    Args:
        line_up_name (str): The first artist name (e.g., from a lineup).
        info_name (str): The second artist name (e.g., from AllMusic).

    Returns:
        bool: True if the names match after normalization, False otherwise.
    """
    line_up_name = unidecode(line_up_name.lower())
    info_name = unidecode(info_name.lower()).replace("&amp;", "&") #allmusic replaces & with &amp; (and so do LLM's apparently ;p)
    if line_up_name == info_name:
        return 1
    else: #added else in case of unstripped line up name
        return (' '+info_name.strip()).find(line_up_name) #offset ' ' so that when the line starts with the act name it will return 1 instead of 0


def _get_info(
    act_name: str, info_url: str, act_url: str, verbose: bool
) -> dict[str, str]:
    """Fetches and parses artist information from an AllMusic URL.

    If a valid AllMusic URL is provided, this function scrapes the page for the
    artist's active years, genres, and styles. It compares the found name with
    the act name to ensure correctness.

    Args:
        act_name (str): The name of the artist.
        info_url (str | None): The AllMusic URL for the artist. If None, default
            empty information is returned.
        act_url (str): The original URL for the act from the festival website.
        verbose (bool): If True, prints the scraped information.

    Returns:
        dict[str, str]: A dictionary containing the artist's information,
            including name, active dates, genres, styles, and URLs.

    Raises:
        ConnectionError: If the HTTP request to the AllMusic artist page fails.
    """
    if not info_url:
        return {
            "name": act_name,
            "activeDate": ";",
            "genres": ";",
            "styles": ";",
            "act_url": act_url,
            "info_url": ";",
        }

    try:
        response = requests.get(info_url, headers=constants.HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to fetch artist page at {info_url}: {e}") from e

    soup = BeautifulSoup(response.text, features="lxml")

    name_tag = soup.find("h1", {"id": "artistName"})
    name = name_tag.text.strip() if isinstance(name_tag, Tag) else ""

    if not _compare_names(act_name, name):
        print(
            f"INFO: Found information for '{name}' did not match act name '{act_name}'."
        )
        return {
            "name": act_name,
            "activeDate": ";",
            "genres": ";",
            "styles": ";",
            "act_url": act_url,
            "info_url": info_url,
        }

    active_dates_tag = soup.find("div", {"class": "activeDates"})
    active_date = (
        active_dates_tag.div.text.strip() if isinstance(active_dates_tag, Tag) else ""
    )

    genres_tag = soup.find("div", {"class": "genre"})
    genres = (
        [a.text for a in genres_tag.findAll("a")] if isinstance(genres_tag, Tag) else []
    )

    styles_tag = soup.find("div", {"class": "styles"})
    styles = (
        [a.text for a in styles_tag.findAll("a")] if isinstance(styles_tag, Tag) else []
    )

    if verbose:
        print(
            f"{name:<40} | {active_date:<13} | {';'.join(genres):<28} |{';'.join(styles)}"
        )

    return {
        "name": act_name,
        "activeDate": active_date,
        "genres": ";".join(genres),
        "styles": ";".join(styles),
        "act_url": act_url,
        "info_url": info_url,
    }


def info_crawler(artists: list[dict[str, str]], verbose: bool) -> list[dict[str, str]]:
    """Crawls AllMusic for information about a list of artists.

    For each artist in the list, this function finds their AllMusic page,
    scrapes relevant information, and returns an updated list of artist
    dictionaries.

    Args:
        artists (list[dict[str, str]]): A list of artist dictionaries. Each
            dictionary should contain at least a "name" and "link" key.
        verbose (bool): If True, enables detailed logging during the crawling
            process.

    Returns:
        list[dict[str, str]]: A list of artist dictionaries, updated with
            information from AllMusic (activeDate, genres, styles, info_url).
    """
    all_info: list[dict[str, str]] = []
    for artist in artists:
        try:
            info_url = _find_info_url(artist["name"])
            artist_info = _get_info(artist["name"], info_url, artist["link"], verbose)
            all_info.append({**artist, **artist_info})
        except ConnectionError as e:
            print(f"ERROR: Could not process {artist['name']}. Reason: {e}")
    return all_info
