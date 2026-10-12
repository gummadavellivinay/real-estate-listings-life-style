# True Home Search

A Streamlit lifestyle search project using all 2,500 homes from `synthetic_real_estate_data.csv`. Managed with uv; no API keys required.

## Run

Install uv if needed using its official installer, then:

```sh
cd real-estate-listings-life-style
uv sync
uv run streamlit run app.py
```

Open the local URL printed by Streamlit (normally http://localhost:8501).

## Features

- Landing page focuses on search and suggestions; results appear after a search. Result count and sorting share a row below suggestions, with data disclosures in the footer.

- Text search recognizes lifestyle terms, budgets (`under $450k`), bedrooms, bathrooms and drive-time preferences (`within 10 minutes`). Sidebar filters combine with text search.
- Continuous voice dictation in the search box until the microphone is tapped again, with transcript preservation across browser session restarts, editable transcripts, microphone status, and clickable suggestion pills. Voice requires a supported browser (such as Chrome), microphone permission, and localhost or HTTPS. The browser may use its speech provider to process audio; the app does not store recordings. Typed search remains available.
- Sixteen lifestyle choices including tennis, pickleball, trails, gyms, coffee, Whole Foods, dog parks, culture and golf.
- Strict proximity matching or soft ranking, property filters, sorting, paginated home cards, details, an illustrative map, and comparison of up to four homes.
- Downloadable showing request drafts. No booking or messages are sent.
- Listing cards and details include randomly assigned sample home photos, kept consistent by listing ID. Seven bundled Unsplash photos are reused across the demo; they do not depict the listed properties.

## Data boundaries

The reference document informed the search, cards, map, comparison and detail sections. The CSV provides historical synthetic sale prices, neighborhood codes, property specifications and condition codes, not live listings. Bathrooms displayed are above-ground full baths plus half baths. Basement bathrooms are excluded.

Walking and driving times appear side by side on cards, details and comparisons. Walking times are illustrative values modeled as five times driving times; filters and lifestyle scores continue to use driving times. Nearby drive times and coordinates are deterministic examples generated from listing IDs. They are not Google Places results, travel estimates or real locations. Lifestyle score averages `max(0, 1 - demo_minutes / (2 * preferred_minutes))` across selections, scaled to 100. Strict mode also requires every drive time to meet the threshold. No lifestyles means no lifestyle score.

Real addresses, photos, schools, quietness, HVAC age, HOA, truth scores, certification and disclosures are unavailable. They are not inferred. Customer/agent authentication, location detection, real Places integration and actual showing scheduling are future integrations, not implemented demo features. The existing LangChain `.env` is never accessed.

Text parsing is rule-based; review the sidebar after applying a query. Recognized text fields replace their corresponding filters; unmentioned property filters remain. Negative phrases and arbitrary location searches are not supported.

## Tests

```sh
uv run python -m unittest discover -s tests -v
node tests/test_voice_search.mjs
```

`search.py` is independent of Streamlit; `app.py` is the UI. Replace generated proximity with verified geocoded addresses and a real places/routing provider before using this for real home decisions.
