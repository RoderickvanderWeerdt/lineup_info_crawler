from ..params import CrawlParams
from .festivals import get_crawler


def _ensure_default_keys(artists: list[dict]) -> list[dict]:
    """Ensure every artist dict has `day` and `backup_styles`, defaulting when absent."""
    for artist in artists:
        artist.setdefault("day", None)
        artist.setdefault("backup_styles", "")
    return artists


def lineup_crawler(params: CrawlParams) -> list[dict]:
    """Crawl the lineup page for `params.festival` and return its artists."""
    crawl = get_crawler(params.festival)
    return _ensure_default_keys(crawl(params))
