from .artist_shape import _check_backup_styles
from .crawlers.info_crawler import info_crawler
from .crawlers.lineup_crawler import lineup_crawler
from .params import CrawlParams

__all__ = ["crawl_lineup_info", "info_crawler", "lineup_crawler"]


def _apply_backup_styles_fallback(all_info: list[dict]) -> list[dict]:
    """Apply the backup_styles fallback to every artist in a crawl's results."""
    return [_check_backup_styles(artist) for artist in all_info]


def crawl_lineup_info(params: CrawlParams, verbose: bool = False) -> list[dict]:
    """Crawl a festival's lineup and enrich each artist with AllMusic info."""
    artists = lineup_crawler(params)
    all_info = info_crawler(artists, verbose)
    return _apply_backup_styles_fallback(all_info)
