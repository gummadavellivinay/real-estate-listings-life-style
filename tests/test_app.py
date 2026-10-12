"""Exercise the frontend search event through Streamlit's widget protocol."""
import json
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
from streamlit.components.v2.bidi_component.main import _make_trigger_id


class SearchUITests(unittest.TestCase):
    def test_search_event_and_reset(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertFalse(app.get('image'))
        self.assertFalse(app.tabs)
        self.assertFalse(app.selectbox)
        component = app.get('bidi_component')[0]
        widgets = app._tree.get_widget_states()
        state = widgets.widgets.add()
        state.id = component.proto.id
        state.json_value = '{}'
        event = widgets.widgets.add()
        event.id = _make_trigger_id(component.proto.id, 'events')
        query = 'Near trails and gym, 4 beds under $500k'
        event.json_trigger_value = json.dumps([{'event': 'search', 'value': query}])
        app._run(widgets, timeout=30)
        self.assertFalse(app.exception)
        self.assertTrue(app.session_state['has_searched'])
        self.assertEqual(len(app.get('image')), 12)
        self.assertEqual(app.selectbox(key='sort').label, 'Sort homes')
        self.assertEqual(app.session_state['beds'], 4)
        self.assertEqual(app.session_state['max_price'], 500000)
        self.assertEqual(app.session_state['lifestyles'], ['Trails & cycling', 'Gym & fitness'])
        self.assertEqual(json.loads(app.get('bidi_component')[0].proto.json)['query'], query)
        app.run()
        self.assertFalse(app.exception)
        component = app.get('bidi_component')[0]
        widgets = app._tree.get_widget_states()
        state = widgets.widgets.add()
        state.id = component.proto.id
        state.json_value = '{}'
        event = widgets.widgets.add()
        event.id = _make_trigger_id(component.proto.id, 'events')
        event.json_trigger_value = json.dumps([{'event': 'search', 'value': ''}])
        app._run(widgets, timeout=30)
        self.assertFalse(app.exception)
        self.assertFalse(app.session_state['has_searched'])
        self.assertEqual(app.session_state['query'], '')
        self.assertFalse(app.get('image'))
        self.assertFalse(app.tabs)
        self.assertEqual(app.session_state['beds'], 0)
        self.assertEqual(app.session_state['max_price'], 1000000)
        self.assertEqual(app.session_state['lifestyles'], [])
        self.assertEqual(app.session_state['minutes'], 10)
        next(button for button in app.button if button.label == 'Reset filters').click().run()
        self.assertEqual(app.session_state['query'], '')
        self.assertEqual(app.session_state['beds'], 0)
        self.assertFalse(app.get('image'))
        self.assertFalse(app.tabs)
