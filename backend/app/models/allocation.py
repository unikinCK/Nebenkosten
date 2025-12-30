"""Allocation models."""

from __future__ import annotations

from enum import Enum


class AllocationKey(str, Enum):
    """Supported allocation keys for settlement distribution."""

    LIVING_AREA = "living_area"
    CONSUMPTION = "consumption"
    PERSONS = "persons"
    UNITS = "units"
    CUSTOM = "custom"
