# App Access Matrix

Status: Draft / Pending Live Core DB Verification
Owner: Altus Core Backend
Applies to: ECC, Price Engine, Field App, Construction Manager, Investor Hub, Deal Room, Altus Core Admin, Future Apps
Canonical Repo: Altus-Realty-Group/altus-core-backend
Database Authority: Altus Core Supabase project srzwamukysmhiaaviwiv
Mutation Status: Documentation only; no DB writes

## Summary

This matrix defines default access posture. It does not replace action permissions, scoped grants, assignments, backend hard denials, or RLS.

Legend:

- `default` means allowed by approved internal policy
- `explicit` means allowed only by explicit entitlement
- `scoped` means explicit entitlement plus scope grant or assignment
- `deny` means blocked by default

| App | Altus Internal | Client | Contractor | Vendor | Investor | Lender | Agent | Owner | Tenant | Guest | Service Account |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ECC | default | deny | deny | deny | deny | deny | deny | deny | deny | deny | explicit |
| Price Engine | explicit | deny | deny | deny | deny | deny | deny | deny | deny | deny | explicit |
| Field App | explicit | explicit if portal approved | scoped | scoped | deny | deny | deny | explicit if approved | explicit if approved | deny | explicit |
| Construction Manager | explicit | explicit if approved | scoped | scoped | deny | deny | deny | explicit if approved | deny | deny | explicit |
| Investor Hub | explicit if needed | explicit if portal approved | deny | deny | scoped | scoped | scoped | explicit if approved | deny | invite-only scoped | explicit |
| Deal Room | explicit if needed | scoped | deny by default | deny by default | scoped | scoped | scoped | scoped | deny | invite-only scoped | explicit |
| Altus Core Admin | explicit admin only | deny | deny | deny | deny | deny | deny | deny | deny | deny | explicit |
| Future Apps | deny by default until registered | deny | deny | deny | deny | deny | deny | deny | deny | deny | explicit if approved |

## Default App Policy

- ECC: internal only
- Price Engine: internal only
- Field App: internal plus scoped contractors, vendors, and field users
- Construction Manager: internal plus scoped contractors, vendors, estimators, and approved external project users
- Investor Hub: investor-scoped
- Deal Room: deal or invite scoped
- Altus Core Admin: internal platform-owner or super-admin only
- Future apps: DENIED BY DEFAULT until app entitlement exists

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
