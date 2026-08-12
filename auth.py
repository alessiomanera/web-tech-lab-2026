"""
auth.py
-------
Authentication blueprint managing user registration, login, logout, and session state.
Includes a decorator `login_required` to protect restricted routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import db, User

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
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        preferences = request.form.get('preferences')

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))

        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            preferences=preferences
        )
        db.session.add(new_user)
        db.session.commit()

        # Log them in automatically
        session['user_id'] = new_user.id
        return redirect(url_for('main.home'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    On POST, verifies credentials against the database and establishes a session.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        session['user_id'] = user.id
        return redirect(url_for('main.home'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """
    Logs out the user by clearing the session data (including chat history).
    """
    session.clear()
    return redirect(url_for('main.home'))
