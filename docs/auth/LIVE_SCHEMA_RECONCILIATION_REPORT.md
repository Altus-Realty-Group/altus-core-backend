# Live Schema Reconciliation Report

Status: Draft / Pending Live Core DB Verification
Owner: Altus Core Backend
Applies to: ECC, Price Engine, Field App, Construction Manager, Investor Hub, Deal Room, Altus Core Admin, Future Apps
Canonical Repo: Altus-Realty-Group/altus-core-backend
Database Authority: Altus Core Supabase project srzwamukysmhiaaviwiv
Mutation Status: Documentation only; no DB writes

## Project Ref Inspected

- `srzwamukysmhiaaviwiv`

## Inspection Method

- `VERIFIED_REPO`: backend repo inspection in `altus-core-backend`
- `VERIFIED_REPO`: local tool availability check for `gh`, `supabase`, and `psql`
- `VERIFIED_REPO`: local search for connection-method references and GitHub secret names only
- `BLOCKED`: direct live Supabase schema inspection, because usable local DB tooling and secret values were not available in this environment

## Access Status

### Available Connection Metadata

- `VERIFIED_REPO`: GitHub CLI is installed and authenticated
- `VERIFIED_REPO`: repo secret names exist for `SUPABASE_ACCESS_TOKEN`, `SUPABASE_PROJECT_REF`, `SUPABASE_DB_PASSWORD`, `SUPABASE_STAGING_PROJECT_REF`, `SUPABASE_STAGING_DB_PASSWORD`, `ALTUS_CORE_DB_HOST`, `ALTUS_CORE_DB_NAME`, `ALTUS_CORE_DB_PORT`, and `ALTUS_CORE_DB_USER`
- `VERIFIED_REPO`: repo workflows reference `supabase login` and `psql`-based DB access patterns

### Blockers

- `BLOCKED`: `supabase` CLI is not installed locally
- `BLOCKED`: `psql` is not installed locally
- `BLOCKED`: GitHub secret values are not retrievable through this inspection lane
- `BLOCKED`: no local approved connection string or password value was available without exposing secrets

## Schema Inventory Summary

### Live Inventory

- `BLOCKED`: no direct live table inventory was collected
- `BLOCKED`: no direct live row count inventory was collected
- `BLOCKED`: no direct live RLS or policy inventory was collected
- `BLOCKED`: no direct live function inventory was collected

### Repo Inventory

- `VERIFIED_REPO`: `supabase/migrations/0002_altus_core_identity.sql` defines `public.organizations`, `public.profiles`, and `public.organization_members`
- `VERIFIED_REPO`: the same migration defines `public.altus_current_org_id()`, `public.altus_is_org_member(uuid)`, `public.altus_login(text)`, `public.altus_me()`, and `public.altus_logout()`
- `VERIFIED_REPO`: `supabase/migrations/0003_altus_is_org_member_service_role.sql` alters `altus_is_org_member` so `service_role` returns true
- `VERIFIED_REPO`: `docs/database/SCHEMA_INVENTORY_V1.md` treats `organizations`, `profiles`, and `organization_members` as the repo-proven shared-auth tables
- `VERIFIED_REPO`: `docs/auth/ALTUS_CORE_AUTH_MODEL.md` and `docs/auth/APP_ENTITLEMENT_MODEL.md` define the intended platform auth model and explicitly defer physical-name decisions until live DB verification

## Auth Table Mapping

### Verified Live Auth Tables

- `BLOCKED`: `auth.users`
- `BLOCKED`: `auth.identities`
- `BLOCKED`: `auth.sessions`
- `BLOCKED`: `auth.refresh_tokens`
- `BLOCKED`: `public.altus_users`
- `BLOCKED`: `public.altus_sessions`
- `BLOCKED`: `public.client_companies`
- `BLOCKED`: `public.client_company_members`
- `BLOCKED`: `public.profiles`
- `BLOCKED`: `public.organizations`
- `BLOCKED`: `public.organization_members`
- `BLOCKED`: `public.app_access`
- `BLOCKED`: `public.apps`
- `BLOCKED`: `public.app_entitlements`
- `BLOCKED`: `public.roles`
- `BLOCKED`: `public.permissions`
- `BLOCKED`: `public.role_permissions`
- `BLOCKED`: `public.user_role_assignments`
- `BLOCKED`: `public.scoped_access_grants`
- `BLOCKED`: `public.auth_audit_log`

### Verified Repo Auth Tables And Functions

- `VERIFIED_REPO`: `public.organizations`
- `VERIFIED_REPO`: `public.profiles`
- `VERIFIED_REPO`: `public.organization_members`
- `VERIFIED_REPO`: `public.altus_current_org_id()`
- `VERIFIED_REPO`: `public.altus_is_org_member(uuid)`
- `VERIFIED_REPO`: `public.altus_login(text)`
- `VERIFIED_REPO`: `public.altus_me()`
- `VERIFIED_REPO`: `public.altus_logout()`

### PM-Evidence Live Candidates

- `INFERRED`: prior PM evidence indicates live Altus Core may contain `public.altus_users`
- `INFERRED`: prior PM evidence indicates live Altus Core may contain `public.altus_sessions`
- `INFERRED`: prior PM evidence indicates live Altus Core may contain `public.client_companies`
- `INFERRED`: prior PM evidence indicates live Altus Core may contain `public.client_company_members`

## RLS And Policy Summary

- `BLOCKED`: no direct live RLS state was inspected
- `VERIFIED_REPO`: the repo model enables RLS on `public.organizations`, `public.profiles`, and `public.organization_members`
- `VERIFIED_REPO`: the repo model uses helper-function-driven policies centered on `altus_is_org_member`
- `REQUIRES_DECISION`: any future entitlement tables must preserve or strengthen RLS, not weaken it

## Function Or RPC Summary

- `BLOCKED`: no direct live function inventory was collected
- `VERIFIED_REPO`: `altus_login(text)` bootstraps profile, organization, and membership in the repo model
- `VERIFIED_REPO`: `altus_me()` returns authenticated identity and organization summary in the repo model
- `VERIFIED_REPO`: `altus_logout()` is a no-op placeholder for sign-out symmetry in the repo model
- `VERIFIED_REPO`: `altus_is_org_member(uuid)` is the core RLS membership helper in the repo model

## Row Count Summary

- `BLOCKED`: no direct live row counts were collected
- `REQUIRES_DECISION`: when live access is available, row counts only should be captured for auth or access tables before any migration draft

## Live Vs Repo Divergence

- `VERIFIED_REPO`: repo migrations and docs currently model shared auth around `profiles`, `organizations`, `organization_members`, and auth RPCs
- `INFERRED`: prior PM evidence suggests live Altus Core may instead use `altus_users`, `altus_sessions`, `client_companies`, and `client_company_members`
- `VERIFIED_REPO`: platform docs in `docs/auth/` define the logical model as identity, category, membership, role, app entitlement, permission, scope grant, assignment, and audit
- `REQUIRES_DECISION`: physical naming cannot be finalized until live schema inspection confirms whether the PM-evidence tables exist and whether they are populated

## Physical-Name Decision Matrix

| Logical concept | Live candidate | Repo candidate | Recommended physical name | Compatibility path | Migration risk | Destructive rename required |
| --- | --- | --- | --- | --- | --- | --- |
| platform user | `INFERRED public.altus_users` | `VERIFIED_REPO public.profiles` | `REQUIRES_DECISION bridge after live inspection` | compatibility view or bridge table | high | no |
| identity link | `BLOCKED auth.identities` | `INFERRED user_id on public.profiles` | `REQUIRES_DECISION after live inspection` | map Supabase auth IDs to platform user record | medium | no |
| company or organization | `INFERRED public.client_companies` | `VERIFIED_REPO public.organizations` | `REQUIRES_DECISION bridge after live inspection` | compatibility view or dual-write migration | high | no |
| membership | `INFERRED public.client_company_members` | `VERIFIED_REPO public.organization_members` | `REQUIRES_DECISION bridge after live inspection` | compatibility view or migration mapping | high | no |
| app registry | `BLOCKED public.apps` | `INFERRED missing in repo` | `INFERRED public.apps` | add new table after live inspection | medium | no |
| app entitlement | `BLOCKED public.app_entitlements` | `INFERRED missing in repo` | `INFERRED public.app_entitlements` | add new table after live inspection | medium | no |
| role | `BLOCKED public.roles` | `INFERRED organization_members.role only` | `INFERRED public.roles` | normalize from current role fields | medium | no |
| permission | `BLOCKED public.permissions` | `INFERRED missing in repo` | `INFERRED public.permissions` | add new table | medium | no |
| role permission | `BLOCKED public.role_permissions` | `INFERRED missing in repo` | `INFERRED public.role_permissions` | add new table | medium | no |
| user role assignment | `BLOCKED public.user_role_assignments` | `INFERRED organization_members.role` | `INFERRED public.user_role_assignments` | bridge from membership role field | medium | no |
| scope grant | `BLOCKED public.scoped_access_grants` | `INFERRED missing in repo` | `INFERRED public.scoped_access_grants` | add new table | medium | no |
| app session | `INFERRED public.altus_sessions or auth.sessions` | `VERIFIED_REPO public.altus_logout RPC only` | `REQUIRES_DECISION bridge after live inspection` | likely preserve live session table if populated | high | no |
| audit log | `BLOCKED public.auth_audit_log` | `INFERRED missing in repo` | `INFERRED public.auth_audit_log` | add new table or preserve live if present | medium | no |

## Recommended Physical-Name Strategy

- `REQUIRES_DECISION`: final physical names must follow live inspection evidence
- `INFERRED`: if live `altus_users`, `altus_sessions`, `client_companies`, and `client_company_members` exist and contain data, preserve them and bridge the repo model to them
- `INFERRED`: if live tables do not exist or are empty, the repo model may become the safer physical baseline for some concepts

## Recommended Reconciliation Strategy

Recommendation: `C`.

`C: Bridge model is canonical; preserve live names where data exists, add compatibility tables or views or functions, migrate apps gradually.`

Why:

- `VERIFIED_REPO`: current app estate already has divergent auth assumptions
- `INFERRED`: live Altus Core may already have different physical names than the repo model
- `BLOCKED`: live schema inspection is not yet available, so destructive rename would be guesswork
- `REQUIRES_DECISION`: shared app registry, entitlement, permission, scope, and audit tables should be introduced through a compatibility-first migration plan

## Migration Preconditions

- `VERIFIED_REPO`: canonical docs exist in `docs/auth/`
- `BLOCKED`: direct live schema inventory must be collected first
- `BLOCKED`: direct live row counts for auth and access tables must be collected first
- `BLOCKED`: direct live RLS and policy inventory must be collected first
- `BLOCKED`: direct live RPC or function inventory must be collected first
- `REQUIRES_DECISION`: physical-name mapping must be approved before drafting migrations

## Migration Stop Conditions

- `BLOCKED`: stop if live access remains unavailable
- `REQUIRES_DECISION`: stop if live populated tables conflict with repo names and no bridge plan is approved
- `REQUIRES_DECISION`: stop if any migration would require destructive rename without explicit authorization
- `REQUIRES_DECISION`: stop if any change would weaken RLS or expose auth-sensitive data

## Next Implementation Plan

1. Install or enable an approved read-only live inspection path for Altus Core.
2. Verify that the accessible project ref is `srzwamukysmhiaaviwiv`.
3. Run read-only inventory queries for public and auth schemas.
4. Capture column, constraint, index, RLS, policy, and function summaries for auth-related objects.
5. Capture row counts only for auth and access tables.
6. Finalize the physical-name decision matrix from live evidence.
7. Approve the bridge-first reconciliation strategy.
8. Only then open a separate migration-draft prompt.
