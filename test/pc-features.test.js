// 캘린더·이동·사진 초안 + 사진 첨부·하루 영상 표시 검증 (pc-test.html)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.route('https://fonts.googleapis.com/**', r => r.abort());
  await p.route('https://api.open-meteo.com/**', r => r.abort());
  await p.goto('file://' + path.resolve(__dirname, '../pc-test.html')); await p.waitForTimeout(1000);
  await p.click('.pcmock>button'); await p.click('#pmGrant'); await p.click('.pcmock>button'); await p.waitForTimeout(1500);
  await p.click('#btnPrevDay'); await p.waitForTimeout(1500);
  const drafts = async () => p.$$eval('#draftCard li.draft', l => l.map(x => x.innerText.replace(/\s+/g, ' ').slice(0, 110)));
  console.log('YDAY', JSON.stringify(await drafts(), null, 1));
  console.log('THUMBS', await p.$$eval('#draftCard .ph-strip img', l => l.filter(i => i.src.startsWith('data:')).length));
  await p.screenshot({ path: path.resolve(__dirname, 'f1.png'), fullPage: true });
  // accept first draft that has photos
  const n = await p.$$eval('#draftCard li.draft', l => l.findIndex(x => x.querySelector('.ph-strip') && x.innerText.includes('맞아요')));
  console.log('photo-draft idx', n);
  if (n >= 0){ await (await p.$$('#draftCard li.draft'))[n].$('button:has-text("맞아요")').then(x => x.click()); await p.waitForTimeout(1500); }
  console.log('ACTS', await p.evaluate(() => (window.Haru.data.days[window.Haru.sel]?.activities || []).map(a => [a.type, a.title, a.time.value, a.source, (a.photos || []).length])));
  console.log('LIST IMGS', await p.$$eval('#actList .ph-strip img', l => l.map(i => i.src.slice(0, 10))));
  // standalone photo draft → 기록하기 opens form with photos
  const k = await p.$$eval('#draftCard li.draft', l => l.findIndex(x => x.innerText.includes('기록하기')));
  console.log('loose idx', k);
  if (k >= 0){
    await (await p.$$('#draftCard li.draft'))[k].$('button:has-text("기록하기")').then(x => x.click()); await p.waitForTimeout(1200);
    console.log('FORM photos', await p.$$eval('#fPhotos .ph img', l => l.length));
    await p.click('#ft-cafe', { force: true }); await p.click('#actForm button[type=submit]'); await p.waitForTimeout(800);
  }
  // manual upload on new record
  await p.click('#btnAdd'); await p.waitForTimeout(300);
  await p.click('#ft-hobby', { force: true });
  const png = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==', 'base64');
  await p.setInputFiles('#fPhotoFile', { name: 'a.png', mimeType: 'image/png', buffer: png }); await p.waitForTimeout(800);
  console.log('MANUAL form photos', await p.$$eval('#fPhotos .ph img', l => l.length));
  await p.click('#actForm button[type=submit]'); await p.waitForTimeout(800);
  console.log('ACTS2', await p.evaluate(() => (window.Haru.data.days[window.Haru.sel]?.activities || []).map(a => [a.type, a.title, (a.photos || []).length])));
  // movie card with photos
  await p.click('#btnPlay'); await p.waitForTimeout(3600);
  console.log('MOVIE photos', await p.$$eval('#mvCard .mv-photos img', l => l.length));
  await p.screenshot({ path: path.resolve(__dirname, 'f2.png') });
  await p.click('#thClose');
  // settings card
  await p.click('#tab-settings'); await p.waitForTimeout(600);
  await (await p.$('#nativeCard')).screenshot({ path: path.resolve(__dirname, 'f3.png') });
  // reload: photos persist
  await p.reload(); await p.waitForTimeout(1500);
  console.log('AFTER RELOAD idb keys', await p.evaluate(() => new Promise(r => { const q = indexedDB.open('harulog-photos'); q.onsuccess = () => { const t = q.result.transaction('p').objectStore('p').getAllKeys(); t.onsuccess = () => r(t.result.length); }; })));
  console.log('ERR', errs); await b.close();
})();
