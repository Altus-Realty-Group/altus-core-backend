begin;

create or replace function public.altus_is_org_member(org_id uuid)
returns boolean
language sql
stable
as $function$
  select
    case
      when auth.role() = 'service_role' then true
      else exists (
        select 1
        from public.organization_members m
        where m.organization_id = org_id
          and m.user_id = auth.uid()
      )
    end;
$function$;

commit;
