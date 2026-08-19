"""
test_feedback.py
----------------
Tests for the post-visit rating and feedback submission loop.
Verifies validation, user ownership constraints, and database updates.
"""
import json
import database
from tests.test_base import BaseTestCase


class FeedbackTestCase(BaseTestCase):
    """Verifies feedback API endpoints, user ownership enforcement, and database updates."""

    def setUp(self):
        super().setUp()
        self.login('explorer@test.com', 'Password123!')

        # Create a confirmed ticket for test user 1
        with self.app.app_context():
            db = database.get_db()
            db.execute(
                """INSERT INTO tickets (id, booking_code, user_id, experience_id, visit_date, time_slot, total_price, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (10, 'EXP-2026-FDBK', 1, 1, '2026-08-01', '09:30 - 11:00', 65.0, 'Confirmed')
            )
            # Create a ticket belonging to user 2
            db.execute(
                """INSERT INTO users (id, name, email, password_hash)
                   VALUES (?, ?, ?, ?)""",
                (2, 'Other User', 'other@test.com', 'dummyhash')
            )
            db.execute(
                """INSERT INTO tickets (id, booking_code, user_id, experience_id, visit_date, time_slot, total_price, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (11, 'EXP-2026-OTH1', 2, 1, '2026-08-01', '09:30 - 11:00', 65.0, 'Confirmed')
            )
            db.commit()

    def test_feedback_successful(self):
        """POST /api/feedback saves rating and review comment for the user's booking."""
        payload = {
            'booking_id': 10,
            'rating': 5,
            'comment': 'Outstanding docent tour! The Botticelli room was breathtaking.'
        }
        response = self.client.post(
            '/api/feedback',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])

        # Verify in SQLite database
        with self.app.app_context():
            db = database.get_db()
            ticket = db.execute("SELECT * FROM tickets WHERE id = 10").fetchone()
            self.assertEqual(ticket['feedback_rating'], 5)
            self.assertEqual(ticket['feedback_text'], 'Outstanding docent tour! The Botticelli room was breathtaking.')
            self.assertIsNotNone(ticket['feedback_date'])

    def test_feedback_missing_rating_or_id(self):
        """POST /api/feedback rejects payload missing booking_id or rating."""
        payload = {'booking_id': 10}  # Missing rating
        response = self.client.post(
            '/api/feedback',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_feedback_ownership_security(self):
        """POST /api/feedback rejects review attempt on another user's booking (404 Not Found)."""
        payload = {
            'booking_id': 11,  # Belongs to user 2
            'rating': 5,
            'comment': 'Unauthorized review attempt'
        }
        response = self.client.post(
            '/api/feedback',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
