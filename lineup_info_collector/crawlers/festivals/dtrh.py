from bs4 import BeautifulSoup

from ...params import CrawlParams
from ..utils import _get_soup
from .registry import register


def parse_dtrh(soup: BeautifulSoup) -> list[dict]:
    """Parse Down The Rabbit Hole's lineup page HTML for artists."""
    artists = []
    for div in soup.find_all("a", attrs={"class": "group"}):
        artists.append({"name": div.attrs["title"], "link": div.attrs["href"]})
    return artists


@register("dtrh", default_url="https://downtherabbithole.nl/programma")
def crawl(params: CrawlParams) -> list[dict]:
    """Crawl Down The Rabbit Hole's lineup page for artists."""
    return parse_dtrh(_get_soup(params.url))
