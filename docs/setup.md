# Setup

## Voraussetzungen

- Docker + Docker Compose
- Optional: Python 3.12 für lokale Backend-Entwicklung

## Lokale Nutzung mit Docker Compose

1. `.env.example` nach `.env` kopieren und Werte anpassen:

   ```bash
   cp .env.example .env
   ```

2. Services starten:

   ```bash
   docker compose up --build
   ```

3. Backend läuft unter `http://localhost:5000`.

## Lokale Backend-Entwicklung ohne Docker

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

## Produktiver Betrieb (Beispiel)

```bash
docker compose -f docker-compose.yml up --build -d
```

Passe `.env` für Produktionswerte (DB, Keycloak, Secrets) an und verwalte Secrets über dein Secret-Management-System.
