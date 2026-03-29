# Projektstatus / Roadmap

## Phase 1 – Fundament (aktueller Stand)

**Status:** weitgehend umgesetzt (ca. 75–80%).

### Bereits umgesetzt
- Flask-App mit API-Blueprint-Struktur.
- Grundlegende REST-Endpunkte für `meters`, `readings`, `invoices`, `settlements`.
- SQLAlchemy-Domainmodell für Mandanten, Objekte, Einheiten, Zähler, Ablesungen, Perioden usw.
- Alembic-Migrations-Setup inkl. Initial-Migration `0001_initial_schema`.
- Docker-Compose-Basis für Backend/Frontend ist vorhanden.
- OIDC-Konfigurationsbasis inkl. Rollen-Mapping (Dokumentation + Backend-Konfig).

### Noch offen für „Phase 1 abgeschlossen"
- API persistiert aktuell noch **in-memory** (Repository in `storage.py`) statt über SQLAlchemy/PostgreSQL.
- Fehlende echte DB-Integration in Service- und API-Layer (Sessions, Repositories, Transaktionen).
- PostgreSQL/Keycloak-Services im Compose-Stack ergänzen (derzeit nicht enthalten).
- Seed/Bootstrap-Daten und optional Health-/Readiness-Checks für DB.

## Nächste Schritte (Phase 1 -> Phase 2 Übergang)

1. **Persistenz umstellen**
   - In-Memory-Repositories schrittweise durch DB-Repositories ersetzen.
   - `SessionLocal` aus `app.db` in Services/API integrieren.

2. **Migrationen als Standard-Workflow verankern**
   - Bei Modeländerungen: `alembic revision --autogenerate -m "..."`.
   - Danach: `alembic upgrade head`.

3. **DB-Lebenszyklus dokumentieren und automatisieren**
   - Dev-Setup: Compose hochfahren + Migration ausführen.
   - Optional: Startscript, das beim Backend-Start Migrationen anstößt.

4. **Domänenlogik auf DB testen**
   - Integrations-Tests gegen PostgreSQL-Container.
   - Mindestabdeckung für CRUD + Settlement-Flow.

## Wie wird die DB erzeugt?

### A) Mit Docker Compose (empfohlen)
1. `.env` anlegen:
   ```bash
   cp .env.example .env
   ```
2. PostgreSQL bereitstellen (z. B. als zusätzlicher Compose-Service oder extern).
3. Stack starten:
   ```bash
   docker compose up --build
   ```
4. Migration ausführen (in separater Shell):
   ```bash
   docker compose exec backend alembic -c /app/migrations/alembic.ini upgrade head
   ```

Damit wird das aktuelle Schema in der angebundenen PostgreSQL-Datenbank angelegt.

### B) Lokal ohne Docker (Backend + externe PostgreSQL)
1. `DATABASE_URL` setzen (z. B. in `.env` oder Shell).
2. Python-Umgebung installieren.
3. Migration starten:
   ```bash
   cd backend
   alembic -c migrations/alembic.ini upgrade head
   ```
