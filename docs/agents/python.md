# Python conventions

Requires Python 3.13 (see `pyproject.toml`). Managed with `uv`. Flat, single-package layout — code lives directly under `lineup_info_collector/` and `main.py`, no `src/` layout, no `uv` workspace.

## Running

```bash
uv sync
uv run python main.py --festival lowlands --year 2026
```

`main.py` takes `-f`/`--festival`, `-y`/`--year`, an optional `-u`/`--url` (overrides the festival's registered default), and `-v`/`--verbose`. Crawl parameters flow through the codebase as a frozen `CrawlParams` dataclass (`lineup_info_collector/params.py`), not a dict — see ADR-0001 (`docs/adr/0001-crawl-params-shape-and-source.md`, landing via #32).

## Public API surface

`lineup_info_collector/__init__.py` re-exports exactly three names — `crawl_lineup_info`, `lineup_crawler`, `info_crawler` — as the sanctioned public surface. External callers (including `festival_lijstje_web`'s `crawler_service.py`) should import from the package root, not deep-import submodules under `crawlers/`, so internal reorganizing can't break them. This is a scoped exception, not a general re-export-everything convention — other helpers (`CrawlParams`, `get_default_columns`, `get_default_url`, `export_data`) stay at their existing import paths.

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

## See also

- [linting.md](linting.md) — `ruff` and `ty` usage
- [testing.md](testing.md) — pytest conventions
