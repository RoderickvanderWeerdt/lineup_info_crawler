from ..utils import _get_soup
from .registry import register


@register("DTRH")
def crawl(params: dict) -> list[dict]:
    """Crawl Down The Rabbit Hole's lineup page for artists."""
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.find_all("a", attrs={"class": "group"}):
        artists.append({"name": div.attrs["title"], "link": div.attrs["href"]})
    return artists
