"""Application configuration."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AuthConfig:
    """Configuration values for OIDC authentication."""

    issuer: str
    client_id: str
    jwks_url: str

    @classmethod
    def from_env(cls) -> "AuthConfig":
        issuer = os.getenv("OIDC_ISSUER", "https://keycloak.local/realms/neb")
        client_id = os.getenv("OIDC_CLIENT_ID", "nebenkosten-backend")
        jwks_url = os.getenv(
            "OIDC_JWKS_URL",
            f"{issuer}/protocol/openid-connect/certs",
        )
        return cls(issuer=issuer, client_id=client_id, jwks_url=jwks_url)
