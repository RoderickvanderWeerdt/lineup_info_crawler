from lineup_info_collector.crawlers.festivals.registry import register
from lineup_info_collector.crawlers.utils import _get_soup


def _str_dayfinder(txt: str, day: str) -> str | int:
    """Return `day` if it occurs in `txt`, else 0.

    Args:
        txt: The text to search.
        day: The day name to look for.

    Returns:
        `day` if found in `txt`, otherwise `0`.
    """
    if txt.find(day) >= 0:
        return day
    return 0


def _str_weekend_dayfinder(txt: str) -> str | None:
    """Return whichever weekend day name occurs in `txt`, if any.

    Args:
        txt: The text to search.

    Returns:
        The matching day name (`"Friday"`, `"Saturday"`, or `"Sunday"`), or `None` if none match.
    """
    if _str_dayfinder(txt, "Friday"):
        return "Friday"
    if _str_dayfinder(txt, "Saturday"):
        return "Saturday"
    if _str_dayfinder(txt, "Sunday"):
        return "Sunday"
    return None


@register("BKS")
def crawl(params: dict) -> list[dict]:
    """Crawl Best Kept Secret's lineup page for artists.

    Args:
        params: Crawl parameters; must include `"URL"`.

    Returns:
        A list of artist dicts with `name`, `link`, `day`, and `backup_styles` keys.
    """
    soup = _get_soup(params["URL"])
    artists = []
    for div in soup.find_all("a", attrs={"class": "act"}):
        artists.append(
            {
                "name": div.figure.div.h3.text.strip(),
                "link": "https://www.bestkeptsecret.nl" + div.attrs["href"],
                "day": _str_weekend_dayfinder(div.text.strip()),
                "backup_styles": div.figure.div.span.text.strip(),
            }
        )
    return artists
