"""
test_catalog.py
---------------
Tests for the Experience & Museum Catalog Directory.
Verifies multi-criteria filtering, search keyword querying, and detail views.
"""
from tests.test_base import BaseTestCase


class CatalogTestCase(BaseTestCase):
    """Verifies catalog directory routes, dynamic SQL filters, and detail pages."""

    def test_home_page(self):
        """GET / renders the landing page with featured cultural packages."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Italy Experience', response.data)
        self.assertIn(b'Uffizi VIP Masterpieces Tour', response.data)

    def test_experiences_catalog_all(self):
        """GET /experiences renders the full catalog with all experiences."""
        response = self.client.get('/experiences')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Uffizi VIP Masterpieces Tour', response.data)
        self.assertIn(b'Colosseum &amp; Roman Forum Twilight Walk', response.data)

    def test_experiences_filter_by_city(self):
        """GET /experiences?city=Florence filters experiences strictly to Florence."""
        response = self.client.get('/experiences?city=Florence')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Uffizi VIP Masterpieces Tour', response.data)
        self.assertNotIn(b'Colosseum &amp; Roman Forum Twilight Walk', response.data)

    def test_experiences_filter_by_theme(self):
        """GET /experiences?theme=Ancient+Rome filters experiences strictly to Ancient Rome."""
        response = self.client.get('/experiences?theme=Ancient Rome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Colosseum &amp; Roman Forum Twilight Walk', response.data)
        self.assertNotIn(b'Uffizi VIP Masterpieces Tour', response.data)

    def test_experiences_search_query(self):
        """GET /experiences?q=Botticelli performs keyword search across highlights/title/description."""
        response = self.client.get('/experiences?q=Botticelli')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Uffizi VIP Masterpieces Tour', response.data)
        self.assertNotIn(b'Colosseum & Roman Forum Twilight Walk', response.data)

    def test_experience_detail_valid(self):
        """GET /experiences/<id> renders detailed page with full itinerary and perks."""
        response = self.client.get('/experiences/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Uffizi VIP Masterpieces Tour', response.data)
        self.assertIn(b'Botticelli Birth of Venus', response.data)
        self.assertIn(b'Private Art Historian', response.data)

    def test_experience_detail_not_found(self):
        """GET /experiences/<invalid_id> returns 404."""
        response = self.client.get('/experiences/999')
        self.assertEqual(response.status_code, 404)

    def test_museums_directory(self):
        """GET /museums renders the list of baseline cultural institutions."""
        response = self.client.get('/museums')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Galleria degli Uffizi', response.data)
