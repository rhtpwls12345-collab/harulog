"""하루로그 '기록 → 장면' 그림 데이터 만들기
design/scene 의 pets/*.svg · props/*.svg · fx/*.svg · pets/anchors.json 을 읽어
앱이 바로 그릴 수 있는 그리기 명령(ops)으로 바꾸고 src/harulog.html 의 sceneAssets 블록에 넣는다.

  사용: python3 scripts/build-scene-assets.py   (그 다음 node scripts/build-www.mjs)

ops 형식은 build-village-assets.py 와 같고, 아래가 더해진다.
  [7,alpha,ops]                투명도 묶음
  [8,a,b,c,d,e,f,ops]          변환(행렬) 묶음
  [9,'c'|'h',ops]              목줄(c)·하네스(h) 중 고른 것만 그림
  색 '$f' '$d' '$g'            털 색 · 진한 털 색 · 장비 색 (그릴 때 바꿔 끼움)
"""
import json, math, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = os.path.join(ROOT, 'design', 'scene')
NUM = lambda v: round(float(v), 2)
VARS = {'--fur-dark': '$d', '--fur': '$f', '--gear': '$g'}

def style_of(a):
    out = {}
    for part in (a.get('style') or '').split(';'):
        if ':' in part:
            k, v = part.split(':', 1); out[k.strip()] = v.strip()
    return out

def color(a, key, default):
    st = style_of(a)
    v = st.get(key) or a.get(key, default)
    if v is None or v == 'none': return 0
    m = re.match(r'var\((--[a-z-]+)', v)
    if m: return VARS[m.group(1)]
    return v

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

def wrap(op, a):
    tf = a.get('transform')
    if tf:
        m = parse_tf(tf)
        if m[:4] == [1, 0, 0, 1]: op = [5, NUM(m[4]), NUM(m[5]), [op]]
        else: op = [8, *m, [op]]
    if a.get('opacity') not in (None, '1'): op = [7, NUM(a['opacity']), [op]]
    return op

def walk(node):
    ops = []
    for el in node:
        tag = el.tag.split('}')[-1]; a = el.attrib
        if 'leash-ring' in a.get('class', ''): continue
        st = color(a, 'stroke', None)
        sw = NUM(a.get('stroke-width', 1)) if st else 0
        dash = [NUM(x) for x in re.split(r'[ ,]+', a['stroke-dasharray'].strip())] if a.get('stroke-dasharray') else 0
        fill = color(a, 'fill', '#000')
        op = None
        if tag == 'rect':
            op = [0, NUM(a.get('x', 0)), NUM(a.get('y', 0)), NUM(a['width']), NUM(a['height']), NUM(a.get('rx', 0)), fill, st, sw, dash]
        elif tag in ('ellipse', 'circle'):
            rx = a.get('rx', a.get('r')); ry = a.get('ry', a.get('r'))
            op = [1, NUM(a['cx']), NUM(a['cy']), NUM(rx), NUM(ry), fill, st, sw, dash]
        elif tag == 'path':
            d = re.sub(r'(\d\.\d\d)\d+', r'\1', a['d'])
            op = [2, d, fill, st, sw, dash]
        elif tag == 'line':
            op = [3, NUM(a['x1']), NUM(a['y1']), NUM(a['x2']), NUM(a['y2']), st or '#000', sw or 1]
        elif tag == 'text':
            op = [4, el.text or '', NUM(a.get('x', 0)), NUM(a.get('y', 0)), NUM(a.get('font-size', 6)), fill,
                  a.get('text-anchor', 'start'), 'middle' if a.get('dominant-baseline') == 'middle' else 'alphabetic']
        elif tag in ('g', 'svg'):
            sub = walk(el); cls = a.get('class', '')
            if 'gear-collar' in cls: ops.append([9, 'c', sub]); continue
            if 'gear-harness' in cls: ops.append([9, 'h', sub]); continue
            if not a.get('transform') and a.get('opacity') in (None, '1'): ops.extend(sub); continue
            op = [5, 0, 0, sub]
        if op is not None: ops.append(wrap(op, a))
    return ops

import xml.etree.ElementTree as ET
def svg_file(rel):
    s = open(os.path.join(SC, rel), encoding='utf-8').read()
    root = ET.fromstring(s)
    return walk(root), [NUM(v) for v in root.attrib['viewBox'].split()]

OUT = {'pets': {}, 'props': {}, 'fx': {}}
anch = json.load(open(os.path.join(SC, 'pets', 'anchors.json'), encoding='utf-8'))
for f in sorted(os.listdir(os.path.join(SC, 'pets'))):
    if not f.endswith('.svg'): continue
    name = f[:-4]; parts = name.split('-')
    kind = parts[0]; breed = 'mix' if parts[1] in ('walk', 'sit', 'lie') else parts[1]
    pose = '-'.join(parts[1:] if breed == 'mix' else parts[2:])
    ops, vb = svg_file('pets/' + f)
    OUT['pets'][f'{kind}-{breed}-{pose}'] = {'ops': ops, 'ring': [NUM(v) for v in anch['frames'][name]['leashRing']]}
OUT['furDark'] = anch['furDark']
for d in ('props', 'fx'):
    for f in sorted(os.listdir(os.path.join(SC, d))):
        if f.endswith('.svg'): OUT[d][f[:-4]] = svg_file(f'{d}/{f}')[0]

js = json.dumps(OUT, ensure_ascii=False, separators=(',', ':'))
block = '<script id="sceneAssets">\n/* 자동 생성: scripts/build-scene-assets.py (design/scene) — 직접 고치지 마세요 */\nwindow.HARU_SCENE = ' + js + ';\n</script>'
p = os.path.join(ROOT, 'src', 'harulog.html')
s = open(p, encoding='utf-8').read()
if '<script id="sceneAssets">' in s:
    i = s.index('<script id="sceneAssets">'); j = s.index('</script>', i) + len('</script>')
    s = s[:i] + block + s[j:]
else:
    i = s.index('<script id="villageAssets">'); j = s.index('</script>', i) + len('</script>')
    s = s[:j] + '\n' + block + s[j:]
open(p, 'w', encoding='utf-8').write(s)
print(f'scene assets: {len(js)//1024} KB, pets {len(OUT["pets"])}, props {len(OUT["props"])}, fx {len(OUT["fx"])} → src/harulog.html')
