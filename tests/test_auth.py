"""
test_auth.py
------------
Tests for user registration, authentication, password hashing, session state,
and @login_required route protection.
"""
from werkzeug.security import check_password_hash
import database
from tests.test_base import BaseTestCase


class AuthTestCase(BaseTestCase):
    """Verifies authentication logic, password security, and session management."""

    def test_register_page_loads(self):
        """GET /register should return 200 OK."""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Account', response.data)

    def test_register_successful(self):
        """POST /register with valid parameters creates a user and establishes session."""
        response = self.register('Marco Polo', 'marco@venice.it', 'Secret123!')
        self.assertEqual(response.status_code, 200)

        # Verify in database that password was hashed
        with self.app.app_context():
            db = database.get_db()
            user = db.execute("SELECT * FROM users WHERE email = 'marco@venice.it'").fetchone()
            self.assertIsNotNone(user)
            self.assertEqual(user['name'], 'Marco Polo')
            self.assertNotEqual(user['password_hash'], 'Secret123!')
            self.assertTrue(check_password_hash(user['password_hash'], 'Secret123!'))

    def test_register_duplicate_email(self):
        """POST /register with existing email flashes an error and does not duplicate."""
        response = self.register('Duplicate', 'explorer@test.com', 'Pass123!')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email address already exists', response.data)

    def test_register_missing_fields(self):
        """POST /register with missing required fields fails validation."""
        response = self.client.post('/register', data={
            'name': '',
            'email': 'incomplete@test.com',
            'password': ''
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please fill in all required fields', response.data)

    def test_login_page_loads(self):
        """GET /login should return 200 OK."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)

    def test_login_successful(self):
        """POST /login with valid credentials logs the user in."""
        response = self.login('explorer@test.com', 'Password123!')
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('user_id'), 1)

    def test_login_wrong_password(self):
        """POST /login with incorrect password fails with error message."""
        response = self.login('explorer@test.com', 'WrongPassword!')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please check your login details', response.data)
        with self.client.session_transaction() as sess:
            self.assertIsNone(sess.get('user_id'))

    def test_login_nonexistent_email(self):
        """POST /login with unregistered email fails."""
        response = self.login('nobody@nowhere.com', 'Password123!')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please check your login details', response.data)

    def test_logout(self):
        """GET /logout clears user session."""
        self.login('explorer@test.com', 'Password123!')
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertIsNone(sess.get('user_id'))

    def test_login_required_protection(self):
        """Protected routes redirect unauthenticated users to /login."""
        protected_routes = ['/booking', '/concierge', '/profile']
        for route in protected_routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login', response.headers['Location'])
