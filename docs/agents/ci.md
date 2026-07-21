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

The GitHub Actions workflow runs on every pull request: `ruff check`, `ruff format --check`, `ty check`, `pytest`. It mirrors the same commands documented in [linting.md](linting.md) and [testing.md](testing.md) — nothing CI-specific to configure beyond what those already require locally, once `ruff.toml` (#13) and `ty` (#14) have landed. Until then, the `ty check` and `ruff check` steps fail on every PR — expected, not a workflow bug (see #11).
