"""
test_database.py
----------------
Tests for database connection lifecycle, PRAGMA foreign_keys enforcement,
table creation, and relational cascade constraints.
"""
import sqlite3
import database
from tests.test_base import BaseTestCase


class DatabaseTestCase(BaseTestCase):
    """Verifies SQLite schema structure, foreign key enforcement, and database helpers."""

    def test_database_connection_and_pragma(self):
        """Verify get_db returns a valid connection with foreign keys enabled."""
        with self.app.app_context():
            db = database.get_db()
            self.assertIsInstance(db, sqlite3.Connection)
            # Verify PRAGMA foreign_keys is ON
            fk_status = db.execute("PRAGMA foreign_keys").fetchone()[0]
            self.assertEqual(fk_status, 1)

    def test_unique_email_constraint_on_users(self):
        """Verify unique constraint on users.email."""
        with self.app.app_context():
            db = database.get_db()
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute(
                    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                    ('Duplicate User', 'explorer@test.com', 'dummyhash')
                )
                db.commit()

    def test_unique_booking_code_constraint_on_tickets(self):
        """Verify unique constraint on tickets.booking_code."""
        with self.app.app_context():
            db = database.get_db()
            db.execute(
                """INSERT INTO tickets (booking_code, user_id, experience_id, visit_date, time_slot, total_price)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                ('EXP-2026-TEST', 1, 1, '2026-09-01', '09:30 - 11:00', 65.0)
            )
            db.commit()

            with self.assertRaises(sqlite3.IntegrityError):
                db.execute(
                    """INSERT INTO tickets (booking_code, user_id, experience_id, visit_date, time_slot, total_price)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    ('EXP-2026-TEST', 1, 1, '2026-09-02', '11:30 - 13:00', 65.0)
                )
                db.commit()

    def test_foreign_key_cascade_on_user_deletion(self):
        """Verify tickets are deleted when their parent user is deleted."""
        with self.app.app_context():
            db = database.get_db()
            db.execute(
                """INSERT INTO tickets (booking_code, user_id, experience_id, visit_date, time_slot, total_price)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                ('EXP-2026-DEL1', 1, 1, '2026-09-01', '09:30 - 11:00', 65.0)
            )
            db.commit()

            # Verify ticket exists
            ticket = db.execute("SELECT * FROM tickets WHERE booking_code = 'EXP-2026-DEL1'").fetchone()
            self.assertIsNotNone(ticket)

            # Delete user
            db.execute("DELETE FROM users WHERE id = 1")
            db.commit()

            # Verify ticket was cascade deleted
            ticket_after = db.execute("SELECT * FROM tickets WHERE booking_code = 'EXP-2026-DEL1'").fetchone()
            self.assertIsNone(ticket_after)

    def test_foreign_key_set_null_on_museum_deletion(self):
        """Verify experience museum_id is set to NULL when parent museum is deleted."""
        with self.app.app_context():
            db = database.get_db()
            # Delete museum 1
            db.execute("DELETE FROM museums WHERE id = 1")
            db.commit()

            # Experience should still exist, but museum_id should be NULL
            exp = db.execute("SELECT museum_id FROM experiences WHERE id = 1").fetchone()
            self.assertIsNotNone(exp)
            self.assertIsNone(exp['museum_id'])
