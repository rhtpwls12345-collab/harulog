"""Furniture catalog — each item drawn with its footprint's top-left at (0,0) in building-local units.
ITEM = (key, label, w, h, draw_fn, solid)   w x h = visual footprint (3/4 view: top face + front face)."""
from art import *

W_ = "#B98D62"; WD = "#9C7450"; WL = "#D6B087"; WLD = "#B58C63"
GR = "#9AA6B0"; GRD = "#77828C"; DK = "#3A3F45"; WH_ = "#FFFFFF"; CR = "#F2EDE4"
SCR = "#3B4A63"

def screen(x, y, w, h):
    return rect(x, y, w, h, OL, 1) + rect(x + 0.8, y + 0.8, w - 1.6, h - 1.6, SCR, 0.6) + rect(x + 2, y + 2, w * 0.4, 0.9, "#8CB8E0") + rect(x + 2, y + 4, w * 0.6, 0.9, "#8DB596") + line(x + 2, y + h - 2, x + w * 0.35, y + 1.5, "rgba(255,255,255,.18)", 1.2)

def mug(x, y, c="#FFFFFF"):
    return rect(x, y, 4.5, 4.5, c, 0.8, OL, 0.35) + rect(x, y, 4.5, 1.2, "#8A5A3C", 0.5) + path(f"M{x+4.5},{y+1.2} q1.8,0 1.8,1.6 q0,1.6 -1.8,1.6", "none", OL, 0.4)

def legs(x, y, w, col=DK):
    return rect(x + 1, y, 1.4, 2.4, col) + rect(x + w - 2.4, y, 1.4, 2.4, col)

# ======================================================== HOME (집)
def h_tv():
    return (block(0, 14, 44, 8, 8, W_, WD) + rect(4, 24, 16, 4, WD, 0.6, OL, 0.3) + rect(24, 24, 16, 4, WD, 0.6, OL, 0.3)
            + rect(6, 0, 32, 17, OL, 1.4) + rect(7, 1, 30, 15, "#2E3A5C", 0.8) + path("M7,13 Q17,6 26,11 T37,8 L37,16 L7,16 Z", "#3E5A7C") + line(10, 4, 18, 4, "rgba(255,255,255,.3)", 1)
            + rect(18, 16, 8, 1.6, DK) + plant_small(41, 15))

def h_wardrobe():
    return (block(0, 0, 34, 6, 30, "#E2C29A", "#C39E73") + line(17, 7, 17, 35, OL, 0.5) + ell(15, 21, 0.8, 0.8, "#E9C46A", OL, 0.3) + ell(19, 21, 0.8, 0.8, "#E9C46A", OL, 0.3)
            + rect(3, 9, 11, 3, "rgba(255,255,255,.25)", 1) + rect(20, 9, 11, 3, "rgba(255,255,255,.25)", 1) + legs(0, 36, 34, WD))

def h_fridge():
    return (block(0, 0, 18, 6, 30, "#EAF2F6", "#CCD9E1", 2) + line(2, 18, 16, 18, "#AFC0CB", 0.6) + rect(14, 10, 1.4, 5, GR, 0.6) + rect(14, 21, 1.4, 8, GR, 0.6)
            + rect(3, 8, 6, 5, "#FFE7A3", 0.4) + ell(5, 22, 1.6, 1.6, "#F29A7F") + ell(9, 24, 1.4, 1.4, "#8DB596"))

def h_kitchen():
    out = block(0, 0, 46, 10, 12, "#F2EDE4", "#D8CDBE")
    out += rect(4, 2, 14, 6, "#B9C4CD", 1.6, OL, 0.4) + rect(6, 3.4, 10, 3.2, "#8CC7E6", 1) + path("M11,2 L11,-2 L14,-2", "none", GR, 1)
    out += ell(28, 5, 3, 2.2, DK) + ell(36, 5, 3, 2.2, DK) + ell(28, 5, 1.5, 1, "#5A5F66") + ell(36, 5, 1.5, 1, "#5A5F66")
    out += ell(36, 3.6, 3.4, 2.2, "#E06A52", OL, 0.4) + rect(39, 3, 4, 1, "#E06A52")
    for i in range(4):
        out += rect(2 + i * 11, 13, 10, 8, "rgba(0,0,0,.05)", 1, OL, 0.25) + rect(6 + i * 11, 14.5, 2, 0.8, GR)
    return out

def h_dinette():
    return (chair(2, 0, 12, 10, 4, W_, "#F2C9A8") + chair(24, 0, 12, 10, 4, W_, "#F2C9A8")
            + shadow(19, 30, 16, 2.4) + block(0, 10, 38, 12, 7, WL, WLD) + ell(11, 15, 3.4, 1.6, WH_, OL, 0.35) + ell(27, 15, 3.4, 1.6, WH_, OL, 0.35)
            + ell(11, 14.6, 2, 0.8, "#E06A52") + ell(27, 14.6, 2, 0.8, "#8DB596") + rect(18, 12, 2.6, 4, "#F7D07A", 0.8, OL, 0.3) + legs(0, 29, 38, WD))

def h_desk():
    return (block(0, 6, 36, 10, 10, WL, WLD) + rect(22, 18, 12, 6, WD, 0.8, OL, 0.3) + screen(8, 0, 14, 10) + rect(12, 10, 6, 1.6, DK)
            + rect(28, 2, 1.2, 8, DK) + path("M25,3 L33,3 L31,-1 L27,-1 Z", "#8DB596", OL, 0.4) + rect(2, 9, 5, 4, "#F7E1A0", 0.4, OL, 0.3) + chair(10, 24, 14, 10, 3, "#7E8FA3", "#AFC0D2"))

def h_armchair():
    return (shadow(12, 26, 13, 2) + block(0, 0, 24, 8, 12, "#E99A6E", "#D48058", 3) + block(0, 10, 5, 12, 6, "#E99A6E", "#D48058", 2) + block(19, 10, 5, 12, 6, "#E99A6E", "#D48058", 2)
            + block(5, 11, 14, 9, 5, "#F2B892", "#E39A7A", 2) + block(8, 9, 8, 5, 2, "#FFF4E0", "#EADFCF", 2))

def h_aquarium():
    return (block(0, 14, 30, 6, 10, WD, "#7A5A42") + rect(1, 0, 28, 15, "#BFE6F2", 1.4, OL, 0.5) + rect(1, 0, 28, 3, "#5A4033", 1)
            + rect(2, 11, 26, 3, "#E9D8B6", 0.5) + path("M6,14 q1,-6 -1,-9 M8,14 q2,-5 1,-7", "none", "#5E9E52", 1)
            + path("M14,7 q3,-2.4 5,0 q-2,2.4 -5,0 l-1.6,-1.4 l0,2.8 z", "#F29A4F", OL, 0.3) + path("M21,10 q2,-1.6 3.4,0 q-1.4,1.6 -3.4,0 l-1,-1 l0,2 z", "#F7D07A", OL, 0.3)
            + ell(24, 4, 0.7, 0.7, "#FFFFFF", OL, 0.2) + ell(25.4, 2.4, 0.5, 0.5, "#FFFFFF", OL, 0.2))

def h_piano():
    out = block(0, 0, 40, 10, 16, "#2F2A2E", "#1F1B1F")
    out += rect(2, 9.5, 36, 5, WH_, 0.6, OL, 0.35)
    for i in range(1, 12):
        out += line(2 + i * 3, 9.5, 2 + i * 3, 14.5, "#BFBFBF", 0.3)
        if i % 7 not in (3, 0):
            out += rect(1.2 + i * 3, 9.5, 1.4, 3, "#1F1B1F")
    out += rect(14, 2, 12, 5, CR, 0.4) + chair(13, 28, 14, 7, 3, "#2F2A2E", "#E06A52")
    return out

def h_floorsit():
    return (ell(20, 14, 20, 8, "#B7A1D9", OL, 0.45) + ell(20, 14, 16, 6, "#CDBDEA") + block(10, 4, 20, 9, 3, W_, WD, 2)
            + ell(15, 7.4, 2, 1.2, WH_, OL, 0.3) + rect(21, 6, 6, 3, "#8CB8E0", 0.4, OL, 0.25)
            + block(0, 14, 9, 7, 2, "#F2B892", "#E39A7A", 3) + block(31, 14, 9, 7, 2, "#B9D7C1", "#9DC0A8", 3))

def h_clothes():
    out = shadow(16, 26, 16, 2) + rect(1, 2, 1.4, 22, GR) + rect(29.6, 2, 1.4, 22, GR) + rect(0, 2, 32, 1.4, GR, 0.6, OL, 0.3)
    for i, c in enumerate(("#E06A52", "#8CB8E0", "#F7D07A", "#8DB596", "#D98BA6")):
        out += path(f"M{4+i*5},{3.4} l2.2,0 l1,3 l0,12 l-4.4,0 l0,-12 z", c, OL, 0.35)
    out += rect(0, 23, 3.4, 1.4, DK) + rect(28.6, 23, 3.4, 1.4, DK)
    return out

def h_washer():
    return (block(0, 0, 20, 6, 18, WH_, "#E1E6EA", 2) + rect(2, 7, 16, 2, "#D5DCE1", 0.6) + ell(15, 8, 0.8, 0.8, "#6FCB8A")
            + ell(10, 17, 6, 6, GR, OL, 0.45) + ell(10, 17, 4.6, 4.6, "#BFE3F2") + path("M6,18 q4,-3 8,0 q-4,3 -8,0", "#8CB8E0") + ell(8, 15, 1.2, 0.8, "rgba(255,255,255,.7)"))

def h_bathtub():
    return (shadow(22, 24, 22, 2) + rect(0, 2, 44, 20, WH_, 9, OL, 0.6) + rect(3, 4.5, 38, 15, "#BFE6F2", 7) + ell(14, 11, 5, 2.4, "rgba(255,255,255,.75)")
            + ell(20, 13, 3, 1.6, "rgba(255,255,255,.75)") + ell(27, 10, 4, 2, "rgba(255,255,255,.75)") + rect(38, 0, 3, 6, GR, 1, OL, 0.35)
            + path("M30,9 q1.6,-2 3.2,0 q-1.6,1.4 -3.2,0 Z", "#F7D07A", OL, 0.3) + ell(33.6, 8.6, 1.4, 1.4, "#F7D07A", OL, 0.3))

def h_monstera():
    out = shadow(10, 26, 9, 2) + rect(4, 18, 12, 8, "#F2EDE4", 2, OL, 0.45) + rect(4, 18, 12, 2, "#E2D8CA", 1)
    for (dx, dy, r, c) in ((-3, 10, 6.5, "#4C8E5D"), (7, 6, 7, "#5E9E52"), (13, 12, 6, "#4C8E5D"), (5, 13, 5, "#6FB05E")):
        out += ell(dx + 2, dy, r, r * 0.75, c, OL, 0.45) + line(dx + 2 - r * 0.6, dy, dx + 2 + r * 0.6, dy, shade(c, -0.2), 0.4)
    return out

def h_dresser():
    return (block(0, 10, 30, 6, 14, WL, WLD) + line(1, 22, 29, 22, OL, 0.35) + rect(13, 18, 4, 1, "#E9C46A") + rect(13, 25, 4, 1, "#E9C46A")
            + ell(15, 6, 9, 7, "#E9C46A", OL, 0.5) + ell(15, 6, 7.4, 5.6, "#DCEAF2") + line(11, 9, 17, 3, "rgba(255,255,255,.7)", 1)
            + rect(3, 12, 3, 4, "#D98BA6", 0.8, OL, 0.3) + ell(25, 14, 2, 1.4, "#F7C9B8", OL, 0.3))

HOME = [("tv", "TV와 TV장", 46, 30, h_tv, True), ("wardrobe", "옷장", 34, 39, h_wardrobe, True), ("fridge", "냉장고", 18, 36, h_fridge, True),
        ("kitchen", "싱크대·가스레인지", 46, 22, h_kitchen, True), ("dinette", "2인 식탁", 38, 31, h_dinette, True), ("desk", "공부 책상", 36, 35, h_desk, True),
        ("armchair", "1인 소파", 24, 28, h_armchair, True), ("aquarium", "어항", 30, 30, h_aquarium, True), ("piano", "업라이트 피아노", 40, 38, h_piano, True),
        ("floorsit", "좌식 테이블", 40, 22, h_floorsit, False), ("clothes", "행거", 32, 26, h_clothes, True), ("washer", "세탁기", 20, 24, h_washer, True),
        ("bathtub", "욕조", 44, 25, h_bathtub, True), ("monstera", "몬스테라 화분", 22, 27, h_monstera, True), ("dresser", "화장대", 30, 30, h_dresser, True)]

# ======================================================== OFFICE (작업실)
def o_pcdesk():
    return (block(0, 10, 44, 12, 10, "#EDEFF2", "#CDD3D9") + screen(5, 0, 15, 11) + screen(22, 0, 15, 11) + rect(10, 11, 5, 1.6, DK) + rect(27, 11, 5, 1.6, DK)
            + rect(12, 14, 16, 4, "#DDE1E5", 0.8, OL, 0.35) + ell(33, 16, 1.6, 2, "#DDE1E5", OL, 0.35) + mug(38, 12) + legs(0, 32, 44, GR))

def o_partition():
    out = rect(0, 0, 44, 4, "#9FB7C9", 1, OL, 0.45) + rect(0, 0, 4, 34, "#9FB7C9", 1, OL, 0.45) + rect(40, 0, 4, 34, "#9FB7C9", 1, OL, 0.45)
    out += block(4, 4, 36, 10, 8, WL, WLD) + screen(14, -2, 14, 9) + rect(6, 5, 5, 4, "#FFE7A3", 0.3) + rect(32, 5, 4, 4, "#F7C9B8", 0.3)
    out += chair(15, 24, 14, 10, 3, DK, "#5A6B80")
    return out

def o_whiteboard():
    return (shadow(18, 30, 18, 2) + rect(2, 22, 1.4, 8, GR) + rect(32.6, 22, 1.4, 8, GR) + rect(0, 0, 36, 22, "#FFFFFF", 1.4, OL, 0.55) + rect(0, 20, 36, 2, GR, 0.6)
            + path("M4,6 q4,-3 8,0 t8,0", "none", "#2F6FA8", 0.8) + rect(4, 10, 14, 1, "#E06A52", 0.4) + rect(4, 13, 10, 1, "#8DB596", 0.4)
            + rect(22, 9, 9, 7, "#FFE7A3", 0.4) + ell(28, 5, 2.6, 2.6, "none", "#E06A52", 0.6) + rect(8, 20.4, 4, 1, "#E06A52") + rect(14, 20.4, 4, 1, "#2F6FA8"))

def o_printer():
    return (block(0, 6, 24, 10, 10, "#EDEFF2", "#CDD3D9", 2) + rect(4, 2, 16, 6, WH_, 0.4, OL, 0.35) + rect(6, 14, 12, 3, WH_, 0.4, OL, 0.35)
            + rect(17, 8, 5, 3, DK, 0.6) + ell(19, 9.5, 0.6, 0.6, "#6FCB8A") + rect(2, 26, 20, 2, GR))

def o_cooler():
    return (shadow(8, 36, 8, 1.6) + rect(1, 12, 14, 24, "#EDEFF2", 2, OL, 0.5) + rect(4, 18, 8, 4, DK, 1) + rect(5, 19, 2, 2, "#8CB8E0") + rect(9, 19, 2, 2, "#E06A52")
            + path("M3,12 L3,6 Q3,0 8,0 Q13,0 13,6 L13,12 Z", "#BFE3F5", OL, 0.5) + rect(5, 2, 2, 7, "rgba(255,255,255,.6)", 1) + rect(16, 24, 4, 6, WH_, 0.6, OL, 0.3))

def o_cabinet():
    out = block(0, 0, 18, 6, 28, GR, GRD, 1.4)
    for i in range(3):
        out += rect(1.5, 8 + i * 8.6, 15, 7.6, "rgba(255,255,255,.1)", 0.8, OL, 0.3) + rect(7, 10 + i * 8.6, 4, 1.2, "#DDE1E5", 0.4)
    return out + rect(3, -3, 10, 4, "#F7E1A0", 0.4, OL, 0.3)

def o_meeting():
    out = ""
    for i in range(3):
        out += chair(4 + i * 18, 0, 13, 9, 3, DK, "#5A6B80")
    out += shadow(30, 38, 28, 3) + rect(0, 9, 60, 22, "#E2C29A", 11, OL, 0.6) + rect(0, 27, 60, 6, "#C39E73", 3) + rect(0, 9, 60, 22, "#E2C29A", 11)
    out += rect(0, 9, 60, 22, "none", 11, OL, 0.6) + rect(14, 14, 10, 7, WH_, 0.4, OL, 0.3) + rect(36, 15, 9, 6, "#B9C4CD", 0.6, OL, 0.3) + mug(26, 16) + ell(50, 19, 2, 2, "#8DB596", OL, 0.3)
    return out

def o_chair():
    return (shadow(9, 26, 9, 1.6) + ell(9, 24, 8, 2, DK) + rect(8.2, 16, 1.6, 8, GR) + block(1, 0, 16, 5, 10, DK, "#2A2E33", 3) + block(0, 9, 18, 9, 4, "#5A6B80", "#46566A", 3))

def o_coffee():
    return (block(0, 10, 30, 10, 10, W_, WD) + rect(3, 0, 12, 14, "#4F5560", 1.4, OL, 0.45) + rect(5, 2, 8, 3, "#8CB8E0", 0.6) + rect(7, 8, 4, 4, WH_, 0.4)
            + mug(19, 8) + mug(24, 9, "#F7C9B8") + rect(17, 2, 10, 5, "#E2C29A", 1, OL, 0.3))

def o_projector():
    return (shadow(22, 34, 22, 2) + rect(0, 0, 44, 2, GR, 1, OL, 0.4) + rect(2, 2, 40, 24, "#FFFFFF", 0.6, OL, 0.45) + rect(5, 5, 34, 18, "#DCEAF2", 0.6)
            + rect(8, 15, 5, 6, "#8CB8E0", 0.3) + rect(15, 11, 5, 10, "#8DB596", 0.3) + rect(22, 8, 5, 13, "#F7D07A", 0.3) + rect(29, 13, 5, 8, "#F29A7F", 0.3)
            + rect(21.3, 26, 1.4, 8, GR) + rect(16, 33, 12, 1.4, GR))

def o_lounge():
    return (shadow(24, 26, 24, 2.4) + block(0, 0, 48, 8, 10, "#6F8FB5", "#5A7AA0", 3) + block(0, 9, 7, 13, 6, "#6F8FB5", "#5A7AA0", 2) + block(41, 9, 7, 13, 6, "#6F8FB5", "#5A7AA0", 2)
            + block(7, 11, 34, 10, 4, "#8CA9CC", "#6F8FB5", 2) + block(10, 9, 9, 5, 2, "#F7D07A", "#E7C878", 2) + plant_small(46, 2))

def o_standing():
    return (shadow(16, 34, 16, 2) + rect(2, 16, 2, 18, DK) + rect(28, 16, 2, 18, DK) + rect(0, 32, 32, 2, DK, 1)
            + block(0, 8, 32, 9, 4, "#F2EDE4", "#D8CDBE") + screen(9, 0, 14, 9) + ell(28, 12, 1.4, 1.6, "#DDE1E5", OL, 0.3) + rect(4, 30, 24, 4, "#5A6B80", 1, OL, 0.3))

def o_mailshelf():
    out = block(0, 0, 30, 5, 24, W_, WD)
    for r in range(3):
        for c in range(4):
            out += rect(2 + c * 6.8, 7 + r * 7, 6, 6, "#7A5A42", 0.4)
            if (r + c) % 2 == 0:
                out += rect(2.6 + c * 6.8, 9 + r * 7, 4.8, 3.6, ["#FFFFFF", "#F7E1A0", "#BFE3F5"][(r + c) % 3], 0.3, OL, 0.2)
    return out

def o_tabletennis():
    return (shadow(24, 26, 24, 2.4) + block(0, 0, 48, 20, 4, "#3E8C6A", "#2F6F54", 1.4) + line(24, 0.5, 24, 19.5, WH_, 0.6) + line(1, 10, 47, 10, WH_, 0.4)
            + rect(23, -2, 2, 22, "rgba(255,255,255,.6)", 0.4, OL, 0.3) + legs(2, 24, 44) + ell(10, 6, 1.2, 1.2, "#FFFFFF", OL, 0.3)
            + ell(38, 14, 2.6, 2.6, "#E06A52", OL, 0.35) + rect(39.6, 15.6, 1.2, 3.6, W_))

OFFICE = [("pcdesk", "듀얼 모니터 책상", 44, 34, o_pcdesk, True), ("partition", "파티션 자리", 44, 37, o_partition, True), ("whiteboard", "화이트보드", 36, 31, o_whiteboard, True),
          ("printer", "복합기", 24, 28, o_printer, True), ("cooler", "정수기", 20, 37, o_cooler, True), ("cabinet", "서류 캐비닛", 18, 34, o_cabinet, True),
          ("meeting", "회의 테이블", 60, 35, o_meeting, True), ("officechair", "사무용 의자", 18, 27, o_chair, False), ("coffee", "커피 스테이션", 30, 30, o_coffee, True),
          ("projector", "프로젝터 스크린", 44, 35, o_projector, True), ("lounge", "라운지 소파", 48, 28, o_lounge, True), ("standing", "스탠딩 책상", 32, 35, o_standing, True),
          ("mailshelf", "우편함 선반", 30, 29, o_mailshelf, True), ("pingpong", "탁구대", 48, 28, o_tabletennis, True)]

# ======================================================== CAFE (카페)
def c_espresso():
    return (block(0, 10, 40, 12, 12, "#E2C29A", "#C39E73") + rect(4, 0, 18, 14, "#B9C4CD", 1.6, OL, 0.5) + rect(6, 2, 14, 3, "#DDE1E5", 0.6)
            + rect(8, 7, 2, 4, DK) + rect(16, 7, 2, 4, DK) + rect(7, 11, 4, 3, WH_, 0.4, OL, 0.25) + ell(30, 9, 5, 4, "#7A5238", OL, 0.4) + rect(27, 12, 6, 3, DK, 0.5)
            + rect(34, 12, 4, 6, WH_, 0.6, OL, 0.3))

def c_pastry():
    out = block(0, 4, 40, 12, 14, "#F2EDE4", "#D8CDBE") + rect(2, 0, 36, 12, "rgba(200,230,245,.55)", 2, OL, 0.45) + line(2, 6, 38, 6, "rgba(255,255,255,.7)", 0.5)
    for i, c in enumerate(("#E8B64C", "#D98B6A", "#F7C9B8", "#B7A1D9", "#E8B64C")):
        out += ell(6 + i * 7, 4, 2.6, 1.6, c, OL, 0.3) + ell(6 + i * 7, 9.5, 2.6, 1.4, ["#F29A7F", "#FFFFFF", "#8DB596", "#D98B6A", "#F7D07A"][i], OL, 0.3)
    return out + rect(4, 20, 32, 3, "rgba(0,0,0,.06)", 1)

def c_roundset():
    return (chair(0, 6, 12, 10, 4, W_, "#8DB596") + chair(32, 6, 12, 10, 4, W_, "#8DB596") + shadow(22, 28, 10, 2) + rect(20.6, 14, 2.8, 12, DK)
            + ell(22, 26, 5, 1.6, DK) + ell(22, 13, 10, 4, "#F2EDE4", OL, 0.5) + ell(22, 14.5, 10, 4, "#D8CDBE") + ell(22, 13, 10, 4, "#F2EDE4", OL, 0.5) + mug(18, 9) + ell(26.5, 12.4, 2, 1.1, WH_, OL, 0.3))

def c_barstools():
    out = block(0, 0, 50, 8, 6, W_, WD)
    for i in range(3):
        x = 6 + i * 16
        out += shadow(x, 26, 4, 1) + rect(x - 0.6, 16, 1.2, 10, DK) + ell(x, 25.4, 3, 0.8, DK) + ell(x, 15, 4.4, 2, "#E06A52", OL, 0.4)
    return out + mug(10, 1) + plant_small(42, 5)

def c_beans():
    out = ""
    for i, (x, c) in enumerate(((0, "#C9A076"), (14, "#B98D62"), (7, "#D6B087"))):
        y = 6 if i < 2 else 0
        out += shadow(x + 6, y + 18, 6, 1.4) + path(f"M{x},{y+18} L{x+1},{y+4} Q{x+6},{y} {x+11},{y+4} L{x+12},{y+18} Z", c, OL, 0.45) + rect(x + 3, y + 9, 6, 4, CR, 0.5, OL, 0.25) + ell(x + 6, y + 11, 1.2, 0.8, "#7A5238")
    out += ell(8, 22, 2, 1, "#7A5238") + ell(11, 23, 1.2, 0.7, "#5A4033")
    return out

def c_coldbrew():
    return (block(0, 12, 26, 8, 8, W_, WD) + rect(3, 0, 8, 14, "rgba(200,230,245,.6)", 1.4, OL, 0.45) + rect(3.6, 5, 6.8, 8.4, "#6B4630", 1) + rect(15, 0, 8, 14, "rgba(200,230,245,.6)", 1.4, OL, 0.45)
            + rect(15.6, 6, 6.8, 7.4, "#F2C9A8", 1) + rect(6, 14, 2, 2, DK) + rect(18, 14, 2, 2, DK) + ell(4, 2, 1, 1, "#FFFFFF"))

def c_pos():
    return (block(0, 6, 26, 10, 10, "#E2C29A", "#C39E73") + rect(4, 0, 12, 8, OL, 1) + rect(5, 1, 10, 6, "#DCEAF2", 0.6) + rect(6, 2, 5, 1, "#8DB596")
            + rect(18, 3, 6, 4, "#F2EDE4", 0.6, OL, 0.3) + ell(21, 12, 2, 0.8, "#E8B64C", OL, 0.25) + rect(3, 10, 8, 3, "#3A3F45", 0.6))

def c_booth():
    return (block(0, 0, 50, 8, 12, "#C9564B", "#A94540", 3) + block(0, 26, 50, 8, 6, "#C9564B", "#A94540", 3) + shadow(25, 30, 18, 2)
            + block(8, 12, 34, 12, 6, "#E2C29A", "#C39E73") + mug(14, 14) + ell(30, 17, 3, 1.4, WH_, OL, 0.3) + ell(30, 16.6, 1.8, 0.7, "#D98B6A"))

def c_cakestand():
    return (shadow(10, 22, 9, 1.6) + rect(9.2, 4, 1.6, 18, "#E9C46A", 0.6) + ell(10, 21, 6, 1.8, "#E9C46A", OL, 0.35) + ell(10, 15, 9, 3, WH_, OL, 0.45)
            + ell(10, 8, 6, 2, WH_, OL, 0.4) + ell(6, 13.4, 2, 1.2, "#F7C9B8", OL, 0.25) + ell(12, 13, 2, 1.2, "#E8B64C", OL, 0.25) + ell(10, 6.6, 2, 1.2, "#D98BA6", OL, 0.25) + ell(10, 2.5, 1.2, 1.2, "#E06A52", OL, 0.25))

def c_plantshelf():
    out = rect(0, 0, 1.6, 30, W_) + rect(30.4, 0, 1.6, 30, W_)
    for i in range(3):
        out += rect(0, 8 + i * 9, 32, 2, WL, 0.6, OL, 0.3)
        for j in range(3):
            out += plant_small(5 + j * 11, 8 + i * 9)
    return out

def c_board():
    out = shadow(16, 30, 16, 1.6) + rect(0, 0, 32, 24, "#C9A076", 1.4, OL, 0.5) + rect(2, 2, 28, 20, "#D9B48A", 0.8)
    for i, (x, y, w, h, c) in enumerate(((4, 4, 8, 7, "#FFE7A3"), (14, 3, 9, 9, "#FFFFFF"), (24, 5, 5, 6, "#F7C9B8"), (5, 13, 10, 7, "#BFE3F5"), (18, 14, 9, 6, "#B9D7C1"))):
        out += rect(x, y, w, h, c, 0.3, OL, 0.25) + ell(x + w / 2, y + 0.8, 0.7, 0.7, ["#E06A52", "#2F6FA8", "#6FA387"][i % 3])
    return out + rect(5, 24, 1.4, 6, WD) + rect(25.6, 24, 1.4, 6, WD)

def c_takeout():
    return (block(0, 6, 34, 10, 12, "#F2EDE4", "#D8CDBE") + rect(0, 0, 34, 6, "#E99A6E", 1, OL, 0.4) + path("M0,6 " + " ".join(f"q{2.83/1},3 5.66,0" for _ in range(6)), "#E99A6E", OL, 0.35)
            + rect(4, 8, 7, 7, WH_, 1, OL, 0.3) + rect(13, 9, 6, 6, "#C9A076", 0.6, OL, 0.3) + rect(22, 8, 8, 4, WH_, 0.6, OL, 0.3) + f'<text x="17" y="24" font-family="Jua, sans-serif" font-size="4" fill="#9C7450" text-anchor="middle">TAKE OUT</text>')

CAFE = [("espresso", "에스프레소 바", 40, 34, c_espresso, True), ("pastry", "디저트 쇼케이스", 40, 30, c_pastry, True), ("roundset", "원형 테이블 세트", 44, 30, c_roundset, True),
        ("barstools", "창가 바 테이블", 50, 27, c_barstools, True), ("beans", "원두 자루", 26, 26, c_beans, True), ("coldbrew", "콜드브루 디스펜서", 26, 28, c_coldbrew, True),
        ("pos", "계산대", 26, 26, c_pos, True), ("booth", "부스 좌석", 50, 40, c_booth, True), ("cakestand", "케이크 스탠드", 20, 23, c_cakestand, False),
        ("plantshelf", "식물 선반", 32, 32, c_plantshelf, True), ("board", "동네 게시판", 32, 30, c_board, True), ("takeout", "테이크아웃 창구", 34, 28, c_takeout, True),
        ("armchair", "1인 소파", 24, 28, h_armchair, True)]

# ======================================================== RESTAURANT (식당)
def r_round():
    out = ""
    for (x, y) in ((16, 0), (0, 14), (34, 14)):
        out += chair(x, y, 12, 10, 3, W_, "#F2C9A8")
    out += shadow(23, 36, 14, 2.4) + ell(23, 24, 14, 6, "#FFFDF6", OL, 0.5) + ell(23, 26, 14, 6, "#E7D7C0") + ell(23, 24, 14, 6, "#FFFDF6", OL, 0.5)
    out += ell(23, 23.6, 4, 1.8, WH_, OL, 0.3) + ell(23, 23.2, 2.6, 1, "#E06A52") + ell(15, 25, 2.4, 1.2, WH_, OL, 0.3) + ell(31, 25, 2.4, 1.2, WH_, OL, 0.3)
    return out

def r_stove():
    out = block(0, 4, 46, 12, 14, "#B9C4CD", "#97A4AE") + rect(0, 0, 46, 5, "#DDE1E5", 1, OL, 0.4)
    for x in (8, 22, 36):
        out += ell(x, 9, 4, 2.4, DK) + ell(x, 9, 2, 1.2, "#E06A52")
    out += ell(8, 7, 4.6, 2.6, "#5A5F66", OL, 0.4) + rect(12, 6, 5, 1.2, DK) + ell(22, 7.6, 4.2, 2, "#E2C29A", OL, 0.35) + ell(22, 7, 2.4, 1, "#F7D07A")
    for i in range(3):
        out += rect(4 + i * 14, 20, 10, 6, "rgba(0,0,0,.08)", 1, OL, 0.25) + ell(9 + i * 14, 23, 1, 1, DK)
    return out + path("M8,4 q-2,-3 0,-6 M22,4 q2,-3 0,-6", "none", "rgba(200,200,210,.8)", 0.8)

def r_grill():
    out = shadow(14, 26, 14, 2) + rect(0, 4, 28, 14, DK, 3, OL, 0.5) + rect(2, 6, 24, 10, "#5A5F66", 2)
    for i in range(5):
        out += line(4 + i * 5, 6.5, 4 + i * 5, 15.5, "#8C9AA6", 0.6)
    out += rect(5, 8, 7, 4, "#C9564B", 1.6, OL, 0.3) + rect(15, 9, 7, 4, "#D98B6A", 1.6, OL, 0.3) + ell(22, 7, 1.6, 1, "#8DB596")
    out += rect(2, 18, 2, 8, GR) + rect(24, 18, 2, 8, GR) + path("M8,4 q-2,-3 0,-6 M18,4 q2,-3 0,-6", "none", "rgba(200,200,210,.8)", 0.8)
    return out

def r_sushibar():
    out = block(0, 0, 56, 12, 10, "#E2C29A", "#C39E73") + rect(2, 3, 52, 6, "#8C9AA6", 3, OL, 0.35)
    for i in range(6):
        x = 6 + i * 8.6
        out += ell(x, 6, 3, 1.6, WH_ if i % 2 else "#2F6FA8", OL, 0.3) + ell(x, 5.4, 1.6, 0.8, ["#F29A7F", "#F7D07A", "#E06A52"][i % 3])
    for i in range(4):
        out += shadow(8 + i * 14, 34, 3, 1) + rect(7.4 + i * 14, 26, 1.2, 8, DK) + ell(8 + i * 14, 25, 4, 1.8, "#C9564B", OL, 0.4)
    return out

def r_winerack():
    out = block(0, 0, 26, 6, 26, W_, WD)
    for r in range(4):
        for c in range(4):
            out += ell(4 + c * 6, 10 + r * 5.6, 2.2, 2.2, "#5A4033") + ell(4 + c * 6, 10 + r * 5.6, 1.4, 1.4, ["#7A2E3A", "#6FA387", "#7A2E3A", "#E9C46A"][(r + c) % 4])
    return out

def r_saladbar():
    out = block(0, 8, 50, 12, 10, "#E2C29A", "#C39E73") + rect(2, 0, 46, 12, "rgba(200,230,245,.45)", 2, OL, 0.4)
    for i, c in enumerate(("#8DB596", "#E06A52", "#F7D07A", "#F29A7F", "#B7E3A0", "#D98BA6")):
        out += rect(4 + i * 7.4, 9, 6.4, 6, "#DDE1E5", 1, OL, 0.3) + ell(7.2 + i * 7.4, 11.4, 2.4, 1.6, c)
    return out

def r_bar():
    out = block(0, 0, 50, 10, 12, "#7A5238", "#5A4033") + rect(0, 0, 50, 2, "#9C6B45", 1)
    for i in range(3):
        x = 8 + i * 17
        out += shadow(x, 34, 4, 1) + rect(x - 0.6, 26, 1.2, 8, DK) + ell(x, 25, 4.2, 1.8, "#E9C46A", OL, 0.4)
    out += path("M10,3 l4,0 l-2,3 z", "rgba(220,240,255,.7)", OL, 0.3) + rect(11.4, 6, 1.2, 2, OL) + rect(28, 1, 3, 7, "#6FA387", 1, OL, 0.3)
    return out

def r_highchair():
    return (shadow(9, 30, 8, 1.4) + line(3, 14, 1, 30, W_, 1.4) + line(15, 14, 17, 30, W_, 1.4) + block(2, 0, 14, 6, 10, WL, WLD, 2)
            + block(1, 10, 16, 6, 3, "#F7D07A", "#E7C878", 2) + ell(9, 12, 3, 1, "#E06A52"))

def r_dessertcart():
    return (shadow(16, 30, 16, 2) + ell(5, 28, 3, 3, DK) + ell(27, 28, 3, 3, DK) + block(0, 10, 32, 10, 6, "#F2EDE4", "#D8CDBE", 2)
            + path("M4,12 Q16,0 28,12 Z", "rgba(220,240,255,.6)", OL, 0.45) + ell(10, 11, 3, 1.6, "#D98BA6", OL, 0.3) + ell(17, 10.4, 3, 1.6, "#E8B64C", OL, 0.3) + ell(23, 11, 2.4, 1.4, "#FFFFFF", OL, 0.3)
            + rect(14.4, 3.6, 3, 1.6, "#E9C46A", 0.6) + rect(30, 12, 6, 1.6, GR, 0.8))

def r_fishtank():
    return (block(0, 16, 40, 6, 8, DK, "#2A2E33") + rect(0, 0, 40, 17, "#8CC7E6", 1.4, OL, 0.5) + rect(1, 13, 38, 3, "#E9D8B6", 0.5)
            + path("M8,14 q2,-8 0,-11 M33,14 q-2,-6 0,-9", "none", "#5E9E52", 1.2)
            + path("M14,7 q4,-3 7,0 q-3,3 -7,0 l-2,-1.6 l0,3.2 z", "#F29A4F", OL, 0.3) + path("M24,10 q3,-2 5,0 q-2,2 -5,0 l-1.4,-1.2 l0,2.4 z", "#F7D07A", OL, 0.3)
            + ell(26, 4, 0.8, 0.8, WH_, OL, 0.2) + ell(27, 2, 0.6, 0.6, WH_, OL, 0.2))

def r_host():
    return (shadow(9, 30, 9, 1.6) + block(0, 4, 18, 8, 18, "#7A5238", "#5A4033", 2) + rect(2, 0, 14, 8, "#FFFDF6", 0.6, OL, 0.35)
            + rect(4, 2, 10, 0.8, "#B0835C") + rect(4, 4, 7, 0.8, "#B0835C") + ell(14, 18, 1.6, 1.6, "#E9C46A", OL, 0.3))

def r_kitchenpass():
    out = block(0, 4, 54, 10, 12, "#DDE1E5", "#B9C4CD") + rect(0, 0, 54, 4, "#5A5F66", 1, OL, 0.4)
    for i in range(4):
        x = 8 + i * 13
        out += ell(x, 8, 4.6, 2.2, WH_, OL, 0.35) + ell(x, 7.6, 3, 1.2, ["#E06A52", "#F7D07A", "#8DB596", "#D98B6A"][i])
    out += ell(50, 6, 1.6, 1.6, "#E9C46A", OL, 0.3) + f'<text x="27" y="23" font-family="Jua, sans-serif" font-size="4" fill="#5A5F66" text-anchor="middle">ORDER UP</text>'
    return out

def r_buffet():
    out = block(0, 6, 54, 12, 10, "#FFFDF6", "#E7D7C0")
    for i in range(3):
        x = 10 + i * 17
        out += ell(x, 10, 7, 3, "#B9C4CD", OL, 0.4) + path(f"M{x-7},{10} Q{x},{1} {x+7},{10} Z", "#DDE1E5", OL, 0.4) + ell(x, 4.6, 1.2, 0.8, DK)
    return out

DINING = [("roundtable", "원형 테이블(3인)", 46, 38, r_round, True), ("stove", "주방 화구", 46, 30, r_stove, True), ("grill", "숯불 그릴", 28, 26, r_grill, True),
          ("sushibar", "초밥 바", 56, 35, r_sushibar, True), ("winerack", "와인 랙", 26, 32, r_winerack, True), ("saladbar", "샐러드 바", 50, 30, r_saladbar, True),
          ("bar", "바 카운터", 50, 35, r_bar, True), ("highchair", "아기 의자", 18, 31, r_highchair, True), ("dessertcart", "디저트 카트", 36, 31, r_dessertcart, True),
          ("fishtank", "수족관", 40, 30, r_fishtank, True), ("host", "안내 데스크", 18, 31, r_host, True), ("kitchenpass", "주방 픽업대", 54, 26, r_kitchenpass, True),
          ("buffet", "뷔페 워머", 54, 28, r_buffet, True), ("booth", "부스 좌석", 50, 40, c_booth, True)]

# ======================================================== GYM (체육관)
def g_treadmill():
    return (shadow(15, 36, 15, 2) + rect(2, 10, 26, 26, DK, 4, OL, 0.5) + rect(5, 12, 20, 22, "#5A5F66", 3) + line(5, 18, 25, 18, "#6B737B", 0.5) + line(5, 26, 25, 26, "#6B737B", 0.5)
            + rect(1, 2, 2, 14, GR) + rect(27, 2, 2, 14, GR) + rect(1, 0, 28, 6, "#4F5560", 2, OL, 0.45) + rect(9, 1, 12, 3.4, "#8CC7EE", 0.6) + ell(24, 3, 1, 1, "#E06A52"))

def g_pool():
    out = shadow(40, 46, 42, 3) + rect(0, 0, 80, 44, "#E7EEF2", 6, OL, 0.6) + rect(4, 4, 72, 36, "#7CC4E4", 4) + rect(4, 4, 72, 10, "#9AD3EC", 4)
    for i in range(1, 4):
        y = 4 + i * 9
        out += line(5, y, 75, y, "#FFFFFF", 0.6, ' stroke-dasharray="2 1.4"') + "".join(ell(5 + k * 7, y, 0.9, 0.9, "#E06A52" if k % 2 else "#FFFFFF") for k in range(11))
    out += path("M10,20 q4,-2 8,0 M40,30 q4,-2 8,0 M60,12 q3,-2 6,0", "none", "rgba(255,255,255,.7)", 0.8)
    out += rect(70, -2, 1.2, 10, GR) + rect(73, -2, 1.2, 10, GR) + line(70, 1, 74, 1, GR, 0.8) + line(70, 4, 74, 4, GR, 0.8)
    out += ell(20, 28, 4, 4, "#F7D07A", OL, 0.4) + ell(20, 28, 2, 2, "#7CC4E4")
    return out

def g_track():
    out = rect(0, 0, 100, 50, "#D9775F", 25, OL, 0.6) + rect(12, 12, 76, 26, "#8DB596", 13, OL, 0.5)
    for i in (4, 8):
        out += rect(i, i, 100 - 2 * i, 50 - 2 * i, "none", 25 - i, "#FFFFFF", 0.5)
    out += line(50, 0.5, 50, 12, WH_, 1) + rect(20, 18, 60, 14, "none", 7, "rgba(255,255,255,.5)", 0.5)
    return out + f'<text x="50" y="28" font-family="Jua, sans-serif" font-size="6" fill="#FFFFFF" text-anchor="middle">TRACK</text>'

def g_bike():
    return (shadow(14, 30, 12, 1.8) + rect(4, 24, 20, 3, DK, 1.4) + path("M8,24 L12,10 L20,10 L22,24", "none", "#4F5560", 2) + ell(19, 18, 5, 5, "#5A5F66", OL, 0.45)
            + ell(19, 18, 2, 2, "#8C9AA6") + rect(9, 8, 6, 2.4, DK, 1.2) + path("M20,10 L22,4 L26,4", "none", "#4F5560", 1.6) + rect(24, 2, 4, 3, "#8CC7EE", 0.6, OL, 0.3))

def g_rowing():
    return (shadow(22, 20, 22, 1.6) + rect(0, 12, 44, 4, "#4F5560", 2, OL, 0.45) + ell(38, 12, 6, 6, "#5A5F66", OL, 0.45) + ell(38, 12, 3, 3, "#8CC7EE")
            + rect(8, 9, 10, 4, DK, 1.6) + rect(24, 14, 6, 4, "#E06A52", 1) + line(30, 8, 34, 10, DK, 1) + rect(28, 6, 6, 2, GR, 1))

def g_yoga():
    out = ""
    for i, c in enumerate(("#B7A1D9", "#8DB596", "#F29A7F")):
        out += rect(i * 16, 0, 14, 34, c, 2, OL, 0.45) + line(i * 16 + 2, 6, i * 16 + 12, 6, "rgba(255,255,255,.4)", 0.5)
    return out + ell(8, 30, 3, 1.4, WH_, OL, 0.3)

def g_kettle():
    out = block(0, 8, 40, 8, 6, GR, GRD)
    for i, c in enumerate(("#E06A52", "#F2B84B", "#6FA387", "#2F6FA8", "#3A3F45")):
        x = 4 + i * 8
        out += ell(x, 9, 3 + i * 0.2, 3 + i * 0.2, c, OL, 0.4) + path(f"M{x-2},{6} q2,-4 4,0", "none", c, 1.2)
    return out

def g_lockers():
    out = block(0, 0, 44, 6, 26, "#6F8FB5", "#5A7AA0", 1.4)
    for i in range(4):
        out += rect(1.6 + i * 10.6, 8, 9.6, 22, "rgba(255,255,255,.08)", 0.8, OL, 0.3)
        for k in range(3):
            out += line(3.5 + i * 10.6, 10 + k * 1.4, 9 + i * 10.6, 10 + k * 1.4, "rgba(0,0,0,.25)", 0.4)
        out += rect(8.4 + i * 10.6, 18, 1, 3, "#DDE1E5", 0.3)
    return out

def g_bench():
    return (shadow(20, 30, 20, 2) + rect(0, 4, 2, 22, GR) + rect(38, 4, 2, 22, GR) + rect(-2, 6, 44, 1.6, "#B9C4CD", 0.8, OL, 0.3)
            + ell(-1, 7, 3, 5, DK, OL, 0.35) + ell(41, 7, 3, 5, DK, OL, 0.35) + block(12, 12, 16, 16, 4, "#3A3F45", "#2A2E33", 2) + rect(14, 13, 12, 6, "#E06A52", 2))

def g_pullup():
    return (shadow(18, 34, 18, 1.6) + rect(2, 2, 2.4, 32, GR, 0.6, OL, 0.3) + rect(31.6, 2, 2.4, 32, GR, 0.6, OL, 0.3) + rect(0, 0, 36, 3, "#B9C4CD", 1.4, OL, 0.4)
            + rect(0, 32, 8, 2, DK) + rect(28, 32, 8, 2, DK) + rect(8, 22, 20, 3, "#E06A52", 1.4, OL, 0.35))

def g_ring():
    out = shadow(36, 64, 36, 3) + block(0, 4, 72, 52, 6, "#6F8FB5", "#5A7AA0", 2)
    for i, c in enumerate(("#E06A52", "#FFFFFF", "#2F6FA8")):
        out += rect(2, 6 + i * 2.6, 68, 0.9, c) + rect(2, 52 - i * 2.6, 68, 0.9, c)
    for (x, y) in ((1, 4), (69, 4), (1, 54), (69, 54)):
        out += rect(x - 1, y - 4, 3, 8, ["#E06A52", "#2F6FA8"][(x > 30) ^ (y > 30)], 1, OL, 0.35)
    return out + ell(36, 30, 10, 4, "rgba(255,255,255,.15)")

def g_towels():
    out = block(0, 0, 30, 6, 22, WL, WLD)
    for r in range(2):
        for c in range(3):
            out += rect(2 + c * 9.2, 8 + r * 7, 8, 5, ["#FFFFFF", "#8CC7EE", "#F7C9B8"][(r + c) % 3], 1.6, OL, 0.3)
    return out

def g_score():
    return (shadow(22, 30, 22, 1.6) + rect(20.8, 18, 2.4, 12, GR) + rect(0, 0, 44, 20, DK, 2, OL, 0.5) + rect(3, 3, 17, 11, "#1F1B1F", 1) + rect(24, 3, 17, 11, "#1F1B1F", 1)
            + f'<text x="11.5" y="11.6" font-family="Jua, sans-serif" font-size="8" fill="#F2B84B" text-anchor="middle">12</text><text x="32.5" y="11.6" font-family="Jua, sans-serif" font-size="8" fill="#6FCB8A" text-anchor="middle">09</text>'
            + rect(14, 16, 16, 2, "#E06A52", 0.8))

def g_ballrack():
    out = block(0, 10, 40, 8, 8, GR, GRD)
    for i, c in enumerate(("#E99A6E", "#FFFFFF", "#F7D07A", "#8CC7EE")):
        out += ell(6 + i * 9.4, 9, 4.2, 4.2, c, OL, 0.4) + path(f"M{2+i*9.4},9 q4,-2 8,0", "none", shade(c, -0.25), 0.5)
    return out

GYM = [("treadmill", "러닝머신", 30, 36, g_treadmill, True), ("pool", "수영장(레인 3)", 80, 46, g_pool, True), ("track", "달리기 트랙", 100, 50, g_track, False),
       ("bike", "실내 자전거", 28, 30, g_bike, True), ("rowing", "로잉 머신", 44, 20, g_rowing, True), ("yoga", "요가 매트", 46, 34, g_yoga, False),
       ("kettle", "케틀벨 랙", 40, 22, g_kettle, True), ("lockers", "사물함", 44, 32, g_lockers, True), ("benchpress", "벤치프레스", 42, 32, g_bench, True),
       ("pullup", "철봉", 36, 34, g_pullup, True), ("ring", "복싱 링", 72, 64, g_ring, True), ("towels", "수건 선반", 30, 28, g_towels, True),
       ("scoreboard", "점수판", 44, 30, g_score, True), ("ballrack", "공 거치대", 40, 26, g_ballrack, True)]

# ======================================================== PARK (공원)
def p_slide():
    return (shadow(22, 40, 22, 2.4) + rect(2, 4, 2, 30, "#E06A52") + rect(14, 4, 2, 30, "#E06A52") + block(0, 0, 18, 10, 3, "#F7D07A", "#E7C878", 1)
            + line(4, 14, 14, 14, "#E06A52", 1) + line(4, 20, 14, 20, "#E06A52", 1) + line(4, 26, 14, 26, "#E06A52", 1)
            + path("M16,2 L40,30 Q42,34 38,34 L34,34 L12,8 Z", "#6FB0DA", OL, 0.5) + path("M18,6 L38,30", "none", "rgba(255,255,255,.6)", 1))

def p_swing():
    out = shadow(24, 36, 24, 2) + path("M2,36 L8,2 L14,36 M34,36 L40,2 L46,36", "none", "#B98D62", 2) + rect(6, 0, 36, 3, "#C9A076", 1.4, OL, 0.4)
    for x, c in ((16, "#E06A52"), (30, "#2F6FA8")):
        out += line(x - 3, 3, x - 3, 24, GR, 0.5) + line(x + 3, 3, x + 3, 24, GR, 0.5) + rect(x - 4, 24, 8, 2.4, c, 1, OL, 0.35)
    return out

def p_seesaw():
    return (shadow(24, 18, 24, 1.6) + path("M20,18 L24,8 L28,18 Z", "#F7D07A", OL, 0.45) + path("M0,13 L48,5 L48,8 L0,16 Z", "#6FA387", OL, 0.45)
            + rect(3, 8, 6, 5, "#E06A52", 1, OL, 0.3) + rect(39, 1, 6, 5, "#E06A52", 1, OL, 0.3) + line(5, 7, 5, 4, DK, 1) + line(42, 0, 42, -3, DK, 1))

def p_sandbox():
    out = block(0, 0, 44, 30, 3, "#C9A076", "#A9805A", 2) + rect(3, 3, 38, 24, "#F1E2BC", 2) + ell(14, 14, 6, 3, "#E8D5A6")
    out += path("M28,18 l4,-6 l4,6 z", "#E8D5A6", OL, 0.3) + rect(10, 18, 5, 4, "#E06A52", 0.6, OL, 0.3) + line(34, 8, 38, 4, "#2F6FA8", 1) + ell(33, 9, 2, 1.2, "#2F6FA8")
    return out

def p_picnic():
    return (shadow(22, 34, 22, 2) + block(0, 0, 44, 5, 3, WL, WLD, 1) + block(0, 26, 44, 5, 3, WL, WLD, 1) + block(2, 8, 40, 14, 4, WL, WLD, 1)
            + path("M6,9 h32 v12 h-32 z", "#F7C9B8") + "".join(line(6 + i * 4, 9, 6 + i * 4, 21, "rgba(255,255,255,.7)", 1) for i in range(9))
            + ell(16, 14, 3, 1.6, WH_, OL, 0.3) + rect(26, 11, 6, 5, "#C9A076", 0.8, OL, 0.3))

def p_gazebo():
    out = shadow(30, 58, 30, 3) + ell(30, 50, 26, 8, "#D8D2C2", OL, 0.5)
    for x in (8, 30, 52):
        out += rect(x - 1.4, 24, 2.8, 26, WH_, 0.6, OL, 0.35)
    out += path("M2,26 L30,4 L58,26 Q30,32 2,26 Z", "#C9564B", OL, 0.6) + path("M10,24 L30,8 L50,24", "none", "#E06A52", 0.8) + ell(30, 4, 2, 2, "#E9C46A", OL, 0.3)
    return out + p_bench_small(22, 46)

def p_bench_small(x, y):
    return block(x - 7, y - 4, 14, 3, 2, WL, WLD, 0.8)

def p_arch():
    out = shadow(22, 40, 22, 1.6) + path("M4,40 L4,18 Q4,0 22,0 Q40,0 40,18 L40,40", "none", "#7A5A42", 1.6)
    for i in range(14):
        import math as m
        a = m.pi * (1 - i / 13)
        x, y = 22 + m.cos(a) * 18, 18 - m.sin(a) * 18
        if i == 0 or i == 13:
            y = 22
        out += ell(x, y, 3, 2.6, "#6FB05E", OL, 0.3) + ell(x + 1, y - 1, 1, 1, ["#F29A7F", "#FFFFFF", "#D98BA6"][i % 3])
    for y in (28, 34):
        out += ell(4, y, 3, 2.4, "#6FB05E", OL, 0.3) + ell(40, y, 3, 2.4, "#6FB05E", OL, 0.3)
    return out

def p_bikerack():
    out = shadow(22, 26, 22, 1.4) + rect(0, 22, 44, 2, GR, 1)
    for i in range(4):
        out += path(f"M{4+i*11},{23} L{4+i*11},{12} Q{4+i*11},{8} {8+i*11},{8} Q{12+i*11},{8} {12+i*11},{12} L{12+i*11},{23}", "none", GR, 1.2)
    out += ell(10, 18, 5, 5, "none", DK, 1) + ell(22, 18, 5, 5, "none", DK, 1) + path("M10,18 L15,12 L22,18 L14,18 Z M15,12 L14,9", "none", "#E06A52", 1)
    return out

def p_icecream():
    return (shadow(18, 34, 18, 2) + ell(6, 32, 3, 3, DK) + ell(30, 32, 3, 3, DK) + block(0, 14, 36, 8, 10, "#F7C9B8", "#E8A9A0", 2)
            + rect(2, 0, 1.4, 16, GR) + path("M-4,2 Q2,-6 8,2 Z", "#8CC7EE", OL, 0.4) + path("M8,2 Q14,-6 20,2 Z", "#FFFFFF", OL, 0.4)
            + path("M24,10 l3,8 l3,-8 z", "#E2C29A", OL, 0.35) + ell(27, 9, 3, 2.6, "#D98BA6", OL, 0.35) + ell(10, 18, 2.6, 1.4, WH_, OL, 0.3)
            + f'<text x="18" y="27" font-family="Jua, sans-serif" font-size="4.2" fill="#C9564B" text-anchor="middle">ICE</text>')

def p_drinking():
    return (shadow(8, 26, 8, 1.4) + rect(4, 8, 8, 18, "#B9C4CD", 2, OL, 0.45) + ell(8, 8, 7, 3, "#DDE1E5", OL, 0.45) + ell(8, 8, 4.4, 1.6, "#8CC7E6")
            + rect(7.4, 4, 1.4, 4, GR) + path("M8.8,4 q3,-3 4,2", "none", "#8CC7E6", 0.8))

def p_trash():
    return (shadow(8, 22, 8, 1.4) + rect(1, 6, 14, 16, "#6FA387", 2, OL, 0.45) + ell(8, 6, 7.6, 2.6, "#5A8C72", OL, 0.45) + ell(8, 5.6, 4, 1.2, DK)
            + line(5, 10, 5, 19, "rgba(255,255,255,.3)", 1) + line(11, 10, 11, 19, "rgba(255,255,255,.3)", 1) + rect(5, 12, 6, 4, "#FFFFFF", 0.6) + path("M6,14.6 l1.2,-1.6 l1.6,2 l1.2,-1.2", "none", "#6FA387", 0.5))

def p_signpost():
    return (shadow(8, 32, 6, 1.2) + rect(7, 2, 2, 30, W_, 0.5, OL, 0.3) + path("M8,4 L28,4 L32,7.5 L28,11 L8,11 Z", "#E2C29A", OL, 0.45) + path("M8,13 L-10,13 L-14,16.5 L-10,20 L8,20 Z", "#B9D7C1", OL, 0.45)
            + f'<text x="19" y="9" font-family="Jua, sans-serif" font-size="4" fill="#7A5238" text-anchor="middle">카페</text><text x="-2" y="18" font-family="Jua, sans-serif" font-size="4" fill="#4F7F63" text-anchor="middle">연못</text>')

def p_junglegym():
    out = shadow(24, 36, 26, 2) + block(0, 8, 48, 26, 2, "#F7D07A", "#E7C878", 1, False)
    out = shadow(24, 36, 26, 2)
    for x in (2, 24, 46):
        out += rect(x - 1, 4, 2, 32, "#2F6FA8")
    for y in (6, 16, 26):
        out += line(2, y, 46, y, "#E06A52", 1.4)
    out += path("M2,4 L24,-4 L46,4", "none", "#6FA387", 1.4) + rect(10, 15, 10, 2, "#F7D07A", 0.6, OL, 0.3)
    return out

def p_duckboat():
    out = ell(26, 16, 26, 10, "#8CC7E6", OL, 0.5) + ell(26, 17, 22, 7.4, "#79B8DA")
    out += path("M14,18 q4,-6 12,-2 q4,-6 8,0 q-2,4 -10,4 z", "#FFFFFF", OL, 0.4) + ell(31, 11, 3, 2.6, "#FFFFFF", OL, 0.35) + path("M33.6,11 l2.4,0.6 l-2.4,0.8 z", "#F2B84B")
    out += path("M38,20 q2,-3 4,0 q-2,2 -4,0", "#F7D07A", OL, 0.3) + ell(41, 18.6, 1.4, 1.2, "#F7D07A", OL, 0.3) + path("M8,14 q2,-1 4,0 M40,24 q2,-1 4,0", "none", "rgba(255,255,255,.7)", 0.6)
    return out

PARK = [("slide", "미끄럼틀", 42, 40, p_slide, True), ("swing", "그네", 48, 37, p_swing, True), ("seesaw", "시소", 48, 19, p_seesaw, True),
        ("sandbox", "모래놀이터", 44, 33, p_sandbox, False), ("picnic", "피크닉 테이블", 44, 35, p_picnic, True), ("gazebo", "정자", 60, 60, p_gazebo, True),
        ("arch", "꽃 아치", 44, 41, p_arch, False), ("bikerack", "자전거 거치대", 44, 26, p_bikerack, True), ("icecream", "아이스크림 카트", 36, 35, p_icecream, True),
        ("drinking", "음수대", 16, 26, p_drinking, True), ("trash", "분리수거함", 16, 23, p_trash, True), ("signpost", "이정표", 32, 32, p_signpost, True),
        ("junglegym", "정글짐", 48, 37, p_junglegym, True), ("duckpond", "오리 연못", 52, 27, p_duckboat, True)]

CATALOG = {"home": ("집", HOME), "work": ("작업실·사무실", OFFICE), "cafe": ("카페", CAFE), "dining": ("식당", DINING), "gym": ("체육관", GYM), "park": ("공원", PARK)}
