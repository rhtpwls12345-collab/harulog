"""Harulog pets — dogs & cats, facing right, feet centre at (0,0), logical units (body ~12-14 wide).
Recolourable faces use style="fill:var(--fur,…)" / var(--fur-dark,…). Gear uses var(--gear,…)."""
import math

OL = "#3A2E2A"
SW = 0.38
FUR = ("--fur", "#C98B5A")
FURD = ("--fur-dark", "#9C6440")
GEAR = ("--gear", "#E06A52")
WHITE = "#FFF8EE"
PINK = "#F4A7A0"
FUR_DARK_MAP = {"#C98B5A": "#9C6440", "#F2EDE4": "#CFC2AE", "#3A2E2A": "#221A17", "#E8C79A": "#C49C66", "#9AA3B5": "#6F7A8E"}

def fl(c):
    if isinstance(c, tuple):
        return f'fill="{c[1]}" style="fill:var({c[0]},{c[1]})"'
    return f'fill="{c}"'

def sk(c):
    if isinstance(c, tuple):
        return f'stroke="{c[1]}" style="stroke:var({c[0]},{c[1]})"'
    return f'stroke="{c}"'

def n(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")

def E(cx, cy, rx, ry, c, o=True, rot=0, extra=""):
    s = f' stroke="{OL}" stroke-width="{SW}"' if o else ""
    t = f' transform="rotate({n(rot)} {n(cx)} {n(cy)})"' if rot else ""
    return f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" {fl(c)}{s}{t}{extra}></ellipse>'

def Pth(d, c, o=True, extra=""):
    s = f' stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round"' if o else ""
    return f'<path d="{d}" {fl(c)}{s}{extra}></path>'

def Ln(x1, y1, x2, y2, c, w):
    return f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" {sk(c)} stroke-width="{n(w)}" stroke-linecap="round"></line>'

def SL(d, c=OL, w=0.35):
    return f'<path d="{d}" fill="none" {sk(c)} stroke-width="{n(w)}" stroke-linecap="round" stroke-linejoin="round"></path>'

def leg(x1, y1, x2, y2, c, w=1.5, paw=None):
    out = Ln(x1, y1, x2, y2, OL, w + 0.75) + Ln(x1, y1, x2, y2, c, w)
    if paw:
        out += E(x2 + 0.25, y2 - 0.35, w * 0.55, 0.42, paw, True)
    return out

def shadow(rx=6, cx=0):
    return f'<ellipse cx="{n(cx)}" cy="0.2" rx="{n(rx)}" ry="1.1" fill="rgba(60,40,20,.16)"></ellipse>'

def eye(x, y, closed=False):
    if closed:
        return SL(f"M{n(x-0.6)},{n(y)} q0.6,0.5 1.2,0", OL, 0.35)
    return E(x, y, 0.48, 0.55, OL, False) + E(x + 0.15, y - 0.2, 0.17, 0.17, "#FFFFFF", False)

# ---------------------------------------------------------------- gait
DX_A = [1.4, 0.4, -1.4, -0.4]
DX_B = [-1.4, -0.4, 1.4, 0.4]
LIFT_A = [0, 0, 0, 0.9]
LIFT_B = [0, 0.9, 0, 0]
BOB = [0, -0.25, 0, -0.25]
WAG = [28, 48, 28, 8]

def gear_layer(cx, cy, body_rx, harness_x, harness_y, h=4.6):
    """collar ring + harness. returns svg, ring point"""
    col = f'<g class="gear-collar">' + E(cx, cy, 0.45, 1.35, GEAR, True, 18) + E(cx + 0.45, cy + 1.2, 0.42, 0.42, "#F2C94C", True) + '</g>'
    har = (f'<g class="gear-harness" style="display:none">'
           + Pth(f"M{n(harness_x-0.7)},{n(harness_y-h/2)} l1.4,0 l0.2,{n(h)} l-1.4,0 Z", GEAR)
           + Pth(f"M{n(harness_x-0.6)},{n(harness_y-h/2+0.2)} L{n(harness_x-4)},{n(harness_y-h/2+0.6)} l0,1 L{n(harness_x-0.6)},{n(harness_y-h/2+1.2)} Z", GEAR)
           + E(harness_x - 2.4, harness_y - h / 2 + 0.6, 0.5, 0.5, "#F2C94C", True) + '</g>')
    ring = (n(cx + 0.45), n(cy + 1.2))
    return col + har + f'<circle class="leash-ring" cx="{ring[0]}" cy="{ring[1]}" r="0.01" fill="none"></circle>', ring

# ---------------------------------------------------------------- DOG
DOG = {
    "mix":       dict(rx=5.4, ry=3.1, legl=4.6, head=3.0, snout=1.9, ear="flop", tail="wag"),
    "poodle":    dict(rx=4.8, ry=3.0, legl=5.0, head=2.8, snout=1.6, ear="puff", tail="pom"),
    "shiba":     dict(rx=5.2, ry=3.1, legl=4.6, head=3.0, snout=1.8, ear="prick", tail="curl"),
    "dachshund": dict(rx=7.4, ry=2.8, legl=2.9, head=2.8, snout=2.4, ear="long", tail="wag"),
}

def dog_head(hx, hy, b, closed=False, tilt=0):
    out = ""
    r = b["head"]
    if b["ear"] == "prick":
        out += Pth(f"M{n(hx-2.2)},{n(hy-1.4)} L{n(hx-1.8)},{n(hy-4.6)} L{n(hx+0.2)},{n(hy-2.6)} Z", FUR) + Pth(f"M{n(hx-1.7)},{n(hy-1.9)} L{n(hx-1.6)},{n(hy-3.6)} L{n(hx-0.5)},{n(hy-2.5)} Z", PINK, False)
    if b["ear"] == "puff":
        out += "".join(E(hx + dx, hy + dy, 1.5, 1.5, FURD) for dx, dy in ((-2.3, -1.2), (-2.6, 0.6), (-2.0, 2.0)))
    out += E(hx, hy, r, r * 0.92, FUR)
    if b["ear"] == "puff":
        out += E(hx - 0.3, hy - r + 0.2, 1.8, 1.4, FUR) + E(hx + 0.8, hy - r + 0.5, 1.2, 1.0, FUR)
    sx = hx + r * 0.75
    out += E(sx + b["snout"] * 0.45, hy + 0.9, b["snout"], 1.3, FUR if "shiba" != b.get("name") else WHITE)
    if b.get("name") == "shiba":
        out += E(hx + 0.6, hy + 1.2, 1.6, 1.0, WHITE, False) + E(sx + b["snout"] * 0.45, hy + 0.9, b["snout"], 1.3, WHITE)
    out += E(sx + b["snout"] * 1.3, hy + 0.5, 0.6, 0.48, OL, False) + SL(f"M{n(sx+b['snout']*1.2)},{n(hy+1.4)} q-0.6,0.6 -1.3,0.2")
    out += eye(hx + 0.9, hy - 0.5, closed)
    if b["ear"] == "flop":
        out += Pth(f"M{n(hx-0.8)},{n(hy-2.6)} Q{n(hx-2.8)},{n(hy-1.6)} {n(hx-2.0)},{n(hy+1.6)} Q{n(hx-0.6)},{n(hy+0.4)} {n(hx-0.2)},{n(hy-2.4)} Z", FURD)
    if b["ear"] == "long":
        out += Pth(f"M{n(hx-0.8)},{n(hy-2.4)} Q{n(hx-2.8)},{n(hy-0.6)} {n(hx-1.8)},{n(hy+3.2)} Q{n(hx-0.4)},{n(hy+1.4)} {n(hx-0.1)},{n(hy-2.2)} Z", FURD)
    out += E(hx + 1.6, hy + 1.6, 0.6, 0.35, "#F7A6A6", False, 0, ' opacity="0.6"')
    return out

def dog_tail(tx, ty, b, wag, sit=False):
    a = math.radians(180 + wag)
    if b["tail"] == "curl":
        return E(tx + 0.6, ty - 1.6, 1.7, 1.6, FUR) + E(tx + 0.7, ty - 1.6, 0.7, 0.6, WHITE, False)
    if b["tail"] == "pom":
        ex, ey = tx + math.cos(a) * 2.6, ty - abs(math.sin(a)) * 2.6 - 1
        return Ln(tx, ty, ex, ey, OL, 1.2) + Ln(tx, ty, ex, ey, FUR, 0.6) + E(ex, ey, 1.3, 1.2, FUR)
    ex, ey = tx + math.cos(a) * 4, ty - abs(math.sin(a)) * 4 - 0.6
    mx, my = tx + math.cos(a) * 1.6, ty - 2.6
    return SL(f"M{n(tx)},{n(ty)} Q{n(mx)},{n(my)} {n(ex)},{n(ey)}", OL, 1.6) + SL(f"M{n(tx)},{n(ty)} Q{n(mx)},{n(my)} {n(ex)},{n(ey)}", FUR, 0.9)

def dog_body(cx, cy, b):
    if b["ear"] == "puff":
        return "".join(E(cx + dx, cy + dy, 2.0, 1.8, FUR) for dx, dy in ((-2.6, -0.4), (-0.6, -0.9), (1.4, -0.5), (-1.6, 0.9), (0.6, 0.8))) + "".join(
            E(cx + dx, cy + dy, 1.6, 1.4, FUR, False) for dx, dy in ((-2.6, -0.4), (-0.6, -0.9), (1.4, -0.5), (-1.6, 0.9), (0.6, 0.8)))
    out = E(cx, cy, b["rx"], b["ry"], FUR)
    if b.get("name") == "shiba":
        out += E(cx + b["rx"] * 0.55, cy + b["ry"] * 0.35, b["rx"] * 0.35, b["ry"] * 0.5, WHITE, False)
    out += E(cx - b["rx"] * 0.2, cy - b["ry"] * 0.55, b["rx"] * 0.5, 0.45, "rgba(255,255,255,.25)", False)
    return out

def dog(breed="mix", pose="walk", f=0):
    b = dict(DOG[breed]); b["name"] = breed
    L = b["legl"]; rx = b["rx"]
    paw = FUR if breed != "poodle" else FUR
    if pose == "walk":
        bob = BOB[f]
        by = -(L + b["ry"] * 0.55) + bob
        hipx, shx = -rx + 1.4, rx - 1.6
        out = shadow(rx + 1.2)
        # far legs
        out += leg(shx - 0.6, by + 1.2, shx - 0.6 + DX_B[f], -LIFT_B[f], FURD, 1.3, None)
        out += leg(hipx + 0.6, by + 1.2, hipx + 0.6 + DX_A[f], -LIFT_A[f], FURD, 1.3, None)
        out += dog_tail(-rx + 0.6, by - 0.6, b, WAG[f])
        out += dog_body(0, by, b)
        out += leg(shx + 0.4, by + 1.0, shx + 0.4 + DX_A[f], -LIFT_A[f], FUR, 1.5, "#FFFFFF" if breed == "shiba" else None)
        out += leg(hipx - 0.2, by + 1.0, hipx - 0.2 + DX_B[f], -LIFT_B[f], FUR, 1.5, "#FFFFFF" if breed == "shiba" else None)
        if breed == "poodle":
            for x, y in ((shx + 0.4 + DX_A[f], -LIFT_A[f]), (hipx - 0.2 + DX_B[f], -LIFT_B[f])):
                out += E(x, y - 0.6, 1.0, 0.9, FUR)
        hx, hy = rx + 0.6, by - 3.2
        g, ring = gear_layer(hx - 2.2, hy + 2.0, rx, rx - 1.6, by)
        out += g + dog_head(hx, hy, b)
        return out, ring
    if pose == "sit":
        out = shadow(5)
        out += dog_tail(-3.4, -0.8, b, -10) if b["tail"] in ("wag",) else dog_tail(-3.2, -2.6, b, 30)
        out += E(-1.6, -2.6, 3.4 if breed != "dachshund" else 4.2, 2.6, FUR)                       # haunch
        out += E(0.8, -6.2, 2.8, 4.4 if breed != "dachshund" else 3.6, FUR, True, 22)            # chest
        if breed == "shiba":
            out += E(1.6, -5.6, 1.4, 2.8, WHITE, False, 22)
        out += leg(2.2, -5.0, 2.4, 0, FURD, 1.3) + leg(3.0, -5.0, 3.3, 0, FUR, 1.5)
        out += E(-1.0, -0.4, 2.0, 0.8, FUR)
        hx, hy = 2.6, -11.4 if breed != "dachshund" else -9.8
        g, ring = gear_layer(1.6, hy + 2.6, 3, 1.4, -6)
        out += g + dog_head(hx, hy, b)
        return out, ring
    # lie (resting at home)
    out = shadow(rx + 2)
    out += dog_tail(-rx + 0.6, -1.6, b, -30) if b["tail"] == "wag" else dog_tail(-rx + 0.8, -2.4, b, 10)
    out += E(-0.4, -2.3, rx + 0.6, 2.4, FUR)
    if breed == "shiba":
        out += E(1.6, -1.2, 3.4, 1.0, WHITE, False)
    out += leg(rx - 1.6, -0.9, rx + 3.4, -0.6, FURD, 1.2) + leg(rx - 1.2, -0.5, rx + 3.8, -0.2, FUR, 1.4)
    hx, hy = rx + 1.8, -3.8
    g, ring = gear_layer(hx - 1.8, hy + 1.6, rx, rx - 1.6, -2.3, 3.6)
    out += g + dog_head(hx, hy, b, closed=True)
    out += f'<text x="{n(hx+1)}" y="{n(hy-4)}" font-family="Jua, sans-serif" font-size="2.4" fill="#7A8CB8">z</text>'
    return out, ring

# ---------------------------------------------------------------- CAT
CAT_PATTERN = ("mix", "cheese", "tuxedo", "calico")

def cat_head(hx, hy, pat, closed=False):
    out = Pth(f"M{n(hx-2.4)},{n(hy-1.2)} L{n(hx-2.0)},{n(hy-4.4)} L{n(hx-0.3)},{n(hy-2.4)} Z", FUR) + Pth(f"M{n(hx+0.6)},{n(hy-2.5)} L{n(hx+2.0)},{n(hy-4.6)} L{n(hx+2.6)},{n(hy-1.4)} Z", FUR)
    out += Pth(f"M{n(hx-1.9)},{n(hy-1.8)} L{n(hx-1.8)},{n(hy-3.4)} L{n(hx-0.9)},{n(hy-2.4)} Z", PINK, False) + Pth(f"M{n(hx+1.1)},{n(hy-2.6)} L{n(hx+1.9)},{n(hy-3.8)} L{n(hx+2.1)},{n(hy-1.9)} Z", PINK, False)
    out += E(hx, hy, 2.9, 2.6, FUR)
    if pat == "cheese":
        out += SL(f"M{n(hx-0.6)},{n(hy-2.4)} l0.2,1.1 M{n(hx+0.4)},{n(hy-2.5)} l0,1.2 M{n(hx+1.3)},{n(hy-2.3)} l-0.2,1.0", FURD, 0.45)
    if pat == "tuxedo":
        out += Pth(f"M{n(hx+0.3)},{n(hy+0.3)} Q{n(hx+1.6)},{n(hy-0.6)} {n(hx+2.8)},{n(hy+0.6)} Q{n(hx+2.4)},{n(hy+2.6)} {n(hx+0.8)},{n(hy+2.4)} Q{n(hx-0.4)},{n(hy+1.6)} {n(hx+0.3)},{n(hy+0.3)} Z", "#FFFFFF", False)
    if pat == "calico":
        out += Pth(f"M{n(hx-2.6)},{n(hy-0.8)} Q{n(hx-2.2)},{n(hy-2.6)} {n(hx-0.6)},{n(hy-2.5)} Q{n(hx-0.4)},{n(hy-0.6)} {n(hx-2.6)},{n(hy-0.8)} Z", "#E8A05A", False)
        out += Pth(f"M{n(hx+0.6)},{n(hy-2.5)} Q{n(hx+2.4)},{n(hy-2.4)} {n(hx+2.7)},{n(hy-0.6)} Q{n(hx+1.6)},{n(hy-1.2)} {n(hx+0.6)},{n(hy-2.5)} Z", "#3A2E2A", False)
    out += eye(hx + 0.7, hy - 0.2, closed) + (eye(hx + 2.0, hy - 0.2, closed) if not closed else SL(f"M{n(hx+1.5)},{n(hy-0.2)} q0.5,0.45 1,0"))
    out += Pth(f"M{n(hx+1.3)},{n(hy+0.7)} l0.4,0 l-0.2,0.35 z", PINK, False) + SL(f"M{n(hx+1.5)},{n(hy+1.05)} q-0.4,0.5 -0.8,0.1 M{n(hx+1.5)},{n(hy+1.05)} q0.4,0.5 0.8,0.1", OL, 0.28)
    out += SL(f"M{n(hx+2.4)},{n(hy+0.9)} l1.8,-0.4 M{n(hx+2.4)},{n(hy+1.2)} l1.8,0.3", "#8A7A70", 0.2)
    return out

def cat_tail(tx, ty, swish, pat):
    ex, ey = tx - 2.4 + swish, ty - 6.6
    d = f"M{n(tx)},{n(ty)} Q{n(tx-3.6)},{n(ty-1.4)} {n(tx-2.8+swish*0.4)},{n(ty-4)} T{n(ex)},{n(ey)}"
    out = SL(d, OL, 1.75) + SL(d, FUR, 1.05)
    if pat == "cheese":
        out += SL(d, FURD, 1.05).replace("stroke-linecap", 'stroke-dasharray="0.8 1.1" stroke-linecap')
    if pat == "calico":
        out += E(ex, ey + 0.4, 0.6, 0.9, "#3A2E2A", False)
    return out

def cat_body_marks(cx, cy, rx, ry, pat):
    out = ""
    if pat == "cheese":
        for i in range(3):
            x = cx - rx * 0.5 + i * rx * 0.45
            out += SL(f"M{n(x)},{n(cy-ry+0.3)} q0.6,{n(ry*0.6)} 0,{n(ry*1.1)}", FURD, 0.5)
    if pat == "tuxedo":
        out += E(cx + rx * 0.62, cy + ry * 0.3, rx * 0.32, ry * 0.62, "#FFFFFF", False)
    if pat == "calico":
        out += E(cx - rx * 0.35, cy - ry * 0.35, rx * 0.4, ry * 0.5, "#E8A05A", False) + E(cx + rx * 0.25, cy - ry * 0.45, rx * 0.28, ry * 0.4, "#3A2E2A", False)
    return out

def cat(pat="mix", pose="walk", f=0):
    paw = "#FFFFFF" if pat == "tuxedo" else None
    if pose == "walk":
        rx, ry, L = 5.0, 2.6, 4.4
        by = -(L + ry * 0.5) + BOB[f] * 0.6
        hipx, shx = -rx + 1.4, rx - 1.5
        out = shadow(6)
        out += leg(shx - 0.6, by + 1, shx - 0.6 + DX_B[f] * 0.9, -LIFT_B[f], FURD, 1.15) + leg(hipx + 0.6, by + 1, hipx + 0.6 + DX_A[f] * 0.9, -LIFT_A[f], FURD, 1.15)
        out += cat_tail(-rx + 0.6, by - 0.4, [0, 0.8, 0, -0.8][f], pat)
        out += E(0, by, rx, ry, FUR) + cat_body_marks(0, by, rx, ry, pat)
        out += leg(shx + 0.4, by + 0.8, shx + 0.4 + DX_A[f] * 0.9, -LIFT_A[f], FUR, 1.3, paw) + leg(hipx - 0.2, by + 0.8, hipx - 0.2 + DX_B[f] * 0.9, -LIFT_B[f], FUR, 1.3, paw)
        hx, hy = rx + 0.4, by - 2.6
        g, ring = gear_layer(hx - 1.8, hy + 2.0, rx, rx - 1.6, by, 4.0)
        return out + g + cat_head(hx, hy, pat), ring
    if pose == "sit":
        out = shadow(4.6)
        out += cat_tail(-2.4, -0.8, 0, pat).replace("M-2.4,-0.8", "M-2.4,-0.8")
        out = shadow(4.6) + SL("M-2.6,-0.9 Q-5.6,-0.4 -4,1 Q0,1.8 3.6,0.6", OL, 1.75) + SL("M-2.6,-0.9 Q-5.6,-0.4 -4,1 Q0,1.8 3.6,0.6", FUR, 1.05)
        out += Pth("M-3.6,0 Q-4.4,-6 -0.6,-8.8 Q2.6,-9.4 3,-5.6 Q3.2,-1.6 2.2,0 Z", FUR) + cat_body_marks(0, -4.2, 3.2, 3.6, pat)
        out += leg(1.4, -4.4, 1.6, 0, FURD, 1.1) + leg(2.4, -4.4, 2.7, 0, FUR, 1.3, paw)
        hx, hy = 1.4, -10.6
        g, ring = gear_layer(0.8, hy + 2.4, 3, 0.6, -6, 3.6)
        return out + g + cat_head(hx, hy, pat), ring
    out = shadow(6.4)
    out += E(-0.4, -2.4, 5.6, 2.6, FUR) + cat_body_marks(-0.4, -2.4, 5.6, 2.6, pat)
    d = "M-5.6,-1.4 Q-7.6,1.2 -2,0.9 Q2.6,0.6 4.4,0.2"
    out += SL(d, OL, 1.75) + SL(d, FUR, 1.05)
    out += leg(3.4, -0.8, 6.0, -0.4, FUR, 1.2, paw)
    hx, hy = 5.0, -3.4
    g, ring = gear_layer(3.4, hy + 1.6, 5, 3.4, -2.4, 3.4)
    out += g + cat_head(hx, hy, pat, closed=True)
    out += f'<text x="{n(hx+1.4)}" y="{n(hy-4.2)}" font-family="Jua, sans-serif" font-size="2.4" fill="#7A8CB8">z</text>'
    return out, ring

def pet(kind, breed, pose, f=0):
    return dog(breed, pose, f) if kind == "dog" else cat(breed, pose, f)

VIEWBOX = "-12 -16 25 18"
POSES = [("walk", 0), ("walk", 1), ("walk", 2), ("walk", 3), ("sit", 0), ("lie", 0)]
POSE_NAME = {("walk", 0): "walk-1", ("walk", 1): "walk-2", ("walk", 2): "walk-3", ("walk", 3): "walk-4", ("sit", 0): "sit", ("lie", 0): "lie"}
BREEDS = {"dog": [("mix", "기본"), ("poodle", "푸들"), ("shiba", "시바"), ("dachshund", "닥스훈트")],
          "cat": [("mix", "기본"), ("cheese", "치즈 태비"), ("tuxedo", "턱시도"), ("calico", "삼색")]}
FURS = ["#C98B5A", "#F2EDE4", "#3A2E2A", "#E8C79A", "#9AA3B5"]

def furvars(c):
    return f"--fur:{c};--fur-dark:{FUR_DARK_MAP[c]}"

def wrap(body, w=88, h=72, fur=None, gear="collar", label="반려동물", flip=False):
    st = f' style="{furvars(fur)}"' if fur else ""
    gstyle = '<style>.gear-harness{display:inline}.gear-collar{display:none}</style>' if gear == "harness" else ""
    b = body if not flip else f'<g transform="scale(-1,1)">{body}</g>'
    if gear == "harness":
        b = b.replace('class="gear-harness" style="display:none"', 'class="gear-harness"').replace('<g class="gear-collar">', '<g class="gear-collar" style="display:none">')
    return f'<svg viewBox="{VIEWBOX}" width="{w}" height="{h}" role="img" aria-label="{label}"{st} style="display: block; overflow: visible">{b}</svg>' if not fur else f'<svg viewBox="{VIEWBOX}" width="{w}" height="{h}" role="img" aria-label="{label}" style="display: block; overflow: visible; {furvars(fur)}">{b}</svg>'
