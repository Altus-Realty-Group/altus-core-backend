-- ENTERPRISE ASSET MASTER V1
create table if not exists public.assets (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null,
  address_canonical text,
  apn text,
  clip text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.asset_data_raw (
  id uuid primary key default gen_random_uuid(),
  asset_id uuid not null references public.assets(id) on delete cascade,
  source text not null,
  payload_jsonb jsonb not null,
  fetched_at timestamptz not null default now()
);

create table if not exists public.asset_specs_reconciled (
  asset_id uuid primary key references public.assets(id) on delete cascade,
  beds numeric,
  baths numeric,
  sqft numeric,
  year_built integer,
  property_type text,
  units_count integer,
  updated_at timestamptz not null default now(),
  updated_by_user_id uuid
);

create index if not exists idx_assets_org on public.assets(organization_id);
create index if not exists idx_asset_raw_asset on public.asset_data_raw(asset_id);
