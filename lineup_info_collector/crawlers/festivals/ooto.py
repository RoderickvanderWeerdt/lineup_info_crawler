from bs4 import BeautifulSoup

from ...params import CrawlParams
from ..utils import _get_soup
from .registry import register


def parse_ooto(soup: BeautifulSoup) -> list[dict]:
    """Parse Out of the Ordinary's lineup page HTML for artists."""
    artists = []
    for div in soup.find_all("h3"):
        artists.append({"name": div.text.strip(), "link": "~"})
    return artists


@register("ooto", default_url="https://outoftheordinary-festival.nl/programma/")
def crawl(params: CrawlParams) -> list[dict]:
    """Crawl Out of the Ordinary's lineup page for artists."""
    return parse_ooto(_get_soup(params.url))
