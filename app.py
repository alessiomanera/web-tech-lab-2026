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
from auth import auth_bp, csrf_token, csrf_protect


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

    # Session cookie hardening. HttpOnly keeps the cookie away from JavaScript;
    # SameSite=Lax stops the browser attaching it to cross-site POSTs at all.
    # Current browsers default to Lax, but relying on a browser default is not
    # a decision — setting it here makes it one, and is the second layer under
    # the CSRF token below.
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Apply test configuration overrides if provided
    if test_config is not None:
        app.config.update(test_config)

    # Register the raw sqlite3 database helpers
    database.init_app(app)

    # Create database tables if they don't exist
    with app.app_context():
        database.init_db()

    # CSRF protection: every state-changing request must present the session
    # token, and every template can embed it via {{ csrf_token() }}.
    app.before_request(csrf_protect)
    app.jinja_env.globals['csrf_token'] = csrf_token

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
    # Debug mode is opt-in. With it on, Flask hands exceptions to the Werkzeug
    # debugger instead of the registered error handlers, so the branded
    # 500.html page never renders. Enable it deliberately while developing:
    #   Windows PowerShell:  $env:FLASK_DEBUG=1; python app.py
    #   macOS / Linux:       FLASK_DEBUG=1 python app.py
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')
