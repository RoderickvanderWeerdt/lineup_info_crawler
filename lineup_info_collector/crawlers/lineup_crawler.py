from .festivals import get_crawler


def lineup_crawler(params: dict) -> list[dict]:
    """Crawl the lineup page for `params["FESTIVAL"]` and return its artists."""
    crawl = get_crawler(params["FESTIVAL"])
    return crawl(params)
