\pset pager off
\pset footer on

begin;

create temp table expected_tables (
  table_name text primary key
) on commit drop;

insert into expected_tables (table_name) values
  ('organizations'),
  ('profiles'),
  ('organization_members'),
  ('assets'),
  ('asset_data_raw'),
  ('asset_specs_reconciled');

create temp table expected_functions (
  routine_name text primary key
) on commit drop;

insert into expected_functions (routine_name) values
  ('_touch_updated_at'),
  ('altus_current_org_id'),
  ('altus_is_org_member'),
  ('altus_login'),
  ('altus_me'),
  ('altus_logout');

create temp table expected_policies (
  schemaname text not null,
  tablename text not null,
  policyname text not null,
  primary key (schemaname, tablename, policyname)
) on commit drop;

insert into expected_policies (schemaname, tablename, policyname) values
  ('public', 'organizations', 'org_select'),
  ('public', 'profiles', 'profiles_select_self'),
  ('public', 'profiles', 'profiles_update_self'),
  ('public', 'organization_members', 'org_members_select'),
  ('public', 'assets', 'assets_select'),
  ('public', 'assets', 'assets_insert'),
  ('public', 'assets', 'assets_update'),
  ('public', 'assets', 'assets_delete'),
  ('public', 'asset_data_raw', 'adr_select'),
  ('public', 'asset_data_raw', 'adr_insert'),
  ('public', 'asset_data_raw', 'adr_update'),
  ('public', 'asset_data_raw', 'adr_delete'),
  ('public', 'asset_specs_reconciled', 'asr_select'),
  ('public', 'asset_specs_reconciled', 'asr_insert'),
  ('public', 'asset_specs_reconciled', 'asr_update'),
  ('public', 'asset_specs_reconciled', 'asr_delete'),
  ('public', 'assets', 'assets_org_isolation');

create temp table expected_columns (
  table_name text not null,
  column_name text not null,
  evidence_source text not null,
  primary key (table_name, column_name, evidence_source)
) on commit drop;

insert into expected_columns (table_name, column_name, evidence_source) values
  ('assets', 'id', 'migration-0001'),
  ('assets', 'organization_id', 'migration-0001'),
  ('assets', 'address_canonical', 'migration-0001'),
  ('assets', 'apn', 'migration-0001'),
  ('assets', 'clip', 'migration-0001'),
  ('assets', 'created_at', 'migration-0001'),
  ('assets', 'updated_at', 'migration-0001'),
  ('asset_data_raw', 'id', 'migration-0001'),
  ('asset_data_raw', 'asset_id', 'migration-0001'),
  ('asset_data_raw', 'source', 'migration-0001'),
  ('asset_data_raw', 'payload_jsonb', 'migration-0001'),
  ('asset_data_raw', 'fetched_at', 'migration-0001'),
  ('asset_specs_reconciled', 'asset_id', 'migration-0001'),
  ('asset_specs_reconciled', 'beds', 'migration-0001'),
  ('asset_specs_reconciled', 'baths', 'migration-0001'),
  ('asset_specs_reconciled', 'sqft', 'migration-0001'),
  ('asset_specs_reconciled', 'year_built', 'migration-0001'),
  ('asset_specs_reconciled', 'property_type', 'migration-0001'),
  ('asset_specs_reconciled', 'units_count', 'migration-0001'),
  ('asset_specs_reconciled', 'updated_at', 'migration-0001'),
  ('asset_specs_reconciled', 'updated_by_user_id', 'migration-0001'),
  ('organizations', 'id', 'migration-0002'),
  ('organizations', 'name', 'migration-0002'),
  ('organizations', 'created_at', 'migration-0002'),
  ('profiles', 'user_id', 'migration-0002'),
  ('profiles', 'organization_id', 'migration-0002'),
  ('profiles', 'display_name', 'migration-0002'),
  ('profiles', 'created_at', 'migration-0002'),
  ('profiles', 'updated_at', 'migration-0002'),
  ('organization_members', 'organization_id', 'migration-0002'),
  ('organization_members', 'user_id', 'migration-0002'),
  ('organization_members', 'role', 'migration-0002'),
  ('organization_members', 'created_at', 'migration-0002'),
  ('assets', 'id', 'migration-0002'),
  ('assets', 'organization_id', 'migration-0002'),
  ('assets', 'asset_type', 'migration-0002'),
  ('assets', 'name', 'migration-0002'),
  ('assets', 'status', 'migration-0002'),
  ('assets', 'created_at', 'migration-0002'),
  ('assets', 'updated_at', 'migration-0002'),
  ('asset_data_raw', 'id', 'migration-0002'),
  ('asset_data_raw', 'organization_id', 'migration-0002'),
  ('asset_data_raw', 'asset_id', 'migration-0002'),
  ('asset_data_raw', 'source', 'migration-0002'),
  ('asset_data_raw', 'payload', 'migration-0002'),
  ('asset_data_raw', 'created_at', 'migration-0002'),
  ('asset_specs_reconciled', 'asset_id', 'migration-0002'),
  ('asset_specs_reconciled', 'organization_id', 'migration-0002'),
  ('asset_specs_reconciled', 'specs', 'migration-0002'),
  ('asset_specs_reconciled', 'updated_at', 'migration-0002'),
  ('asset_data_raw', 'payload_sha256', 'runtime-function-app'),
  ('asset_data_raw', 'source_record_id', 'runtime-function-app'),
  ('assets', 'display_name', 'runtime-function-app'),
  ('assets', 'external_ids', 'runtime-function-app');

\echo '=== PROVEN_TABLES ==='
select
  e.table_name,
  case when c.table_name is not null then 'present' else 'missing' end as live_status
from expected_tables e
left join information_schema.tables c
  on c.table_schema = 'public'
 and c.table_name = e.table_name
order by e.table_name;

\echo '=== PROVEN_FUNCTIONS_RPCS ==='
select
  e.routine_name,
  case when r.routine_name is not null then 'present' else 'missing' end as live_status
from expected_functions e
left join information_schema.routines r
  on r.routine_schema = 'public'
 and r.routine_name = e.routine_name
order by e.routine_name;

\echo '=== PROVEN_POLICY_OBJECTS ==='
select
  e.schemaname,
  e.tablename,
  e.policyname,
  case when p.policyname is not null then 'present' else 'missing' end as live_status
from expected_policies e
left join pg_policies p
  on p.schemaname = e.schemaname
 and p.tablename = e.tablename
 and p.policyname = e.policyname
order by e.tablename, e.policyname;

\echo '=== CONFIRMED_MISSING_OBJECTS ==='
with missing_tables as (
  select 'table' as object_type, e.table_name as object_name
  from expected_tables e
  left join information_schema.tables c
    on c.table_schema = 'public'
   and c.table_name = e.table_name
  where c.table_name is null
), missing_functions as (
  select 'function' as object_type, e.routine_name as object_name
  from expected_functions e
  left join information_schema.routines r
    on r.routine_schema = 'public'
   and r.routine_name = e.routine_name
  where r.routine_name is null
), missing_policies as (
  select 'policy' as object_type, e.tablename || '.' || e.policyname as object_name
  from expected_policies e
  left join pg_policies p
    on p.schemaname = e.schemaname
   and p.tablename = e.tablename
   and p.policyname = e.policyname
  where p.policyname is null
)
select * from missing_tables
union all
select * from missing_functions
union all
select * from missing_policies
order by object_type, object_name;

\echo '=== COLUMN_MISMATCHES_REPO_VS_STAGING ==='
with live_columns as (
  select table_name, column_name
  from information_schema.columns
  where table_schema = 'public'
), expected_union as (
  select table_name, column_name,
         string_agg(evidence_source, ', ' order by evidence_source) as repo_evidence
  from expected_columns
  group by table_name, column_name
)
select
  e.table_name,
  e.column_name,
  e.repo_evidence,
  case when l.column_name is not null then 'present' else 'missing' end as live_status
from expected_union e
left join live_columns l
  on l.table_name = e.table_name
 and l.column_name = e.column_name
where l.column_name is null
order by e.table_name, e.column_name;

\echo '=== LIVE_EXTRA_COLUMNS_NOT_PROVEN_IN_REPO_INVENTORY ==='
with expected_union as (
  select distinct table_name, column_name
  from expected_columns
)
select
  c.table_name,
  c.column_name
from information_schema.columns c
left join expected_union e
  on e.table_name = c.table_name
 and e.column_name = c.column_name
where c.table_schema = 'public'
  and c.table_name in (select table_name from expected_tables)
  and e.column_name is null
order by c.table_name, c.column_name;

rollback;
