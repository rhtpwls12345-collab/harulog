// 새 마을 꾸미기 UI: 칸 종류 바꾸기(유일 건물 맞바꿈), 위치 바꾸기, 크기·벽색·바닥, 맵 크기, 소품 놓기/지우기, 저장 데이터 구조 유지
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 1100 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('https://fonts.googleapis.com/**', r => r.abort());
  await p.goto('file://' + path.resolve(__dirname, '../www/index.html')); await p.waitForTimeout(700);
  await p.click('#tab-world'); await p.waitForTimeout(400);
  const W = () => p.evaluate(() => JSON.parse(JSON.stringify(window.Haru.data.profile.world)));
  const kinds = async () => (await W()).slots.map(s => s.kind).join(',');
  console.log('start', await kinds());
  await p.click('#wSlots .slot >> nth=1'); await p.click('#wEdit .kchip:has-text("카페")'); await p.waitForTimeout(200);
  console.log('work→cafe (swap)', await kinds());
  await p.click('#wEdit button[aria-label="오른쪽 칸과 바꾸기"]'); await p.waitForTimeout(200);
  console.log('move right', await kinds());
  await p.click('#wEdit .seg button:has-text("크게")'); await p.click('#wEdit .wsw[aria-label="벽 색 라벤더"]'); await p.click('#wEdit .ftile:has-text("모던")'); await p.waitForTimeout(200);
  console.log('slot2', JSON.stringify((await W()).slots[2]));
  await p.click('#wSize button:has-text("작게")'); await p.waitForTimeout(200); console.log('small', await kinds());
  await p.click('#wSize button:has-text("보통")'); await p.waitForTimeout(200);
  // props: place 2, erase 1
  await p.click('#propPalette .ptile:has-text("허수아비")'); const box = await (await p.$('#preview')).boundingBox();
  await p.mouse.click(box.x + box.width*.45, box.y + box.height*.52); await p.waitForTimeout(150);
  await p.mouse.click(box.x + box.width*.2, box.y + box.height*.53); await p.waitForTimeout(150);
  console.log('hint', await p.isVisible('#pvHint'), await p.textContent('#pvHint'));
  console.log('props', JSON.stringify((await W()).props.village));
  await p.click('#propPalette .ptile.erase'); await p.mouse.click(box.x + box.width*.45, box.y + box.height*.52 - 2); await p.waitForTimeout(150);
  console.log('after erase', (await W()).props.village.length, await p.textContent('#propCount'));
  const w = await W(); console.log('keys', Object.keys(w).join(','), Object.keys(w.slots[0]).join(','));
  // reload keeps it
  await p.reload(); await p.waitForTimeout(500); console.log('reload', await kinds());
  console.log('ERR', errs); await b.close();
})();
