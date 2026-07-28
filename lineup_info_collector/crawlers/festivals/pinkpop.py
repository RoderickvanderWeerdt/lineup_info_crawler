from ..utils import _get_soup
from .registry import register


@register("pinkpop")
def crawl(params: dict) -> list[dict]:
    """Crawl Pinkpop's lineup page for artists."""
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.find_all("a", attrs={"data-day": ["friday", "saturday", "sunday"]}):
        text = div.text.strip()
        artist_name = text[text.find("juni") + len("juni") :]  # remove day from name
        artist_day = text.split(" ")[0]
        artists.append({"name": artist_name, "link": div.attrs["href"], "day": artist_day})
    return artists
