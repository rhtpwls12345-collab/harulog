-- harulog: server backup table (Supabase > SQL Editor > New query > paste all > Run)
-- Rule: a signed-in user can only read/insert/delete their own backups (RLS).

create table if not exists public.backups (id bigint generated always as identity primary key, user_id uuid not null default auth.uid() references auth.users(id) on delete cascade, created_at timestamptz not null default now(), days integer not null default 0, acts integer not null default 0, size integer not null default 0, data jsonb not null);

alter table public.backups add constraint backups_limits check (days between 0 and 100000 and acts between 0 and 1000000 and size between 0 and 5242880 and octet_length(data::text) <= 5242880);

create index if not exists backups_user_created on public.backups (user_id, created_at desc);

alter table public.backups enable row level security;
alter table public.backups force row level security;

drop policy if exists "own backups read" on public.backups;
drop policy if exists "own backups insert" on public.backups;
drop policy if exists "own backups delete" on public.backups;
create policy "own backups read" on public.backups for select to authenticated using (user_id = auth.uid());
create policy "own backups insert" on public.backups for insert to authenticated with check (user_id = auth.uid());
create policy "own backups delete" on public.backups for delete to authenticated using (user_id = auth.uid());

revoke all on public.backups from anon;
revoke all on public.backups from authenticated;
grant select, insert, delete on public.backups to authenticated;

-- keep only the latest 10 backups per user
create or replace function public.trim_backups() returns trigger language plpgsql security definer set search_path = public as $$ begin delete from public.backups where user_id = new.user_id and id not in (select id from public.backups where user_id = new.user_id order by created_at desc, id desc limit 10); return null; end $$;

drop trigger if exists backups_trim on public.backups;
create trigger backups_trim after insert on public.backups for each row execute function public.trim_backups();
