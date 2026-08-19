"""
test_booking.py
---------------
Tests for the 4-Step Ticketing & Reservation Engine.
Verifies booking wizard rendering, pre-selection query parameters,
server-side input validation, pricing calculations, and ticket creation.
"""
from datetime import datetime, timedelta
import json
import database
from tests.test_base import BaseTestCase


class BookingTestCase(BaseTestCase):
    """Verifies booking wizard flow, RESTful API validation, and ticket persistence."""

    def setUp(self):
        super().setUp()
        # Log in default test user
        self.login('explorer@test.com', 'Password123!')

    def test_booking_page_get(self):
        """GET /booking renders the 4-step booking wizard."""
        response = self.client.get('/booking')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book Your Experience', response.data)
        self.assertIn(b'Package &amp; Add-ons', response.data)

    def test_booking_page_preselected_exp(self):
        """GET /booking?exp_id=1 pre-selects the specified experience."""
        response = self.client.get('/booking?exp_id=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Uffizi VIP Masterpieces Tour', response.data)

    def test_api_book_successful(self):
        """POST /api/book successfully creates a ticket with calculated total price and booking code."""
        future_date = (datetime.now().date() + timedelta(days=7)).strftime('%Y-%m-%d')
        selected_addons = [
            {'id': 'docent', 'name': 'Private Art Historian', 'price': 40.0},
            {'id': 'audio', 'name': 'Digital Audio Guide', 'price': 8.0}
        ]

        payload = {
            'experience_id': 1,
            'visit_date': future_date,
            'time_slot': '09:30 - 11:00',
            'guests_count': 2,
            'selected_addons': selected_addons
        }

        response = self.client.post(
            '/api/book',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['booking_code'].startswith('EXP-2026-'))

        # Pricing check: (base €65 + docent €40 + audio €8) * 2 guests = €226.00
        self.assertEqual(data['total_price'], '€226.00')

        # Verify record in database
        with self.app.app_context():
            db = database.get_db()
            ticket = db.execute(
                "SELECT * FROM tickets WHERE booking_code = ?",
                (data['booking_code'],)
            ).fetchone()
            self.assertIsNotNone(ticket)
            self.assertEqual(ticket['user_id'], 1)
            self.assertEqual(ticket['guests_count'], 2)
            self.assertEqual(ticket['total_price'], 226.0)
            self.assertEqual(ticket['status'], 'Confirmed')

    def test_api_book_past_date_rejected(self):
        """POST /api/book rejects visit dates in the past."""
        past_date = (datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')
        payload = {
            'experience_id': 1,
            'visit_date': past_date,
            'time_slot': '09:30 - 11:00',
            'guests_count': 1
        }
        response = self.client.post(
            '/api/book',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('Visit date cannot be in the past', data['error'])

    def test_api_book_invalid_guest_count(self):
        """POST /api/book rejects guest counts below 1 or above 6."""
        future_date = (datetime.now().date() + timedelta(days=7)).strftime('%Y-%m-%d')
        for invalid_count in [0, 7, -1, 'invalid']:
            payload = {
                'experience_id': 1,
                'visit_date': future_date,
                'time_slot': '09:30 - 11:00',
                'guests_count': invalid_count
            }
            response = self.client.post(
                '/api/book',
                data=json.dumps(payload),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 400)

    def test_api_book_invalid_time_slot(self):
        """POST /api/book rejects time slots outside the standard schedule."""
        future_date = (datetime.now().date() + timedelta(days=7)).strftime('%Y-%m-%d')
        payload = {
            'experience_id': 1,
            'visit_date': future_date,
            'time_slot': '03:00 - 04:00',  # Invalid slot
            'guests_count': 1
        }
        response = self.client.post(
            '/api/book',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('Invalid time slot', data['error'])

    def test_api_book_nonexistent_experience(self):
        """POST /api/book returns 404 for invalid experience ID."""
        future_date = (datetime.now().date() + timedelta(days=7)).strftime('%Y-%m-%d')
        payload = {
            'experience_id': 9999,
            'visit_date': future_date,
            'time_slot': '09:30 - 11:00',
            'guests_count': 1
        }
        response = self.client.post(
            '/api/book',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
