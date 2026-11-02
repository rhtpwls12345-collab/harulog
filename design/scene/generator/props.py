"""Exercise props & effects. Anchor (0,0) = character's feet centre (character ~34 tall, facing right for side props).
Reference points on a standing Haru avatar (front view): shoulder y=-14.5, hands (±4.9,-8.6), eyes (±2.3,-21.2), head centre y=-22.4, head top y=-27.8."""
import math
from pets import E, Pth, Ln, SL, n, OL

DK = "#3A3F45"; GR = "#9AA6B0"; RED = "#E06A52"; BLU = "#2F6FA8"; YEL = "#F2B84B"

def R(x, y, w, h, c, rx=0, o=True):
    s = f' stroke="{OL}" stroke-width="0.38"' if o else ""
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(rx)}" fill="{c}"{s}></rect>'

def plate(x, y, h, c):
    return R(x - 0.9, y - h / 2, 1.8, h, c, 0.7) + R(x - 0.2, y - h / 2 + 0.6, 0.6, h - 1.2, "rgba(255,255,255,.3)", 0.3, False)

def barbell(y=-15.0, half=14):
    out = R(-half, y - 0.45, half * 2, 0.9, "#B9C4CD", 0.45)
    for s in (-1, 1):
        out += plate(s * (half - 4.2), y, 7.2, RED) + plate(s * (half - 2.4), y, 5.6, BLU) + plate(s * (half - 0.9), y, 4.0, YEL)
        out += R(s * (half - 5.6) - 0.6, y - 1.1, 1.2, 2.2, DK, 0.4)
    return out

def barbell_rack():
    out = E(0, 0.3, 15, 1.4, "rgba(60,40,20,.16)", False)
    for x in (-11, 11):
        out += R(x - 0.8, -18, 1.6, 18, "#5A5F66", 0.5) + R(x - 2.6, -0.8, 5.2, 1.2, DK, 0.5) + R(x - 1.6, -16.6, 2.4, 1.0, DK, 0.4)
    return out + barbell(-17, 14)

def spin_back():
    """spin bike — rear layer (drawn behind the rider). side view facing right; seat top at y=-11.5"""
    out = E(0, 0.4, 13, 1.4, "rgba(60,40,20,.18)", False)
    out += R(-10, -1.4, 20, 1.4, DK, 0.7)
    out += Pth("M-7,-1.4 L-3,-10 L-1.4,-10 L-5,-1.4 Z", "#4F5560") + Pth("M-3,-10 L6,-7 L6.6,-8.6 L-2.4,-11.6 Z", "#4F5560")
    out += E(3.6, -5.2, 4.6, 4.6, "#5A5F66") + E(3.6, -5.2, 3.2, 3.2, "#8C9AA6", False) + E(3.6, -5.2, 1.0, 1.0, DK)
    out += R(-5.4, -12.6, 5.2, 1.6, DK, 0.8) + R(-3.4, -11.2, 1.0, 2.4, "#5A5F66", 0.3)
    return out

def spin_front(f=0):
    """spin bike — front layer (handlebar + near pedal). f = 0/1 pedal phase"""
    a = math.radians(30 + f * 180)
    px, py = 3.6 + math.cos(a) * 2.6, -5.2 + math.sin(a) * 2.6
    out = Ln(3.6, -5.2, px, py, "#3A3F45", 0.9) + R(px - 1.3, py - 0.4, 2.6, 0.8, DK, 0.3)
    out += Pth("M6,-7 L8,-15.6 L9.4,-15.6 L7.6,-7 Z", "#4F5560") + R(7.2, -17, 5.2, 1.4, DK, 0.7) + R(10.6, -17.6, 1.2, 2.4, RED, 0.5)
    out += R(7.6, -19.4, 3.4, 2.0, "#8CC7EE", 0.5)
    return out

def bicycle_back():
    out = E(0, 0.4, 14, 1.3, "rgba(60,40,20,.16)", False)
    for cx in (-8, 8):
        out += f'<circle cx="{cx}" cy="-4.4" r="4.4" fill="none" stroke="{DK}" stroke-width="1.1"></circle><circle cx="{cx}" cy="-4.4" r="0.7" fill="{GR}"></circle>'
        out += "".join(Ln(cx, -4.4, cx + math.cos(math.radians(a)) * 4, -4.4 + math.sin(math.radians(a)) * 4, "#B9C4CD", 0.2) for a in range(0, 360, 45))
    out += SL("M-8,-4.4 L-2,-4.4 L-4,-11 Z M-2,-4.4 L5,-11 L-4,-11 M5,-11 L8,-4.4", "#6FA387", 1.0)
    out += R(-6.2, -12.6, 4.6, 1.4, DK, 0.7)
    return out

def bicycle_front(f=0):
    a = math.radians(40 + f * 180)
    px, py = -2 + math.cos(a) * 2.4, -4.4 + math.sin(a) * 2.4
    out = Ln(-2, -4.4, px, py, DK, 0.8) + R(px - 1.2, py - 0.4, 2.4, 0.8, DK, 0.3)
    out += SL("M5,-11 L6,-15 L8.6,-15.4", "#6FA387", 1.0) + R(7.4, -16.2, 2.6, 1.4, DK, 0.6) + E(9.6, -12, 1.2, 0.9, "#F7D07A")
    out += E(5.2, -8.2, 2.2, 1.6, "#C9A076") + SL("M3.2,-8.6 q2,-1.6 4,0", "#9C7450", 0.4)
    return out

def yoga_mat(c="#B7A1D9"):
    return (E(0, 0.5, 13, 1.5, "rgba(60,40,20,.14)", False) + Pth("M-12,-3 L12,-3 L13,1.6 L-13,1.6 Z", c) + Pth("M-12,-3 L12,-3 L12.3,-1.6 L-12.3,-1.6 Z", "rgba(255,255,255,.25)", False)
            + E(-13, -0.6, 1.2, 2.4, c) + SL("M-13,-2.6 q-1,2 0,4", "rgba(0,0,0,.2)", 0.3))

def yoga_aura():
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="0.7"></circle>' for x, y, r in ((-9, -26, 0.6), (8, -28, 0.8), (-6, -32, 0.5), (10, -22, 0.5))) + \
        SL("M-6,-31 q6,-4 12,0", "#B7A1D9", 0.5)

def glove(x=0, y=0, c=RED, flip=False):
    g = (Pth("M-2,-1.6 Q-2.4,-3.4 -0.4,-3.6 L1.8,-3.6 Q3.4,-3.4 3.2,-1.4 L3.2,1.2 Q3,2.6 1.4,2.6 L-1.2,2.6 Q-2.2,2.4 -2.2,1.2 Z", c)
         + Pth("M-2.2,1.6 L-2.6,3.6 L1.2,3.6 L1.4,2.6 Z", "#FFFFFF") + SL("M-2,-1.4 q1.4,1 0,2.6", "rgba(0,0,0,.25)", 0.35) + E(1.6, -2.4, 0.9, 0.5, "rgba(255,255,255,.45)", False))
    t = f"translate({n(x)},{n(y)})" + (" scale(-1,1)" if flip else "")
    return f'<g transform="{t}">{g}</g>'

def gloves_guard():
    return glove(-3.4, -12.6, RED, True) + glove(3.4, -12.6, RED)

def gloves_jab(side=1):
    return glove(-3.4 * side, -12.6, RED, side > 0) + glove(8.6 * side, -14.6, RED, side < 0) + SL(f"M{n(11.2*side)},-17 l1.6,-1 M{n(11.8*side)},-14.6 l2,0 M{n(11.2*side)},-12.2 l1.6,1", "#F2B84B", 0.5)

def sandbag(ang=0):
    out = E(0, 0.4, 6, 1.2, "rgba(60,40,20,.16)", False)
    out += R(-0.6, -36, 1.2, 36, "#5A5F66", 0.4) + R(-3.4, -36, 10, 1.6, "#5A5F66", 0.6) + R(-2.6, -0.8, 5.2, 1.2, DK, 0.5)
    bag = (SL("M0,0 L0,4", "#8C9AA6", 0.4) + R(-3, 4, 6, 15, RED, 3) + R(-3, 6, 6, 1, "rgba(0,0,0,.18)", 0, False) + R(-3, 16, 6, 1, "rgba(0,0,0,.18)", 0, False)
           + R(-2.2, 5, 1.2, 12, "rgba(255,255,255,.3)", 0.6, False))
    return out + f'<g transform="translate(5,-35) rotate({n(ang)})">{bag}</g>'

def water(f=0):
    out = E(0, -6, 13, 4.2, "#79B8DA") + E(0, -6.6, 11.4, 3.2, "#9AD3EC", False)
    for i, (x, y) in enumerate(((-9, -7), (8, -5.6), (-3, -3.6))):
        dx = (f * 1.2) * (-1 if i % 2 else 1)
        out += SL(f"M{n(x+dx)},{n(y)} q1.4,-0.9 2.8,0", "#FFFFFF", 0.5)
    out += "".join(f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}" fill="#FFFFFF" stroke="{OL}" stroke-width="0.2"></circle>' for x, y, r in ((-6 - f, -11, 0.7), (6 + f, -12, 0.55), (4, -10.5 - f, 0.45)))
    return out

def water_front():
    """front lip of the water that covers the body below the neck"""
    return Pth("M-13,-6 Q0,-1 13,-6 L13,-1 Q0,3 -13,-1 Z", "#79B8DA", False) + SL("M-13,-6 Q0,-1.6 13,-6", "#FFFFFF", 0.6)

def goggles(c="#2F6FA8"):
    return (SL("M-4.8,-21.4 Q0,-23.6 4.8,-21.4", c, 0.8) + E(-2.3, -21.2, 1.6, 1.2, "#BFE6F2") + E(2.3, -21.2, 1.6, 1.2, "#BFE6F2")
            + f'<ellipse cx="-2.3" cy="-21.2" rx="1.6" ry="1.2" fill="none" stroke="{c}" stroke-width="0.6"></ellipse><ellipse cx="2.3" cy="-21.2" rx="1.6" ry="1.2" fill="none" stroke="{c}" stroke-width="0.6"></ellipse>'
            + Ln(-0.7, -21.2, 0.7, -21.2, c, 0.5) + E(-2.8, -21.6, 0.5, 0.3, "#FFFFFF", False) + E(1.8, -21.6, 0.5, 0.3, "#FFFFFF", False))

def swim_cap(c="#E06A52"):
    return Pth("M-5.6,-23 Q-5.8,-29.4 0,-29.4 Q5.8,-29.4 5.6,-23 Q0,-24.6 -5.6,-23 Z", c) + E(-2, -27.6, 1.2, 0.6, "rgba(255,255,255,.4)", False)

def sweat(x=6, y=-24):
    return Pth(f"M{n(x)},{n(y)} q-1.2,1.8 0,2.6 q1.2,-0.8 0,-2.6 Z", "#8CC7EE") + Pth(f"M{n(x-10)},{n(y+3)} q-0.9,1.4 0,2 q0.9,-0.6 0,-2 Z", "#8CC7EE")

def treadmill_side():
    out = E(0, 0.4, 13, 1.3, "rgba(60,40,20,.16)", False)
    out += R(-11, -2.6, 22, 2.6, DK, 1.3) + R(-10, -2.2, 18, 1.0, "#5A5F66", 0.5)
    out += Pth("M8,-2.6 L10,-16 L11.4,-16 L10,-2.6 Z", "#4F5560") + R(8.6, -18.2, 5.2, 3, "#4F5560", 0.8) + R(9.4, -17.6, 3.4, 1.6, "#8CC7EE", 0.3)
    return out

# effects for interactions & moods
def heart(x=0, y=-30, s=1, c="#FF5C8A"):
    return f'<g transform="translate({n(x)},{n(y)}) scale({n(s)})">' + Pth("M0,1.8 C-3,-0.4 -2,-3 0,-1.4 C2,-3 3,-0.4 0,1.8 Z", c) + "</g>"

def spark(x, y, s=1, c="#F2B84B"):
    d = "M0,-3 L0.7,-0.7 L3,0 L0.7,0.7 L0,3 L-0.7,0.7 L-3,0 L-0.7,-0.7 Z"
    return f'<g transform="translate({n(x)},{n(y)}) scale({n(s)})">' + Pth(d, c) + "</g>"

def wave_lines(x, y):
    return SL(f"M{n(x)},{n(y)} q1,-1.6 0,-3.2 M{n(x+1.6)},{n(y+0.6)} q1.4,-2.2 0,-4.4", "#7A6E62", 0.45)

def note(x, y):
    return SL(f"M{n(x)},{n(y)} l0,-3.6 l2.4,-0.8 l0,3.2", "#6F8FB5", 0.5) + E(x - 0.6, y, 0.8, 0.6, "#6F8FB5", False) + E(x + 1.8, y - 0.6, 0.8, 0.6, "#6F8FB5", False)

def zzz(x, y):
    return f'<text x="{n(x)}" y="{n(y)}" font-family="Jua, sans-serif" font-size="3.4" fill="#7A8CB8">z</text><text x="{n(x+2.4)}" y="{n(y-2.8)}" font-family="Jua, sans-serif" font-size="2.4" fill="#7A8CB8">z</text>'

def leash(x1, y1, x2, y2, sag=3, c="#E06A52"):
    mx, my = (x1 + x2) / 2, max(y1, y2) + sag
    d = f"M{n(x1)},{n(y1)} Q{n(mx)},{n(my)} {n(x2)},{n(y2)}"
    return SL(d, "#3A2E2A", 0.9) + SL(d, c, 0.5) + E(x1, y1, 0.6, 0.6, c)

PROPS = [
    ("barbell", "바벨(어깨 위)", lambda: barbell(), "-16 -21 32 12"),
    ("barbell-rack", "바벨 랙", barbell_rack, "-17 -24 34 26"),
    ("spin-bike-back", "스피닝 바이크(뒤 레이어)", spin_back, "-12 -20 26 22"),
    ("spin-bike-front-1", "스피닝 바이크(앞 레이어·페달 1)", lambda: spin_front(0), "-12 -20 26 22"),
    ("spin-bike-front-2", "스피닝 바이크(앞 레이어·페달 2)", lambda: spin_front(1), "-12 -20 26 22"),
    ("bike-back", "자전거(뒤 레이어)", bicycle_back, "-14 -18 28 20"),
    ("bike-front-1", "자전거(앞 레이어·페달 1)", lambda: bicycle_front(0), "-14 -18 28 20"),
    ("bike-front-2", "자전거(앞 레이어·페달 2)", lambda: bicycle_front(1), "-14 -18 28 20"),
    ("yoga-mat", "요가 매트", yoga_mat, "-15 -5 30 8"),
    ("yoga-aura", "요가 반짝임", yoga_aura, "-12 -35 24 16"),
    ("gloves-guard", "복싱 글러브(가드)", gloves_guard, "-8 -18 16 10"),
    ("gloves-jab", "복싱 글러브(잽)", lambda: gloves_jab(1), "-8 -20 24 12"),
    ("sandbag-1", "샌드백(왼쪽 흔들림)", lambda: sandbag(8), "-6 -38 18 40"),
    ("sandbag-2", "샌드백(가운데)", lambda: sandbag(0), "-6 -38 18 40"),
    ("sandbag-3", "샌드백(오른쪽 흔들림)", lambda: sandbag(-8), "-6 -38 18 40"),
    ("water-1", "수영 물결 1", lambda: water(0), "-14 -14 28 12"),
    ("water-2", "수영 물결 2", lambda: water(1), "-14 -14 28 12"),
    ("water-front", "수영 물 앞면(몸 가림)", water_front, "-14 -8 28 12"),
    ("goggles", "수경", goggles, "-6 -24 12 5"),
    ("swim-cap", "수영모", swim_cap, "-7 -31 14 9"),
    ("sweat", "땀방울", sweat, "-6 -26 14 6"),
    ("treadmill-side", "러닝머신(옆)", treadmill_side, "-12 -19 27 21"),
]
FX = [("heart", "하트", lambda: heart(0, 0, 1.4), "-5 -4 10 7"), ("spark", "하이파이브 반짝", lambda: spark(0, 0, 1.2), "-4 -4 8 8"),
      ("wave", "손 흔들기 선", lambda: wave_lines(0, 0), "-1 -6 5 7"), ("note", "음표", lambda: note(0, 0), "-2 -6 6 7"), ("zzz", "졸림", lambda: zzz(0, 0), "-1 -6 7 7")]
