# Testing conventions

Tests run with `pytest`; coverage is tracked via `pytest-cov`. `[tool.pytest.ini_options]` and `[tool.coverage.run]` are configured in `pyproject.toml`. No tests exist yet; this doc pins down the conventions ahead of the first one.

```bash
uv run pytest
```

- Mirror the package structure (`lineup_info_collector/crawlers/`, `lineup_info_collector/exporter/`) under `tests/`.
- Test through real behavior where practical; mock external systems (e.g. the crawlers' HTTP calls), not internal logic.
- `legacy/` is not covered by tests.
