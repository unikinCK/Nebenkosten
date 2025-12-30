"""Service layer for settlements and settlement periods."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.models import AllocationKey
from app.services.allocation_service import AllocationError, calculate_allocations
from app.services.storage import settlements_repo


class SettlementError(ValueError):
    """Raised when settlement operations fail."""


def create_settlement(payload: dict[str, Any]) -> dict:
    payload = dict(payload)
    payload.setdefault("status", "open")
    payload.setdefault("allocations", [])
    payload.setdefault("closed_at", None)
    return settlements_repo.create(payload)


def get_settlement(settlement_id: int) -> dict | None:
    return settlements_repo.get(settlement_id)


def list_settlements() -> list[dict]:
    return settlements_repo.list()


def close_settlement(settlement_id: int) -> dict:
    settlement = settlements_repo.get(settlement_id)
    if not settlement:
        raise SettlementError("Settlement not found.")
    if settlement.get("status") == "closed":
        raise SettlementError("Settlement is already closed.")

    try:
        allocations = calculate_allocations(
            total_amount=settlement["total_amount"],
            units=settlement["units"],
            key=AllocationKey(settlement["allocation_key"]),
        )
    except AllocationError as exc:
        raise SettlementError(str(exc)) from exc

    settlement = dict(settlement)
    settlement["allocations"] = allocations
    settlement["status"] = "closed"
    settlement["closed_at"] = datetime.utcnow().isoformat()
    settlements_repo.update(settlement_id, settlement)
    return settlement


def export_settlement(settlement_id: int) -> dict:
    settlement = settlements_repo.get(settlement_id)
    if not settlement:
        raise SettlementError("Settlement not found.")
    if settlement.get("status") != "closed":
        raise SettlementError("Settlement must be closed before export.")
    return {
        "id": settlement["id"],
        "period_start": settlement["period_start"],
        "period_end": settlement["period_end"],
        "allocation_key": settlement["allocation_key"],
        "total_amount": settlement["total_amount"],
        "closed_at": settlement["closed_at"],
        "allocations": settlement["allocations"],
    }
