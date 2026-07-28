from .crawlers.info_crawler import info_crawler
from .crawlers.lineup_crawler import lineup_crawler
from .params import CrawlParams

__all__ = ["crawl_lineup_info", "info_crawler", "lineup_crawler"]


def crawl_lineup_info(params: CrawlParams, verbose: bool = False) -> list[dict]:
    """Crawl a festival's lineup and enrich each artist with AllMusic info."""
    artists = lineup_crawler(params)
    return info_crawler(artists, verbose)
