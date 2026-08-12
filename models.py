"""
models.py
---------
Database models for the Museum Ticketing & AI Guide application.
Defines User, Museum, Exhibition, and Ticket classes mapping to SQLite tables.
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """
    User model representing registered users.
    Stores email and hashed password.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    preferences = db.Column(db.Text, nullable=True) # JSON or comma-separated
    tickets = db.relationship('Ticket', backref='user', lazy=True)

class Museum(db.Model):
    """
    Museum model representing a cultural institution.
    Contains basic info like name, description, location, and an image URL.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(300), nullable=True)
    exhibitions = db.relationship('Exhibition', backref='museum', lazy=True)

class Exhibition(db.Model):
    """
    Exhibition model representing a specific event or collection hosted at a Museum.
    Linked to a Museum via museum_id foreign key.
    """
    id = db.Column(db.Integer, primary_key=True)
    museum_id = db.Column(db.Integer, db.ForeignKey('museum.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    tickets = db.relationship('Ticket', backref='exhibition', lazy=True)

class Ticket(db.Model):
    """
    Ticket model representing a user's booking for an Exhibition.
    Links a User and an Exhibition, tracking the booking status.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exhibition_id = db.Column(db.Integer, db.ForeignKey('exhibition.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Confirmed')
