# SCHEMA_INVENTORY_V1

Status: staging-proof reconciliation snapshot
Proof source: `supabase_apply` staging run `23061906826`
Verification SQL: `supabase/verification/0001_schema_inventory_assertions.sql`
Proof timestamp (UTC): 2026-03-13T17:06:40.850528Z
Staging project ref: `sdlgnecmvupzcmxqgnlu`

This document records only what the staging verification artifact proved. It does not claim production truth.

## Proven Tables Present In Staging

Confirmed present:
- `public.organizations`
- `public.profiles`
- `public.organization_members`
- `public.assets`
- `public.asset_data_raw`
- `public.asset_specs_reconciled`

## Proven Functions / RPCs Present In Staging

Confirmed present:
- `public._touch_updated_at`
- `public.altus_current_org_id`
- `public.altus_is_org_member`
- `public.altus_login`
- `public.altus_me`
- `public.altus_logout`

## Proven Policy Objects Present In Staging

Confirmed present:
- `public.organization_members.org_members_select`
- `public.organizations.org_select`
- `public.profiles.profiles_select_self`
- `public.profiles.profiles_update_self`
- `public.assets.assets_select`
- `public.assets.assets_insert`
- `public.assets.assets_update`
- `public.assets.assets_delete`
- `public.asset_data_raw.adr_select`
- `public.asset_data_raw.adr_insert`
- `public.asset_data_raw.adr_update`
- `public.asset_data_raw.adr_delete`
- `public.asset_specs_reconciled.asr_select`
- `public.asset_specs_reconciled.asr_insert`
- `public.asset_specs_reconciled.asr_update`
- `public.asset_specs_reconciled.asr_delete`

## Confirmed Missing Objects In Staging

Confirmed missing relative to repo-proven expectations:
- `public.assets.assets_org_isolation`

## Confirmed Repo-vs-Staging Mismatches

### Columns expected by repo truth but missing in staging

Confirmed missing in staging:
- `public.asset_data_raw.created_at`
- `public.asset_data_raw.organization_id`
- `public.asset_data_raw.payload`
- `public.asset_data_raw.payload_sha256`
- `public.asset_data_raw.source_record_id`
- `public.assets.name`

### Live staging columns not currently proven in repo inventory

Confirmed present in staging but not in the current repo inventory assertion set:
- `public.asset_specs_reconciled.created_at`
- `public.asset_specs_reconciled.effective_at`
- `public.asset_specs_reconciled.id`
- `public.asset_specs_reconciled.provenance`
- `public.asset_specs_reconciled.spec_version`

## Reconciliation Meaning

What the proof supports:
- the core table set exists in staging
- the expected function / RPC set exists in staging
- almost all repo-proven policy objects exist in staging

What the proof does not support:
- a claim that repo truth and staging are fully reconciled
- a claim that current runtime write expectations are fully aligned with live staging columns
- a claim that `assets_org_isolation` exists in staging

## Readiness Decision

Repository truth does not yet match staging closely enough to begin schema-changing DB work safely.

Why:
- one expected policy object is missing from staging
- current runtime-oriented column expectations for `asset_data_raw` are not present in staging
- staging contains additional `asset_specs_reconciled` columns that are not yet represented in the repo-proven inventory

## Next DB-Only Action

Open a DB-only reconciliation PR that decides whether each mismatch should be resolved by:
- backfilling repo truth to match staging
- normalizing staging to the intended repo schema
- or explicitly marking the object as intentionally out-of-scope for current DB governance
