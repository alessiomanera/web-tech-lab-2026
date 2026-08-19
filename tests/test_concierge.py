"""
test_concierge.py
-----------------
Tests for the Grounded AI Cultural Concierge.
Verifies interactive chat interface rendering, heuristic fallback matcher,
actionable booking recommendation tags, dynamic taste memory extraction,
and taste profile resets.
"""
import json
from unittest.mock import patch, MagicMock
import database
from tests.test_base import BaseTestCase


class ConciergeTestCase(BaseTestCase):
    """Verifies AI Concierge conversational discovery, grounded RAG parsing, and memory lifecycle."""

    def setUp(self):
        super().setUp()
        self.login('explorer@test.com', 'Password123!')

    def test_concierge_page_loads(self):
        """GET /concierge renders the AI guide interface for authenticated users."""
        response = self.client.get('/concierge')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AI Cultural Concierge', response.data)
        self.assertIn(b'Taste Memory', response.data)

    def test_concierge_heuristic_fallback_matching_city(self):
        """POST /api/chat without Gemini API key uses grounded local heuristic matcher for Florence."""
        with patch.dict('os.environ', {'GEMINI_API_KEY': ''}):
            payload = {'message': 'I want to visit Florence and see Renaissance art.'}
            response = self.client.post(
                '/api/chat',
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('response', data)
            self.assertIn('Uffizi VIP Masterpieces Tour', data['response'])
            # Verify recommendation card trigger tag
            self.assertIn('[RECOMMEND:', data['response'])
            self.assertIn('id=1', data['response'])

    def test_concierge_heuristic_fallback_matching_theme(self):
        """POST /api/chat matches Ancient Rome theme accurately."""
        with patch.dict('os.environ', {'GEMINI_API_KEY': ''}):
            payload = {'message': 'Tell me about Ancient Rome gladiators.'}
            response = self.client.post(
                '/api/chat',
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('Colosseum & Roman Forum Twilight Walk', data['response'])
            self.assertIn('id=2', data['response'])

    def test_concierge_empty_message_rejected(self):
        """POST /api/chat rejects empty or whitespace-only messages."""
        payload = {'message': '   '}
        response = self.client.post(
            '/api/chat',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    @patch('routes._call_gemini_concierge')
    def test_concierge_gemini_rag_and_taste_memory_update(self, mock_gemini):
        """POST /api/chat with Gemini RAG extracts updated taste profile and persists it to SQLite."""
        mock_response_text = (
            "Benvenuto! For an extraordinary visit, I recommend the Uffizi VIP tour.\n\n"
            "[RECOMMEND: id=1, title=\"Uffizi VIP Masterpieces Tour\", city=\"Florence\", price=65.00]"
        )
        mock_updated_profile = (
            "### Cultural Taste Profile\n"
            "- **Primary Interests:** Botticelli, Renaissance Painting\n"
            "- **Visit Pacing:** Unrushed & Curated\n"
            "- **Favorite Cities:** Florence"
        )
        mock_gemini.return_value = (mock_response_text, mock_updated_profile)

        with patch.dict('os.environ', {'GEMINI_API_KEY': 'mock_valid_key'}):
            payload = {'message': 'I love Botticelli and want an unrushed pace in Florence.'}
            response = self.client.post(
                '/api/chat',
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('Uffizi VIP Masterpieces Tour', data['response'])
            self.assertEqual(data['updated_profile'], mock_updated_profile)

            # Verify SQLite database updated
            with self.app.app_context():
                db = database.get_db()
                user = db.execute("SELECT preferences FROM users WHERE id = 1").fetchone()
                self.assertEqual(user['preferences'], mock_updated_profile)

    def test_reset_taste_memory(self):
        """POST /api/profile/reset-memory clears user's cultural taste profile."""
        response = self.client.post('/api/profile/reset-memory')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])

        with self.app.app_context():
            db = database.get_db()
            user = db.execute("SELECT preferences FROM users WHERE id = 1").fetchone()
            self.assertIsNone(user['preferences'])
