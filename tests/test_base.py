"""
test_base.py
------------
Base test case providing setup and teardown of an isolated temporary SQLite database,
Flask test client configuration, and shared authentication helpers.
"""
import os
import re
import tempfile
import unittest
from werkzeug.security import generate_password_hash
import database
from app import create_app


class BaseTestCase(unittest.TestCase):
    """
    Base test case for all application unit and integration tests.
    Each test runs with an isolated temporary SQLite database.
    """

    def setUp(self):
        # Create a temporary file to use as the database
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.db')

        # Configure the test app instance
        self.app = create_app({
            'TESTING': True,
            'DATABASE': self.db_path,
            'SECRET_KEY': 'test-secret-key-do-not-use-in-production'
        })
        self.client = self.app.test_client()

        # Every state-changing request needs a CSRF token. `raw_post` is the
        # untouched client method — tests that exercise the CSRF guard itself
        # use it directly; `self.client.post` is wrapped below so the other
        # ~24 call sites keep reading as ordinary requests, exactly as a real
        # browser behaves once it has rendered a page.
        self.raw_post = self.client.post
        self.client.post = self._post_with_csrf

        # Seed initial test data
        with self.app.app_context():
            db = database.get_db()
            self._seed_test_data(db)

    def csrf_token(self):
        """
        Reads the CSRF token the way the browser does: out of the meta tag that
        base.html renders. Uses `/` because it does not consume flashed
        messages, which the login and register pages do.
        """
        html = self.client.get('/').get_data(as_text=True)
        match = re.search(r'name="csrf-token" content="([^"]+)"', html)
        return match.group(1) if match else None

    def _post_with_csrf(self, *args, **kwargs):
        """
        Attaches the session's CSRF token to a POST the same way the real
        front end does: a hidden form field for form submissions, an
        X-CSRFToken header for the JSON endpoints.
        """
        token = self.csrf_token()
        if token:
            if isinstance(kwargs.get('data'), dict):
                kwargs['data'] = {**kwargs['data'], 'csrf_token': token}
            else:
                headers = dict(kwargs.get('headers') or {})
                headers.setdefault('X-CSRFToken', token)
                kwargs['headers'] = headers
        return self.raw_post(*args, **kwargs)

    def tearDown(self):
        # Close file descriptor and remove the temporary database file
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            try:
                os.unlink(self.db_path)
            except PermissionError:
                pass

    def _seed_test_data(self, db):
        """Seeds standard test entities: a museum, experiences, and a default user."""
        # 1. Test User
        db.execute(
            """INSERT INTO users (name, email, password_hash, preferences)
               VALUES (?, ?, ?, ?)""",
            ('Test Explorer', 'explorer@test.com',
             generate_password_hash('Password123!'),
             '### Cultural Taste Profile\n- **Primary Interests:** Renaissance Art\n- **Favorite Cities:** Florence')
        )

        # 2. Test Museum
        db.execute(
            """INSERT INTO museums (name, description, location, city, image_url)
               VALUES (?, ?, ?, ?, ?)""",
            ('Galleria degli Uffizi', 'World famous art museum in Florence.', 'Piazzale degli Uffizi 6', 'Florence', '/static/images/museums/uffizi.jpg')
        )

        # 3. Test Experiences
        db.execute(
            """INSERT INTO experiences
               (museum_id, title, tagline, city, theme, duration_minutes, base_price,
                badge, included_items_json, available_addons_json, description, highlights, image_url, is_featured)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (1, 'Uffizi VIP Masterpieces Tour', 'Skip the line into Renaissance history', 'Florence', 'Renaissance Art',
             120, 65.0, 'Best Seller',
             '["Priority Entry", "Licensed Guide", "Headsets"]',
             '[{"id": "docent", "name": "Private Art Historian", "price": 40.0}, {"id": "audio", "name": "Digital Audio Guide", "price": 8.0}]',
             'A comprehensive curated visit through Botticelli, Leonardo, and Caravaggio.',
             'Botticelli Birth of Venus, Leonardo Annunciation',
             '/static/images/experiences/uffizi.jpg', 1)
        )

        db.execute(
            """INSERT INTO experiences
               (museum_id, title, tagline, city, theme, duration_minutes, base_price,
                badge, included_items_json, available_addons_json, description, highlights, image_url, is_featured)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (1, 'Colosseum & Roman Forum Twilight Walk', 'Explore Ancient Rome after dark', 'Rome', 'Ancient Rome',
             150, 55.0, 'Curators Choice',
             '["Arena Floor Access", "Gladiator Gate", "Forum Entry"]',
             '[{"id": "vr", "name": "VR Gladiator Reconstruction", "price": 15.0}]',
             'Walk the subterranean corridors and arena floor as twilight falls.',
             'Gladiator Arena, Underground Chambers, Arch of Titus',
             '/static/images/experiences/colosseum.jpg', 0)
        )
        db.commit()

    def register(self, name='New User', email='newuser@test.com', password='Password123!', preferences=None):
        """Helper to submit registration form."""
        return self.client.post('/register', data={
            'name': name,
            'email': email,
            'password': password,
            'preferences': preferences or ''
        }, follow_redirects=True)

    def login(self, email='explorer@test.com', password='Password123!'):
        """Helper to log in with credentials."""
        return self.client.post('/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        """Helper to log out the current session."""
        return self.client.get('/logout', follow_redirects=True)
