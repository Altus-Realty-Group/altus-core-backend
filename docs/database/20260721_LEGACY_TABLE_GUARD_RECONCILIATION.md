# 2026-07-21 Supabase migration reconciliation

## Status

This record reconciles two migrations already present in the canonical ECC Supabase migration history with repository authority:

- `20260721170328_harden_owned_tables_and_block_legacy_api_20260721`
- `20260721170720_allow_postgrest_pre_request_guard_execution_20260721`

Issue: #94

This is a historical backfill. The associated pull request must not be used to re-apply either migration to the canonical database.

## Why reconciliation is required

The live migration records and their statement arrays existed outside this repository. Without matching files in `supabase/migrations/`, the database control could not be reviewed, reproduced in a new environment, or governed by the repository DB proof gate.

## Technical effect

The first migration:

1. Creates the `private` schema if absent.
2. Creates `private.block_unowned_legacy_table_api()` as a security-invoker PL/pgSQL function with an empty `search_path`.
3. Blocks direct Data API requests whose normalized request path is either:
   - `dl_aging_export_2025_11_08`
   - `dl_payment_status_audit`
4. Configures `authenticator.pgrst.db_pre_request` to call the guard.
5. Enables RLS on each ordinary or partitioned `public` table owned by the executing project-owner role.
6. Revokes all table privileges from `PUBLIC` on those owned tables.
7. Revokes `TRUNCATE`, `REFERENCES`, and `TRIGGER` from `anon` and `authenticated` on those owned tables.
8. Revokes table default privileges from `PUBLIC`, `anon`, and `authenticated` for future tables created by `postgres` in `public`.
9. Requests a PostgREST configuration reload.

The second migration grants the schema usage and function execution required for the PostgREST pre-request path, then requests another configuration reload.

## Direct database evidence reviewed on 2026-07-22

- Both migration versions and names are present in `supabase_migrations.schema_migrations`.
- The stored statement arrays are the source for the two repository migration files.
- The guard is security invoker and pins an empty `search_path`.
- The `authenticator` role contains the pre-request configuration.
- Required PostgREST-facing roles have schema usage and function execution.
- The two legacy tables exist and were observed with RLS disabled.
- All other observed public tables had RLS enabled.
- The two legacy tables were observed empty; emptiness is not an invariant and is not asserted by verification SQL.

## Verification

Run `supabase/verification/20260721_legacy_table_guard_reconciliation.sql` after apply in a non-canonical target. It fails closed when:

- either migration record is absent;
- the guard is absent, security definer, or lacks the pinned search path;
- either legacy path is not blocked;
- the authenticator setting or execution privileges are incomplete;
- a project-owner-owned public table lacks RLS;
- prohibited table or default privileges remain.

The verification accepts a future state where either legacy table gains table-native RLS. It does not require RLS to remain disabled.

## Deployment boundary

- Canonical ECC database: no apply. Both versions are already recorded.
- New or rebuilt environment: normal staging-first apply and verification.
- Production promotion: manual authorization under the repository deployment SOP.
- No credential values or project secrets belong in the issue, migration files, verification output, or PR.

## Rollback boundary

Reverting the reconciliation PR only removes repository artifacts; it does not authorize a live database rollback.

For a newly applied environment, rollback requires an approved pre-change privilege and RLS snapshot. Removing the guard requires clearing `pgrst.db_pre_request`, removing related grants/function objects, and reloading PostgREST only after alternate controls are proven. RLS and privilege hardening must not be broadly reversed without a reviewed least-privilege policy/grant restoration plan.
