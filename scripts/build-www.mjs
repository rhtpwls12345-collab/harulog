// src/harulog.html(웹 버전 원본) → www/index.html(앱용 완전한 HTML 문서)
// 사용: npm run build  (그 다음 npx cap sync android)
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
// copyFileSync 는 일부 공유 폴더(Windows 마운트)에서 실패할 수 있어 읽고 쓰는 방식으로 복사한다
const copy = (from, to) => writeFileSync(to, readFileSync(from));
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const src = readFileSync(join(root, 'src/harulog.html'), 'utf8');
const cut = src.indexOf('</style>') + '</style>'.length;
if (cut < 8) throw new Error('src/harulog.html 에서 </style> 을 찾지 못했어요');
const head = src.slice(0, cut), body = src.slice(cut);

// 보안: 이 페이지가 연결할 수 있는 곳을 정해 둔다 (글꼴 · 날씨 · Supabase 서버만)
const CSP = [
  "default-src 'self'", "script-src 'self' 'unsafe-inline'", "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
  "font-src 'self' https://fonts.gstatic.com data:", "img-src 'self' data: blob:",
  "connect-src 'self' https://*.supabase.co https://api.open-meteo.com", "object-src 'none'", "base-uri 'none'", "form-action 'none'",
].join('; ');
// 서버 설정(src/config.js)을 페이지 안에 넣는다
const config = '<script>\n' + readFileSync(join(root, 'src/config.js'), 'utf8').replace(/<\/script/gi, '<\\/script') + '\n</script>';
const page = scripts => `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#F7F1E8">
<meta http-equiv="Content-Security-Policy" content="${CSP}">
<meta name="referrer" content="no-referrer">
${head}
<style>
/* 앱: 상태바·내비게이션바 영역 피하기 (Capacitor SystemBars 가 --safe-area-inset-* 를 넣어 줌) */
body{padding-top:var(--safe-area-inset-top,env(safe-area-inset-top,0px));padding-bottom:var(--safe-area-inset-bottom,env(safe-area-inset-bottom,0px))}
.native-row{display:flex;gap:10px;align-items:flex-start;justify-content:space-between;padding:10px 0;border-top:1px solid var(--line)}
.native-row:first-of-type{border-top:0}
.native-row b{display:block}
.native-row small{color:var(--muted)}
.native-state{font-size:12px;border-radius:999px;padding:2px 8px;background:var(--surface-2);white-space:nowrap}
.native-state.on{background:var(--sage-soft);color:var(--ink)}
</style>
${scripts}
</head>
<body>
${body}
</body>
</html>
`;
const html = page(config + '\n<script src="capacitor.js"></script>\n<script src="native.js"></script>');
mkdirSync(join(root, 'www'), { recursive: true });
writeFileSync(join(root, 'www/index.html'), html);
const core = join(root, 'node_modules/@capacitor/core/dist/capacitor.js');
if (existsSync(core)) copy(core, join(root, 'www/capacitor.js'));
else if (!existsSync(join(root, 'www/capacitor.js'))) console.warn('⚠ node_modules 가 없어 www/capacitor.js 를 만들지 못했어요. npm install 후 다시 실행하세요.');
copy(join(root, 'src/native.js'), join(root, 'www/native.js'));
copy(join(root, 'src/privacypolicy.html'), join(root, 'www/privacypolicy.html'));
console.log('www/index.html 생성 완료 (' + Math.round(html.length / 1024) + ' KB)');

// PC 테스트용 단일 파일: 가짜 플러그인(pc-mock.js) + 연동 레이어(native.js) 를 안에 넣는다. 앱(www)에는 포함되지 않음.
const inline = f => '<script>\n' + readFileSync(join(root, f), 'utf8').replace(/<\/script/gi, '<\\/script') + '\n</script>';
const pc = page(config + '\n' + inline('src/pc-mock.js') + '\n' + inline('src/native.js').replace("href:'privacypolicy.html'", "href:'www/privacypolicy.html'"))
  .replace('<title>하루로그</title>', '<title>하루로그 · PC 테스트</title>');
writeFileSync(join(root, 'pc-test.html'), pc);
console.log('pc-test.html 생성 완료 — 더블클릭해서 브라우저로 열면 앱 버전을 PC에서 테스트할 수 있어요');
