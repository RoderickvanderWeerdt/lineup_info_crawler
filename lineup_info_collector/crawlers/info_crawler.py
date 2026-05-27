import requests
from bs4 import BeautifulSoup, Tag
from unidecode import unidecode

from .. import constants
from .utils import extract_streaming_links

# def _find_info_url(artist: str) -> str:
#     """Finds the AllMusic URL for a given artist.

#     This function searches for an artist on AllMusic and returns the URL to their
#     main page.

#     Args:
#         artist (str): The name of the artist to search for.

#     Returns:
#         str | None: The AllMusic URL for the artist if found, otherwise None.

#     Raises:
#         ConnectionError: If the HTTP request to AllMusic fails.
#     """
#     try:
#         response = requests.get(
#             f"https://www.allmusic.com/search/artists/{artist}",
#             headers=constants.HEADERS,
#         )
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         raise ConnectionError(
#             f"Failed to fetch search results for {artist}: {e}"
#         ) from e

#     soup = BeautifulSoup(response.text, features="lxml")
#     artist_div = soup.find("div", {"class": "artist"})

#     if isinstance(artist_div, Tag) and artist_div.a and "href" in artist_div.a.attrs:
#         url = artist_div.a["href"]
#         if isinstance(url, str):
#             return url
#         elif isinstance(url, list):
#             return url[0]

#     print(f"INFO: No AllMusic URL found for {artist}")
#     return ""



def _find_info_url(artist):
    source_code = requests.get(
        "https://www.allmusic.com/search/artists/" + artist, headers=constants.HEADERS
    )
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features="lxml")

    for div in soup.findAll("div", {"class": "artist"}):
        tag = """<a href="""
        url = str(div)[str(div).find(tag) + len(tag) + 1 :]
        url = url[: url.find("""\"""")]
        return url

def _compare_names(line_up_name, info_name):
    line_up_name = unidecode(line_up_name.lower())
    info_name = unidecode(info_name.lower()).replace("&amp;", "&") #allmusic replaces & with &amp; (and so do LLM's apparently ;p)
    info_name = info_name[:info_name.find('(followed')-1]
    info_name = info_name[:info_name.find('(be one of')-1]
    print("info_name: '", info_name.strip(), "'")
    print("line_up_name: '", line_up_name, "'")
    if line_up_name == info_name.strip():
        return 1
    # else: #added else in case of unstripped line up name ##Removed else because it is too lacks
    #     return (' '+info_name.strip()).find(line_up_name) #offset ' ' so that when the line starts with the act name it will return 1 instead of 0


_EMPTY_STREAMING: dict[str, str] = {
    "spotify_url": "",
    "apple_music_url": "",
    "youtube_url": "",
}


def _get_info(
    act_name: str, info_url: str, act_url: str, verbose: bool
) -> dict[str, str]:
    """Fetches and parses artist information from an AllMusic URL.

    If a valid AllMusic URL is provided, this function scrapes the page for the
    artist's active years, genres, styles, and streaming links. It compares the
    found name with the act name to ensure correctness.

    Args:
        act_name (str): The name of the artist.
        info_url (str | None): The AllMusic URL for the artist. If None, default
            empty information is returned.
        act_url (str): The original URL for the act from the festival website.
        verbose (bool): If True, prints the scraped information.

    Returns:
        dict[str, str]: A dictionary containing the artist's information,
            including name, active dates, genres, styles, streaming URLs, and
            source URLs.

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
            **_EMPTY_STREAMING,
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
            **_EMPTY_STREAMING,
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

    streaming = extract_streaming_links(soup)

    if verbose:
        print(
            f"{act_name:<40} | {active_date:<13} | {';'.join(genres):<28} |{';'.join(styles)}"
        )
    return {
        "name": act_name,
        "activeDate": active_date,
        "genres": ";".join(genres),
        "styles": ";".join(styles),
        "act_url": act_url,
        "info_url": info_url,
        **streaming,
    }


def info_crawler(artists: list[dict[str, str]], verbose: bool) -> list[dict[str, str]]:
    """Enriches a list of artists with AllMusic metadata and streaming links.

    For each artist, looks up the AllMusic page to retrieve active dates,
    genres, styles, and any streaming URLs present on that page. Streaming
    links already collected by the lineup crawler (e.g. from the festival's
    own artist pages) are preserved when AllMusic does not have them.

    Args:
        artists: Artist dicts from the lineup crawler. Each must have a
            ``name`` key and a ``link`` key.
        verbose: If True, prints progress for each artist.

    Returns:
        Merged list of dicts with AllMusic metadata added. Streaming link
        keys (``spotify_url``, ``apple_music_url``, ``youtube_url``) are
        always present; empty string means not found.
    """
    all_info = []
    for artist in artists:
        info_url = _find_info_url(artist["name"])
        info = _get_info(artist["name"], info_url, artist.get("link", ""), verbose)
        merged = artist | info
        # Prefer any non-empty streaming link: festival pages (lineup crawler)
        # often have direct Spotify links that AllMusic may lack.
        for key in ("spotify_url", "apple_music_url", "youtube_url"):
            merged[key] = info.get(key) or artist.get(key, "")
        all_info.append(merged)
    return all_info
