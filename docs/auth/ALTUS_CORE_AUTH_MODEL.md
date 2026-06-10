# Altus Core Auth Model

Status: Draft / Pending Live Core DB Verification
Owner: Altus Core Backend
Applies to: ECC, Price Engine, Field App, Construction Manager, Investor Hub, Deal Room, Altus Core Admin, Future Apps
Canonical Repo: Altus-Realty-Group/altus-core-backend
Database Authority: Altus Core Supabase project srzwamukysmhiaaviwiv
Mutation Status: Documentation only; no DB writes

## Executive Decision

Altus Core Auth MUST be the shared platform identity and entitlement service for the Altus application ecosystem.

Individual apps MUST NOT invent separate permanent auth models.

Transitional app-local auth MAY remain only until each app is migrated to the shared Altus Core model.

Every current and future app MUST plug into the same platform primitives:

- shared identity
- app registry
- app entitlements
- internal roles
- action permissions
- scoped grants
- assignments where required
- audit trail

This decision applies to:

- ECC
- Price Engine
- Field App
- Construction Manager
- Investor Hub
- Deal Room
- Altus Core Admin
- future Altus apps

## Verified Evidence vs Pending Verification

### Verified Repository Evidence

The backend repository currently proves a shared-auth direction in `supabase/migrations/0002_altus_core_identity.sql` and the database docs:

- `public.organizations`
- `public.profiles`
- `public.organization_members`
- `public.altus_current_org_id()`
- `public.altus_is_org_member(uuid)`
- `public.altus_login(text)`
- `public.altus_me()`
- `public.altus_logout()`

The repository also proves `0003_altus_is_org_member_service_role.sql`, which intentionally changes `altus_is_org_member` so `service_role` can bypass the membership check server-side.

### Verified Cross-App Divergence

The current Altus app estate is not yet on one shared auth model.

- Price Engine currently uses transitional Supabase session hydration and operator-session normalization.
- Field App currently uses app-local Passport plus optional Azure AD patterns.
- Construction Manager currently uses app-local auth support tables and app-specific RLS helpers.
- Deal Room currently uses local Express auth and a local role-permission map.
- ECC frontend inspection during this task did not prove a shared auth integration surface.

### Pending Live Verification

Direct live inspection of Altus Core was not performed in this task.

Because database is the source of truth, physical naming and migration decisions remain pending until the live Altus Core schema is inspected directly.

## Shared Platform Model

The platform model MUST keep these concerns separate.

### Identity

Identity answers who the subject is.

There MUST be one shared Altus identity per person or service account, backed by Supabase Auth and mapped to a platform user record.

## App-First Access Modeling Rule

Access MUST be defined from actual Altus apps and workflows backward.

Do NOT create user roles just because a real estate business might interact with that party.

Every role, permission, and entitlement MUST map to:

- a real Altus app
- a real workflow
- a real screen or data surface
- a real business reason
- a real data scope
- a known create, edit, view, or delete boundary

Unknown future users MUST remain open questions, not modeled permissions.

### User Category

User category answers what business class the subject belongs to.

Current planning-scope user categories:

- `altus_internal`
- `client`
- `contractor`
- `vendor`
- `investor`
- `service_account`

User category MUST NOT be collapsed into role, entitlement, or scope.

### Organization or Company Membership

Organization or company membership answers what company context the subject belongs to.

This logical layer may map to `organizations` and `organization_memberships` or to `client_companies` and `client_company_members` after live verification.

### Internal Role

Internal role answers what internal Altus operating role the subject has.

Canonical internal roles:

- `platform_owner`
- `super_admin`
- `admin`
- `operations_manager`
- `property_manager`
- `construction_manager`
- `field_supervisor`
- `leasing`
- `accounting`
- `legal`
- `analyst`
- `viewer`

Internal role MUST NOT be treated as app access by itself.

### App Entitlement

App entitlement answers whether the subject may enter a given app.

Required current app entitlements:

- `ecc.access`
- `price_engine.access`
- `field_app.access`
- `construction_manager.access`
- `investor_hub.access`
- `deal_room.access`
- `altus_core_admin.access`

### Action Permission

Action permission answers what the subject may do inside an app.

Examples:

- `ecc.operations.view`
- `ecc.legal.note.view`
- `price_engine.scenario.edit`
- `field_app.daily_log.submit`
- `construction_manager.po.view`
- `deal_room.document.sign`

### Scope Grant

Scope grant answers where the entitlement or permission applies.

Supported scope types SHOULD include:

- `organization`
- `company`
- `property`
- `project`
- `deal`
- `opportunity`
- `scenario`
- `portfolio`
- `job`
- `task`
- `work_order`
- `purchase_order`
- `portal_context`

### Assignment

Assignment narrows access to resources explicitly assigned to the user.

Assignments are required for contractor and vendor workflows in Field App and Construction Manager.

### Audit Trail

All grants, denials, access decisions, revocations, and sensitive operations MUST be auditable.

## App Registry

Every app MUST be registerable in the database without rewriting the auth system.

Required `apps` columns:

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

Required current app keys:

- `ecc`
- `price_engine`
- `field_app`
- `construction_manager`
- `investor_hub`
- `deal_room`
- `altus_core_admin`

Future apps MUST be denied by default until an app registry record and entitlement model exist.

## Internal Altus Access Policy

Altus internal users MAY receive broad multi-app access by approved policy, but they are still subject to:

- explicit approval or invitation
- internal role assignment
- action-level permission checks
- per-app suspension
- global suspension
- audit

An `@altus-realty.com` email address MUST NOT be treated as automatic admin.

## Explicitly Excluded Access Classes - Current Scope

The following are NOT current app-access classes unless later approved by Dion with a specific app workflow:

- appraisers
- insurance contacts
- inspectors
- title companies
- closing attorneys
- external agents
- external brokers
- generic vendors not tied to a real Altus app workflow
- bookkeeping or accounting app users, because no bookkeeping app is currently approved in this auth model

## External Segmented Access Policy

External users MUST have explicit app entitlement and explicit scope.

External users:

- MUST NOT access internal-only routes
- MUST NOT infer unrelated Altus apps
- MUST NOT cross client, contractor, vendor, or investor boundaries
- MUST have revocable grants
- MUST have grant, denial, and revocation audit records

## Attorney Access Correction

Attorney access, if created, is for legal operations only.

Legal operations include evictions, damages, collections, demand letters, tenant or property disputes, and related legal work.

- attorneys do NOT receive Deal Room access by default
- attorneys do NOT receive global property, investor, underwriting, or admin access by default
- any attorney access MUST be case, property, or matter scoped
- attorney access SHOULD be treated as a limited external legal-work surface, not a general platform role

## App Defaults

### ECC

ECC is internal-only by default.

### Price Engine

Price Engine is internal-only by default.

### Field App

Field App supports internal users plus scoped contractors and vendors tied to real field workflows.

### Construction Manager

Construction Manager supports internal users plus scoped contractors and vendors tied to real project workflows.

### Investor Hub

Investor Hub is investor-scoped.

### Deal Room

Deal Room is deal-scoped and invite-scoped.

Attorney access is NOT implied by default.

### Altus Core Admin

Altus Core Admin is platform-owner or super-admin only.

## Required App Access Definition Register

Each real Altus app MUST be defined in an app access register before entitlement, role, or RLS design is finalized.

| Field | Required Definition |
| --- | --- |
| App Name | Name of the actual Altus app or module |
| Primary Purpose | What the app exists to do |
| Core Workflow | Main business process supported |
| Primary Internal Users | Altus staff roles that use it |
| External Users | External users, if any |
| External Access Type | None, portal, task-only, document-only, case-scoped, deal-scoped, property-scoped, or similar |
| Data Access Scope | Exact data boundaries |
| Create/Edit/Delete Rights | Who can change data |
| View-Only Rights | Who can only view data |
| Explicit No-Access Parties | Parties that should not access this app |
| Auth/RLS Notes | Required entitlement and RLS implications |
| Open Questions | Unknowns requiring Dion approval |

No entitlement table, app role, or RLS design SHOULD be finalized until the app register is completed or at least seeded with the real Altus apps currently in scope.

## Live Schema Reconciliation Required Before Migration

Prior PM evidence indicates the live Altus Core project may contain:

- `altus_users`
- `altus_sessions`
- `client_companies`
- `client_company_members`

Repository migration evidence currently appears to use:

- `profiles`
- `organizations`
- `organization_members`
- auth RPC concepts such as `altus_login`, `altus_me`, and `altus_logout`

No migration SHOULD be applied until the live Altus Core schema is directly inspected and mapped.

The recommended path is a bridge or migration strategy, not a blind destructive rename.

## Recommended Canonical Model Decision

The recommended canonical model is a bridge or migration model.

Why:

1. The backend repo already expresses the intended shared-auth direction.
2. The live Altus Core physical table names are not yet directly verified in this task.
3. The app repos prove multiple divergent auth implementations already exist.

Current decision:

- logical canonical model: the platform model in this document
- physical naming: pending direct live schema verification
- migration posture: compatibility-first bridge plan

## Enforcement Model

Backend enforcement order MUST be:

1. authenticate session
2. resolve platform user
3. confirm app entitlement
4. confirm required permission
5. confirm scope grant or assignment
6. emit audit event

Frontend route guards MUST consume only safe session or me data and MUST NOT be treated as the primary enforcement boundary.

RLS MUST remain enforced for data surfaces.

Service-role credentials MUST remain server-side only.

## Example Safe Session or Me Payload

```json
{
  "user": {
    "id": "c4d5d25f-8e4a-4f3b-9f3b-0fd9dbd4c501",
    "email": "operator@altus-realty.com",
    "display_name": "Altus Operator",
    "user_category": "altus_internal",
    "global_status": "active"
  },
  "apps": [
    {
      "app_key": "ecc",
      "entitled": true,
      "roles": ["operations_manager"],
      "permissions": ["ecc.operations.view", "ecc.field.dispatch"],
      "scope_summary": { "type": "organization", "ids": ["org_001"] }
    },
    {
      "app_key": "price_engine",
      "entitled": true,
      "roles": ["analyst"],
      "permissions": ["price_engine.opportunity.view", "price_engine.scenario.edit"],
      "scope_summary": { "type": "organization", "ids": ["org_001"] }
    }
  ]
}
```

## Next Implementation Plan

1. Perform live core schema inspection for `srzwamukysmhiaaviwiv`.
2. Choose bridge versus migration physical naming after the live inspection.
3. Draft the non-destructive migration and compatibility plan.
4. Define the canonical `session/me` endpoint contract.
5. Implement reusable backend middleware for entitlement, permission, scope, and assignment checks.
6. Add backend and policy-facing tests.
7. Migrate Price Engine first.
8. Migrate Field App and Construction Manager external access paths.
9. Migrate Deal Room and Investor Hub scoped access paths.
10. Remove deprecated app-local auth assumptions only after proof.
