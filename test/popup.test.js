// 팝업 장소: 키워드 → 임시 가게, 도로 트럭(빈 땅 없음) / 빈 땅 부스, 수동 지정, 데이터 저장
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 1200 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('https://fonts.googleapis.com/**', r => r.abort());
  await p.goto('file://' + path.resolve(__dirname, '../www/index.html')); await p.waitForTimeout(700);
  const L = [['other', '병원', '치과 진료 받았다', 'clinic'], ['hobby', '영화 봤다', '팝콘 최고', 'cinema'], ['study', '도서관에서 공부', '', 'library'], ['other', '마트 장보기', '', 'market'],
    ['other', '미용실', '머리 잘랐다', 'salon'], ['other', '은행 업무', '', 'office'], ['meet', '친구랑 노래방', '', 'stage'], ['meal', '점심', '', null]];
  for (const [type, title, raw] of L){ await p.click('#btnAdd'); await p.click('#ft-' + type, { force: true }); await p.fill('#fTitle', title); await p.fill('#fRaw', raw); await p.waitForTimeout(80);
    if (title === '병원') console.log('form auto', await p.$eval('#fPop .chip.auto', e => e.textContent), 'hidden', await p.$eval('#fPopWrap', e => e.hidden));
    await p.click('#actForm button[type=submit]'); await p.waitForTimeout(150); }
  const run = async (tag) => {
    for (let i = 0; i < L.length; i++){
      await p.click(`#actList .act >> nth=${i}`); await p.waitForTimeout(i === 0 ? 5500 : 4500);
      const st = await p.evaluate(() => { const a = window.Haru._world.actor; return {pop:a.spot?.pop || null, arrived:a.arrived, pose:a.spot?.pose}; });
      console.log(tag, L[i][3], JSON.stringify(st), st.pop === L[i][3] ? 'OK' : 'MISMATCH');
      if (i < 7) await (await p.$('.stage-view')).screenshot({ path: path.resolve(__dirname, `pop-${tag}-${L[i][3]}.png`) });
    }
  };
  await run('truck');
  console.log('place', await p.$eval('#mvCard', e => e.textContent).catch(() => 'n/a'));
  // 빈 땅이 있는 마을로 바꿔서 다시
  await p.evaluate(() => { const d = JSON.parse(localStorage.getItem('harulog.data')); d.profile.world.slots[2].kind = 'empty'; localStorage.setItem('harulog.data', JSON.stringify(d)); });
  await p.reload(); await p.waitForTimeout(800);
  await run('lot');
  // 수동: 점심을 '원래 장소' 대신 영화관으로
  await p.evaluate(() => { const d = JSON.parse(localStorage.getItem('harulog.data')); const k = Object.keys(d.days)[0]; console.log(k); }).catch(() => {});
  console.log('ERR', errs); await b.close();
})();
