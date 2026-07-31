from lineup_info_collector.crawlers.festivals.registry import register
from lineup_info_collector.crawlers.utils import _get_soup


@register("DTRH")
def crawl(params: dict) -> list[dict]:
    """Crawl Down The Rabbit Hole's lineup page for artists.

    Args:
        params: Crawl parameters; must include `"URL"`.

    Returns:
        A list of artist dicts with `name` and `link` keys.
    """
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.find_all("a", attrs={"class": "group"}):
        artists.append({"name": div.attrs["title"], "link": div.attrs["href"]})
    return artists
