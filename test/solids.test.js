// 리디자인에서 새로 놓은 가구 6개가 길찾기 '못 지나가는 자리'로 등록됐는지, 각 활동 자리까지 가는 길이 가구를 뚫지 않는지 검사
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('https://fonts.googleapis.com/**', r => r.abort());
  await p.goto('file://' + path.resolve(__dirname, '../www/index.html')); await p.waitForTimeout(800);
  const r = await p.evaluate(() => {
    const W = window.Haru._world, out = {blocked:[], crossings:[]};
    const NEW = {home:[[88,86,24,15],[152,76,14,16]], gym:[[20,96,34,15],[204,62,10,30],[204,40,12,14]], cafe:[[30,112,12,16]]};
    const cell = (x, y) => W.grid[Math.floor(y/W.GC)*W.GW + Math.floor(x/W.GC)];
    for (const [k, rects] of Object.entries(NEW)){ const bd = W.BUILDINGS.find(q => q.kind === k);
      for (const [x, y, w, h] of rects){ const cx = bd.x + bd.cx + x + w/2, cy = bd.y + y + h/2; out.blocked.push([k, [x, y, w, h].join(','), cell(cx, cy) === 1]); } }
    // 모든 활동 자리로 집 문 앞에서 길찾기 → 경로가 새 가구 사각형을 지나가는지
    const home = W.BUILDINGS.find(q => q.kind === 'home'), start = [home.x + home.w/2, home.y + home.h + 12];
    const inside = (px, py) => Object.entries(NEW).some(([k, rects]) => { const bd = W.BUILDINGS.find(q => q.kind === k); return rects.some(([x, y, w, h]) => px > bd.x + bd.cx + x && px < bd.x + bd.cx + x + w && py > bd.y + y && py < bd.y + y + h); });
    for (const [name, sp] of Object.entries(W.SPOT)){ if (sp.world || !sp.b) continue; const bd = sp.b === 'park' ? W.PARKB : W.BUILDINGS.find(q => q.kind === sp.b); if (!bd) continue;
      const ap = W.toWorld(sp, sp.ap), fin = W.toWorld(sp, sp.fin), path = [start, ...W.findPath(start, ap), fin];
      for (let i = 1; i < path.length; i++){ const [x0, y0] = path[i - 1], [x1, y1] = path[i]; for (let k = 0; k <= 40; k++){ const x = x0 + (x1 - x0)*k/40, y = y0 + (y1 - y0)*k/40; if (inside(x, y)){ out.crossings.push(name); k = 99; i = 99; } } } }
    return out;
  });
  console.log(JSON.stringify(r), errs); await b.close();
})();
