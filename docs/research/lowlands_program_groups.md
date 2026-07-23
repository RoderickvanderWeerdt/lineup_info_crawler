# Research: program-group data on Lowlands' `/acts/` page

Ticket: [RoderickvanderWeerdt/lineup_info_crawler#8](https://github.com/RoderickvanderWeerdt/lineup_info_crawler/issues/8)
Snapshot date: 2026-07-19, fetched from `https://lowlands.nl/acts/` (219 acts, 2026 edition).

## Data shape found

The page is server-rendered by a Nuxt 3 app. Every act's full structured data is embedded
directly in the HTML response as a devalue-serialized JSON payload:

```html
<script type="application/json" data-nuxt-data="nuxt-app" id="__NUXT_DATA__">...</script>
```

No separate API call or `/acts/{slug}` page fetch is needed — one request to `/acts/` yields
every act's category, genres, stage/tent, and set times. (The current crawler's
`_lowlands_crawler2` visits each act's detail page individually for `backup_styles`; that's no
longer necessary for category/genre data specifically.)

Each act object looks like:

```json
{
  "url": "/acts/aqueerius-big-fat-trojan-wedding/",
  "title": "Aqueerius – Big Fat Trojan Wedding",
  "location": { "id": 43, "position": 80, "title": "Juliet" },
  "dates": [{ "startDate": "2026-08-22T15:00:00Z", "endDate": "2026-08-22T15:40:00Z" }],
  "category": { "id": 29, "position": 40, "title": "Theater & Dans", "icon": "theatre", "hasGenreFilter": false },
  "genres": []
}
```

`devalue` payloads are reference-flattened (values are indices into a flat array rather than
inline), so parsing requires resolving those indices rather than a plain `json.loads` walk —
straightforward recursively, not exposed via any documented API.

**Caveat — `location` and `dates` are timetable fields, not act fields.** The full timetable
(tent assignment + set times) is only released sometime in the final weeks leading up to the
festival, well after acts are first announced. This snapshot already has `location`/`dates`
populated on every act, meaning the 2026 timetable had already dropped by snapshot time.
Earlier in the season, right after the lineup is first announced, expect `location` and `dates`
to be `null`/absent even though `category` and `genres` are already populated — those come from
the act announcement itself, not the timetable. Any crawler relying on this data shape should
treat `location`/`dates` as optional/late-arriving and `category`/`genres` as available from the
start. This wasn't independently verified against an earlier-season snapshot as part of this
research.

## Program-group categories

The top-level `category` field is a closed, small set (also exposed as the page's own filter
dropdown, `<select class="select-input act-filters__filter">`):

| id | title (NL) | icon slug | count (2026) |
|----|---|---|---|
| 1  | Muziek | — | 157 |
| 26 | Comedy | — | 22 |
| 28 | Wetenschap | — | 18 |
| 31 | Literatuur | — | 11 |
| 29 | Theater & Dans | theatre | 10 |
| 46 | Specials | — | 1 |

Every one of the 219 acts has a `category`; this field is 100% reliable and needs no fallback.

## Electronic/DJ music — not a top-level category, but reliably tagged

There is **no separate "electronic" or "DJ/night" top-level category** — DJs and bands are both
under **Muziek**. But `hasGenreFilter: true` only on Muziek, and each Muziek act carries a
`genres` list (acts can have more than one):

| genre | count (of 157 Muziek acts) |
|---|---|
| Electronic | 92 |
| Pop | 32 |
| Rock | 29 |
| Indie | 20 |
| World/Roots | 17 |
| Hiphop | 16 |
| R&B | 14 |
| Singer/songwriter | 8 |
| Jazz | 7 |
| Metal | 6 |
| Soul | 4 |
| Urban | 3 |
| Klassiek | 1 |

Only 2 of 157 Muziek acts have an empty `genres` list (~98.7% coverage) — reliable enough to use
directly, no inference needed. "Electronic" is not a minor tag: it's the single largest genre,
59% of all Muziek acts.

Corroborating signal: the "Hacienda" tent (22 acts, spanning all day into the night) is 100%
Electronic-tagged — almost certainly the all-day/night DJ tent. Tent name alone isn't a reliable
general-purpose signal (tents aren't semantically named across festivals), but it lines up with
the `genres` finding here.

Non-Muziek categories (Comedy, Theater & Dans, Wetenschap, Literatuur, Specials) never carry
genre tags (`hasGenreFilter: false`, empty `genres` on every act checked).

## Confidence / reliability summary

| group | extractable? | confidence |
|---|---|---|
| Music vs. Comedy vs. Theater & Dans vs. Wetenschap vs. Literatuur vs. Specials | yes, direct `category.title` field | high — present on 100% of acts, available from initial lineup announcement |
| Electronic/DJ vs. other music | yes, via `genres` containing `"Electronic"` within Muziek acts | high — present on ~99% of Muziek acts, available from initial lineup announcement |
| Tent/stage as a grouping proxy | possible but not recommended standalone | low — not semantically reliable in general; also only available once the timetable is released in the final weeks before the festival, not at lineup announcement |

## Open questions (for downstream design, not this ticket)

- Whether "act-grouping" (issue #17 on `festival_lijstje_web`) should surface Electronic as its
  own top-level group alongside Muziek/Comedy/etc., or as a sub-filter/genre facet under Muziek —
  this is a UX/design decision, not a data-availability question. Raised because it directly
  affects users who want to exclude DJ-heavy acts from their view (a real ask from the group
  using `festival_lijstje_web` — a large chunk of Lowlands' lineup, and one full tent, is
  all-day/night electronic/DJ acts).
- This research only covers Lowlands. Other festivals' program pages (DTRH, Pinkpop, BKS, etc.)
  were not checked and may not expose an equivalent category/genre structure — no assumption
  should be made that this generalizes.
- Not investigated: whether `genres` values are stable/enumerable ahead of time (a fixed
  taxonomy) or free-text per edition — only the 2026 edition was sampled.
- Not investigated: how a crawl run before the timetable drops should behave — whether the
  crawler needs to run twice per festival (once at lineup announcement for category/genre, once
  after the timetable lands for tent/set-time), or whether `festival_lijstje_web` even needs
  tent/set-time data at all for act-grouping purposes.
