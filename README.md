# Nebenkosten
WebApp, um als Vermieter Mietnebenkosten abzurechnen.

# Anforderungen
## Architektur
- Docker-Container (lokal + produktiv nutzbar)
- Python (Flask, neueste stabile Version)
- geeignete Open-Source-Datenbank (z. B. PostgreSQL)
- Login / Benutzerverwaltung via Keycloak (OIDC)
- vollständig AI-generierter Code
- Test-Pipeline (Unit-, Integrations- und ggf. E2E-Tests)
- Dokumentation (Setup, Betrieb, Benutzerhandbuch, API)

## Funktionen
- Zählerstände erfassen (Heizung, Strom, Wasser, Wärmezähler etc.)
- Rechnungen erfassen (Mietnebenkosten, Strom, Wasser)
- Nebenkosten anhand verschiedener Schlüssel (Wohnfläche, Verbrauch, Personen, Einheiten, benutzerdefiniert) auf Mieter verteilen
- Basis-Mieterverwaltung
- Abrechnungsperioden verwalten (Jahr/Monat, Abschluss, Export)
- Auswertungen/Reports (PDF-Export, Zusammenfassung je Mieter)
- Rechte/Rollen (z. B. Verwalter, Eigentümer)
- Datenimport/-export (CSV/Excel)
- Protokollierung/Audit-Log wichtiger Änderungen
- Mehrmandantenfähigkeit (mehrere Objekte/Immobilien)
- welche weiteren Funktionen sinnvoll?
