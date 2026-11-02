// 동작별 소품 그림 확인: 근력·달리기·수영·요가·사이클·복싱·회의 (스크린샷 test/mo-*.png)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 1200 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('https://fonts.googleapis.com/**', r => r.abort());
  await p.goto('file://' + path.resolve(__dirname, '../www/index.html')); await p.waitForTimeout(700);
  const L = [['exercise', '하체 운동', '스쿼트', 'strength'], ['exercise', '러닝', '5km 달렸다', 'run'], ['exercise', '수영', '자유형 연습', 'swim'], ['exercise', '요가', '', 'yoga'],
    ['exercise', '스피닝', '', 'bike'], ['exercise', '복싱', '샌드백 쳤다', 'boxing'], ['work', '주간 회의', '발표 준비', 'meeting']];
  for (const [type, title, raw] of L){ await p.click('#btnAdd'); await p.click('#ft-' + type, { force: true }); await p.fill('#fTitle', title); await p.fill('#fRaw', raw); await p.click('#actForm button[type=submit]'); await p.waitForTimeout(150); }
  for (let i = 0; i < L.length; i++){
    await p.click(`#actList .act >> nth=${i}`); await p.waitForTimeout(5200);
    const st = await p.evaluate(() => { const a = window.Haru._world.actor; return {pose:a.spot?.pose, motion:a.spot?.motion, item:a.spot?.item || null, arrived:a.arrived}; });
    console.log(L[i][3], JSON.stringify(st));
    await (await p.$('.stage-view')).screenshot({ path: path.resolve(__dirname, `mo-${L[i][3]}.png`) });
  }
  console.log('ERR', errs); await b.close();
})();
