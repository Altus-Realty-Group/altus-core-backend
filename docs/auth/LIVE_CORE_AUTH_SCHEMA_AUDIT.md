# Live Core Auth Schema Audit

Status: Draft / Pending Direct Live DB Verification
Owner: Altus Core Backend
Inspection Date: 2026-06-09
Canonical Repo: Altus-Realty-Group/altus-core-backend
Project Ref: srzwamukysmhiaaviwiv
Repo Branch: auth/live-schema-reconciliation
Repo HEAD: 07032cce09ceb0a31ec683cbaae8956ba988a73b
Mutation Status: Documentation only; no DB writes

## Scope

This document records the current state of the Altus Core live-auth schema investigation.

It separates:

- directly verified repository facts
- externally observed live database facts that were supplied to this lane but not directly re-run here
- blocked live inspection areas

This document does not claim that repository migrations are the live source of truth.

## Inspection Method

### VERIFIED_REPO Tooling And Secrets

- verified backend repo remote, branch, and HEAD in `altus-core-backend`
- verified local tooling state for `gh`, `supabase`, and `psql`
- verified repo workflow references for Supabase and Postgres access patterns
- verified repo secret names only, not values
- verified repo-side auth migrations and schema docs
- verified staged auth architecture docs in `altus-core-ops/docs/auth`

### BLOCKED Live Inspection Path

- direct live inspection of Supabase project `srzwamukysmhiaaviwiv`
- direct re-verification of live table inventory
- direct re-verification of live row counts
- direct re-verification of live RLS or policy state
- direct re-verification of live trigger inventory
- direct re-verification of live function or RPC inventory

## Live Access Status

### VERIFIED_REPO Policy Posture

- GitHub CLI is installed and authenticated
- backend repo contains secret names that imply an approved DB access path exists elsewhere
- backend workflows reference `supabase login` and `psql` usage patterns

### BLOCKED Live Policy Verification

- `supabase` CLI is not installed locally in this VS environment
- `psql` is not installed locally in this VS environment
- no approved read-only secret values were available in this lane
- no local connection string was available without exposing secrets

Conclusion:

- direct live DB inspection is blocked in this lane

## Directly Verified Repo Model

### VERIFIED_REPO: Shared Auth Tables In Repo Migrations

`supabase/migrations/0002_altus_core_identity.sql` defines:

- `public.organizations`
- `public.profiles`
- `public.organization_members`

It also defines repository-side shared auth functions:

- `public.altus_current_org_id()`
- `public.altus_is_org_member(uuid)`
- `public.altus_login(text)`
- `public.altus_me()`
- `public.altus_logout()`

`supabase/migrations/0003_altus_is_org_member_service_role.sql` changes `altus_is_org_member` so `service_role` returns true.

### VERIFIED_REPO: Shared Auth Docs In Repo

The canonical backend repo now contains:

- `docs/auth/ALTUS_CORE_AUTH_MODEL.md`
- `docs/auth/APP_ENTITLEMENT_MODEL.md`
- `docs/auth/APP_ACCESS_MATRIX.md`
- `docs/auth/FUTURE_APP_AUTH_ONBOARDING.md`
- `docs/auth/LIVE_SCHEMA_RECONCILIATION_REPORT.md`

These docs define the logical platform model as:

- identity
- user category
- organization or company membership
- internal role
- app entitlement
- action permission
- scope grant
- assignment
- audit

## Externally Observed Live Facts

The following items were supplied to this lane as externally observed live facts.

They were not directly re-run here, so they are recorded as `INFERRED` until revalidated.

### INFERRED: Previously Observed Public Tables

- `public.altus_users`
- `public.altus_sessions`
- `public.client_companies`
- `public.client_company_members`
- `public.clients`
- `public.assets`
- `public.asset_data_raw`
- `public.asset_specs_reconciled`
- `public.audit_log`
- `public.investor_criteria`
- `public.investor_sync_queue`
- `public.investors_legacy`

### INFERRED: Previously Observed Auth Tables

- `auth.users`
- `auth.sessions`
- `auth.identities`
- `auth.refresh_tokens`
- `auth.audit_log_entries`

### INFERRED: Previously Observed Row Counts

- `auth.users`: `0`
- `public.altus_users`: `0`
- `public.client_companies`: `0`
- `public.client_company_members`: `0`
- `public.clients`: `3`

## Auth Or Client Table Detail Status

### BLOCKED: Direct Table Detail Verification

The following table details were requested but could not be directly verified here for:

- `public.altus_users`
- `public.altus_sessions`
- `public.client_companies`
- `public.client_company_members`
- `public.clients`

Blocked detail categories:

- columns
- data types
- nullable status
- defaults
- primary keys
- foreign keys
- unique constraints
- check constraints
- indexes
- RLS enabled or disabled status
- policies
- triggers
- row count recheck

## App-Auth Related Table Search Status

### BLOCKED: Direct Live Search

No direct live search could be run for public tables containing or implying:

- app
- role
- permission
- entitlement
- membership
- organization
- org
- tenant
- session
- user
- invite
- contractor
- vendor
- investor
- client
- audit

### VERIFIED_REPO: Repo-Side Logical Targets

The platform auth docs require eventual support for:

- `apps`
- `app_entitlements`
- `roles`
- `permissions`
- `role_permissions`
- `user_role_assignments`
- `scoped_access_grants`
- `auth_audit_log`

## RLS And Policy Summary

### VERIFIED_REPO

The repo model enables RLS on:

- `public.organizations`
- `public.profiles`
- `public.organization_members`
- `public.assets`
- `public.asset_data_raw`
- `public.asset_specs_reconciled`

The repo model uses helper-function-driven policies centered on `altus_is_org_member`.

### BLOCKED

The live status of RLS, policy names, roles, commands, `using`, and `with check` expressions for `altus_users`, `altus_sessions`, `client_companies`, `client_company_members`, and `clients` could not be re-verified in this lane.

## Repo Vs Live Divergence

### Live Database Model

- `INFERRED`: live physical model appears to center on `altus_users`, `altus_sessions`, `client_companies`, and `client_company_members`
- `INFERRED`: live auth backbone also includes standard Supabase `auth.*` tables
- `INFERRED`: live public model includes business tables such as `clients`, `assets`, `asset_data_raw`, `asset_specs_reconciled`, and investor tables

### Repo Migration Model

- `VERIFIED_REPO`: repo shared-auth model centers on `profiles`, `organizations`, and `organization_members`
- `VERIFIED_REPO`: repo shared-auth access is currently organization-scoped and function-assisted
- `VERIFIED_REPO`: repo does not yet prove physical tables for app registry, app entitlements, normalized roles, permissions, scoped grants, or auth audit log

### Staged Auth Architecture Model

- `VERIFIED_REPO`: platform auth docs define Altus Core Auth as the shared identity and entitlement layer for ECC, Price Engine, Field App, Construction Manager, Investor Hub, Deal Room, Altus Core Admin, and future apps
- `VERIFIED_REPO`: staged model requires app registry, app entitlements, roles, permissions, scoped grants, assignments, audit, and future-app onboarding without app-local permanent auth divergence

### Exact Conflicts

- `REQUIRES_DECISION`: live physical user table may be `altus_users` while repo physical user table is `profiles`
- `REQUIRES_DECISION`: live physical company and membership tables may be `client_companies` and `client_company_members` while repo physical tables are `organizations` and `organization_members`
- `VERIFIED_REPO`: repo model has no proven app registry or app entitlement physical tables yet
- `REQUIRES_DECISION`: live session ownership may be represented through `altus_sessions`, `auth.sessions`, or both

## Recommended Physical Bridge Path

Recommendation: preserve and bridge where live data or dependencies may already exist.

Current recommendation by concept:

- platform user: preserve `public.altus_users` if it exists, bridge logical platform-user model to it, and do not blind-rename to `profiles`
- company or organization: preserve `public.client_companies` if it exists, bridge logical organization model to it, and avoid destructive rename
- membership: preserve `public.client_company_members` if it exists, bridge membership semantics to it, and avoid destructive rename
- app registry: add `public.apps` if absent after live verification
- app entitlements: add `public.app_entitlements` if absent after live verification
- roles and permissions: add normalized `roles`, `permissions`, `role_permissions`, and `user_role_assignments` after live verification
- scoped access: add `scoped_access_grants` after live verification
- audit: add or preserve an auth-focused audit log separate from general audit surfaces where needed

## SQL Inspection Pack

The following SQL is read-only and safe to hand to a separately authenticated inspection lane.

### 1. Table Inventory

```sql
select
  table_schema,
  table_name,
  table_type
from information_schema.tables
where table_schema in ('public', 'auth')
order by table_schema, table_name;
```

### 2. Auth-Related Table Name Search

```sql
select
  table_schema,
  table_name,
  table_type
from information_schema.tables
where table_schema in ('public', 'auth')
  and (
    table_name ilike '%app%'
    or table_name ilike '%role%'
    or table_name ilike '%permission%'
    or table_name ilike '%entitlement%'
    or table_name ilike '%member%'
    or table_name ilike '%organization%'
    or table_name ilike '%org%'
    or table_name ilike '%tenant%'
    or table_name ilike '%session%'
    or table_name ilike '%user%'
    or table_name ilike '%invite%'
    or table_name ilike '%contractor%'
    or table_name ilike '%vendor%'
    or table_name ilike '%investor%'
    or table_name ilike '%client%'
    or table_name ilike '%audit%'
  )
order by table_schema, table_name;
```

### 3. Column Inventory

```sql
select
  table_schema,
  table_name,
  ordinal_position,
  column_name,
  data_type,
  is_nullable,
  column_default
from information_schema.columns
where table_schema in ('public', 'auth')
  and table_name in (
    'altus_users',
    'altus_sessions',
    'client_companies',
    'client_company_members',
    'clients'
  )
order by table_schema, table_name, ordinal_position;
```

### 4. Constraints

```sql
select
  tc.table_schema,
  tc.table_name,
  tc.constraint_name,
  tc.constraint_type,
  kcu.column_name,
  ccu.table_schema as foreign_table_schema,
  ccu.table_name as foreign_table_name,
  ccu.column_name as foreign_column_name
from information_schema.table_constraints tc
left join information_schema.key_column_usage kcu
  on tc.constraint_name = kcu.constraint_name
 and tc.table_schema = kcu.table_schema
 and tc.table_name = kcu.table_name
left join information_schema.constraint_column_usage ccu
  on tc.constraint_name = ccu.constraint_name
 and tc.table_schema = ccu.table_schema
where tc.table_schema in ('public', 'auth')
  and tc.table_name in (
    'altus_users',
    'altus_sessions',
    'client_companies',
    'client_company_members',
    'clients'
  )
order by tc.table_schema, tc.table_name, tc.constraint_name, kcu.ordinal_position;
```

### 5. Check Constraints

```sql
select
  tc.table_schema,
  tc.table_name,
  tc.constraint_name,
  cc.check_clause
from information_schema.table_constraints tc
join information_schema.check_constraints cc
  on tc.constraint_name = cc.constraint_name
where tc.constraint_type = 'CHECK'
  and tc.table_schema in ('public', 'auth')
  and tc.table_name in (
    'altus_users',
    'altus_sessions',
    'client_companies',
    'client_company_members',
    'clients'
  )
order by tc.table_schema, tc.table_name, tc.constraint_name;
```

### 6. Indexes

```sql
select
  schemaname,
  tablename,
  indexname,
  indexdef
from pg_indexes
where schemaname in ('public', 'auth')
  and tablename in (
    'altus_users',
    'altus_sessions',
    'client_companies',
    'client_company_members',
    'clients'
  )
order by schemaname, tablename, indexname;
```

### 7. Triggers

```sql
select
  event_object_schema as table_schema,
  event_object_table as table_name,
  trigger_name,
  action_timing,
  event_manipulation,
  action_statement
from information_schema.triggers
where event_object_schema in ('public', 'auth')
  and event_object_table in (
    'altus_users',
    'altus_sessions',
    'client_companies',
    'client_company_members',
    'clients'
  )
order by event_object_schema, event_object_table, trigger_name;
```

### 8. RLS Enabled Status

```sql
select
  schemaname,
  tablename,
  rowsecurity,
  forcerowsecurity
from pg_tables
where schemaname in ('public', 'auth')
  and tablename in (
    'altus_users',
    'altus_sessions',
    'client_companies',
    'client_company_members',
    'clients'
  )
order by schemaname, tablename;
```

### 9. Policies

```sql
select
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
from pg_policies
where schemaname in ('public', 'auth')
  and tablename in (
    'altus_users',
    'altus_sessions',
    'client_companies',
    'client_company_members',
    'clients'
  )
order by schemaname, tablename, policyname;
```

### 10. Row Counts

```sql
select 'auth.users' as table_name, count(*) as row_count from auth.users
union all
select 'auth.sessions', count(*) from auth.sessions
union all
select 'auth.identities', count(*) from auth.identities
union all
select 'auth.refresh_tokens', count(*) from auth.refresh_tokens
union all
select 'auth.audit_log_entries', count(*) from auth.audit_log_entries
union all
select 'public.altus_users', count(*) from public.altus_users
union all
select 'public.altus_sessions', count(*) from public.altus_sessions
union all
select 'public.client_companies', count(*) from public.client_companies
union all
select 'public.client_company_members', count(*) from public.client_company_members
union all
select 'public.clients', count(*) from public.clients
order by table_name;
```

### 11. Function Inventory

```sql
select
  n.nspname as schema_name,
  p.proname as function_name,
  pg_get_function_identity_arguments(p.oid) as arguments,
  pg_get_function_result(p.oid) as return_type,
  p.prosecdef as security_definer,
  l.lanname as language_name
from pg_proc p
join pg_namespace n on p.pronamespace = n.oid
join pg_language l on p.prolang = l.oid
where n.nspname in ('public', 'auth')
  and (
    p.proname ilike '%auth%'
    or p.proname ilike '%user%'
    or p.proname ilike '%role%'
    or p.proname ilike '%permission%'
    or p.proname ilike '%entitlement%'
    or p.proname ilike '%membership%'
    or p.proname ilike '%session%'
    or p.proname ilike '%scope%'
    or p.proname in ('altus_login', 'altus_me', 'altus_logout')
  )
order by n.nspname, p.proname;
```

## Migration Preconditions

- direct live inspection must be rerun through an approved authenticated lane
- physical table names must be verified before migration drafting
- row counts and dependency risk must be reconfirmed for the live auth and client tables
- bridge path must be approved before any destructive rename is considered

## Stop Conditions

- stop if live access requires secret exposure
- stop if any action would mutate database state
- stop if any migration or policy change is required to continue inspection
- stop if physical-name conflicts cannot be bridged safely from evidence

## Next Implementation Plan

1. Run the SQL inspection pack through an approved authenticated lane.
2. Capture direct live table definitions, constraints, indexes, policies, triggers, functions, and row counts.
3. Finalize the physical-name mapping of `altus_users` versus `profiles` and `client_companies` versus `organizations`.
4. Approve the compatibility-first bridge path.
5. Only then open a separate migration-draft prompt.
