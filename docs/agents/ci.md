# Pre-commit & CI

`.pre-commit-config.yaml` runs checks locally before a commit lands; `.github/workflows/ci.yml` runs the same class of checks on every pull request. Neither fixes existing violations in the codebase for you — see [linting.md](linting.md) for the current known exceptions.

## Pre-commit

```bash
uvx pre-commit install
uvx pre-commit run --all-files
```

The `uv-sync` hook keeps your local `.venv` matching `uv.lock` automatically, but it only runs on `post-checkout`/`post-merge`/`post-rewrite`, not on commit — `pre-commit install` only wires up the `pre-commit` stage by default. To get `uv-sync` firing too, install the extra hook types:

```bash
uvx pre-commit install --hook-type pre-commit --hook-type post-checkout --hook-type post-merge --hook-type post-rewrite
```

Hook versions are pinned in `.pre-commit-config.yaml`; bump them with `uvx pre-commit autoupdate`.

## CI

The GitHub Actions workflow runs on every pull request: `ruff check`, `ruff format --check`, `ty check`, `pytest`. It mirrors the same commands documented in [linting.md](linting.md) and [testing.md](testing.md) — nothing CI-specific to configure beyond what those already require locally.

The `ruff check` and `ty check` steps currently fail on every PR regardless of what it touches, because they lint the whole repo and pre-existing violations haven't been remediated yet — see [linting.md](linting.md) and [lineup_info_crawler#5](https://github.com/RoderickvanderWeerdt/lineup_info_crawler/issues/5). Expected, not a workflow bug.

The `Test` step treats pytest's exit code 5 ("no tests collected") as passing, since no tests exist yet — any other nonzero exit code still fails the build.
