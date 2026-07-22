# Reconciled ECC migration history

This directory preserves exact historical SQL recovered from the canonical ECC Supabase migration history.

## Deployment boundary

- Files here are evidence, not active Altus Core staging migrations.
- Automatic Supabase workflows consume `supabase/migrations/`; they do not consume this directory.
- Do not move a file from this directory into an active migration path without direct proof that the configured target has the same database lineage and affected objects.
- Run the paired verification only against the canonical ECC database or a separately authorized ECC-lineage clone.
- A future ECC deployment lane requires its own governed target identity, issue, proof, and authorization.
