// 앱 연동 레이어(native.js)를 가짜 플러그인으로 브라우저에서 검증
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 412, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' || m.type()==='warning') errs.push(m.text()); });
  await p.route('**/capacitor.js', r => r.fulfill({ body: '/* mocked */', contentType: 'text/javascript' }));
  await p.route('https://fonts.googleapis.com/**', r => r.abort());
  await p.route('https://api.open-meteo.com/**', r => {
    const t = [], code = [], mx = [], mn = [], w = [];
    for (let i = 31; i >= 0; i--) { const d = new Date(); d.setDate(d.getDate() - i); t.push(d.toISOString().slice(0, 10)); code.push(i === 0 ? 61 : 1); mx.push(14); mn.push(6); w.push(12); }
    r.fulfill({ contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: JSON.stringify({ daily: { time: t, weather_code: code, temperature_2m_max: mx, temperature_2m_min: mn, wind_speed_10m_max: w } }) });
  });
  await p.addInitScript(() => {
    const day = (off, h, m = 0) => { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() + off); d.setHours(h, m); return d; };
    window.__calls = [];
    const log = (n, a) => { window.__calls.push(n); };
    const mocks = {
      Geolocation: { checkPermissions: async () => ({ location: 'granted', coarseLocation: 'granted' }), requestPermissions: async () => ({ coarseLocation: 'granted' }),
        getCurrentPosition: async () => ({ coords: { latitude: 37.5665, longitude: 126.978 } }) },
      Health: { isAvailable: async () => ({ available: true }), checkAuthorization: async () => ({ readAuthorized: ['sleep', 'steps', 'workouts'], readDenied: [] }),
        requestAuthorization: async () => ({}), openHealthConnectSettings: async () => {},
        readSamples: async o => { log('readSamples', o); return { samples: [
          { startDate: day(-1, 23, 40).toISOString(), endDate: day(0, 3, 0).toISOString(), sleepState: 'light' },
          { startDate: day(0, 3, 0).toISOString(), endDate: day(0, 3, 20).toISOString(), sleepState: 'awake' },
          { startDate: day(0, 3, 20).toISOString(), endDate: day(0, 7, 10).toISOString(), sleepState: 'deep' } ] }; },
        queryWorkouts: async () => ({ workouts: [{ workoutType: 'running', duration: 1800, startDate: day(0, 7, 30).toISOString(), endDate: day(0, 8, 0).toISOString() }] }),
        queryAggregated: async () => ({ samples: [{ startDate: day(0, 13).toISOString(), value: 3200 }, { startDate: day(0, 18).toISOString(), value: 2500 }] }) },
      PhoneSignals: { checkUsageAccess: async () => ({ granted: true }), openUsageAccessSettings: async () => {},
        getScreenEvents: async () => ({ events: [
          { time: day(-1, 23, 50).getTime(), type: 'off' }, { time: day(0, 2, 0).getTime(), type: 'on' }, { time: day(0, 2, 1).getTime(), type: 'off' },
          { time: day(0, 7, 5).getTime(), type: 'on' } ] }) } };
    window.Capacitor = { isNativePlatform: () => true, registerPlugin: n => mocks[n] };
  });
  await p.goto('file://' + path.resolve(__dirname, '../www/index.html'));
  await p.waitForTimeout(1500);
  const drafts = await p.$$eval('#draftCard li.draft', ls => ls.map(l => l.innerText.replace(/\s+/g, ' ')));
  console.log('EARLY', errs);
  console.log('DRAFTS', JSON.stringify(drafts, null, 1));
  await p.screenshot({ path: path.resolve(__dirname, 'shot-today.png'), fullPage: false });
  // accept all
  const all = await p.$('#draftCard .btn.primary:has-text("모두 맞아요")'); if (all) await all.click();
  await p.waitForTimeout(400);
  const saved = await p.evaluate(() => { const d = window.Haru.data.days[window.Haru.todayStr()]; return { weather: d.weather, temp: d.temp, acts: d.activities.map(a => [a.type, a.title, a.time.value, a.source, a.sleepHours]) }; });
  console.log('SAVED', JSON.stringify(saved));
  // settings card
  await p.click('#tab-settings'); await p.waitForTimeout(500);
  console.log('CARD', (await p.innerText('#nativeCard')).replace(/\n+/g, ' | '));
  console.log('NOTE', await p.innerText('#storeNote'));
  await (await p.$('#nativeCard')).screenshot({ path: path.resolve(__dirname, 'shot-settings.png') });
  // phone-only fallback: turn off health
  await p.click('#nativeCard button:has-text("건강 앱 끄기")'); await p.click('#tab-today'); await p.evaluate(() => window.Haru.setView('today'));
  await p.click('#btnPrevDay'); await p.waitForTimeout(800);
  await p.waitForTimeout(1500); console.log('SEL', await p.evaluate(()=>window.Haru.sel), await p.evaluate(()=>window.__calls.length));
  console.log('YESTERDAY (health off)', JSON.stringify(await p.$$eval('#draftCard li.draft', ls => ls.map(l => l.innerText.replace(/\s+/g, ' ')))));
  console.log('ERRORS', errs);
  await b.close();
})();
