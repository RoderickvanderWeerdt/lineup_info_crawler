from lineup_info_collector.crawlers.festivals.registry import register
from lineup_info_collector.crawlers.utils import _get_soup


@register("pinkpop")
def crawl(params: dict) -> list[dict]:
    """Crawl Pinkpop's lineup page for artists.

    Args:
        params: Crawl parameters; must include `"URL"`.

    Returns:
        A list of artist dicts with `name`, `link`, and `day` keys.
    """
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.find_all("a", attrs={"data-day": ["friday", "saturday", "sunday"]}):
        text = div.text.strip()
        artist_name = text[text.find("juni") + len("juni") :]  # remove day from name
        artist_day = text.split(" ")[0]
        artists.append({"name": artist_name, "link": div.attrs["href"], "day": artist_day})
    return artists
