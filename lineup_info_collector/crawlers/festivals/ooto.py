from ...params import CrawlParams
from ..utils import _get_soup
from .registry import register


@register("ooto", default_url="https://outoftheordinary-festival.nl/programma/")
def crawl(params: CrawlParams) -> list[dict]:
    """Crawl Out of the Ordinary's lineup page for artists."""
    soup = _get_soup(params.url)
    artists = []
    for div in soup.find_all("h3"):
        artists.append({"name": div.text.strip(), "link": "~"})
    return artists
