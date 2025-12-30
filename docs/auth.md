# Keycloak OIDC Setup

This project uses Keycloak for OIDC authentication.

## Realm & Client
1. Create a realm named `neb`.
2. Create a confidential client named `nebenkosten-backend`.
3. Enable **Standard Flow**.
4. Set **Valid Redirect URIs** to your backend URL (if applicable).

## Roles
Create the following roles in Keycloak:

- `admin`
- `manager`
- `owner`

Roles can be assigned as realm roles or as client roles on
`nebenkosten-backend`. Both are mapped by the backend.

## Token Mappers
Ensure the following claims are included in access tokens:
- `realm_access.roles`
- `resource_access.{client_id}.roles`

The default Keycloak configuration already includes these for access tokens.

## Backend Configuration
Set the following environment variables:

| Variable | Example | Purpose |
| --- | --- | --- |
| `OIDC_ISSUER` | `https://keycloak.example/realms/neb` | Token issuer |
| `OIDC_CLIENT_ID` | `nebenkosten-backend` | Audience |
| `OIDC_JWKS_URL` | `https://keycloak.example/realms/neb/protocol/openid-connect/certs` | JWKS endpoint |

The backend resolves these in `backend/app/config.py`.
