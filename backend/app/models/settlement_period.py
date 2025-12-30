"""Settlement period model."""

from __future__ import annotations

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class SettlementPeriod(Base, TimestampMixin):
    """Represents a settlement period for a property."""

    __tablename__ = "settlement_periods"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"), nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)

    tenant = relationship("Tenant", back_populates="settlement_periods")
    property = relationship("Property", back_populates="settlement_periods")
    invoices = relationship("Invoice", back_populates="settlement_period", cascade="all, delete-orphan")
