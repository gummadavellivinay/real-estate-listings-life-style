# Search behavior and user guide

[Back to README](../README.md)

## Start a search

The landing page displays the heading, search field, microphone, suggestions, sidebar, and footer. Cards, map, comparison, result count, and sorting are hidden until a nonempty query is submitted.

Type a query and press Enter or **Find my home**, or click a suggestion. Voice dictation fills the same field and requires a separate search submission after review.

Example:

```text
3 bedrooms 2 baths under $550k near tennis and coffee within 10 minutes
```

This sets minimum bedrooms to 3, minimum bathrooms to 2, maximum price to $550,000, preferred driving minutes to 10, and selects tennis and coffee.

The five suggestions are defined in `voice_search.py`. They cover tennis/coffee, trails/gym, Whole Foods/coffee, dog parks/restaurants, and highways/hospitals.

## Parsing rules

`parse_query()` uses case-insensitive regular expressions, not an LLM. It recognizes the first numeric match for each field.

| Field | Supported syntax examples |
| --- | --- |
| Maximum price | `under $450k`, `below 450000`, `max $500k`, `maximum $500k`, `up to $1.2 million` |
| Minimum bedrooms | `3 beds`, `3 bedrooms`, `3+ bedrooms` |
| Minimum bathrooms | `2 baths`, `2.5 bathrooms`, `2+ baths` |
| Preferred drive time | `within 10 minutes`, `under 8 min` |
| Lifestyles | Matching keywords such as `tennis`, `coffee`, `gym`, `trails`, `whole foods` |

Supported price multipliers are `k`, `m`, and `million`. Bedroom and bathroom counts mean **minimums**, not exact matches. Parsed driving minutes are clamped to 1–30 in `apply_query()`.

Each submitted query replaces the entire lifestyle selection with the lifestyles found in that query, including an empty selection when none are found. Numeric filters are replaced only when recognized; other property filters remain as selected. A suggestion follows the same rules and does not reset existing property filters first.

Important parser edge cases:

- Number words such as `three bedrooms` are not converted to digits.
- Locations, school quality, HOA requirements, yard size, negative phrases, and walk-time preferences are not understood as filters.
- Matching is keyword-based: `no coffee` still selects coffee. `dog parks` also matches the general Parks keyword; `pet` selects Dog parks.
- `under 10 minutes` can also be interpreted as a maximum price of $10,000,000, because the budget expression treats the initial `m` in `minutes` as the million multiplier. Prefer `within 10 minutes` and an explicit budget.
- Unsupported-term warnings detect `school`, `quiet`, `hvac`, `verified`, `disclosure`, and `commute`. Other unsupported requests can be silently ignored.
- Numeric conversion has no general malformed-input error handling. Review sidebar values after searching.

## Sidebar defaults and filters

| Control | Initial value | Effect |
| --- | --- | --- |
| Lifestyle choices | None | Select amenities to rank by |
| Maximum drive time | 10 minutes | Preference threshold, selectable 1–30 |
| Require every lifestyle match | Off | When on, every selected amenity must meet the threshold |
| Minimum price | $0 | Inclusive lower bound |
| Maximum price | $1,000,000 | Inclusive upper bound |
| Minimum bedrooms | 0 | Inclusive minimum |
| Minimum bathrooms | 0 | Inclusive minimum, above ground |
| Minimum living area | 0 sq ft | Inclusive minimum |
| Built in or after | 1800 | Inclusive minimum construction year |
| Neighborhood codes | None | No neighborhood restriction; selections match CSV codes |
| Garage | Off | When on, require `GarageCars > 0` |
| Central air | Off | When on, require `CentralAir == "Y"` |

Sidebar changes update results once a search has been submitted. Changing sidebar controls on the landing page does not make results visible.

## Ranking and sorting

For selected lifestyles, each home's score is:

```text
round(100 × mean(max(0, 1 − drive_minutes / (2 × preferred_minutes))))
```

For example, with a 10-minute preference and drive times of 5 and 15 minutes, contributions are 0.75 and 0.25, producing a score of 50. The five-minute amenity meets the preference; the fifteen-minute amenity does not.

Soft mode retains homes that exceed preferred drive times, subject to property filters. Strict mode requires every selected amenity's drive time to be at most the preference. No selected lifestyles means `score = None`; strict mode then adds no proximity restriction. Walking times never affect filtering or scores.

| Sort option | Ordering |
| --- | --- |
| Best lifestyle match | Score descending, then price ascending; without lifestyles, price ascending |
| Price: low to high | Price ascending |
| Price: high to low | Price descending |
| Newest built | Construction year descending |

## Browse and compare

The result count and sorting controls appear below suggestions. Cards are rendered in three columns, initially up to 12. **Show 12 more homes** increases the rendered count by 12; it is incremental loading, not numbered pages. New submitted searches reset that count to 12; sidebar changes do not explicitly reset it.

Cards show a sample photo, ID, neighborhood code, price, beds, baths, area, construction year, and price per square foot. Selected lifestyles add a score and walking/driving times. Without selected lifestyles, cards ask the user to select lifestyles; details still list all amenities.

**View details** opens a dialog with additional property fields, amenity times, unavailable-information disclosures, and a downloadable showing-request draft containing home ID, date, and notes. Nothing is sent or booked.

**Illustrative map** displays up to the first 100 sorted matches and their identifying table. Positions are generated; amenities are not mapped.

**Compare homes** accepts up to four selections. It uses selected records from the full dataset, so selections survive filtering, new searches, and resets. The comparison table uses dataset order rather than selection order. It shows property values and walk/drive times for selected lifestyles, or all lifestyles when none are selected. Tradeoff text uses driving minutes. Remove selections from cards or use **Clear comparison**.

## Clear and reset

Deleting all text, using the search field's browser-provided clear control, or submitting whitespace emits an empty search event. This stops active dictation and calls `reset()`: results disappear, sidebar defaults return, the warning clears, and card count returns to 12. **Reset filters** performs the same backend reset. Comparison selections remain.

Nonempty text edits do not automatically run a new search; the existing result set remains until submission. An invalid price range produces an error. No matches produce a warning, while the result tabs remain available.
