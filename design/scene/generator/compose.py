import json
from pets import *
from props import *

AV = json.load(open("avs.json"))
S = 34 / 270

def av(pid, d, f, x=0, y=0, h=34, sy=1.0, clip_y=None, uid="a"):
    """avatar layers placed with feet at (x,y) in scene units"""
    w = h * 172 / 270
    inner = AV[pid][f"{d}{f}"]
    body = f'<svg x="{n(-w/2)}" y="{n(-h*0.97)}" width="{n(w)}" height="{n(h)}" viewBox="14 18 172 270" overflow="visible">{inner}</svg>'
    if clip_y is not None:
        body = f'<clipPath id="cl{uid}"><rect x="-20" y="-60" width="40" height="{n(60+clip_y)}"></rect></clipPath><g clip-path="url(#cl{uid})">{body}</g>'
    t = f"translate({n(x)},{n(y)})" + (f" scale(1,{n(sy)})" if sy != 1 else "")
    return f'<g transform="{t}">{body}</g>'

def at(svg, x, y, extra=""):
    return f'<g transform="translate({n(x)},{n(y)}){extra}">{svg}</g>'

def scene_svg(vb, body, w, h, label, bg=None):
    b = (f'<rect x="-100" y="-100" width="400" height="400" fill="{bg}"></rect>' if bg else "") + body
    return f'<svg viewBox="{vb}" width="{w}" height="{h}" role="img" aria-label="{label}" style="display: block">{b}</svg>'

FLOOR = '<rect x="-60" y="-60" width="120" height="120" fill="#E6EAEE"></rect>' + "".join(f'<line x1="-60" y1="{y}" x2="60" y2="{y}" stroke="#D3D9DE" stroke-width="0.3"></line>' for y in range(-40, 20, 8))
GRASS = '<rect x="-60" y="-60" width="120" height="120" fill="#B4D79A"></rect>'

def motion_lift(squat=False):
    sy = 0.86 if squat else 1
    by = -14.5 * sy
    return FLOOR + at(barbell_rack(), 0, -14).replace("translate(0,-14)", "translate(0,-14) scale(0.6)") + av("M01", "down", 0, 0, 0, 34, sy) + barbell(by, 13) + (sweat(6, -22 * sy) if squat else "")

def motion_jog(f=1):
    return FLOOR + treadmill_side() + av("M01", "right", f, -1, -2.6) + sweat(5, -25)

def motion_swim(f=0):
    pool = '<rect x="-60" y="-60" width="120" height="120" fill="#7CC4E4"></rect>' + "".join(f'<path d="M{x},{y} q2,-1.2 4,0" fill="none" stroke="#FFFFFF" stroke-width="0.4" opacity="0.6"></path>' for x, y in ((-20, -20), (12, -26), (-14, 6), (16, 4)))
    return pool + water(f) + av("M01", "down", 0, 0, 8, 34, 1, -14.5, "sw" + str(f)) + at(swim_cap(), 0, 8) + at(goggles(), 0, 8) + at(water_front(), 0, 0)

def motion_yoga():
    legs = E(0, -2.4, 7, 2.6, "#2F2F3D") + E(-4.6, -1.6, 2.2, 1.2, "#FFFFFF") + E(4.6, -1.6, 2.2, 1.2, "#FFFFFF")
    return FLOOR + yoga_mat() + legs + av("M01", "down", 0, 0, 7.6, 34, 1, -9.5, "yg") + yoga_aura()

def motion_bike(f=0):
    return FLOOR + spin_back() + av("M01", "right", 0, -2.2, -4.4, 34, 1, None) + spin_front(f) + sweat(3, -30)

def motion_box(f=0):
    return FLOOR + sandbag(-8 if f else 4) .replace("translate(5,-35)", "translate(13,-35)") + av("M01", "right", 0, 0, 0) + (gloves_jab(1) if f else glove(3.6, -12.4) + glove(6.4, -13.6))

def motion_talk():
    wb = R(-16, -30, 20, 13, "#FFFFFF", 0.8) + R(-15, -28, 8, 1, "#2F6FA8", 0.3, False) + R(-15, -25.6, 12, 1, "#E06A52", 0.3, False) + R(-15, -23.2, 10, 1, "#8DB596", 0.3, False) + Ln(-6, -17, -6, -10, GR, 0.6)
    return FLOOR + wb + av("M01", "left", 0, 6, 0) + note(-2, -30) + wave_lines(-1.6, -22)

def walk_with_pet(kind="dog", breed="mix", fur="#C98B5A", f=0, gear="collar"):
    body, ring = pet(kind, breed, "walk", f)
    px = -15
    hand = (1.8, -9.0)
    rx, ry = float(ring[0]) + px, float(ring[1])
    pet_svg = f'<g style="{furvars(fur)}" transform="translate({px},0)">{body}</g>'
    if gear == "harness":
        pet_svg = pet_svg.replace('class="gear-harness" style="display:none"', 'class="gear-harness"').replace('<g class="gear-collar">', '<g class="gear-collar" style="display:none">')
        # harness ring is on the back strap
    return GRASS + pet_svg + av("M01", "right", [1, 0, 2, 0][f], 0, 0) + leash(hand[0], hand[1], rx, ry, 2.5)
