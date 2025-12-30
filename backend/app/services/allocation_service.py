"""Business logic for allocating settlement amounts."""

from __future__ import annotations

from typing import Iterable

from app.models import AllocationKey


class AllocationError(ValueError):
    """Raised when allocation cannot be computed."""


def _select_weight(unit: dict, key: AllocationKey) -> float:
    if key == AllocationKey.LIVING_AREA:
        return float(unit.get("living_area", 0))
    if key == AllocationKey.CONSUMPTION:
        return float(unit.get("consumption", 0))
    if key == AllocationKey.PERSONS:
        return float(unit.get("persons", 0))
    if key == AllocationKey.UNITS:
        return float(unit.get("units", 0))
    if key == AllocationKey.CUSTOM:
        return float(unit.get("custom", 0))
    return 0.0


def calculate_allocations(
    total_amount: float,
    units: Iterable[dict],
    key: AllocationKey,
) -> list[dict]:
    """Calculate allocations for each unit based on the chosen key."""

    units_list = [dict(unit) for unit in units]
    weights = [_select_weight(unit, key) for unit in units_list]
    if total_amount < 0:
        raise AllocationError("Total amount must be non-negative.")
    if not units_list:
        raise AllocationError("At least one unit is required for allocation.")
    if any(weight < 0 for weight in weights):
        raise AllocationError("Allocation weights must be non-negative.")

    total_weight = sum(weights)
    if total_weight <= 0:
        raise AllocationError("Allocation weights sum to zero.")

    allocations = []
    for unit, weight in zip(units_list, weights, strict=True):
        share = weight / total_weight
        allocations.append(
            {
                "unit_id": unit["unit_id"],
                "weight": weight,
                "share": round(share, 6),
                "amount": round(total_amount * share, 2),
            }
        )
    return allocations
