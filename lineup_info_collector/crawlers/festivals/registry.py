from collections.abc import Callable
from dataclasses import dataclass, field

from ...params import CrawlParams

CrawlFn = Callable[[CrawlParams], list[dict]]

_DEFAULT_COLUMNS = ["name", "genres", "styles", "activeDate", "act_url", "info_url"]
COLUMNS_WITH_DAY = ["name", "genres", "styles", "activeDate", "day", "act_url", "info_url"]


@dataclass(frozen=True)
class _RegistryEntry:
    crawl: CrawlFn
    default_url: str
    default_columns: list[str] = field(default_factory=lambda: list(_DEFAULT_COLUMNS))


_REGISTRY: dict[str, _RegistryEntry] = {}


def register(key: str, *, default_url: str, default_columns: list[str] | None = None) -> Callable[[CrawlFn], CrawlFn]:
    """Register a festival's `crawl(params)` function under `key`, canonicalized lowercase."""

    def decorator(fn: CrawlFn) -> CrawlFn:
        _REGISTRY[key.lower()] = _RegistryEntry(
            crawl=fn,
            default_url=default_url,
            default_columns=_DEFAULT_COLUMNS if default_columns is None else default_columns,
        )
        return fn

    return decorator


def _get_entry(festival: str) -> _RegistryEntry:
    try:
        return _REGISTRY[festival.lower()]
    except KeyError:
        message = f"Unknown festival {festival}. Currently accepted are: {sorted(_REGISTRY)}"
        raise ValueError(message) from None


def get_crawler(festival: str) -> CrawlFn:
    """Look up the registered crawl function for `festival` (case-insensitive)."""
    return _get_entry(festival).crawl


def get_default_url(festival: str) -> str:
    """Look up `festival`'s registered default lineup URL (case-insensitive)."""
    return _get_entry(festival).default_url


def get_default_columns(festival: str) -> list[str]:
    """Look up `festival`'s registered default CSV columns (case-insensitive)."""
    return _get_entry(festival).default_columns
