-- Optional: run once in the instructor-owned Supabase project's SQL Editor.
-- Public visitors can submit rows without signing in. Never use service_role in the browser.
create table if not exists public.week1_quiz_responses (
  id uuid primary key default gen_random_uuid(),
  submitted_at timestamptz not null default now(),
  session_code text not null check (
    char_length(session_code) between 1 and 40 and session_code ~ '^[A-Za-z0-9 _.-]+$'
  ),
  topic_slug text not null check (topic_slug in (
    'ch01_intro_to_ml', 'ch02_ml_lifecycle', 'topic03_supervised_vs_unsupervised',
    'ch05_tools_and_sklearn', 'ch08_simple_linear_regression',
    'ch09_multiple_linear_regression', 'ch10_polynomial_and_regularisation',
    'ch12_logistic_regression'
  )),
  question_id text not null check (
    char_length(question_id) between 4 and 80 and question_id ~ '^[a-z0-9_]+$'
  ),
  question_type text not null check (question_type in ('multiple_choice', 'true_false', 'word_cloud')),
  answer_text text not null check (char_length(answer_text) between 1 and 500 and btrim(answer_text) <> ''),
  answer_index smallint check (answer_index is null or answer_index between 0 and 4),
  is_correct boolean,
  display_name text check (display_name is null or (
    char_length(display_name) between 1 and 32 and btrim(display_name) <> '' and display_name !~ '[[:cntrl:]]'
  )),
  check (
    (question_type = 'word_cloud' and answer_index is null and is_correct is null)
    or (question_type in ('multiple_choice', 'true_false') and answer_index is not null and is_correct is not null)
  )
);

alter table public.week1_quiz_responses enable row level security;
drop policy if exists week1_quiz_responses_anon_insert on public.week1_quiz_responses;
create policy week1_quiz_responses_anon_insert
  on public.week1_quiz_responses for insert to anon with check (true);

revoke all on table public.week1_quiz_responses from public, anon, authenticated;
grant usage on schema public to anon;
grant insert on table public.week1_quiz_responses to anon;

-- Instructor-only review, run in the Supabase Dashboard SQL Editor:
-- select submitted_at, session_code, topic_slug, question_id, question_type,
--        answer_text, answer_index, is_correct, display_name
-- from public.week1_quiz_responses order by submitted_at desc;
