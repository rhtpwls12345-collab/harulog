// 그리기 성능: 휴대폰 수준(CPU 4배 느리게)에서 오늘 화면·전체 지도·마을 미리보기의 초당 프레임
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 412, height: 900 }, deviceScaleFactor: 2.6 });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('https://fonts.googleapis.com/**', r => r.abort());
  await p.goto('file://' + path.resolve(__dirname, process.env.F || '../www/index.html')); await p.waitForTimeout(800);
  const cdp = await p.context().newCDPSession(p); await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  const fps = () => p.evaluate(() => new Promise(r => { let n = 0; const t0 = performance.now(); const f = () => { n++; performance.now() - t0 < 3000 ? requestAnimationFrame(f) : r(+(n/3).toFixed(1)); }; requestAnimationFrame(f); }));
  const out = {};
  out.today = await fps();
  await p.click('#btnMap'); await p.waitForTimeout(500); out.map = await fps(); await p.click('#btnMap');
  await p.click('#tab-world'); await p.waitForTimeout(800); out.editor = await fps();
  console.log(JSON.stringify(out), errs); await b.close();
})();
