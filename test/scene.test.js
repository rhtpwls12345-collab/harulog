// 기록 → 장면: 키워드 동작, 반려동물 등록·동행, 함께한 사람, 말풍선, 폼 수동 지정
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 1200 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('https://fonts.googleapis.com/**', r => r.abort());
  await p.goto('file://' + path.resolve(__dirname, '../www/index.html')); await p.waitForTimeout(700);
  // 반려동물 등록
  await p.click('#tab-settings'); console.log('pet body hidden before answer', await p.$eval('#petBody', e => e.hidden));
  await p.click('#petHas button[data-v=no]'); console.log('no → hidden', await p.$eval('#petBody', e => e.hidden), await p.evaluate(() => window.Haru.data.profile.petsOn));
  await p.click('#petHas button[data-v=yes]'); console.log('yes → shown', !(await p.$eval('#petBody', e => e.hidden)));
  await (await p.$('#petCard')).screenshot({ path: path.resolve(__dirname, 'scene-pets-empty.png') });
  await p.fill('#petName', '콩이'); await p.click('#petKind button:has-text("강아지")'); await p.click('#petBreed .chip:has-text("시바")'); await p.click('#petColor .swatch >> nth=0'); await p.click('#petAddBtn');
  await p.fill('#petName', '나비'); await p.click('#petKind button:has-text("고양이")'); await p.click('#petBreed .chip:has-text("턱시도")'); await p.click('#petColor .swatch >> nth=2'); await p.click('#petGear .chip:has-text("하네스")'); await p.click('#petAddBtn'); await p.waitForTimeout(200);
  // 수정: 나비 → 삼색
  await p.click('#petList .pet-row >> nth=1 >> button:has-text("수정")'); await p.click('#petBreed .chip:has-text("삼색")'); await p.click('#petAddBtn'); await p.waitForTimeout(200);
  console.log('pet data', JSON.stringify(await p.evaluate(() => window.Haru.data.profile.pets.map(({name, kind, breed, color, gear}) => ({name, kind, breed, color, gear})))));
  console.log('pets', await p.evaluate(() => window.Haru.data.profile.pets.map(x => x.name + ':' + x.kind).join(',')), 'rows', await p.$$eval('#petList .pet-row', r => r.length));
  
  await (await p.$('#petCard')).screenshot({ path: path.resolve(__dirname, 'scene-pets.png') });
  const add = async (type, title, raw, people) => {
    await p.click('#tab-today'); await p.click('#btnAdd'); await p.click('#ft-' + type, { force: true }); await p.fill('#fTitle', title); if (raw) await p.fill('#fRaw', raw); if (people) await p.fill('#fPeople', people);
    await p.waitForTimeout(100);
    const ui = await p.evaluate(() => ({motion: document.querySelector('#fMotion .chip[aria-pressed=true]')?.textContent, motionHidden: document.querySelector('#fMotionWrap').hidden, pets:[...document.querySelectorAll('#fPets .chip[aria-pressed=true]')].map(x => x.textContent)}));
    await p.click('#actForm button[type=submit]'); await p.waitForTimeout(250); return ui;
  };
  console.log('form strength', JSON.stringify(await add('exercise', '헬스장 하체 운동', '스쿼트 5세트 했다')));
  console.log('form walk', JSON.stringify(await add('walk', '콩이랑 산책', '날씨 좋아서 한강까지 걸었다')));
  console.log('form meal', JSON.stringify(await add('meal', '점심', '오늘 점심 최고였다', '민수, 지아')));
  // 수동 지정: 요가 칩을 고르고 저장 → scene.m
  await p.click('#btnAdd'); await p.click('#ft-exercise', { force: true }); await p.fill('#fTitle', '운동'); await p.click('#fMotion .chip[data-m=yoga]'); await p.click('#fPets .chip >> nth=0');
  await (await p.$('#fSceneWrap')).screenshot({ path: path.resolve(__dirname, 'scene-form.png') });
  await p.click('#actForm button[type=submit]'); await p.waitForTimeout(200);
  console.log('manual scene', JSON.stringify(await p.evaluate(() => window.Haru.data.days[window.Haru.sel].activities.at(-1).scene)));
  const play = async (i, ms, name) => {
    await p.click(`#actList .act >> nth=${i}`); await p.waitForTimeout(ms);
    const st = await p.evaluate(() => { const H = window.Haru._world, a = H.actor;
      return {pose:a.spot?.pose, item:a.spot?.item, motion:a.spot?.motion, arrived:a.arrived, comps:[...H.companions.entries()].map(([k, c]) => `${k}:${c.active ? 'on' : 'home'}`),
        tags:[...document.querySelectorAll('.stage-view .tag')].filter(t => !t.hidden && t.textContent).map(t => t.className + '=' + t.textContent)}; });
    console.log(name, JSON.stringify(st)); await (await p.$('.stage-view')).screenshot({ path: path.resolve(__dirname, `scene-${name}.png`) });
  };
  await play(0, 5000, 'strength'); await play(1, 6000, 'walk'); await play(2, 6500, 'meal'); await play(3, 5000, 'manual');
  await (await p.$('#mvCard')).screenshot({ path: path.resolve(__dirname, 'scene-mvcard.png') }).catch(() => console.log('mvCard hidden'));
  // 아니요 → 마을에서 반려동물 빠짐, 다시 예 → 돌아옴
  await p.click('#tab-settings'); await p.click('#petHas button[data-v=no]'); await p.click('#tab-today'); await p.click('#actList .act >> nth=1'); await p.waitForTimeout(800);
  console.log('pets off comps', await p.evaluate(() => [...window.Haru._world.companions.keys()].filter(k => k.startsWith('pet:')).length));
  console.log('ERR', errs); await b.close();
})();
