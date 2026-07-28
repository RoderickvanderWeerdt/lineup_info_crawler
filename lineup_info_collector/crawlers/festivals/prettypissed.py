from bs4 import BeautifulSoup

from ...params import CrawlParams
from ..utils import _get_soup
from .registry import register


def parse_prettypissed(soup: BeautifulSoup) -> list[dict]:
    """Parse Pretty Pissed's lineup page HTML for artists."""
    artists = []
    for div in soup.find_all("a", attrs={"class": "styles_page-preview-medium__link__Biqrh"}):
        artists.append({"name": div.text.strip(), "link": "https://www.melkweg.nl" + str(div.attrs["href"])})
    return artists


@register("prettypissed", default_url="https://www.melkweg.nl/nl/agenda/pretty-pissed-24-05-2025/")
def crawl(params: CrawlParams) -> list[dict]:
    """Crawl Pretty Pissed's lineup page for artists."""
    return parse_prettypissed(_get_soup(params.url))
