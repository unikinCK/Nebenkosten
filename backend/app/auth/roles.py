"""Role mapping helpers."""

from __future__ import annotations

from typing import Iterable

ROLES = ["admin", "manager", "owner"]


def extract_roles_from_claims(claims: dict, client_id: str) -> list[str]:
    """Extract known roles from Keycloak claims."""
    roles: set[str] = set()
    realm_roles = claims.get("realm_access", {}).get("roles", [])
    client_roles = (
        claims.get("resource_access", {}).get(client_id, {}).get("roles", [])
    )
    roles.update(realm_roles)
    roles.update(client_roles)
    return [role for role in roles if role in ROLES]


def has_required_role(user_roles: Iterable[str], required: Iterable[str]) -> bool:
    required_set = set(required)
    return any(role in required_set for role in user_roles)
