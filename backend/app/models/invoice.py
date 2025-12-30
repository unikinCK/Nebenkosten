"""Invoice model."""

from __future__ import annotations

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Invoice(Base, TimestampMixin):
    """Represents an invoice for a settlement period."""

    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"), nullable=False)
    settlement_period_id: Mapped[int] = mapped_column(
        ForeignKey("settlement_periods.id"),
        nullable=False,
    )
    invoice_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    issued_at: Mapped[Date] = mapped_column(Date, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    tenant = relationship("Tenant", back_populates="invoices")
    property = relationship("Property", back_populates="invoices")
    settlement_period = relationship("SettlementPeriod", back_populates="invoices")
