# Testing conventions

Tests run with `pytest`; coverage will be tracked via a coverage plugin. Neither is configured in `pyproject.toml` yet — that lands in a follow-up PR (see #11). No tests exist yet either; this doc pins down the conventions ahead of the first one.

```bash
uv run pytest
```

- Mirror the package structure (`lineup_info_collector/crawlers/`, `lineup_info_collector/exporter/`) under `tests/`.
- Test through real behavior where practical; mock external systems (e.g. the crawlers' HTTP calls), not internal logic.
- `legacy/` is not covered by tests.
