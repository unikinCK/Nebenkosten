"""REST API endpoints for meter readings."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.api.errors import ApiError
from app.api.schemas import ReadingCreate
from app.services.storage import meters_repo, readings_repo

readings_bp = Blueprint("readings", __name__, url_prefix="/readings")


@readings_bp.get("")
def list_readings():
    return jsonify(readings_repo.list())


@readings_bp.post("")
def create_reading():
    payload = ReadingCreate.model_validate(request.get_json() or {})
    if not meters_repo.get(payload.meter_id):
        raise ApiError(400, "invalid_meter", "Meter does not exist.")
    reading = readings_repo.create(payload.model_dump())
    return jsonify(reading), 201


@readings_bp.get("/<int:reading_id>")
def get_reading(reading_id: int):
    reading = readings_repo.get(reading_id)
    if not reading:
        raise ApiError(404, "reading_not_found", "Reading not found.")
    return jsonify(reading)


@readings_bp.put("/<int:reading_id>")
def update_reading(reading_id: int):
    payload = ReadingCreate.model_validate(request.get_json() or {})
    if not meters_repo.get(payload.meter_id):
        raise ApiError(400, "invalid_meter", "Meter does not exist.")
    reading = readings_repo.update(reading_id, payload.model_dump())
    if not reading:
        raise ApiError(404, "reading_not_found", "Reading not found.")
    return jsonify(reading)


@readings_bp.delete("/<int:reading_id>")
def delete_reading(reading_id: int):
    deleted = readings_repo.delete(reading_id)
    if not deleted:
        raise ApiError(404, "reading_not_found", "Reading not found.")
    return "", 204
