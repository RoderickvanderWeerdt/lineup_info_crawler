# Research: standardizing the artist-dict return shape across festival crawlers

Written to resolve [Research standardizing the artist-dict return shape across festival crawlers (#35)](https://github.com/RoderickvanderWeerdt/lineup_info_crawler/issues/35), part of Wayfinder map #18.

## What each crawler actually returns

`lineup_crawler(params)` dispatches to one per-festival function (`lineup_info_collector/crawlers/lineup_crawler.py`). Every one of them returns `name` and `link`. Beyond that, only two keys ever appear, and only for some festivals:

| Festival | `day` | `backup_styles` |
|---|---|---|
| DTRH | – | – |
| pinkpop | ✓ | – |
| ooto | – | – |
| prettypissed | – | – |
| lowlands (`_lowlands_crawler2`, the live one) | – | ✓ |
| BKS | ✓ | ✓ |

`info_crawler()` then merges in a second, *always*-present set of keys from the AllMusic lookup: `activeDate`, `genres`, `styles`, `act_url`, `info_url` (`info_crawler.py:163`). So the "heterogeneity" is narrow: only two optional keys, not a sprawling divergence — the shape is `{name, link, activeDate, genres, styles, act_url, info_url}` plus `day` and/or `backup_styles` when the source festival happens to expose them.

## What festival_lijstje_web's upsert actually reads

`update_festival_lineup()` (`backend/src/festival_ranking/services/festival_service.py:235`) reads: `name`, `genres`, `styles`, `activeDate` (→ `Artist.start_decade`), `info_url` (→ `Artist.allmusic_url`), and `act_url`/`link` (→ `festival_artists.festival_page_url`).

It never reads `day` or `backup_styles` directly. That's not a coincidental oversight in one place — it's two different situations:

- **`day` is a real, unused capability.** `festival_artists` already has a `performance_date` column (`db/models.py`, `festival_artists` table) sized for exactly this, but `update_festival_lineup()` never sets it — dead column, dead crawler field. Whether to wire the two together is a *product* decision on the `festival_lijstje_web` side (does the app want to show which day an artist plays?), not something this crawler-side ticket should decide.
- **`backup_styles` is a real, silent bug.** It exists purely as a fallback: `exporter.py`'s `_check_backup_styles()` copies `backup_styles` into `styles` when AllMusic returned nothing. But that function only runs on the CLI/CSV export path (`main.py` → `exporter.py`) — the library-call path `festival_lijstje_web` actually uses (`crawler_service.py:35-36`, `lineup_crawler()` → `info_crawler()` directly, no exporter step) never calls it. So today, any lowlands or BKS artist AllMusic fails to match gets an empty `styles` in the live app, even though the festival's own page told us their genre — the fallback silently doesn't fire on the path that matters.

## Recommendation

This doesn't need its own wayfinder map — the shape itself is small (two optional keys) and the fix is mechanical, not a design question with branches to grill. Two small, independent follow-ups:

1. **Fix the `backup_styles` propagation gap.** Move (or duplicate) the `_check_backup_styles` fallback into the shared `crawl_lineup_info()` entry point (decided in #22) so both the CLI export path and the `festival_lijstje_web` library path apply it — not just CSV export. This is a real bug fix, not a shape change.
2. **Normalize the optional keys, don't standardize the shape.** Every crawler returning `day` and `backup_styles` as always-present keys (defaulting to `None`/empty instead of being absent) removes the need for callers to guard with `.get()` or `try/except` — cheap, low-risk, no behavior change for festivals that don't have the data.

`day` → `performance_date` wiring is explicitly **not** recommended here: it's a `festival_lijstje_web`-side product decision outside this repo's scope, following the same split already used for #23's downstream gaps ([festival_lijstje_web#28](https://github.com/VSJMilewski/festival_lijstje_web/issues/28), [festival_lijstje_web#29](https://github.com/VSJMilewski/festival_lijstje_web/issues/29)).
