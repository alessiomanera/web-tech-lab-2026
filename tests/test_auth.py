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

    def test_login_honours_relative_next_parameter(self):
        """After login the user lands on the page they originally requested."""
        response = self.client.post(
            '/login?next=/profile',
            data={'email': 'explorer@test.com', 'password': 'Password123!'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith('/profile'))

    def test_login_rejects_absolute_next_parameter(self):
        """An off-site next target is ignored (open-redirect protection)."""
        response = self.client.post(
            '/login?next=https://evil.example.com/steal',
            data={'email': 'explorer@test.com', 'password': 'Password123!'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('evil.example.com', response.headers['Location'])

    # ------------------------------------------------------------------
    # CSRF protection
    #
    # These use `self.raw_post` (the unwrapped test client) so the request
    # arrives without a token, which is exactly what a cross-site forgery
    # looks like, since another origin can make the browser send our session
    # cookie but cannot read the token out of our HTML.
    # ------------------------------------------------------------------

    def test_csrf_token_is_rendered_for_the_client(self):
        """Every page exposes the session token for forms and fetch calls."""
        html = self.client.get('/login').get_data(as_text=True)
        self.assertIn('name="csrf-token"', html)
        self.assertIn('name="csrf_token"', html)
        self.assertTrue(self.csrf_token())

    def test_csrf_blocks_form_post_without_token(self):
        """A form POST carrying no CSRF token is rejected."""
        response = self.raw_post(
            '/login', data={'email': 'explorer@test.com', 'password': 'Password123!'}
        )
        self.assertEqual(response.status_code, 400)

    def test_csrf_blocks_form_post_with_wrong_token(self):
        """A forged token does not pass the constant-time comparison."""
        self.csrf_token()  # establish a session token first
        response = self.raw_post(
            '/login',
            data={'email': 'explorer@test.com',
                  'password': 'Password123!',
                  'csrf_token': 'not-the-real-token'}
        )
        self.assertEqual(response.status_code, 400)

    def test_csrf_blocks_booking_post_without_token(self):
        """The booking wizard's POST is protected too, not just auth."""
        self.login()
        response = self.raw_post('/booking', data={'experience_id': 1})
        self.assertEqual(response.status_code, 400)

    def test_csrf_blocks_json_api_and_answers_in_json(self):
        """A JSON endpoint refuses an untokened POST and replies with JSON, not HTML."""
        self.login()
        response = self.raw_post(
            '/api/feedback', json={'booking_id': 1, 'rating': 5}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('security token', response.get_json()['error'])

    def test_csrf_allows_post_with_valid_token(self):
        """The same request succeeds once the token is presented."""
        response = self.raw_post(
            '/login',
            data={'email': 'explorer@test.com',
                  'password': 'Password123!',
                  'csrf_token': self.csrf_token()}
        )
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as sess:
            self.assertIn('user_id', sess)

    def test_csrf_does_not_interfere_with_get_requests(self):
        """Read-only requests are never blocked."""
        for path in ('/', '/experiences', '/museums', '/login', '/register'):
            self.assertEqual(self.client.get(path).status_code, 200, path)
