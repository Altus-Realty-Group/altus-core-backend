-- Block direct Data API access to legacy tables owned by Supabase's reserved
-- read-only role; their ownership prevents postgres from enabling RLS directly.
create schema if not exists private;

create or replace function private.block_unowned_legacy_table_api()
returns void
language plpgsql
security invoker
set search_path = ''
as $$
declare
  request_path text := trim(both '/' from split_part(coalesce(current_setting('request.path', true), ''), '?', 1));
begin
  if request_path in ('dl_aging_export_2025_11_08', 'dl_payment_status_audit') then
    raise insufficient_privilege using
      message = 'Direct Data API access to this legacy table is disabled.';
  end if;
end;
$$;

revoke all on function private.block_unowned_legacy_table_api() from public, anon, authenticated, service_role;
grant usage on schema private to authenticator;
grant execute on function private.block_unowned_legacy_table_api() to authenticator;
alter role authenticator set pgrst.db_pre_request = 'private.block_unowned_legacy_table_api';

-- Harden every public table owned by the project owner.
do $$
declare
  t record;
begin
  for t in
    select n.nspname as schema_name, c.relname as table_name, c.relrowsecurity
    from pg_class c
    join pg_namespace n on n.oid = c.relnamespace
    join pg_roles owner_role on owner_role.oid = c.relowner
    where n.nspname = 'public'
      and c.relkind in ('r', 'p')
      and owner_role.rolname = current_user
  loop
    if not t.relrowsecurity then
      execute format('alter table %I.%I enable row level security', t.schema_name, t.table_name);
    end if;
    execute format('revoke all privileges on table %I.%I from public', t.schema_name, t.table_name);
    execute format(
      'revoke truncate, references, trigger on table %I.%I from anon, authenticated',
      t.schema_name,
      t.table_name
    );
  end loop;
end
$$;

alter default privileges for role postgres in schema public
  revoke all privileges on tables from anon, authenticated;
alter default privileges for role postgres in schema public
  revoke all privileges on tables from public;

notify pgrst, 'reload config';
