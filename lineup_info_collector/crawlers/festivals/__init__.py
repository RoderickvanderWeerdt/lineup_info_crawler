import importlib
import pkgutil

from lineup_info_collector.crawlers.festivals.registry import get_crawler


def _register_all_festivals() -> None:
    """Import every sibling module so its `@register(...)` decorator runs."""
    for module_info in pkgutil.iter_modules(__path__, prefix=f"{__name__}."):
        if module_info.name != f"{__name__}.registry":
            importlib.import_module(module_info.name)


_register_all_festivals()

__all__ = ["get_crawler"]
