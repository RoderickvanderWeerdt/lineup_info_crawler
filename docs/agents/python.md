# Python conventions

Requires Python 3.13 (see `pyproject.toml`). Managed with `uv`. Flat, single-package layout — code lives directly under `lineup_info_collector/` and `main.py`, no `src/` layout, no `uv` workspace.

## Running

```bash
uv sync
uv run python main.py --festival lowlands --year 2026
```

`main.py` takes `-f`/`--festival`, `-y`/`--year`, an optional `-u`/`--url` (overrides the festival's registered default), and `-v`/`--verbose`. Crawl parameters flow through the codebase as a frozen `CrawlParams` dataclass (`lineup_info_collector/params.py`), not a dict — see ADR-0001 (`docs/adr/0001-crawl-params-shape-and-source.md`, landing via #32).

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
