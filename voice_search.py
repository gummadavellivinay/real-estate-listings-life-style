"""Accessible search UI with browser-native dictation and suggested queries."""
from pathlib import Path
import streamlit as st

ASSETS = Path(__file__).parent / 'components' / 'search_box'
SUGGESTIONS = [
    '3 beds near tennis and coffee, under $550k',
    'Near trails and gym, 4 beds under $500k',
    'Close to Whole Foods and coffee under $480k',
    'Near dog parks and restaurants, 3 beds under $450k',
    '4 beds, highway access, close to hospital under $520k',
]
search_box = st.components.v2.component(
    'home_voice_search',
    html=(ASSETS / 'search.html').read_text(),
    css=(ASSETS / 'search.css').read_text(),
    js=(ASSETS / 'search.js').read_text(),
)
