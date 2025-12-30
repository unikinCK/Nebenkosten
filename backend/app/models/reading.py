"""Reading model."""

from __future__ import annotations

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Reading(Base, TimestampMixin):
    """Represents a meter reading."""

    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    meter_id: Mapped[int] = mapped_column(ForeignKey("meters.id"), nullable=False)
    reading_date: Mapped[Date] = mapped_column(Date, nullable=False)
    value: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)

    tenant = relationship("Tenant", back_populates="readings")
    meter = relationship("Meter", back_populates="readings")
