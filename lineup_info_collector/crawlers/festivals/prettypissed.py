from lineup_info_collector.crawlers.festivals.registry import register
from lineup_info_collector.crawlers.utils import _get_soup


@register("prettypissed")
def crawl(params: dict) -> list[dict]:
    """Crawl Pretty Pissed's lineup page for artists.

    Args:
        params: Crawl parameters; must include `"URL"`.

    Returns:
        A list of artist dicts with `name` and `link` keys.
    """
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.find_all("a", attrs={"class": "styles_page-preview-medium__link__Biqrh"}):
        artists.append({"name": div.text.strip(), "link": "https://www.melkweg.nl" + div.attrs["href"]})
    return artists
