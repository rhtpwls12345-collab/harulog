// 계정·서버 백업: 가짜 Supabase 서버로 회원가입 → 로그인 → 백업 → 기록 삭제 → 복구, RLS 흉내(내 것만), 토큰 갱신
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const src = fs.readFileSync(path.resolve(__dirname, '../www/index.html'), 'utf8')
    .replace("supabaseUrl: ''", "supabaseUrl: 'https://test.supabase.co'").replace("supabaseAnonKey: ''", "supabaseAnonKey: 'anon-test'");
  const tmp = path.resolve(__dirname, '../www/_acct-test.html'); fs.writeFileSync(tmp, src);
  const users = {}, rows = []; let nid = 1, tok = 0; const tokens = {};
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 1100 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('https://fonts.googleapis.com/**', r => r.abort());
  await p.route('https://test.supabase.co/**', async r => {
    const req = r.request(), u = new URL(req.url()), body = req.postData() ? JSON.parse(req.postData()) : null, H = req.headers();
    const j = (status, obj) => r.fulfill({ status, contentType: 'application/json', body: obj === undefined ? '' : JSON.stringify(obj) });
    if (H.apikey !== 'anon-test') return j(401, { message: 'no apikey' });
    const sess = email => { const a = 'at' + (++tok), rf = 'rt' + tok; tokens[a] = email; tokens[rf] = email; return { access_token: a, refresh_token: rf, expires_in: 3600, expires_at: Math.floor(Date.now() / 1000) + 3600, user: { email } }; };
    if (u.pathname === '/auth/v1/signup'){ if (users[body.email]) return j(400, { msg: 'User already registered' }); users[body.email] = body.password; return j(200, sess(body.email)); }
    if (u.pathname === '/auth/v1/token'){
      if (u.searchParams.get('grant_type') === 'password') return users[body.email] === body.password ? j(200, sess(body.email)) : j(400, { error_description: 'Invalid login credentials' });
      return tokens[body.refresh_token] ? j(200, sess(tokens[body.refresh_token])) : j(400, { error_description: 'bad refresh' });
    }
    if (u.pathname === '/auth/v1/logout') return j(204);
    const me = tokens[(H.authorization || '').replace('Bearer ', '')]; if (!me) return j(401, { message: 'JWT expired' });
    if (u.pathname === '/rest/v1/backups'){
      const mine = rows.filter(x => x.user === me);   // RLS 흉내
      if (req.method() === 'POST'){ rows.push(Object.assign({ id: nid++, user: me, created_at: new Date(Date.now() + nid * 1000).toISOString() }, body)); return j(201); }
      if (req.method() === 'DELETE'){ const ids = (u.searchParams.get('id') || '').replace(/^in\.\(|\)$/g, '').split(',').map(Number); for (const id of ids){ const i = rows.findIndex(x => x.id === id && x.user === me); if (i >= 0) rows.splice(i, 1); } return j(204); }
      const idq = u.searchParams.get('id'); let list = mine.slice().sort((a, b) => b.created_at.localeCompare(a.created_at));
      if (idq) list = list.filter(x => x.id === Number(idq.replace('eq.', '')));
      const sel = (u.searchParams.get('select') || '').split(',');
      return j(200, list.map(x => Object.fromEntries(sel.map(k => [k, x[k]]))));
    }
    return j(404, { message: 'nf' });
  });
  await p.goto('file://' + tmp); await p.waitForTimeout(700);
  // 기록 2개
  for (const t of ['아침 산책', '점심']){ await p.click('#btnAdd'); await p.click('#ft-walk', { force: true }); await p.fill('#fTitle', t); await p.click('#actForm button[type=submit]'); await p.waitForTimeout(100); }
  await p.click('#tab-settings'); await p.waitForTimeout(200);
  console.log('logged-out card:', (await p.textContent('#acctBody')).slice(0, 40));
  await p.click('#acctBody button:has-text("회원가입")'); await p.fill('#loginEmail', 'me@test.com'); await p.fill('#loginPw', 'password1'); await p.fill('#loginPw2', 'password2'); await p.click('#loginGo');
  console.log('pw mismatch:', await p.textContent('#loginErr'));
  await p.fill('#loginPw2', 'password1'); await p.click('#loginGo'); await p.waitForTimeout(400);
  console.log('dialog closed:', !(await p.evaluate(() => document.getElementById('loginDlg').open)), 'stored pw?', (await p.evaluate(() => localStorage.getItem('harulog.auth'))).includes('password1'));
  await p.click('#acctBody button:has-text("지금 서버에 백업")'); await p.waitForTimeout(500);
  console.log('after backup:', (await p.textContent('#acctBody')).replace(/\s+/g, ' ').slice(0, 160));
  // 다른 사용자 데이터 끼워 넣기 → 안 보여야 함
  rows.push({ id: 999, user: 'other@x.com', created_at: new Date(Date.now() + 1e9).toISOString(), days: 9, acts: 99, size: 10, data: {} });
  // 기록 전체 삭제 → 서버에서 복구
  await p.evaluate(() => { window.confirm = () => true; });
  await p.click('#btnWipe'); await p.click('#askYes'); await p.waitForTimeout(200);
  console.log('acts after wipe:', await p.evaluate(() => Object.values(window.Haru.data.days).reduce((s, d) => s + d.activities.length, 0)));
  await p.click('#acctBody button:has-text("로그아웃")'); await p.click('#askYes'); await p.waitForTimeout(300);
  await p.click('#acctBody button:has-text("로그인")'); await p.fill('#loginEmail', 'me@test.com'); await p.fill('#loginPw', 'wrongpass'); await p.click('#loginGo'); await p.waitForTimeout(300);
  console.log('wrong pw:', await p.textContent('#loginErr'));
  await p.fill('#loginPw', 'password1'); await p.click('#loginGo'); await p.waitForTimeout(600);
  console.log('list:', (await p.textContent('#acctBody')).replace(/\s+/g, ' ').slice(0, 200), '| sees other user?', (await p.textContent('#acctBody')).includes('활동 99개'));
  // 토큰 만료 흉내 → 자동 갱신
  await p.evaluate(() => { const a = JSON.parse(localStorage.getItem('harulog.auth')); a.access_token = 'expired'; localStorage.setItem('harulog.auth', JSON.stringify(a)); });
  await p.reload(); await p.waitForTimeout(600); await p.click('#tab-settings'); await p.waitForTimeout(600);
  await p.click('#acctBody button:has-text("복구") >> nth=0'); await p.click('#askYes'); await p.waitForTimeout(600);
  console.log('acts after restore:', await p.evaluate(() => Object.values(window.Haru.data.days).reduce((s, d) => s + d.activities.length, 0)));
  await (await p.$('#acctCard')).screenshot({ path: path.resolve(__dirname, 'acct.png') });
  await p.click('#acctBody button:has-text("로그아웃")'); await p.click('#askYes'); await p.click('#acctBody button:has-text("로그인")'); await p.waitForTimeout(200);
  await (await p.$('#loginDlg')).screenshot({ path: path.resolve(__dirname, 'acct-login.png') });
  console.log('ERR', errs); await b.close(); fs.unlinkSync(tmp);
})();
