// 하루로그 서버 설정 (Supabase)
// Supabase 대시보드 → Project Settings → API 에서 두 값을 복사해 넣으세요.
//  - supabaseUrl: "https://xxxx.supabase.co"
//  - supabaseAnonKey: "anon public" 또는 "Publishable key"(sb_publishable_…) (공개용 키라 앱에 들어가도 괜찮아요. 데이터는 RLS 규칙으로 보호돼요)
// ⚠ "service_role" 키나 "Secret key"(sb_secret_…)는 절대 넣지 마세요. 그 키는 모든 데이터를 열 수 있어요.
window.HARU_CONFIG = {
  supabaseUrl: '',
  supabaseAnonKey: '',
};
