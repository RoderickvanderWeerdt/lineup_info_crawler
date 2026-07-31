from dataclasses import dataclass


@dataclass(frozen=True)
class CrawlParams:
    """A single crawl invocation's festival, edition year, and lineup URL."""

    festival: str
    year: int
    url: str

    def __post_init__(self) -> None:
        """Canonicalize `festival` to lowercase so dispatch stays case-insensitive."""
        object.__setattr__(self, "festival", self.festival.lower())
