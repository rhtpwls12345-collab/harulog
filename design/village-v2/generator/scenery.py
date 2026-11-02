"""Theme scenery — landscape pieces, vehicles, animals. Anchor (0,0) = ground point (bottom centre) unless noted."""
import math
from art import *

DK = "#3A3F45"; GR = "#9AA6B0"; WH_ = "#FFFFFF"

# ============================================================ CITY
def tower(w=60, h=150, body="#9FB7C9", glass="#CFE3EE", kind="glass", seed=0):
    """anchor = bottom-left corner of the facade"""
    out = rect(4, -6, w, 8, "rgba(40,50,60,.18)", 2)
    out += rect(0, -h, w, h, body, 2, OL, 0.6)
    side = shade(body, -0.2)
    out += path(f"M{w},{-h} l8,-6 l0,{h} l-8,6 Z", side, OL, 0.5) + path(f"M0,{-h} l8,-6 l{w},0 l-8,6 Z", shade(body, 0.2), OL, 0.5)
    cols = max(2, int(w / 11)); rows = int((h - 22) / 13)
    for r in range(rows):
        for c in range(cols):
            lit = (r * 7 + c * 3 + seed) % 5 == 0
            x = 4 + c * (w - 8) / cols
            y = -h + 8 + r * 13
            if kind == "glass":
                out += rect(x, y, (w - 8) / cols - 2, 10, "#FFE9A8" if lit else glass, 0.6)
                out += line(x + 1, y + 8, x + 4, y + 2, "rgba(255,255,255,.5)", 0.6)
            elif kind == "brick":
                out += rect(x + 1, y + 1, (w - 8) / cols - 4, 8, "#FFE9A8" if lit else "#DCEAF2", 0.6, OL, 0.3) + rect(x, y + 9, (w - 8) / cols - 2, 1.4, shade(body, -0.25))
            else:
                out += rect(x, y + 2, (w - 8) / cols - 2, 6, "#FFE9A8" if lit else glass, 0.4)
    out += rect(w / 2 - 7, -14, 14, 14, "#4F5560", 1, OL, 0.45) + rect(w / 2 - 6, -13, 5.4, 12, "#BFE3F2", 0.4) + rect(w / 2 + 0.6, -13, 5.4, 12, "#BFE3F2", 0.4)
    out += rect(-2, -16, w + 4, 3, shade(body, -0.3), 1)
    return out

def tower_roof(w, h, kind):
    if kind == "tank":
        return block(w - 22, -h - 18, 12, 6, 10, "#C9A076", "#A9805A", 3) + line(w - 20, -h - 2, w - 20, -h - 6, DK, 1) + line(w - 12, -h - 2, w - 12, -h - 6, DK, 1)
    if kind == "antenna":
        return line(w / 2, -h - 6, w / 2, -h - 30, GR, 1.2) + ell(w / 2, -h - 31, 1.6, 1.6, "#E06A52")
    if kind == "sign":
        return rect(6, -h - 20, w - 12, 14, "#E06A52", 2, OL, 0.5) + f'<text x="{w/2}" y="{-h-10}" font-family="Jua, sans-serif" font-size="9" fill="#FFFFFF" text-anchor="middle">HARU</text>'
    return ""

def car_side(col="#E06A52", facing=1, kind="sedan"):
    """side view, anchor = road contact centre. facing 1 = right"""
    if kind == "bus":
        b = (rect(-28, -20, 56, 18, col, 4, OL, 0.6) + rect(-28, -8, 56, 3, WH_, 0)
             + "".join(rect(-24 + i * 9, -17, 7, 6, "#BFE3F2", 1, OL, 0.3) for i in range(5)) + rect(20, -17, 6, 12, "#BFE3F2", 1, OL, 0.3)
             + rect(-28, -20, 56, 18, "none", 4, OL, 0.6))
        wheels = [(-17, 0), (17, 0)]
    elif kind == "truck":
        b = (rect(-26, -22, 36, 20, "#F2EDE4", 2, OL, 0.6) + f'<text x="-8" y="-9" font-family="Jua, sans-serif" font-size="6" fill="#6FA387" text-anchor="middle">하루택배</text>'
             + path("M10,-2 L10,-16 L19,-16 L25,-9 L25,-2 Z", col, OL, 0.6) + path("M12,-14 L18,-14 L22,-9 L12,-9 Z", "#BFE3F2", OL, 0.3))
        wheels = [(-16, 0), (16, 0)]
    else:
        b = (path("M-18,-3 L-18,-9 Q-17,-11 -12,-11 L-8,-17 Q-6,-19 -2,-19 L7,-19 Q10,-19 12,-16 L15,-11 Q19,-11 19,-8 L19,-3 Z", col, OL, 0.6)
             + path("M-6.5,-16.5 L-2,-16.5 L-2,-11.5 L-10,-11.5 Z", "#BFE3F2", OL, 0.3) + path("M0,-16.5 L7,-16.5 Q9,-16.5 11,-13.5 L12,-11.5 L0,-11.5 Z", "#BFE3F2", OL, 0.3)
             + rect(-18, -6, 37, 1.4, "rgba(255,255,255,.35)") + ell(18, -8, 1.2, 1, "#FFF3B8") + rect(-18.4, -8, 1.4, 2, "#E06A52"))
        if kind == "taxi":
            b += rect(-4, -22, 8, 3, "#F7D07A", 1, OL, 0.35) + f'<text x="0" y="-19.8" font-family="Jua, sans-serif" font-size="2.4" fill="#3A3F45" text-anchor="middle">TAXI</text>'
            b += "".join(rect(-16 + i * 4, -6.4, 2, 1.4, "#3A3F45" if i % 2 else "#FFFFFF") for i in range(9))
        wheels = [(-11, 0), (12, 0)]
    for wx, wy in wheels:
        b += ell(wx, wy - 3, 4, 4, DK, OL, 0.4) + ell(wx, wy - 3, 1.8, 1.8, "#B9C4CD")
    out = ell(0, 0.6, 26 if kind in ("bus", "truck") else 20, 2.4, "rgba(40,40,40,.18)") + b
    return out if facing == 1 else f'<g transform="scale(-1,1)">{out}</g>'

def car_front(col="#E06A52", back=False):
    """front/back view for vertical roads, anchor = road contact centre"""
    out = ell(0, 0.6, 9, 2, "rgba(40,40,40,.18)")
    out += rect(-8, -11, 16, 9, col, 3, OL, 0.6) + path("M-6,-11 L-5,-18 L5,-18 L6,-11 Z", col, OL, 0.6) + path("M-4.6,-12 L-4,-16.6 L4,-16.6 L4.6,-12 Z", "#BFE3F2", OL, 0.3)
    out += rect(-8, -4, 2.4, 4, DK, 1) + rect(5.6, -4, 2.4, 4, DK, 1)
    if back:
        out += rect(-7, -8, 3, 1.6, "#E06A52", 0.6) + rect(4, -8, 3, 1.6, "#E06A52", 0.6) + rect(-3, -6, 6, 2, "#F2EDE4", 0.4, OL, 0.25)
    else:
        out += ell(-5, -7, 1.6, 1.3, "#FFF3B8", OL, 0.3) + ell(5, -7, 1.6, 1.3, "#FFF3B8", OL, 0.3) + rect(-3, -5.6, 6, 1.6, DK, 0.6)
    return out

def hydrant():
    return (shadow(0, 0, 4, 1.2) + rect(-3, -9, 6, 9, "#E06A52", 1.4, OL, 0.45) + ell(0, -9, 3.6, 1.6, "#C9564B", OL, 0.4) + ell(0, -10.4, 1.4, 1, "#C9564B", OL, 0.3)
            + rect(-5, -6, 10, 2.4, "#C9564B", 1, OL, 0.35))

def trashcan():
    return shadow(0, 0, 4, 1.2) + rect(-3.6, -10, 7.2, 10, "#6FA387", 1.4, OL, 0.45) + ell(0, -10, 4.2, 1.6, "#5A8C72", OL, 0.4) + line(-1.6, -8, -1.6, -2, "rgba(255,255,255,.3)", 0.8)

def foodtruck():
    return (ell(0, 0.6, 28, 2.6, "rgba(40,40,40,.18)") + rect(-26, -26, 46, 24, "#F7D07A", 3, OL, 0.6) + path("M20,-2 L20,-18 L26,-18 L30,-10 L30,-2 Z", "#F2B84B", OL, 0.6)
            + rect(-20, -22, 30, 11, "#5A4033", 1, OL, 0.4) + rect(-20, -22, 30, 2, "#E06A52") + path("M-22,-11 L12,-11 L14,-8 L-24,-8 Z", "#E06A52", OL, 0.4)
            + ell(-12, -16, 2, 1.4, "#F2B84B") + ell(-4, -16, 2, 1.4, "#E8B64C") + rect(2, -18, 5, 5, "#FFFFFF", 0.6, OL, 0.3)
            + f'<text x="-5" y="-23.4" font-family="Jua, sans-serif" font-size="3.2" fill="#E06A52" text-anchor="middle">떡볶이</text>'
            + ell(-16, -3, 4, 4, DK, OL, 0.4) + ell(-16, -3, 1.8, 1.8, "#B9C4CD") + ell(20, -3, 4, 4, DK, OL, 0.4) + ell(20, -3, 1.8, 1.8, "#B9C4CD"))

def subway():
    return (shadow(0, 0, 18, 2) + rect(-16, -8, 32, 8, "#4F5560", 1, OL, 0.5) + rect(-13, -6, 26, 6, DK, 0.6) + "".join(line(-12, -5 + i * 1.6, 12, -5 + i * 1.6, "#5A5F66", 0.6) for i in range(4))
            + rect(-18, -10, 2, 10, GR) + rect(16, -10, 2, 10, GR) + rect(-6, -22, 12, 10, "#2F6FA8", 2, OL, 0.45) + rect(-1, -12, 2, 4, GR)
            + f'<text x="0" y="-15" font-family="Jua, sans-serif" font-size="6" fill="#FFFFFF" text-anchor="middle">M</text>')

def billboard():
    return (shadow(0, 0, 12, 1.6) + rect(-1, -26, 2, 26, GR) + rect(-20, -44, 40, 20, "#FFFDF6", 1.4, OL, 0.6) + rect(-18, -42, 36, 16, "#F7C9B8", 0.6)
            + ell(-8, -34, 5, 5, "#FFFFFF", OL, 0.35) + path("M-11,-34 l3,-2 l3,2 l-3,2 z", "#E06A52") + f'<text x="6" y="-35" font-family="Jua, sans-serif" font-size="5" fill="#C9564B" text-anchor="middle">하루로그</text>'
            + f'<text x="6" y="-29" font-family="Jua, sans-serif" font-size="3" fill="#7A5A42" text-anchor="middle">오늘을 기록해요</text>')

def kiosk():
    return (shadow(0, 0, 10, 1.6) + rect(-9, -18, 18, 18, "#6FA387", 2, OL, 0.5) + path("M-11,-18 L11,-18 L9,-24 L-9,-24 Z", "#E06A52", OL, 0.45)
            + rect(-7, -15, 14, 7, "#FFFDF6", 0.6) + "".join(rect(-6 + i * 4.4, -14, 3.4, 5, c, 0.3, OL, 0.2) for i, c in enumerate(("#F7D07A", "#8CC7EE", "#F29A7F")))
            + rect(-7, -6, 14, 2, "#5A8C72", 0.4))

def pigeons():
    out = ""
    for (x, y, f) in ((-6, 0, 1), (3, 2, -1), (9, -1, 1)):
        b = ell(0, -2.4, 3, 2, "#9AA6B0", OL, 0.35) + ell(2.4, -4, 1.6, 1.5, "#7D848C", OL, 0.3) + path("M3.8,-4 l1.2,0.3 l-1.2,0.4 z", "#F2B84B") + path("M-2,-2.6 l-2.6,-0.6 l1,1.6 z", "#7D848C") + line(0, -0.6, 0, 0.4, "#E06A52", 0.4)
        out += f'<g transform="translate({x},{y}) scale({f},1)">{b}</g>'
    return out

def cone():
    return shadow(0, 0, 4, 1) + rect(-4, -1.4, 8, 1.4, "#E06A52", 0.4) + path("M-2.8,-1.4 L0,-10 L2.8,-1.4 Z", "#F29A4F", OL, 0.4) + path("M-1.8,-4.5 L1.8,-4.5 L1.3,-6.3 L-1.3,-6.3 Z", WH_)

def phonebooth():
    return (shadow(0, 0, 7, 1.4) + rect(-6, -26, 12, 26, "#E06A52", 1.4, OL, 0.5) + rect(-4.4, -22, 8.8, 18, "#BFE3F2", 0.6, OL, 0.3) + line(-4.4, -13, 4.4, -13, "#E06A52", 0.6)
            + rect(-6, -28, 12, 3, "#C9564B", 1, OL, 0.35) + rect(-1.6, -18, 3, 4, DK, 0.4))

CITY = [("tower_glass", "고층빌딩(유리)", lambda: tower(60, 150, "#9FB7C9", "#CFE3EE", "glass", 1) + tower_roof(60, 150, "antenna")),
        ("tower_brick", "아파트", lambda: tower(52, 110, "#D9A27E", "#DCEAF2", "brick", 2) + tower_roof(52, 110, "tank")),
        ("tower_office", "오피스 빌딩", lambda: tower(70, 128, "#B7C3CC", "#8CA9CC", "office", 3) + tower_roof(70, 128, "sign")),
        ("car", "승용차(가로)", lambda: car_side("#E06A52")), ("taxi", "택시", lambda: car_side("#F7D07A", 1, "taxi")),
        ("bus", "버스", lambda: car_side("#6FA387", 1, "bus")), ("truck", "택배 트럭", lambda: car_side("#2F6FA8", 1, "truck")),
        ("car_front", "승용차(세로·앞)", lambda: car_front("#8CB8E0")), ("car_back", "승용차(세로·뒤)", lambda: car_front("#B7A1D9", True)),
        ("foodtruck", "푸드트럭", foodtruck), ("subway", "지하철 입구", subway), ("billboard", "광고판", billboard), ("kiosk", "가판대", kiosk),
        ("hydrant", "소화전", hydrant), ("trashcan", "쓰레기통", trashcan), ("pigeons", "비둘기 떼", pigeons), ("cone", "공사 콘", cone), ("phonebooth", "공중전화", phonebooth)]

# ============================================================ FOREST
def stream(w=200, h=34):
    """anchor = top-left; a horizontal brook band"""
    out = path(f"M0,4 C{w*0.25},-4 {w*0.5},10 {w*0.75},2 S{w},6 {w},4 L{w},{h-4} C{w*0.75},{h+4} {w*0.5},{h-10} {w*0.25},{h-2} S0,{h-6} 0,{h-4} Z", "#C9C2B0", OL, 0.6)
    out += path(f"M0,7 C{w*0.25},-1 {w*0.5},13 {w*0.75},5 S{w},9 {w},7 L{w},{h-7} C{w*0.75},{h+1} {w*0.5},{h-13} {w*0.25},{h-5} S0,{h-9} 0,{h-7} Z", "#79B8DA")
    for i in range(int(w / 26)):
        x = 10 + i * 26
        out += path(f"M{x},{h/2+(i%2)*4-2} q4,-2 8,0", "none", "rgba(255,255,255,.7)", 0.8)
    for i in range(int(w / 40)):
        x = 18 + i * 40
        out += ell(x, h / 2 + (6 if i % 2 else -6), 4, 2.6, "#B5AFA0", OL, 0.4) + ell(x - 1, h / 2 + (5 if i % 2 else -7), 2, 1, "rgba(255,255,255,.5)")
    return out

def waterfall():
    out = path("M-26,0 L-24,-40 Q-10,-50 0,-46 Q14,-50 26,-40 L28,0 Z", "#A8A290", OL, 0.6) + path("M-24,-40 Q-10,-50 0,-46 Q14,-50 26,-40 L22,-36 Q0,-44 -20,-36 Z", "#7FB86A", OL, 0.45)
    out += rect(-8, -40, 16, 40, "#9AD3EC", 2) + "".join(line(-6 + i * 3, -38, -6 + i * 3, -2, "rgba(255,255,255,.7)", 0.8) for i in range(5))
    out += ell(0, 0, 16, 5, "#79B8DA", OL, 0.45) + ell(-6, -1, 4, 1.6, "rgba(255,255,255,.8)") + ell(6, 0, 3, 1.4, "rgba(255,255,255,.8)")
    out += ell(-20, -14, 5, 4, "#B5AFA0", OL, 0.4) + ell(20, -10, 6, 4, "#B5AFA0", OL, 0.4) + ell(-22, -16, 2.4, 1.4, "#7FB86A")
    return out

def bridge():
    out = shadow(0, 2, 26, 3) + path("M-26,0 Q0,-12 26,0 L26,6 Q0,-6 -26,6 Z", "#B98D62", OL, 0.6)
    for i in range(9):
        x = -22 + i * 5.5
        y = -0.2 * (26 - abs(x)) * 0.45
        out += line(x, y - 0.5, x, y + 5.5, "#9C7450", 0.5)
    out += path("M-26,-6 Q0,-18 26,-6", "none", "#7A5A42", 1.2) + "".join(line(x, -6 - 0.45 * (26 - abs(x)) * 0.45, x, 0.0 - 0.45 * (26 - abs(x)) * 0.45, "#7A5A42", 1) for x in (-24, -12, 0, 12, 24))
    return out

def meadow(w=60, h=26):
    out = ell(0, 0, w / 2, h / 2, "#9BCB7E")
    cols = ("#FFFFFF", "#F7D07A", "#F29A7F", "#D98BA6", "#B7A1D9")
    for i in range(int(w * h / 22)):
        a = i * 2.39996
        r = math.sqrt(i / (w * h / 22))
        x, y = math.cos(a) * r * w / 2 * 0.9, math.sin(a) * r * h / 2 * 0.9
        c = cols[i % 5]
        out += line(x, y, x, y + 1.6, "#5E9E52", 0.4) + ell(x, y, 1.1, 0.9, c) + ell(x, y, 0.4, 0.4, "#F2B84B" if c != "#F7D07A" else "#E06A52")
    return out

def fox():
    return (shadow(0, 0, 7, 1.4) + path("M-7,-4 C-14,-6 -14,-12 -9,-12 C-11,-9 -9,-6 -5,-6 Z", "#E8793A", OL, 0.4) + path("M-13.4,-10 q-1,-2 1,-2.6", "none", WH_, 1.2)
            + ell(-1, -4.6, 6, 3.4, "#E8793A", OL, 0.45) + line(-4, -2, -4, 0, OL, 0.9) + line(2, -2, 2, 0, OL, 0.9)
            + path("M3,-6 L5,-11 L7,-9 L9,-11 L10,-6 Q10,-3 6.5,-2.4 Q3,-3 3,-6 Z", "#E8793A", OL, 0.45) + path("M5,-5 Q6.5,-2.8 8.4,-5 Q6.5,-3.6 5,-5", WH_)
            + ell(5.6, -6.6, 0.5, 0.5, OL) + ell(8.2, -6.6, 0.5, 0.5, OL) + ell(6.9, -4.4, 0.6, 0.45, OL))

def bearcub():
    return (shadow(0, 0, 8, 1.6) + ell(0, -6, 7, 6, "#9C6B45", OL, 0.5) + ell(-4, -1, 2.4, 1.6, "#9C6B45", OL, 0.4) + ell(4, -1, 2.4, 1.6, "#9C6B45", OL, 0.4)
            + ell(0, -15, 5.4, 5, "#9C6B45", OL, 0.5) + ell(-4.4, -19, 2, 2, "#9C6B45", OL, 0.4) + ell(4.4, -19, 2, 2, "#9C6B45", OL, 0.4) + ell(-4.4, -19, 0.9, 0.9, "#D9B48A")
            + ell(4.4, -19, 0.9, 0.9, "#D9B48A") + ell(0, -13, 2.6, 2, "#D9B48A") + ell(0, -13.8, 0.9, 0.6, OL) + ell(-2, -16, 0.5, 0.5, OL) + ell(2, -16, 0.5, 0.5, OL) + ell(0, -6, 3.6, 3, "#D9B48A"))

def owl():
    return (shadow(0, 0, 6, 1.4) + rect(-6, -8, 12, 8, "#9C6B45", 2, OL, 0.45) + ell(0, -8, 6, 1.6, "#D9B48A", OL, 0.4) + ell(0, -8, 3, 0.8, "none", "#B98D62", 0.4)
            + ell(0, -14, 4, 5, "#8A6446", OL, 0.45) + path("M-3.6,-18 l-1,-2.6 l2.4,1.4 z M3.6,-18 l1,-2.6 l-2.4,1.4 z", "#8A6446", OL, 0.3)
            + ell(-1.6, -15.6, 1.6, 1.6, WH_, OL, 0.3) + ell(1.6, -15.6, 1.6, 1.6, WH_, OL, 0.3) + ell(-1.6, -15.6, 0.7, 0.7, OL) + ell(1.6, -15.6, 0.7, 0.7, OL)
            + path("M-0.6,-14 l0.6,1.2 l0.6,-1.2 z", "#F2B84B") + ell(0, -12, 2, 1.6, "#D9B48A"))

def ducks():
    out = ""
    for i, (x, s) in enumerate(((-8, 1), (2, 0.8), (9, 0.8))):
        c = "#FFFFFF" if i == 0 else "#F7D07A"
        out += f'<g transform="translate({x},0) scale({s})">' + ell(0, -2.4, 4, 2.4, c, OL, 0.4) + ell(3, -5, 2, 1.8, c, OL, 0.35) + path("M4.6,-5 l1.8,0.4 l-1.8,0.6 z", "#F2B84B") + ell(3.4, -5.4, 0.35, 0.35, OL) + path("M-5,-1 q4,1.6 9,0", "none", "rgba(255,255,255,.7)", 0.6) + "</g>"
    return out

def butterflies():
    out = ""
    for (x, y, c) in ((-6, -10, "#F7D07A"), (5, -16, "#D98BA6"), (10, -7, "#8CC7EE")):
        out += ell(x - 1.6, y, 1.8, 1.3, c, OL, 0.25) + ell(x + 1.6, y, 1.8, 1.3, c, OL, 0.25) + line(x, y - 1.2, x, y + 1.2, OL, 0.5) + path(f"M{x-4},{y+4} q2,-2 4,0", "none", "rgba(80,60,40,.25)", 0.3, ' stroke-dasharray="0.6 0.8"')
    return out

def hedgehog():
    out = shadow(0, 0, 5, 1.2) + path("M-6,-1 Q-6,-8 0,-8 Q5,-8 6,-3 L6,-1 Z", "#7A5A42", OL, 0.45)
    for i in range(6):
        out += path(f"M{-5+i*2},{-7+abs(i-2.5)*0.6} l1,-2.4 l1,2.4", "none", "#5A4033", 0.5)
    return out + ell(6, -2.4, 2.4, 1.6, "#E2C29A", OL, 0.35) + ell(8.3, -2.6, 0.5, 0.5, OL) + ell(6.6, -3.2, 0.35, 0.35, OL)

def tent():
    return (shadow(0, 0, 18, 2.4) + path("M-18,0 L0,-24 L18,0 Z", "#F2B84B", OL, 0.6) + path("M0,-24 L18,0 L10,0 Z", "#E39A3A") + path("M-6,0 L0,-12 L6,0 Z", "#7A5238", OL, 0.45)
            + line(0, -24, 0, -28, OL, 0.6) + path("M0,-28 l4,1 l-4,1 z", "#E06A52") + line(-18, 0, -24, 2, "#9C7450", 0.4) + line(18, 0, 24, 2, "#9C7450", 0.4))

def campfire():
    out = shadow(0, 0, 9, 2) + "".join(ell(math.cos(i / 8 * math.tau) * 7, math.sin(i / 8 * math.tau) * 2.4 - 1, 2, 1.4, "#B5AFA0", OL, 0.3) for i in range(8))
    out += line(-5, -1, 5, -3, "#8A6446", 1.6) + line(-5, -3, 5, -1, "#9C6B45", 1.6)
    out += path("M-4,-2 Q-5,-8 -1,-12 Q-1,-8 1,-9 Q2,-13 0,-16 Q6,-11 4,-2 Z", "#F29A4F", OL, 0.4) + path("M-2,-2 Q-2,-6 0,-8 Q1,-5 2,-6 Q3,-4 2,-2 Z", "#F7D07A")
    out += ell(0, -6, 12, 7, "rgba(255,200,120,.15)")
    for (x, y) in ((-10, 2), (11, 1)):
        out += rect(x - 4, y - 2, 8, 3, "#9C6B45", 1.4, OL, 0.35)
    return out

def fireflies():
    return "".join(ell(x, y, 2.4, 2.4, "rgba(255,240,150,.35)") + ell(x, y, 0.8, 0.8, "#FFF3B8") for (x, y) in ((-8, -6), (-2, -14), (5, -9), (10, -16), (2, -20), (-10, -18)))

def birdhouse():
    return (shadow(0, 0, 4, 1) + rect(-0.8, -18, 1.6, 18, "#8A6446") + rect(-5, -27, 10, 10, "#F2C9A8", 0.8, OL, 0.45) + path("M-6.6,-26 L0,-32 L6.6,-26 Z", "#C9564B", OL, 0.45)
            + ell(0, -23, 1.8, 1.8, "#5A4033") + line(0, -19.6, 0, -18.6, OL, 0.6) + ell(4, -31, 1.8, 1.4, "#8CC7EE", OL, 0.3) + path("M5.4,-31 l1,0.3 l-1,0.3 z", "#F2B84B"))

def berrybush():
    out = shadow(0, 0, 9, 2) + ell(-4, -5, 6, 5, "#4C8E5D", OL, 0.45) + ell(4, -5, 6, 5, "#4C8E5D", OL, 0.45) + ell(0, -9, 6, 5, "#5E9E52", OL, 0.45)
    return out + "".join(ell(x, y, 1, 1, "#C9364B") for (x, y) in ((-5, -6), (-2, -10), (3, -8), (6, -4), (1, -4), (-6, -2)))

FOREST = [("stream", "계곡 물줄기", lambda: stream(160, 34)), ("waterfall", "작은 폭포", waterfall), ("bridge", "나무 다리", bridge), ("meadow", "꽃밭", lambda: meadow(60, 26)),
          ("fox", "여우", fox), ("bearcub", "아기 곰", bearcub), ("owl", "부엉이(그루터기)", owl), ("ducks", "오리 가족", ducks), ("butterflies", "나비", butterflies),
          ("hedgehog", "고슴도치", hedgehog), ("tent", "텐트", tent), ("campfire", "모닥불", campfire), ("fireflies", "반딧불이", fireflies), ("birdhouse", "새집", birdhouse),
          ("berrybush", "산딸기 덤불", berrybush)]

# ============================================================ COAST
def lighthouse():
    out = ell(0, 0, 26, 8, "#A8A290", OL, 0.6) + ell(-10, -3, 8, 4, "#B5AFA0", OL, 0.4) + ell(12, -2, 9, 4, "#B5AFA0", OL, 0.4)
    out += path("M-9,-4 L-6,-60 L6,-60 L9,-4 Z", WH_, OL, 0.6)
    for i in range(3):
        y0 = -10 - i * 17
        out += path(f"M{-9+i*1},{y0} L{-8.5+i*1},{y0-8} L{8.5-i*1},{y0-8} L{9-i*1},{y0} Z", "#E06A52")
    out += path("M-9,-4 L-6,-60 L6,-60 L9,-4 Z", "none", OL, 0.6) + rect(-3, -14, 6, 10, "#7A5A42", 3, OL, 0.4)
    out += rect(-9, -63, 18, 3, DK, 1) + rect(-6, -73, 12, 10, "#FFF3B8", 1, OL, 0.5) + "".join(line(-6 + i * 4, -73, -6 + i * 4, -63, DK, 0.6) for i in range(4))
    out += path("M-8,-73 Q0,-82 8,-73 Z", "#E06A52", OL, 0.5) + ell(0, -82, 1.4, 1.4, DK)
    out += path("M6,-70 L40,-78 L40,-62 Z", "rgba(255,240,170,.35)") + path("M-6,-70 L-40,-78 L-40,-62 Z", "rgba(255,240,170,.25)")
    return out

def fishboat():
    return (ell(0, 2, 26, 3, "rgba(30,80,120,.25)") + path("M-24,-8 L24,-8 L18,2 L-18,2 Z", "#2F6FA8", OL, 0.6) + rect(-24, -9, 48, 2.4, WH_, 0, OL, 0.4)
            + rect(-4, -22, 16, 14, WH_, 1.4, OL, 0.5) + rect(-2, -19, 5, 5, "#BFE3F2", 0.6, OL, 0.3) + rect(5, -19, 5, 5, "#BFE3F2", 0.6, OL, 0.3) + rect(-6, -24, 20, 3, "#E06A52", 1, OL, 0.4)
            + line(-14, -9, -14, -34, "#7A5A42", 1) + line(-14, -32, -2, -24, GR, 0.4) + line(-14, -32, -22, -12, GR, 0.4)
            + path("M-22,-12 q4,4 8,0 q-2,6 -6,4 z", "none", "#8A6446", 0.4, ' stroke-dasharray="0.8 0.8"') + rect(-22, -12, 4, 3, "#F29A4F", 0.8, OL, 0.3)
            + path("M-14,-34 l6,1.6 l-6,1.6 z", "#F7D07A") + ell(18, -10, 1.6, 1.6, "#F2B84B", OL, 0.3))

def sailboat():
    return (ell(0, 2, 16, 2.4, "rgba(30,80,120,.25)") + path("M-16,-5 L16,-5 L11,2 L-11,2 Z", "#FFFDF6", OL, 0.55) + rect(-16, -5, 32, 1.6, "#E06A52")
            + line(0, -5, 0, -40, "#7A5A42", 1) + path("M1,-38 L18,-8 L1,-8 Z", WH_, OL, 0.5) + path("M-1,-34 L-14,-8 L-1,-8 Z", "#8CC7EE", OL, 0.5) + path("M0,-40 l5,1.4 l-5,1.4 z", "#F7D07A"))

def pier():
    out = ""
    for i in range(6):
        out += rect(-3 + (i % 2) * 18, -10 + i * 10, 2.4, 14, "#7A5A42", 0.6, OL, 0.35)
    out += rect(-4, -18, 26, 70, "#C9A47A", 1, OL, 0.6)
    for i in range(14):
        out += rect(-4, -18 + i * 5, 26, 0.6, "rgba(110,75,40,.4)")
    out += rect(-5, -18, 1.4, 70, "#9C7450") + rect(21.6, -18, 1.4, 70, "#9C7450")
    return out

def lifeguard():
    return (shadow(0, 0, 12, 2) + path("M-10,0 L-6,-20 M10,0 L6,-20 M-8,-10 L8,-10", "none", WH_, 1.6) + path("M-10,0 L-6,-20 M10,0 L6,-20", "none", OL, 0.3)
            + block(-9, -26, 18, 6, 4, "#E06A52", "#C9564B", 1) + path("M-12,-28 L12,-28 L8,-36 L-8,-36 Z", "#FFFFFF", OL, 0.45) + path("M-4,-36 L4,-36 L5,-28 L-5,-28 Z", "#E06A52")
            + rect(-5, -24, 10, 3, WH_, 0.6) + path("M-2,-22.6 h4 m-2,-1.4 v2.8", "none", "#E06A52", 0.8))

def crab():
    return (shadow(0, 0, 6, 1.2) + ell(0, -3, 5, 3, "#E06A52", OL, 0.45) + path("M-5,-3 l-3,-2 M5,-3 l3,-2 M-4,-1 l-3,1 M4,-1 l3,1", "none", "#E06A52", 0.8)
            + ell(-8, -6, 1.8, 1.4, "#E06A52", OL, 0.35) + ell(8, -6, 1.8, 1.4, "#E06A52", OL, 0.35) + line(-1.4, -6, -1.4, -7.4, OL, 0.4) + line(1.4, -6, 1.4, -7.4, OL, 0.4)
            + ell(-1.4, -7.6, 0.7, 0.7, WH_, OL, 0.25) + ell(1.4, -7.6, 0.7, 0.7, WH_, OL, 0.25))

def shells():
    star = "M0,-5 L1.2,-1.6 L4.8,-1.6 L1.9,0.6 L3,4 L0,1.9 L-3,4 L-1.9,0.6 L-4.8,-1.6 L-1.2,-1.6 Z"
    return (f'<g transform="translate(-5,-3)">{path(star, "#F29A4F", OL, 0.4)}</g>' + path("M4,-1 q3,-6 6,0 z", "#F7C9B8", OL, 0.35) + "".join(line(7, -1, 5 + i * 1.2, -4, "#E8A9A0", 0.3) for i in range(4))
            + ell(1, 1, 1.4, 1, "#FFFFFF", OL, 0.3))

def buoy():
    return (ell(0, 1, 7, 2, "rgba(30,80,120,.25)") + path("M-5,0 Q-5,-6 0,-7 Q5,-6 5,0 Z", "#E06A52", OL, 0.45) + rect(-5, -3, 10, 1.6, WH_) + line(0, -7, 0, -13, DK, 0.8) + ell(0, -14, 1.6, 1.6, "#F7D07A", OL, 0.3))

def fishcrates():
    out = ""
    for (x, y) in ((-12, 0), (2, 0), (-5, -9)):
        out += block(x, y - 9, 13, 5, 5, "#C9A076", "#A9805A", 0.6) + ell(x + 4, y - 7, 2.4, 1.2, "#8CB8E0", OL, 0.25) + ell(x + 9, y - 7, 2.4, 1.2, "#B9C4CD", OL, 0.25)
    out += path("M14,0 Q20,-10 26,0 Z", "#9C7450", OL, 0.4) + "".join(line(16 + i * 2, 0, 18 + i * 1.4, -6, "rgba(255,255,255,.5)", 0.3) for i in range(4))
    return out

def fishstall():
    return (shadow(0, 0, 20, 2) + block(-18, -14, 36, 10, 10, "#FFFDF6", "#DDE1E5") + rect(-17, -13, 34, 8, "#BFE3F2", 1)
            + "".join(path(f"M{-13+i*6},-9 q2.4,-2 4.8,0 q-2.4,2 -4.8,0 l-1.2,-1 l0,2 z", ["#8CB8E0", "#F29A7F", "#B9C4CD", "#8CB8E0", "#F29A7F", "#B9C4CD"][i], OL, 0.25) for i in range(6))
            + rect(-20, -30, 1.6, 26, "#7A5A42") + rect(18.4, -30, 1.6, 26, "#7A5A42") + path("M-22,-30 L22,-30 L19,-24 L-19,-24 Z", "#2F6FA8", OL, 0.45)
            + "".join(path(f"M{-19+i*7.6},-24 q3.8,3 7.6,0", "#2F6FA8" if i % 2 else WH_, OL, 0.3) for i in range(5))
            + f'<text x="0" y="-25.6" font-family="Jua, sans-serif" font-size="4" fill="#FFFFFF" text-anchor="middle">수산</text>')

def volleyball():
    return (shadow(0, 0, 22, 2) + line(-22, 0, -22, -20, "#7A5A42", 1.2) + line(22, 0, 22, -20, "#7A5A42", 1.2)
            + rect(-22, -20, 44, 8, "none", 0, WH_, 0.6) + "".join(line(-22 + i * 4, -20, -22 + i * 4, -12, "rgba(255,255,255,.7)", 0.3) for i in range(12))
            + "".join(line(-22, -20 + i * 2, 22, -20 + i * 2, "rgba(255,255,255,.7)", 0.3) for i in range(5)) + rect(-22, -21, 44, 1.4, WH_)
            + ell(10, -28, 3, 3, "#FFFFFF", OL, 0.4) + path("M7,-28 q3,-2 6,0 M10,-31 q-1.4,3 0,6", "none", "#F7D07A", 0.6))

def beachhut():
    return (shadow(0, 0, 14, 2) + rect(-12, -22, 24, 22, "#8CC7EE", 1, OL, 0.55) + "".join(rect(-12 + i * 4, -22, 2, 22, "#FFFFFF") for i in range(6))
            + rect(-12, -22, 24, 22, "none", 1, OL, 0.55) + path("M-15,-22 L0,-32 L15,-22 Z", "#E06A52", OL, 0.5) + rect(-4, -14, 8, 14, "#F7D07A", 0.6, OL, 0.4) + ell(2, -7, 0.7, 0.7, OL))

def kayak():
    return (shadow(0, 1, 18, 2) + path("M-20,-2 Q0,-9 20,-2 Q0,4 -20,-2 Z", "#F29A4F", OL, 0.5) + ell(0, -3, 5, 1.8, DK) + line(-14, -10, 14, 4, "#7A5A42", 0.8)
            + path("M-16,-11 l-3,-1 l1,3 z M16,5 l3,1 l-1,-3 z", "#F7D07A", OL, 0.3))

def towel():
    return (path("M-12,-4 L10,-6 L13,4 L-9,6 Z", "#8CC7EE", OL, 0.45) + "".join(path(f"M{-11+i*4},{-4-i*0.4} L{-8+i*4},{5.6-i*0.4}", "none", WH_, 1.1) for i in range(6))
            + ell(-6, 0, 3, 1.4, "#FFFFFF", OL, 0.3) + path("M6,-1 l3,-1 l1,3 l-3,1 z", "#F7D07A", OL, 0.3))

COAST = [("lighthouse", "등대", lighthouse), ("fishboat", "고기잡이 배", fishboat), ("sailboat", "돛단배", sailboat), ("pier", "나무 부두", pier),
         ("lifeguard", "인명구조 망루", lifeguard), ("crab", "꽃게", crab), ("shells", "불가사리·조개", shells), ("buoy", "부표", buoy),
         ("fishcrates", "생선 상자·그물", fishcrates), ("fishstall", "수산 가판", fishstall), ("volleyball", "비치발리볼 네트", volleyball), ("beachhut", "비치 오두막", beachhut),
         ("kayak", "카약", kayak), ("towel", "비치 타월", towel)]

# ============================================================ VILLAGE (시골)
def field(w=80, h=40, crop="cabbage"):
    """anchor = top-left"""
    out = rect(0, 0, w, h, "#A9805A", 3, OL, 0.6)
    rows = int(h / 8)
    for r in range(rows):
        y = 4 + r * 8
        out += rect(2, y - 1, w - 4, 3, "#8A6446", 1.4)
        for i in range(int((w - 8) / 8)):
            x = 6 + i * 8
            if crop == "cabbage":
                out += ell(x, y, 3, 2.4, "#8FCB78", OL, 0.35) + ell(x, y - 0.4, 1.6, 1.2, "#B7E3A0")
            elif crop == "carrot":
                out += path(f"M{x},{y} l-1.6,-3 M{x},{y} l0,-3.6 M{x},{y} l1.6,-3", "none", "#5E9E52", 0.8) + ell(x, y + 0.6, 1.2, 0.8, "#F29A4F")
            else:
                out += path(f"M{x-2},{y+1} l0.4,-5 M{x},{y+1} l0,-5.6 M{x+2},{y+1} l-0.4,-5", "none", "#C9A04E", 0.6) + ell(x, y - 5, 1.2, 1.8, "#E8C35E")
    return out

def barn():
    return (shadow(0, 0, 30, 3) + rect(-26, -30, 52, 30, "#C9564B", 1, OL, 0.6) + "".join(line(-26 + i * 4, -30, -26 + i * 4, 0, "rgba(0,0,0,.12)", 0.5) for i in range(1, 13))
            + path("M-30,-28 L-18,-46 L18,-46 L30,-28 Z", "#7A5238", OL, 0.6) + path("M-30,-28 L-18,-46 L18,-46 L30,-28", "none", "#FFFFFF", 1.2)
            + rect(-10, -20, 20, 20, "#A94540", 0.6, OL, 0.5) + path("M-10,-20 L10,0 M10,-20 L-10,0", "none", "#FFFFFF", 1.2) + rect(-10, -20, 20, 20, "none", 0.6, "#FFFFFF", 1)
            + rect(-5, -40, 10, 8, "#FFF3B8", 0.6, OL, 0.4) + line(0, -40, 0, -32, "#7A5238", 0.6))

def windmill(t=0):
    out = shadow(0, 0, 12, 2) + path("M-9,0 L-5,-40 L5,-40 L9,0 Z", "#F2EDE4", OL, 0.6) + rect(-3, -12, 6, 12, "#7A5A42", 3, OL, 0.4) + ell(0, -26, 2, 2.4, "#8CC7EE", OL, 0.35)
    out += path("M-7,-40 L0,-48 L7,-40 Z", "#C9564B", OL, 0.5)
    for i in range(4):
        a = math.radians(45 + i * 90 + t)
        ex, ey = math.cos(a) * 24, -42 + math.sin(a) * 24
        px, py = -math.sin(a) * 4, math.cos(a) * 4
        out += path(f"M0,-42 L{f(ex)},{f(ey)} L{f(ex+px)},{f(ey+py)} L{f(px*0.4)},{f(-42+py*0.4)} Z", "#FFFDF6", OL, 0.45)
        out += line(0, -42, ex, ey, "#9C7450", 0.8)
    return out + ell(0, -42, 2, 2, "#7A5A42", OL, 0.4)

def chicken(c="#FFFFFF"):
    return (shadow(0, 0, 4, 1) + ell(0, -4, 4, 3.2, c, OL, 0.4) + ell(3, -7.4, 2.2, 2.2, c, OL, 0.4) + path("M2.4,-9.6 l0.6,-1.4 l0.8,1 l0.6,-1 l0.4,1.6 z", "#E06A52")
            + path("M5,-7.4 l1.6,0.4 l-1.6,0.6 z", "#F2B84B") + ell(3.6, -7.8, 0.4, 0.4, OL) + path("M-4,-5 l-2,-2 l0.6,3 z", c, OL, 0.3) + line(-1, -1, -1, 0, "#F2B84B", 0.6) + line(1, -1, 1, 0, "#F2B84B", 0.6))

def cow():
    return (shadow(0, 0, 12, 2) + "".join(line(x, -6, x, 0, "#5A4033", 1.4) for x in (-8, -5, 5, 8)) + rect(-11, -14, 22, 10, WH_, 5, OL, 0.5)
            + ell(-5, -11, 3.6, 2.6, "#3A2E2A") + ell(5, -8, 2.6, 2, "#3A2E2A") + ell(12, -14, 4, 4, WH_, OL, 0.45) + ell(13, -11.6, 3.4, 2, "#F7C9B8", OL, 0.35)
            + ell(12.2, -11.6, 0.4, 0.4, OL) + ell(14.6, -11.6, 0.4, 0.4, OL) + ell(11, -15.4, 0.5, 0.5, OL) + path("M9,-17 l-2,-2 M15,-17 l2,-2", "none", "#E2C29A", 1)
            + path("M-11,-12 q-3,2 -2,6", "none", OL, 0.6) + ell(0, -4, 2, 1.2, "#F7C9B8", OL, 0.3))

def sheep():
    out = shadow(0, 0, 8, 1.6) + "".join(line(x, -4, x, 0, OL, 1) for x in (-4, -1.6, 2, 4.4))
    for (x, y) in ((-5, -8), (-1, -10), (3, -9), (5, -6), (-4, -5), (1, -5)):
        out += ell(x, y, 3.4, 3, WH_, OL, 0.35)
    for (x, y) in ((-5, -8), (-1, -10), (3, -9), (5, -6), (-4, -5), (1, -5)):
        out += ell(x, y, 2.8, 2.4, WH_)
    return out + ell(8, -8, 2.6, 2.2, "#3A2E2A", OL, 0.35) + ell(7.2, -10, 1.4, 0.8, "#3A2E2A") + ell(8.8, -8.4, 0.5, 0.5, WH_)

def pumpkins():
    out = path("M-14,0 q6,-4 10,-1 q6,-4 12,0 q4,-2 6,1", "none", "#5E9E52", 0.8)
    for (x, s) in ((-8, 1), (4, 1.3), (14, 0.8)):
        out += shadow(x, 0, 5 * s, 1.2) + ell(x, -3.4 * s, 5 * s, 3.4 * s, "#F29A4F", OL, 0.45) + path(f"M{x-2*s},{-6.4*s} q-1,3 0,6 M{x+2*s},{-6.4*s} q1,3 0,6", "none", "#D9772F", 0.5) + rect(x - 0.6, -8 * s, 1.2, 2 * s, "#5E9E52", 0.4)
    return out + ell(-2, -4, 3, 1.6, "#6FB05E", OL, 0.3)

def jangdok():
    out = shadow(0, 0, 22, 3) + rect(-22, -6, 44, 6, "#B5AFA0", 1, OL, 0.5) + "".join(rect(-22 + i * 8.8, -6, 8.8, 6, "none", 0, "rgba(0,0,0,.12)", 0.4) for i in range(5))
    for (x, y, s) in ((-14, -6, 1.2), (0, -6, 1.4), (14, -6, 1.1), (-7, -1, 0.8), (8, -1, 0.85)):
        out += path(f"M{x-6*s},{y-9*s} Q{x-8*s},{y-4*s} {x-4*s},{y} L{x+4*s},{y} Q{x+8*s},{y-4*s} {x+6*s},{y-9*s} Z", "#7A4A32", OL, 0.45)
        out += ell(x, y - 9 * s, 5 * s, 1.8 * s, "#5A3424", OL, 0.4) + ell(x, y - 10.2 * s, 2 * s, 0.9 * s, "#5A3424", OL, 0.3) + path(f"M{x-4*s},{y-7*s} q2,-1 3,0", "none", "rgba(255,255,255,.35)", 0.6)
    return out

def beehive():
    return (shadow(0, 0, 8, 1.6) + rect(-1, -6, 2, 6, "#8A6446") + block(-7, -20, 14, 4, 4, "#F2EDE4", "#D8CDBE", 1) + block(-7, -14, 14, 4, 6, "#F7D07A", "#E7C878", 1)
            + path("M-8,-20 L0,-24 L8,-20 Z", "#C9A076", OL, 0.45) + rect(-2, -6.6, 4, 1, OL) + "".join(ell(x, y, 1.2, 0.9, "#F2B84B", OL, 0.25) for (x, y) in ((10, -18), (12, -12), (-11, -16))))

def tractor():
    return (ell(0, 0.6, 18, 2.4, "rgba(40,40,40,.18)") + rect(-14, -14, 20, 8, "#6FA387", 2, OL, 0.55) + rect(2, -24, 12, 14, "#6FA387", 1.4, OL, 0.55) + rect(4, -22, 8, 6, "#BFE3F2", 0.6, OL, 0.3)
            + rect(-10, -20, 2, 6, DK) + ell(-9, -22, 1.4, 1, "#8C9AA6") + ell(8, -6, 7, 7, DK, OL, 0.45) + ell(8, -6, 3, 3, "#F7D07A") + ell(-10, -4, 4.4, 4.4, DK, OL, 0.45) + ell(-10, -4, 1.8, 1.8, "#F7D07A"))

def laundry():
    out = shadow(0, 0, 22, 1.6) + line(-22, 0, -22, -24, "#8A6446", 1.2) + line(22, 0, 22, -24, "#8A6446", 1.2) + path("M-22,-22 Q0,-17 22,-22", "none", GR, 0.5)
    for i, c in enumerate(("#8CC7EE", "#F7C9B8", "#FFFFFF", "#F7D07A")):
        x = -16 + i * 10
        y = -21 + 3.5 * (1 - ((x / 22) ** 2))
        out += (path(f"M{x-3},{y} l6,0 l1,3 l-1.6,0 l0,7 l-5.8,0 l0,-7 l-1.6,0 z", c, OL, 0.35) if i % 2 == 0 else rect(x - 3.4, y, 6.8, 9, c, 0.4, OL, 0.35)) + line(x - 1.6, y - 0.6, x - 1.6, y + 1, "#C9A076", 0.6)
    return out

def mailbox():
    return (shadow(0, 0, 4, 1) + rect(-0.8, -12, 1.6, 12, "#8A6446") + path("M-6,-12 L-6,-18 Q-6,-21 0,-21 Q6,-21 6,-18 L6,-12 Z", "#E06A52", OL, 0.45)
            + line(-6, -16, 6, -16, "rgba(255,255,255,.4)", 0.5) + rect(5, -22, 1.2, 6, "#7A5A42") + rect(6, -22, 4, 2.4, "#F7D07A", 0.4, OL, 0.25))

def stepstones():
    out = ""
    for i in range(6):
        out += ell(-20 + i * 8, (i % 2) * 2, 3.6, 2, "#D8D2C2", OL, 0.4) + ell(-21 + i * 8, (i % 2) * 2 - 0.6, 1.6, 0.6, "rgba(255,255,255,.5)")
    return out

def persimmon():
    out = tree(0, 0, "round", 1.15)
    return out + "".join(ell(x, y, 1.5, 1.4, "#F2862E", OL, 0.3) for (x, y) in ((-5, -17), (4, -22), (6, -14), (-2, -24), (-7, -12), (1, -16)))

def duckpond_small():
    return ell(0, -2, 18, 7, "#C9C2B0", OL, 0.5) + ell(0, -2, 15, 5.4, "#79B8DA") + ell(-4, -3, 3, 1.4, "rgba(255,255,255,.5)") + ducks()

VILLAGE = [("field_cabbage", "배추밭", lambda: field(80, 40, "cabbage")), ("field_carrot", "당근밭", lambda: field(64, 32, "carrot")), ("field_wheat", "밀밭", lambda: field(80, 40, "wheat")),
           ("barn", "빨간 헛간", barn), ("windmill", "풍차", lambda: windmill(0)), ("chicken", "닭", lambda: chicken() + f'<g transform="translate(9,2)">{chicken("#E8B64C")}</g>'),
           ("cow", "젖소", cow), ("sheep", "양", sheep), ("pumpkins", "호박밭", pumpkins), ("jangdok", "장독대", jangdok), ("beehive", "벌통", beehive),
           ("tractor", "트랙터", tractor), ("laundry", "빨랫줄", laundry), ("mailbox", "우체통", mailbox), ("stepstones", "징검다리", stepstones), ("persimmon", "감나무", persimmon)]

SCENERY = {"city": ("콘크리트 도시", CITY), "forest": ("숲속 마을", FOREST), "coast": ("해안 도시", COAST), "village": ("시골 마을", VILLAGE)}
