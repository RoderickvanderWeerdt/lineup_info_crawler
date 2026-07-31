# Linting & type checking

`ruff` for linting and formatting, `ty` for type checking. Run both before opening a PR.

## Ruff

```bash
uv run ruff check
uv run ruff format
```

`ruff.toml` (`select = ["ALL"]` plus a curated ignore list) configures both. Run the commands above before opening a PR; CI enforces both on every pull request (see [ci.md](ci.md)).

`ruff check`/`ty check` currently fail against pre-existing violations in four files, predating the strict config — that remediation approach is still undecided (see [lineup_info_crawler#5](https://github.com/RoderickvanderWeerdt/lineup_info_crawler/issues/5)), so CI showing red there isn't a sign anything is misconfigured.

## Type checking

```bash
uv run ty check
```

`ty` is a dev dependency, configured via `[tool.ty.src]` in `pyproject.toml` to exclude notebooks (`**/*.ipynb`) so `legacy/crawl_AllMusic.ipynb` isn't type-checked.
