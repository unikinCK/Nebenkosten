"""REST API endpoints for settlements."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.api.errors import ApiError
from app.api.schemas import SettlementCreate
from app.services import SettlementError
from app.services.settlement_service import (
    close_settlement,
    create_settlement,
    export_settlement,
    get_settlement,
    list_settlements,
)

settlements_bp = Blueprint("settlements", __name__, url_prefix="/settlements")


@settlements_bp.get("")
def list_all_settlements():
    return jsonify(list_settlements())


@settlements_bp.post("")
def create_new_settlement():
    payload = SettlementCreate.model_validate(request.get_json() or {})
    settlement = create_settlement(payload.model_dump())
    return jsonify(settlement), 201


@settlements_bp.get("/<int:settlement_id>")
def get_settlement_by_id(settlement_id: int):
    settlement = get_settlement(settlement_id)
    if not settlement:
        raise ApiError(404, "settlement_not_found", "Settlement not found.")
    return jsonify(settlement)


@settlements_bp.post("/<int:settlement_id>/close")
def close_settlement_period(settlement_id: int):
    try:
        settlement = close_settlement(settlement_id)
    except SettlementError as exc:
        raise ApiError(400, "settlement_close_failed", str(exc)) from exc
    return jsonify(settlement)


@settlements_bp.get("/<int:settlement_id>/export")
def export_settlement_period(settlement_id: int):
    try:
        export_payload = export_settlement(settlement_id)
    except SettlementError as exc:
        raise ApiError(400, "settlement_export_failed", str(exc)) from exc
    return jsonify(export_payload)
