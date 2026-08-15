"""
models.py
---------
Database models for the Museum Ticketing & AI Cultural Guide application.
Defines User, Museum, Exhibition, Experience, and Booking (Ticket) classes mapping to SQLite tables.
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    """
    User model representing registered visitors.
    Stores authentication details and an evolving Markdown Cultural Taste Profile.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    preferences = db.Column(db.Text, nullable=True) # Stores Markdown Cultural Taste Profile
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"


class Museum(db.Model):
    """
    Museum model representing a cultural institution or heritage site.
    """
    __tablename__ = 'museums'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False, default="Italy")
    image_url = db.Column(db.String(500), nullable=True)

    exhibitions = db.relationship('Exhibition', backref='museum', lazy=True, cascade="all, delete-orphan")
    experiences = db.relationship('Experience', backref='museum', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Museum {self.name}>"


class Exhibition(db.Model):
    """
    Exhibition model representing a specific exhibition hosted at a Museum.
    """
    __tablename__ = 'exhibitions'

    id = db.Column(db.Integer, primary_key=True)
    museum_id = db.Column(db.Integer, db.ForeignKey('museums.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Exhibition {self.title}>"


class Experience(db.Model):
    """
    Experience model representing a pre-configured, curated cultural package.
    Includes duration, price, badge, included items, and customizable add-ons.
    """
    __tablename__ = 'experiences'

    id = db.Column(db.Integer, primary_key=True)
    museum_id = db.Column(db.Integer, db.ForeignKey('museums.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    tagline = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    theme = db.Column(db.String(100), nullable=False) # e.g., Renaissance, Ancient History, Baroque
    duration_minutes = db.Column(db.Integer, nullable=False, default=120)
    base_price = db.Column(db.Float, nullable=False, default=25.0)
    badge = db.Column(db.String(100), nullable=True) # e.g. "Best Seller", "Skip-The-Line"
    
    included_items_json = db.Column(db.Text, nullable=False, default="[]") # JSON list of strings
    available_addons_json = db.Column(db.Text, nullable=False, default="[]") # JSON list of addon objects
    
    description = db.Column(db.Text, nullable=False)
    highlights = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)

    bookings = db.relationship('Booking', backref='experience', lazy=True)

    @property
    def included_items(self):
        """Returns included items as Python list."""
        try:
            return json.loads(self.included_items_json) if self.included_items_json else []
        except Exception:
            return []

    @property
    def available_addons(self):
        """Returns available add-ons as Python list of dicts."""
        try:
            return json.loads(self.available_addons_json) if self.available_addons_json else []
        except Exception:
            return []

    def __repr__(self):
        return f"<Experience {self.title} ({self.city})>"


class Booking(db.Model):
    """
    Booking model representing a confirmed cultural reservation with add-ons and feedback.
    """
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    booking_code = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    experience_id = db.Column(db.Integer, db.ForeignKey('experiences.id'), nullable=False)
    
    visit_date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(100), nullable=False) # e.g. "10:00 - 11:30"
    guests_count = db.Column(db.Integer, nullable=False, default=1)
    
    selected_addons_json = db.Column(db.Text, nullable=False, default="[]") # JSON array
    total_price = db.Column(db.Float, nullable=False, default=0.0)
    
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Confirmed') # Confirmed, Completed, Cancelled
    
    # Feedback & Rating
    feedback_rating = db.Column(db.Integer, nullable=True) # 1 to 5
    feedback_text = db.Column(db.Text, nullable=True)
    feedback_date = db.Column(db.DateTime, nullable=True)

    @property
    def selected_addons(self):
        """Returns selected add-ons as Python list."""
        try:
            return json.loads(self.selected_addons_json) if self.selected_addons_json else []
        except Exception:
            return []

    def __repr__(self):
        return f"<Booking {self.booking_code} - User {self.user_id}>"

# Backward compatibility alias
Ticket = Booking
