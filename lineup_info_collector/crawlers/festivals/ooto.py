from ..utils import _get_soup
from .registry import register


@register("ooto")
def crawl(params: dict) -> list[dict]:
    """Crawl Out of the Ordinary's lineup page for artists."""
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.find_all("h3"):
        artists.append({"name": div.text.strip(), "link": "~"})
    return artists
