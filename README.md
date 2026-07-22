# altus-core-backend

> **REPOSITORY STATUS: FROZEN PENDING RETIREMENT**

This repository is no longer an active Altus backend development repository.

The only canonical backend repository for the Altus Platform is:

```text
Altus-Realty-Group/altus-control-plane
```

## Effective Immediately

Do not open or implement new work here involving:

- backend runtime features
- API routes or contracts
- Supabase/Postgres schema or migrations
- authentication or session logic
- Azure Functions or deployment changes
- shared integrations
- backend governance or CI/CD controls

All such work must be created in `Altus-Realty-Group/altus-control-plane`.

## Permitted Changes During Freeze

Until this repository is archived or terminated, changes are limited to:

- migration verification
- retirement and archival documentation
- recovery of unique material into `altus-control-plane`
- explicit cleanup authorized by the Control Plane retirement issue

## Historical Purpose

This repository previously housed Enterprise Asset Master and Azure Functions backend work. Its durable and approved responsibilities are being consolidated into Altus Control Plane.

This repository remains available temporarily for historical reference and uniqueness auditing only. It must not be treated as deployment authority, schema authority, API authority, authentication authority, or source of truth for current backend development.

## Retirement Tracking

Retirement is tracked in [Altus Control Plane Issue #7: Retire legacy Altus backend repositories](https://github.com/Altus-Realty-Group/altus-control-plane/issues/7).

## Final Rule

New backend work committed here is non-canonical and must be rejected or migrated to `altus-control-plane`.
