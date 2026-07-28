from bs4 import BeautifulSoup, Tag

from ...params import CrawlParams
from ..utils import _get_soup
from .registry import COLUMNS_WITH_DAY, register


def _str_dayfinder(txt: str, day: str) -> str | int:
    """Return `day` if it occurs in `txt`, else 0."""
    if txt.find(day) >= 0:
        return day
    return 0


def _str_weekend_dayfinder(txt: str) -> str | None:
    """Return whichever weekend day name occurs in `txt`, if any."""
    if _str_dayfinder(txt, "Friday"):
        return "Friday"
    if _str_dayfinder(txt, "Saturday"):
        return "Saturday"
    if _str_dayfinder(txt, "Sunday"):
        return "Sunday"
    return None


def parse_bks(soup: BeautifulSoup) -> list[dict]:
    """Parse Best Kept Secret's lineup page HTML for artists."""
    artists = []
    for div in soup.find_all("a", attrs={"class": "act"}):
        name_tag = div.find("h3")
        name = name_tag.text.strip() if isinstance(name_tag, Tag) else ""
        styles_tag = div.find("span")
        backup_styles = styles_tag.text.strip() if isinstance(styles_tag, Tag) else ""
        artists.append(
            {
                "name": name,
                "link": "https://www.bestkeptsecret.nl" + str(div.attrs["href"]),
                "day": _str_weekend_dayfinder(div.text.strip()),
                "backup_styles": backup_styles,
            }
        )
    return artists


@register(
    "bks",
    default_url="https://www.bestkeptsecret.nl/program/list/",
    default_columns=COLUMNS_WITH_DAY,
)
def crawl(params: CrawlParams) -> list[dict]:
    """Crawl Best Kept Secret's lineup page for artists."""
    return parse_bks(_get_soup(params.url))
