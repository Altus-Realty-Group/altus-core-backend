# Altus Auth Bridge Migration Plan

Status: Draft / Non-Executable Planning Only
Owner: Altus Core Backend
Canonical Repo: Altus-Realty-Group/altus-core-backend
Database Authority: Altus Core Supabase project srzwamukysmhiaaviwiv
Mutation Status: Planning only; no DB writes; no executable migration SQL

## Goal

Define the safe bridge from the live Altus Core physical schema to the platform auth model without assuming that repo-side table names are already the live truth.

## Planning Principle

Bridge first. Rename last.

If live tables exist and have data or downstream dependencies, preserve them and adapt the logical model through compatibility tables, views, functions, or phased migrations.

## Live Source Tables

### INFERRED Live Source Tables

- `public.altus_users`
- `public.altus_sessions`
- `public.client_companies`
- `public.client_company_members`
- `public.clients`

### VERIFIED_REPO Shared-Auth Repo Tables

- `public.profiles`
- `public.organizations`
- `public.organization_members`

### VERIFIED_REPO Shared-Auth Repo Functions

- `public.altus_current_org_id()`
- `public.altus_is_org_member(uuid)`
- `public.altus_login(text)`
- `public.altus_me()`
- `public.altus_logout()`

## Proposed Canonical Logical Model

The logical model MUST support:

- platform user
- user identity link
- organization or company container
- organization or company membership
- app registry
- app entitlement
- internal role
- permission
- role permission mapping
- user role assignment
- scoped access grant
- app session
- auth audit log

Logical tables:

- `core_users`
- `user_identities`
- `organizations`
- `organization_memberships`
- `apps`
- `app_entitlements`
- `roles`
- `permissions`
- `role_permissions`
- `user_role_assignments`
- `scoped_access_grants`
- `app_sessions`
- `auth_audit_log`

These are logical targets, not final physical names.

## Physical Preservation Strategy

### Preserve Or Replace `public.altus_users`

Recommendation: preserve if it exists live.

Reason:

- it may already be the physical platform-user table
- row counts may be zero today, but dependencies must be checked before replacement
- platform docs can map logical `core_users` to physical `altus_users`

Proposed bridge path:

- preserve physical `public.altus_users`
- map logical platform-user model to it
- only consider replacement if live verification proves it is empty and unused

### Preserve Or Replace `public.client_companies` And `public.client_company_members`

Recommendation: preserve if they exist live.

Reason:

- they likely already encode external company and membership semantics closer to the business model than generic `organizations`
- repo-side `organizations` and `organization_members` can be treated as logical equivalents, not forced physical replacements

Proposed bridge path:

- preserve physical `client_companies`
- preserve physical `client_company_members`
- map logical organization and membership concepts to those tables where appropriate
- add compatibility views or helper functions if repo-side code expects organization-style naming

## Compatibility Strategy

Use a bridge model as canonical.

Bridge components may include:

- compatibility views
- compatibility helper functions
- phased backfill tables
- read-through adapters in backend middleware
- app-by-app migration away from local auth assumptions

Do not start with destructive rename.

## Proposed App Registry Model

Physical target after live verification:

- `public.apps`

Required app keys:

- `ecc`
- `price_engine`
- `field_app`
- `construction_manager`
- `investor_hub`
- `deal_room`
- `altus_core_admin`

Required fields:

- `id`
- `app_key`
- `app_name`
- `app_category`
- `enabled`
- `internal_only`
- `supports_external_users`
- `default_internal_access_policy`
- `required_entitlement`
- `route_metadata_json`
- `domain_metadata_json`
- `created_at`
- `updated_at`

Future apps must be plug-and-play by inserting app records and related entitlements, not by rewriting auth architecture.

## Proposed App Entitlement Model

Physical target after live verification:

- `public.app_entitlements`

Required semantics:

- explicit app entry grant
- grant status
- granted by
- grant reason
- effective window
- revoke metadata

## Proposed Role And Permission Model

Physical targets after live verification:

- `public.roles`
- `public.permissions`
- `public.role_permissions`
- `public.user_role_assignments`

This model separates:

- internal role
- action permission
- user assignment to role

It must not collapse role and app access into the same field.

## Proposed Scoped Access Grant Model

Physical target after live verification:

- `public.scoped_access_grants`

Supported scope types SHOULD include:

- organization
- company
- property
- project
- deal
- opportunity
- scenario
- portfolio
- job
- task
- work_order
- purchase_order
- portal_context

Assignments for contractor or vendor work can remain a separate table or a constrained scope-grant subtype, but logical separation must remain clear.

## Proposed Audit Model

Physical target after live verification:

- `public.auth_audit_log`

This log should capture:

- user approval
- app entitlement grant
- app entitlement revoke
- scope grant grant
- scope grant revoke
- access allowed
- access denied
- assignment created
- assignment revoked
- user suspended
- session invalidated

## Segmentation Rules

The bridge model MUST support these user classes:

- Altus internal users
- clients
- contractors
- vendors
- investors
- lenders
- agents
- owners
- tenants
- guests
- service accounts

Required rules:

- internal Altus email or domain is not automatic admin
- approved internal Altus users may receive broad app access only through explicit internal role and entitlement policy
- external users require explicit app entitlement plus explicit scope grant
- contractors must not access Price Engine, ECC, Investor Hub, Deal Room, or Altus Core Admin by default
- contractors may access only Field App and or Construction Manager if explicitly entitled and assigned
- investor access must flow through Investor Hub or scoped Deal Room access, not raw Price Engine access
- Deal Room access must be deal or invite scoped
- ECC and Altus Core Admin are internal-only by default
- backend and RLS must deny even when frontend navigation is wrong

## Default App Segmentation

- ECC: internal only
- Price Engine: internal only
- Field App: internal plus scoped contractors, vendors, and field users
- Construction Manager: internal plus scoped contractors, vendors, estimators, and approved external project users
- Investor Hub: investor-scoped
- Deal Room: deal or invite scoped
- Altus Core Admin: platform-owner and super-admin only
- future apps: denied by default until entitlement exists

## RLS Strategy

RLS remains mandatory.

Recommended approach:

- keep or add helper functions that resolve current platform user, app entitlement, scope, and assignment
- preserve existing proven RLS patterns where possible
- add new RLS policies for app registry, entitlements, scope grants, and audit tables carefully
- never weaken RLS to make migration easier

## Rollback Strategy

Rollback must be compatibility-first.

Required rollback characteristics:

- no destructive rename in the first migration wave
- ability to disable newly introduced bridge reads without dropping live source tables
- ability to stop app cutover per app, not platform-wide
- ability to preserve historical audit records

## Future App Onboarding Strategy

Every new app must follow the shared onboarding path:

1. add app registry record
2. define app entitlement key
3. define internal access policy
4. define external eligibility
5. define scopes
6. define permissions
7. define backend guards
8. define frontend session or me consumption
9. define audit events
10. define RLS requirements
11. test denial behavior before release

## Migration Preconditions

- direct live verification of `altus_users`, `altus_sessions`, `client_companies`, and `client_company_members`
- direct row counts and dependency checks
- direct RLS and policy inspection
- direct trigger and function inventory
- approved physical-name mapping

## Stop Conditions

- stop if live inspection is still blocked
- stop if destructive rename is proposed before dependency proof
- stop if any step would weaken RLS
- stop if any step requires app runtime changes in this lane

## Recommended Next Step

Run the read-only SQL inspection pack from `LIVE_CORE_AUTH_SCHEMA_AUDIT.md` through an authenticated lane, then finalize the physical-name mapping before any executable migration draft is written.
