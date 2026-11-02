"""하루로그 팝업 건물 그림 데이터 만들기
design/popup (Claude Design 결과물)의 catalog.json · furniture/*/*.svg · exterior/*.svg · lifecycle/*.svg 를
앱이 바로 그릴 수 있는 그리기 명령(ops)으로 바꾸고 src/harulog.html 의 popupAssets 블록에 넣는다.

  사용: python3 scripts/build-popup-assets.py   (그 다음 node scripts/build-www.mjs)

ops 형식은 build-scene-assets.py 와 같고, 아래가 더해진다.
  [10,[x,y,w,h],ops]   잘라 그리기(clipPath) 묶음
"""
import json, math, os, re
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PD = os.path.join(ROOT, 'design', 'popup')
NUM = lambda v: round(float(v), 2)

def mat_mul(m, n):
    a, b, c, d, e, f = m; A, B, C, D, E, F = n
    return [a*A + c*B, b*A + d*B, a*C + c*D, b*C + d*D, a*E + c*F + e, b*E + d*F + f]

def parse_tf(s):
    m = [1, 0, 0, 1, 0, 0]
    for name, args in re.findall(r'(\w+)\(([^)]*)\)', s or ''):
        v = [float(x) for x in re.split(r'[ ,]+', args.strip()) if x]
        if name == 'translate': n = [1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0]
        elif name == 'scale': n = [v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0]
        elif name == 'rotate':
            r = math.radians(v[0]); cs, sn = math.cos(r), math.sin(r)
            n = [cs, sn, -sn, cs, 0, 0]
            if len(v) == 3: n = mat_mul(mat_mul([1, 0, 0, 1, v[1], v[2]], n), [1, 0, 0, 1, -v[1], -v[2]])
        else: continue
        m = mat_mul(m, n)
    return [round(x, 3) for x in m]

def col(a, key, default):
    v = a.get(key, default)
    return 0 if v is None or v == 'none' else v

def wrap(op, a):
    tf = a.get('transform')
    if tf:
        m = parse_tf(tf)
        op = [5, NUM(m[4]), NUM(m[5]), [op]] if m[:4] == [1, 0, 0, 1] else [8, *m, [op]]
    if a.get('opacity') not in (None, '1'): op = [7, NUM(a['opacity']), [op]]
    return op

def walk(node, clips):
    ops = []
    for el in node:
        tag = el.tag.split('}')[-1]; a = el.attrib
        if tag == 'clipPath':
            r = next(iter(el), None)
            if r is not None: clips[a['id']] = [NUM(r.get('x', 0)), NUM(r.get('y', 0)), NUM(r.get('width')), NUM(r.get('height'))]
            continue
        st = col(a, 'stroke', None)
        sw = NUM(a.get('stroke-width', 1)) if st else 0
        dash = [NUM(x) for x in re.split(r'[ ,]+', a['stroke-dasharray'].strip())] if a.get('stroke-dasharray') else 0
        fill = col(a, 'fill', '#000')
        op = None
        if tag == 'rect':
            op = [0, NUM(a.get('x', 0)), NUM(a.get('y', 0)), NUM(a['width']), NUM(a['height']), NUM(a.get('rx', 0)), fill, st, sw, dash]
        elif tag in ('ellipse', 'circle'):
            op = [1, NUM(a['cx']), NUM(a['cy']), NUM(a.get('rx', a.get('r'))), NUM(a.get('ry', a.get('r'))), fill, st, sw, dash]
        elif tag == 'path':
            op = [2, re.sub(r'(\d\.\d\d)\d+', r'\1', a['d']), fill, st, sw, dash]
        elif tag == 'line':
            op = [3, NUM(a['x1']), NUM(a['y1']), NUM(a['x2']), NUM(a['y2']), st or '#000', sw or 1]
        elif tag == 'text':
            op = [4, el.text or '', NUM(a.get('x', 0)), NUM(a.get('y', 0)), NUM(a.get('font-size', 6)), fill,
                  a.get('text-anchor', 'start'), 'middle' if a.get('dominant-baseline') == 'middle' else 'alphabetic']
        elif tag in ('g', 'svg'):
            sub = walk(el, clips)
            cp = re.match(r'url\(#([^)]+)\)', a.get('clip-path', ''))
            if cp and cp.group(1) in clips: op = [10, clips[cp.group(1)], sub]
            elif not a.get('transform') and a.get('opacity') in (None, '1'): ops.extend(sub); continue
            else: op = [5, 0, 0, sub]
        if op is not None: ops.append(wrap(op, a))
    return ops

def svg_ops(rel):
    root = ET.fromstring(open(os.path.join(PD, rel), encoding='utf-8').read())
    return walk(root, {})

cat = json.load(open(os.path.join(PD, 'catalog.json'), encoding='utf-8'))
OUT = {'buildings': {}, 'furn': {}, 'ext': {}, 'life': {}, 'truck': {}}
for k, v in cat['popupBuildings'].items():
    OUT['buildings'][k] = {'label': v['label'], 'wall': v['wall'], 'floor': v['floor'], 'rooms': v['rooms']['items'], 'spot': v['spot']}
for k, items in cat['furniture'].items():
    OUT['furn'][k] = {it['key']: {'fp': it['footprint'], 'sr': it.get('solidRect'), 'solid': bool(it['solid']), 'spot': it.get('spot'), 'ops': svg_ops(it['svg'])} for it in items}
for f in sorted(os.listdir(os.path.join(PD, 'exterior'))):
    if not f.endswith('.svg'): continue
    name = f[:-4]
    if name.startswith('truck-'): OUT['truck'][name[6:]] = svg_ops('exterior/' + f)
    else: OUT['ext'][name] = svg_ops('exterior/' + f)
for f in sorted(os.listdir(os.path.join(PD, 'lifecycle'))):
    if f.endswith('.svg'): OUT['life'][f[:-4]] = svg_ops('lifecycle/' + f)

js = json.dumps(OUT, ensure_ascii=False, separators=(',', ':'))
block = '<script id="popupAssets">\n/* 자동 생성: scripts/build-popup-assets.py (design/popup) — 직접 고치지 마세요 */\nwindow.HARU_POPUP = ' + js + ';\n</script>'
p = os.path.join(ROOT, 'src', 'harulog.html')
s = open(p, encoding='utf-8').read()
if '<script id="popupAssets">' in s:
    i = s.index('<script id="popupAssets">'); j = s.index('</script>', i) + len('</script>')
    s = s[:i] + block + s[j:]
else:
    i = s.index('<script id="sceneAssets">'); j = s.index('</script>', i) + len('</script>')
    s = s[:j] + '\n' + block + s[j:]
open(p, 'w', encoding='utf-8').write(s)
print(f'popup assets: {len(js)//1024} KB, buildings {len(OUT["buildings"])}, furniture {sum(len(v) for v in OUT["furn"].values())}, ext {len(OUT["ext"])}, truck {len(OUT["truck"])}, life {len(OUT["life"])} → src/harulog.html')
