# Linting & type checking

`ruff` for linting and formatting, `ty` for type checking. Run both before opening a PR.

## Ruff

```bash
uv run ruff check
uv run ruff format
```

`ruff.toml` (`select = ["ALL"]` plus a curated ignore list) is not in the repo yet — it lands in a follow-up PR (see #11). The commands above are the target workflow.

## Type checking

```bash
uv run ty check
```

`ty` is a dev dependency, configured via `[tool.ty.src]` in `pyproject.toml` to exclude notebooks (`**/*.ipynb`) so `legacy/crawl_AllMusic.ipynb` isn't type-checked.
