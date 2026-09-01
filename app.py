"""
app.py
------
Main application factory for the Museum Ticketing & AI Guide application.
Initializes the Flask app, configures the SQLite database via raw sqlite3,
and registers blueprints.
"""
import os
import logging
from flask import Flask
from dotenv import load_dotenv
import database
from routes import main_bp
from auth import auth_bp


def create_app(test_config=None):
    """
    Application factory function.
    Loads environment variables, configures the database, and initializes plugins.
    Returns a configured Flask app instance.
    """
    load_dotenv()

    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO)

    # Configure default settings
    app.config['DATABASE'] = os.path.join(app.instance_path, 'app.db')
    app.config['SECRET_KEY'] = os.environ.get(
        'FLASK_SECRET_KEY', 'dev-secret-key-change-in-production'
    )

    # Apply test configuration overrides if provided
    if test_config is not None:
        app.config.update(test_config)

    # Register the raw sqlite3 database helpers
    database.init_app(app)

    # Create database tables if they don't exist
    with app.app_context():
        database.init_db()

    # Register Blueprints for routing
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Register custom error pages
    from flask import render_template

    @app.errorhandler(400)
    def bad_request_error(e):
        return render_template('400.html', error=e), 400

    @app.errorhandler(404)
    def not_found_error(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
