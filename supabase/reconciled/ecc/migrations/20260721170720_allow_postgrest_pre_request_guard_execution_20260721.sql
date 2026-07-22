grant usage on schema private to anon, authenticated, service_role, authenticator;
grant execute on function private.block_unowned_legacy_table_api()
  to anon, authenticated, service_role, authenticator;
notify pgrst, 'reload config';
