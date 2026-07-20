# AGENTS

## Purpose

`lineup_info_crawler` crawls festival lineup pages, enriches artist data from other sources, and exports the result to CSV — usable standalone or as a library. It's also pulled into `festival_lijstje_web` via git subtree.

## Repository shape

- `lineup_info_collector/`: crawler and enrichment library code (`crawlers/`, `exporter/`).
- `main.py`: CLI entry point.
- `params/`: per-festival YAML configs.
- `legacy/`: pre-refactor notebook and CSV exports, kept for reference.

## Documentation routing

- `AGENTS.md` (this file): high-level overview and pointers only. Keep it short — put specifics in the linked docs.
- [docs/agents/python.md](docs/agents/python.md) — running the crawler, `uv` dependency management.
- [docs/agents/linting.md](docs/agents/linting.md) — running `ruff` and `ty` locally.
- [docs/agents/testing.md](docs/agents/testing.md) — pytest conventions.
- [docs/agents/git.md](docs/agents/git.md) — commit conventions, PR-splitting norms, AI-assisted-PR norm.

## Quality bar

Land larger changes as multiple small, independently reviewable PRs rather than one large diff. See [docs/agents/git.md](docs/agents/git.md).
