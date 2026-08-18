"""
database.py
-----------
Database connection helpers for raw sqlite3 access.
Provides get_db() for per-request connections, close_db() for teardown,
init_db() to run schema.sql, and init_app() to register with the Flask app.
"""
import os
import sqlite3
from flask import g, current_app


def get_db():
    """
    Returns a sqlite3 connection for the current request.
    Stores it on Flask's `g` object so the same connection is reused
    within a single request. Enables FOREIGN KEY enforcement and
    sets row_factory to sqlite3.Row for dict-like column access.
    """
    if 'db' not in g:
        db_path = current_app.config.get('DATABASE', 'instance/app.db')
        # Ensure the instance directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    """
    Closes the database connection at the end of the request.
    Registered as a teardown handler via init_app().
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """
    Initializes the database by executing schema.sql.
    Creates all tables if they do not already exist.
    """
    db = get_db()
    schema_path = os.path.join(current_app.root_path, 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        db.executescript(f.read())


def init_app(app):
    """
    Registers the database teardown handler with the Flask app.
    Call this from the application factory (create_app).
    """
    app.teardown_appcontext(close_db)
