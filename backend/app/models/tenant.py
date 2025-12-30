"""Tenant model."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Tenant(Base, TimestampMixin):
    """Represents a tenant (mandant)."""

    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)

    properties = relationship("Property", back_populates="tenant", cascade="all, delete-orphan")
    units = relationship("Unit", back_populates="tenant", cascade="all, delete-orphan")
    meters = relationship("Meter", back_populates="tenant", cascade="all, delete-orphan")
    readings = relationship("Reading", back_populates="tenant", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="tenant", cascade="all, delete-orphan")
    allocation_keys = relationship(
        "AllocationKey",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )
    settlement_periods = relationship(
        "SettlementPeriod",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="tenant", cascade="all, delete-orphan")
