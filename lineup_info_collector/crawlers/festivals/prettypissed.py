from ..utils import _get_soup
from .registry import register


@register("prettypissed")
def crawl(params: dict) -> list[dict]:
    """Crawl Pretty Pissed's lineup page for artists."""
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.find_all("a", attrs={"class": "styles_page-preview-medium__link__Biqrh"}):
        artists.append({"name": div.text.strip(), "link": "https://www.melkweg.nl" + div.attrs["href"]})
    return artists
