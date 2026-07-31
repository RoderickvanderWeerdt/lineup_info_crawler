from lineup_info_collector.crawlers.festivals.registry import register
from lineup_info_collector.crawlers.utils import _get_soup


def _get_lowlands_styles(url: str) -> str:
    """Fetch an act's Lowlands detail page and return its backup styles text.

    Args:
        url: The act's detail page URL.

    Returns:
        The act's backup styles text, or an empty string if the page didn't load.
    """
    soup = _get_soup(url)
    div = soup.find("h2", {"class": "act-detail__subtitle"})
    if div is None:
        print(f"Act url not working: {url}")
        return ""
    return div.text.strip()


@register("lowlands")
def crawl(params: dict) -> list[dict]:
    """Crawl Lowlands' lineup page for artists.

    Args:
        params: Crawl parameters; must include `"URL"`.

    Returns:
        A list of artist dicts with `name`, `link`, and `backup_styles` keys.
    """
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.find_all("a", attrs={"class": "act-list-card__button"}):  # changed to 2026 terminology
        href = "https://www.lowlands.nl" + div.attrs["href"]
        artists.append({"name": div.text.strip(), "link": href, "backup_styles": _get_lowlands_styles(href)})
    return artists
