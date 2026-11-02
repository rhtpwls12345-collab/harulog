"""Harulog village — illustrated SVG renderer (3/4 top-down, roofless buildings).
All coordinates are the app's logical world units (slot 344x224, building 224/272/320 wide)."""
import math

OL = "#4A3428"          # warm outline
OLW = 0.7               # outline width
FLOOR = 36

def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")

def shade(hexc, k):
    h = hexc.lstrip("#"); r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    fn = (lambda v: v * (1 + k)) if k < 0 else (lambda v: v + (255 - v) * k)
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(fn(v)))) for v in (r, g, b))

def rect(x, y, w, h, fill, rx=0, stroke=None, sw=OLW, extra=""):
    s = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" fill="{fill}"{s}{extra}></rect>'

def ell(cx, cy, rx, ry, fill, stroke=None, sw=OLW, extra=""):
    s = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}"{s}{extra}></ellipse>'

def path(d, fill, stroke=None, sw=OLW, extra=""):
    s = f' stroke="{stroke}" stroke-width="{f(sw)}" stroke-linejoin="round" stroke-linecap="round"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{s}{extra}></path>'

def line(x1, y1, x2, y2, col, w=0.6, extra=""):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" stroke-width="{f(w)}" stroke-linecap="round"{extra}></line>'

def g(content, tx=0, ty=0, extra=""):
    if not tx and not ty and not extra:
        return content
    t = f' transform="translate({f(tx)},{f(ty)})"' if (tx or ty) else ""
    return f"<g{t}{extra}>{content}</g>"

def shadow(x, y, rx, ry=None, a=0.16):
    return ell(x, y, rx, ry if ry is not None else rx * 0.35, f"rgba(60,40,20,{a})")

def block(x, y, w, d, h, top, front=None, r=1.4, outline=True):
    """3/4 view box: top face (depth d) above a front face (height h)."""
    front = front or shade(top, -0.16)
    out = rect(x + 0.8, y + d + h - 0.8, w, 2.6, "rgba(60,40,20,.14)", 1.3)
    out += rect(x, y, w, d + h, front, r)
    out += rect(x, y, w, d, top, r)
    if h:
        out += rect(x + 0.4, y + d - 0.2, w - 0.8, 0.5, "rgba(0,0,0,.10)")
        out += rect(x + 0.4, y + d + h - 1.4, w - 0.8, 1, "rgba(0,0,0,.08)", 0.5)
    out += rect(x + r * 0.7, y + 0.5, w - r * 1.4, 0.45, "rgba(255,255,255,.45)", 0.2)
    if outline:
        out += rect(x, y, w, d + h, "none", r, OL, 0.5)
    return out

# ---------------------------------------------------------------- palettes
WALLS = {
    "cream":    dict(label="크림",   wall="#F6E3CC", line="#EED6BA", sign="#D98B6A"),
    "mint":     dict(label="민트",   wall="#E3EEDF", line="#D5E4D0", sign="#6FA387"),
    "sky":      dict(label="하늘",   wall="#DDEAEE", line="#CFE0E5", sign="#6F8FB5"),
    "peach":    dict(label="복숭아", wall="#FBE2CF", line="#F3D3BA", sign="#D9775F"),
    "lavender": dict(label="라벤더", wall="#ECE5F3", line="#DED4EB", sign="#8C7BB5"),
    "latte":    dict(label="라테",   wall="#E8D5BE", line="#DCC6AC", sign="#B0835C"),
}
THEMES = {
    "village": dict(label="시골 마을", desc="잔디와 흙길, 꽃이 핀 동네", g1="#B4D79A", g2="#A6CC8B", road="#E2D3B6", roadE="#C4AE88", tree="round"),
    "city":    dict(label="콘크리트 도시", desc="아스팔트 도로와 화단 가로수", g1="#D3D6D9", g2="#C5C9CD", road="#5D636A", roadE="#8C9198", tree="planter"),
    "coast":   dict(label="해안 도시", desc="모래사장과 나무 데크, 바다", g1="#F1E2BC", g2="#E8D5A6", road="#C9A47A", roadE="#A47F55", tree="palm"),
    "forest":  dict(label="숲속 마을", desc="짙은 숲과 돌길, 버섯", g1="#93C07D", g2="#7FAF6A", road="#C3BCAA", roadE="#9A9382", tree="pine"),
}
BSIZES = {"s": (224, 140), "m": (272, 156), "l": (320, 172)}

# ---------------------------------------------------------------- small reusable pieces
def window(x, y, w, h, frame="#FFFDF6", curtain="#F2B8A0", night=False):
    sky = "#2E3A5C" if night else "#BFE3F2"
    out = rect(x - 1.5, y - 1.5, w + 3, h + 3, "#B98D62", 1.2, OL, 0.5)
    out += rect(x, y, w, h, sky, 0.6)
    if not night:
        out += path(f"M{x},{y+h*0.65} Q{x+w*0.3},{y+h*0.45} {x+w*0.55},{y+h*0.62} T{x+w},{y+h*0.5} L{x+w},{y+h} L{x},{y+h} Z", "#A9D8A0")
        out += ell(x + w * 0.78, y + h * 0.3, 2.2, 2.2, "#FFF3B8")
        out += path(f"M{x+w*0.18},{y+h*0.28} q2,-2 4,0 q2,-1 3,1 z", "#FFFFFF")
    out += rect(x + w / 2 - 0.5, y, 1, h, frame) + rect(x, y + h / 2 - 0.5, w, 1, frame)
    out += line(x + 2, y + h - 2, x + 7, y + 2, "rgba(255,255,255,.55)", 0.8)
    # curtains
    out += path(f"M{x-3},{y-2.5} L{x+5},{y-2.5} Q{x+3},{y+h*0.5} {x+4.5},{y+h+1} L{x-3},{y+h+1} Z", curtain, OL, 0.45)
    out += path(f"M{x+w+3},{y-2.5} L{x+w-5},{y-2.5} Q{x+w-3},{y+h*0.5} {x+w-4.5},{y+h+1} L{x+w+3},{y+h+1} Z", curtain, OL, 0.45)
    out += rect(x - 4, y - 3.6, w + 8, 1.4, "#9C7450", 0.7)
    out += rect(x - 2, y + h + 1.5, w + 4, 1.8, "#E9D8C2", 0.6, OL, 0.4)
    return out

def plant(x, y, pot="#E39A6E", leaf="#7DBA6A"):
    out = shadow(x, y + 0.5, 5, 1.6)
    out += path(f"M{x-4},{y-6} L{x+4},{y-6} L{x+3},{y} L{x-3},{y} Z", pot, OL, 0.5)
    out += rect(x - 4.6, y - 7.2, 9.2, 1.8, shade(pot, 0.15), 0.8, OL, 0.45)
    for a, l, c in ((-55, 9, leaf), (-95, 11, shade(leaf, -0.12)), (-130, 9, leaf), (-75, 12, shade(leaf, 0.12)), (-110, 10, leaf)):
        rad = math.radians(a)
        ex, ey = x + math.cos(rad) * l, y - 7 + math.sin(rad) * l
        out += path(f"M{x},{y-7} Q{f((x+ex)/2 - math.sin(rad)*3)},{f((y-7+ey)/2 + math.cos(rad)*3)} {f(ex)},{f(ey)} Q{f((x+ex)/2 + math.sin(rad)*3)},{f((y-7+ey)/2 - math.cos(rad)*3)} {x},{y-7} Z", c, OL, 0.4)
    return out

def frame_pic(x, y, w, h, inner):
    return rect(x - 1, y - 1, w + 2, h + 2, "#7A5A42", 0.6, OL, 0.4) + rect(x, y, w, h, "#FFFDF6", 0.3) + inner

def sign_plate(x, y, text, col):
    w = max(18, len(text) * 7 + 8)
    return (rect(x - w / 2, y - 5, w, 10, col, 3, OL, 0.5) + rect(x - w / 2 + 1, y - 4.2, w - 2, 1, "rgba(255,255,255,.35)", 0.5)
            + f'<text x="{f(x)}" y="{f(y + 0.3)}" font-family="Jua, sans-serif" font-size="6.6" fill="#FFFFFF" text-anchor="middle" dominant-baseline="middle">{text}</text>')

# ---------------------------------------------------------------- floors
def floor_fill(kind, x, y, w, h, uid):
    cid = f"fl{uid}"
    out = f'<clipPath id="{cid}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"></rect></clipPath><g clip-path="url(#{cid})">'
    if kind == "wood":
        out += rect(x, y, w, h, "#E2B985")
        row = 0
        for yy in range(int(y), int(y + h) + 8, 8):
            off = (row * 23) % 40
            tone = ["#E2B985", "#DDB17C", "#E8C291"][row % 3]
            out += rect(x, yy, w, 8, tone)
            out += rect(x, yy, w, 0.5, "#C69766")
            out += rect(x, yy + 0.6, w, 0.5, "rgba(255,255,255,.25)")
            for xx in range(int(x) - off, int(x + w), 40):
                out += rect(xx, yy, 0.5, 8, "#C69766")
                out += path(f"M{xx+8},{yy+4} q6,-1.2 12,0", "none", "rgba(160,110,70,.35)", 0.35)
            row += 1
    elif kind == "tile":
        out += rect(x, y, w, h, "#F4E6D4")
        for r, yy in enumerate(range(int(y), int(y + h) + 16, 16)):
            for c, xx in enumerate(range(int(x), int(x + w) + 16, 16)):
                if (r + c) % 2 == 0:
                    out += rect(xx, yy, 16, 16, "#EBCFB4")
                out += rect(xx, yy, 0.5, 16, "rgba(255,255,255,.7)")
            out += rect(x, yy, w, 0.5, "rgba(255,255,255,.7)")
    else:  # modern
        out += rect(x, y, w, h, "#DEDBD5")
        for yy in range(int(y) + 24, int(y + h), 24):
            out += rect(x, yy, w, 0.5, "#C7C2B9")
        for xx in range(int(x) + 32, int(x + w), 32):
            out += rect(xx, y, 0.5, h, "#C7C2B9")
        for i in range(60):
            out += rect(x + (i * 41.3) % w, y + (i * 17.9) % h, 0.6, 0.6, "#CFCAC2" if i % 2 else "#ECE9E4")
    out += "</g>"
    return out

# ---------------------------------------------------------------- interiors (local coords, base width 224)
def furn_home(o):
    out = window(20, 8, 34, 18, curtain="#F2B8A0")
    out += frame_pic(80, 9, 20, 14, rect(81.5, 10.5, 17, 11, "#CDE6D3") + path("M81.5,21.5 L86,15 L90,19 L93,16 L98.5,21.5 Z", "#7FAE7E") + ell(95, 13, 1.6, 1.6, "#F2B84B"))
    out += rect(113, 13.5, 30, 1.8, "#9C7450", 0.8, OL, 0.4)
    out += rect(116, 6, 6, 7.5, "#E99A6E", 0.6, OL, 0.35) + rect(123.5, 8, 4.5, 5.5, "#8CB8E0", 0.6, OL, 0.35) + plant_small(136, 13.5)
    # rug
    out += ell(100, 112, 37, 13.5, "#D9A27E", OL, 0.5) + ell(100, 112, 33, 11.5, "#F3CDB0") + ell(100, 112, 33, 11.5, "none", "#E7B18E", 1.2, ' stroke-dasharray="2 2"')
    out += ell(100, 112, 22, 7.2, "#E7B18E") + ell(100, 112, 18, 5.6, "#F7DCC6") + ell(100, 112, 7, 2.5, "#EBBE9C")
    out += plant(12, 54)
    # floor lamp
    out += shadow(156, 57.5, 5, 1.5) + rect(152, 55, 8, 2.5, "#5A4033", 1.2) + rect(155.3, 38, 1.4, 17, "#7A5A42")
    out += path("M149,39 L163,39 L160.5,31 L151.5,31 Z", "#F2B84B", OL, 0.5) + rect(151, 31.5, 10, 1, "#F7D07A") + ell(156, 50, 10, 3, "rgba(255,226,140,.18)")
    # sofa
    out += block(66, 42, 68, 9, 10, "#A9CBB2", "#8DB59A")
    out += block(66, 62, 68, 12, 6, "#B9D7C1", "#9DC0A8")
    out += rect(70, 63, 29, 9, "#C6E0CC", 2, OL, 0.35) + rect(101, 63, 29, 9, "#C6E0CC", 2, OL, 0.35)
    out += block(62, 52, 8, 22, 8, "#8DB596", "#769F82") + block(130, 52, 8, 22, 8, "#8DB596", "#769F82")
    out += block(74, 56, 11, 7, 2.5, "#F2B892", "#E39A7A", 2) + block(114, 57, 10, 6, 2.5, "#F7E1A0", "#E7C878", 2)
    # coffee table + mug + book
    out += block(88, 86, 24, 10, 5, "#C9A076", "#A9805A") + ell(94, 89.5, 2, 1.1, "#FFFFFF", OL, 0.35) + rect(102, 87.5, 7, 4.5, "#8CB8E0", 0.5, OL, 0.3)
    # bed
    out += block(172, 22, 42, 6, 12, "#B98D62", "#9C7450")
    out += block(172, 40, 42, 48, 6, "#FFFFFF", "#E5DCCF")
    out += block(180, 43, 26, 9, 2.5, "#F7F3EC", "#E6DED2", 3)
    out += block(174, 62, 38, 24, 2, "#F0C3A3", "#D9A988")
    for i in range(5):
        out += line(176, 66 + i * 4, 210, 66 + i * 4, "rgba(255,255,255,.35)", 0.6)
    out += rect(173, 94.5, 3, 3, "#5A4033", 0.5) + rect(210, 94.5, 3, 3, "#5A4033", 0.5)
    out += cat(128, 120)
    # nightstand
    out += block(152, 76, 14, 8, 8, "#C9A076", "#A9805A") + rect(156, 73, 6, 4, "#F2EDE4", 1, OL, 0.35)
    return out

def chair(x, y, w, d, h, wood="#B98D62", cushion="#F2C9A8"):
    out = rect(x + 1.5, y + d + h - 1, 1.6, 2.4, shade(wood, -0.35)) + rect(x + w - 3.1, y + d + h - 1, 1.6, 2.4, shade(wood, -0.35))
    out += block(x, y, w, 4, h + d - 4, wood, shade(wood, -0.18), 1.6)
    out += block(x + 1, y + 4.5, w - 2, d - 4.5, h * 0.55, cushion, shade(cushion, -0.15), 2)
    return out

def rug(cx, cy, rx, ry, a, b):
    return (ell(cx, cy, rx, ry, a, OL, 0.45) + ell(cx, cy, rx - 2.5, ry - 1.8, "none", b, 1, ' stroke-dasharray="1.5 1.5"')
            + ell(cx, cy, rx * 0.55, ry * 0.55, b))

def cat(x, y, c="#F2B84B"):
    return (shadow(x, y + 1, 6, 1.4) + ell(x, y - 1.5, 6, 3, c, OL, 0.45) + ell(x + 5, y - 3, 3, 2.6, c, OL, 0.45)
            + path(f"M{x+3},{y-5} l0.6,-2.4 l1.4,1.6 z M{x+6},{y-5.2} l1,-2.2 l0.8,2 z", c, OL, 0.35)
            + path(f"M{x+4},{y-3} q0.6,0.6 1.2,0 M{x+6},{y-3} q0.6,0.6 1.2,0", "none", OL, 0.35)
            + path(f"M{x-6},{y-1} q-3,-1 -2,-4", "none", c, 1.6) + path(f"M{x-2},{y-4} l1,1 M{x+1},{y-4.4} l1,1", "none", shade(c, -0.2), 0.6))

def string_lights(x0, x1, y, cols=("#F7D07A", "#F29A7F", "#8CC7EE", "#B7E3A0")):
    out = path(f"M{x0},{y} Q{(x0+x1)/2},{y+5} {x1},{y}", "none", "#7A5A42", 0.4)
    n = int((x1 - x0) / 7)
    for i in range(1, n):
        t = i / n
        px = x0 + (x1 - x0) * t
        py = y + 5 * 2 * t * (1 - t)
        out += ell(px, py + 1, 0.9, 1.1, cols[i % len(cols)], OL, 0.25)
    return out

def plant_small(x, y):
    return (rect(x - 2.5, y - 4, 5, 4, "#E39A6E", 0.6, OL, 0.35) + ell(x - 1.5, y - 6, 2.2, 2.6, "#7DBA6A", OL, 0.35)
            + ell(x + 1.6, y - 6.5, 2, 2.4, "#8FC77B", OL, 0.35))

def furn_work(o):
    out = window(164, 8, 34, 18, curtain="#B9D7C1")
    out += ell(112, 15, 6.5, 6.5, "#5A4033") + ell(112, 15, 5.5, 5.5, "#FFFDF6") + line(112, 15, 112, 11, OL, 0.6) + line(112, 15, 115, 15, OL, 0.6) + ell(112, 15, 0.7, 0.7, OL)
    out += rect(69.5, 7.5, 25, 15, "#5A4033", 1) + rect(70.5, 8.5, 23, 13, "#FFFDF6", 0.6)
    out += rect(73, 11, 10, 1, "#8CB8E0") + rect(73, 14, 16, 1, "#E99A6E") + rect(73, 17, 12, 1, "#8DB596")
    out += rect(85, 11, 6, 6, "#FFE7A3", 0.4) + rect(78, 4, 5, 4, "#F2B84B", 0.3)
    # bookshelf
    out += block(10, 16, 40, 6, 40, "#B98D62", "#9C7450")
    out += rect(11.5, 23, 37, 37, "#7A5A42", 0.8)
    bc = ["#E99A6E", "#8DB596", "#8CB8E0", "#E8B64C", "#D98BA6", "#F2EDE4", "#B7A1D9"]
    for s in range(3):
        out += rect(11.5, 34 + s * 12, 37, 1.5, "#B98D62")
        for i in range(10):
            bh = 8 - (1.5 if i % 3 == 0 else 0)
            bx = 13 + i * 3.5
            if s == 1 and i in (7, 8):
                continue
            out += rect(bx, 34 + s * 12 - bh, 3, bh, bc[(i + s * 2) % 7], 0.4, OL, 0.25)
        if s == 1:
            out += path("M38.5,46 L45,40 L46.5,41.2 L40,47 Z", "#E8B64C", OL, 0.25)
    out += plant(212, 56)
    out += rug(118, 128, 44, 9, "#B9D7C1", "#9DC0A8")
    out += rect(120, 6, 22, 15, "#C9A076", 1, OL, 0.45) + rect(122, 8, 5, 5, "#FFE7A3", 0.3) + rect(129, 9, 5, 4, "#B9D7C1", 0.3) + rect(135, 8, 5, 6, "#F7C9B8", 0.3) + ell(124.5, 8, 0.6, 0.6, "#E06A52") + ell(131.5, 9, 0.6, 0.6, "#2F6FA8")
    # chairs
    for cx0 in (56, 160):
        out += chair(cx0, 52, 20, 14, 6, "#7E8FA3", "#AFC0D2")
    # desks
    for dx in (28, 132):
        out += block(dx, 84, 76, 14, 12, "#D6B087", "#B58C63")
        out += rect(dx + 4, 100, 32, 6, "#B98D62", 1, OL, 0.35) + rect(dx + 40, 100, 32, 6, "#B98D62", 1, OL, 0.35)
        out += ell(dx + 20, 103, 1, 0.7, "#E9C46A") + ell(dx + 56, 103, 1, 0.7, "#E9C46A")
    # laptop on desk 1
    out += rect(51.5, 73.5, 29, 14, OL, 1.2) + rect(52.5, 74.5, 27, 12, "#3B4A63", 0.8)
    out += rect(54, 76, 14, 1.2, "#8CB8E0") + rect(54, 79, 20, 1.2, "#8DB596") + rect(54, 82, 10, 1.2, "#E99A6E")
    out += rect(50, 87, 33, 3.2, "#C8CFD6", 1, OL, 0.4)
    out += rect(89.5, 85.5, 7, 7, OL, 1) + rect(90, 86, 6, 6, "#FFFFFF", 0.8) + rect(90, 86, 6, 1.5, "#8A5A3C", 0.5)
    out += path("M96,87.5 q2.4,0 2.4,2 q0,2 -2.4,2", "none", OL, 0.5)
    # desk 2: lamp + notebooks + pencil cup
    out += rect(144.4, 77, 1.4, 12, "#5A4033") + path("M139,79 L151,79 L149,72.5 L141,72.5 Z", "#F2B84B", OL, 0.45)
    out += rect(186, 90, 16, 3, "#8CB8E0", 0.5, OL, 0.3) + rect(187, 87, 14, 3, "#D98BA6", 0.5, OL, 0.3) + rect(188, 84, 12, 3, "#8DB596", 0.5, OL, 0.3)
    out += rect(164, 86, 5, 6, "#E99A6E", 0.6, OL, 0.35) + line(165, 86, 164, 82, "#F2B84B", 0.8) + line(167.5, 86, 168.5, 82.5, "#8CB8E0", 0.8)
    return out

def furn_cafe(o):
    out = window(14, 10, 40, 16, curtain="#F6E3CC")
    out += rug(98, 118, 40, 10, "#E7B18E", "#F3CDB0")
    for i in range(9):
        c = "#E99A6E" if i % 2 == 0 else "#FFFDF6"
        out += path(f"M{8+i*6},{2.5} L{14+i*6},{2.5} L{14+i*6},{6.5} Q{11+i*6},{9} {8+i*6},{6.5} Z", c, OL, 0.35)
    out += rect(67.5, 5.5, 37, 23, "#7A5238", 1.2, OL, 0.5) + rect(69.5, 7.5, 33, 19, "#3F5A4A", 0.6)
    out += f'<text x="86" y="12" font-family="Jua, sans-serif" font-size="4.6" fill="#FFF8E6" text-anchor="middle">MENU</text>'
    for i in range(3):
        out += rect(73, 15 + i * 3.6, 14, 0.6, "rgba(255,255,255,.75)") + rect(92, 15 + i * 3.6, 6, 0.6, "#F2B84B")
    out += ell(119, 15, 4.5, 4.5, "#F6E3CC", OL, 0.45) + path("M116.5,15 h5 v3 q-2.5,1.8 -5,0 Z", "#FFFFFF", OL, 0.35)  # cup sign
    # counter
    out += block(150, 30, 70, 14, 16, "#E2C29A", "#C39E73")
    out += rect(150, 46, 70, 1.2, "#A9805A")
    for i in range(6):
        out += rect(153 + i * 11, 48, 9, 9, "rgba(255,255,255,.18)", 1)
    out += rect(159.5, 17.5, 17, 17, OL, 1.4) + rect(160.5, 18.5, 15, 15, "#9AA8B4", 1)
    out += rect(162, 20, 12, 4, "#C9D3DB", 0.6) + ell(168, 21.8, 1, 1, "#E06A52") + rect(165.5, 27, 5, 4.5, "#FFFFFF", 0.6, OL, 0.3)
    out += rect(183.5, 28.5, 5, 6.5, "#FFFFFF", 0.8, OL, 0.35) + rect(191.5, 27.5, 5, 7.5, "#F2EDE4", 0.8, OL, 0.35)
    out += ell(207, 33, 6, 2.4, "#FFFFFF", OL, 0.4) + ell(204.5, 31.6, 2, 1.5, "#E8B64C", OL, 0.3) + ell(208.5, 31.4, 2, 1.5, "#D98B6A", OL, 0.3)
    out += path("M200,29 q7,-6 14,0 Z", "rgba(220,240,255,.55)", OL, 0.35)
    out += plant(132, 56)
    # stool + tables
    out += chair(80, 52, 20, 14, 6, "#9C7450", "#F2B892")
    out += string_lights(4, 140, 3)
    out += shadow(90, 111, 15, 3) + block(74, 84, 32, 12, 8, "#E2C29A", "#C39E73", 2) + rect(88, 104, 4, 6, "#7A5A42")
    out += ell(80, 89, 4.5, 1.6, OL) + ell(80, 89, 4, 1.3, "#FFFFFF") + ell(80, 88.4, 2.5, 0.8, "#E8B64C")
    out += rect(96.5, 85.5, 7, 7, OL, 1) + rect(97, 86, 6, 6, "#FFFFFF", 0.8) + rect(97, 86, 6, 1.5, "#8A5A3C", 0.5)
    out += path("M98.5,83 q-1,-2 0,-4 M101,82.5 q1,-2 0,-4", "none", "rgba(160,140,130,.6)", 0.5)
    out += chair(156, 76, 22, 16, 4, "#9C7450", "#F2B892")
    out += path("M30,128 L36,112 L42,128 Z", "#7A5238", OL, 0.45) + path("M31.5,126 L36,114.5 L40.5,126 Z", "#3F5A4A") + rect(33.5, 119, 5, 0.6, "#FFFFFF") + rect(34, 121.5, 4, 0.6, "#F2B84B")
    out += block(154, 98, 30, 12, 8, "#E2C29A", "#C39E73", 2) + rect(165.5, 91.5, 7, 7, OL, 1) + rect(166, 92, 6, 6, "#F2EDE4", 0.8)
    out += plant_small(176, 102)
    return out

def furn_dining(o):
    out = window(18, 8, 34, 18, curtain="#F2C9A8")
    out += rect(150, 16, 44, 1.6, "#9C7450", 0.6, OL, 0.35)
    for i in range(4):
        out += ell(156 + i * 10, 12, 4, 3.6, OL) + ell(156 + i * 10, 12, 3.4, 3, "#FFFFFF" if i % 2 else "#F2EDE4") + ell(156 + i * 10, 12, 1.6, 1.4, "#8CB8E0" if i % 2 else "#E99A6E")
    out += frame_pic(96, 8, 16, 16, rect(97, 9, 14, 14, "#FFF4E6") + ell(104, 16, 4.5, 4.5, "#F2A47F") + path("M101,18 q3,2 6,0", "none", "#FFFFFF", 0.6))
    out += plant(212, 56)
    out += rug(112, 104, 58, 20, "#E7C9A8", "#F3DDC4")
    out += chair(102, 50, 20, 14, 6, "#B98D62", "#F2EDE4")
    out += rect(20, 40, 18, 16, "#FFFDF6", 1, OL, 0.45) + '<text x="29" y="46" font-family="Jua, sans-serif" font-size="3.4" fill="#B0835C" text-anchor="middle">오늘의</text><text x="29" y="51" font-family="Jua, sans-serif" font-size="3.4" fill="#B0835C" text-anchor="middle">메뉴</text>' 
    # long table with runner
    out += shadow(112, 116, 46, 4)
    out += block(70, 80, 84, 24, 10, "#D6B087", "#B58C63")
    out += rect(70, 88, 84, 8, "#FFFDF6") + rect(70, 89, 84, 0.6, "#F2A47F") + rect(70, 94.4, 84, 0.6, "#F2A47F")
    out += ell(112, 91.5, 8.5, 3.4, OL) + ell(112, 91.5, 8, 3, "#FFFFFF") + ell(112, 90.4, 5.5, 2.2, "#F2B84B") + ell(110, 89.8, 1.4, 0.8, "#E06A52") + ell(114, 90, 1.3, 0.7, "#8DB596")
    out += ell(94, 92, 5, 2.2, OL) + ell(94, 92, 4.5, 1.8, "#FFFFFF") + ell(94, 91.6, 3, 1, "#E06A52")
    out += ell(130, 92, 5, 2.2, OL) + ell(130, 92, 4.5, 1.8, "#FFFFFF") + ell(130, 91.6, 3, 1, "#8DB596")
    out += line(86, 89, 86, 95, "#B9C4CD", 0.6) + line(138, 89, 138, 95, "#B9C4CD", 0.6)
    out += rect(121, 84, 3, 5, "#F2EDE4", 0.8, OL, 0.3) + ell(122.5, 83.4, 1, 1.4, "#F2B84B")
    return out

def furn_gym(o):
    out = window(168, 8, 34, 18, curtain="#CFE0E5")
    out += rect(65.5, 4.5, 65, 27, "#8C9AA6", 1, OL, 0.5) + rect(67, 6, 62, 24, "#DCE8EE", 0.6)
    for k in range(3):
        out += line(76 + k * 6, 26, 84 + k * 6, 9, "rgba(255,255,255,.75)", 1.2)
    out += rect(79.5, 89.5, 65, 33, OL, 2) + rect(80, 90, 64, 32, "#8DB596", 1.6)
    for yy in range(94, 122, 4):
        out += rect(81, yy, 62, 0.5, "#7FA888")
    out += rect(80, 90, 64, 2, "rgba(255,255,255,.2)", 1)
    out += block(10, 30, 44, 8, 10, "#9AA6B0", "#77828C")
    for i in range(3):
        dx = 14 + i * 13
        out += rect(dx, 28.5, 3, 7, "#3A3F45", 0.8) + rect(dx + 8, 28.5, 3, 7, "#3A3F45", 0.8) + rect(dx + 3, 31.3, 5, 1.5, "#B5BEC6")
    out += shadow(196, 114, 8, 2) + ell(196, 106, 8.5, 8.5, OL) + ell(196, 106, 8, 8, "#E99A6E")
    out += path("M188.5,106 Q196,103 203.5,106", "none", "#C87A55", 0.7) + path("M196,98 Q193,106 196,114", "none", "#C87A55", 0.7) + ell(193, 103, 2, 1.4, "rgba(255,255,255,.35)")
    out += rect(159.5, 99.5, 6, 12, OL, 1.4) + rect(160, 102, 5, 9, "#8CC7EE", 1) + rect(160, 100, 5, 2, "#3A3F45", 0.6)
    out += block(20, 96, 34, 9, 6, "#4F5560", "#3A3F45", 2) + rect(22, 97, 30, 6, "#E06A52", 2)
    out += ell(30, 70, 7, 7, "#3A3F45", OL, 0.45) + ell(30, 70, 4, 4, "#8C9AA6") + ell(30, 70, 1.5, 1.5, "#3A3F45")
    out += rect(204, 66, 10, 26, "#E06A52", 4, OL, 0.45) + rect(206, 62, 6, 5, "#4F5560", 1) + rect(205, 70, 8, 1, "rgba(255,255,255,.4)")
    out += rect(204, 40, 12, 14, "#EDEFF2", 2, OL, 0.4) + rect(206, 43, 8, 3, "#8CB8E0", 1)
    return out

FURN = {"home": furn_home, "work": furn_work, "cafe": furn_cafe, "dining": furn_dining, "gym": furn_gym}
KIND_LABEL = {"home": "집", "work": "작업실", "cafe": "카페", "dining": "식당", "gym": "체육관", "park": "공원", "plaza": "광장", "grove": "작은 숲", "empty": "빈 땅"}

def building(kind, size, color, style, uid, avatars="", interior=None):
    """returns SVG group in building-local coords (0,0 = top-left of back wall)."""
    bw, bh = BSIZES[size]
    c = WALLS[color]
    cx = (bw - 224) / 2
    T = 4.5  # wall thickness (seen from above)
    out = shadow(bw / 2 + 2, bh + 3, bw / 2 + 8, 6, 0.18)
    # floor
    out += floor_fill(style, 0, FLOOR, bw, bh - FLOOR, uid)
    # back wall
    out += rect(0, 0, bw, FLOOR, c["wall"])
    out += rect(0, 20, bw, FLOOR - 20, c["line"])
    for xx in range(6, int(bw), 10):
        out += rect(xx, 22, 0.5, FLOOR - 26, "rgba(0,0,0,.06)") + rect(xx + 0.5, 22, 0.5, FLOOR - 26, "rgba(255,255,255,.3)")
    out += rect(0, 19.5, bw, 1.2, shade(c["line"], -0.18)) + rect(0, 20.7, bw, 0.6, "rgba(255,255,255,.4)")
    out += rect(0, FLOOR - 3.5, bw, 3.5, "#A27A57") + rect(0, FLOOR - 3.5, bw, 0.6, "#C9A27A")
    # floor AO
    out += rect(0, FLOOR, bw, 2, "rgba(60,40,20,.14)") + rect(0, FLOOR + 2, bw, 2, "rgba(60,40,20,.06)")
    out += rect(T, FLOOR, 2.5, bh - FLOOR, "rgba(60,40,20,.08)") + rect(bw - T - 2.5, FLOOR, 2.5, bh - FLOOR, "rgba(60,40,20,.08)")
    # interior
    out += interior if interior is not None else g(FURN[kind]({}), cx, 0)
    out += avatars
    # walls seen from above (left / right / front with door gap)
    cap = shade(c["line"], 0.25)
    side = shade(c["wall"], -0.22)
    door = bw / 2
    out += rect(-T, -T, T, bh + T, cap, 0, OL, 0.6) + rect(bw, -T, T, bh + T, cap, 0, OL, 0.6)
    out += rect(-T, -T, bw + 2 * T, T, cap, 0, OL, 0.6)
    out += rect(-T, bh - 1, door - 13 + T, T + 1, cap, 0, OL, 0.6) + rect(door + 13, bh - 1, bw - door - 13 + T, T + 1, cap, 0, OL, 0.6)
    out += rect(-T, bh + T, door - 13 + T, 5, side, 0, OL, 0.6) + rect(door + 13, bh + T, bw - door - 13 + T, 5, side, 0, OL, 0.6)
    out += rect(-T, -T, T + 0.01, 0.01, "none")
    # door mat + step
    out += rect(door - 11, bh - 1, 22, T + 1, shade(c["sign"], 0.55)) + rect(door - 9, bh + 0.2, 18, 2.6, c["sign"], 1, OL, 0.35)
    out += rect(door - 13, bh + T + 1, 26, 4, "#D9C7AE", 1, OL, 0.45)
    # corner posts
    for px, py in ((-T, -T), (bw, -T), (-T, bh - 1), (bw, bh - 1)):
        out += rect(px - 0.6, py - 0.6, T + 1.2, T + 1.2, shade(c["sign"], 0.1), 1, OL, 0.5)
    # name sign on front wall
    out += sign_plate(28, bh + T + 2.5, KIND_LABEL[kind], c["sign"])
    # wall-mounted lamp at entrance
    out += ell(door + 18, bh + T + 1.5, 1.8, 1.8, "#F7D07A", OL, 0.4)
    return out

# ---------------------------------------------------------------- outdoor
def tree(x, y, kind="round", s=1.0):
    out = shadow(x + 2, y, 9 * s, 3 * s, 0.2)
    if kind == "round":
        out += path(f"M{x-1.8*s},{y} L{x-1.2*s},{y-10*s} L{x+1.2*s},{y-10*s} L{x+1.8*s},{y} Z", "#8A6446", OL, 0.5)
        for dx, dy, r, col in ((-4.5, -14, 7, "#5E9E52"), (4.5, -14, 7, "#5E9E52"), (0, -19, 8, "#6FB05E"), (-3, -16, 6, "#7DBE6A"), (3, -20, 5, "#8FCB78")):
            out += ell(x + dx * s, y + dy * s, r * s, r * 0.9 * s, col, OL, 0.5)
        out += ell(x - 2.5 * s, y - 21 * s, 2 * s, 1.3 * s, "rgba(255,255,255,.35)")
        out += ell(x + 4 * s, y - 13 * s, 1 * s, 1 * s, "#F29A7F") + ell(x - 5 * s, y - 16 * s, 0.9 * s, 0.9 * s, "#F29A7F")
    elif kind == "pine":
        out += rect(x - 1.5 * s, y - 6 * s, 3 * s, 6 * s, "#7A5238", 0.5, OL, 0.45)
        for i, (w, yy, col) in enumerate(((10, -6, "#3F7F52"), (8, -12, "#4C8E5D"), (6, -17.5, "#5A9E69"))):
            out += path(f"M{x-w*s},{y+yy*s} L{x},{y+(yy-9)*s} L{x+w*s},{y+yy*s} Q{x},{y+(yy+2)*s} {x-w*s},{y+yy*s} Z", col, OL, 0.5)
        out += path(f"M{x-1*s},{y-25*s} l{1.5*s},{-1.5*s}", "none", "rgba(255,255,255,.4)", 0.6)
    elif kind == "palm":
        out += path(f"M{x-1.6*s},{y} Q{x+1*s},{y-10*s} {x+3*s},{y-20*s} L{x+5*s},{y-20*s} Q{x+3*s},{y-10*s} {x+1.6*s},{y} Z", "#B98D62", OL, 0.5)
        for i in range(4):
            out += line(x + (0 + i * 0.8) * s, y - (4 + i * 4.2) * s, x + (2.4 + i * 0.8) * s, y - (4.6 + i * 4.2) * s, "#9C7450", 0.5)
        tx, ty = x + 4 * s, y - 21 * s
        for ang, col in ((200, "#5E9E52"), (160, "#6FB05E"), (-20, "#5E9E52"), (20, "#6FB05E"), (250, "#7DBE6A"), (-70, "#7DBE6A")):
            r = math.radians(ang)
            ex, ey = tx + math.cos(r) * 13 * s, ty + math.sin(r) * 6 * s + 5 * s
            mx, my = tx + math.cos(r) * 6 * s, ty + math.sin(r) * 6 * s - 4 * s
            out += path(f"M{f(tx)},{f(ty)} Q{f(mx)},{f(my-2*s)} {f(ex)},{f(ey)} Q{f(mx)},{f(my+2*s)} {f(tx)},{f(ty)} Z", col, OL, 0.45)
        out += ell(tx - 1.2 * s, ty + 1.5 * s, 1.4 * s, 1.4 * s, "#8A6446", OL, 0.35) + ell(tx + 1.4 * s, ty + 1.8 * s, 1.4 * s, 1.4 * s, "#8A6446", OL, 0.35)
    elif kind == "planter":
        out += block(x - 6 * s, y - 5 * s, 12 * s, 3.5 * s, 3 * s, "#A9AFB5", "#8A9097", 1)
        out += rect(x - 0.9 * s, y - 11 * s, 1.8 * s, 7 * s, "#8A6446", 0.4, OL, 0.4)
        for dx, dy, r, col in ((-3, -14, 5, "#5E9E52"), (3, -14, 5, "#5E9E52"), (0, -18, 5.6, "#6FB05E"), (1.5, -19.5, 3, "#8FCB78")):
            out += ell(x + dx * s, y + dy * s, r * s, r * 0.9 * s, col, OL, 0.45)
    return out

def street_lamp(x, y, night=False):
    out = shadow(x + 1, y, 3, 1)
    out += rect(x - 2, y - 2, 4, 2, "#4F5560", 0.8, OL, 0.4) + rect(x - 0.6, y - 20, 1.2, 18, "#4F5560")
    out += path(f"M{x-3},{y-20} L{x+3},{y-20} L{x+2},{y-24} L{x-2},{y-24} Z", "#FFE9A8" if not night else "#FFF4C2", OL, 0.45)
    out += rect(x - 3.4, y - 25, 6.8, 1.4, "#4F5560", 0.6)
    if night:
        out += ell(x, y - 8, 12, 9, "rgba(255,230,150,.2)")
    return out

def grass_detail(x, y, w, h, th, seed=0):
    out = ""
    n = int(w * h / 900)
    for i in range(n):
        px = x + ((i * 73.7 + seed * 31) % w)
        py = y + ((i * 41.9 + seed * 17) % h)
        k = (i + seed) % 7
        if th in ("village", "forest"):
            col = shade(THEMES[th]["g2"], -0.15)
            out += path(f"M{f(px-1.2)},{f(py)} l0.6,-2.2 l0.6,2.2 l0.6,-1.8 l0.4,1.8", "none", col, 0.45)
            if th == "village" and k == 0:
                out += ell(px + 3, py - 1, 0.9, 0.9, ["#FFFFFF", "#F7D07A", "#F29A7F"][i % 3]) + ell(px + 3, py - 1, 0.35, 0.35, "#F2B84B")
            if th == "forest" and k == 1:
                out += ell(px, py, 2, 1.2, "#A8A290", OL, 0.3)
        elif th == "coast":
            if k < 3:
                out += path(f"M{f(px-2)},{f(py)} q2,-1 4,0", "none", shade(THEMES[th]["g2"], -0.12), 0.45)
            elif k == 3:
                out += path(f"M{f(px)},{f(py)} l1.2,-1.4 l1.2,1.4 z", "#F7C9B8", OL, 0.25)
        elif th == "city":
            if k == 0:
                out += ell(px, py, 0.6, 0.6, shade(THEMES[th]["g2"], -0.15))
    return out
