from ..utils import _get_soup
from .registry import register


def _get_lowlands_styles(url: str) -> str:
    """Fetch an act's Lowlands detail page and return its backup styles text."""
    soup = _get_soup(url)
    div = soup.find("h2", {"class": "act-detail__subtitle"})
    if div is None:
        print(f"Act url not working: {url}")
        return ""
    return div.text.strip()


@register("lowlands")
def crawl(params: dict) -> list[dict]:
    """Crawl Lowlands' lineup page for artists."""
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.find_all("a", attrs={"class": "act-list-card__button"}):  # changed to 2026 terminology
        href = "https://www.lowlands.nl" + div.attrs["href"]
        artists.append({"name": div.text.strip(), "link": href, "backup_styles": _get_lowlands_styles(href)})
    return artists
