"""Property model."""

from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Property(Base, TimestampMixin):
    """Represents a building or property."""

    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)

    tenant = relationship("Tenant", back_populates="properties")
    units = relationship("Unit", back_populates="property", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="property", cascade="all, delete-orphan")
    allocation_keys = relationship(
        "AllocationKey",
        back_populates="property",
        cascade="all, delete-orphan",
    )
    settlement_periods = relationship(
        "SettlementPeriod",
        back_populates="property",
        cascade="all, delete-orphan",
    )
