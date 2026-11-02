from art import *
from furniture import CATALOG
from world import park as park_plot
IT = {b: {k: fn for k, l, w, h, fn, s in lst} for b, (lbl, lst) in CATALOG.items()}
def place(b, items):
    return "".join(f'<g transform="translate({x},{y})">{IT[b][k]()}</g>' for k, x, y in sorted(items, key=lambda z: z[2]))
LAYOUT = {
 "home": (window(22, 8, 34, 18) + frame_pic(64, 9, 16, 12, rect(65, 10, 14, 10, "#CDE6D3")) + rug(170, 120, 46, 14, "#E7B18E", "#F3CDB0"),
          [("kitchen", 92, 16), ("fridge", 142, 8), ("wardrobe", 270, 4), ("tv", 190, 14), ("dinette", 92, 52), ("armchair", 216, 92),
           ("floorsit", 150, 116), ("monstera", 240, 14), ("piano", 18, 120), ("aquarium", 18, 46), ("clothes", 276, 70)]),
 "work": (window(244, 8, 34, 18) + string_lights(0, 0, -100),
          [("whiteboard", 16, 6), ("projector", 120, 4), ("cabinet", 62, 8), ("printer", 84, 14), ("cooler", 204, 4), ("mailshelf", 280, 6),
           ("partition", 16, 52), ("partition", 64, 52), ("pcdesk", 128, 54), ("standing", 190, 50), ("meeting", 236, 92), ("lounge", 16, 126), ("coffee", 120, 130), ("officechair", 160, 96)]),
 "cafe": (window(16, 10, 40, 16) + string_lights(4, 316, 3),
          [("espresso", 150, 18), ("pastry", 194, 20), ("pos", 238, 24), ("coldbrew", 268, 24), ("beans", 120, 44), ("barstools", 14, 40),
           ("roundset", 20, 82), ("roundset", 90, 74), ("booth", 160, 112), ("plantshelf", 280, 74), ("board", 232, 108), ("cakestand", 210, 78), ("takeout", 20, 132)]),
 "dining": (window(16, 8, 34, 18) + rug(150, 120, 70, 22, "#E7C9A8", "#F3DDC4"),
          [("kitchenpass", 110, 16), ("stove", 172, 16), ("winerack", 234, 6), ("host", 270, 40), ("roundtable", 30, 60), ("roundtable", 120, 92),
           ("booth", 200, 70), ("saladbar", 20, 128), ("dessertcart", 270, 120), ("highchair", 180, 126), ("fishtank", 60, 6), ("grill", 226, 130)]),
 "gym": (window(244, 8, 34, 18),
          [("scoreboard", 120, 4), ("treadmill", 14, 14), ("treadmill", 48, 14), ("bike", 84, 22), ("lockers", 196, 6), ("towels", 280, 60),
           ("pool", 16, 74), ("yoga", 110, 76), ("benchpress", 170, 64), ("kettle", 228, 52), ("pullup", 232, 96), ("rowing", 110, 130), ("ballrack", 176, 134)]),
}
def room(kind, color, style, uid):
    decor, items = LAYOUT[kind]
    return building(kind, "l", color, style, uid, interior=decor + place(kind, items))
def park_room():
    base = rect(0, 0, 320, 176, "#A9D58E", 8) + grass_detail(0, 0, 320, 176, "village", 9) + rect(0, 0, 320, 176, "none", 8, "#5E9E52", 3.2) + rect(0, 0, 320, 176, "none", 8, OL, 0.5)
    base += path("M150,176 Q150,110 100,96 T20,70 M150,110 Q200,96 300,100", "none", "#E9DCC0", 10)
    items = [("gazebo", 14, 6), ("slide", 96, 18), ("swing", 156, 10), ("seesaw", 226, 24), ("icecream", 278, 52), ("sandbox", 200, 64), ("junglegym", 254, 110),
             ("picnic", 90, 118), ("duckpond", 18, 116), ("arch", 140, 120), ("bikerack", 196, 136), ("trash", 74, 74), ("drinking", 182, 104), ("signpost", 128, 64)]
    return base + place("park", items) + sign_plate(30, 182, "공원", "#6FA387")
