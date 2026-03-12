-- Non-destructive staging smoke check for the DB autonomy apply path.
select current_database() as current_database;
select current_schema() as current_schema;
select to_regclass('supabase_migrations.schema_migrations') as schema_migrations_table;
select now() as checked_at_utc;
