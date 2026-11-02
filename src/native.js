/* 하루로그 Android 연동 레이어 (Capacitor)
 * 웹(아티팩트)에서는 아무것도 하지 않고, 앱에서만 window.HaruNative 를 만든다.
 * 하루 초안 카드(draftItems)는 HaruNative.items(date) 가 돌려주는 실제 신호를 '예시' 대신 사용한다.
 *  - 날씨: 대략적 위치(coarse) → Open-Meteo (키 없음)
 *  - 워치·건강 앱: Health Connect (@capgo/capacitor-health) 수면 / 운동 / 걸음 수
 *  - 휴대폰 사용: 자체 플러그인 PhoneSignals (화면 켜짐·꺼짐 기록) → 수면 추정 (건강 앱 수면이 없을 때만)
 *  - 캘린더·이동 수단·사진: 자체 플러그인 DayData (휴대폰 캘린더 일정, 구글 활동 인식 전환 기록, 갤러리 사진 시각)
 * 모든 판단은 기기 안에서 하고, 확인(‘맞아요’) 전에는 기록에 저장하지 않는다.
 */
(() => {
  const C = window.Capacitor;
  if (!C || typeof C.isNativePlatform !== 'function' || !C.isNativePlatform() || typeof C.registerPlugin !== 'function') return;

  const Health = C.registerPlugin('Health');
  const Geo = C.registerPlugin('Geolocation');
  const Phone = C.registerPlugin('PhoneSignals');
  const Day = C.registerPlugin('DayData');
  const H = () => window.Haru;

  /* ---------- 설정 (기록 데이터와 분리해 저장) ---------- */
  const KEY = 'harulog.native';
  const conf = (() => {
    try {
      const v = JSON.parse(localStorage.getItem(KEY) || '{}');
      const loc = v.loc && Number.isFinite(v.loc.lat) && Number.isFinite(v.loc.lon) ? v.loc : null;
      return {weather:v.weather !== false, health:v.health !== false, phone:v.phone !== false, calendar:v.calendar !== false, move:v.move !== false, photos:v.photos !== false, loc};
    } catch (e) { return {weather:true, health:true, phone:true, calendar:true, move:true, photos:true, loc:null}; }
  })();
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(conf)); } catch (e) {} };

  const state = {location:'unknown', health:'unknown', healthReason:'', healthRead:[], usage:'unknown', calendar:'unknown', photos:'unknown', activity:'unknown', tracking:false, checked:false};
  const HEALTH_READ = ['sleep', 'steps', 'workouts'];

  /* ---------- 날짜 도우미 ---------- */
  const at = (date, h, m = 0) => { const d = H().parseYmd(date); d.setHours(h, m, 0, 0); return d; };
  const hm = d => `${H().pad(d.getHours())}:${H().pad(d.getMinutes())}`;
  const half = x => Math.round(x*2)/2;
  const daysAgo = date => Math.round((H().parseYmd(H().todayStr()) - H().parseYmd(date))/864e5);

  /* ---------- 상태 확인 ---------- */
  async function checkLocation(){
    try { const p = await Geo.checkPermissions(); state.location = p.coarseLocation || p.location || 'prompt'; }
    catch (e) { state.location = 'off'; } // 기기 위치 서비스가 꺼져 있으면 예외
  }
  async function checkHealth(){
    try {
      const a = await Health.isAvailable();
      if (!a.available){ state.health = 'unavailable'; state.healthReason = a.reason || ''; return; }
      const s = await Health.checkAuthorization({read:HEALTH_READ});
      state.healthRead = s.readAuthorized || [];
      state.health = state.healthRead.length === HEALTH_READ.length ? 'granted' : state.healthRead.length ? 'partial' : 'prompt';
    } catch (e) { state.health = 'unavailable'; state.healthReason = String(e && e.message || e); }
  }
  async function checkUsage(){
    try { const r = await Phone.checkUsageAccess(); state.usage = r.granted ? 'granted' : 'prompt'; }
    catch (e) { state.usage = 'unavailable'; }
  }
  async function checkDay(){
    try { const r = await Day.checkAccess(); Object.assign(state, {calendar:r.calendar, photos:r.photos, activity:r.activity, tracking:!!r.tracking}); }
    catch (e) { Object.assign(state, {calendar:'unavailable', photos:'unavailable', activity:'unavailable', tracking:false}); }
  }
  async function checkAll(){ await Promise.all([checkLocation(), checkHealth(), checkUsage(), checkDay()]); state.checked = true; }

  /* ---------- 날씨 (Open-Meteo, 최근 31일 + 오늘) ---------- */
  let wxTable = null; // {key, at, days:{ymd:{code,tmax,tmin,wind}}}
  async function coords(askUser){
    if (conf.loc && Date.now() - conf.loc.at < 6*3600e3) return conf.loc;
    if (state.location !== 'granted'){
      if (!askUser) return conf.loc;
      const p = await Geo.requestPermissions({permissions:['coarseLocation']});
      state.location = p.coarseLocation || p.location || 'denied';
      if (state.location !== 'granted') return conf.loc;
    }
    const pos = await Geo.getCurrentPosition({enableHighAccuracy:false, timeout:15000, maximumAge:3600e3});
    // 소수점 2자리(약 1km)로만 보관·전송
    conf.loc = {lat:Math.round(pos.coords.latitude*100)/100, lon:Math.round(pos.coords.longitude*100)/100, at:Date.now()};
    save();
    return conf.loc;
  }
  async function weatherDays(loc){
    const key = loc.lat + ',' + loc.lon;
    if (wxTable && wxTable.key === key && Date.now() - wxTable.at < 30*60e3) return wxTable.days;
    const url = 'https://api.open-meteo.com/v1/forecast?latitude=' + loc.lat + '&longitude=' + loc.lon +
      '&daily=weather_code,temperature_2m_max,temperature_2m_min,wind_speed_10m_max&timezone=auto&past_days=31&forecast_days=1';
    const res = await fetch(url);
    if (!res.ok) throw new Error('날씨 서버 응답 ' + res.status);
    const j = await res.json(), d = j.daily || {}, days = {};
    (d.time || []).forEach((t, i) => { days[t] = {code:d.weather_code[i], tmax:d.temperature_2m_max[i], tmin:d.temperature_2m_min[i], wind:d.wind_speed_10m_max[i]}; });
    wxTable = {key, at:Date.now(), days};
    return days;
  }
  function wxKind(w){
    const c = w.code;
    let k = c <= 1 ? 'sunny' : c <= 3 ? 'cloudy' : c === 45 || c === 48 ? 'foggy'
      : (c >= 71 && c <= 77) || c === 85 || c === 86 ? 'snowy' : 'rainy';
    if ((k === 'sunny' || k === 'cloudy') && w.wind >= 30) k = 'windy';
    const mean = (w.tmax + w.tmin)/2;
    const temp = mean >= 25 ? 'hot' : mean >= 16 ? 'warm' : mean >= 6 ? 'cool' : 'cold';
    return {weather:k, temp};
  }
  async function weatherItem(date, askUser){
    if (!conf.weather || daysAgo(date) > 31) return null;
    const loc = await coords(askUser);
    if (!loc) return null;
    const w = (await weatherDays(loc))[date];
    if (!w || w.code == null) return null;
    const {weather, temp} = wxKind(w), W = H().WEATHER, T = H().TEMP;
    return {id:'nat-wx', src:'weather', weather, temp, title:`${W[weather].label} · ${T[temp].label}`,
      why:`현재 위치 기준 · 최고 ${Math.round(w.tmax)}° / 최저 ${Math.round(w.tmin)}° (Open-Meteo)`};
  }

  /* ---------- Health Connect ---------- */
  const has = t => state.health === 'granted' || (state.health === 'partial' && state.healthRead.includes(t));
  function sessions(samples){
    const list = samples.map(s => ({a:new Date(s.startDate), b:new Date(s.endDate), awake:s.sleepState === 'awake'}))
      .filter(s => s.b > s.a).sort((x, y) => x.a - y.a);
    const out = [];
    for (const s of list){
      const last = out[out.length - 1];
      if (last && s.a - last.b <= 60*60e3){ last.b = new Date(Math.max(last.b, s.b)); if (s.awake) last.awake += s.b - s.a; }
      else out.push({a:s.a, b:s.b, awake:s.awake ? s.b - s.a : 0});
    }
    return out.map(s => Object.assign(s, {hours:half(Math.max(0, s.b - s.a - s.awake)/36e5)})).filter(s => s.hours >= 1);
  }
  async function healthSleep(date){
    if (!conf.health || !has('sleep')) return null;
    const r = await Health.readSamples({dataType:'sleep', startDate:at(date, -6).toISOString(), endDate:at(date, 30).toISOString(), limit:500, ascending:true});
    const all = sessions(r.samples || []);
    // 오늘 아침에 끝난 잠 → 기상, 오늘 밤에 시작해 이미 끝난 잠 → 취침
    const morning = all.filter(s => s.b >= at(date, 3) && s.b <= at(date, 14)).sort((x, y) => y.hours - x.hours)[0] || null;
    const night = all.filter(s => s.a >= at(date, 19) && s.a <= at(date, 29) && s.b <= new Date()).sort((x, y) => y.hours - x.hours)[0] || null;
    return {morning, night};
  }
  const WORKOUT = {running:'러닝', walking:'걷기', cycling:'자전거', swimming:'수영', yoga:'요가', hiking:'등산', pilates:'필라테스',
    strengthTraining:'근력 운동', traditionalStrengthTraining:'근력 운동', functionalStrengthTraining:'근력 운동', highIntensityIntervalTraining:'인터벌 운동',
    dance:'댄스', tennis:'테니스', badminton:'배드민턴', soccer:'축구', basketball:'농구', golf:'골프', elliptical:'일립티컬', rowing:'로잉', stairClimbing:'계단 오르기'};
  async function healthWorkouts(date){
    if (!conf.health || !has('workouts')) return [];
    const r = await Health.queryWorkouts({startDate:at(date, 0).toISOString(), endDate:at(date, 24).toISOString(), limit:20, ascending:true});
    return (r.workouts || []).map(w => {
      const a = new Date(w.startDate), min = Math.round((w.duration || (new Date(w.endDate) - a)/1000)/60);
      const walk = w.workoutType === 'walking' || w.workoutType === 'hiking';
      return {id:'hc-wk-' + a.getTime(), src:'watch', multi:true, a, b:new Date(w.endDate || a.getTime() + min*60e3), type:walk ? 'walk' : 'exercise', title:WORKOUT[w.workoutType] || '운동',
        time:{kind:'clock', value:hm(a)}, why:`워치·건강 앱 운동 기록 ${hm(a)}부터 ${min}분`};
    }).filter(w => !Number.isNaN(+w.id.slice(6)));
  }
  async function healthSteps(date){
    if (!conf.health || !has('steps')) return null;
    const r = await Health.queryAggregated({dataType:'steps', startDate:at(date, 0).toISOString(), endDate:at(date, 24).toISOString(), bucket:'hour', aggregation:'sum'});
    const rows = (r.samples || []).map(s => ({h:new Date(s.startDate).getHours(), v:Number(s.value) || 0}));
    const total = rows.reduce((s, x) => s + x.v, 0);
    if (total < 4000) return null;
    const peak = rows.slice().sort((x, y) => y.v - x.v)[0];
    const period = peak.h >= 5 && peak.h < 11 ? 'morning' : peak.h < 17 && peak.h >= 11 ? 'afternoon' : peak.h >= 17 && peak.h < 21 ? 'evening' : 'night';
    return {id:'hc-steps', src:'steps', type:'walk', title:'걷기', time:{kind:'period', value:period},
      why:`하루 ${Math.round(total).toLocaleString('ko-KR')}보 · ${peak.h}시쯤 가장 많이 걸었어요`};
  }

  /* ---------- 휴대폰 사용으로 수면 추정 ---------- */
  // 화면이 꺼져 있던 가장 긴 구간(사이에 3분 미만으로 잠깐 켠 건 이어 붙임)을 잠으로 본다.
  function longestOff(events, from, to){
    const ev = events.filter(e => e.time >= from - 12*3600e3).sort((x, y) => x.time - y.time);
    const offs = []; let offAt = null;
    for (const e of ev){
      if (e.type === 'off'){ if (offAt == null) offAt = e.time; }
      else if (offAt != null){ offs.push({a:offAt, b:e.time}); offAt = null; }
    }
    const merged = [];
    for (const o of offs){ const l = merged[merged.length - 1]; if (l && o.a - l.b < 3*60e3) l.b = o.b; else merged.push({...o}); }
    return merged.filter(o => o.a >= from && o.a <= to && o.b - o.a >= 3*3600e3).sort((x, y) => (y.b - y.a) - (x.b - x.a))[0] || null;
  }
  async function phoneSleep(date){
    if (!conf.phone || state.usage !== 'granted') return null;
    const r = await Phone.getScreenEvents({start:at(date, -12).getTime(), end:Math.min(Date.now(), at(date, 38).getTime())}) // 다음날 14시까지 봐야 밤잠의 끝(기상)을 알 수 있다;
    const ev = r.events || [];
    const m = longestOff(ev, at(date, -4).getTime(), at(date, 6).getTime());       // 어젯밤 20시~오늘 6시에 잠듦
    const n = longestOff(ev, at(date, 20).getTime(), at(date, 30).getTime());      // 오늘 20시~내일 6시에 잠듦
    const toS = o => o && o.b <= Date.now() && new Date(o.b) >= at(date, -4) ? {a:new Date(o.a), b:new Date(o.b), hours:half((o.b - o.a)/36e5)} : null;
    const morning = toS(m), night = toS(n);
    return {morning:morning && morning.b <= at(date, 14) ? morning : null, night};
  }

  function sleepItems(date, s, src){
    const out = [], label = src === 'phone' ? '휴대폰 화면이 꺼져 있던 시간으로 추정했어요' : '워치·건강 앱 수면 기록';
    if (s.morning) out.push({id:src + '-wake', src, type:'wake', title:'기상', time:{kind:'clock', value:hm(s.morning.b)},
      why:`${label} · ${hm(s.morning.a)}~${hm(s.morning.b)}, ${s.morning.hours}시간 잤어요`});
    if (s.night) out.push({id:src + '-bed', src, type:'sleep', title:'취침', sleepHours:s.night.hours, time:{kind:'clock', value:hm(s.night.a)},
      why:`${label} · ${hm(s.night.a)}에 잠들어 ${hm(s.night.b)}까지 ${s.night.hours}시간`});
    return out;
  }

  /* ---------- 캘린더 ---------- */
  async function calendarItems(date){
    if (!conf.calendar || state.calendar !== 'granted') return [];
    const r = await Day.getEvents({start:at(date, 0).getTime(), end:at(date, 24).getTime()});
    const now = Date.now();
    return (r.events || []).filter(e => !e.allDay && e.begin <= now && e.begin >= at(date, 0).getTime()).slice(0, 12).map(e => {
      const a = new Date(e.begin), b = new Date(e.end), title = String(e.title || '일정').trim().slice(0, 80) || '일정';
      return {id:'cal-' + e.id + '-' + e.begin, src:'calendar', multi:true, type:H().suggestFor(title + ' ' + (e.location || '')) || 'other', title,
        time:{kind:'clock', value:hm(a)}, a, b,
        why:`캘린더 · ${hm(a)}~${hm(b)}` + (e.location ? ` · ${String(e.location).slice(0, 30)}` : '') + (e.calendar ? ` (${String(e.calendar).slice(0, 20)})` : '')};
    });
  }

  /* ---------- 이동 수단 (활동 인식 전환 기록) ---------- */
  const MOVE = {vehicle:{type:'commute', title:'차량 이동', min:8, note:'버스·지하철·자동차'}, bicycle:{type:'commute', title:'자전거 이동', min:8, note:'자전거'},
    running:{type:'exercise', title:'달리기', min:10, note:'달리기'}, walking:{type:'walk', title:'걷기', min:15, note:'걷기'}};
  function moveSegments(trs, from, to){
    const segs = [], open = {};
    for (const t of trs.slice().sort((x, y) => x.time - y.time)){
      if (t.kind === 'enter'){ for (const k in open){ segs.push({act:k, a:open[k], b:t.time}); delete open[k]; } open[t.activity] = t.time; }
      else if (open[t.activity] != null){ segs.push({act:t.activity, a:open[t.activity], b:t.time}); delete open[t.activity]; }
    }
    const merged = [];
    for (const g of segs.sort((x, y) => x.a - y.a)){ const l = merged[merged.length - 1]; if (l && l.act === g.act && g.a - l.b < 5*60e3) l.b = Math.max(l.b, g.b); else merged.push({...g}); }
    return merged.filter(g => MOVE[g.act] && g.a >= from && g.a < to && g.b - g.a >= MOVE[g.act].min*60e3);
  }
  async function moveItems(date){
    if (!conf.move || !state.tracking) return [];
    const r = await Day.getTransitions({start:at(date, -2).getTime(), end:Math.min(Date.now(), at(date, 26).getTime())});
    return moveSegments(r.transitions || [], at(date, 0).getTime(), at(date, 24).getTime()).map(g => {
      const m = MOVE[g.act], a = new Date(g.a), b = new Date(g.b), min = Math.round((g.b - g.a)/60e3);
      return {id:'mv-' + g.act + '-' + g.a, src:'move', multi:true, type:m.type, title:m.title, time:{kind:'clock', value:hm(a)}, a, b, act:g.act,
        why:`이동 감지 · ${hm(a)}~${hm(b)} (${min}분) · ${m.note}`};
    });
  }

  /* ---------- 사진 ---------- */
  async function dayPhotos(date){
    if (!conf.photos || !(state.photos === 'granted' || state.photos === 'limited')) return [];
    const r = await Day.getPhotos({start:at(date, 0).getTime(), end:Math.min(Date.now(), at(date, 24).getTime())});
    return (r.photos || []).filter(p => !p.screenshot).sort((x, y) => x.time - y.time);
  }
  // 60분 넘게 끊기면 다른 묶음
  function clusters(ps){
    const out = [];
    for (const p of ps){ const l = out[out.length - 1]; if (l && p.time - l.b <= 60*60e3){ l.list.push(p); l.b = p.time; } else out.push({a:p.time, b:p.time, list:[p]}); }
    return out;
  }
  const pick = (list, n) => list.length <= n ? list : Array.from({length:n}, (_, i) => list[Math.round(i*(list.length - 1)/(n - 1))]);
  function attachPhotos(items, ps){
    const rest = [];
    for (const c of clusters(ps)){
      const mid = (c.a + c.b)/2;
      // 같은 시간대 일정·운동·이동 초안이 있으면 거기에 사진을 붙인다
      const host = items.find(it => it.a && it.b && mid >= it.a.getTime() - 15*60e3 && mid <= it.b.getTime() + 30*60e3 && !it.photoRefs);
      const refs = pick(c.list, 6).map(p => p.id);
      if (host){ host.photoRefs = refs; host.thumbs = refs.slice(0, 4); host.photoCount = c.list.length; host.why += ` · 사진 ${c.list.length}장`; continue; }
      const a = new Date(c.a), b = new Date(c.b);
      rest.push({id:'ph-' + c.list[0].id, src:'photo', multi:true, type:null, title:'', time:{kind:'clock', value:hm(a)}, photoRefs:refs, thumbs:refs.slice(0, 4), photoCount:c.list.length,
        why:c.list.length > 1 ? `사진 ${c.list.length}장 · ${hm(a)}~${hm(b)}에 찍었어요` : `사진 1장 · ${hm(a)}에 찍었어요`});
    }
    return rest;
  }

  /* ---------- 날짜별 초안 모으기 ---------- */
  const cache = new Map(); // date -> {items, at, loading, errors}
  async function fetchDay(date, askUser){
    const prev = cache.get(date);
    const entry = {items:prev ? prev.items : [], at:Date.now(), loading:true, errors:[]};
    cache.set(date, entry);
    if (!state.checked) await checkAll();
    const safe = (name, p) => p.catch(e => { entry.errors.push(name); console.warn('[harulog]', name, e); return null; });
    const [wx, hs, wk, st] = await Promise.all([
      safe('날씨', weatherItem(date, askUser)), safe('수면', healthSleep(date)), safe('운동', healthWorkouts(date)), safe('걸음', healthSteps(date))]);
    let items = [];
    if (wx) items.push(wx);
    let sleep = hs && (hs.morning || hs.night) ? hs : null, src = 'watch';
    const ps = await safe('휴대폰', phoneSleep(date));
    if (ps){ // 건강 앱에 없는 쪽만 휴대폰 추정으로 채운다
      if (!sleep) { sleep = ps; src = 'phone'; }
      else items.push(...sleepItems(date, {morning:sleep.morning ? null : ps.morning, night:sleep.night ? null : ps.night}, 'phone'));
    }
    if (sleep) items.unshift(...sleepItems(date, sleep, src));
    const [cal, mv, ph] = await Promise.all([safe('캘린더', calendarItems(date)), safe('이동', moveItems(date)), safe('사진', dayPhotos(date))]);
    const workouts = wk || [], overlaps = (g, list) => list.some(w => w.a ? (g.a < w.b && g.b > w.a) : false);
    const moves = (mv || []).filter(g => !(g.type !== 'commute' && overlaps(g, workouts))); // 워치 운동과 겹치면 워치 쪽을 쓴다
    const timed = [...(cal || []), ...workouts, ...moves];
    const loose = attachPhotos(timed, ph || []);
    items.push(...workouts, ...(cal || []), ...moves);
    if (st && !workouts.some(w => w.type === 'walk') && !moves.some(g => g.act === 'walking')) items.push(st);
    items.push(...loose);
    // 같은 종류는 하나만 (여러 번 있을 수 있는 multi 항목은 제외)
    const seen = new Set();
    items = items.filter(it => { if (it.multi) return true; const k = it.src === 'weather' ? 'wx' : it.type; if (seen.has(k)) return false; seen.add(k); return true; });
    items.sort((x, y) => (x.src === 'weather' ? -1 : 0) - (y.src === 'weather' ? -1 : 0) || tkey(x) - tkey(y));
    items = items.map(({a, b, act, ...rest}) => rest);
    const changed = JSON.stringify(items) !== JSON.stringify(entry.items) || entry.loading;
    Object.assign(entry, {items, at:Date.now(), loading:false});
    if (changed && H() && H().sel === date) H().renderDraft();
  }
  const tkey = it => !it.time || it.time.kind !== 'clock' ? ({morning:420, afternoon:780, evening:1080, night:1320}[it.time && it.time.value] || 1500) : (+it.time.value.slice(0, 2))*60 + +it.time.value.slice(3);
  const ttl = date => date === H().todayStr() ? 10*60e3 : 6*3600e3;

  /* ---------- 설정 카드 ---------- */
  function row(title, desc, status, on, actions){
    const el = H().el;
    return el('div', {class:'native-row'},
      el('div', {class:'stack', style:'gap:2px;flex:1'}, el('b', {text:title}), el('small', {text:desc}),
        actions.length ? el('div', {class:'btns', style:'margin-top:6px'}, ...actions) : null),
      el('span', {class:'native-state' + (on ? ' on' : ''), text:status}));
  }
  function toggle(key, label){
    const el = H().el;
    return el('button', {type:'button', class:'btn sm', 'aria-pressed':String(conf[key]), onclick:() => { conf[key] = !conf[key]; save(); cache.clear(); api.renderCard(); H().renderDraft(); }},
      conf[key] ? `${label} 끄기` : `${label} 켜기`);
  }
  const toBlob = u => { const [h, b64] = u.split(','), bin = atob(b64), arr = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i); return new Blob([arr], {type:(h.match(/data:([^;]+)/) || [])[1] || 'image/jpeg'}); };
  const thumbs = new Map();
  let cardBox = null;
  const api = {
    thumb(ref){
      if (!thumbs.has(ref)){ thumbs.set(ref, Day.getPhoto({id:ref, max:240}).then(r => r.dataUrl, () => null)); if (thumbs.size > 200) thumbs.delete(thumbs.keys().next().value); }
      return thumbs.get(ref);
    },
    async importPhotos(refs){
      const out = [];
      for (const ref of refs){ try { const r = await Day.getPhoto({id:ref, max:1280}); out.push(r.dataUrl ? toBlob(r.dataUrl) : null); } catch (e) { out.push(null); } }
      return out;
    },
    items(date){
      if (!H()) return []; // 앱 초기화 중 (ready() 가 곧 다시 그린다)
      if (H().isFuture(date)) return [];
      const c = cache.get(date);
      if (!c || (!c.loading && Date.now() - c.at > ttl(date))) fetchDay(date, false);
      return c ? c.items : [];
    },
    loading(date){ const c = cache.get(date); return !c || c.loading; },
    refresh(date){ cache.delete(date); wxTable = null; state.checked = false; fetchDay(date, false); H().toast('휴대폰·건강 데이터를 다시 읽고 있어요'); },
    emptyNote(date){
      if (api.loading(date)) return '휴대폰·건강 데이터를 확인하는 중이에요…';
      const any = (conf.weather && conf.loc) || (conf.health && (state.health === 'granted' || state.health === 'partial')) || (conf.phone && state.usage === 'granted')
        || (conf.calendar && state.calendar === 'granted') || (conf.move && state.tracking) || (conf.photos && (state.photos === 'granted' || state.photos === 'limited'));
      return any ? '이 날짜에 더 확인할 초안이 없어요.' : '‘연결 설정’에서 날씨·워치·캘린더·사진 등을 켜면 하루 초안이 자동으로 만들어져요.';
    },
    openSettings(){ H().setView('settings'); requestAnimationFrame(() => { const c = document.getElementById('nativeCard'); c && c.scrollIntoView({behavior:'smooth', block:'start'}); }); },
    async renderCard(box){
      if (box) cardBox = box;
      if (!cardBox) return;
      const el = H().el;
      cardBox.hidden = false;
      if (!state.checked) { cardBox.replaceChildren(el('h2', {style:'font-size:20px', text:'자동 기록 연결'}), el('p', {class:'hint', text:'연결 상태를 확인하는 중이에요…'})); await checkAll(); }
      const LOC = {granted:'허용됨', denied:'거부됨', prompt:'미설정', 'prompt-with-rationale':'미설정', off:'위치 꺼짐', unknown:'확인 중'};
      const HL = {granted:'연결됨', partial:'일부 연결', prompt:'미연결', unavailable:'사용 불가', unknown:'확인 중'};
      const US = {granted:'허용됨', prompt:'미허용', unavailable:'지원 안 됨', unknown:'확인 중'};
      const wxActs = [toggle('weather', '날씨')];
      if (conf.weather && state.location !== 'granted') wxActs.unshift(el('button', {type:'button', class:'btn sm primary', onclick:async () => {
        try { await weatherItem(H().todayStr(), true); } catch (e) { H().toast('위치를 가져오지 못했어요. 기기의 위치 서비스를 켜 주세요'); }
        await checkLocation(); cache.clear(); api.renderCard(); H().renderDraft(); }}, '위치 허용'));
      const hcActs = [toggle('health', '건강 앱')];
      if (state.health === 'unavailable') hcActs.unshift(el('button', {type:'button', class:'btn sm primary', onclick:() => Health.openHealthConnectSettings().catch(() => H().toast('Health Connect를 열지 못했어요'))}, 'Health Connect 설치·열기'));
      else if (conf.health && state.health !== 'granted') hcActs.unshift(el('button', {type:'button', class:'btn sm primary', onclick:async () => {
        try { await Health.requestAuthorization({read:HEALTH_READ}); } catch (e) { H().toast('권한 요청을 열지 못했어요'); }
        await checkHealth(); cache.clear(); api.renderCard(); H().renderDraft(); }}, '연결하기'));
      else if (state.health === 'granted') hcActs.push(el('button', {type:'button', class:'btn sm ghost', onclick:() => Health.openHealthConnectSettings().catch(() => {})}, '권한 관리'));
      const PM = {granted:'허용됨', limited:'일부 사진만', denied:'거부됨', prompt:'미허용', 'prompt-with-rationale':'미허용', unavailable:'지원 안 됨', unknown:'확인 중'};
      const askDay = (kind, then) => async () => {
        try { await Day.requestAccess({kind}); } catch (e) { H().toast('권한 요청을 열지 못했어요'); }
        await checkDay(); if (then) await then(); cache.clear(); api.renderCard(); H().renderDraft(); };
      const denied = k => state[k] === 'denied' ? el('button', {type:'button', class:'btn sm ghost', onclick:() => Day.openAppSettings().catch(() => {})}, '앱 설정 열기') : null;
      const calActs = [toggle('calendar', '캘린더')];
      if (conf.calendar && state.calendar !== 'granted' && state.calendar !== 'unavailable') calActs.unshift(el('button', {type:'button', class:'btn sm primary', onclick:askDay('calendar')}, '캘린더 허용'));
      const mvActs = [el('button', {type:'button', class:'btn sm', onclick:async () => {
        conf.move = !conf.move; save();
        try { if (conf.move && state.activity === 'granted') await Day.startMoveTracking(); else if (!conf.move) await Day.stopMoveTracking(); } catch (e) {}
        await checkDay(); cache.clear(); api.renderCard(); H().renderDraft(); }}, conf.move ? '이동 감지 끄기' : '이동 감지 켜기')];
      if (conf.move && state.activity !== 'granted' && state.activity !== 'unavailable') mvActs.unshift(el('button', {type:'button', class:'btn sm primary', onclick:askDay('activity', async () => {
        await checkDay(); if (state.activity === 'granted') { try { await Day.startMoveTracking(); } catch (e) { H().toast('이동 감지를 시작하지 못했어요: ' + (e.message || e)); } } })}, '신체 활동 허용'));
      else if (conf.move && state.activity === 'granted' && !state.tracking) mvActs.unshift(el('button', {type:'button', class:'btn sm primary', onclick:async () => {
        try { await Day.startMoveTracking(); } catch (e) { H().toast('이동 감지를 시작하지 못했어요: ' + (e.message || e)); } await checkDay(); api.renderCard(); }}, '이동 감지 시작'));
      const phoActs = [toggle('photos', '사진')];
      if (conf.photos && state.photos !== 'granted' && state.photos !== 'unavailable') phoActs.unshift(el('button', {type:'button', class:'btn sm primary', onclick:askDay('photos')}, state.photos === 'limited' ? '사진 더 고르기' : '사진 허용'));
      const phActs = [toggle('phone', '추정')];
      if (conf.phone && state.usage === 'prompt') phActs.unshift(el('button', {type:'button', class:'btn sm primary', onclick:() => Phone.openUsageAccessSettings().catch(() => H().toast('설정을 열지 못했어요'))}, '사용 정보 접근 허용'));
      cardBox.replaceChildren(...[
        el('h2', {style:'font-size:20px', text:'자동 기록 연결'}),
        el('p', {class:'hint', text:'켜 둔 항목은 ‘오늘 하루 초안’ 카드에 제안으로만 나타나고, ‘맞아요’를 눌러야 기록돼요.'}),
        row('날씨 자동 입력', '대략적 위치(약 1km)로 그날 날씨와 기온을 채워요. 최근 31일까지.', conf.weather ? LOC[state.location] || state.location : '꺼짐', conf.weather && state.location === 'granted', wxActs),
        row('워치·건강 앱', 'Health Connect에서 수면(취침·기상), 운동, 걸음 수를 읽어요. 삼성 헬스·Fitbit·구글 핏 등이 Health Connect에 기록해 둔 데이터예요.',
          conf.health ? HL[state.health] : '꺼짐', conf.health && state.health === 'granted', hcActs),
        state.health === 'unavailable' && state.healthReason ? el('p', {class:'hint', text:'Health Connect: ' + state.healthReason}) : null,
        row('휴대폰 사용으로 수면 추정', '밤사이 화면이 꺼져 있던 가장 긴 시간을 잠으로 추정해요. 워치 수면 기록이 없을 때만 써요. 어떤 앱을 썼는지는 읽지 않아요.',
          conf.phone ? US[state.usage] : '꺼짐', conf.phone && state.usage === 'granted', phActs),
        row('캘린더 일정', '휴대폰 캘린더(구글 캘린더 포함)에서 그날 일정의 제목·시간·장소를 읽어 초안으로 제안해요. 하루 종일 일정과 거절한 일정은 빼요.',
          conf.calendar ? PM[state.calendar] || state.calendar : '꺼짐', conf.calendar && state.calendar === 'granted', [...calActs, denied('calendar')].filter(Boolean)),
        row('이동 수단 감지', '걷기·달리기·자전거·차량 이동이 시작되고 끝난 시각만 휴대폰에 남겨요. 위치는 쓰지 않아요. 켠 뒤부터 기록돼요.',
          !conf.move ? '꺼짐' : state.tracking ? '감지 중' : PM[state.activity] || state.activity, conf.move && state.tracking, [...mvActs, denied('activity')].filter(Boolean)),
        row('사진', '그날 찍은 사진의 시각으로 “이때 뭐 했어요?” 초안을 만들고, 같은 시간대 일정·운동에는 사진을 붙여 줘요. 고른 사진만 작게 줄여 앱 안에 복사해요.',
          conf.photos ? PM[state.photos] || state.photos : '꺼짐', conf.photos && (state.photos === 'granted' || state.photos === 'limited'), [...phoActs, denied('photos')].filter(Boolean)),
        el('p', {class:'hint', style:'margin-top:8px'}, '데이터는 이 휴대폰 안에서만 읽고 저장해요. 외부로 나가는 건 날씨 조회용 대략적 위치뿐이에요. 캘린더 일정·사진은 ‘맞아요’를 누른 것만 기록에 남아요. ',
          el('a', {href:'privacypolicy.html', text:'개인정보 처리방침'}))
      ].filter(Boolean));
    },
    async ready(){
      const note = document.getElementById('storeNote');
      if (note) note.textContent = '기록은 이 휴대폰의 하루로그 앱 안에만 저장돼요. 앱을 삭제하거나 앱 데이터를 지우면 함께 지워지니, 설정의 백업을 가끔 만들어 두세요.';
      await checkAll();
      // 이동 감지는 앱이 다시 켜질 때마다 등록을 확인 (재부팅 후에는 BootReceiver 가 다시 등록)
      if (conf.move && state.activity === 'granted' && !state.tracking) { try { await Day.startMoveTracking(); await checkDay(); } catch (e) {} }
      fetchDay(H().sel, false);
    }
  };
  // 권한 화면(설정 앱·Health Connect)에서 돌아오면 상태를 다시 확인
  document.addEventListener('visibilitychange', async () => {
    if (document.visibilityState !== 'visible' || !H()) return;
    await checkAll(); cache.clear();
    if (cardBox && !cardBox.hidden && document.getElementById('view-settings') && !document.getElementById('view-settings').hidden) api.renderCard();
    fetchDay(H().sel, false);
  });
  window.HaruNative = api;
})();
