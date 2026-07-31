# Testing conventions

Tests run with `pytest`; coverage is tracked via `pytest-cov`. `[tool.pytest.ini_options]` and `[tool.coverage.run]` are configured in `pyproject.toml`, including `pythonpath = ["."]` so `tests/` can import `lineup_info_collector` without installing the project.

```bash
uv run pytest
```

- Mirror the package structure (`lineup_info_collector/crawlers/`, `lineup_info_collector/exporter/`) under `tests/`.
- No HTTP mocking anywhere — not `unittest.mock.patch`, no mocking library. Each festival crawler's `crawl(params)` is a thin `parse_<festival>(_get_soup(params.url))` composition; the pure `parse_<festival>(soup)` half is what gets tested, fed a minimal handwritten `.html` fixture under `tests/crawlers/fixtures/` (e.g. `tests/crawlers/fixtures/lowlands.html`). Fetch wrappers (`_get_soup`, `info_crawler.py`'s fetch functions) aren't unit tested. The shared `load_fixture` fixture in `tests/conftest.py` loads one by name.
- Already-pure helper functions with no HTTP involved (`_compare_names`, `_str_dayfinder`, `_str_weekend_dayfinder`, `_check_backup_styles`, etc.) get direct unit tests, no fixtures needed.
- `legacy/` is not covered by tests.
