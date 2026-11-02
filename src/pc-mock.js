/* 하루로그 PC 테스트 모드
 * 앱(Capacitor)의 플러그인을 가짜로 흉내 내서, PC 브라우저에서 앱 버전 화면과 자동 기록 흐름을 그대로 확인한다.
 * 이 파일은 pc-test.html 에만 들어가고, 휴대폰 앱(www/)에는 들어가지 않는다.
 * 가짜 데이터: 날짜마다 같은 결과가 나오도록 날짜로 시드를 만든다.
 */
(() => {
  const KEY = 'harulog.pcmock';
  const st = (() => {
    const d = {location:'prompt', health:'prompt', usage:false, calendar:'prompt', photos:'prompt', activity:'prompt', tracking:false, scenario:'watch', hcInstalled:true};
    try { return Object.assign(d, JSON.parse(localStorage.getItem(KEY) || '{}')); } catch (e) { return d; }
  })();
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} };
  const SEOUL = {latitude:37.5665, longitude:126.978};

  // 날짜별 고정 난수
  const hash = s => { let h = 2166136261; for (let i = 0; i < s.length; i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; };
  const rng = seed => { let x = seed || 1; return () => { x ^= x << 13; x ^= x >>> 17; x ^= x << 5; return ((x >>> 0) % 10000)/10000; }; };
  const ymd = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const at = (s, h, m = 0) => { const [y, mo, d] = s.split('-').map(Number); return new Date(y, mo - 1, d, h, m); };
  const days = (a, b) => { const out = []; const d = new Date(a); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - 1); for (; d <= b; d.setDate(d.getDate() + 1)) out.push(ymd(d)); return out; };

  // 날짜 s 의 밤(그날 밤 잠들어 다음날 아침 깸)
  function night(s){
    const r = rng(hash('night' + s));
    const bed = at(s, 22, 30 + Math.floor(r()*10)*12);           // 22:30 ~ 00:18
    const wake = new Date(bed.getTime() + (6 + r()*2.5)*36e5);       // 6 ~ 8.5시간
    const awakeAt = new Date(bed.getTime() + (2 + r()*2)*36e5);
    return {bed, wake, awakeAt, awakeMin:Math.floor(r()*25)};
  }
  const nightsBetween = (a, b) => days(a, b).map(night).filter(n => n.wake > a && n.bed < b && n.wake <= new Date());

  const Health = {
    isAvailable: async () => st.hcInstalled ? {available:true, platform:'android'} : {available:false, platform:'android', reason:'Health Connect가 설치되지 않았어요 (PC 테스트)'},
    checkAuthorization: async () => st.health === 'granted' ? {readAuthorized:['sleep', 'steps', 'workouts'], readDenied:[]} : {readAuthorized:[], readDenied:['sleep', 'steps', 'workouts']},
    requestAuthorization: async () => { st.health = 'granted'; save(); note('Health Connect 권한을 허용한 것으로 처리했어요'); return {}; },
    openHealthConnectSettings: async () => { if (!st.hcInstalled){ st.hcInstalled = true; save(); note('Health Connect를 설치한 것으로 처리했어요'); back(); } else note('실제 폰에서는 Health Connect 권한 화면이 열려요'); },
    readSamples: async o => {
      if (st.scenario !== 'watch') return {samples:[]};
      const a = new Date(o.startDate), b = new Date(o.endDate), out = [];
      for (const n of nightsBetween(a, b)){
        const awakeEnd = new Date(n.awakeAt.getTime() + n.awakeMin*60e3);
        out.push({startDate:n.bed.toISOString(), endDate:n.awakeAt.toISOString(), sleepState:'light', value:0, unit:'minute'});
        if (n.awakeMin) out.push({startDate:n.awakeAt.toISOString(), endDate:awakeEnd.toISOString(), sleepState:'awake', value:0, unit:'minute'});
        out.push({startDate:awakeEnd.toISOString(), endDate:n.wake.toISOString(), sleepState:'deep', value:0, unit:'minute'});
      }
      return {samples:out};
    },
    queryWorkouts: async o => {
      if (st.scenario !== 'watch') return {workouts:[]};
      const s = ymd(new Date(o.startDate)), r = rng(hash('wk' + s));
      if (r() > .55) return {workouts:[]};
      const types = ['running', 'yoga', 'strengthTraining', 'cycling', 'walking', 'swimming'];
      const start = at(s, 7 + Math.floor(r()*13), Math.floor(r()*4)*15), dur = (20 + Math.floor(r()*50))*60;
      if (start > new Date()) return {workouts:[]};
      return {workouts:[{workoutType:types[Math.floor(r()*types.length)], duration:dur, startDate:start.toISOString(), endDate:new Date(start.getTime() + dur*1000).toISOString()}]};
    },
    queryAggregated: async o => {
      if (st.scenario !== 'watch') return {samples:[]};
      const s = ymd(new Date(o.startDate)), r = rng(hash('steps' + s)), now = new Date(), out = [];
      for (let h = 7; h < 22; h++){
        const t = at(s, h); if (t > now) break;
        out.push({startDate:t.toISOString(), endDate:at(s, h + 1).toISOString(), value:Math.floor(r()*(h === 12 || h === 18 ? 2400 : 700))});
      }
      return {samples:out};
    },
    showPrivacyPolicy: async () => { location.href = 'privacypolicy.html'; }
  };

  const Geolocation = {
    checkPermissions: async () => ({location:st.location, coarseLocation:st.location}),
    requestPermissions: async () => { st.location = 'granted'; save(); note('대략적 위치를 허용한 것으로 처리했어요 (서울 시청 기준)'); return {location:'granted', coarseLocation:'granted'}; },
    getCurrentPosition: async () => ({coords:Object.assign({accuracy:1500}, SEOUL), timestamp:Date.now()})
  };

  const PhoneSignals = {
    checkUsageAccess: async () => ({granted:!!st.usage, screenEventsSupported:true}),
    openUsageAccessSettings: async () => { setTimeout(() => { st.usage = true; save(); note('사용 정보 접근을 허용한 것으로 처리했어요'); back(); }, 400); },
    getScreenEvents: async o => {
      if (!st.usage || st.scenario === 'empty') return {events:[]};
      const a = new Date(o.start), b = new Date(o.end), ev = [];
      for (const s of days(a, b)){
        const n = night(s), r = rng(hash('scr' + s));
        // 낮에는 자주 켜고 끄고, 밤에는 잠깐 시계 확인 한 번
        const prev = new Date(at(s, 12)); prev.setDate(prev.getDate() - 1);
        for (let t = night(ymd(prev)).wake.getTime() + 15*60e3; t < n.bed.getTime() - 20*60e3; t += (25 + r()*60)*60e3){ ev.push({time:t, type:'on'}); ev.push({time:t + (2 + r()*15)*60e3, type:'off'}); }
        const off = n.bed.getTime() + 5*60e3; ev.push({time:off - 12*60e3, type:'on'}); ev.push({time:off, type:'off'}); // 자기 전 잠깐 사용
        ev.push({time:n.awakeAt.getTime(), type:'on'}); ev.push({time:n.awakeAt.getTime() + 60e3, type:'off'});
        ev.push({time:n.wake.getTime() + 4*60e3, type:'on'}); ev.push({time:n.wake.getTime() + 5*60e3, type:'unlock'});
      }
      return {events:ev.filter(e => e.time >= a && e.time <= b && e.time <= Date.now()).sort((x, y) => x.time - y.time)};
    }
  };

  // 날씨 서버에 못 닿을 때(오프라인·미리보기 페이지 등) 가짜 날씨로 대신 응답
  const realFetch = window.fetch.bind(window);
  window.fetch = async (url, opt) => {
    const u = String(url);
    if (!u.includes('api.open-meteo.com')) return realFetch(url, opt);
    try { const r = await realFetch(url, opt); if (r.ok) return r; throw 0; }
    catch (e) {
      const t = [], code = [], mx = [], mn = [], wd = [], now = new Date();
      for (let i = 31; i >= 0; i--){
        const d = new Date(now); d.setDate(d.getDate() - i); const s = ymd(d), r = rng(hash('wx' + s)), m = d.getMonth() + 1;
        const base = [0, -2, 1, 7, 13, 18, 22, 26, 26, 21, 14, 7, 1][m];
        t.push(s); code.push([0, 1, 2, 3, 61, 63, 45, 80, m <= 2 || m === 12 ? 71 : 1][Math.floor(r()*9)]);
        mx.push(base + 4 + r()*4); mn.push(base - 4 - r()*3); wd.push(5 + r()*30);
      }
      note('날씨 서버에 연결하지 못해 가짜 날씨를 보여 줘요');
      return new Response(JSON.stringify({daily:{time:t, weather_code:code, temperature_2m_max:mx, temperature_2m_min:mn, wind_speed_10m_max:wd}}), {headers:{'content-type':'application/json'}});
    }
  };

  /* 캘린더·이동·사진 (DayData) */
  const CAL = [['팀 회의', '회의실 3층', 'work'], ['점심 약속 (민수)', '을지로', ''], ['수업: 데이터 분석', '온라인', ''], ['치과 예약', '연세치과', ''], ['요가 클래스', '동네 요가원', ''], ['스터디 모임', '스타벅스 시청점', ''], ['저녁 약속', '성수동', '']];
  function events(s){
    const r = rng(hash('cal' + s)), wd = at(s, 12).getDay(), out = [];
    const n = st.scenario === 'empty' ? 0 : wd === 0 || wd === 6 ? Math.floor(r()*2) : 1 + Math.floor(r()*3);
    const used = new Set();
    for (let i = 0; i < n; i++){
      let k = Math.floor(r()*CAL.length); if (used.has(k)) continue; used.add(k);
      const h = [10, 12, 14, 16, 19][Math.floor(r()*5)], b = at(s, h, r() < .5 ? 0 : 30), len = (k === 1 || k === 6 ? 90 : 60)*60e3;
      out.push({id:100 + k, title:CAL[k][0], begin:b.getTime(), end:b.getTime() + len, allDay:false, location:CAL[k][1], calendar:'내 캘린더'});
    }
    if (r() < .2) out.push({id:999, title:'엄마 생신', begin:at(s, 0).getTime(), end:at(s, 24).getTime(), allDay:true, location:'', calendar:'가족'});
    return out.sort((x, y) => x.begin - y.begin);
  }
  function transitions(s){
    if (st.scenario === 'empty') return [];
    const r = rng(hash('mv' + s)), n = night(ymd(new Date(at(s, -12)))), out = [];
    const seg = (act, a, min) => { out.push({time:a.getTime(), activity:act, kind:'enter'}); out.push({time:a.getTime() + min*60e3, activity:act, kind:'exit'}); };
    const leave = new Date(n.wake.getTime() + (50 + r()*30)*60e3);
    seg('walking', leave, 6); seg('vehicle', new Date(leave.getTime() + 7*60e3), 25 + Math.floor(r()*20));
    if (r() < .6) seg('walking', at(s, 12, 20), 18);
    const home = at(s, 18, Math.floor(r()*50)); seg('vehicle', home, 20 + Math.floor(r()*25));
    if (r() < .35) seg('bicycle', at(s, 20, 10), 22);
    if (r() < .3) seg('running', at(s, 21), 25);
    return out;
  }
  const COLORS = [['#F6C28B', '#E9866E'], ['#9FD3C7', '#4E8F8B'], ['#C3B6F2', '#7A6BC2'], ['#F7E39A', '#E2A93B'], ['#A9CDEB', '#4F7FB6'], ['#F2B5C4', '#C9667F']];
  function photos(s){
    if (st.scenario === 'empty') return [];
    const r = rng(hash('ph' + s)), out = [];
    const shoot = (h, m, n) => { for (let i = 0; i < n; i++){ const t = at(s, h, m + i*(2 + Math.floor(r()*6))); out.push({id:String(hash(s + h + m + i) % 1e9), time:t.getTime(), width:1600, height:1200, screenshot:false}); } };
    const ev = events(s); if (ev.length && r() < .8){ const e = ev[Math.floor(r()*ev.length)]; if (!e.allDay){ const d = new Date(e.begin); shoot(d.getHours(), d.getMinutes() + 10, 2 + Math.floor(r()*3)); } }
    if (r() < .7) shoot(15, 20, 1 + Math.floor(r()*4));
    if (r() < .5) shoot(19, 40, 1 + Math.floor(r()*2));
    out.push({id:'7' + hash(s), time:at(s, 11, 5).getTime(), width:1080, height:2340, screenshot:true});
    return out.filter(p => p.time <= Date.now());
  }
  function photoData(id, max){
    const c = document.createElement('canvas'), w = Math.min(max, 640), h = Math.round(w*.75); c.width = w; c.height = h;
    const g = c.getContext('2d'), [c1, c2] = COLORS[Number(id) % COLORS.length], gr = g.createLinearGradient(0, 0, w, h);
    gr.addColorStop(0, c1); gr.addColorStop(1, c2); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = 'rgba(255,255,255,.35)'; g.beginPath(); g.arc(w*.72, h*.3, h*.16, 0, 7); g.fill();
    g.fillStyle = 'rgba(0,0,0,.12)'; g.beginPath(); g.moveTo(0, h); g.lineTo(w*.35, h*.45); g.lineTo(w*.6, h*.75); g.lineTo(w*.8, h*.55); g.lineTo(w, h); g.fill();
    g.fillStyle = 'rgba(255,255,255,.9)'; g.font = `bold ${Math.round(h*.09)}px system-ui,sans-serif`; g.fillText('PC 테스트 사진', w*.06, h*.16);
    return c.toDataURL('image/jpeg', .8);
  }
  const DayData = {
    checkAccess: async () => ({calendar:st.calendar, photos:st.photos, activity:st.activity, tracking:!!st.tracking && st.activity === 'granted'}),
    requestAccess: async ({kind}) => { st[kind] = 'granted'; save(); note({calendar:'캘린더', photos:'사진', activity:'신체 활동'}[kind] + ' 권한을 허용한 것으로 처리했어요'); return DayData.checkAccess(); },
    openAppSettings: async () => note('실제 폰에서는 앱 설정 화면이 열려요'),
    getEvents: async ({start, end}) => ({events:days(new Date(start), new Date(end)).flatMap(events).filter(e => e.begin < end && e.end > start)}),
    getPhotos: async ({start, end}) => ({photos:days(new Date(start), new Date(end)).flatMap(photos).filter(p => p.time >= start && p.time < end)}),
    getPhoto: async ({id, max}) => ({dataUrl:photoData(id, max || 640)}),
    startMoveTracking: async () => { st.tracking = true; save(); note('이동 감지를 시작했어요 (PC 테스트는 지난 날짜도 가짜 기록이 있어요)'); },
    stopMoveTracking: async () => { st.tracking = false; save(); },
    getTransitions: async ({start, end}) => ({transitions:days(new Date(start), new Date(end)).flatMap(transitions).filter(t => t.time >= start && t.time <= end && t.time <= Date.now())})
  };

  const plugins = {Health, Geolocation, PhoneSignals, DayData};
  window.Capacitor = {
    isNativePlatform: () => true, getPlatform: () => 'android', isPluginAvailable: n => n in plugins,
    registerPlugin: n => plugins[n] || new Proxy({}, {get: () => async () => { throw new Error(n + ' 은 PC 테스트에서 지원하지 않아요'); }}),
    Plugins: plugins
  };

  // 권한 화면에서 돌아온 것처럼 알림 (native.js 가 상태를 다시 확인)
  function back(){ document.dispatchEvent(new Event('visibilitychange')); }
  let lastNote = '';
  function note(msg){
    if (msg === lastNote) return; lastNote = msg; setTimeout(() => { lastNote = ''; }, 3000);
    if (window.Haru) window.Haru.toast('PC 테스트 · ' + msg); else console.info('[PC 테스트]', msg);
  }

  /* ---------- 화면 아래 PC 테스트 패널 ---------- */
  function panel(){
    const box = document.createElement('div');
    box.className = 'pcmock';
    box.innerHTML = `
      <style>
        .pcmock{position:fixed;right:12px;bottom:12px;z-index:60;font:13px/1.45 system-ui,sans-serif;color:#3A2E25}
        .pcmock>button{border:0;border-radius:999px;padding:8px 14px;background:#3A2E25;color:#F7F1E8;font-weight:700;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.25)}
        .pcmock .pm{display:none;position:absolute;right:0;bottom:44px;width:min(300px,calc(100vw - 24px));background:#FFFDF8;border:1px solid #E6DACB;border-radius:14px;padding:12px 14px;box-shadow:0 10px 30px rgba(0,0,0,.2)}
        .pcmock.open .pm{display:block}
        .pcmock b{display:block;font-size:14px;margin-bottom:4px}
        .pcmock p{margin:0 0 8px;color:#7A6A5A}
        .pcmock label{display:block;margin:6px 0 2px;font-weight:600}
        .pcmock select,.pcmock .pb{width:100%;padding:6px 8px;border:1px solid #E6DACB;border-radius:8px;background:#fff;font:inherit;color:inherit}
        .pcmock .pb{margin-top:8px;cursor:pointer}
        .pcmock .st{margin-top:8px;font-size:12px;color:#7A6A5A}
      </style>
      <button type="button" aria-expanded="false">PC 테스트 모드</button>
      <div class="pm" role="dialog" aria-label="PC 테스트 설정">
        <b>PC 테스트 모드</b>
        <p>휴대폰 권한·워치·캘린더·이동·사진 데이터를 가짜로 흉내 내요. 날씨는 서울 기준 실제 날씨(연결 안 되면 가짜)예요. 휴대폰 앱에는 이 패널이 없어요.</p>
        <label for="pmScn">데이터 상황</label>
        <select id="pmScn">
          <option value="watch">워치 있음 (수면·운동·걸음)</option>
          <option value="phone">워치 없음 (휴대폰 사용만)</option>
          <option value="empty">데이터 없음</option>
        </select>
        <label for="pmHc">Health Connect</label>
        <select id="pmHc"><option value="1">설치됨</option><option value="0">미설치 (Android 13 이하)</option></select>
        <button type="button" class="pb" id="pmReset">권한 처음 상태로 (모두 미허용)</button>
        <button type="button" class="pb" id="pmGrant">권한 모두 허용</button>
        <div class="st" id="pmSt"></div>
      </div>`;
    document.body.append(box);
    const $ = id => box.querySelector('#' + id), tog = box.querySelector('button');
    const show = () => { const y = v => v === 'granted' || v === true ? '허용' : '미허용'; $('pmSt').textContent = `위치 ${y(st.location)} · 건강 ${y(st.health)} · 사용 정보 ${y(st.usage)} · 캘린더 ${y(st.calendar)} · 사진 ${y(st.photos)} · 이동 ${st.tracking ? '감지 중' : '꺼짐'}`; $('pmScn').value = st.scenario; $('pmHc').value = st.hcInstalled ? '1' : '0'; };
    tog.onclick = () => { const o = box.classList.toggle('open'); tog.setAttribute('aria-expanded', String(o)); show(); };
    const apply = msg => { save(); show(); back(); if (msg) note(msg); };
    $('pmScn').onchange = e => { st.scenario = e.target.value; apply('데이터 상황을 바꿨어요'); };
    $('pmHc').onchange = e => { st.hcInstalled = e.target.value === '1'; if (!st.hcInstalled) st.health = 'prompt'; apply(); };
    $('pmReset').onclick = () => { Object.assign(st, {location:'prompt', health:'prompt', usage:false, calendar:'prompt', photos:'prompt', activity:'prompt', tracking:false}); try { const n = JSON.parse(localStorage.getItem('harulog.native') || '{}'); delete n.loc; localStorage.setItem('harulog.native', JSON.stringify(n)); } catch (e) {} apply('권한을 처음 상태로 돌렸어요'); location.reload(); };
    $('pmGrant').onclick = () => { Object.assign(st, {location:'granted', health:'granted', usage:true, calendar:'granted', photos:'granted', activity:'granted', tracking:true, hcInstalled:true}); apply('권한을 모두 허용했어요'); };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', panel); else panel();
})();
