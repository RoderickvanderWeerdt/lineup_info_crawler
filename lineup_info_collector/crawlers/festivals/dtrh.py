from ...params import CrawlParams
from ..utils import _get_soup
from .registry import register


@register("dtrh", default_url="https://downtherabbithole.nl/programma")
def crawl(params: CrawlParams) -> list[dict]:
    """Crawl Down The Rabbit Hole's lineup page for artists."""
    soup = _get_soup(params.url)
    artists = []
    for div in soup.find_all("a", attrs={"class": "group"}):
        artists.append({"name": div.attrs["title"], "link": div.attrs["href"]})
    return artists
