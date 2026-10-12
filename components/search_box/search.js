export default function(component) {
  const {parentElement, data, setTriggerValue} = component;
  const input = parentElement.querySelector('input');
  const form = parentElement.querySelector('form');
  const mic = parentElement.querySelector('.mic');
  const status = parentElement.querySelector('.status');
  const suggestions = parentElement.querySelector('.suggestions');
  if (input.dataset.appliedQuery !== (data.query || '')) {
    input.value = data.query || '';
    input.dataset.appliedQuery = data.query || '';
  }
  let recognition = null;
  let listening = false;
  let disposed = false;
  let keepListening = false;
  let restartTimer = null;
  let discardResults = false;
  const stopCapture = (abort = false) => {
    keepListening = false;
    clearTimeout(restartTimer);
    restartTimer = null;
    mic.setAttribute('aria-pressed', 'false');
    mic.setAttribute('aria-label', 'Start voice search');
    mic.title = 'Speak your search';
    if (recognition) {
      if (abort) { discardResults = true; recognition.abort(); }
      else if (listening) recognition.stop();
    }
  };
  const clearSearch = () => {
    stopCapture(true);
    setTriggerValue('search', '');
  };
  input.oninput = () => {
    if (!input.value.trim()) clearSearch();
  };
  const submit = () => {
    if (!input.value.trim()) { clearSearch(); status.textContent = 'Describe a home to start your search.'; input.focus(); return; }
    stopCapture(true);
    setTriggerValue('search', input.value.trim());
  };
  form.onsubmit = event => { event.preventDefault(); submit(); };
  suggestions.replaceChildren();
  for (const text of data.suggestions) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = text;
    button.onclick = () => { input.value = text; submit(); };
    suggestions.appendChild(button);
  }
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition || !window.isSecureContext) {
    mic.disabled = true;
    mic.title = 'Voice search needs a supported browser on localhost or HTTPS';
    status.textContent = 'Voice is unavailable here. Type a search or choose a suggestion.';
  } else {
    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = true;
    recognition.continuous = true;
    let transcript = '';
    let previousSessions = '';
    let failed = false;
    recognition.onstart = () => {
      listening = true;
      if (!keepListening || disposed) { recognition.stop(); return; }
      mic.setAttribute('aria-pressed', 'true');
      mic.setAttribute('aria-label', 'Stop voice search');
      mic.title = 'Stop voice search';
      status.textContent = 'Listening… describe your ideal home. Tap the microphone to stop.';
    };
    recognition.onresult = event => {
      if (disposed || discardResults) return;
      const sessionText = Array.from(event.results).map(result => result[0].transcript).join(' ');
      transcript = [previousSessions, sessionText].filter(Boolean).join(' ');
      input.value = transcript;
    };
    recognition.onerror = event => {
      if (disposed) return;
      if (event.error === 'no-speech' && keepListening) {
        status.textContent = 'Still listening… speak whenever you are ready, or tap to stop.';
        return;
      }
      failed = true;
      keepListening = false;
      clearTimeout(restartTimer);
      const messages = {
        'not-allowed': 'Microphone access was blocked. Allow it in your browser settings, or type your search.',
        'service-not-allowed': 'Speech recognition is unavailable in this browser. Please type your search.',
        'audio-capture': 'No microphone was found. Connect one, or type your search.',
        'no-speech': 'No speech detected. Tap the microphone to try again.',
        'network': 'Speech recognition could not connect. Try again, or type your search.'
      };
      status.textContent = messages[event.error] || 'Voice input stopped. Try again, or type your search.';
    };
    const startRecognition = () => {
      if (!keepListening || disposed) return;
      try { recognition.start(); }
      catch {
        failed = true;
        stopCapture(true);
        status.textContent = 'Voice input could not start. Try again, or type your search.';
      }
    };
    recognition.onend = () => {
      listening = false;
      if (disposed) return;
      if (keepListening && !failed) {
        // Browser speech services may end a session even in continuous mode.
        // Keep completed text and start another session until the user stops.
        previousSessions = transcript;
        restartTimer = setTimeout(() => {
          restartTimer = null;
          startRecognition();
        }, 500);
        return;
      }
      mic.setAttribute('aria-pressed', 'false');
      mic.setAttribute('aria-label', 'Start voice search');
      mic.title = 'Speak your search';
      if (!failed) status.textContent = transcript ? 'Ready. Review your words, then select Find my home.' : 'No speech detected. Tap the microphone to try again.';
      if (transcript) input.focus();
    };
    mic.onclick = () => {
      if (keepListening) {
        stopCapture();
        status.textContent = transcript ? 'Ready. Review your words, then select Find my home.' : 'Voice input stopped. Tap the microphone to try again.';
        return;
      }
      transcript = ''; previousSessions = ''; failed = false; discardResults = false;
      keepListening = true;
      mic.setAttribute('aria-pressed', 'true');
      mic.setAttribute('aria-label', 'Stop voice search');
      mic.title = 'Stop voice search';
      startRecognition();
    };
  }
  return () => {
    disposed = true;
    keepListening = false;
    clearTimeout(restartTimer);
    if (recognition) { recognition.onend = null; recognition.onresult = null; recognition.onerror = null; recognition.onstart = null; recognition.abort(); }
    form.onsubmit = null; mic.onclick = null; input.oninput = null;
  };
}
