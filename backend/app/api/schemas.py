"""Pydantic schemas for request validation."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models import AllocationKey


class _BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class MeterCreate(_BaseSchema):
    label: str = Field(min_length=1)
    unit: Optional[str] = None


class ReadingCreate(_BaseSchema):
    meter_id: int = Field(gt=0)
    timestamp: datetime
    value: float = Field(gt=0)


class InvoiceCreate(_BaseSchema):
    vendor: str = Field(min_length=1)
    amount: float = Field(gt=0)
    period_start: datetime
    period_end: datetime
    description: Optional[str] = None

    @model_validator(mode="after")
    def validate_period(self):
        if self.period_end <= self.period_start:
            raise ValueError("period_end must be after period_start")
        return self


class SettlementUnitInput(_BaseSchema):
    unit_id: str = Field(min_length=1)
    living_area: float = Field(ge=0)
    consumption: float = Field(ge=0)
    persons: float = Field(ge=0)
    units: float = Field(ge=0)
    custom: float = Field(ge=0)


class SettlementCreate(_BaseSchema):
    period_start: datetime
    period_end: datetime
    allocation_key: AllocationKey
    total_amount: float = Field(ge=0)
    units: List[SettlementUnitInput] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_period(self):
        if self.period_end <= self.period_start:
            raise ValueError("period_end must be after period_start")
        return self
