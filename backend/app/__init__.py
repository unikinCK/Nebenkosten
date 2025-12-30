"""Flask application factory."""

from flask import Flask


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="change-me",
    )

    return app
