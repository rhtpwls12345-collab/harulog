import math
from art import *

SLOT_W, SLOT_H = 344, 224
GRID = {"small": (2, 2), "medium": (3, 2), "large": (4, 2)}

# ---------------------------------------------------------------- props (anchor = feet point x,y)
def p_gull(x, y):
    return (shadow(x, y + 6, 4, 1.2, 0.1) + path(f"M{x-6},{y-2} Q{x-3},{y-6} {x},{y-2} Q{x+3},{y-6} {x+6},{y-2} Q{x+3},{y-3.5} {x},{y-0.6} Q{x-3},{y-3.5} {x-6},{y-2} Z", "#FFFFFF", OL, 0.45)
            + ell(x + 0.2, y - 1.6, 1.4, 1, "#FFFFFF", OL, 0.35) + path(f"M{x+1.4},{y-1.6} l1.6,0.4 l-1.6,0.4 z", "#F2B84B"))

def p_parasol(x, y):
    out = shadow(x + 3, y, 12, 4) + line(x, y, x + 1, y - 20, "#8A6446", 1)
    for i in range(6):
        a0, a1 = math.radians(180 + i * 30), math.radians(180 + (i + 1) * 30)
        col = "#E06A52" if i % 2 == 0 else "#FFFDF6"
        out += path(f"M{x+1},{y-24} L{f(x+1+math.cos(a0)*13)},{f(y-18+math.sin(a0)*3)} L{f(x+1+math.cos(a1)*13)},{f(y-18+math.sin(a1)*3)} Z", col, OL, 0.45)
    out += path(f"M{x-12},{y-18} Q{x+1},{y-14} {x+14},{y-18}", "none", OL, 0.45) + ell(x + 1, y - 24.5, 1, 1, "#E06A52", OL, 0.3)
    out += block(x - 10, y - 4, 13, 4, 2, "#8CC7EE", "#6FB0DA", 1)
    return out

def p_surfboard(x, y):
    return (shadow(x + 1, y, 4, 1.2) + path(f"M{x},{y} C{x-4},{y-6} {x-3},{y-16} {x+1},{y-20} C{x+5},{y-16} {x+5},{y-6} {x},{y} Z", "#79C2DE", OL, 0.5)
            + path(f"M{x+0.8},{y-19} L{x},{y-1}", "none", "#FFFFFF", 0.8) + path(f"M{x-2.6},{y-9} q3,-1 5.6,0", "none", "#F2B84B", 0.9))

def p_sandcastle(x, y):
    out = shadow(x, y, 9, 2.5)
    out += block(x - 8, y - 7, 16, 3, 4, "#F0D9A6", "#D9BE87", 0.8)
    for dx in (-6, 0, 6):
        out += block(x + dx - 2.5, y - 13 - (3 if dx == 0 else 0), 5, 2, 6 + (3 if dx == 0 else 0), "#F4E0B4", "#DDC390", 0.6)
    out += line(x, y - 17, x, y - 22, "#8A6446", 0.5) + path(f"M{x},{y-22} l4,1.2 l-4,1.2 z", "#E06A52", OL, 0.3)
    out += ell(x + 9, y - 1, 1.5, 1, "#F7C9B8", OL, 0.3)
    return out

def p_lamp(x, y):
    return street_lamp(x, y)

def p_sign(x, y):
    return (shadow(x, y, 3, 1) + rect(x - 0.6, y - 16, 1.2, 16, "#7D848C") + rect(x - 7, y - 18, 14, 6, "#3E8C6A", 1, OL, 0.45)
            + path(f"M{x-4},{y-15} h7 m-2,-1.6 l2,1.6 l-2,1.6", "none", "#FFFFFF", 0.7) + rect(x - 5, y - 11, 10, 3.6, "#2F6FA8", 0.8, OL, 0.4))

def p_traffic(x, y):
    out = shadow(x, y, 3, 1) + rect(x - 0.7, y - 14, 1.4, 14, "#4F5560") + rect(x - 3.2, y - 24, 6.4, 11, "#3A3F45", 1.4, OL, 0.45)
    out += ell(x, y - 21.5, 1.6, 1.6, "#E0675A") + ell(x, y - 18.5, 1.6, 1.6, "#5A5F66") + ell(x, y - 15.5, 1.6, 1.6, "#6FCB8A")
    return out

def p_bench(x, y):
    out = shadow(x, y + 0.5, 10, 2)
    out += block(x - 9, y - 7, 18, 3.5, 3, "#D6AE80", "#B58C63", 0.8)
    out += block(x - 9, y - 12, 18, 1.6, 5, "#C9A076", "#A9805A", 0.8)
    out += rect(x - 8, y - 1, 1.5, 1.6, "#4F5560") + rect(x + 6.5, y - 1, 1.5, 1.6, "#4F5560")
    return out

def p_vending(x, y):
    out = shadow(x + 1, y, 7, 2)
    out += block(x - 5.5, y - 20, 11, 3, 17, "#E0675A", "#C9564B", 1.2)
    out += rect(x - 4, y - 15, 8, 7, "#DCEAF2", 0.6, OL, 0.35)
    for i in range(3):
        out += rect(x - 3.2 + i * 2.4, y - 14 + (i % 2), 1.6, 3.2, ["#8CB8E0", "#F2B84B", "#8DB596"][i], 0.4)
        out += rect(x - 3.2 + i * 2.4, y - 10, 1.6, 1.6, ["#F2EDE4", "#D98BA6", "#8CB8E0"][i], 0.4)
    out += rect(x - 3, y - 6, 6, 1.6, "#3A2E2A", 0.4) + rect(x + 2.5, y - 14, 1, 2, "#FFFFFF")
    return out

def p_planter(x, y):
    out = block(x - 9, y - 6, 18, 4, 3, "#A9AFB5", "#8A9097", 1)
    for i in range(6):
        cx = x - 7 + i * 2.8
        out += ell(cx, y - 6.5, 1.8, 1.4, "#6FB05E", OL, 0.3) + ell(cx, y - 7, 0.9, 0.9, ["#F29A7F", "#F2B84B", "#D98BA6", "#FFFFFF", "#F29A7F", "#B7A1D9"][i])
    return out

def p_scarecrow(x, y):
    out = shadow(x, y, 5, 1.4) + rect(x - 0.6, y - 18, 1.2, 18, "#8A6446")
    out += line(x - 9, y - 13, x + 9, y - 13, "#8A6446", 1.2)
    out += path(f"M{x-6},{y-15} L{x+6},{y-15} L{x+5},{y-6} L{x-5},{y-6} Z", "#6F8FB5", OL, 0.45) + rect(x - 1.5, y - 13, 3, 3, "#E06A52", 0.4)
    out += path(f"M{x-9},{y-13} l-2,2 M{x+9},{y-13} l2,2", "none", "#E8C35E", 0.8)
    out += ell(x, y - 18.5, 4, 3.6, "#F2DDB0", OL, 0.45) + ell(x - 1.4, y - 19, 0.5, 0.5, OL) + ell(x + 1.4, y - 19, 0.5, 0.5, OL) + path(f"M{x-1.4},{y-17.2} q1.4,1 2.8,0", "none", OL, 0.4)
    out += path(f"M{x-7},{y-21} L{x+7},{y-21} L{x+4},{y-23} L{x+3},{y-27} L{x-3},{y-27} L{x-4},{y-23} Z", "#C9A04E", OL, 0.45) + rect(x - 4, y - 23, 8, 1, "#E06A52")
    return out

def p_flowerbed(x, y):
    out = ell(x, y - 2, 11, 4.4, "#9A6E4C", OL, 0.45) + ell(x, y - 2.6, 9.6, 3.4, "#7DBA6A")
    pts = [(-7, -3, "#F29A7F"), (-4, -1.5, "#FFFFFF"), (-2, -4, "#F2B84B"), (1, -2, "#D98BA6"), (4, -4, "#FFFFFF"), (6.5, -2, "#F29A7F"), (3, -0.8, "#F2B84B"), (-5, -4.8, "#B7A1D9")]
    for dx, dy, c in pts:
        for a in range(5):
            r = math.radians(a * 72)
            out += ell(x + dx + math.cos(r) * 0.9, y + dy + math.sin(r) * 0.6, 0.7, 0.55, c)
        out += ell(x + dx, y + dy, 0.45, 0.4, "#F2B84B" if c != "#F2B84B" else "#E06A52")
    return out

def p_fence(x, y):
    out = shadow(x, y, 12, 1.4)
    out += rect(x - 12, y - 7.5, 24, 1.4, "#C9A076", 0.5, OL, 0.35) + rect(x - 12, y - 3.8, 24, 1.4, "#C9A076", 0.5, OL, 0.35)
    for i in range(4):
        px = x - 11 + i * 6.6
        out += path(f"M{px},{y} L{px},{y-9} L{px+1.3},{y-10.5} L{px+2.6},{y-9} L{px+2.6},{y} Z", "#DDB88C", OL, 0.45)
    return out

def p_haystack(x, y):
    out = shadow(x + 1, y, 8, 2) + path(f"M{x-8},{y} C{x-8},{y-8} {x-4},{y-11} {x},{y-11} C{x+4},{y-11} {x+8},{y-8} {x+8},{y} Z", "#E8C35E", OL, 0.5)
    for i in range(5):
        out += path(f"M{x-6+i*3},{y-1} q0.6,-3 0,-6", "none", "#C9A04E", 0.45)
    out += rect(x - 8, y - 5, 16, 1.2, "#C9A04E", 0.4)
    return out

def p_well(x, y):
    out = shadow(x + 1, y, 8, 2)
    out += block(x - 7, y - 9, 14, 4.5, 5, "#BDB7AA", "#9A9488", 1.6)
    for i in range(4):
        out += line(x - 7 + i * 4, y - 4.5, x - 7 + i * 4, y, "rgba(0,0,0,.12)", 0.4)
    out += ell(x, y - 6.8, 5, 1.8, "#34466E") + ell(x - 1.5, y - 7.2, 1.4, 0.4, "rgba(255,255,255,.4)")
    out += line(x - 5.5, y - 6, x - 5.5, y - 17, "#8A6446", 1) + line(x + 5.5, y - 6, x + 5.5, y - 17, "#8A6446", 1)
    out += path(f"M{x-8},{y-16} L{x},{y-21} L{x+8},{y-16} Z", "#C9564B", OL, 0.5) + line(x - 5.5, y - 13, x + 5.5, y - 13, "#7A5A42", 0.6)
    out += line(x, y - 13, x, y - 9.5, "#7A5A42", 0.4) + rect(x - 1.2, y - 10, 2.4, 2, "#9C7450", 0.3, OL, 0.3)
    return out

def p_deer(x, y):
    out = shadow(x, y, 7, 1.6)
    for lx in (-4, -2, 3, 5):
        out += line(x + lx, y - 6, x + lx, y, "#9C6B45", 1)
    out += ell(x, y - 8, 7, 3.6, "#C98B5A", OL, 0.45) + ell(x - 1, y - 8.6, 0.6, 0.6, "#FFFFFF") + ell(x + 2, y - 7.6, 0.6, 0.6, "#FFFFFF") + ell(x - 6.5, y - 9, 1.2, 1.4, "#FFFFFF", OL, 0.3)
    out += path(f"M{x+5},{y-10} L{x+7},{y-15} L{x+9},{y-14} L{x+7.5},{y-9} Z", "#C98B5A", OL, 0.45)
    out += ell(x + 8.5, y - 15.5, 2.6, 2, "#C98B5A", OL, 0.45) + ell(x + 9.6, y - 15.8, 0.5, 0.5, OL) + ell(x + 11, y - 15, 0.6, 0.5, OL)
    out += path(f"M{x+7.5},{y-17} l-1,-3 l-1.4,-0.6 M{x+6.9},{y-18.6} l1.2,-1 M{x+9},{y-17} l0.6,-3 l1.4,-0.6", "none", "#8A6446", 0.6)
    return out

def p_rabbit(x, y):
    return (shadow(x, y, 4, 1) + ell(x, y - 3, 4, 3, "#FFFFFF", OL, 0.45) + ell(x + 3.2, y - 5.6, 2.4, 2.2, "#FFFFFF", OL, 0.45)
            + path(f"M{x+2.4},{y-7.2} q-0.6,-4 0.6,-5 q1,1 0.4,5 Z M{x+4},{y-7.2} q0.4,-4 1.8,-4.4 q0.6,1.6 -0.6,4.6 Z", "#FFFFFF", OL, 0.4)
            + ell(x + 4, y - 5.8, 0.45, 0.45, OL) + ell(x - 4, y - 3, 1, 1, "#FFFFFF", OL, 0.3) + ell(x + 5.2, y - 4.8, 0.5, 0.35, "#F29A9A"))

def p_squirrel(x, y):
    return (shadow(x, y, 4, 1) + path(f"M{x-2},{y-2} C{x-9},{y-4} {x-9},{y-14} {x-3},{y-13} C{x-7},{y-10} {x-5},{y-6} {x-1},{y-4} Z", "#C9783E", OL, 0.45)
            + ell(x + 1, y - 3, 3, 2.6, "#D98B4E", OL, 0.45) + ell(x + 2.6, y - 6, 2.2, 2, "#D98B4E", OL, 0.45) + ell(x + 3.3, y - 6.3, 0.45, 0.45, OL)
            + path(f"M{x+1.6},{y-7.6} l0.4,-1.6 l0.8,1.2 z", "#C9783E", OL, 0.3) + ell(x + 3.6, y - 3, 1, 1.2, "#9C6B45", OL, 0.3))

def p_mushroom(x, y):
    out = ""
    for dx, s, c in ((-2.5, 1.0, "#D9534F"), (2.8, 0.75, "#E8B64C")):
        out += shadow(x + dx, y, 2.6 * s, 0.8 * s) + rect(x + dx - 0.9 * s, y - 3.6 * s, 1.8 * s, 3.6 * s, "#F2EDE4", 0.6 * s, OL, 0.35)
        out += path(f"M{x+dx-3*s},{y-3.4*s} Q{x+dx},{y-8*s} {x+dx+3*s},{y-3.4*s} Z", c, OL, 0.4)
        out += ell(x + dx - 1 * s, y - 5.2 * s, 0.6 * s, 0.5 * s, "#FFFFFF") + ell(x + dx + 1 * s, y - 4.4 * s, 0.45 * s, 0.4 * s, "#FFFFFF")
    return out

def p_log(x, y):
    return (shadow(x, y, 10, 1.6) + rect(x - 9, y - 6, 18, 5.6, "#9C6B45", 2.8, OL, 0.5) + line(x - 6, y - 4, x + 4, y - 4, "#7A5238", 0.4)
            + ell(x + 9, y - 3.2, 2, 2.8, "#E2C29A", OL, 0.45) + ell(x + 9, y - 3.2, 1, 1.4, "none", "#B98D62", 0.4)
            + ell(x - 3, y - 6, 2.4, 1, "#7FB86A", OL, 0.3) + ell(x + 1, y - 6.2, 1.2, 0.7, "#8FCB78"))

PROPS = {
    "coast":   [("gull", "갈매기", p_gull), ("parasol", "파라솔", p_parasol), ("surfboard", "서핑보드", p_surfboard), ("sandcastle", "모래성", p_sandcastle), ("palm", "야자수", lambda x, y: tree(x, y, "palm"))],
    "city":    [("lamp", "가로등", p_lamp), ("sign", "표지판", p_sign), ("traffic", "신호등", p_traffic), ("bench", "벤치", p_bench), ("vending", "자판기", p_vending), ("planter", "화단", p_planter)],
    "village": [("scarecrow", "허수아비", p_scarecrow), ("flowerbed", "꽃밭", p_flowerbed), ("fence", "나무 울타리", p_fence), ("haystack", "짚더미", p_haystack), ("well", "우물", p_well)],
    "forest":  [("deer", "사슴", p_deer), ("rabbit", "토끼", p_rabbit), ("squirrel", "다람쥐", p_squirrel), ("mushroom", "버섯", p_mushroom), ("log", "통나무", p_log), ("pine", "나무", lambda x, y: tree(x, y, "pine"))],
}
PROP_FN = {k: fn for th in PROPS.values() for k, _, fn in th}

# ---------------------------------------------------------------- slots (outdoor)
def park(bx, by, bw, bh, th):
    hedge = "#5E9E52"
    out = rect(bx, by, bw, bh, "#A9D58E", 6) + grass_detail(bx, by, bw, bh, "village", 3)
    out += rect(bx, by, bw, bh, "none", 6, hedge, 3.2) + rect(bx, by, bw, bh, "none", 6, OL, 0.5)
    # loop path
    out += rect(bx + 30, by + 50, bw - 60, bh - 64, "none", 10, "#E9DCC0", 9) + rect(bx + 30, by + 50, bw - 60, bh - 64, "none", 10, "#D3C19F", 0.6, ' stroke-dasharray="1 4"')
    out += rect(bx + bw / 2 - 5, by + bh - 18, 10, 22, "#E9DCC0")
    # pond
    pcx, pcy = bx + bw / 2, by + 84
    out += ell(pcx, pcy, 34, 13, "#C9C2B0", OL, 0.6) + ell(pcx, pcy, 31, 11, "#8CC7E6") + ell(pcx, pcy + 1.5, 28, 8.5, "#79B8DA")
    out += ell(pcx - 10, pcy - 3, 5, 1.2, "rgba(255,255,255,.55)") + ell(pcx + 12, pcy + 3, 3.2, 1.4, "#7DBA6A", OL, 0.3) + ell(pcx + 12, pcy + 2.4, 0.8, 0.6, "#F7B6C8")
    out += ell(pcx - 16, pcy + 2, 2.6, 1.1, "#7DBA6A", OL, 0.3)
    # stones around pond
    for i in range(10):
        a = i / 10 * math.tau
        out += ell(pcx + math.cos(a) * 33, pcy + math.sin(a) * 12.4, 2.2, 1.3, "#D8D2C2", OL, 0.3)
    # picnic mat + basket, bushes
    out += path(f"M{bx+70},{by+106} l26,-3 l4,14 l-26,3 z", "#F7C9B8", OL, 0.5)
    for i in range(4):
        out += line(bx + 71 + i * 6.5, by + 105.4 - i * 0.75, bx + 75 + i * 6.5, by + 119.6 - i * 0.75, "rgba(255,255,255,.7)", 1.2)
    out += block(bx + 82, by + 104, 9, 4, 4, "#D6AE80", "#B58C63", 1) + path(f"M{bx+83},{by+104} q3.5,-5 7,0", "none", "#9C7450", 0.7)
    for (ux, uy) in ((bx + 150, by + 120), (bx + 176, by + 122), (bx + 216, by + 108)):
        out += ell(ux, uy, 7, 4.6, "#6FB05E", OL, 0.45) + ell(ux - 2, uy - 1.5, 3, 1.8, "#8FCB78") + ell(ux + 3, uy - 0.6, 0.9, 0.9, "#F29A7F")
    out += p_bench(bx + 49, by + bh - 34) + street_lamp(bx + bw - 22, by + 104) + p_flowerbed(bx + bw - 54, by + bh - 26) + p_flowerbed(bx + 52, by + 40)
    for tx, ty in ((bx + 16, by + 40), (bx + bw - 18, by + 34), (bx + bw / 2 + 2, by + 30)):
        out += tree(tx, ty, THEMES[th]["tree"] if th != "city" else "round")
    out += sign_plate(bx + 30, by + bh + 3, "공원", "#6FA387")
    return out

def plaza(x, y, w, h, th):
    cx, cy = x + w / 2, y + h / 2 + 6
    out = rect(x + 20, y + 30, w - 40, h - 40, "#E7DDCB", 8, OL, 0.6)
    for yy in range(int(y + 38), int(y + h - 10), 9):
        for i, xx in enumerate(range(int(x + 26) + (yy // 9 % 2) * 6, int(x + w - 26), 12)):
            out += rect(xx, yy, 10, 7, "#EFE7D8" if i % 3 else "#DDD1BC", 1.5)
    out += ell(cx, cy + 4, 26, 10, "rgba(60,40,20,.15)") + ell(cx, cy, 24, 9, "#C9C2B0", OL, 0.6) + ell(cx, cy - 1, 20, 7, "#8CC7E6") + ell(cx, cy, 17, 5, "#79B8DA")
    out += block(cx - 3, cy - 10, 6, 2.5, 8, "#D8D2C2", "#BDB7AA", 1)
    out += path(f"M{cx},{cy-11} q-4,-8 -8,2 M{cx},{cy-11} q4,-8 8,2 M{cx},{cy-11} l0,-6", "none", "#BFE3F5", 1)
    out += p_bench(x + 60, y + h - 18) + p_bench(x + w - 60, y + h - 18) + p_planter(x + 46, y + 46) + p_planter(x + w - 46, y + 46)
    return out

def grove(x, y, w, h, th):
    kind = THEMES[th]["tree"]
    out = ell(x + w / 2, y + h / 2 + 10, w / 2 - 20, h / 2 - 22, shade(THEMES[th]["g2"], -0.06))
    pts = [(60, 70), (120, 56), (200, 66), (262, 78), (90, 120), (160, 112), (230, 130), (130, 160), (50, 150), (280, 150)]
    for i, (px, py) in enumerate(sorted(pts, key=lambda p: p[1])):
        out += tree(x + px, y + py, kind, 1.0 + (i % 3) * 0.12)
    out += p_mushroom(x + 110, y + 140) + p_log(x + 200, y + 158)
    return out

def empty_lot(x, y, w, h, th):
    out = rect(x + 30, y + 40, w - 60, h - 56, "none", 8, shade(THEMES[th]["g2"], -0.2), 1, ' stroke-dasharray="4 4"')
    out += rect(x + w / 2 - 0.6, y + h / 2 - 6, 1.2, 14, "#8A6446") + rect(x + w / 2 - 14, y + h / 2 - 14, 28, 10, "#FFFDF6", 2, OL, 0.5)
    out += f'<text x="{f(x+w/2)}" y="{f(y+h/2-8.6)}" font-family="Jua, sans-serif" font-size="6" fill="#7A5A42" text-anchor="middle" dominant-baseline="middle">빈 땅</text>'
    return out

# ---------------------------------------------------------------- roads
def road_h(x, y, w, h, th):
    t = THEMES[th]
    if th == "city":
        out = rect(x, y - 3, w, h + 6, "#B9BDC2") + rect(x, y, w, h, t["road"]) + rect(x, y - 3, w, 1, "#9EA3A9") + rect(x, y + h + 2, w, 1, "#9EA3A9")
        for xx in range(int(x) + 6, int(x + w), 22):
            out += rect(xx, y + h / 2 - 0.6, 11, 1.2, "#F2EFE6", 0.6)
        return out
    if th == "coast":
        out = rect(x, y, w, h, t["road"]) + rect(x, y, w, 1, t["roadE"]) + rect(x, y + h - 1, w, 1, t["roadE"])
        for xx in range(int(x), int(x + w), 6):
            out += rect(xx, y, 0.6, h, "rgba(110,75,40,.35)")
            out += ell(xx + 3, y + 2, 0.35, 0.35, "rgba(110,75,40,.4)") + ell(xx + 3, y + h - 2, 0.35, 0.35, "rgba(110,75,40,.4)")
        return out
    out = rect(x, y, w, h, t["road"]) + rect(x, y, w, 1.2, t["roadE"]) + rect(x, y + h - 1.2, w, 1.2, t["roadE"])
    for i, xx in enumerate(range(int(x) + 3, int(x + w), 9)):
        out += rect(xx, y + 3 + (i % 2) * 6, 6.5, 4.5, shade(t["road"], -0.06), 1.8) + rect(xx + 2, y + 12 - (i % 2) * 5, 5, 4, shade(t["road"], 0.08), 1.6)
    return out

def road_v(x, y, w, h, th):
    t = THEMES[th]
    if th == "city":
        out = rect(x, y, w, h, t["road"])
        for yy in range(int(y) + 8, int(y + h) - 8, 18):
            out += rect(x + w / 2 - 0.6, yy, 1.2, 9, "#F2EFE6", 0.6)
        for i in range(5):
            out += rect(x + 2, y + 4 + i * 3.4, w - 4, 1.8, "#F2EFE6", 0.4)
        return out
    out = rect(x, y, w, h, t["road"]) + rect(x, y, 1.2, h, t["roadE"]) + rect(x + w - 1.2, y, 1.2, h, t["roadE"])
    if th == "coast":
        for yy in range(int(y), int(y + h), 6):
            out += rect(x, yy, w, 0.6, "rgba(110,75,40,.35)")
        return out
    for i, yy in enumerate(range(int(y) + 3, int(y + h), 9)):
        out += rect(x + 3 + (i % 2) * 5, yy, 6, 5, shade(t["road"], -0.06), 1.8)
    return out

# ---------------------------------------------------------------- world
def world_svg(cfg, avatars=None, w_px=None, show_labels=True):
    """cfg = {theme, size, slots:[{kind,size,color,style}], props:{theme:[{k,x,y}]}}; avatars = [(svg_inner, x, y, h)]"""
    th = cfg["theme"]; t = THEMES[th]
    cols, rows = GRID[cfg["size"]]
    WW, WH = cols * SLOT_W + 24, rows * SLOT_H + 24 + (64 if th == "coast" else 0)
    out = []
    # ground
    out.append(rect(0, 0, WW, WH, t["g1"]))
    if th == "city":
        for yy in range(0, WH, 16):
            for xx in range((yy // 16 % 2) * 8, WW, 16):
                out.append(rect(xx + 0.4, yy + 0.4, 15.2, 15.2, t["g2"] if (xx // 16 + yy // 16) % 3 == 0 else t["g1"], 1.2))
    else:
        for i in range(int(WW * WH / 2600)):
            out.append(ell((i * 97.3) % WW, (i * 57.1) % WH, 14 + (i % 4) * 4, 6 + (i % 3) * 2, t["g2"]))
        out.append(grass_detail(0, 0, WW, WH, th))
    # roads
    for r in range(rows):
        out.append(road_h(0, 24 + r * SLOT_H + 180, WW, 24, th))
    for c in range(cols - 1):
        out.append(road_v(24 + c * SLOT_W + 322, 24 + 180, 20, (rows - 1) * SLOT_H, th))
    # sea
    if th == "coast":
        sy = rows * SLOT_H + 24
        wy = sy + 28
        out.append(rect(0, sy, WW, 28, "#F4E6C2") + grass_detail(0, sy, WW, 28, "coast", 5))
        out.append(rect(0, wy, WW, 64 - 28, "#7CC4E4") + rect(0, wy + 12, WW, 64 - 40, "#5FB0D8"))
        out.append(path(" ".join(f"M{x},{wy+2} q6,-4 12,0 t12,0" for x in range(0, WW, 24)), "none", "#FFFFFF", 1.6))
        out.append(rect(0, wy - 1.5, WW, 2.5, "rgba(255,255,255,.55)"))
        for i in range(24):
            out.append(path(f"M{(i*61)%WW},{wy+10+(i*13)%24} q3,-2 6,0", "none", "rgba(255,255,255,.6)", 0.8))
    # slots: outdoor first, then buildings sorted by y
    items = []
    for i, s in enumerate(cfg["slots"]):
        c, r = i % cols, i // cols
        sx0, sy0 = 24 + c * SLOT_W, 24 + r * SLOT_H
        bw, bh = BSIZES[s.get("size", "m")]
        bx, by = sx0 + (320 - bw) / 2, sy0 + 172 - bh
        k = s["kind"]
        if k in FURN:
            av = ""
            for (svg, ax, ay, ah, slot) in (avatars or []):
                if slot == i:
                    aw = ah * 172 / 270
                    av += f'<svg x="{f(ax-aw/2)}" y="{f(ay-ah*0.97)}" width="{f(aw)}" height="{f(ah)}" viewBox="14 18 172 270">{svg}</svg>'
            items.append((by, g(building(k, s.get("size", "m"), s.get("color", "cream"), s.get("style", "wood"), f"b{i}", av), bx, by)))
        elif k == "park":
            items.append((by, park(bx, by, bw, bh, th)))
        elif k == "plaza":
            items.append((sy0, plaza(sx0, sy0, 320, 176, th)))
        elif k == "grove":
            items.append((sy0, grove(sx0, sy0, 320, 176, th)))
        else:
            items.append((sy0, empty_lot(sx0, sy0, 320, 176, th)))
    for _, svg in sorted(items, key=lambda z: z[0]):
        out.append(svg)
    # roadside trees, lamps, bus stop, props + avatars on the street, sorted by y
    sprites = []
    kind = t["tree"]
    for r in range(rows):
        yy = 24 + r * SLOT_H + 214
        for xx in range(30, WW, 96 if th != "forest" else 64):
            if any(abs(xx - (24 + c * SLOT_W + 332)) < 18 for c in range(cols - 1)):
                continue
            if r == rows - 1 or True:
                sprites.append((yy + 16, tree(xx, yy + 16, kind, 0.9)))
    for x0 in (8, WW - 10):
        for yy in range(60, WH - 40, 60):
            sprites.append((yy, tree(x0, yy, kind, 0.85)))
    for r in range(rows):
        for c in range(cols):
            sprites.append((24 + r * SLOT_H + 210, street_lamp(24 + c * SLOT_W + 40, 24 + r * SLOT_H + 210)))
    bx, byy = 24 + 280, 24 + 210
    sprites.append((byy, rect(bx - 1, byy - 16, 1.4, 16, "#4F5560") + ell(bx - 0.3, byy - 17, 3.6, 3.6, "#2F6FA8", OL, 0.45)
                    + f'<text x="{f(bx-0.3)}" y="{f(byy-16.6)}" font-family="Jua, sans-serif" font-size="3.6" fill="#FFFFFF" text-anchor="middle" dominant-baseline="middle">BUS</text>'))
    for q in cfg.get("props", {}).get(th, []):
        sprites.append((q["y"], PROP_FN[q["k"]](q["x"], q["y"])))
    for (svg, ax, ay, ah, slot) in (avatars or []):
        if slot is None:
            aw = ah * 172 / 270
            sprites.append((ay, f'<svg x="{f(ax-aw/2)}" y="{f(ay-ah*0.97)}" width="{f(aw)}" height="{f(ah)}" viewBox="14 18 172 270">{svg}</svg>'))
    for _, svg in sorted(sprites, key=lambda z: z[0]):
        out.append(svg)
    return WW, WH, "".join(out)
