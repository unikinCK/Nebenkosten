"""API blueprint registration."""

from __future__ import annotations

from flask import Blueprint, jsonify
from pydantic import ValidationError

from app.api.errors import ApiError, error_response
from app.api.invoices import invoices_bp
from app.api.meters import meters_bp
from app.api.readings import readings_bp
from app.api.settlements import settlements_bp


def create_api_blueprint() -> Blueprint:
    api_bp = Blueprint("api", __name__, url_prefix="/api")
    api_bp.register_blueprint(meters_bp)
    api_bp.register_blueprint(readings_bp)
    api_bp.register_blueprint(invoices_bp)
    api_bp.register_blueprint(settlements_bp)

    api_bp.register_error_handler(ApiError, error_response)
    api_bp.register_error_handler(ValidationError, _handle_validation_error)

    return api_bp


def _handle_validation_error(error: ValidationError):
    payload = {
        "error": {
            "code": "validation_error",
            "message": "Request validation failed.",
            "details": error.errors(),
        }
    }
    return jsonify(payload), 422
