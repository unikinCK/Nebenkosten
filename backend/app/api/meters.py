"""REST API endpoints for meters."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.api.errors import ApiError
from app.api.schemas import MeterCreate
from app.services.storage import meters_repo

meters_bp = Blueprint("meters", __name__, url_prefix="/meters")


@meters_bp.get("")
def list_meters():
    return jsonify(meters_repo.list())


@meters_bp.post("")
def create_meter():
    payload = MeterCreate.model_validate(request.get_json() or {})
    meter = meters_repo.create(payload.model_dump())
    return jsonify(meter), 201


@meters_bp.get("/<int:meter_id>")
def get_meter(meter_id: int):
    meter = meters_repo.get(meter_id)
    if not meter:
        raise ApiError(404, "meter_not_found", "Meter not found.")
    return jsonify(meter)


@meters_bp.put("/<int:meter_id>")
def update_meter(meter_id: int):
    payload = MeterCreate.model_validate(request.get_json() or {})
    meter = meters_repo.update(meter_id, payload.model_dump())
    if not meter:
        raise ApiError(404, "meter_not_found", "Meter not found.")
    return jsonify(meter)


@meters_bp.delete("/<int:meter_id>")
def delete_meter(meter_id: int):
    deleted = meters_repo.delete(meter_id)
    if not deleted:
        raise ApiError(404, "meter_not_found", "Meter not found.")
    return "", 204
