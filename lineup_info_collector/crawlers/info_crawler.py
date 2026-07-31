import requests
from bs4 import BeautifulSoup, Tag
from unidecode import unidecode

from .. import constants


def _fetch_search_soup(artist: str) -> BeautifulSoup:
    """Fetch AllMusic's artist search results page as HTML."""
    source_code = requests.get("https://www.allmusic.com/search/artists/" + artist, headers=constants.HEADERS)
    return BeautifulSoup(source_code.text, features="lxml")


def _parse_info_url(soup: BeautifulSoup) -> str | None:
    """Parse AllMusic's search results HTML for the first matching artist's URL."""
    for div in soup.findAll("div", {"class": "artist"}):
        tag = """<a href="""
        url = str(div)[str(div).find(tag) + len(tag) + 1 :]
        return url[: url.find("""\"""")]
    return None


def _find_info_url(artist):
    return _parse_info_url(_fetch_search_soup(artist))


def _compare_names(line_up_name, info_name):
    line_up_name = unidecode(line_up_name.lower())
    info_name = unidecode(info_name.lower()).replace(
        "&amp;", "&"
    )  # allmusic replaces & with &amp; (and so do LLM's apparently ;p)
    info_name = info_name[: info_name.find("(followed") - 1]
    info_name = info_name[: info_name.find("(be one of") - 1]
    print("info_name: '", info_name.strip(), "'")
    print("line_up_name: '", line_up_name, "'")
    if line_up_name == info_name.strip():
        return 1
    # else: #added else in case of unstripped line up name ##Removed else because it is too lacks
    #     return (' '+info_name.strip()).find(line_up_name) #offset ' ' so that when the line starts with the act name it will return 1 instead of 0


def _fetch_info_soup(info_url: str) -> BeautifulSoup:
    """Fetch an AllMusic artist page as HTML."""
    try:
        response = requests.get(info_url, headers=constants.HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to fetch artist page at {info_url}: {e}") from e
    return BeautifulSoup(response.text, features="lxml")


def _parse_info(soup: BeautifulSoup) -> dict[str, str]:
    """Parse an AllMusic artist page HTML for name, active dates, genres, and styles."""
    name_tag = soup.find("h1", {"id": "artistName"})
    name = name_tag.text.strip() if isinstance(name_tag, Tag) else ""

    active_dates_tag = soup.find("div", {"class": "activeDates"})
    active_date = active_dates_tag.div.text.strip() if isinstance(active_dates_tag, Tag) else ""

    genres_tag = soup.find("div", {"class": "genre"})
    genres = [a.text for a in genres_tag.findAll("a")] if isinstance(genres_tag, Tag) else []

    styles_tag = soup.find("div", {"class": "styles"})
    styles = [a.text for a in styles_tag.findAll("a")] if isinstance(styles_tag, Tag) else []

    return {
        "name": name,
        "activeDate": active_date,
        "genres": ";".join(genres),
        "styles": ";".join(styles),
    }


def _get_info(act_name: str, info_url: str, act_url: str, verbose: bool) -> dict[str, str]:
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

    parsed = _parse_info(_fetch_info_soup(info_url))

    if not _compare_names(act_name, parsed["name"]):
        print(f"INFO: Found information for '{parsed['name']}' did not match act name '{act_name}'.")
        return {
            "name": act_name,
            "activeDate": ";",
            "genres": ";",
            "styles": ";",
            "act_url": act_url,
            "info_url": info_url,
        }

    if verbose:
        print(f"{act_name:<40} | {parsed['activeDate']:<13} | {parsed['genres']:<28} |{parsed['styles']}")
    return {
        "name": act_name,
        "activeDate": parsed["activeDate"],
        "genres": parsed["genres"],
        "styles": parsed["styles"],
        "act_url": act_url,
        "info_url": info_url,
    }


def info_crawler(artists, verbose):
    all_info = []
    for artist in artists:
        info_url = _find_info_url(artist["name"])
        all_info.append(artist | _get_info(artist["name"], info_url, artist["link"], verbose))
    return all_info
