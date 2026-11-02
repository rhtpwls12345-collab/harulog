// v2 가구: 추천 배치·가구 추가·끌어 옮기기·겹침 막기·삭제·길찾기 장애물·활동 자리 연결, 기존 데이터 호환
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 1200 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('https://fonts.googleapis.com/**', r => r.abort());
  await p.goto('file://' + path.resolve(__dirname, '../www/index.html')); await p.waitForTimeout(700);
  await p.click('#tab-world'); await p.waitForTimeout(300);
  const W = () => p.evaluate(() => JSON.parse(JSON.stringify(window.Haru.data.profile.world)));
  // 체육관 칸(5번째) 선택 → 크게 → 추천 배치
  await p.click('#wSlots .slot >> nth=4'); await p.click('#wEdit .seg button:has-text("크게")'); await p.waitForTimeout(200);
  await p.click('#wEdit button:has-text("추천 배치")'); await p.waitForTimeout(300);
  let w = await W(); console.log('gym items', w.slots[4].items.map(q => q.k).join(','));
  // 블록 확인: 러닝머신 자리 막힘
  const blocked = await p.evaluate(() => { const H = window.Haru._world, b = H.BUILDINGS.find(q => q.kind === 'gym'), it = window.Haru.data.profile.world.slots[b.slot].items.find(q => q.k === 'treadmill');
    const x = b.x + it.x + 15, y = b.y + it.y + 18; return H.grid[Math.floor(y/H.GC)*H.GW + Math.floor(x/H.GC)]; });
  console.log('treadmill blocked', blocked === 1);
  // 가구 하나 더 추가 (복싱 링)
  await p.click('#wEdit .furngrid .ptile:has-text("복싱 링")'); await p.waitForTimeout(300);
  w = await W(); console.log('after add', w.slots[4].items.length, w.slots[4].items.at(-1));
  await p.screenshot({ path: path.resolve(__dirname, 'furn1.png') });
  // 삭제
  const del = await p.$('#wEdit .furnsel button:has-text("삭제")'); console.log('delete visible', !!del); if (del) await del.click(); await p.waitForTimeout(200);
  w = await W(); console.log('after delete', w.slots[4].items.length);
  // 운동 활동 → 가구 자리
  await p.click('#tab-today'); await p.click('#btnAdd'); await p.click('#ft-exercise', { force: true }); await p.click('#actForm button[type=submit]'); await p.waitForTimeout(300);
  await p.click('#actList .act >> nth=0'); await p.waitForTimeout(4500);
  const sp = await p.evaluate(() => { const a = window.Haru._world.actor; return {item:a.spot.item, x:Math.round(a.x), y:Math.round(a.y)}; });
  console.log('exercise spot', JSON.stringify(sp));
  await (await p.$('.stage-view')).screenshot({ path: path.resolve(__dirname, 'furn2.png') });
  // 모두 치우기 → 기본 가구
  await p.click('#tab-world'); await p.click('#wSlots .slot >> nth=4'); await p.click('#wEdit button:has-text("가구 모두 치우기")'); await p.waitForTimeout(200);
  w = await W(); console.log('cleared', w.slots[4].items === undefined);
  // 기존(옛) 데이터 호환: items 없는 world 그대로
  console.log('keys', Object.keys(w).join(','));
  console.log('ERR', errs); await b.close();
})();
