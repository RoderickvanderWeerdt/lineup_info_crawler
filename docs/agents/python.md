# Python conventions

Requires Python 3.13 (see `pyproject.toml`). Managed with `uv`. Flat, single-package layout — code lives directly under `lineup_info_collector/` and `main.py`, no `src/` layout, no `uv` workspace.

## Running

```bash
uv sync
uv run python main.py
```

`main.py` accepts `-p`/`--params` (path to a `params/<festival>.yaml` config) and `-v`/`--verbose`, but CLI parsing is currently commented out in `main()` — it runs whichever `params/` file is hardcoded in the `get_params(...)` call. Edit that call to target a different festival config.

## Dependency management

Always add or remove dependencies via `uv` CLI commands — never edit `pyproject.toml` directly.

```bash
uv add <package>          # runtime dependency
uv add --dev <package>    # dev-only dependency
```

## Type hints

- Prefer builtin generics over `typing`: `list`, `dict`, `tuple` instead of `List`, `Dict`, `Tuple`.
- Use `|` for unions and optionals (`str | int`, `str | None`) instead of `Union`/`Optional`.

Enforced by ruff's `UP` ruleset (see [linting.md](linting.md)) rather than by convention alone.

## Docstrings

Google-style docstrings on every function: a one-line summary, then `Args:`, `Returns:`, and `Raises:` sections as applicable — omit any section that doesn't apply (e.g. no `Returns:` for a function returning `None`, no `Raises:` if nothing is deliberately raised). No need for prose beyond the summary line unless something non-obvious needs explaining.

```python
def get_crawler(festival: str) -> CrawlFn:
    """Look up the registered crawl function for a festival.

    Args:
        festival: The festival's dispatch key, as used in `params["FESTIVAL"]`.

    Returns:
        The festival's `crawl(params)` function.

    Raises:
        ValueError: If no crawler is registered under `festival`.
    """
```

## Imports

No relative imports (`from . import x`, `from .. import x`). Always import via the full `lineup_info_collector...` path, e.g. `from lineup_info_collector.crawlers.utils import _get_soup`. This matches how `main.py` already imports the package from outside, so the convention is the same whether the importing file lives inside or outside `lineup_info_collector/`.

## See also

- [linting.md](linting.md) — `ruff` and `ty` usage
- [testing.md](testing.md) — pytest conventions
