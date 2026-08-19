"""
test_errors.py
--------------
Tests for custom HTTP error handlers (400, 404, 500) and the user profile dashboard.
"""
from tests.test_base import BaseTestCase


class ErrorsAndProfileTestCase(BaseTestCase):
    """Verifies error page rendering and user account dashboard."""

    def test_custom_404_error_page(self):
        """GET request to a nonexistent URL returns custom 404 error page."""
        response = self.client.get('/this-route-does-not-exist')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Error 404', response.data)
        self.assertIn(b'Page Not Found', response.data)

    def test_error_400_preview(self):
        """GET /400 renders custom 400 Bad Request preview."""
        response = self.client.get('/400')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'400', response.data)

    def test_error_404_preview(self):
        """GET /404 renders custom 404 Not Found preview."""
        response = self.client.get('/404')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data)

    def test_error_500_preview(self):
        """GET /500 renders custom 500 Internal Server Error preview."""
        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'500', response.data)

    def test_profile_dashboard_authenticated(self):
        """GET /profile renders user account dashboard with digital passes and taste profile."""
        self.login('explorer@test.com', 'Password123!')
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Explorer', response.data)
        self.assertIn(b'Taste Profile', response.data)
        self.assertIn(b'Renaissance Art', response.data)
