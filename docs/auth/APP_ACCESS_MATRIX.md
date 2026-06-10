# App Access Matrix

Status: Draft / Pending Live Core DB Verification
Owner: Altus Core Backend
Applies to: ECC, Price Engine, Field App, Construction Manager, Investor Hub, Deal Room, Altus Core Admin, Future Apps
Canonical Repo: Altus-Realty-Group/altus-core-backend
Database Authority: Altus Core Supabase project srzwamukysmhiaaviwiv
Mutation Status: Documentation only; no DB writes

## Summary

This matrix defines default access posture. It does not replace action permissions, scoped grants, assignments, backend hard denials, or RLS.

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

Legend:

- `default` means allowed by approved internal policy
- `explicit` means allowed only by explicit entitlement
- `scoped` means explicit entitlement plus scope grant or assignment
- `deny` means blocked by default

| App | Altus Internal | Client | Contractor | Vendor | Investor | Service Account |
| --- | --- | --- | --- | --- | --- | --- |
| ECC | default | deny | deny | deny | deny | explicit |
| Price Engine | explicit | deny | deny | deny | deny | explicit |
| Field App | explicit | deny | scoped | scoped | deny | explicit |
| Construction Manager | explicit | deny | scoped | scoped | deny | explicit |
| Investor Hub | explicit if needed | deny | deny | deny | scoped | explicit |
| Deal Room | explicit if needed | scoped | deny by default | deny by default | scoped | explicit |
| Altus Core Admin | explicit admin only | deny | deny | deny | deny | explicit |
| Future Apps | deny by default until registered | deny | deny | deny | deny | explicit if approved |

## Default App Policy

- ECC: internal only
- Price Engine: internal only
- Field App: internal plus scoped contractors and vendors tied to real field workflows
- Construction Manager: internal plus scoped contractors and vendors tied to real project workflows
- Investor Hub: investor-scoped
- Deal Room: deal or invite scoped
- Altus Core Admin: internal platform-owner or super-admin only
- Future apps: DENIED BY DEFAULT until app entitlement exists

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

## App-Specific Rules

### ECC

- internal command center only
- external users denied by default
- future external portal views MUST use separate curated entitlements

### Price Engine

- internal underwriting tool only by default
- investors and clients consume published outputs elsewhere
- no raw underwriting access for external users unless an explicit future policy changes that rule

### Field App

Allowed contractor actions when granted:

- view assigned work orders, jobs, tasks, and properties
- upload photos or videos
- submit daily logs
- submit completion notes
- submit quotes or invoices only if separately granted
- view lockbox or access notes only if explicit time-bound access exists

Denied contractor actions:

- ECC access
- Price Engine access
- Investor Hub access
- Deal Room access unless separately invited for a specific scoped case
- unrelated properties
- unrelated contractors' work
- owner financials
- acquisition underwriting
- internal legal notes

### Construction Manager

Allowed contractor or vendor actions when granted:

- view assigned project
- view assigned task, trade, schedule, or PO
- upload required media
- submit daily logs
- see approved scope documents
- view payment or PO status only when granted

Denied contractor or vendor actions:

- internal estimates unless published
- other bids
- unrelated scopes
- owner financials
- investor underwriting
- global cost catalog unless explicitly exposed
- internal management notes

### Investor Hub

- investor-scoped
- limited to assigned investor profile, commitments, communications, and published opportunities or deals
- operational data denied unless explicitly published

### Deal Room

- deal-scoped
- only invited users may enter a room
- access levels SHOULD include `viewer`, `commenter`, `signer`, `investor`, `client_admin`, and `room_admin`
- only published artifacts are visible

## Attorney Access Correction

Attorney access, if created, is for legal operations only.

Legal operations include evictions, damages, collections, demand letters, tenant or property disputes, and related legal work.

- attorneys do NOT receive Deal Room access by default
- attorneys do NOT receive global property, investor, underwriting, or admin access by default
- any attorney access MUST be case, property, or matter scoped
- attorney access SHOULD be treated as a limited external legal-work surface, not a general platform role

### Altus Core Admin

- platform-owner or super-admin only
- not available to general internal operators

### Future Apps

- no app may ship with visibility or access until the app registry, entitlement, scope, and enforcement surfaces exist

## Denial Examples

| Scenario | Result |
| --- | --- |
| Contractor requests `price_engine` route | `403 app_not_entitled` |
| Investor requests uninvited deal room | `403 deal_scope_required` |
| Vendor requests another vendor's PO | `403 assignment_required` |
| Internal analyst opens `altus_core_admin` without admin entitlement | `403 permission_denied` |

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
