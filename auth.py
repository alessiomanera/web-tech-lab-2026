"""
auth.py
-------
Authentication blueprint managing user registration, login, logout, and session state.
Includes a decorator `login_required` to protect restricted routes.
Uses raw sqlite3 with parameterized queries for all database access.
"""
import secrets
from urllib.parse import urlparse
from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, flash, abort, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database import get_db

auth_bp = Blueprint('auth', __name__)

# Methods that can change server state and therefore require a CSRF token.
CSRF_PROTECTED_METHODS = ('POST', 'PUT', 'PATCH', 'DELETE')


def csrf_token():
    """
    Returns this session's CSRF token, minting one on first use.

    Registered as a Jinja global so every page can embed it. The token lives in
    the signed session cookie: another origin's page can make the browser SEND
    our cookie, but the same-origin policy stops it READING the token out of
    our HTML — which is exactly what makes the comparison meaningful.
    """
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_urlsafe(32)
    return session['_csrf_token']


def csrf_protect():
    """
    Rejects any state-changing request that does not carry this session's CSRF
    token, supplied either as a hidden `csrf_token` form field or, for the JSON
    endpoints, an `X-CSRFToken` header. Registered as a before_request hook by
    create_app(), so it covers every blueprint without per-route decoration.

    Compared with `secrets.compare_digest` so the check takes constant time and
    cannot be probed a character at a time.
    """
    if request.method not in CSRF_PROTECTED_METHODS:
        return None

    submitted = request.form.get('csrf_token') or request.headers.get('X-CSRFToken')
    expected = session.get('_csrf_token')

    if not expected or not submitted or not secrets.compare_digest(submitted, expected):
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Invalid or missing security token. Please reload the page.'
            }), 400
        abort(400)

    return None


def login_required(f):
    """
    Decorator to ensure a user is logged in before accessing a route.
    Redirects to the login page if not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def _safe_next_target(raw_target):
    """
    Returns raw_target only if it is a same-site relative path.
    Blocks open-redirect attempts such as ?next=https://evil.example.com.
    """
    if not raw_target:
        return None
    parsed = urlparse(raw_target)
    if parsed.scheme or parsed.netloc:
        return None
    if not raw_target.startswith('/') or raw_target.startswith('//'):
        return None
    return raw_target


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    On POST, hashes the password and creates a new User in the database.
    """
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        password = request.form.get('password') or ''
        preferences = request.form.get('preferences')

        if not name or not email or not password:
            flash('Please fill in all required fields.')
            return redirect(url_for('auth.register'))

        db = get_db()

        # Check if user exists
        existing = db.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()

        if existing:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))

        db.execute(
            "INSERT INTO users (name, email, password_hash, preferences) VALUES (?, ?, ?, ?)",
            (name, email, generate_password_hash(password), preferences)
        )
        db.commit()

        # Retrieve the new user's id to log them in
        new_user = db.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()

        # Log them in automatically
        session['user_id'] = new_user['id']
        return redirect(url_for('main.home'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    On POST, verifies credentials against the database and establishes a session.
    """
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        password = request.form.get('password') or ''

        if not email or not password:
            flash('Please fill in all required fields.')
            return redirect(url_for('auth.login'))

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()

        if not user or not check_password_hash(user['password_hash'], password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        session['user_id'] = user['id']
        target = _safe_next_target(request.args.get('next') or request.form.get('next'))
        return redirect(target or url_for('main.home'))

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """
    Logs out the user by clearing all session data.
    """
    session.clear()
    return redirect(url_for('main.home'))
