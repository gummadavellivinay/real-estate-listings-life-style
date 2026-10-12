# Future improvements

[Back to README](../README.md)

These are proposals, not implemented features.

## Search correctness

- Separate budget and duration parsing so `under 10 minutes` cannot set a price of $10,000,000.
- Normalize spoken number words and currency phrases before parsing.
- Handle malformed numeric inputs without crashing and identify unsupported requirements explicitly.
- Add negative-phrase handling and clearer rules for overlapping lifestyle keywords.
- Add walk/drive mode selection with separate thresholds and ranking only after trustworthy travel data is available.

## Data and integrations

- Replace synthetic records with a validated listing source containing real addresses and property-specific licensed images.
- Add geocoding, verified amenity destinations, and routing for walking/driving travel times.
- Add data timestamps and source attribution for prices, disclosures, HOA information, and other evidence.
- Add schema validation, conversion-error reporting, and a missing-image fallback.

## Product experience

- Add saved searches and persistent comparison selections if user accounts and storage are introduced.
- Improve compact/mobile result controls and verify the single-line heading across screen sizes.
- Decide whether Reset filters should also reset sorting or comparison selections; it currently does neither explicitly.
- Add actual showing scheduling and agent messaging only through a defined workflow with clear user review and confirmation.

## Voice robustness and privacy

- Test real speech providers across target browsers, devices, long pauses, network failures, and rerenders.
- Improve transcript handling around restart gaps and user edits during active dictation.
- Consider a configurable speech provider if browser dictation is insufficient, with explicit audio handling and retention rules.

## Engineering and operations

- Expand tests for parser conflicts, all defaults, reset/compare persistence, walking values, sorting variants, detail downloads, and asset failures.
- Add real-browser visual and accessibility checks; current DOM mocks cannot validate layout or microphone capture.
- Reduce reliance on Streamlit private test helpers where supported alternatives become available.
- Add CI, deployment instructions, and production observability when a hosting target is selected. No deployment pipeline is defined in the current source.
