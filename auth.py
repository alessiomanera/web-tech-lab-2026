"""
auth.py
-------
Authentication blueprint managing user registration, login, logout, and session state.
Includes a decorator `login_required` to protect restricted routes.
Uses raw sqlite3 with parameterized queries for all database access.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database import get_db

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    """
    Decorator to ensure a user is logged in before accessing a route.
    Redirects to the login page if not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


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
        return redirect(url_for('main.home'))

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """
    Logs out the user by clearing all session data.
    """
    session.clear()
    return redirect(url_for('main.home'))
