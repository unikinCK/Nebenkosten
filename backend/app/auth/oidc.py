"""OIDC verification helpers and decorators."""

from __future__ import annotations

from functools import lru_cache, wraps
import json
from typing import Iterable
from urllib.request import urlopen

from flask import abort, g, request
import jwt

from ..config import AuthConfig
from .roles import extract_roles_from_claims, has_required_role


@lru_cache(maxsize=4)
def fetch_jwks(jwks_url: str) -> dict:
    with urlopen(jwks_url) as response:
        return json.loads(response.read().decode("utf-8"))


def _select_public_key(token: str, jwks: dict) -> str:
    header = jwt.get_unverified_header(token)
    key_id = header.get("kid")
    for key in jwks.get("keys", []):
        if key.get("kid") == key_id:
            return jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
    raise jwt.InvalidKeyError("Matching JWKS key not found.")


def decode_token(token: str, config: AuthConfig) -> dict:
    jwks = fetch_jwks(config.jwks_url)
    public_key = _select_public_key(token, jwks)
    return jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=config.client_id,
        issuer=config.issuer,
    )


def require_auth(config: AuthConfig):
    """Decorator enforcing valid bearer token."""

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                abort(401)
            token = auth_header.split(" ", 1)[1].strip()
            try:
                claims = decode_token(token, config)
            except jwt.PyJWTError:
                abort(401)
            g.oidc_claims = claims
            g.roles = extract_roles_from_claims(claims, config.client_id)
            return view(*args, **kwargs)

        return wrapper

    return decorator


def require_role(required_roles: Iterable[str], config: AuthConfig):
    """Decorator enforcing role membership."""

    def decorator(view):
        @wraps(view)
        @require_auth(config)
        def wrapper(*args, **kwargs):
            if not has_required_role(g.roles, required_roles):
                abort(403)
            return view(*args, **kwargs)

        return wrapper

    return decorator
