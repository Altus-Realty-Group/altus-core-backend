alter table public.assets enable row level security;
alter table public.asset_data_raw enable row level security;
alter table public.asset_specs_reconciled enable row level security;

create policy "assets_org_isolation"
on public.assets
for all
using (organization_id = current_setting('request.jwt.claim.organization_id', true)::uuid);
