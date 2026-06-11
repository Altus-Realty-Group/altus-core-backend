# Altus Core Backend - Cross-Repo Runtime Consumer Map

## Status

- Status: PARTIAL
- Repository: Altus-Realty-Group/altus-core-backend
- Branch: auth/runtime-evidence-docs-clean
- Base commit: origin/main / 07032cc
- Worktree path: c:\Users\Dionr\OneDrive\Documents\GitHub\_backend-auth-runtime-evidence-clean
- Inspection date: 2026-06-11
- Evidence scope: tracked files in this clean worktree only
- Explicit exclusions: untracked files, dirty worktree evidence, other local clones, other repositories, live database state, deployed Azure resources, secrets, environment values, runtime logs, generated artifacts, and `altus-core-staging` as Altus Core authority

This document is documentation-only runtime evidence. It records what tracked repository files prove, what they do not prove, and where the current caller trace remains unknown. It does not authorize code changes, auth logic changes, SQL execution, RLS changes, grants, policies, migrations, schema changes, seeds, secrets, CI changes, package changes, Azure Functions behavior changes, frontend changes, cleanup, deletion, or legacy object removal.

## Executive Summary

Tracked backend evidence proves that this repository contains Azure Function code that talks to Supabase through service-role REST access for a narrow set of backend asset surfaces.

Tracked evidence found:

- `azure/functions/asset_ingest/function_app.py` inserts into `assets` and `asset_data_raw` using Supabase REST with the service-role key.
- `azure/functions/asset_ingest/ecc_portfolio_assets_service.py` reads `assets` and `asset_specs_reconciled` using Supabase REST with the service-role key.
- `azure/functions/asset_ingest/ecc_portfolio_summary_service.py` reads `assets` and `asset_specs_reconciled` using Supabase REST with the service-role key.
- `supabase/migrations/0002_altus_core_identity.sql` defines identity tables, org-membership RLS helpers, asset tables, policies, and RPCs including `altus_login`, `altus_me`, and `altus_logout`.
- `supabase/verification/0001_schema_inventory_assertions.sql` verifies the presence of the core identity and asset surfaces.
- `staging-nightly-audit.yml` performs CI/database audit and migration validation work against Supabase.
- `altus-core-staging` is excluded as an authoritative Altus Core runtime, database, schema, auth, migration, onboarding, or evidence source.

Tracked evidence did not prove browser/client Supabase usage, `/auth/me` callers, `/session/me` callers, entitlement middleware, permission middleware, scope middleware, or session-claim inspection in this clean worktree.

## Evidence Rules

- Only tracked files in `c:\Users\Dionr\OneDrive\Documents\GitHub\_backend-auth-runtime-evidence-clean` were used.
- No untracked files were used.
- No dirty worktree evidence was used.
- No assumptions were made from filenames alone.
- Runtime consumer claims require file content evidence.
- `UNKNOWN` is used where tracked files do not prove runtime behavior.
- `NOT FOUND` is used where tracked searches found no matching caller or implementation evidence.

## Altus Core Staging Exclusion

`altus-core-staging` was temporary ECC-related infrastructure. It is not an authoritative Altus Core runtime or database target.

`altus-core-staging` must not be used for Altus Core runtime proof, schema authority, auth evidence, migration evidence, or onboarding reference.

Altus Core database authority must come only from the confirmed production Altus Core Supabase project and repo-tracked backend migration/schema evidence.

Runtime proof must come only from the confirmed live Altus Core backend/runtime, not the temporary ECC staging project.

This document does not use staging logs, staging schema, staging migrations, staging auth, staging keys, staging URLs, or the `altus-core-staging` project as Altus Core evidence.

## Runtime Consumer Table

| Repo | Object | Consumer | File/Route | Access Type | Role Context | Risk if Grants/RLS Change | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| altus-core-backend | `assets` | Azure Function asset ingest | `azure/functions/asset_ingest/function_app.py`; route `POST /api/assets/ingest` | insert | service_role | High: service-role REST writes depend on table availability and service-role access; RLS may be bypassed by service role but grants/schema/table changes can still break writes. | `_insert_supabase_row(table="assets", ...)`, Supabase REST endpoint, `apikey`, and `Authorization: Bearer` service-role key. | Tracked runtime/service consumer. Not an end-user auth/session middleware consumer. |
| altus-core-backend | `asset_data_raw` | Azure Function asset ingest | `azure/functions/asset_ingest/function_app.py`; route `POST /api/assets/ingest` | insert | service_role | High: service-role REST writes depend on table availability and expected columns; schema/grant changes can break ingest evidence writes. | `_insert_supabase_row(table="asset_data_raw", ...)`, Supabase REST endpoint, `apikey`, and `Authorization: Bearer` service-role key. | Tracked runtime/service consumer. Not an end-user auth/session middleware consumer. |
| altus-core-backend | `assets` | ECC portfolio assets service | `azure/functions/asset_ingest/ecc_portfolio_assets_service.py`; route `GET /api/ecc/portfolio/assets` via `function_app.py` | read | service_role | Medium: route-backed cohort reads depend on `assets`, `external_ids`, and service-role REST access. | REST request to `/rest/v1/assets` with `select=id,display_name,status`, `external_ids` filter, `apikey`, and `Authorization: Bearer`. | Tracked runtime/service consumer. Not `/auth/me` or `/session/me`. |
| altus-core-backend | `asset_specs_reconciled` | ECC portfolio assets service | `azure/functions/asset_ingest/ecc_portfolio_assets_service.py`; route `GET /api/ecc/portfolio/assets` via `function_app.py` | read | service_role | Medium: route-backed enrichment depends on `asset_specs_reconciled.asset_id` and `units_count`. | REST request to `/rest/v1/asset_specs_reconciled` with `select=asset_id,units_count`, `apikey`, and `Authorization: Bearer`. | Tracked runtime/service consumer. Not `/auth/me` or `/session/me`. |
| altus-core-backend | `assets` | ECC portfolio summary service | `azure/functions/asset_ingest/ecc_portfolio_summary_service.py`; route `GET /api/ecc/portfolio/summary` via `function_app.py` | read | service_role | Medium: route-backed summary reads depend on `assets`, `external_ids`, and service-role REST access. | REST request to `/rest/v1/assets` with `select=id`, `external_ids` filter, `Prefer: count=exact`, `apikey`, and `Authorization: Bearer`. | Tracked runtime/service consumer. Not `/auth/me` or `/session/me`. |
| altus-core-backend | `asset_specs_reconciled` | ECC portfolio summary service | `azure/functions/asset_ingest/ecc_portfolio_summary_service.py`; route `GET /api/ecc/portfolio/summary` via `function_app.py` | read | service_role | Medium: route-backed total-units calculation depends on `asset_specs_reconciled.asset_id` and `units_count`. | REST request to `/rest/v1/asset_specs_reconciled` with `select=asset_id,units_count`, `apikey`, and `Authorization: Bearer`. | Tracked runtime/service consumer. Not `/auth/me` or `/session/me`. |
| altus-core-backend | `organizations` | Identity schema | `supabase/migrations/0002_altus_core_identity.sql` | raw_sql | authenticated | Medium: policies and helper functions depend on organization membership; changes can affect authenticated access semantics. | Creates `public.organizations`, enables RLS, and defines `org_select`. | Schema evidence, not application runtime caller code. |
| altus-core-backend | `profiles` | Identity schema | `supabase/migrations/0002_altus_core_identity.sql` | raw_sql | authenticated | Medium: profile policies and auth-owned user mapping affect authenticated identity shape. | Creates `public.profiles`, references `auth.users`, enables RLS, defines self/org read and self update policies. | Schema evidence, not application runtime caller code. |
| altus-core-backend | `organization_members` | Identity schema and RLS helpers | `supabase/migrations/0002_altus_core_identity.sql` | raw_sql | authenticated | High: org-scoped RLS helpers and policies depend on membership rows. | Creates `public.organization_members`, enables RLS, defines `altus_is_org_member`, and uses `auth.uid()`. | Schema evidence, not application runtime caller code. |
| altus-core-backend | `assets` | Identity/asset schema | `supabase/migrations/0002_altus_core_identity.sql` | raw_sql | authenticated | High: RLS policies define authenticated CRUD expectations for asset rows. | Creates `public.assets`, enables RLS, defines `assets_select`, `assets_insert`, `assets_update`, and `assets_delete`. | Schema evidence, not application runtime caller code. |
| altus-core-backend | `asset_data_raw` | Identity/asset schema | `supabase/migrations/0002_altus_core_identity.sql` | raw_sql | authenticated | High: RLS policies define authenticated CRUD expectations through associated `assets` membership checks. | Creates `public.asset_data_raw`, enables RLS, defines `adr_select`, `adr_insert`, `adr_update`, and `adr_delete`. | Schema evidence, not application runtime caller code. |
| altus-core-backend | `asset_specs_reconciled` | Identity/asset schema | `supabase/migrations/0002_altus_core_identity.sql` | raw_sql | authenticated | High: RLS policies define authenticated CRUD expectations for reconciled specs. | Creates `public.asset_specs_reconciled`, enables RLS, defines `asr_select`, `asr_insert`, `asr_update`, and `asr_delete`. | Schema evidence, not application runtime caller code. |
| altus-core-backend | `altus_login` | Identity RPC schema | `supabase/migrations/0002_altus_core_identity.sql` | rpc | authenticated | Medium: auth onboarding behavior depends on RPC grant and schema implementation. | Defines `public.altus_login(text)`, uses `auth.uid()`, ensures profile/org/membership, grants execute to `authenticated`. | Schema/RPC evidence only; no tracked application caller found. |
| altus-core-backend | `altus_me` | Identity RPC schema | `supabase/migrations/0002_altus_core_identity.sql` | rpc | authenticated | Medium: current-user identity response depends on RPC grant and implementation. | Defines `public.altus_me()`, reads profiles, organizations, and organization_members, grants execute to `authenticated`. | Schema/RPC evidence only; no tracked application caller found. |
| altus-core-backend | `altus_logout` | Identity RPC schema | `supabase/migrations/0002_altus_core_identity.sql` | rpc | authenticated | Low: currently a no-op placeholder RPC; grants still affect client availability. | Defines `public.altus_logout()`, grants execute to `authenticated`. | Schema/RPC evidence only; no tracked application caller found. |
| altus-core-backend | core identity and asset tables/functions | Schema inventory verification | `supabase/verification/0001_schema_inventory_assertions.sql` | raw_sql | unknown | Low to medium: verification depends on expected objects existing but is not product runtime behavior. | Queries information_schema and pg_policies for organizations, profiles, organization_members, assets, asset_data_raw, asset_specs_reconciled, and identity functions. | Verification evidence, not application runtime caller code. |
| altus-core-backend | Supabase audit workflow | Staging nightly audit | `staging-nightly-audit.yml` | raw_sql | unknown | Low to medium: CI audit can fail if DB access, migrations, RLS, or policy shape changes. | Uses Supabase CLI, `supabase db push`, `psql`, migration inventory, table presence, RLS status, policies, and indexes checks. | CI/database verification only; not product runtime auth caller and not Altus Core runtime/schema/auth/migration authority. |
| altus-core-backend | `altus_users` | NOT FOUND | tracked files | unknown | unknown | UNKNOWN | Tracked search found no `altus_users` reference. | No runtime consumer proven. |
| altus-core-backend | `altus_sessions` | NOT FOUND | tracked files | unknown | unknown | UNKNOWN | Tracked search found no `altus_sessions` reference. | No runtime consumer proven. |
| altus-core-backend | `audit_log` | NOT FOUND | tracked files | unknown | unknown | UNKNOWN | Tracked search found no `audit_log` reference. | No runtime consumer proven. |
| altus-core-backend | `client_companies` | NOT FOUND | tracked files | unknown | unknown | UNKNOWN | Tracked search found no `client_companies` reference. | No runtime consumer proven. |
| altus-core-backend | `client_company_members` | NOT FOUND | tracked files | unknown | unknown | UNKNOWN | Tracked search found no `client_company_members` reference. | No runtime consumer proven. |
| altus-core-backend | `clients` | NOT FOUND as table/object | tracked files | unknown | unknown | UNKNOWN | Tracked search found only comment wording about clients in `supabase/migrations/0002_altus_core_identity.sql`, not a table/object consumer. | No runtime consumer proven. |
| altus-core-backend | `investors` | NOT FOUND | tracked files | unknown | unknown | UNKNOWN | Tracked search found no `investors` reference. | No runtime consumer proven. |
| altus-core-backend | `investors_legacy` | NOT FOUND | tracked files | unknown | unknown | UNKNOWN | Tracked search found no `investors_legacy` reference. | No runtime consumer proven. |
| altus-core-backend | `investors_legacy_2` | NOT FOUND | tracked files | unknown | unknown | UNKNOWN | Tracked search found no `investors_legacy_2` reference. | No runtime consumer proven. |
| altus-core-backend | `investor_criteria` | NOT FOUND | tracked files | unknown | unknown | UNKNOWN | Tracked search found no `investor_criteria` reference. | No runtime consumer proven. |
| altus-core-backend | `investor_sync_queue` | NOT FOUND | tracked files | unknown | unknown | UNKNOWN | Tracked search found no `investor_sync_queue` reference. | No runtime consumer proven. |

## Backend Runtime Findings

### `azure/functions/asset_ingest/function_app.py`

Verified tracked file evidence:

- The Azure Functions app is configured with `func.AuthLevel.ANONYMOUS` on discovered routes.
- `RuntimeConfig` reads Supabase URL and service-role key secret names from environment and resolves values through Key Vault.
- `_insert_supabase_row()` builds `/rest/v1/{table}` URLs and sends both `apikey` and `Authorization: Bearer` headers using the service-role key.
- `assets_ingest()` writes to `assets` and then writes to `asset_data_raw`.
- `function_app.py` also wires anonymous HTTP routes for ECC, price-engine, and title-rate handlers, but tracked evidence in this pass only proves direct Supabase writes in `assets_ingest()`.

Classification:

- Tracked runtime/service consumer.
- Supabase service-role REST consumer.
- Not an end-user session/auth middleware consumer.
- Not a `/auth/me` or `/session/me` caller.

### `azure/functions/asset_ingest/ecc_portfolio_assets_service.py`

Verified tracked file evidence:

- `_AssetsExternalIdsPortfolioAssetsSource` reads a page of `assets` filtered by `external_ids`.
- The same source reads `asset_specs_reconciled` by `asset_id` to enrich portfolio asset rows with `units_count`.
- Requests use Supabase REST URLs and service-role `apikey` / `Authorization: Bearer` headers.
- The service falls back to stub payloads when backing configuration or REST reads are unavailable.

Classification:

- Tracked runtime/service consumer.
- Supabase service-role REST consumer.
- Read access to `assets` and `asset_specs_reconciled`.
- Not an end-user session/auth middleware consumer.
- Not a `/auth/me` or `/session/me` caller.

### `azure/functions/asset_ingest/ecc_portfolio_summary_service.py`

Verified tracked file evidence:

- `_AssetsExternalIdsPortfolioCohortResolver` reads an asset cohort from `assets` filtered by `external_ids`.
- It reads `asset_specs_reconciled` by `asset_id` to calculate total units.
- Requests use Supabase REST URLs and service-role `apikey` / `Authorization: Bearer` headers.
- The service falls back to stub summary fields when backing configuration or REST reads are unavailable.

Classification:

- Tracked runtime/service consumer.
- Supabase service-role REST consumer.
- Read access to `assets` and `asset_specs_reconciled`.
- Not an end-user session/auth middleware consumer.
- Not a `/auth/me` or `/session/me` caller.

### `supabase/migrations/0002_altus_core_identity.sql`

Verified tracked file evidence:

- Defines identity tables: `organizations`, `profiles`, `organization_members`.
- Defines asset tables: `assets`, `asset_data_raw`, `asset_specs_reconciled`.
- Enables RLS on those tables.
- Defines org-membership helper functions including `altus_current_org_id()` and `altus_is_org_member(uuid)`.
- Defines RPCs `altus_login(text)`, `altus_me()`, and `altus_logout()`.
- Grants RPC execution to `authenticated`.

Classification:

- Schema and RPC definition evidence.
- RLS/grant/policy evidence.
- Not application runtime caller code.

### `supabase/verification/0001_schema_inventory_assertions.sql`

Verified tracked file evidence:

- Checks presence of core identity and asset tables.
- Checks presence of identity and helper routines.
- Checks policy presence through `pg_policies`.

Classification:

- Schema verification evidence.
- Not application runtime caller code.

## Auth and Entitlement Findings

- `/auth/me` caller: NOT FOUND in tracked files.
- `/session/me` caller: NOT FOUND in tracked files.
- Entitlement middleware: NOT FOUND in tracked files.
- Role middleware: UNKNOWN. Schema-level `organization_members.role` and RPC output were found, but no tracked middleware implementation was proven.
- Permission middleware: NOT FOUND in tracked files.
- Scope middleware: NOT FOUND in tracked files.
- Session claim inspection: NOT FOUND in tracked files.
- Browser/client Supabase usage: NOT FOUND in tracked files. `git ls-files client` returned no tracked client files, and tracked search did not find Supabase JS `createClient`, `@supabase/supabase-js`, `supabase.auth`, `getSession`, `getUser`, `signIn`, or `signOut` usage.
- Service-role Supabase usage: FOUND in tracked Azure Function service files listed above.
- End-user auth/session route implementation: NOT FOUND in tracked files.

## CI and Verification Findings

Tracked CI/database verification evidence exists in `staging-nightly-audit.yml`.

This workflow is CI/database verification context only. It is not product runtime evidence, and it does not make `altus-core-staging` authoritative for Altus Core runtime, database, schema, auth, migration, onboarding, or proof decisions.

This workflow:

- Installs and logs into the Supabase CLI using GitHub secrets.
- Contains database URL construction for workflow execution, but no staging URL is used here as Altus Core evidence.
- Runs `supabase db push` against staging.
- Compares repository migrations to DB-applied migrations.
- Uses `psql` for table presence, RLS status, policy, and asset index checks.
- Uploads audit artifacts.

Classification:

- CI/database verification and audit usage.
- Not product runtime caller code.
- Not browser/client auth usage.
- Not `/auth/me` or `/session/me` caller evidence.
- Not Altus Core runtime proof, schema authority, auth evidence, migration evidence, or onboarding reference.

## Gaps and Required Follow-Up

- No tracked `docs/auth` baseline exists on `origin/main`.
- No full cross-repo frontend caller trace is included in this document.
- No browser/client auth consumer is proven from tracked files in this clean worktree.
- No entitlement middleware is proven from tracked files.
- No permission middleware is proven from tracked files.
- No scope middleware is proven from tracked files.
- No session endpoint caller is proven from tracked files.
- No `/auth/me` caller is proven from tracked files.
- No `/session/me` caller is proven from tracked files.
- No tracked consumer was found for `altus_users`, `altus_sessions`, `audit_log`, `client_companies`, `client_company_members`, `investors`, `investors_legacy`, `investors_legacy_2`, `investor_criteria`, or `investor_sync_queue`.
- `clients` appeared only as ordinary comment wording in the identity migration; no tracked `clients` table/object consumer was proven.
- External repositories such as frontend apps, field apps, construction manager apps, deal room apps, and investor-facing apps were not inspected in this clean worktree.
- Live database state was not queried.
- Deployed Azure behavior was not inspected.
- `altus-core-staging` was not used as Altus Core authority, runtime proof, schema authority, auth evidence, migration evidence, or onboarding reference.

## Governance Decision

This document is evidence-only.

`altus-core-staging` is temporary ECC-related infrastructure and is explicitly excluded as Altus Core authority.

Altus Core database authority must come only from the confirmed production Altus Core Supabase project and repo-tracked backend migration/schema evidence.

Altus Core runtime proof must come only from the confirmed live Altus Core backend/runtime.

It does not authorize schema changes, RLS changes, grant changes, auth changes, runtime changes, SQL execution, migrations, cleanup, deletion, CI changes, package changes, Azure Functions behavior changes, frontend changes, or legacy object removal.

It is not a full runtime dependency certification.

It is safe for documentation review only.
