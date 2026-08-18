"""
app.py
------
Main application factory for the Museum Ticketing & AI Guide application.
Initializes the Flask app, configures the SQLite database via raw sqlite3,
and registers blueprints.
"""
import os
from flask import Flask
from dotenv import load_dotenv
import database
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

    # Configure the SQLite database path and secret key
    app.config['DATABASE'] = os.path.join(app.instance_path, 'app.db')
    app.config['SECRET_KEY'] = os.environ.get(
        'FLASK_SECRET_KEY', 'dev-secret-key-change-in-production'
    )

    # Register the raw sqlite3 database helpers
    database.init_app(app)

    # Create database tables if they don't exist
    with app.app_context():
        database.init_db()

    # Register Blueprints for routing
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
