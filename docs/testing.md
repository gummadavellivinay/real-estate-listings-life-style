# Testing and verification

[Back to README](../README.md)

## Automated checks

Run from the repository root after `uv sync`:

```sh
uv run python -m unittest discover -s tests -v
node tests/test_voice_search.mjs
```

No additional Node dependencies or frontend build step are required for the JavaScript checks.

| File | Current coverage |
| --- | --- |
| `tests/test_search.py` | Four tests: CSV count/sample fields; query parsing; combined property filters and strict proximity; empty results, price sorting, and score ordering |
| `tests/test_app.py` | One integration test: landing has no cards/tabs/sort; a component event applies filters and renders 12 cards; query reaches component data; rerun succeeds; empty input hides results and resets filters; Reset filters returns to landing |
| `tests/test_voice_search.mjs` | Mocked DOM/speech checks: editable transcript, explicit submission, suggestions, permission errors, cleanup, typed fallback, continuous recognition, retained transcripts, silence restart, explicit Stop, cancellation during restart delay, fatal-error retry prevention, and clear-input behavior |

The Python UI test uses Streamlit's widget protocol and internal helpers such as `_make_trigger_id`, `_tree`, and `_run`. Framework changes may require test updates. JavaScript tests use lightweight mocks, not a real browser or microphone. Automated tests do not verify CSS rendering, map tiles, actual speech recognition, all parser edge cases, or every comparison/detail action.

## Manual browser checklist

1. Launch the application. Confirm the heading is one line and the landing view contains no results.
2. Submit `3 bedrooms under $550k near tennis and coffee within 10 minutes`. Verify sidebar values, result count/sort alignment below suggestions, and cards.
3. Click a suggestion. Confirm recognized filters update; unmentioned property filters remain.
4. Change sidebar filters after searching. Toggle strict mode and change sort order. Check zero-match and invalid-budget states.
5. Start voice dictation in a supporting browser on localhost or HTTPS. Confirm the Stop icon, live text, continued listening across pauses, and transcript review before submission.
6. Stop during a pause. Confirm listening does not restart. Check permission denial and typed fallback.
7. Clear all text using both deletion and the field's clear control. Confirm results disappear, sidebar defaults return, and dictation stops.
8. Open details; check walk/drive columns and download a showing-request draft. Confirm no booking or message is sent.
9. Select up to four homes, compare them, then change filters. Confirm selections remain. Try a fifth selection and remove/clear selections.
10. Open the map. Confirm generated-location disclosure and a maximum of 100 listed matches.
11. Load more cards and check that the synthetic-data disclosures remain below the results.
12. Check narrow-screen layout and keyboard focus for input, microphone, suggestions, and search submission.

## Documentation verification record

Documentation was reviewed against the current source on October 12, 2026:

- `app.py`: layout gate, callbacks, defaults, reset semantics, cards, details, comparison, map limits, walking-time calculation, and footer.
- `search.py`: field normalization, keyword patterns, numeric expressions, filters, score formula, sort keys, and generated data formulas.
- `voice_search.py` and component HTML/CSS/JS: suggestions, recognition lifecycle, Stop icon, accessibility labels, and empty-input triggers.
- `pyproject.toml`, `uv.lock`, local photo assets, CSV, and test files: setup, dependencies, asset counts, and automated coverage.

All five Python tests and the JavaScript assertion suite passed during documentation generation. Additional source/data probes checked CSV count, photo count, generated-time ranges, the score example, and documented parser edge cases. This review did not perform a fresh live-microphone, full browser-layout, or deployment validation.
