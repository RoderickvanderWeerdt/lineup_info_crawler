from ...params import CrawlParams
from ..utils import _get_soup
from .registry import register


@register("prettypissed", default_url="https://www.melkweg.nl/nl/agenda/pretty-pissed-24-05-2025/")
def crawl(params: CrawlParams) -> list[dict]:
    """Crawl Pretty Pissed's lineup page for artists."""
    soup = _get_soup(params.url)
    artists = []
    for div in soup.find_all("a", attrs={"class": "styles_page-preview-medium__link__Biqrh"}):
        artists.append({"name": div.text.strip(), "link": "https://www.melkweg.nl" + div.attrs["href"]})
    return artists
