// pc-test.html: 처음(권한 없음) → 설정에서 연결 → 초안 카드에 제안이 뜨는지
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 860 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('https://fonts.googleapis.com/**', r => r.abort());
  await p.route('https://api.open-meteo.com/**', r => r.abort()); // 오프라인 대체 확인
  await p.goto('file://' + path.resolve(__dirname, '../pc-test.html')); await p.waitForTimeout(1200);
  const txt = async () => (await p.innerText('#draftCard')).replace(/\s+/g, ' ');
  console.log('START', await txt());
  await p.click('#draftCard button:has-text("연결 설정")'); await p.waitForTimeout(600);
  await p.click('#nativeCard button:has-text("위치 허용")'); await p.waitForTimeout(500);
  await p.click('#nativeCard button:has-text("연결하기")'); await p.waitForTimeout(500);
  await p.click('#nativeCard button:has-text("사용 정보 접근 허용")'); await p.waitForTimeout(1200);
  console.log('CARD', (await p.innerText('#nativeCard')).replace(/\n+/g, ' | ').slice(0, 400));
  await p.click('#tab-today'); await p.waitForTimeout(1200);
  console.log('TODAY', await p.$$eval('#draftCard li.draft', l => l.map(x => x.innerText.replace(/\s+/g, ' '))));
  await p.screenshot({ path: path.resolve(__dirname, 'pc1.png') });
  await p.click('#btnPrevDay'); await p.waitForTimeout(1000);
  console.log('YDAY', await p.$$eval('#draftCard li.draft', l => l.map(x => x.innerText.replace(/\s+/g, ' ').slice(0, 60))));
  await p.click('.pcmock>button'); await p.selectOption('#pmScn', 'phone'); await p.waitForTimeout(1200);
  console.log('PHONE', await p.$$eval('#draftCard li.draft', l => l.map(x => x.innerText.replace(/\s+/g, ' ').slice(0, 70))));
  await p.screenshot({ path: path.resolve(__dirname, 'pc2.png') });
  console.log('ERR', errs); await b.close();
})();
