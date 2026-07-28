from bs4 import BeautifulSoup

from ...params import CrawlParams
from ..utils import _get_soup
from .registry import register


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


@register("lowlands", default_url="https://lowlands.nl/acts/")
def crawl(params: CrawlParams) -> list[dict]:
    """Crawl Lowlands' lineup page for artists, enriching each with its backup styles."""
    artists = parse_lowlands(_get_soup(params.url))
    for artist in artists:
        artist["backup_styles"] = _get_lowlands_styles(artist["link"])
    return artists
