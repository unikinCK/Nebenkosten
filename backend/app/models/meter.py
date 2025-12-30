"""Meter model."""

from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Meter(Base, TimestampMixin):
    """Represents a meter attached to a unit."""

    __tablename__ = "meters"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)
    meter_type: Mapped[str] = mapped_column(String(100), nullable=False)
    serial_number: Mapped[str | None] = mapped_column(String(100), nullable=True)

    tenant = relationship("Tenant", back_populates="meters")
    unit = relationship("Unit", back_populates="meters")
    readings = relationship("Reading", back_populates="meter", cascade="all, delete-orphan")
