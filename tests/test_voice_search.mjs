import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const source = await readFile(new URL('../components/search_box/search.js', import.meta.url), 'utf8');
const {default: render} = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const element = () => ({dataset:{}, children:[], attributes:{}, value:'', textContent:'', focus(){this.focused=true}, setAttribute(key,value){this.attributes[key]=value}, replaceChildren(){this.children=[]}, appendChild(child){this.children.push(child)}});
function mount(supported=true) {
  const elements = Object.fromEntries(['input','form','.mic','.status','.suggestions'].map(key=>[key,element()]));
  let speech;
  class Recognition {
    constructor(){speech=this}
    start(){this.starts=(this.starts || 0)+1;this.onstart()}
    stop(){this.onend?.()}
    abort(){this.aborted=true;this.onend?.()}
  }
  globalThis.window={isSecureContext:true, SpeechRecognition:supported ? Recognition : undefined};
  globalThis.document={createElement:element};
  const events=[];
  const cleanup=render({parentElement:{querySelector:key=>elements[key]},data:{query:'',suggestions:['Near trails, 4 beds under $500k']},setTriggerValue:(...event)=>events.push(event)});
  return {elements,events,cleanup,speech};
}
const voice=mount();
voice.elements['.mic'].onclick();
assert.equal(voice.elements['.mic'].attributes['aria-pressed'],'true');
voice.speech.onresult({results:[[{transcript:'three bedrooms near coffee'}]]});
voice.elements['.mic'].onclick();
assert.equal(voice.elements.input.value,'three bedrooms near coffee');
assert.equal(voice.events.length,0,'Dictation must allow review before searching');
voice.elements.input.value='3 bedrooms near coffee under $450k';
voice.elements.form.onsubmit({preventDefault(){}});
assert.deepEqual(voice.events.at(-1),['search','3 bedrooms near coffee under $450k']);
voice.elements['.suggestions'].children[0].onclick();
assert.deepEqual(voice.events.at(-1),['search','Near trails, 4 beds under $500k']);
voice.speech.onerror({error:'not-allowed'});
voice.speech.onend();
assert.match(voice.elements['.status'].textContent,/blocked/);
voice.cleanup();
assert.equal(voice.speech.aborted,true);
const fallback=mount(false);
assert.equal(fallback.elements['.mic'].disabled,true);
fallback.elements.input.value='near tennis';
fallback.elements.form.onsubmit({preventDefault(){}});
assert.deepEqual(fallback.events,[['search','near tennis']]);
console.log('Voice transcript review, edited search, suggestions, permission error, cleanup, and typed fallback pass.');

const longVoice=mount();
longVoice.elements['.mic'].onclick();
assert.equal(longVoice.speech.continuous,true);
longVoice.speech.onresult({results:[[{transcript:'3 bedrooms'}]]});
longVoice.speech.onend();
await new Promise(resolve=>setTimeout(resolve,550));
assert.equal(longVoice.speech.starts,2,'Unexpected session end restarts recognition');
longVoice.speech.onresult({results:[[{transcript:'near coffee'}]]});
longVoice.speech.onresult({results:[[{transcript:'near coffee under $500k'}]]});
assert.equal(longVoice.elements.input.value,'3 bedrooms near coffee under $500k');
longVoice.speech.onerror({error:'no-speech'});
longVoice.speech.onend();
await new Promise(resolve=>setTimeout(resolve,550));
assert.equal(longVoice.speech.starts,3,'Silence must not end dictation');
longVoice.elements['.mic'].onclick();
await new Promise(resolve=>setTimeout(resolve,550));
assert.equal(longVoice.speech.starts,3,'Explicit Stop must not restart');
longVoice.cleanup();
const pending=mount();
pending.elements['.mic'].onclick();
pending.speech.onend();
pending.elements['.mic'].onclick();
await new Promise(resolve=>setTimeout(resolve,550));
assert.equal(pending.speech.starts,1,'Stop during restart delay cancels restart');
pending.cleanup();
const blocked=mount();
blocked.elements['.mic'].onclick();
blocked.speech.onerror({error:'not-allowed'});
blocked.speech.onend();
await new Promise(resolve=>setTimeout(resolve,550));
assert.equal(blocked.speech.starts,1,'Permission errors must not retry');
blocked.cleanup();
console.log('Continuous dictation, transcript preservation, silence recovery, manual Stop, and fatal error checks pass.');

const cleared=mount();
cleared.elements.input.value='near coffee';
cleared.elements.input.oninput();
assert.equal(cleared.events.length,0,'Editing nonempty text must not search automatically');
cleared.elements['.mic'].onclick();
cleared.elements.input.value='';
cleared.elements.input.oninput();
assert.deepEqual(cleared.events,[['search','']]);
assert.equal(cleared.speech.aborted,true,'Clearing must stop dictation');
assert.equal(cleared.elements['.mic'].attributes['aria-pressed'],'false');
cleared.cleanup();
console.log('Clearing input hides results and stops dictation.');
