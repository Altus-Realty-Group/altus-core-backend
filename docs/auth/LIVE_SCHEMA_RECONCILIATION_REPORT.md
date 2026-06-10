# Live Schema Reconciliation Report

Status: In Progress / Physical Schema Reconciliation Underway / Migration Drafting Blocked
Owner: Altus Core Backend
Applies to: ECC, Price Engine, Field App, Construction Manager, Investor Hub, Deal Room, Altus Core Admin, Future Apps
Canonical Repo: Altus-Realty-Group/altus-core-backend
Database Authority: Altus Core Supabase project `srzwamukysmhiaaviwiv`
Inspection Timestamp: `2026-06-10T00:00:00Z` (report revision)
Mutation Status: Read-only inspection only; no DB writes; no migrations executed

## Executive Result

Recommendation: `NO-GO` for executable migration drafting until bridge prerequisites are satisfied.

Reason:

- project access and read-only inspection path are verified
- live physical auth-adjacent tables appear to exist under legacy or client-centered names
- repo migration model and live physical model are not one-to-one
- final column, function, policy, and RLS proof is still pending

## VERIFIED

- project ref: `srzwamukysmhiaaviwiv`
- project name: `altus-core`
- status: `ACTIVE_HEALTHY`
- region: `us-west-2`
- postgres engine: `17`
- database version: `17.6.1.063`

## Project Ref Inspected

- target project ref: `srzwamukysmhiaaviwiv`
- repo branch used for comparison: `auth/live-schema-reconciliation`

## Live Inspection Conclusions Used For This Revision

1. The live Altus Core physical model is not the same as the repo migration model.
2. The live public schema appears centered on existing physical tables:

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
3. The repo migration model is centered on:

   - `public.profiles`
   - `public.organizations`
   - `public.organization_members`
   - `public.altus_current_org_id()`
   - `public.altus_is_org_member(uuid)`
   - `public.altus_login(text)`
   - `public.altus_me()`
   - `public.altus_logout()`
4. Implementation strategy must be bridge-first and non-destructive:

   - preserve existing live physical tables
   - do not blindly rename live tables
   - do not drop live tables
   - add bridge or compatibility layer only after final column and RLS confirmation
   - map canonical logical auth concepts onto live physical tables where safe
   - add missing platform-auth tables only where they do not already exist

## Live Inspection Status

Status:
PARTIALLY VERIFIED

Reason:
Project access and read-only inspection path have been verified.
Schema reconciliation remains in progress.
Migration drafting remains blocked until physical table mapping is completed.

## Prior Blocker Resolution

State:

The previous report concluded that schema inspection could not proceed because:

- no local Supabase CLI
- no local psql
- no local authenticated dashboard session

That conclusion is no longer sufficient because a verified external Supabase inspection path exists.

The blocker is now:

"Schema reconciliation incomplete"

instead of:

"No inspection access exists"

## Revised Migration Gate

Migration drafting is still blocked until the missing `public` schema metadata is verified, especially:

- `public.altus_users`
- `public.altus_sessions`
- `public.client_companies`
- `public.client_company_members`
- `public.clients`
- existing app entitlement/role/permission tables if present
- RLS policies on live public auth/access tables
- functions/RPCs related to auth/access/session/member/app/role/permission
- triggers and constraints on the live public auth/access tables

Project access itself is no longer a blocker.

## Connector-Verified Public Schema Metadata

A read-only Supabase connector metadata inspection verified the following public tables, columns, row counts, primary keys, foreign keys, and RLS posture.

### Verified Public Tables

1. `public.altus_users`
    - RLS enabled: true
    - rows: 0
    - primary key: `id`
    - columns:
       - `id` uuid default `gen_random_uuid()`
       - `is_active` boolean default `true`
       - `created_at` timestamptz default `now()`
       - `updated_at` timestamptz default `now()`
       - `email` text unique
       - `password_hash` text
       - `role` text with check: OWNER, ADMIN, OPS, ANALYST
    - foreign key targets:
       - `public.investor_sync_queue.requested_by -> public.altus_users.id`
       - `public.altus_sessions.user_id -> public.altus_users.id`

2. `public.altus_sessions`
    - RLS enabled: true
    - rows: 0
    - primary key: `id`
    - columns:
       - `user_id` uuid
       - `session_token` text unique
       - `expires_at` timestamptz
       - `id` uuid default `gen_random_uuid()`
       - `created_at` timestamptz default `now()`
    - foreign key:
       - `public.altus_sessions.user_id -> public.altus_users.id`

3. `public.investors_legacy`
    - RLS enabled: true
    - rows: 0
    - primary key: `id`
    - columns:
       - `first_name` text nullable
       - `last_name` text nullable
       - `email` text
       - `email_norm` text unique
       - `phone` text nullable
       - `phone_norm` text nullable
       - `capital_available_min` numeric nullable
       - `capital_available_max` numeric nullable
       - `risk_profile` text nullable
       - `timeline` text nullable
       - `liquidity_needs` text nullable
       - `accreditation_status` text nullable
       - `compliance_flags` jsonb nullable
       - `id` uuid default `gen_random_uuid()`
       - `geography` text[] default empty array
       - `strategies` text[] default empty array
       - `tags` text[] default empty array
       - `source_app` text default `unknown`
       - `created_at` timestamptz default `now()`
       - `updated_at` timestamptz default `now()`
    - foreign key targets:
       - `public.investor_criteria.investor_id -> public.investors_legacy.id`
       - `public.investor_sync_queue.investor_id -> public.investors_legacy.id`

4. `public.investor_criteria`
    - RLS enabled: true
    - rows: 0
    - primary key: `investor_id`
    - columns:
       - `investor_id` uuid
       - `min_irr` numeric nullable
       - `max_hold_years` integer nullable
       - `notes` text nullable
       - `preferred_asset_types` text[] default empty array
       - `preferred_states` text[] default empty array
    - foreign key:
       - `public.investor_criteria.investor_id -> public.investors_legacy.id`

5. `public.investor_sync_queue`
    - RLS enabled: true
    - rows: 0
    - primary key: `id`
    - columns:
       - `investor_id` uuid
       - `target_system` text with check: ECC, DEAL_ROOM, PRICE_ENGINE
       - `status` text with check: PENDING, APPROVED, SENT, FAILED
       - `requested_by` uuid nullable
       - `processed_at` timestamptz nullable
       - `id` uuid default `gen_random_uuid()`
       - `created_at` timestamptz default `now()`
    - foreign keys:
       - `public.investor_sync_queue.requested_by -> public.altus_users.id`
       - `public.investor_sync_queue.investor_id -> public.investors_legacy.id`

6. `public.audit_log`
    - RLS enabled: true
    - rows: 1
    - primary key: `id`
    - columns:
       - `actor_user_id` uuid nullable
       - `actor_type` text
       - `action` text
       - `entity_type` text nullable
       - `entity_id` uuid nullable
       - `details` jsonb nullable
       - `id` uuid default `gen_random_uuid()`
       - `at` timestamptz default `now()`

7. `public.clients`
    - RLS enabled: false
    - rows: 3
    - primary key: `id`
    - columns:
       - `first_name` text nullable
       - `last_name` text nullable
       - `email` text nullable
       - `phone` text nullable
       - `external_ref` jsonb nullable
       - `id` uuid default `gen_random_uuid()`
       - `source_app` text default `unknown`
       - `created_at` timestamptz default `now()`
       - `updated_at` timestamptz default `now()`
    - foreign key target:
       - `public.client_company_members.client_id -> public.clients.id`

8. `public.client_companies`
    - RLS enabled: false
    - rows: 0
    - primary key: `id`
    - columns:
       - `legal_name` text
       - `dba_name` text nullable
       - `ein` text nullable
       - `website` text nullable
       - `notes` text nullable
       - `id` uuid default `gen_random_uuid()`
       - `created_at` timestamptz default `now()`
       - `updated_at` timestamptz default `now()`
    - foreign key target:
       - `public.client_company_members.company_id -> public.client_companies.id`

9. `public.client_company_members`
    - RLS enabled: false
    - rows: 0
    - primary key: `id`
    - columns:
       - `client_id` uuid
       - `company_id` uuid
       - `id` uuid default `gen_random_uuid()`
       - `member_role` text default `owner`
       - `is_primary` boolean default `false`
       - `created_at` timestamptz default `now()`
    - foreign keys:
       - `public.client_company_members.client_id -> public.clients.id`
       - `public.client_company_members.company_id -> public.client_companies.id`

10. `public.assets`
      - RLS enabled: false
      - rows: 0
      - primary key: `id`
      - columns:
         - `organization_id` uuid
         - `address_canonical` text nullable
         - `apn` text nullable
         - `clip` text nullable
         - `id` uuid default `gen_random_uuid()`
         - `created_at` timestamptz default `now()`
         - `updated_at` timestamptz default `now()`
      - foreign key targets:
         - `public.asset_specs_reconciled.asset_id -> public.assets.id`
         - `public.asset_data_raw.asset_id -> public.assets.id`

11. `public.asset_data_raw`
      - RLS enabled: false
      - rows: 0
      - primary key: `id`
      - columns:
         - `asset_id` uuid
         - `source` text
         - `payload_jsonb` jsonb
         - `id` uuid default `gen_random_uuid()`
         - `fetched_at` timestamptz default `now()`
      - foreign key:
         - `public.asset_data_raw.asset_id -> public.assets.id`

12. `public.asset_specs_reconciled`
      - RLS enabled: false
      - rows: 0
      - primary key: `asset_id`
      - columns:
         - `updated_by_user_id` uuid nullable
         - `updated_at` timestamptz default `now()`
         - `asset_id` uuid
         - `beds` numeric nullable
         - `baths` numeric nullable
         - `sqft` numeric nullable
         - `year_built` integer nullable
         - `property_type` text nullable
         - `units_count` integer nullable
      - foreign key:
         - `public.asset_specs_reconciled.asset_id -> public.assets.id`

## Critical RLS Exposure Advisory

The Supabase connector returned a critical advisory that Row Level Security is disabled on six public tables:

- `public.clients`
- `public.client_companies`
- `public.client_company_members`
- `public.assets`
- `public.asset_data_raw`
- `public.asset_specs_reconciled`

Risk:
These tables are exposed to the anon and authenticated roles used by Supabase client libraries unless protected elsewhere. Anyone with the anon key may be able to read or modify every row on these tables.

Important:
Do not auto-apply remediation blindly. Enabling RLS without policies can block legitimate application access.
The exposure is compounded by verified broad table grants to `anon` and `authenticated`.

Proposed-only remediation SQL (not executed):

```sql
ALTER TABLE public.clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.client_companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.client_company_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.asset_data_raw ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.asset_specs_reconciled ENABLE ROW LEVEL SECURITY;
```

## Connector-Verified Public Grants Exposure

A read-only Supabase connector query against `information_schema.role_table_grants` verified that `anon` and `authenticated` have broad privileges on multiple public tables.

| Table | Grantees | Verified privileges |
| --- | --- | --- |
| `public.asset_data_raw` | `anon`, `authenticated` | DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE |
| `public.asset_specs_reconciled` | `anon`, `authenticated` | DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE |
| `public.assets` | `anon`, `authenticated` | DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE |
| `public.client_companies` | `anon`, `authenticated` | DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE |
| `public.client_company_members` | `anon`, `authenticated` | DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE |
| `public.clients` | `anon`, `authenticated` | DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE |
| `public.investors` | `anon`, `authenticated` | DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE |
| `public.investors_legacy_2` | `anon`, `authenticated` | DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE |

### Grants Exposure Interpretation

- The live database grants currently allow broad table-level privileges to Supabase client roles on the listed public tables.
- For tables with RLS disabled, this is a direct exposure risk.
- For tables where RLS may later be enabled, grants must still be reviewed and likely narrowed.
- Security remediation must include both RLS policy design and privilege/grant revocation design.
- Do not auto-revoke grants without dependency and runtime consumer mapping.

### Proposed-Only Grants Remediation Pattern

The following is a proposed remediation pattern only and was not executed:

```sql
REVOKE ALL ON TABLE public.asset_data_raw FROM anon, authenticated;
REVOKE ALL ON TABLE public.asset_specs_reconciled FROM anon, authenticated;
REVOKE ALL ON TABLE public.assets FROM anon, authenticated;
REVOKE ALL ON TABLE public.client_companies FROM anon, authenticated;
REVOKE ALL ON TABLE public.client_company_members FROM anon, authenticated;
REVOKE ALL ON TABLE public.clients FROM anon, authenticated;
REVOKE ALL ON TABLE public.investors FROM anon, authenticated;
REVOKE ALL ON TABLE public.investors_legacy_2 FROM anon, authenticated;
```

This SQL must not be executed until:

- runtime consumers are mapped
- service-role/server-only access paths are confirmed
- RLS policies are designed
- application read/write paths are updated or confirmed

## Connector-Verified Public RLS Policy Inventory

A read-only policy inventory query was executed against project ref `srzwamukysmhiaaviwiv`:

```sql
select schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check
from pg_policies
where schemaname = 'public'
order by tablename, policyname;
```

Verified result:

```json
[]
```

This confirms zero public RLS policies were returned.

No public policies are currently documented for any inspected public table, including tables where RLS is enabled and tables where RLS is disabled.

This strengthens the migration gate because policy design is mandatory before enabling RLS on exposed tables or relying on RLS-enabled auth/platform tables.

### Public RLS Policy Finding

| Finding | Status |
| --- | --- |
| Public RLS policy query executed | Verified |
| Public policies returned | 0 |
| Policies on `public.altus_users` | None returned |
| Policies on `public.altus_sessions` | None returned |
| Policies on `public.audit_log` | None returned |
| Policies on `public.clients` | None returned |
| Policies on `public.client_companies` | None returned |
| Policies on `public.client_company_members` | None returned |
| Policies on `public.assets` | None returned |
| Policies on `public.asset_data_raw` | None returned |
| Policies on `public.asset_specs_reconciled` | None returned |

### RLS Interpretation

- RLS-enabled tables with no policies are not automatically usable by normal Supabase client roles.
- RLS-disabled tables remain exposed unless protected outside Supabase client access.
- The remediation cannot be simply "enable RLS" without creating correct policies.
- The bridge migration must include a policy design phase before executable SQL.
- Existing application consumers must be mapped before any RLS enforcement change.

## Failed Read-Only Catalog Query

- Query type: read-only metadata/catalog inspection.
- Status: failed.
- Failure reason: `pg_tables.forcerowsecurity` column was not available.
- Impact: no data was changed; no schema was changed; prior RLS posture findings remain intact.
- Corrected method: inspect forced RLS through `pg_class.relforcerowsecurity`.

Proposed corrected query for future documentation-only inspection:

```sql
select
   n.nspname as schema_name,
   c.relname as table_name,
   c.relrowsecurity as rls_enabled,
   c.relforcerowsecurity as rls_forced
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
   and c.relkind = 'r'
order by c.relname;
```

## Connector-Verified Public Forced-RLS Inventory

A read-only connector query using `pg_class.relrowsecurity` and `pg_class.relforcerowsecurity` verified the RLS and forced-RLS posture for public base tables.

| Table | RLS enabled | RLS forced |
| --- | ---: | ---: |
| `public.altus_sessions` | true | false |
| `public.altus_users` | true | false |
| `public.asset_data_raw` | false | false |
| `public.asset_specs_reconciled` | false | false |
| `public.assets` | false | false |
| `public.audit_log` | true | false |
| `public.client_companies` | false | false |
| `public.client_company_members` | false | false |
| `public.clients` | false | false |
| `public.investor_criteria` | true | false |
| `public.investor_sync_queue` | true | false |
| `public.investors_legacy` | true | false |

### Forced-RLS Interpretation

- No inspected public table has forced RLS enabled.
- RLS-enabled tables are not forced, meaning table owners and privileged contexts may still bypass RLS.
- RLS-disabled tables remain exposed under the previously documented broad grants.
- Remediation planning must consider both RLS enablement and whether forced RLS is required for any table.
- Do not enable forced RLS blindly; it may affect privileged maintenance/service workflows.

## Connector-Verified Public Table Owner Inventory

A read-only connector query using `pg_class.relowner` and `pg_roles.rolname` verified owner roles for inspected public base tables.

| Table | RLS enabled | RLS forced | Owner role |
| --- | ---: | ---: | --- |
| `public.altus_sessions` | true | false | `postgres` |
| `public.altus_users` | true | false | `postgres` |
| `public.asset_data_raw` | false | false | `postgres` |
| `public.asset_specs_reconciled` | false | false | `postgres` |
| `public.assets` | false | false | `postgres` |
| `public.audit_log` | true | false | `postgres` |
| `public.client_companies` | false | false | `postgres` |
| `public.client_company_members` | false | false | `postgres` |
| `public.clients` | false | false | `postgres` |
| `public.investor_criteria` | true | false | `postgres` |
| `public.investor_sync_queue` | true | false | `postgres` |
| `public.investors_legacy` | true | false | `postgres` |

### Owner and Bypass Interpretation

- All inspected public base tables are owned by `postgres`.
- Because forced RLS is false on all inspected public tables, table-owner and privileged contexts may bypass RLS.
- This does not change the immediate anon/authenticated exposure finding for RLS-disabled tables with broad grants.
- It does affect remediation design because server-side, service-role, and owner-context execution paths must be reviewed before enabling or forcing RLS.
- Do not force RLS blindly. It may break maintenance, migration, service-role, or backend workflows if dependencies are not mapped.

## Auth Architecture Impact

The live schema currently has two identity/session concepts:

1. Supabase-managed auth identity: `auth.users`
2. `auth.sessions`
3. related auth schema tables
4. Legacy/platform public identity/session tables: `public.altus_users`
5. `public.altus_sessions`

This creates a confirmed dual-auth-model risk.

Bridge migration must not blindly preserve password-based public auth as a new canonical standard. The safer path is:

- keep Supabase Auth as the login identity authority
- map platform user records to `auth.users.id`
- evaluate whether `public.altus_users.password_hash` and `public.altus_sessions.session_token` are legacy/deprecated surfaces
- avoid creating new password/session logic outside Supabase Auth unless explicitly approved
- preserve existing live tables until dependencies are fully mapped
- add compatibility views/functions only after RLS and dependency proof

## Physical Schema Decision Matrix

| Logical Concept | Repo Migration Name | Live/Legacy Physical Candidate | Decision | Notes |
| --- | --- | --- | --- | --- |
| Platform user | `public.profiles` | `public.altus_users` | preserve/bridge pending column confirmation | Logical identity target is stable; physical mapping still pending column-level proof. |
| Auth/session surface | `public.altus_login(text)`, `public.altus_me()`, `public.altus_logout()`, plus Supabase auth | `public.altus_sessions` plus Supabase auth schema | bridge, do not replace blindly | Session and RPC surfaces require compatibility mapping before any replacement. |
| Organization/company | `public.organizations` | `public.client_companies` | preserve/bridge | Preserve live naming and bridge logical organization semantics safely. |
| Membership | `public.organization_members` | `public.client_company_members` | preserve/bridge | Membership semantics should be mapped without destructive renames. |
| Client/person record | none canonical in repo migration baseline | `public.clients` | preserve as app/business data, do not collapse into auth identity without proof | Keep business record boundaries intact pending verified linkage rules. |
| Audit surface | not fully implemented | `public.audit_log` | preserve; extend only after event contract confirmation | Reuse existing audit surface where possible; avoid duplicate audit stores without need. |
| App registry | planned platform auth model | not yet confirmed | add only if absent after final inspection | Presence and shape must be proven before create-or-merge decisions. |
| App entitlement | planned platform auth model | not yet confirmed | add only if absent after final inspection | Avoid duplicate entitlement tables if equivalent live storage already exists. |
| Roles | planned platform auth model | not yet confirmed | add only if absent after final inspection | Role storage and linkage remain pending proof. |
| Permissions | planned platform auth model | not yet confirmed | add only if absent after final inspection | Permission catalog storage remains pending proof. |
| Scoped grants / assignments | planned platform auth model | not yet confirmed | add only if absent after final inspection | Scope and assignment storage must be validated before schema additions. |

## Bridge-First Canonical Model

Canonical logical model remains:

- identity
- organization/company
- membership
- app registry
- app entitlement
- role
- permission
- scoped grant
- assignment
- auth audit event

Physical implementation must respect existing live names until dependency and RLS risk is fully understood.

## Non-Destructive Migration Rule

No executable migration may:

- rename `public.altus_users`
- rename `public.client_companies`
- rename `public.client_company_members`
- drop any live auth/access/client table
- disable RLS
- weaken policies
- backfill privileged access without explicit approval
- assume `@altus-realty.com` domain equals admin access

## App Access Rule

Altus Core auth must support plug-and-play app onboarding for:

- Price Engine
- ECC
- Field App
- Construction Manager
- Deal Room
- Investor Hub
- Altus Core Admin
- future Altus apps

Internal Altus users may be eligible across apps, but app access must still be entitlement, role, and permission controlled.

External users must be app-scoped and assignment-scoped:

- clients
- contractors
- vendors
- lenders
- agents
- investors
- guests

Contractors must not receive blanket Altus Platform access.

## Migration Draft Gate

Migration drafting remains blocked until all of the following are documented:

- public table RLS policy design is complete
- forced-RLS decision per public auth/access/asset/client table
- service-role and table-owner bypass impact review
- confirmation whether forced RLS should remain false for server-only tables
- table owner and privileged context review
- owner-bypass impact assessment
- service-role versus anon/authenticated access boundary documentation
- decision whether any table should use `FORCE ROW LEVEL SECURITY`
- public table grant remediation design
- anon/authenticated privilege narrowing plan
- runtime consumer impact assessment before REVOKE/ALTER statements
- existing consumer mapping is complete
- public auth/session usage is confirmed active/deprecated/unused
- confirmation whether `public.investors` and `public.investors_legacy_2` are active, deprecated, or orphaned
- app entitlement/role/permission physical model is decided
- proposed RLS policies are reviewed before execution

Until then, docs may be refined, but executable migration drafting remains blocked.

## Verification Boundary

- Project identity and live access path are verified.
- Partial read-only inspection capability is verified.
- Full schema reconciliation is not yet complete.
- No row-level records are exposed in this report.
- No secrets were exposed.
- No database writes occurred.

## Table-Name Reconciliation Status

Current status: `IN PROGRESS`.

Physical table naming and object-level mapping are still being reconciled for auth-relevant concepts, including but not limited to:

- `auth.users`
- `public.altus_users`
- `public.altus_sessions`
- `public.client_companies`
- `public.client_company_members`
- `public.clients`
- `public.profiles`
- `public.organizations`
- `public.organization_members`
- `public.apps`
- `public.app_entitlements`
- `public.roles`
- `public.permissions`
- `public.role_permissions`
- `public.user_role_assignments`
- `public.scoped_access_grants`
- `public.assignments`
- `public.auth_audit_log`
- `public.audit_log`

## Bridge-Vs-Migration Recommendation

Recommendation: `Bridge-first, non-destructive, no executable migration draft yet`.

Why:

- logical models and migration intent remain valid
- physical table/object reconciliation is still incomplete
- destructive renames remain unsafe until full mapping is complete
- non-destructive bridge strategy remains the safest path

## No-Go Items

- do not draft executable migration SQL yet
- do not finalize physical table-name mappings from assumptions alone
- do not perform destructive renames before full live mapping is complete
- do not alter RLS or policies until live policy posture is fully documented

## Confirmation

- no migration was executed
- no DDL was executed
- no INSERT, UPDATE, DELETE, ALTER, DROP, CREATE, TRUNCATE, GRANT, REVOKE, or policy mutation was performed
- no row-level records were dumped
- no secrets were exposed

## Next Step Required

Complete physical live schema reconciliation for auth, organization/company, membership, entitlement, role/permission, and RLS objects, then open migration drafting under the existing bridge-first and non-destructive constraints.
