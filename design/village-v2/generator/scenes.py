"""Full themed scenes: the app world (3x2) plus a top band and a bottom band of scenery, vehicles and NPCs."""
import json, copy
from themes import *
from scenery import *
from furniture import CATALOG

NPC = json.load(open("npcs.json"))
AVS = fix(avatars())
BANDS = {"city": (150, 80), "forest": (120, 70), "coast": (80, 150), "village": (140, 74)}

def put(svg, x, y):
    return f'<g transform="translate({f(x)},{f(y)})">{svg}</g>'

def npc(i, d, x, y, h=30):
    w = h * 172 / 270
    return f'<svg x="{f(x-w/2)}" y="{f(y-h*0.97)}" width="{f(w)}" height="{f(h)}" viewBox="14 18 172 270">{NPC[i % len(NPC)][d]}</svg>'

def furnish(cfg):
    """add a few new catalog items into buildings (as extra layer on top of interior)"""
    return cfg

def scene(th):
    cfg = theme_cfg(th)
    T, B = BANDS[th]
    W, H, body = world_svg(cfg, AVS)
    SH = T + H + B
    t = THEMES[th]
    bg = rect(0, 0, W, SH, t["g1"])
    if th != "city":
        bg += "".join(ell((i * 97.3) % W, (i * 57.1) % SH, 14 + (i % 4) * 4, 6 + (i % 3) * 2, t["g2"]) for i in range(int(W * SH / 2600)))
        bg += grass_detail(0, 0, W, T, th, 2) + grass_detail(0, T + H, W, B, th, 4)
    top, bot, sprites = "", "", []          # sprites = (y, svg) sorted later
    rows = [T + 24 + r * 224 + 180 for r in range(2)]   # horizontal road tops (scene coords)
    vx = [24 + c * 344 + 322 for c in range(2)]

    if th == "city":
        # skyline band
        top += rect(0, 0, W, T, "#C5CBD1") + rect(0, T - 22, W, 22, "#B9BDC2") + rect(0, T - 22, W, 1.2, "#9EA3A9")
        x = -6; i = 0
        specs = [(60, 140, "#9FB7C9", "glass", "antenna"), (52, 100, "#D9A27E", "brick", "tank"), (70, 120, "#B7C3CC", "office", "sign"), (48, 86, "#E3C9A8", "brick", "tank"),
                 (64, 132, "#8FA9C2", "glass", ""), (56, 108, "#C9B7D9", "office", "antenna"), (60, 94, "#D9A27E", "brick", "tank")]
        while x < W:
            w, h, c, k, roof = specs[i % len(specs)]
            sprites.append((T - 22, put(tower(w, h, c, "#CFE3EE", k, i) + tower_roof(w, h, roof), x, T - 22)))
            x += w + 14; i += 1
        sprites += [(T - 4, put(billboard(), 120, T - 6)), (T - 4, put(subway(), 520, T - 4)), (T - 4, put(kiosk(), 830, T - 4)), (T - 2, put(pigeons(), 690, T - 2))]
        sprites += [(T - 2, npc(0, "right", 300, T - 2)), (T - 2, npc(1, "left", 600, T - 2)), (T - 2, npc(2, "right", 960, T - 2))]
        # bottom avenue
        by = T + H
        bot += rect(0, by + 10, W, 50, "#5D636A") + rect(0, by + 6, W, 4, "#B9BDC2") + rect(0, by + 60, W, 4, "#B9BDC2")
        bot += "".join(rect(xx, by + 34.4, 14, 1.2, "#F2EFE6", 0.6) for xx in range(4, W, 26))
        for i in range(6):
            bot += rect(vx[0] + 2, by + 12 + i * 8, 16, 4, "#F2EFE6", 0.4) if False else ""
        sprites += [(by + 30, put(car_side("#6FA387", -1, "bus"), 300, by + 30)), (by + 30, put(car_side("#E06A52", -1), 640, by + 30)),
                    (by + 56, put(car_side("#F7D07A", 1, "taxi"), 160, by + 56)), (by + 56, put(car_side("#2F6FA8", 1, "truck"), 820, by + 56)),
                    (by + 8, put(foodtruck(), 470, by + 4))]
        # cars on the world roads
        for r, ry in enumerate(rows):
            sprites += [(ry + 10, put(car_side(["#8CB8E0", "#E06A52"][r], -1), 180 + r * 420, ry + 10)), (ry + 22, put(car_side(["#F7D07A", "#B7A1D9"][r], 1, "taxi" if r == 0 else "sedan"), 760 - r * 300, ry + 22))]
        sprites += [(rows[0] + 120, put(car_front("#E06A52"), vx[0] + 10, rows[0] + 120)), (rows[0] + 80, put(car_front("#6FA387", True), vx[1] + 10, rows[0] + 80))]
        # NPCs & street furniture
        for k, (i, d, x, y) in enumerate(((3, "right", 90, rows[0] - 2), (4, "left", 470, rows[0] - 2), (5, "down", 700, rows[0] + 30), (6, "left", 960, rows[1] - 2),
                                          (7, "right", 250, rows[1] + 30), (8, "up", vx[0] - 6, rows[0] + 160), (9, "left", 560, rows[1] + 30), (10, "right", 880, by + 6))):
            sprites.append((y, npc(i, d, x, y)))
        sprites += [(rows[0] - 1, put(hydrant(), 360, rows[0] - 1)), (rows[1] - 1, put(trashcan(), 400, rows[1] - 1)), (rows[1] + 31, put(cone(), 600, rows[1] + 31)),
                    (rows[1] + 31, put(cone(), 610, rows[1] + 33)), (rows[0] + 31, put(phonebooth(), 940, rows[0] + 32)), (by + 4, put(pigeons(), 260, by + 4))]
    elif th == "forest":
        top += put(stream(W + 20, 36), -10, 40)
        sprites += [(76, put(waterfall(), 70, 60)), (60, put(bridge(), vx[1] + 10, 60)), (110, put(tent(), 520, 112)), (112, put(campfire(), 560, 112)),
                    (30, put(meadow(90, 30), 300, 24)), (34, put(meadow(70, 24), 880, 26)), (118, put(meadow(80, 26), 760, 108)),
                    (60, put(ducks(), 410, 60)), (108, put(fox(), 220, 110)), (112, put(bearcub(), 980, 112)), (110, put(owl(), 640, 110)), (20, put(butterflies(), 300, 20)),
                    (28, put(birdhouse(), 1010, 30)), (112, put(hedgehog(), 400, 114)), (22, put(butterflies(), 880, 22))]
        for x in range(10, W, 46):
            if abs(x - 70) > 30:
                sprites.append((26, tree(x, 26, "pine", 0.9 + (x % 3) * 0.08)))
        by = T + H
        for x in range(14, W, 40):
            sprites.append((by + 66, tree(x, by + 66, "pine", 1.0)))
        sprites += [(by + 30, put(berrybush(), 160, by + 30)), (by + 34, put(berrybush(), 700, by + 34)), (by + 28, put(fireflies(), 420, by + 28)),
                    (by + 32, put(hedgehog(), 300, by + 32)), (by + 30, put(meadow(60, 20), 520, by + 30)), (by + 30, put(fireflies(), 900, by + 30))]
        sprites += [(rows[0] + 22, npc(11, "right", 600, rows[0] + 20)), (rows[1] + 22, npc(12, "left", 300, rows[1] + 20))]
    elif th == "coast":
        top += rect(0, 0, W, T, "#F4E6C2")
        sprites += [(60, put(beachhut(), 120, 60)), (60, put(beachhut(), 160, 62)), (62, put(volleyball(), 420, 62)), (40, tree(260, 40, "palm")),
                    (44, tree(620, 44, "palm")), (62, put(fishstall(), 820, 64)), (60, put(fishcrates(), 900, 66)), (64, tree(980, 50, "palm"))]
        sprites += [(64, npc(13, "right", 500, 66)), (60, npc(14, "left", 700, 62))]
        # extended sea
        sy = T + H
        bot += rect(0, sy - 2, W, B + 2, "#5FB0D8") + rect(0, sy - 2, W, 20, "#7CC4E4")
        bot += "".join(path(f"M{(i*83)%W},{sy+20+(i*29)%(B-30)} q4,-2.4 8,0", "none", "rgba(255,255,255,.55)", 0.9) for i in range(40))
        sprites += [(sy + 70, put(fishboat(), 620, sy + 70)), (sy + 120, put(fishboat(), 860, sy + 122)), (sy + 60, put(sailboat(), 300, sy + 60)),
                    (sy + 110, put(sailboat(), 120, sy + 116)), (sy + 40, put(buoy(), 480, sy + 40)), (sy + 96, put(buoy(), 760, sy + 96)), (sy + 60, put(kayak(), 410, sy + 84))]
        pier_x = 200
        sprites.append((sy - 10, put(pier(), pier_x, sy - 40)))
        sprites += [(sy + 30, npc(15, "down", pier_x + 9, sy + 26)), (sy - 6, put(fishcrates(), pier_x + 40, sy - 34))]
        sprites += [(sy + 60, put(lighthouse(), W - 70, sy + 60))]
        bs = T + 24 + 2 * 224   # beach strip in world (coast)
        sprites += [(bs + 14, put(towel(), 640, bs + 12)), (bs + 16, put(crab(), 720, bs + 18)), (bs + 18, put(shells(), 900, bs + 16)),
                    (bs + 14, put(lifeguard(), 960, bs + 18)), (bs + 18, put(shells(), 380, bs + 20))]
        sprites += [(rows[0] + 22, npc(0, "left", 560, rows[0] + 20)), (rows[1] + 22, npc(2, "right", 400, rows[1] + 20))]
        sprites += [(30, put(p_gull_wrap(), 540, 30)), (sy + 20, put(p_gull_wrap(), 700, sy + 20))]
    else:  # village
        sprites += [(20, put(field(110, 48, "cabbage"), 30, 20)), (20, put(field(84, 40, "carrot"), 160, 24)), (20, put(field(120, 48, "wheat"), 600, 18)),
                    (110, put(barn(), 360, 110)), (110, put(windmill(20), 790, 112)), (118, put(cow(), 460, 118)), (124, put(sheep(), 520, 122)),
                    (120, put(sheep(), 540, 128)), (122, put(chicken(), 270, 122)), (124, put(chicken("#E8B64C"), 285, 126)), (128, put(chicken(), 300, 120)),
                    (80, put(pumpkins(), 960, 80)), (120, put(beehive(), 900, 120)), (118, put(tractor(), 700, 120)), (70, put(field(60, 32, "cabbage"), 900, 20))]
        for x in (10, 1040):
            sprites.append((100, tree(x, 100, "round")))
        by = T + H
        bot += put(stream(W + 20, 30), -10, by + 26)
        sprites += [(by + 42, put(stepstones(), vx[0] + 10, by + 40)), (by + 20, put(laundry(), 200, by + 22)), (by + 22, put(jangdok(), 500, by + 22)),
                    (by + 22, put(mailbox(), 640, by + 22)), (by + 24, tree(760, by + 24, "round")), (by + 24, put(persimmon(), 940, by + 24)), (by + 70, put(ducks(), 300, by + 46))]
        sprites += [(rows[0] + 22, npc(1, "right", 300, rows[0] + 20)), (rows[1] + 22, npc(4, "left", 650, rows[1] + 20)), (124, npc(5, "down", 600, 126))]
    world = f'<g transform="translate(0,{T})">{body}</g>'
    spr = "".join(s for _, s in sorted(sprites, key=lambda z: z[0]))
    return W, SH, bg + top + bot + world + spr

def p_gull_wrap():
    from world import p_gull
    return p_gull(0, 0) + put(p_gull(0, 0), 14, -6)

if __name__ == "__main__":
    h = ""
    for th in ("city", "forest", "coast", "village"):
        W, SH, b = scene(th)
        h += f'<svg viewBox="0 0 {W} {SH}" width="{W*0.7}" height="{SH*0.7}" style="display:inline-block;margin:4px">{b}</svg>'
    open("scenes_pv.html", "w").write(f'<html><body style="margin:0;width:1500px">{h}</body></html>')
