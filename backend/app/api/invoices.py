"""REST API endpoints for invoices."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.api.errors import ApiError
from app.api.schemas import InvoiceCreate
from app.services.storage import invoices_repo

invoices_bp = Blueprint("invoices", __name__, url_prefix="/invoices")


@invoices_bp.get("")
def list_invoices():
    return jsonify(invoices_repo.list())


@invoices_bp.post("")
def create_invoice():
    payload = InvoiceCreate.model_validate(request.get_json() or {})
    invoice = invoices_repo.create(payload.model_dump())
    return jsonify(invoice), 201


@invoices_bp.get("/<int:invoice_id>")
def get_invoice(invoice_id: int):
    invoice = invoices_repo.get(invoice_id)
    if not invoice:
        raise ApiError(404, "invoice_not_found", "Invoice not found.")
    return jsonify(invoice)


@invoices_bp.put("/<int:invoice_id>")
def update_invoice(invoice_id: int):
    payload = InvoiceCreate.model_validate(request.get_json() or {})
    invoice = invoices_repo.update(invoice_id, payload.model_dump())
    if not invoice:
        raise ApiError(404, "invoice_not_found", "Invoice not found.")
    return jsonify(invoice)


@invoices_bp.delete("/<int:invoice_id>")
def delete_invoice(invoice_id: int):
    deleted = invoices_repo.delete(invoice_id)
    if not deleted:
        raise ApiError(404, "invoice_not_found", "Invoice not found.")
    return "", 204
