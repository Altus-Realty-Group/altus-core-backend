-- Post-apply verification for issue #94.
-- This script is non-destructive. set_config(..., true) is transaction-local.

do $verify$
declare
  fn record;
  role_settings text[];
  legacy_name text;
  blocked boolean;
begin
  if not exists (
    select 1
    from supabase_migrations.schema_migrations
    where version = '20260721170328'
      and name = 'harden_owned_tables_and_block_legacy_api_20260721'
  ) then
    raise exception 'missing migration 20260721170328';
  end if;

  if not exists (
    select 1
    from supabase_migrations.schema_migrations
    where version = '20260721170720'
      and name = 'allow_postgrest_pre_request_guard_execution_20260721'
  ) then
    raise exception 'missing migration 20260721170720';
  end if;

  select p.prosecdef,
         p.proconfig,
         pg_get_functiondef(p.oid) as definition
    into fn
  from pg_proc p
  join pg_namespace n on n.oid = p.pronamespace
  where n.nspname = 'private'
    and p.proname = 'block_unowned_legacy_table_api'
    and pg_get_function_identity_arguments(p.oid) = '';

  if not found then
    raise exception 'missing private.block_unowned_legacy_table_api()';
  end if;

  if fn.prosecdef then
    raise exception 'pre-request guard must remain security invoker';
  end if;

  if not (
    coalesce(fn.proconfig, array[]::text[])
    @> array['search_path=""']::text[]
  ) then
    raise exception 'pre-request guard must pin an empty search_path';
  end if;

  foreach legacy_name in array array[
    'dl_aging_export_2025_11_08',
    'dl_payment_status_audit'
  ]
  loop
    if position(legacy_name in fn.definition) = 0 then
      raise exception 'pre-request guard does not cover %', legacy_name;
    end if;

    if to_regclass(format('public.%I', legacy_name)) is null then
      raise exception 'expected legacy table public.% is absent', legacy_name;
    end if;

    perform set_config('request.path', '/' || legacy_name, true);
    blocked := false;
    begin
      perform private.block_unowned_legacy_table_api();
    exception
      when insufficient_privilege then
        blocked := true;
    end;

    if not blocked then
      raise exception 'pre-request guard did not block %', legacy_name;
    end if;
  end loop;

  perform set_config('request.path', '/health', true);
  perform private.block_unowned_legacy_table_api();

  select r.rolconfig
    into role_settings
  from pg_roles r
  where r.rolname = 'authenticator';

  if not (
    coalesce(role_settings, array[]::text[])
    @> array['pgrst.db_pre_request=private.block_unowned_legacy_table_api']::text[]
  ) then
    raise exception 'authenticator pre-request setting is absent';
  end if;

  if exists (
    select 1
    from unnest(array['anon','authenticated','service_role','authenticator']) as required_role(role_name)
    where not has_schema_privilege(
      required_role.role_name,
      'private',
      'USAGE'
    )
       or not has_function_privilege(
      required_role.role_name,
      'private.block_unowned_legacy_table_api()',
      'EXECUTE'
    )
  ) then
    raise exception 'required PostgREST guard privileges are incomplete';
  end if;

  if exists (
    select 1
    from pg_class c
    join pg_namespace n on n.oid = c.relnamespace
    join pg_roles owner_role on owner_role.oid = c.relowner
    where n.nspname = 'public'
      and c.relkind in ('r', 'p')
      and owner_role.rolname = current_user
      and not c.relrowsecurity
  ) then
    raise exception 'a project-owner-owned public table is missing RLS';
  end if;

  if exists (
    select 1
    from pg_class c
    join pg_namespace n on n.oid = c.relnamespace
    cross join lateral aclexplode(
      coalesce(c.relacl, acldefault('r', c.relowner))
    ) acl
    left join pg_roles grantee_role on grantee_role.oid = acl.grantee
    where n.nspname = 'public'
      and c.relkind in ('r', 'p')
      and (
        acl.grantee = 0
        or (
          grantee_role.rolname in ('anon', 'authenticated')
          and acl.privilege_type in ('TRUNCATE', 'REFERENCES', 'TRIGGER')
        )
      )
  ) then
    raise exception 'prohibited public-table privileges remain';
  end if;

  if exists (
    select 1
    from pg_default_acl d
    join pg_roles owner_role on owner_role.oid = d.defaclrole
    join pg_namespace n on n.oid = d.defaclnamespace
    cross join lateral aclexplode(d.defaclacl) acl
    left join pg_roles grantee_role on grantee_role.oid = acl.grantee
    where owner_role.rolname = 'postgres'
      and n.nspname = 'public'
      and d.defaclobjtype = 'r'
      and (
        acl.grantee = 0
        or grantee_role.rolname in ('anon', 'authenticated')
      )
  ) then
    raise exception 'prohibited default table privileges remain';
  end if;
end
$verify$;

select
  version,
  name
from supabase_migrations.schema_migrations
where version in ('20260721170328', '20260721170720')
order by version;

select
  c.relname as legacy_table,
  c.relrowsecurity as rls_enabled,
  c.relforcerowsecurity as rls_forced
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
  and c.relname in (
    'dl_aging_export_2025_11_08',
    'dl_payment_status_audit'
  )
order by c.relname;
