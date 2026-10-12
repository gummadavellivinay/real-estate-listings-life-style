# Setup

[Back to README](../README.md)

## Requirements

- Python 3.11 or newer, as declared in `pyproject.toml`.
- uv for dependency installation and running the project.
- A browser for the Streamlit interface.
- Node.js with ES modules and top-level await for `tests/test_voice_search.mjs`; it is not required to run the app.

The project declares Streamlit `>=1.51,<2` and pandas `>=2.2,<3`. `uv.lock` records the resolved dependency versions. The project uses `package = false`; it runs directly from source without installing itself as a package.

## Run locally

Run these commands from the repository root:

```sh
uv sync
uv run streamlit run app.py
```

Open the URL printed by Streamlit. Keep the terminal process running. Press Ctrl+C in that terminal to stop it.

For a different port:

```sh
uv run streamlit run app.py --server.port 8502
```

The CSV, `components/search_box/` assets, and `assets/homes/*.jpg` must remain available alongside the Python source. Paths for those assets are resolved relative to the source files. The application expects at least one bundled JPEG and valid CSV fields; there is no missing-photo fallback or general CSV validation layer.

## Configuration and network use

The app has no required environment variables or API keys and does not load `.env` files.

Python search runs against local files. Voice recognition may require an internet connection through the browser's speech service, and the map can require external map resources. Local search and bundled photos do not require a listing-data service.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Address already in use | Start on another port using `--server.port`. |
| Missing `streamlit` or `pandas` | Run `uv sync`, then use `uv run`. |
| Voice control is disabled | The component checks for `SpeechRecognition` or `webkitSpeechRecognition` and a secure browser context. Use localhost or HTTPS with a supporting browser. |
| Microphone permission error | Allow microphone access in browser/site settings; typed search remains available. |
| Speech service network error | Check connectivity and retry, or type the query. |
| Spoken query does not set the expected filters | Review the transcript and use numeric phrases such as `3 bedrooms under $500k`. Parsing does not convert number words. |
| No cards on first load | Expected: submit a nonempty search or click a suggestion. Sidebar changes alone do not open results on the landing page. |
| Unexpected search behavior | Review the sidebar and the parser limitations in [Search behavior](search-behavior.md). |
