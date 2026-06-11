# Altus Core Backend Repo Identity

`altus-core-backend` is the backend/runtime repository for Altus Core backend services and related runtime evidence.

It is responsible for:

- backend runtime code
- Azure Function surfaces
- backend API behavior
- runtime auth/session behavior where implemented
- backend tests
- backend deployment/runtime proof
- backend-side auth evidence and consumer maps

It is not responsible for:

- general operations planning docs
- broad roadmap docs unrelated to backend runtime
- frontend-only application ownership unless colocated for a specific runtime reason
- governance docs that belong in the ops/control-plane repo

Documentation cleanup does not authorize runtime behavior changes.

No SQL, RLS, grants, migrations, schema changes, auth implementation changes, or legacy object cleanup may occur from this README pass.

This repository is distinct from `Altus-Realty-Group/altus-core-ops`.
