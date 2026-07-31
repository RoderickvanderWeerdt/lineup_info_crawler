from ...params import CrawlParams
from ..utils import _get_soup
from .registry import COLUMNS_WITH_DAY, register


@register(
    "pinkpop",
    default_url="https://www.pinkpop.nl/programma",
    default_columns=COLUMNS_WITH_DAY,
)
def crawl(params: CrawlParams) -> list[dict]:
    """Crawl Pinkpop's lineup page for artists."""
    soup = _get_soup(params.url)
    artists = []
    for div in soup.find_all("a", attrs={"data-day": ["friday", "saturday", "sunday"]}):
        text = div.text.strip()
        artist_name = text[text.find("juni") + len("juni") :]  # remove day from name
        artist_day = text.split(" ")[0]
        artists.append({"name": artist_name, "link": div.attrs["href"], "day": artist_day})
    return artists
