import json

from bs4 import BeautifulSoup

from ...params import CrawlParams
from ..devalue import unflatten
from ..utils import _get_soup
from .registry import register

_NUXT_DATA_SCRIPT_ID = "__NUXT_DATA__"


def parse_lowlands_style(soup: BeautifulSoup) -> str:
    """Parse a Lowlands act detail page HTML for its backup styles text."""
    div = soup.find("h2", {"class": "act-detail__subtitle"})
    return div.text.strip() if div is not None else ""


def _get_lowlands_styles(url: str) -> str:
    """Fetch an act's Lowlands detail page and return its backup styles text."""
    styles = parse_lowlands_style(_get_soup(url))
    if not styles:
        print(f"Act url not working: {url}")
    return styles


def parse_lowlands(soup: BeautifulSoup) -> list[dict]:
    """Parse Lowlands' lineup page HTML for artists (without per-act backup styles)."""
    artists = []
    for div in soup.find_all("a", attrs={"class": "act-list-card__button"}):  # changed to 2026 terminology
        href = "https://www.lowlands.nl" + str(div.attrs["href"])
        artists.append({"name": div.text.strip(), "link": href})
    return artists


def _find_act_entries(node: object, found: list[dict]) -> None:
    """Recursively collect dict nodes that look like an act (have `url` and `category`).

    The acts page embeds its data as a Nuxt payload whose exact top-level shape
    (which fetch keys hold headliners vs. regular acts) is an implementation
    detail that can shift between deploys, so we search for the act shape
    itself instead of hardcoding a path to it.
    """
    if isinstance(node, dict):
        if "url" in node and "category" in node:
            found.append(node)
            return
        for value in node.values():
            _find_act_entries(value, found)
    elif isinstance(node, list):
        for item in node:
            _find_act_entries(item, found)


def parse_lowlands_categories(soup: BeautifulSoup) -> dict[str, dict[str, str]]:
    """Parse Lowlands' embedded Nuxt payload for each act's program category and genres.

    Args:
        soup: The parsed acts page HTML (same page `parse_lowlands` reads).

    Returns:
        A mapping from act URL path (e.g. `"/acts/foo-fighters/"`) to
        `{"category": <title>, "genres": <comma-joined genre titles>}`. Acts
        without a resolvable category are omitted; an empty dict is returned
        if the payload script is missing or unparseable.
    """
    script = soup.find("script", id=_NUXT_DATA_SCRIPT_ID)
    if script is None or not script.string:
        return {}

    try:
        root = unflatten(json.loads(script.string))
    except (json.JSONDecodeError, IndexError, KeyError, TypeError):
        return {}

    entries: list[dict] = []
    _find_act_entries(root, entries)

    categories: dict[str, dict[str, str]] = {}
    for entry in entries:
        url = entry.get("url")
        category = entry.get("category")
        if not url or not isinstance(category, dict):
            continue
        title = category.get("title")
        if not title:
            continue
        genres = entry.get("genres") or []
        genre_names = ", ".join(genre["title"] for genre in genres if isinstance(genre, dict) and genre.get("title"))
        categories[url] = {"category": title, "genres": genre_names}
    return categories


@register("lowlands", default_url="https://lowlands.nl/acts/")
def crawl(params: CrawlParams) -> list[dict]:
    """Crawl Lowlands' lineup page for artists.

    Enriches each artist with its backup styles and program category/genres.
    """
    soup = _get_soup(params.url)
    artists = parse_lowlands(soup)
    categories = parse_lowlands_categories(soup)
    for artist in artists:
        artist["backup_styles"] = _get_lowlands_styles(artist["link"])
        act_path = artist["link"].removeprefix("https://www.lowlands.nl")
        info = categories.get(act_path, {})
        artist["program_group"] = info.get("category", "")
        artist["festival_genre"] = info.get("genres", "")
    return artists
