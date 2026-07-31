# Festival crawler registration: auto-discovery via pkgutil

Supersedes the "triggering registration" part of the dispatch-pattern decision recorded in issue #19 and reaffirmed by `0001-crawl-params-shape-and-source.md` — the rest of that decision (decorator-based self-registration, `crawl(params)` as a free function, one module per festival) is untouched.

Issue #19 deliberately shipped the simple version first: `crawlers/festivals/__init__.py` did a static `from . import bks, dtrh, lowlands, ooto, pinkpop, prettypissed` so each module's `@register("<key>")` decorator would run, with a follow-up ticket already planned to replace it with directory auto-discovery. This ADR records that follow-up landing: `__init__.py` now walks the `festivals/` package with `pkgutil.iter_modules` and imports every module it finds (except `registry.py`) via `importlib.import_module`, instead of naming each one by hand.

```python
def _register_all_festivals() -> None:
    """Import every sibling module so its `@register(...)` decorator runs."""
    for module_info in pkgutil.iter_modules(__path__, prefix=f"{__name__}."):
        if module_info.name != f"{__name__}.registry":
            importlib.import_module(module_info.name)
```

## Considered options

- **Keep the static import list** — rejected. Every new or removed festival module needs a matching hand-edit to `__init__.py`, on top of adding/removing the module file itself. It also needs a `# noqa: F401`, since ruff can't tell a static `from . import x` is intentional (imported only for its `@register` side effect, never referenced by name afterwards).
- **Explicit re-export alias** (`from . import bks as bks, dtrh as dtrh, ...`) — rejected. Recognized by ruff/pyflakes as an intentional re-export, so it drops the `noqa`, but still requires the same manual `__init__.py` edit per festival that the static list does. Only solves half the problem issue #19 flagged.
- **Drop the decorator, register via an explicit dict** (`_CRAWLERS = {"BKS": bks.crawl, ...}`) — rejected. This was implemented briefly during this cleanup and reverted: it reverses the decorator-based dispatch mechanism issue #19 already closed as a deliberate decision. Revisiting that mechanism is a separate discussion, not something to fold into an import-cleanup pass.
- **`pkgutil.iter_modules` + `importlib.import_module` auto-discovery** (chosen) — the exact follow-up issue #19 already anticipated.

## Consequences

Upsides:

- Adding or removing a festival now touches exactly one file — the new/removed `festivals/<name>.py`. `__init__.py` never needs a corresponding edit.
- No `# noqa: F401` anywhere in `festivals/__init__.py` — nothing is statically imported and apparently unused; the loop imports by string name at runtime, so ruff never sees a static "unused" import to flag.
- Forgetting to wire up a new festival module is no longer possible — today, forgetting to add it to the static import list means `get_crawler()` raises `Unknown festival X` at runtime with no direct pointer back to "you forgot to import it"; auto-discovery finds it regardless of whether anyone remembered to touch `__init__.py`.

Downsides:

- **Eager, all-or-nothing loading.** Every module under `festivals/` is imported the moment `lineup_info_collector.crawlers.festivals` is first imported, regardless of which single festival the caller actually wants (e.g. `main.py --festival lowlands` still imports all six). Each module's own dependencies get pulled in and executed at that point too. At today's scale (6 lightweight `bs4`/`requests`-based modules) this is unnoticeable, but it doesn't scale for free: if the festival count grows into the dozens or beyond, single-festival runs still pay the import cost (and memory footprint) of every festival module, not just the one requested. Not a concern at the current scale, but worth naming as the reason this isn't free. If it ever becomes real, the fix is lazy per-key loading (only `importlib.import_module` the specific festival's module inside `get_crawler(festival)`, keyed off filename), not a redesign of this decision.
- **No static list of what's registered.** Reading `festivals/__init__.py` no longer tells a human (or `ty`, or an IDE) which festivals are registered — that's now determined by scanning the directory at runtime. The static list, whatever its maintenance cost, was at least a legible manifest of the registry's contents.
- **Less greppable/traceable.** `importlib.import_module(module_info.name)` is a dynamic, string-based import. `grep 'import dtrh'` and "go to definition" tooling won't find this call site the way a literal `from . import dtrh` would.
- **Any `.py` file dropped into `festivals/` is treated as a festival module by virtue of location alone** (everything except `registry.py` is auto-imported) — there's no explicit per-module opt-in. Low risk in practice (it's a small, deliberately single-purpose directory), but worth naming: a stray helper file placed there would be silently imported and would need its own `@register(...)` (or lack of one) to behave correctly, rather than being ignored by default.
- **Import order is filesystem/directory-listing order**, not declaration order — not guaranteed identical across platforms, unlike an explicit list which always states the exact set. Registration is idempotent and no festival's behavior currently depends on registration order, so this is low-risk today, but it's an assumption this mechanism introduces that the static list didn't have.
