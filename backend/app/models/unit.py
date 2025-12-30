"""Unit model."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Unit(Base, TimestampMixin):
    """Represents a unit within a property."""

    __tablename__ = "units"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    floor_area: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)

    tenant = relationship("Tenant", back_populates="units")
    property = relationship("Property", back_populates="units")
    meters = relationship("Meter", back_populates="unit", cascade="all, delete-orphan")
