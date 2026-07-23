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

Once `ruff.toml` lands (see [linting.md](linting.md)), these are enforced by ruff's `UP` ruleset rather than by convention.

## See also

- [linting.md](linting.md) — `ruff` and `ty` usage
- [testing.md](testing.md) — pytest conventions
