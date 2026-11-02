"""하루로그 마을 확장(v2) 그림 데이터 만들기
design/village-v2 의 catalog.json · furniture/*.svg · scenery/*.svg · generator/*.py 를 읽어
앱이 바로 그릴 수 있는 '그리기 명령(ops)' JSON 으로 바꾸고, src/harulog.html 의 VILLAGE-ASSETS 블록에 넣는다.

  사용: python3 scripts/build-village-assets.py   (그 다음 npm run build)

ops 형식 (논리 단위 좌표, 기준점은 각 그림의 (0,0))
  [0,x,y,w,h,rx,fill,stroke,sw,dash]   사각형
  [1,cx,cy,rx,ry,fill,stroke,sw,dash]  타원
  [2,d,fill,stroke,sw,dash]            path
  [3,x1,y1,x2,y2,stroke,sw]            선
  [4,text,x,y,size,fill,anchor,base]   글자
  [5,tx,ty,ops]                        이동한 묶음
"""
import json, math, os, re, sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = os.path.join(ROOT, 'design', 'village-v2')
sys.path.insert(0, os.path.join(V2, 'generator'))
import art, scenery  # noqa: E402
from art import rect, ell, path, line, tree, shade  # noqa: E402

NUM = lambda v: round(float(v), 2)
def col(v):
    if v is None or v == 'none': return 0
    return v

def compile_svg(markup):
    """SVG 조각(문자열) → ops 배열"""
    root = ET.fromstring('<g xmlns="http://www.w3.org/2000/svg">' + markup + '</g>')
    return walk(root)

TR = re.compile(r'translate\(\s*([-\d.e]+)[ ,]+([-\d.e]+)\s*\)')
def walk(node):
    ops = []
    for el in node:
        tag = el.tag.split('}')[-1]; a = el.attrib
        st, sw = col(a.get('stroke')), NUM(a.get('stroke-width', 0)) if a.get('stroke') not in (None, 'none') else 0
        dash = [NUM(x) for x in re.split(r'[ ,]+', a['stroke-dasharray'].strip())] if a.get('stroke-dasharray') else 0
        if tag == 'rect':
            ops.append([0, NUM(a.get('x', 0)), NUM(a.get('y', 0)), NUM(a['width']), NUM(a['height']), NUM(a.get('rx', 0)), col(a.get('fill', '#000')), st, sw, dash])
        elif tag == 'ellipse':
            ops.append([1, NUM(a['cx']), NUM(a['cy']), NUM(a['rx']), NUM(a['ry']), col(a.get('fill', '#000')), st, sw, dash])
        elif tag == 'circle':
            ops.append([1, NUM(a['cx']), NUM(a['cy']), NUM(a['r']), NUM(a['r']), col(a.get('fill', '#000')), st, sw, dash])
        elif tag == 'path':
            d = re.sub(r'(\d\.\d\d)\d+', r'\1', a['d'])
            ops.append([2, d, col(a.get('fill', '#000')), st, sw, dash])
        elif tag == 'line':
            ops.append([3, NUM(a['x1']), NUM(a['y1']), NUM(a['x2']), NUM(a['y2']), st or '#000', sw or 1])
        elif tag == 'text':
            ops.append([4, el.text or '', NUM(a.get('x', 0)), NUM(a.get('y', 0)), NUM(a.get('font-size', 6)), col(a.get('fill', '#000')),
                        a.get('text-anchor', 'start'), 'middle' if a.get('dominant-baseline') == 'middle' else 'alphabetic'])
        elif tag in ('g', 'svg'):
            m = TR.search(a.get('transform', ''))
            sub = walk(el)
            if a.get('transform', '').startswith('scale(-1'): ops.append([6, sub])
            elif m: ops.append([5, NUM(m.group(1)), NUM(m.group(2)), sub])
            else: ops.extend(sub)
    return ops

def svg_file(rel):
    s = open(os.path.join(V2, rel), encoding='utf-8').read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1).split()
    inner = s[s.index('>') + 1: s.rindex('</svg>')]
    return compile_svg(inner), [NUM(v) for v in vb]

cat = json.load(open(os.path.join(V2, 'catalog.json'), encoding='utf-8'))
OUT = {'furniture': {}, 'scenery': {}, 'sprites': {}, 'bands': {}, 'rooms': cat['rooms']}

# ---- 가구 84종
for kind, v in cat['furniture'].items():
    items = []
    for it in v['items']:
        ops, vb = svg_file(it['svg'])
        items.append({'k': it['key'], 'label': it['label'], 'fp': it['footprint'], 'bbox': it['bbox'], 'solid': bool(it['solid']),
                      'sr': it.get('solidRect'), 'spot': it.get('spot'), 'ops': ops})
    OUT['furniture'][kind] = {'label': v['label'], 'items': items}

# ---- 테마 배경 요소 (소품·움직이는 요소)
for th, v in cat['scenery'].items():
    for it in v['items']:
        ops, vb = svg_file(it['svg'])
        OUT['scenery'].setdefault(th, {})[it['key']] = {'label': it['label'], 'bbox': it['bbox'], 'anchor': it['anchor'], 'ops': ops}

# ---- 움직이는 요소용 변형 (차 색·방향, 풍차 몸통)
SPR = OUT['sprites']
for name, svg in {
    'sedan_red': scenery.car_side('#E06A52', 1), 'sedan_blue': scenery.car_side('#8CB8E0', 1), 'sedan_purple': scenery.car_side('#B7A1D9', 1),
    'sedan_green': scenery.car_side('#6FA387', 1), 'taxi': scenery.car_side('#F7D07A', 1, 'taxi'), 'bus': scenery.car_side('#6FA387', 1, 'bus'),
    'truck': scenery.car_side('#2F6FA8', 1, 'truck'), 'front_red': scenery.car_front('#E06A52'), 'back_green': scenery.car_front('#6FA387', True),
    'front_blue': scenery.car_front('#8CB8E0'), 'back_yellow': scenery.car_front('#F7D07A', True),
    'windmill_body': scenery.windmill(0).split('<path d="M0,-42')[0].replace(ell(0, -42, 2, 2, "#7A5A42", art.OL, 0.4), ''),
}.items():
    SPR[name] = compile_svg(svg)

# ---- 테마 배경 띠 (고정 그림). 지도 폭 3종 × 테마 4종. 좌표는 지도 좌표(위 띠 = 음수 y, 아래 띠 = 지도 높이부터)
BANDS = {'city': (150, 80), 'forest': (120, 70), 'coast': (80, 150), 'village': (140, 74)}
COMPS = {}
def comp(name, svg):
    """고정 그림 조각을 한 번만 저장하고 [이름, x, y] 로 배치한다"""
    if name not in COMPS: COMPS[name] = compile_svg(svg)
    return name
def T_(kind, s=1.0): s = round(s, 2); return comp(f'tree_{kind}_{s}', tree(0, 0, kind, s))

def tower(w, h, body, glass, kind, seed, night):
    # scenery.tower 와 같은 그림. 밤에는 켜진 창 비율 20% → 60%
    out = rect(4, -6, w, 8, "rgba(40,50,60,.18)", 2) + rect(0, -h, w, h, body, 2, art.OL, 0.6)
    out += path(f"M{w},{-h} l8,-6 l0,{h} l-8,6 Z", shade(body, -0.2), art.OL, 0.5) + path(f"M0,{-h} l8,-6 l{w},0 l-8,6 Z", shade(body, 0.2), art.OL, 0.5)
    cols = max(2, int(w / 11)); rows = int((h - 22) / 13)
    for r in range(rows):
        for c in range(cols):
            lit = (r * 7 + c * 3 + seed) % 5 in ((0, 1, 2) if night else (0,))
            x = 4 + c * (w - 8) / cols; y = -h + 8 + r * 13; win = '#FFE9A8' if lit else glass
            if kind == 'glass': out += rect(x, y, (w - 8) / cols - 2, 10, win, 0.6) + line(x + 1, y + 8, x + 4, y + 2, "rgba(255,255,255,.5)", 0.6)
            elif kind == 'brick': out += rect(x + 1, y + 1, (w - 8) / cols - 4, 8, win if lit else '#DCEAF2', 0.6, art.OL, 0.3) + rect(x, y + 9, (w - 8) / cols - 2, 1.4, shade(body, -0.25))
            else: out += rect(x, y + 2, (w - 8) / cols - 2, 6, win, 0.4)
    out += rect(w / 2 - 7, -14, 14, 14, "#4F5560", 1, art.OL, 0.45) + rect(w / 2 - 6, -13, 5.4, 12, "#BFE3F2", 0.4) + rect(w / 2 + 0.6, -13, 5.4, 12, "#BFE3F2", 0.4)
    return out + rect(-2, -16, w + 4, 3, shade(body, -0.3), 1)
SPECS = [(60, 140, "#9FB7C9", "glass", "antenna"), (52, 100, "#D9A27E", "brick", "tank"), (70, 120, "#B7C3CC", "office", "sign"), (48, 86, "#E3C9A8", "brick", "tank"),
         (64, 132, "#8FA9C2", "glass", ""), (56, 108, "#C9B7D9", "office", "antenna"), (60, 94, "#D9A27E", "brick", "tank")]
for i, (w, h, c, k, roof) in enumerate(SPECS):
    for night in (0, 1): comp(f'tower{i}{"n" if night else ""}', tower(w, h, c, "#CFE3EE", k, i, night) + scenery.tower_roof(w, h, roof))

def band(th, W):
    """flat: 바닥 그림 ops (지도 폭에 맞춤), items: [조각 이름, x, y] (y 순)"""
    T, B = BANDS[th]
    H = 2 * 224 + 24 + (64 if th == 'coast' else 0)
    cols = (W - 24) // 344
    sx = lambda x: round(x * W / 1056, 1)
    vx = [24 + c * 344 + 322 for c in range(cols - 1)] or [W / 2]
    flat, it = '', []
    Y = lambda y: y - T
    S = lambda name, svg, x, y, z=None: it.append((y if z is None else z, comp(name, svg), round(x, 1), round(y, 1)))
    if th == 'city':
        flat += rect(0, Y(0), W, T, "#C5CBD1") + rect(0, Y(T - 22), W, 22, "#B9BDC2") + rect(0, Y(T - 22), W, 1.2, "#9EA3A9")
        x, i = -6, 0
        while x < W:
            it.append((Y(T - 22), f'tower{i % 7}', x, Y(T - 22))); x += SPECS[i % 7][0] + 14; i += 1
        S('billboard', scenery.billboard(), sx(120), Y(T - 6)); S('subway', scenery.subway(), sx(520), Y(T - 4)); S('kiosk', scenery.kiosk(), sx(830), Y(T - 4))
        by = H
        flat += rect(0, by + 10, W, 50, "#5D636A") + rect(0, by + 6, W, 4, "#B9BDC2") + rect(0, by + 60, W, 4, "#B9BDC2") + rect(0, by + 64, W, B - 64, "#C5CBD1")
        flat += ''.join(rect(xx, by + 34.4, 14, 1.2, "#F2EFE6", 0.6) for xx in range(4, W, 26))
        S('foodtruck', scenery.foodtruck(), sx(470), by + 4, by + 8)
    elif th == 'forest':
        flat += f'<g transform="translate(-10,{Y(40)})">{scenery.stream(W + 20, 36)}</g>'
        S('waterfall', scenery.waterfall(), sx(70), Y(60), Y(76)); S('bridge', scenery.bridge(), vx[min(1, len(vx) - 1)] + 10, Y(60)); S('tent', scenery.tent(), sx(520), Y(112))
        S('meadow90', scenery.meadow(90, 30), sx(300), Y(24), Y(30)); S('meadow70', scenery.meadow(70, 24), sx(880), Y(26)); S('meadow80', scenery.meadow(80, 26), sx(760), Y(108), Y(118))
        S('birdhouse', scenery.birdhouse(), sx(1010), Y(30)); S('owl', scenery.owl(), sx(640), Y(110))
        for x in range(10, W, 46):
            if abs(x - sx(70)) > 30: it.append((Y(26), T_('pine', 0.9 + (x % 3) * 0.08), x, Y(26)))
        by = H
        for x in range(14, W, 40): it.append((by + 66, T_('pine', 1.0), x, by + 66))
        S('berrybush', scenery.berrybush(), sx(160), by + 30); S('berrybush', scenery.berrybush(), sx(700), by + 34); S('meadow60', scenery.meadow(60, 20), sx(520), by + 30)
    elif th == 'coast':
        flat += rect(0, Y(0), W, T, "#F4E6C2")
        S('beachhut', scenery.beachhut(), sx(120), Y(60)); S('beachhut', scenery.beachhut(), sx(160), Y(62)); S('volleyball', scenery.volleyball(), sx(420), Y(62))
        it += [(Y(40), T_('palm'), sx(260), Y(40)), (Y(44), T_('palm'), sx(620), Y(44)), (Y(64), T_('palm'), sx(980), Y(50))]
        S('fishstall', scenery.fishstall(), sx(820), Y(64)); S('fishcrates', scenery.fishcrates(), sx(900), Y(66))
        sy = H
        flat += rect(0, sy - 2, W, B + 2, "#5FB0D8") + rect(0, sy - 2, W, 20, "#7CC4E4")
        flat += ''.join(path(f"M{(i*83)%W},{sy+20+(i*29)%(B-30)} q4,-2.4 8,0", "none", "rgba(255,255,255,.55)", 0.9) for i in range(int(40 * W / 1056)))
        S('pier', scenery.pier(), sx(200), sy - 40, sy - 10); S('fishcrates', scenery.fishcrates(), sx(200) + 40, sy - 34); S('lighthouse', scenery.lighthouse(), W - 70, sy + 60)
    else:
        S('field_cab110', scenery.field(110, 48, "cabbage"), sx(30), Y(20)); S('field_car84', scenery.field(84, 40, "carrot"), sx(160), Y(24), Y(20))
        S('field_wh120', scenery.field(120, 48, "wheat"), sx(600), Y(18), Y(20)); S('field_cab60', scenery.field(60, 32, "cabbage"), sx(900), Y(20), Y(70))
        S('barn', scenery.barn(), sx(360), Y(110)); S('pumpkins', scenery.pumpkins(), sx(960), Y(80)); S('beehive', scenery.beehive(), sx(900), Y(120))
        S('tractor', scenery.tractor(), sx(700), Y(120)); it += [(Y(100), T_('round'), 10, Y(100)), (Y(100), T_('round'), W - 16, Y(100))]
        by = H
        flat += f'<g transform="translate(-10,{by + 26})">{scenery.stream(W + 20, 30)}</g>'
        S('stepstones', scenery.stepstones(), vx[0] + 10, by + 40, by + 42); S('laundry', scenery.laundry(), sx(200), by + 22); S('jangdok', scenery.jangdok(), sx(500), by + 22)
        S('mailbox', scenery.mailbox(), sx(640), by + 22); it.append((by + 24, T_('round'), sx(760), by + 24)); S('persimmon', scenery.persimmon(), sx(940), by + 24)
    it.sort(key=lambda z: z[0])
    return {'flat': compile_svg(flat), 'items': [[n, x, y] for _, n, x, y in it]}

for th in BANDS:
    OUT['bands'][th] = {'T': BANDS[th][0], 'B': BANDS[th][1]}
    for W in (712, 1056, 1400): OUT['bands'][th][str(W)] = band(th, W)
OUT['comps'] = COMPS

js = json.dumps(OUT, ensure_ascii=False, separators=(',', ':'))
block = '<script id="villageAssets">\n/* 자동 생성: scripts/build-village-assets.py (design/village-v2) — 직접 고치지 마세요 */\nwindow.HARU_VILLAGE = ' + js + ';\n</script>'
p = os.path.join(ROOT, 'src', 'harulog.html')
s = open(p, encoding='utf-8').read()
if '<script id="villageAssets">' in s:
    i = s.index('<script id="villageAssets">'); j = s.index('</script>', i) + len('</script>')
    s = s[:i] + block + s[j:]
else:
    i = s.index('<script>', s.index('<script>') + 1)   # 앱 스크립트 바로 앞 (아바타 키트 다음)
    s = s[:i] + block + '\n' + s[i:]
open(p, 'w', encoding='utf-8').write(s)
print(f'village assets: {len(js)//1024} KB → src/harulog.html')
