"""
app.py
------
Main application factory for the Museum Ticketing & AI Guide application.
Initializes the Flask app, configures the SQLite database, and registers blueprints.
"""
import os
from flask import Flask
from dotenv import load_dotenv
from models import db
from routes import main_bp
from auth import auth_bp

def create_app():
    """
    Application factory function.
    Loads environment variables, configures the database, and initializes plugins.
    Returns a configured Flask app instance.
    """
    load_dotenv()
    
    app = Flask(__name__)
    
    # Configure the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

    # Initialize extensions (SQLAlchemy)
    db.init_app(app)

    # Register Blueprints for routing
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
