# App Entitlement Model

Status: Draft / Pending Live Core DB Verification
Owner: Altus Core Backend
Applies to: ECC, Price Engine, Field App, Construction Manager, Investor Hub, Deal Room, Altus Core Admin, Future Apps
Canonical Repo: Altus-Realty-Group/altus-core-backend
Database Authority: Altus Core Supabase project srzwamukysmhiaaviwiv
Mutation Status: Documentation only; no DB writes

## Purpose

This document defines the Altus Core app registry, entitlement, role, permission, scope, assignment, and audit model.

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

## Separation Rules

The Altus Core model MUST keep the following concerns separate.

### Identity

Identity answers who the subject is.

### User Category

User category answers what business class the subject belongs to.

Current planning-scope categories:

- `altus_internal`
- `client`
- `contractor`
- `vendor`
- `investor`
- `service_account`

### Organization or Company Membership

Organization or company membership answers which company context the subject belongs to.

### Internal Role

Internal role answers what internal Altus operating role the subject holds.

### App Entitlement

App entitlement answers whether the subject may enter an app.

### Action Permission

Action permission answers what actions the subject may perform in an app.

### Scope Grant

Scope grant answers which resource boundary the app access applies to.

### Assignment

Assignment narrows access to the exact work items or resources assigned to the subject.

### Audit Event

Audit event records grant, denial, access, revocation, and privileged operations.

These layers MUST NOT be collapsed into one field or one app-local shortcut.

## App Registry Records

Each app MUST be inserted into the `apps` registry and then governed by entitlements and permissions.

| app_key | app_name | app_category | enabled | internal_only | supports_external_users | default_internal_access_policy | required_entitlement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ecc` | ECC | `operations` | true | true | false | `approved_internal_default` | `ecc.access` |
| `price_engine` | Price Engine | `underwriting` | true | true | false | `approved_internal_default` | `price_engine.access` |
| `field_app` | Field App | `field_operations` | true | false | true | `approved_internal_default` | `field_app.access` |
| `construction_manager` | Construction Manager | `construction` | true | false | true | `approved_internal_default` | `construction_manager.access` |
| `investor_hub` | Investor Hub | `investor_portal` | true | false | true | `invite_or_assignment_required` | `investor_hub.access` |
| `deal_room` | Deal Room | `deal_portal` | true | false | true | `invite_or_assignment_required` | `deal_room.access` |
| `altus_core_admin` | Altus Core Admin | `platform_admin` | true | true | false | `explicit_admin_only` | `altus_core_admin.access` |

## Internal Altus Access Model

Internal users MAY receive broad app access by approved policy, but they still require:

- approval or invitation
- role assignment
- permission checks
- audit
- suspension support

Recommended internal policy modes:

- `approved_internal_default`
- `explicit_admin_only`
- `internal_plus_scope`

## External Access Model

External users MUST satisfy all of the following:

1. active identity
2. active app entitlement
3. active scope grant
4. active assignment when required by the app
5. permission for the requested action

External users are DENIED BY DEFAULT from internal-only apps.

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

## Attorney Access Correction

Attorney access, if created, is for legal operations only.

Legal operations include evictions, damages, collections, demand letters, tenant or property disputes, and related legal work.

- attorneys do NOT receive Deal Room access by default
- attorneys do NOT receive global property, investor, underwriting, or admin access by default
- any attorney access MUST be case, property, or matter scoped
- attorney access SHOULD be treated as a limited external legal-work surface, not a general platform role

## Required App Access Definition Register

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

## Example Entitlement Records

```json
[
  {
    "user_id": "u_internal_001",
    "app_key": "price_engine",
    "entitlement_key": "price_engine.access",
    "status": "active",
    "granted_by": "u_admin_001",
    "reason": "underwriting analyst approval"
  },
  {
    "user_id": "u_contractor_009",
    "app_key": "field_app",
    "entitlement_key": "field_app.access",
    "status": "active",
    "granted_by": "u_ops_002",
    "reason": "assigned maintenance vendor"
  },
  {
    "user_id": "u_investor_014",
    "app_key": "deal_room",
    "entitlement_key": "deal_room.access",
    "status": "active",
    "granted_by": "u_deal_admin_001",
    "reason": "deal room invitation"
  }
]
```

## Example Scope Grants

```json
[
  {
    "user_id": "u_contractor_009",
    "app_key": "field_app",
    "scope_type": "work_order",
    "scope_id": "wo_123",
    "permission_set": ["field_app.work_order.view", "field_app.daily_log.submit"],
    "starts_at": "2026-06-09T00:00:00Z",
    "ends_at": "2026-06-16T00:00:00Z"
  },
  {
    "user_id": "u_vendor_044",
    "app_key": "construction_manager",
    "scope_type": "project",
    "scope_id": "proj_888",
    "permission_set": ["construction_manager.po.view", "construction_manager.photo.upload"]
  },
  {
    "user_id": "u_investor_014",
    "app_key": "deal_room",
    "scope_type": "deal",
    "scope_id": "deal_001",
    "permission_set": ["deal_room.document.view", "deal_room.comment.create"]
  }
]
```

## Minimum Proposed Tables

The following are the minimum logical tables for the shared auth and entitlement model.

- `apps`
- `app_entitlements`
- `roles`
- `permissions`
- `role_permissions`
- `user_role_assignments`
- `scoped_access_grants`
- `auth_audit_log`
- `user_identities`
- `organizations` or `client_companies`
- `organization_memberships` or `client_company_members`
- `app_sessions` or `altus_sessions`

Physical table names MUST be finalized only after live DB verification.

## Revocation Rules

Revocation MUST support:

- global user suspension
- per-app entitlement revocation
- scope grant revocation
- assignment revocation
- scheduled expiry

Revocation effects MUST include:

- navigation entry removed
- frontend route denial
- backend `403`
- RLS row isolation
- audit event recorded

## Audit Events

Minimum events:

- `auth.user_approved`
- `auth.user_suspended`
- `auth.app_entitlement_granted`
- `auth.app_entitlement_revoked`
- `auth.scope_grant_granted`
- `auth.scope_grant_revoked`
- `auth.access_denied`
- `auth.access_allowed`
- `auth.assignment_created`
- `auth.assignment_revoked`
