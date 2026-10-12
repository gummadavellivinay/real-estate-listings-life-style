# Voice search

[Back to README](../README.md)

## User workflow

1. Tap the microphone and allow access if the browser prompts.
2. Speak the query. The microphone changes to a square Stop icon, and the live status announces listening.
3. Tap Stop when finished.
4. Review and edit the transcript, especially numeric budgets and bedroom counts.
5. Select **Find my home** or press Enter. Dictation does not automatically submit a search.

A new microphone activation starts a fresh transcript; it does not append to existing typed text or a previous stopped recording. Within one active dictation, text is retained across automatic recognition restarts.

## Implementation

`search.js` uses `window.SpeechRecognition || window.webkitSpeechRecognition`. It requires `window.isSecureContext`; otherwise the microphone is disabled and typed search and suggestions remain available.

Recognition settings are English (`en-US`), interim results enabled, and continuous mode enabled. Interim transcripts are written directly to the input. On a normal recognition-session end while the user still wants to listen, the component retains the transcript and schedules a restart after 500 milliseconds. Silence errors allow continued listening. This is browser speech dictation, not a recorded-audio upload or audio-file feature.

`keepListening` tracks user intent independently of the current service session. Stop clears that flag and any scheduled restart. Submitting or clearing a query aborts recognition; clearing also emits an empty search event to reset the application. Component cleanup removes handlers, cancels the restart timer, and aborts recognition.

CSS displays the microphone or Stop SVG based on the control's `aria-pressed` attribute. The button also changes its accessible label and tooltip. Status messages use an `aria-live` region.

## Errors and limits

Permission denial, speech-service denial, missing microphone, and network failures stop automatic restarts and show an error message. A startup exception also stops recognition. The user can retry or type.

Recognition availability, service duration, connectivity, and audio quality depend on the browser and device. Continuous mode and automatic restarting do not guarantee uninterrupted transcription: words spoken during a restart gap may be missed. A rerender/unmount can abort capture through the component cleanup lifecycle.

The app does not save recordings or use an application speech API key. The browser may process audio through its own speech provider. Submitted transcripts enter Streamlit session state and the normal rule-based parser; number words are not normalized into digits.

## Verification scope

Mocked JavaScript tests exercise continuous mode, transcript preservation, silence recovery, explicit Stop, pending-restart cancellation, fatal errors, cleanup, typed fallback, and clear-input events. They do not prove actual microphone capture or a browser speech provider's behavior. See [Testing](testing.md) for live checks.
