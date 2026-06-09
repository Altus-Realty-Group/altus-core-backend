# Future App Auth Onboarding

Status: Draft / Pending Live Core DB Verification
Owner: Altus Core Backend
Applies to: ECC, Price Engine, Field App, Construction Manager, Investor Hub, Deal Room, Altus Core Admin, Future Apps
Canonical Repo: Altus-Realty-Group/altus-core-backend
Database Authority: Altus Core Supabase project srzwamukysmhiaaviwiv
Mutation Status: Documentation only; no DB writes

## Goal

New Altus apps MUST plug into Altus Core auth without creating a new identity system, new permanent auth provider, or duplicate user model.

## Plug-and-Play Onboarding Checklist

1. Add the app registry record.
2. Define the app key.
3. Define the internal access policy.
4. Define external eligibility.
5. Define app entitlements.
6. Define supported scope types.
7. Define the permission catalog.
8. Define backend middleware requirements.
9. Define route guards.
10. Define frontend session or me consumption.
11. Define audit events.
12. Define tests.
13. Define RLS requirements.
14. Define revocation behavior.

## Required App Registration Payload

```json
{
  "app_key": "future_app",
  "app_name": "Future App",
  "app_category": "custom",
  "enabled": true,
  "internal_only": false,
  "supports_external_users": true,
  "default_internal_access_policy": "approved_internal_default",
  "required_entitlement": "future_app.access",
  "route_metadata_json": {
    "app_root": "/future-app",
    "login_mode": "altus_core_session"
  },
  "domain_metadata_json": {
    "primary_host": "future.altus-realty.com"
  }
}
```

## Backend Middleware Requirements

Every new app MUST implement the shared checks in this order:

```text
requireSession()
requireAppEntitlement(app_key)
requirePermission(permission_key)
requireScope(scope_type, scope_id)
requireAssignmentIfNeeded(resource_type, resource_id)
```

App business logic MUST NOT run before entitlement and scope checks complete.

## Frontend Session or Me Consumption

Frontend apps MUST consume a safe `GET /auth/me` or `GET /session/me` payload.

Frontend apps MUST implement:

- app-shell guard
- route-level guard
- action-level guard for dangerous UI actions
- hidden navigation for unavailable apps

Frontend apps MUST NOT:

- hardcode user emails as admin
- store service-role credentials
- duplicate the canonical role list inside each app
- rely on hardcoded frontend-only role checks as the primary enforcement path

## Test Requirements

Every new app MUST ship tests for:

- unauthenticated route denial
- app entitlement denial
- permission denial
- scope denial
- assignment denial where applicable
- successful allowed path
- revoked entitlement behavior
- suspended user behavior
- RLS read isolation or equivalent backend data-scope enforcement
- RLS write isolation or equivalent backend data-scope enforcement

## Audit Requirements

Every new app MUST define:

- access allowed event
- access denied event
- entitlement grant event
- entitlement revoke event
- scope grant event
- scope revoke event
- sensitive action event

## Revocation Requirements

Every new app MUST define the effect of:

- user suspension
- app entitlement revocation
- scope revocation
- assignment revocation
- session invalidation

## New App Cannot Ship Until

- app registered
- entitlement created
- backend guard implemented
- frontend guard implemented
- RLS or backend data-scope enforcement implemented
- audit events implemented
- denial behavior tested
- internal and external test users validated
- app does not rely on hardcoded frontend role checks

## Non-Negotiable Rules

New apps MUST NOT require:

- a new auth provider
- a duplicate user table
- a one-off frontend login model
- a hardcoded app access list in the browser
- a separate ungoverned Supabase auth system
