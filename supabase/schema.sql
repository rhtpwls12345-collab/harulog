-- 하루로그 서버 백업 테이블 (Supabase → SQL Editor 에 붙여 넣고 Run)
-- 규칙: 로그인한 사용자는 '자기 백업'만 보고, 올리고, 지울 수 있다 (행 단위 보안 RLS).

create table if not exists public.backups (
  id          bigint generated always as identity primary key,
  user_id     uuid not null default auth.uid() references auth.users(id) on delete cascade,
  created_at  timestamptz not null default now(),
  days        integer not null default 0 check (days >= 0 and days <= 100000),
  acts        integer not null default 0 check (acts >= 0 and acts <= 1000000),
  size        integer not null default 0 check (size >= 0 and size <= 5242880),
  data        jsonb not null check (octet_length(data::text) <= 5242880)
);
create index if not exists backups_user_created on public.backups (user_id, created_at desc);

alter table public.backups enable row level security;
alter table public.backups force row level security;

drop policy if exists "own backups: read"   on public.backups;
drop policy if exists "own backups: insert" on public.backups;
drop policy if exists "own backups: delete" on public.backups;
create policy "own backups: read"   on public.backups for select to authenticated using (user_id = auth.uid());
create policy "own backups: insert" on public.backups for insert to authenticated with check (user_id = auth.uid());
create policy "own backups: delete" on public.backups for delete to authenticated using (user_id = auth.uid());
-- 수정(update) 규칙은 일부러 만들지 않음: 백업은 새로 올리기만 한다.

revoke all on public.backups from anon;
revoke all on public.backups from authenticated;
grant select, insert, delete on public.backups to authenticated;

-- 사용자마다 최근 10개만 남기기 (서버가 직접 정리 → 앱을 조작해도 무한히 쌓을 수 없음)
create or replace function public.trim_backups() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  delete from public.backups
  where user_id = new.user_id
    and id not in (select id from public.backups where user_id = new.user_id order by created_at desc, id desc limit 10);
  return null;
end $$;
drop trigger if exists backups_trim on public.backups;
create trigger backups_trim after insert on public.backups for each row execute function public.trim_backups();
