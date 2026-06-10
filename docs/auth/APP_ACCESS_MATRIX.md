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

### ECC Register Entry

- internal command center only
- external users denied by default
- future external portal views MUST use separate curated entitlements

### Price Engine Register Entry

- internal underwriting tool only by default
- investors and clients consume published outputs elsewhere
- no raw underwriting access for external users unless an explicit future policy changes that rule

### Field App Register Entry

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

### Construction Manager Register Entry

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

### Deal Room Register Entry

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

## Seeded Current App Access Register

### ECC

| Field | Required Definition |
| --- | --- |
| App Name | ECC |
| Primary Purpose | Internal command center and operations surface |
| Core Workflow | Internal operations coordination and approved internal command workflows |
| Primary Internal Users | Approved internal Altus operators, including operations and legal staff when the workflow is documented |
| External Users | None in current scope |
| External Access Type | None |
| Data Access Scope | Internal command-center data and curated ECC-only operational surfaces |
| Create/Edit/Delete Rights | Approved internal ECC operators only |
| View-Only Rights | Approved internal read-only users only |
| Explicit No-Access Parties | Clients, contractors, vendors, investors, attorneys by default, appraisers, insurance contacts, inspectors, title companies, closing attorneys, external agents, external brokers |
| Auth/RLS Notes | `ecc.access`; internal-only by default; any future external portal view must be a separate curated entitlement and separate surface |
| Open Questions | Which exact ECC screens are legal-operations versus general operations surfaces |

### Price Engine

| Field | Required Definition |
| --- | --- |
| App Name | Price Engine |
| Primary Purpose | Internal underwriting and scenario analysis |
| Core Workflow | Internal pricing, underwriting, and scenario review |
| Primary Internal Users | Approved internal underwriting and analysis staff |
| External Users | None in current direct app scope |
| External Access Type | None |
| Data Access Scope | Internal underwriting scenarios and related internal decision-support data |
| Create/Edit/Delete Rights | Approved internal Price Engine users only |
| View-Only Rights | Approved internal read-only users only |
| Explicit No-Access Parties | Clients, contractors, vendors, investors, attorneys by default, appraisers, insurance contacts, inspectors, title companies, closing attorneys, external agents, external brokers |
| Auth/RLS Notes | `price_engine.access`; internal-only by default; published outputs elsewhere are not the same as raw app access |
| Open Questions | Which published outputs may be exposed outside the app and through which separate reporting surface |

### Field App

| Field | Required Definition |
| --- | --- |
| App Name | Field App |
| Primary Purpose | Field work execution and assigned operational task handling |
| Core Workflow | Assigned work orders, jobs, tasks, property access, logs, and completion activity |
| Primary Internal Users | Altus field operations staff and supervising internal operators |
| External Users | Contractors and vendors tied to real field workflows |
| External Access Type | Task-only, assignment-scoped, and property-scoped |
| Data Access Scope | Assigned work orders, jobs, tasks, properties, and explicitly granted supporting notes or media surfaces |
| Create/Edit/Delete Rights | Internal users manage work items; assigned external users may submit logs, media, and completion updates when explicitly granted |
| View-Only Rights | Assigned external users may view only their assigned work and explicitly granted supporting details |
| Explicit No-Access Parties | Investors, attorneys by default, appraisers, insurance contacts, inspectors, title companies, closing attorneys, external agents, external brokers |
| Auth/RLS Notes | `field_app.access`; external users require explicit entitlement plus assignment or scope; no ECC, Price Engine, Investor Hub, or Deal Room access by implication |
| Open Questions | Whether any client-facing field visibility is a real approved workflow or should remain denied |

### Construction Manager

| Field | Required Definition |
| --- | --- |
| App Name | Construction Manager |
| Primary Purpose | Project execution, task coordination, schedule handling, and PO-related workflow |
| Core Workflow | Assigned project, trade, task, schedule, document, and PO coordination |
| Primary Internal Users | Construction managers and approved internal project staff |
| External Users | Contractors and vendors tied to real project workflows |
| External Access Type | Project-scoped and assignment-scoped |
| Data Access Scope | Assigned project, task, trade, schedule, PO, and approved scope-document surfaces |
| Create/Edit/Delete Rights | Internal project staff manage project records; assigned external users may submit approved media or logs and view approved status surfaces when granted |
| View-Only Rights | Assigned external users may view approved assigned project and PO-status surfaces only |
| Explicit No-Access Parties | Investors, attorneys by default, appraisers, insurance contacts, inspectors, title companies, closing attorneys, external agents, external brokers |
| Auth/RLS Notes | `construction_manager.access`; scope and assignment remain mandatory for external users; no investor underwriting or unrelated project visibility |
| Open Questions | Whether any external project user exists beyond contractor or vendor workflow and, if so, which exact screens require it |

### Deal Room

| Field | Required Definition |
| --- | --- |
| App Name | Deal Room |
| Primary Purpose | Deal-scoped invited document and collaboration surface |
| Core Workflow | Invited deal review, document access, commenting, and signing workflows |
| Primary Internal Users | Approved internal deal team and room administrators |
| External Users | Investors and clients only when tied to a documented invited deal workflow |
| External Access Type | Deal-scoped, invite-scoped, and document-scoped |
| Data Access Scope | Only the invited deal room and only published artifacts within that room |
| Create/Edit/Delete Rights | Internal room administrators and explicitly authorized internal deal users; invited external users only according to granted room access level |
| View-Only Rights | Invited viewers and limited invited participants according to room-level permissions |
| Explicit No-Access Parties | Attorneys by default, contractors, vendors, appraisers, insurance contacts, inspectors, title companies, closing attorneys, external agents, external brokers |
| Auth/RLS Notes | `deal_room.access`; invite and deal scope are mandatory; attorney access is not implied by default |
| Open Questions | Which room-level access labels remain approved after app-first review and whether any client-admin label should be narrowed |

### Investor Hub Register Entry

| Field | Required Definition |
| --- | --- |
| App Name | Investor Hub |
| Primary Purpose | Investor-facing access to approved investor communications and published opportunity or deal surfaces |
| Core Workflow | Assigned investor profile review, commitments, communications, and published opportunity or deal visibility |
| Primary Internal Users | Approved internal staff supporting investor communications and publishing workflows |
| External Users | Investors only |
| External Access Type | Investor-scoped portal |
| Data Access Scope | Assigned investor profile, commitments, communications, and published opportunities or deals only |
| Create/Edit/Delete Rights | Internal approved users manage published investor-facing content and assignment decisions |
| View-Only Rights | Assigned investors view only their approved investor-facing surfaces |
| Explicit No-Access Parties | Contractors, vendors, attorneys by default, appraisers, insurance contacts, inspectors, title companies, closing attorneys, external agents, external brokers |
| Auth/RLS Notes | `investor_hub.access`; investor-scoped; external access must stay limited to a documented investor workflow, not broad platform access |
| Open Questions | Whether Investor Hub is a distinct approved app surface today or remains partially satisfied through scoped Deal Room or reporting workflows |

### Altus Core Admin Register Entry

| Field | Required Definition |
| --- | --- |
| App Name | Altus Core Admin |
| Primary Purpose | Platform administration and protected admin-only auth or control surfaces |
| Core Workflow | Approved administrative management of platform-level settings and privileged control flows |
| Primary Internal Users | `platform_owner` and `super_admin` only |
| External Users | None |
| External Access Type | None |
| Data Access Scope | Admin-only platform control and administration surfaces |
| Create/Edit/Delete Rights | Explicit admin users only |
| View-Only Rights | No general internal read-only access by default |
| Explicit No-Access Parties | Clients, contractors, vendors, investors, attorneys by default, appraisers, insurance contacts, inspectors, title companies, closing attorneys, external agents, external brokers, general internal operators without admin entitlement |
| Auth/RLS Notes | `altus_core_admin.access`; explicit admin only; internal email/domain is never sufficient; privileged actions must remain auditable |
| Open Questions | Which exact admin screens and APIs belong here versus a separate internal operations surface |

## Candidate Modules Held As Open Questions

These candidates are intentionally NOT modeled as approved app-access classes yet because the current repo context does not define them as separate approved apps or modules:

- Asset Servicing or Property Operations: workflow area may exist, but no separate approved app/module definition is documented in the current auth planning set
- Investor-facing access outside Investor Hub or scoped Deal Room: keep tied to documented reporting or deal workflows only
- Legal operations surface: may require a case, property, or matter-scoped module, but no separate approved app is documented yet
