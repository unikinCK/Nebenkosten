"""Error handling utilities for the API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from flask import jsonify


@dataclass
class ApiError(Exception):
    """Structured API error with HTTP status code."""

    status_code: int
    code: str
    message: str
    details: Any | None = None


def error_response(error: ApiError):
    payload = {
        "error": {
            "code": error.code,
            "message": error.message,
            "details": error.details,
        }
    }
    return jsonify(payload), error.status_code
