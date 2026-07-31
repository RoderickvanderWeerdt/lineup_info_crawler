from collections.abc import Callable

CrawlFn = Callable[[dict], list[dict]]

_REGISTRY: dict[str, CrawlFn] = {}


def register(key: str) -> Callable[[CrawlFn], CrawlFn]:
    """Register a festival's `crawl(params)` function under `key`.

    Args:
        key: The festival's dispatch key, as used in `params["FESTIVAL"]`.

    Returns:
        A decorator that registers the wrapped function and returns it unchanged.
    """

    def decorator(fn: CrawlFn) -> CrawlFn:
        _REGISTRY[key] = fn
        return fn

    return decorator


def get_crawler(festival: str) -> CrawlFn:
    """Look up the registered crawl function for a festival.

    Args:
        festival: The festival's dispatch key, as used in `params["FESTIVAL"]`.

    Returns:
        The festival's `crawl(params)` function.

    Raises:
        ValueError: If no crawler is registered under `festival`.
    """
    try:
        return _REGISTRY[festival]
    except KeyError:
        message = f"Unknown festival {festival}. Currently accepted are: {sorted(_REGISTRY)}"
        raise ValueError(message) from None
