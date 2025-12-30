import json

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import Flask, jsonify, g

from backend.app.auth.oidc import fetch_jwks, require_auth, require_role
from backend.app.config import AuthConfig


@pytest.fixture()
def rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


@pytest.fixture()
def auth_config():
    return AuthConfig(
        issuer="https://keycloak.example/realms/neb",
        client_id="nebenkosten-backend",
        jwks_url="https://keycloak.example/realms/neb/protocol/openid-connect/certs",
    )


@pytest.fixture()
def app(auth_config, monkeypatch, rsa_keys):
    private_key, public_key = rsa_keys
    jwk = jwt.algorithms.RSAAlgorithm.to_jwk(public_key)
    jwk_payload = {"keys": [{**json.loads(jwk), "kid": "test"}]}

    fetch_jwks.cache_clear()
    monkeypatch.setattr(
        "backend.app.auth.oidc.fetch_jwks",
        lambda _: jwk_payload,
    )

    app = Flask(__name__)

    @app.get("/protected")
    @require_auth(auth_config)
    def protected():
        return jsonify({"sub": g.oidc_claims["sub"], "roles": g.roles})

    @app.get("/admin")
    @require_role(["admin"], auth_config)
    def admin():
        return jsonify({"ok": True})

    app.config["PRIVATE_KEY"] = private_key
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


def _make_token(private_key, auth_config, roles=None):
    payload = {
        "sub": "user-123",
        "iss": auth_config.issuer,
        "aud": auth_config.client_id,
        "realm_access": {"roles": roles or []},
        "resource_access": {auth_config.client_id: {"roles": roles or []}},
    }
    return jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": "test"})


def test_require_auth_allows_valid_token(client, app, auth_config):
    token = _make_token(app.config["PRIVATE_KEY"], auth_config, roles=["owner"])
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.get_json()["roles"] == ["owner"]


def test_require_role_blocks_missing_role(client, app, auth_config):
    token = _make_token(app.config["PRIVATE_KEY"], auth_config, roles=["manager"])
    response = client.get(
        "/admin",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_require_auth_rejects_missing_token(client):
    response = client.get("/protected")
    assert response.status_code == 401
