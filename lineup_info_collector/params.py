from dataclasses import dataclass


@dataclass(frozen=True)
class CrawlParams:
    """A single crawl invocation's festival, edition year, and lineup URL."""

    festival: str
    year: int
    url: str
