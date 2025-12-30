# Datenmodell (ER-Modell)

## Überblick

Die Anwendung nutzt PostgreSQL mit SQLAlchemy. Alle zentralen Tabellen sind
mandantenfähig über `tenant_id`. Das Datenmodell deckt Immobilien, Einheiten,
Zählerstände, Abrechnungszeiträume sowie Benutzer- und Auditdaten ab.

## Entitäten & Beziehungen

- **Tenant**
  - Hat viele `Property`, `Unit`, `Meter`, `Reading`, `Invoice`,
    `AllocationKey`, `SettlementPeriod`, `User`, `AuditLog`.
- **Property**
  - Gehört zu einem `Tenant`.
  - Hat viele `Unit`, `Invoice`, `AllocationKey`, `SettlementPeriod`.
- **Unit**
  - Gehört zu `Tenant` und `Property`.
  - Hat viele `Meter`.
- **Meter**
  - Gehört zu `Tenant` und `Unit`.
  - Hat viele `Reading`.
- **Reading**
  - Gehört zu `Tenant` und `Meter`.
- **SettlementPeriod**
  - Gehört zu `Tenant` und `Property`.
  - Hat viele `Invoice`.
- **Invoice**
  - Gehört zu `Tenant`, `Property`, `SettlementPeriod`.
- **AllocationKey**
  - Gehört zu `Tenant` und `Property`.
- **User**
  - Gehört zu `Tenant`.
  - Hat viele `AuditLog`.
- **AuditLog**
  - Gehört zu `Tenant`.
  - Optionaler Bezug zu `User`.

## Tabellen (Kernfelder)

| Tabelle | Wichtige Felder |
| --- | --- |
| `tenants` | `id`, `name`, `created_at`, `updated_at` |
| `properties` | `id`, `tenant_id`, `name`, `address` |
| `units` | `id`, `tenant_id`, `property_id`, `name`, `floor_area` |
| `meters` | `id`, `tenant_id`, `unit_id`, `meter_type`, `serial_number` |
| `readings` | `id`, `tenant_id`, `meter_id`, `reading_date`, `value` |
| `settlement_periods` | `id`, `tenant_id`, `property_id`, `start_date`, `end_date` |
| `invoices` | `id`, `tenant_id`, `property_id`, `settlement_period_id`, `issued_at`, `total_amount` |
| `allocation_keys` | `id`, `tenant_id`, `property_id`, `name`, `method` |
| `users` | `id`, `tenant_id`, `email`, `full_name`, `is_active` |
| `audit_logs` | `id`, `tenant_id`, `user_id`, `action`, `entity_type`, `entity_id`, `details` |

## Mehrmandantenfähigkeit

- Jede zentrale Tabelle trägt `tenant_id` und referenziert `tenants.id`.
- Dadurch können Daten mandantenspezifisch gefiltert und getrennt verwaltet werden.
