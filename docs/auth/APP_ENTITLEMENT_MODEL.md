# App Entitlement Model

Status: Draft / Pending Live Core DB Verification
Owner: Altus Core Backend
Applies to: ECC, Price Engine, Field App, Construction Manager, Investor Hub, Deal Room, Altus Core Admin, Future Apps
Canonical Repo: Altus-Realty-Group/altus-core-backend
Database Authority: Altus Core Supabase project srzwamukysmhiaaviwiv
Mutation Status: Documentation only; no DB writes

## Purpose

This document defines the Altus Core app registry, entitlement, role, permission, scope, assignment, and audit model.

## Separation Rules

The Altus Core model MUST keep the following concerns separate.

### Identity

Identity answers who the subject is.

### User Category

User category answers what business class the subject belongs to.

Canonical categories:

- `altus_internal`
- `client`
- `contractor`
- `vendor`
- `investor`
- `lender`
- `agent`
- `owner`
- `tenant`
- `guest`
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
