from ..params import CrawlParams
from .festivals import get_crawler


def lineup_crawler(params: CrawlParams) -> list[dict]:
    """Crawl the lineup page for `params.festival` and return its artists."""
    crawl = get_crawler(params.festival)
    return crawl(params)
