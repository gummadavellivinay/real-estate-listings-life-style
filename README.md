# True Home Search

A Streamlit application for exploring 2,500 synthetic homes using property requirements and everyday lifestyle preferences. Search by typing, browser voice dictation, or clickable suggestions. No API keys are required.

## Quick start

Prerequisites: Python 3.11 or newer and uv. Node.js is needed only for the JavaScript tests.

From the project directory:

```sh
uv sync
uv run streamlit run app.py
```

Open the local URL printed by Streamlit, normally `http://localhost:8501`. If that port is busy:

```sh
uv run streamlit run app.py --server.port 8502
```

Try `3 bedrooms under $550k near tennis and coffee within 10 minutes` and select **Find my home**.

## Current features

- Search-focused landing page with a single-line heading and five suggestion pills; results appear after a nonempty search is submitted.
- Browser voice dictation with a Stop icon while listening, editable transcripts, and automatic recognition-session restarts after pauses or normal service disconnections.
- Rule-based parsing of lifestyle terms, maximum budgets, minimum bedrooms and bathrooms, and preferred driving minutes.
- Sixteen lifestyle choices, sidebar property filters, strict proximity matching or soft ranking, and four sorting options.
- Result count and sorting share a row directly below suggestions. Cards initially show up to 12 homes; **Show 12 more homes** expands the list.
- Sample photos, home details, walking and driving times, an illustrative map of up to 100 matches, and comparison of up to four homes.
- Downloadable showing-request text drafts. The application does not send requests or book appointments.
- Clearing the search field stops dictation, hides results, and resets sidebar filters. **Reset filters** also returns to the landing view. Comparison selections remain until explicitly removed or cleared.

## Data boundaries

This is a prototype using synthetic CSV records, seven reused sample photos, generated drive times, and illustrative map coordinates. Walking times are calculated as five times driving times. These are not real route estimates or verified listings. Filters and lifestyle scores use driving times; displayed bathrooms exclude basement bathrooms. Detailed disclosures appear in the page footer.

## Documentation

| Guide | Contents |
| --- | --- |
| [Setup](docs/setup.md) | Dependencies, running locally, troubleshooting |
| [Architecture](docs/architecture.md) | Source layout, Mermaid diagram, event flow, session state |
| [Search and user guide](docs/search-behavior.md) | Parsing, filters, ranking, results, comparison, reset behavior |
| [Voice search](docs/voice-search.md) | Dictation lifecycle, transcript handling, browser requirements |
| [Data model and limitations](docs/data-model-and-limitations.md) | CSV mapping, generated values, unsupported requests |
| [Testing](docs/testing.md) | Commands, automated coverage, manual checks, verification record |
| [Future improvements](docs/future-improvements.md) | Proposed work, separate from implemented features |

## Tests

```sh
uv run python -m unittest discover -s tests -v
node tests/test_voice_search.mjs
```

Documentation was checked against the source and tests on October 12, 2026. See [Testing](docs/testing.md) for the scope of verification.
