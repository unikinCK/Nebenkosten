"""Flask application factory."""

from flask import Flask

from .config import AuthConfig


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="change-me",
        AUTH_CONFIG=AuthConfig.from_env(),
    )

    return app
