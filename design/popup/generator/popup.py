"""Harulog popup buildings — 7 temporary 'real' buildings (clinic, cinema, library, market, salon, office, stage).
Furniture is drawn with its footprint's top-left at (0,0); room layouts use the 224-wide base like KINDS (+cx for bigger sizes)."""
import math
import art
from art import *
from furniture import screen, mug, legs, W_, WD, WL, WLD, GR, GRD, DK, WH_, CR

# ---------------------------------------------------------------- new floors
_old_floor = art.floor_fill
def _floor(kind, x, y, w, h, uid):
    if kind not in ("carpet", "checker", "clinic", "stagewood"):
        return _old_floor(kind, x, y, w, h, uid)
    cid = f"fl{uid}"
    out = f'<clipPath id="{cid}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"></rect></clipPath><g clip-path="url(#{cid})">'
    if kind == "carpet":
        out += rect(x, y, w, h, "#5B3A4E")
        for i, yy in enumerate(range(int(y), int(y + h) + 12, 12)):
            for j, xx in enumerate(range(int(x) + (i % 2) * 6, int(x + w), 12)):
                out += ell(xx, yy, 1.2, 0.8, "#7A4E68") + ell(xx + 6, yy + 6, 0.6, 0.6, "#E9C46A")
    elif kind == "checker":
        out += rect(x, y, w, h, "#F4F1EC")
        for r, yy in enumerate(range(int(y), int(y + h) + 12, 12)):
            for c, xx in enumerate(range(int(x), int(x + w) + 12, 12)):
                if (r + c) % 2 == 0:
                    out += rect(xx, yy, 12, 12, "#3E3A40")
    elif kind == "clinic":
        out += rect(x, y, w, h, "#EEF4F3")
        for yy in range(int(y), int(y + h), 16):
            out += rect(x, yy, w, 0.5, "#D6E2E0")
        for xx in range(int(x), int(x + w), 16):
            out += rect(xx, y, 0.5, h, "#D6E2E0")
        out += rect(x, y + h * 0.55, w, 4, "#B9DCD5")  # guide line
    else:  # stagewood
        out += rect(x, y, w, h, "#3E3438")
        for yy in range(int(y), int(y + h), 7):
            out += rect(x, yy, w, 0.5, "#2E272A")
    return out + "</g>"
art.floor_fill = _floor

POPUP = {
    "clinic":  dict(label="병원", wall="#E8F3F1", line="#D3E8E4", sign="#3E9C8C", floor="clinic", wall2="#F4EEF6"),
    "cinema":  dict(label="영화관", wall="#3B2F3E", line="#4A3A4E", sign="#C9364B", floor="carpet", wall2="#2E3448"),
    "library": dict(label="도서관", wall="#EFE4CF", line="#E2D2B4", sign="#7A5A42", floor="wood", wall2="#E3EBDD"),
    "market":  dict(label="마트", wall="#FFF4DE", line="#F7E6C2", sign="#E8793A", floor="tile", wall2="#E9F4E3"),
    "salon":   dict(label="미용실", wall="#FBE4EA", line="#F3D1DA", sign="#C95B7E", floor="checker", wall2="#E6ECF6"),
    "office":  dict(label="은행·관공서", wall="#E4ECF4", line="#D3DFEB", sign="#3F6EA8", floor="modern", wall2="#ECE8DF"),
    "stage":   dict(label="노래방·공연", wall="#2F2A45", line="#3D3658", sign="#8B5CD6", floor="stagewood", wall2="#43233A"),
}
for k, v in POPUP.items():
    WALLS["pp_" + k] = dict(label=v["label"], wall=v["wall"], line=v["line"], sign=v["sign"])
    KIND_LABEL[k] = v["label"]

PINK = "#F29A9A"; TEAL = "#3E9C8C"; RED = "#C9364B"

# ================================================================ furniture
# ---- clinic
def cl_reception():
    return (block(0, 6, 44, 10, 12, "#FFFFFF", "#DCE8E6") + rect(0, 6, 44, 2.4, TEAL, 1) + screen(26, 0, 12, 9) + rect(30, 9, 4, 1.4, DK)
            + rect(4, 9, 8, 4, "#FFFFFF", 0.4, OL, 0.3) + line(5, 10.4, 11, 10.4, "#B9C4CD", 0.4) + ell(17, 10, 2, 1.2, "#8CC7EE", OL, 0.3)
            + path("M20,26 l2,-3 l2,3 z", TEAL))
def cl_waiting():
    out = rect(0, 18, 48, 2, GR, 1)
    for i in range(4):
        out += block(i * 12, 4, 11, 9, 5, "#8FC9BE", "#6FB0A3", 2) + block(i * 12, 0, 11, 4, 6, "#7FBFB2", "#5FA396", 1.6)
    return out + rect(2, 18, 1.4, 4, DK) + rect(44, 18, 1.4, 4, DK)
def cl_desk():
    return (block(0, 8, 40, 12, 10, "#E2D8CA", "#C9BBA6") + screen(4, 0, 14, 10) + rect(9, 10, 4, 1.4, DK) + rect(22, 9, 9, 6, "#FFFFFF", 0.4, OL, 0.3)
            + path("M24,10.6 h5 M24,12.4 h4", "none", "#B9C4CD", 0.5) + ell(35, 12, 2.2, 1.4, "#FFFFFF", OL, 0.3) + path("M33.6,12 q1.4,-3 2.8,0", "none", DK, 0.5)
            + chair(6, 26, 14, 10, 3, "#5A6B80", "#8CA9CC"))
def cl_bed():
    return (shadow(22, 30, 22, 2) + block(0, 4, 44, 18, 6, "#FFFFFF", "#DCE8E6") + block(1, 5, 12, 16, 2, "#EAF4F2", "#CFE3DF", 3)
            + rect(14, 5, 29, 16, "#B9DCD5", 1) + "".join(line(16, 7 + i * 3, 42, 7 + i * 3, "rgba(255,255,255,.5)", 0.5) for i in range(5))
            + rect(1, 28, 2, 3, GR) + rect(41, 28, 2, 3, GR))
def cl_medshelf():
    out = block(0, 0, 34, 6, 26, "#FFFFFF", "#DCE8E6")
    for r in range(3):
        out += rect(2, 9 + r * 7.6, 30, 1, "#C9DAD7")
        for i in range(5):
            c = ["#F29A9A", "#8CC7EE", "#F7D07A", "#8DB596", "#FFFFFF"][(i + r) % 5]
            out += rect(3.4 + i * 5.8, 4 + r * 7.6, 4, 5, c, 0.8, OL, 0.25) + rect(3.4 + i * 5.8, 4 + r * 7.6, 4, 1.2, "#FFFFFF", 0.4)
    return out + path("M15,-3.6 h4 v-1.6 h1.6 v1.6 h1.6 v1.6 h-1.6 v1.6 h-1.6 v-1.6 h-4 z", RED)
def cl_scale():
    return (shadow(7, 26, 7, 1.4) + rect(1, 20, 12, 5, "#DDE1E5", 1, OL, 0.4) + rect(6, 2, 2, 18, GR, 0.6) + ell(7, 3, 4.2, 4.2, "#FFFFFF", OL, 0.45)
            + line(7, 3, 9, 1.4, RED, 0.5) + "".join(line(7 + math.cos(a) * 3.4, 3 + math.sin(a) * 3.4, 7 + math.cos(a) * 3.9, 3 + math.sin(a) * 3.9, DK, 0.3) for a in [i * math.pi / 6 for i in range(12)]))
def cl_curtain():
    out = rect(0, 0, 2, 30, GR) + rect(42, 0, 2, 30, GR) + rect(0, 0, 44, 1.4, GR, 0.6)
    for i in range(7):
        out += path(f"M{2+i*5.7},{1.4} q2.8,2 5.7,0 l0,24 q-2.8,2 -5.7,0 z", "#B9DCD5" if i % 2 else "#CFE7E2", OL, 0.3)
    return out + rect(0, 28, 6, 2, DK, 0.6) + rect(38, 28, 6, 2, DK, 0.6)
def cl_iv():
    return (shadow(5, 30, 5, 1.2) + rect(4.2, 4, 1.4, 25, GR) + path("M1,29 l3.9,-2 l3.9,2", "none", GR, 1) + rect(1, 3, 8, 1, GR)
            + rect(1, 4, 4, 7, "rgba(200,230,245,.85)", 1.4, OL, 0.35) + line(3, 11, 3, 16, "#8CC7EE", 0.4))

CLINIC = [("reception", "접수 데스크", 44, 26, cl_reception, True, None), ("waiting", "대기 의자", 48, 22, cl_waiting, True, "대기"),
          ("consultdesk", "진료 책상", 40, 36, cl_desk, True, "진료 받기"), ("exambed", "진료 침대", 44, 31, cl_bed, True, "누워서 진료"),
          ("medshelf", "약 선반", 34, 32, cl_medshelf, True, None), ("scale", "체중계", 14, 26, cl_scale, True, None),
          ("curtain", "커튼 칸막이", 44, 30, cl_curtain, False, None), ("ivstand", "수액 걸이", 10, 30, cl_iv, True, None)]

# ---- cinema
def ci_screen(f=0):
    glow = ["#DCEAF2", "#F7E1A0", "#F7C9B8"][f % 3]
    out = rect(-2, -2, 104, 30, "#1F1B22", 2, OL, 0.6) + rect(0, 0, 100, 26, glow, 1)
    scenes = [path("M0,20 Q25,8 50,16 T100,10 L100,26 L0,26 Z", "#8DB596") + ell(78, 7, 5, 5, "#F7D07A"),
              path("M0,26 L0,14 L20,6 L40,14 L60,4 L80,14 L100,8 L100,26 Z", "#6F8FB5") + ell(24, 5, 2, 2, "#FFFFFF"),
              rect(30, 6, 40, 18, "#E99A6E", 2) + ell(50, 15, 6, 6, "#FFF4E0")]
    return out + scenes[f % 3] + rect(0, 0, 100, 26, "rgba(255,255,255,.12)", 1)
def ci_seats():
    out = block(0, 10, 92, 6, 4, "#3E3438", "#2E272A", 1)
    for i in range(7):
        x = 2 + i * 12.8
        out += block(x, 0, 11, 6, 8, RED, "#A3283A", 2.4) + block(x, 8, 11, 6, 3, "#E0506A", RED, 2)
    return out
def ci_booth():
    return (block(0, 10, 40, 10, 12, "#F2EDE4", "#D8CDBE") + rect(0, 0, 40, 10, RED, 2, OL, 0.45) + rect(4, 2, 32, 6, "#FFE9A8", 1)
            + f'<text x="20" y="6.6" font-family="Jua, sans-serif" font-size="4.6" fill="{RED}" text-anchor="middle">TICKET</text>'
            + rect(8, 13, 10, 6, "#DCEAF2", 1, OL, 0.3) + rect(22, 14, 10, 4, "#F7D07A", 0.6, OL, 0.3))
def ci_popcorn():
    out = shadow(10, 34, 10, 1.6) + block(0, 16, 20, 8, 10, RED, "#A3283A", 1.4) + rect(1, 0, 18, 16, "rgba(220,240,255,.6)", 1.4, OL, 0.45)
    for i in range(16):
        out += ell(3 + (i * 7.3) % 14, 9 + (i * 3.1) % 6, 1.3, 1.1, "#FFF4C2", OL, 0.2)
    return out + rect(0, -3, 20, 4, "#F7D07A", 1.6, OL, 0.4) + f'<text x="10" y="31" font-family="Jua, sans-serif" font-size="3.6" fill="#FFF4C2" text-anchor="middle">POPCORN</text>'
def ci_poster(c="#6F8FB5"):
    return (rect(0, 0, 16, 22, "#E9C46A", 0.6, OL, 0.45) + rect(1.4, 1.4, 13.2, 19.2, c, 0.4) + ell(8, 9, 4, 4, "#FFF4E0")
            + rect(3, 16, 10, 1, "#FFFFFF", 0.3) + rect(4, 18, 8, 0.8, "rgba(255,255,255,.6)", 0.3))
def ci_aisle():
    out = rect(0, 0, 14, 60, "#7A4E68", 1)
    for y in range(4, 60, 10):
        out += ell(2, y, 0.8, 0.8, "#F7D07A") + ell(12, y, 0.8, 0.8, "#F7D07A")
    return out
CINEMA = [("seatrow", "좌석 한 줄", 92, 20, ci_seats, True, "앉아서 영화 보기"), ("ticket", "매표소", 40, 32, ci_booth, True, "표 사기"),
          ("popcorn", "팝콘 기계", 20, 34, ci_popcorn, True, "팝콘 사기"), ("poster", "포스터 액자", 16, 22, lambda: ci_poster(), False, None),
          ("aisle", "통로 카펫·유도등", 14, 60, ci_aisle, False, None)]

# ---- library
def li_tallshelf(w=40):
    out = block(0, 0, w, 6, 34, W_, WD)
    out += rect(1.5, 7, w - 3, 31, "#6E4F3A", 0.8)
    bc = ["#E99A6E", "#8DB596", "#8CB8E0", "#E8B64C", "#D98BA6", "#F2EDE4", "#B7A1D9", "#C9564B"]
    for s in range(4):
        out += rect(1.5, 14 + s * 8, w - 3, 1.4, "#B98D62")
        for i in range(int((w - 6) / 3.4)):
            bh = 6.4 - (1.4 if (i + s) % 4 == 0 else 0)
            out += rect(3 + i * 3.4, 14 + s * 8 - bh, 2.9, bh, bc[(i * 3 + s) % 8], 0.3, OL, 0.2)
    return out
def li_readdesk():
    out = chair(4, 0, 12, 9, 3, W_, "#8DB596") + chair(28, 0, 12, 9, 3, W_, "#8DB596")
    out += block(0, 9, 44, 14, 8, "#D6B087", "#B58C63") + rect(6, 12, 9, 6, "#FFFFFF", 0.4, OL, 0.3) + line(10.5, 12, 10.5, 18, "#B9C4CD", 0.4)
    out += rect(28, 12, 8, 6, "#E99A6E", 0.4, OL, 0.3)
    for x in (20, 40):
        out += rect(x - 0.6, 6, 1.2, 8, "#3E7A5A") + path(f"M{x-3},7 L{x+3},7 L{x+2},3 L{x-2},3 Z", "#3E9C6A", OL, 0.4) + ell(x, 10, 5, 2, "rgba(255,240,170,.35)")
    return out + legs(0, 31, 44, WD)
def li_loandesk():
    return (block(0, 6, 46, 12, 12, "#C9A076", "#A9805A") + screen(30, 0, 12, 9) + rect(34, 9, 4, 1.4, DK) + rect(4, 7, 10, 7, "#8CB8E0", 0.4, OL, 0.3)
            + rect(6, 5, 10, 7, "#E99A6E", 0.4, OL, 0.3) + rect(18, 8, 8, 4, DK, 0.8) + ell(22, 10, 1.4, 1, "#E06A52")
            + f'<text x="23" y="27" font-family="Jua, sans-serif" font-size="4" fill="#FFF4E0" text-anchor="middle">대출·반납</text>')
def li_magazine():
    out = block(0, 4, 26, 6, 20, W_, WD)
    for r in range(3):
        for i in range(3):
            out += path(f"M{2+i*8},{10+r*6.4} l7,0 l-0.6,6 l-6,0 z", ["#F7C9B8", "#BFE3F2", "#F7E1A0"][(i + r) % 3], OL, 0.3)
    return out
def li_beanbag(c="#E8B64C"):
    return shadow(10, 18, 10, 1.6) + path("M1,17 Q-1,6 8,4 Q18,2 19,12 Q20,18 10,18 Z", c, OL, 0.5) + path("M5,10 q5,-3 10,1", "none", shade(c, -0.2), 0.6) + ell(9, 7, 3, 1.4, "rgba(255,255,255,.3)")
def li_globe():
    return (shadow(6, 22, 6, 1.2) + path("M2,22 l4,-2 l4,2 z", W_, OL, 0.4) + rect(5.4, 14, 1.2, 6, WD) + ell(6, 8, 6, 6, "#8CC7EE", OL, 0.45)
            + path("M2,6 q3,-2 4,1 q2,3 5,1 M3,11 q2,1 4,-1", "#8DB596", OL, 0.25) + path("M0,8 a6,6 0 0 1 12,0", "none", "#E9C46A", 0.6))
LIBRARY = [("tallshelf", "높은 책장", 40, 40, li_tallshelf, True, None), ("readdesk", "열람 책상", 44, 34, li_readdesk, True, "책 읽기"),
           ("loandesk", "대출 데스크", 46, 28, li_loandesk, True, "책 빌리기"), ("magazine", "잡지 꽂이", 26, 30, li_magazine, True, None),
           ("beanbag", "빈백", 20, 19, li_beanbag, False, "편하게 읽기"), ("globe", "지구본", 12, 23, li_globe, True, None)]

# ---- market
def mk_produce():
    out = block(0, 8, 50, 14, 10, W_, WD)
    crates = [("#E06A52", "apple"), ("#F2B84B", "orange"), ("#8DB596", "veg"), ("#F7D07A", "banana")]
    for i, (c, k) in enumerate(crates):
        x = 2 + i * 12
        out += rect(x, 2, 11, 10, "#C9A076", 1, OL, 0.35)
        for j in range(5):
            out += ell(x + 2.4 + (j % 3) * 3, 4.6 + (j // 3) * 3.4, 1.6, 1.4, c, OL, 0.25)
    return out + rect(2, 13, 46, 1, "#9C7450")
def mk_snack():
    out = block(0, 0, 44, 6, 28, "#E9EEF2", "#C9D2DA")
    cols = ["#E06A52", "#F7D07A", "#8CB8E0", "#B7A1D9", "#8DB596", "#F29A4F"]
    for s in range(3):
        out += rect(1.6, 14 + s * 7, 40.8, 1, "#B9C4CD")
        for i in range(8):
            out += rect(2.6 + i * 5, 9 + s * 7, 4, 5, cols[(i + s * 2) % 6], 0.8, OL, 0.25) + rect(3.2 + i * 5, 10 + s * 7, 2.8, 1.2, "rgba(255,255,255,.5)", 0.3)
    return out
def mk_fridge():
    out = block(0, 0, 40, 6, 30, "#DDE1E5", "#B9C4CD", 1.4)
    for d in range(2):
        out += rect(2 + d * 18.5, 7.6, 17.5, 27, "rgba(200,230,245,.8)", 1, OL, 0.35)
        for s in range(3):
            for i in range(4):
                out += rect(3.4 + d * 18.5 + i * 4, 10 + s * 8.4, 3, 6, ["#8CC7EE", "#F29A9A", "#F7D07A", "#8DB596"][(i + s + d) % 4], 0.8, OL, 0.2)
        out += rect(18 + d * 18.5, 16, 1, 6, GR, 0.4)
    return out + rect(0, -3, 40, 3.4, "#3E9C8C", 1, OL, 0.35) + f'<text x="20" y="-0.4" font-family="Jua, sans-serif" font-size="2.8" fill="#FFFFFF" text-anchor="middle">음료</text>'
def mk_checkout():
    return (block(0, 6, 48, 12, 12, "#E9EEF2", "#C9D2DA") + rect(2, 8, 28, 7, DK, 1) + "".join(line(4 + i * 3, 8.4, 4 + i * 3, 14.6, "#5A5F66", 0.4) for i in range(9))
            + rect(34, 0, 12, 9, OL, 1) + rect(35, 1, 10, 7, "#DCEAF2", 0.6) + rect(36, 2, 5, 1, "#8DB596") + rect(33, 9, 14, 4, "#5A5F66", 0.8)
            + rect(8, 9, 5, 4, "#F29A9A", 0.6, OL, 0.25) + ell(19, 11, 2, 1.6, "#F2B84B", OL, 0.25))
def mk_cart():
    return (shadow(10, 20, 10, 1.4) + path("M2,4 L18,4 L16,14 L4,14 Z", "none", GR, 0.9) + "".join(line(2 + i * 3.2, 4, 4 + i * 2.4, 14, GR, 0.4) for i in range(6))
            + line(0, 2, 2, 4, DK, 1) + rect(-1, 1, 3, 1.6, "#E06A52", 0.8) + ell(5, 18, 1.6, 1.6, DK) + ell(15, 18, 1.6, 1.6, DK) + line(4, 14, 4, 16.4, GR, 0.8) + line(16, 14, 16, 16.4, GR, 0.8)
            + ell(8, 6, 2, 1.6, "#E06A52", OL, 0.25) + rect(11, 3, 4, 4, "#8DB596", 0.6, OL, 0.25))
def mk_baskets():
    out = shadow(9, 14, 9, 1.4)
    for i in range(4):
        out += path(f"M1,{12-i*2} L17,{12-i*2} L15,{6-i*2} L3,{6-i*2} Z", "#E06A52", OL, 0.4)
    return out + path("M4,0 q5,-5 10,0", "none", DK, 0.8)
MARKET = [("produce", "과일·채소 진열대", 50, 30, mk_produce, True, "장보기"), ("snackshelf", "과자 선반", 44, 34, mk_snack, True, "과자 고르기"),
          ("drinkfridge", "음료 냉장고", 40, 36, mk_fridge, True, "음료 고르기"), ("checkout", "계산대", 48, 30, mk_checkout, True, "계산하기"),
          ("cart", "카트", 20, 20, mk_cart, False, None), ("baskets", "장바구니 더미", 18, 14, mk_baskets, True, None)]

# ---- salon
def sa_station():
    return (rect(4, 0, 22, 18, "#E9C46A", 3, OL, 0.5) + rect(6, 2, 18, 14, "#DCEAF2", 2) + line(9, 13, 15, 4, "rgba(255,255,255,.8)", 1)
            + block(2, 18, 26, 6, 4, "#F2EDE4", "#D8CDBE", 1) + rect(5, 18.6, 3, 4, "#F29A9A", 0.6, OL, 0.25) + rect(9, 18.4, 2.4, 4.4, "#B7A1D9", 0.6, OL, 0.25)
            + shadow(15, 46, 9, 1.6) + ell(15, 45, 6, 1.6, DK) + rect(14, 38, 2, 7, GR) + block(8, 26, 14, 6, 8, "#C95B7E", "#A84466", 3) + block(7, 32, 16, 8, 4, "#E07A9A", "#C95B7E", 3))
def sa_shampoo():
    return (block(0, 0, 24, 10, 10, "#FFFFFF", "#DCE8E6", 3) + ell(12, 5, 7, 3.4, "#BFE3F2", OL, 0.4) + rect(11, 1, 2, 3, GR) + chair(2, 16, 20, 14, 4, DK, "#C95B7E"))
def sa_pole(phase=0):
    out = shadow(4, 30, 4, 1) + rect(1, 0, 6, 3, GR, 1.4, OL, 0.4) + rect(1, 27, 6, 3, GR, 1.4, OL, 0.4) + rect(1.6, 3, 4.8, 24, "#FFFFFF", 0, OL, 0.4)
    cid = "pole"
    out += f'<clipPath id="{cid}"><rect x="1.6" y="3" width="4.8" height="24"></rect></clipPath><g clip-path="url(#{cid})">' + "".join(path(f"M1,{y+phase} l6,-4 l0,2.4 l-6,4 z", RED if i % 2 == 0 else "#3F6EA8") for i, y in enumerate(range(2, 36, 3))) + "</g>"
    return out + ell(4, -1, 2.4, 2.4, "#F2EDE4", OL, 0.4)
def sa_sofa():
    return (shadow(20, 24, 20, 2) + block(0, 0, 40, 7, 8, "#B7A1D9", "#9A84C2", 3) + block(0, 8, 6, 12, 5, "#B7A1D9", "#9A84C2", 2) + block(34, 8, 6, 12, 5, "#B7A1D9", "#9A84C2", 2)
            + block(6, 9, 28, 10, 4, "#CDBDEA", "#B7A1D9", 2) + rect(10, 11, 8, 6, "#FFFFFF", 0.4, OL, 0.25))
def sa_dryer():
    return (shadow(10, 32, 9, 1.4) + chair(2, 18, 16, 12, 3, DK, "#E07A9A") + rect(9, 2, 2, 18, GR) + path("M2,8 Q2,0 10,0 Q18,0 18,8 Q10,11 2,8 Z", "#F2EDE4", OL, 0.5) + ell(10, 6, 5, 1.6, "rgba(0,0,0,.08)"))
def sa_trolley():
    out = shadow(7, 24, 7, 1.2) + rect(0, 4, 14, 2, "#C95B7E", 0.6, OL, 0.35) + rect(0, 12, 14, 2, "#C95B7E", 0.6, OL, 0.35) + rect(0.6, 4, 1.2, 18, GR) + rect(12.2, 4, 1.2, 18, GR)
    out += rect(2, 1, 3, 3, "#F7D07A", 0.6, OL, 0.25) + rect(6, 0, 2.4, 4, "#8CB8E0", 0.6, OL, 0.25) + path("M9,3 l4,-2 l0.6,1 l-4,2 z", GR) + rect(3, 9, 8, 3, "#3A3F45", 1)
    return out + ell(2, 23, 1.2, 1.2, DK) + ell(12, 23, 1.2, 1.2, DK)
SALON = [("station", "거울과 미용 의자", 30, 47, sa_station, True, "머리 하기"), ("shampoo", "샴푸대", 24, 34, sa_shampoo, True, "머리 감기"),
         ("pole", "이발소 기둥", 8, 30, sa_pole, True, None), ("waitsofa", "대기 소파", 40, 25, sa_sofa, True, "기다리기"),
         ("dryer", "후드 드라이어", 20, 33, sa_dryer, True, "말리기"), ("trolley", "미용 카트", 14, 24, sa_trolley, True, None)]

# ---- office (bank / civil service)
def of_teller():
    out = block(0, 14, 70, 10, 12, "#E9EEF2", "#C9D2DA")
    for i in range(3):
        x = 2 + i * 23
        out += rect(x, 0, 20, 15, "rgba(200,230,245,.5)", 1, OL, 0.4) + rect(x + 6, 11, 8, 3, "#FFFFFF", 0.4, OL, 0.3) + rect(x + 2, 1, 16, 4, "#3F6EA8", 0.6)
        out += f'<text x="{x+10}" y="4.2" font-family="Jua, sans-serif" font-size="3.2" fill="#FFFFFF" text-anchor="middle">{i+1}번 창구</text>'
    for i in range(4):
        out += rect(i * 23 - 0.6 if i else 0, 0, 1.6, 24, GR, 0.4)
    return out
def of_ticket():
    return (shadow(6, 26, 6, 1.2) + rect(1, 6, 10, 20, "#3F6EA8", 1.6, OL, 0.45) + rect(2.6, 8, 6.8, 5, "#DCEAF2", 0.6) + ell(6, 16, 2.4, 2.4, "#F2B84B", OL, 0.35)
            + rect(3.4, 20, 5.2, 1.4, DK, 0.4) + rect(4, 21, 4, 3, "#FFFFFF", 0.3, OL, 0.25) + f'<text x="6" y="11.6" font-family="Jua, sans-serif" font-size="3" fill="#3F6EA8" text-anchor="middle">번호표</text>')
def of_display(num=27):
    return (rect(0, 0, 30, 14, DK, 1.6, OL, 0.5) + rect(2, 2, 26, 10, "#1F1B22", 1) + f'<text x="9" y="9.8" font-family="Jua, sans-serif" font-size="7" fill="#F2B84B" text-anchor="middle">{num:03d}</text>'
            + f'<text x="22" y="9" font-family="Jua, sans-serif" font-size="3.2" fill="#6FCB8A" text-anchor="middle">→ 2번</text>')
def of_chairs():
    out = rect(0, 16, 44, 2, GR, 1)
    for i in range(4):
        out += block(i * 11, 4, 10, 8, 4, "#6F8FB5", "#5A7AA0", 2) + block(i * 11, 0, 10, 4, 5, "#5A7AA0", "#46638A", 1.6)
    return out
def of_atm():
    return (block(0, 0, 18, 8, 26, "#DDE1E5", "#B9C4CD", 1.4) + rect(3, 4, 12, 8, "#1F3B5C", 1) + rect(4, 5, 10, 6, "#8CC7EE", 0.6) + rect(5, 6, 6, 1, "#FFFFFF")
            + rect(3, 14, 12, 5, DK, 0.8) + "".join(rect(4 + (i % 4) * 2.6, 14.6 + (i // 4) * 1.6, 2, 1.2, "#B9C4CD", 0.3) for i in range(8)) + rect(4, 21, 10, 1.2, "#1F1B22", 0.5)
            + rect(0, -3, 18, 3.4, "#3F6EA8", 1, OL, 0.35) + f'<text x="9" y="-0.4" font-family="Jua, sans-serif" font-size="2.8" fill="#FFFFFF" text-anchor="middle">ATM</text>')
def of_info():
    return (path("M0,10 Q16,0 32,10 L32,20 Q16,12 0,20 Z", "#E9EEF2", OL, 0.5) + path("M0,10 Q16,0 32,10 L32,12 Q16,2 0,12 Z", "#3F6EA8") + screen(18, 0, 10, 7)
            + f'<text x="10" y="17" font-family="Jua, sans-serif" font-size="3.6" fill="#3F6EA8" text-anchor="middle">안내</text>' + ell(6, 8, 1.6, 1.6, "#F2B84B", OL, 0.3))
OFFICE = [("teller", "창구 카운터(3칸)", 70, 26, of_teller, True, "창구 업무"), ("ticketmachine", "번호표 기계", 12, 26, of_ticket, True, "번호표 뽑기"),
          ("numberboard", "번호 화면", 30, 14, lambda: of_display(27), False, None), ("waitchairs", "대기 의자", 44, 18, of_chairs, True, "기다리기"),
          ("atm", "ATM", 18, 34, of_atm, True, "돈 찾기"), ("infodesk", "안내 데스크", 32, 20, of_info, True, "안내 받기")]

# ---- stage / karaoke
def st_stage(light=0):
    out = block(0, 10, 90, 34, 6, "#5A4A70", "#463858", 2) + rect(2, 12, 86, 30, "#6A5884", 1.6)
    for i in range(10):
        out += line(4 + i * 9, 12, 4 + i * 9, 42, "rgba(0,0,0,.12)", 0.5)
    out += rect(0, 40, 90, 3, "#F2B84B", 0.6)
    cols = ["#F7D07A", "#F29A9A", "#8CC7EE"]
    for i, x in enumerate((20, 45, 70)):
        c = cols[(i + light) % 3]
        out += path(f"M{x},0 L{x-12},34 L{x+12},34 Z", c, None, 0, ' opacity="0.28"') + ell(x, 34, 12, 3.6, c, None, 0, ' opacity="0.35"')
        out += rect(x - 3, -4, 6, 5, DK, 1.6, OL, 0.4) + ell(x, 1, 2, 1, c)
    return out
def st_mic():
    return (shadow(4, 28, 4, 1) + path("M0,28 l4,-2 l4,2", "none", DK, 1) + line(4, 26, 4, 8, GR, 1) + line(4, 8, 8, 4, GR, 0.8)
            + ell(9, 3, 2, 2.4, "#5A5F66", OL, 0.4) + "".join(line(7.4, 2 + i, 10.6, 2 + i, "#8C9AA6", 0.3) for i in range(3)))
def st_speaker():
    return (block(0, 0, 16, 6, 22, "#2F2A2E", "#1F1B1F", 1.4) + ell(8, 12, 5, 5, "#3A3F45", OL, 0.4) + ell(8, 12, 2.2, 2.2, "#5A5F66") + ell(8, 22.6, 2.4, 2.4, "#3A3F45", OL, 0.3))
def st_karaoke():
    return (block(0, 22, 56, 14, 6, "#C95B7E", "#A84466", 3) + block(0, 16, 56, 6, 10, "#A84466", "#8A3554", 2)
            + rect(14, 0, 28, 16, OL, 1.4) + rect(15, 1, 26, 14, "#3D2F6A", 0.8) + rect(17, 9, 22, 1.4, "#F7D07A") + rect(17, 11.6, 16, 1.2, "#FFFFFF")
            + "".join(ell(19 + i * 6, 5, 1, 1, ["#F29A9A", "#8CC7EE", "#F7D07A", "#B7A1D9"][i]) for i in range(4))
            + ell(8, 27, 2.6, 1.2, "#F7D07A", OL, 0.3) + rect(46, 26, 6, 3, DK, 1))
def st_audience():
    out = ""
    for i in range(5):
        out += block(i * 12, 0, 10, 8, 5, "#8B5CD6", "#6E45B5", 2) + block(i * 12, 0, 10, 3, 7, "#6E45B5", "#57349A", 1.4)
    return out
STAGE = [("stage", "무대와 조명", 90, 50, lambda: st_stage(0), True, "노래하기"), ("mic", "마이크 스탠드", 12, 29, st_mic, True, None),
         ("speaker", "스피커", 16, 28, st_speaker, True, None), ("karaoke", "노래방 소파·화면", 56, 42, st_karaoke, True, "노래방"),
         ("audience", "객석 의자", 58, 13, st_audience, True, "공연 보기")]

POPFURN = {"clinic": CLINIC, "cinema": CINEMA, "library": LIBRARY, "market": MARKET, "salon": SALON, "office": OFFICE, "stage": STAGE}
FN = {b: {k: fn for k, l, w, h, fn, s, a in lst} for b, lst in POPFURN.items()}

# ================================================================ room layouts (224 base) + wall decor
def decor(b):
    if b == "clinic":
        return rug(150, 110, 40, 10, "#CFE7E2", "#B9DCD5") + window(20, 8, 34, 18, curtain="#CFE7E2") + rect(96, 6, 30, 16, "#FFFFFF", 1, OL, 0.45) + path("M108,8 h4 v4 h4 v4 h-4 v4 h-4 v-4 h-4 v-4 h4 z", RED) + rect(160, 8, 22, 14, "#DCEAF2", 1, OL, 0.4) + "".join(rect(163, 11 + i * 3, 16, 1, "#8CB8E0") for i in range(3))
    if b == "cinema":
        return g(ci_screen(0), 62, 2).replace("translate(62,2)", "translate(62,2)") + g(ci_poster("#6F8FB5"), 16, 6) + g(ci_poster("#C9564B"), 36, 6) + g(ci_poster("#8DB596"), 172, 6) + g(ci_poster("#B7A1D9"), 192, 6)
    if b == "library":
        return window(176, 8, 34, 18, curtain="#B9D7C1") + rect(94, 8, 34, 11, "#7A5A42", 1, OL, 0.4) + f'<text x="111" y="15.6" font-family="Jua, sans-serif" font-size="5.6" fill="#FFF4E0" text-anchor="middle">쉿! 조용히</text>' + rug(122, 120, 52, 12, "#B9D7C1", "#9DC0A8")
    if b == "market":
        return rug(110, 118, 60, 12, "#F7E1A0", "#F2C94C") + string_lights(4, 220, 3) + rect(80, 6, 64, 14, "#E8793A", 2, OL, 0.45) + f'<text x="112" y="16" font-family="Jua, sans-serif" font-size="8" fill="#FFFFFF" text-anchor="middle">오늘의 특가</text>'
    if b == "salon":
        return window(186, 8, 30, 18, curtain="#F3D1DA") + "".join(ell(14 + i * 8, 8, 2.4, 2.4, ["#F29A9A", "#F7D07A", "#B7A1D9"][i % 3], OL, 0.3) for i in range(5))
    if b == "office":
        return window(14, 8, 30, 18, curtain="#D3DFEB") + g(of_display(27), 150, 4) + rect(186, 6, 26, 16, "#FFFFFF", 1, OL, 0.4) + "".join(rect(189, 9 + i * 3, 20, 1, "#B9C4CD") for i in range(4))
    if b == "stage":
        return string_lights(4, 220, 3, ("#F7D07A", "#F29A9A", "#8CC7EE", "#B7A1D9")) + "".join(ell(30 + i * 40, 18, 6, 6, "#FFFFFF", None, 0, ' opacity="0.08"') for i in range(5))
    return ""

ROOMS = {
    "clinic":  [("medshelf", 182, 4), ("reception", 10, 40), ("waiting", 12, 100), ("consultdesk", 124, 44), ("curtain", 168, 50), ("exambed", 170, 58), ("scale", 66, 44), ("ivstand", 212, 72)],
    "cinema":  [("seatrow", 64, 52), ("seatrow", 64, 76), ("seatrow", 64, 100), ("aisle", 46, 44), ("ticket", 8, 96), ("popcorn", 196, 92), ("popcorn", 172, 92)],
    "library": [("tallshelf", 6, 4), ("tallshelf", 48, 4), ("magazine", 132, 8), ("readdesk", 70, 64), ("readdesk", 130, 64), ("loandesk", 10, 102), ("beanbag", 190, 100), ("globe", 200, 58)],
    "market":  [("drinkfridge", 6, 4), ("snackshelf", 166, 4), ("produce", 60, 46), ("produce", 120, 46), ("checkout", 150, 102), ("cart", 20, 104), ("baskets", 108, 110)],
    "salon":   [("station", 10, 2), ("station", 46, 2), ("station", 82, 2), ("shampoo", 130, 40), ("waitsofa", 20, 106), ("dryer", 168, 48), ("trolley", 120, 96), ("dryer", 196, 48)],
    "office":  [("teller", 70, 30), ("ticketmachine", 14, 64), ("waitchairs", 70, 96), ("waitchairs", 124, 96), ("atm", 196, 46), ("infodesk", 12, 104)],
    "stage":   [("stage", 66, 18), ("mic", 106, 34), ("speaker", 62, 30), ("speaker", 148, 30), ("karaoke", 6, 74), ("audience", 82, 104), ("audience", 148, 104)],
}
SPOTS = {  # where the character goes (224-base coords, feet), pose, facing
    "clinic":  dict(x=136, y=78, pose="sit", dir="right", note="진료 의자(진료 책상 앞)"),
    "cinema":  dict(x=108, y=66, pose="sit", dir="up", note="두 번째 줄 가운데 좌석, 뒷모습으로 스크린 보기"),
    "library": dict(x=92, y=72, pose="read", dir="down", note="첫 열람 책상 의자"),
    "market":  dict(x=86, y=82, pose="idle", dir="up", note="과일 진열대 앞 → 이후 계산대 앞(174,98)"),
    "salon":   dict(x=61, y=44, pose="sit", dir="up", note="가운데 미용 의자, 거울을 봄"),
    "office":  dict(x=115, y=62, pose="idle", dir="up", note="2번 창구 앞"),
    "stage":   dict(x=112, y=54, pose="talk", dir="down", note="무대 가운데 마이크 앞"),
}

def place(b, items):
    return "".join(g(FN[b][k](), x, y) for k, x, y in sorted(items, key=lambda z: z[2]))

def exterior_sign(b, bw):
    """sign board standing on the back wall top (local building coords)"""
    c = POPUP[b]["sign"]; lbl = POPUP[b]["label"]
    w = 18 + len(lbl) * 9
    x = bw / 2 - w / 2
    out = rect(x + 4, -12, 1.6, 8, "#5A5F66") + rect(x + w - 5.6, -12, 1.6, 8, "#5A5F66")
    out += rect(x, -26, w, 15, c, 4, OL, 0.6) + rect(x + 1.6, -24.6, w - 3.2, 2, "rgba(255,255,255,.3)", 1)
    icon = {
        "clinic": rect(x + 5, -22, 8, 8, "#FFFFFF", 1.4) + path(f"M{x+7.8},-21 h2.4 v2.4 h2.4 v2.4 h-2.4 v2.4 h-2.4 v-2.4 h-2.4 v-2.4 h2.4 z", RED),
        "cinema": rect(x + 5, -22, 9, 7, "#1F1B22", 1) + "".join(ell(x + 6.4 + i * 3, -15.6, 0.7, 0.7, "#F7D07A") for i in range(3)) + path(f"M{x+8},-20.4 l3,1.6 l-3,1.6 z", "#FFFFFF"),
        "library": path(f"M{x+5},-21 q3,-1.4 4.5,0 q1.5,-1.4 4.5,0 l0,6 q-3,-1.4 -4.5,0 q-1.5,-1.4 -4.5,0 z", "#FFF4E0", OL, 0.4),
        "market": path(f"M{x+5},-21 l9,0 l-1.4,6 l-6.2,0 z", "#FFFFFF", OL, 0.4) + path(f"M{x+7},-21 q2.5,-4 5,0", "none", "#FFFFFF", 0.8),
        "salon": path(f"M{x+6},-21 l7,6 M{x+6},-15 l7,-6", "none", "#FFFFFF", 0.9) + ell(x + 6, -21, 1.4, 1.4, "none", "#FFFFFF", 0.7) + ell(x + 6, -15, 1.4, 1.4, "none", "#FFFFFF", 0.7),
        "office": path(f"M{x+5},-17 l4.5,-4 l4.5,4 z M{x+6},-17 v4 M{x+9.5},-17 v4 M{x+13},-17 v4 M{x+5},-13 h9", "#FFFFFF", "#FFFFFF", 0.6),
        "stage": path(f"M{x+9.5},-22 a2.4,2.4 0 0 1 2.4,2.4 v2 a2.4,2.4 0 0 1 -4.8,0 v-2 a2.4,2.4 0 0 1 2.4,-2.4 z M{x+9.5},-15 v2.4", "#FFFFFF", "#FFFFFF", 0.6),
    }[b]
    out += icon + f'<text x="{f(x+w/2+6)}" y="-15.6" font-family="Jua, sans-serif" font-size="8" fill="#FFFFFF" text-anchor="middle">{lbl}</text>'
    if b == "cinema":
        out += "".join(ell(x + 3 + i * (w - 6) / 9, -26, 0.9, 0.9, "#F7D07A", OL, 0.2) for i in range(10)) + "".join(ell(x + 3 + i * (w - 6) / 9, -11, 0.9, 0.9, "#F7D07A", OL, 0.2) for i in range(10))
    if b == "stage":
        out += "".join(ell(x + 3 + i * (w - 6) / 9, -26, 0.9, 0.9, ["#F29A9A", "#8CC7EE", "#F7D07A"][i % 3], OL, 0.2) for i in range(10))
    return out

def entrance(b, bw, bh):
    """decoration outside the front door (below bh)"""
    d = bw / 2
    if b == "clinic":
        return g(path("M0,0 l3,-14 h4 l3,14 z", "#FFFFFF", OL, 0.45) + rect(2.4, -11, 5, 5, RED, 0.6), d + 20, bh + 16) + plant(d - 24, bh + 14)
    if b == "cinema":
        return g(rect(-2, -22, 20, 20, "#1F1B22", 1.4, OL, 0.45) + rect(0, -20, 16, 16, "#6F8FB5", 0.6) + ell(8, -12, 4, 4, "#FFF4E0") + rect(-1, -2, 18, 2, "#5A5F66", 0.6), d + 18, bh + 18) + g(rect(0, -10, 1.2, 10, "#E9C46A") + rect(14, -10, 1.2, 10, "#E9C46A") + path("M0,-9 q7.6,4 15,0", "none", RED, 1), d - 34, bh + 16)
    if b == "library":
        return g(block(0, -12, 20, 6, 8, "#7A5A42", "#5A4033", 2) + rect(4, -14, 12, 3, "#E8B64C", 0.6, OL, 0.3) + f'<text x="10" y="-3" font-family="Jua, sans-serif" font-size="3.4" fill="#FFF4E0" text-anchor="middle">반납함</text>', d + 18, bh + 16) + plant(d - 22, bh + 14)
    if b == "market":
        return g(FN["market"]["baskets"](), d + 16, bh + 2) + g(FN["market"]["cart"](), d - 40, bh + 2) + g(block(0, -8, 22, 8, 6, "#C9A076", "#A9805A", 1) + "".join(ell(4 + i * 5, -6, 2, 1.6, ["#E06A52", "#F2B84B", "#8DB596", "#F7D07A"][i], OL, 0.25) for i in range(4)), d + 36, bh + 14)
    if b == "salon":
        return g(sa_pole(), d + 16, bh - 16) + g(path("M0,0 L5,-14 L10,0 Z", "#7A5238", OL, 0.45) + path("M1.6,-1.6 L5,-12 L8.4,-1.6 Z", "#FBE4EA") + rect(3, -8, 4, 0.6, "#C95B7E"), d - 30, bh + 15)
    if b == "office":
        return g(rect(0, -24, 1, 24, GR) + path("M1,-24 l10,2 l-10,2 z", "#3F6EA8", OL, 0.3) + rect(14, -24, 1, 24, GR) + path("M15,-24 l10,2 l-10,2 z", RED, OL, 0.3), d + 18, bh + 16) + plant(d - 22, bh + 14)
    if b == "stage":
        return g(rect(0, -20, 16, 20, "#2F2A45", 1, OL, 0.45) + rect(2, -18, 12, 12, "#8B5CD6", 0.6) + f'<text x="8" y="-10.6" font-family="Jua, sans-serif" font-size="4" fill="#FFFFFF" text-anchor="middle">LIVE</text>' + rect(2, -4, 12, 2, "#F7D07A", 0.4), d + 20, bh + 18) + g(path("M0,0 q-3,-8 0,-14 q3,6 0,14", "#F29A9A", OL, 0.35) + path("M6,0 q-3,-8 0,-16 q3,8 0,16", "#8CC7EE", OL, 0.35), d - 30, bh + 14)
    return ""

def popup_building(b, size="m", uid="p", avatars="", sign=True):
    bw, bh = BSIZES[size]
    cx = (bw - 224) / 2
    interior = g(decor(b) + place(b, ROOMS[b]), cx, 0)
    out = building(b, size, "pp_" + b, POPUP[b]["floor"], uid + b + size, avatars=avatars, interior=interior)
    if sign:
        out += exterior_sign(b, bw)
    out += entrance(b, bw, bh)
    return out

# ================================================================ appear / disappear & truck
def fence(bw, bh, prog=1.0, label="곧 문을 열어요"):
    """construction hoarding around the plot (local coords of the building box)"""
    out = rect(-8, -8, bw + 16, bh + 18, "rgba(60,40,20,.08)", 4)
    h = 22 * prog
    for x in range(-8, int(bw) + 8, 12):
        out += rect(x, bh + 10 - h, 11.4, h, "#F2B84B" if (x // 12) % 2 == 0 else "#FFFFFF", 0.6, OL, 0.4)
        out += path(f"M{x},{bh+10-h+4} l11.4,6", "none", "#3A3F45", 1) if prog > 0.5 else ""
    out += rect(bw / 2 - 30, bh - 10, 60, 14, "#3A3F45", 3, OL, 0.5) + f'<text x="{bw/2}" y="{bh-0.6}" font-family="Jua, sans-serif" font-size="7" fill="#F2B84B" text-anchor="middle">{label}</text>'
    out += g(block(0, -18, 26, 10, 10, "#F2B84B", "#D9A23E", 2) + rect(4, -24, 3, 8, "#3A3F45"), 20, 60) + g(art.rect(0, -3, 34, 3, "#C9A076", 0.5, OL, 0.3) * 1, 120, 70)
    for x, y in ((60, 40), (180, 80), (220, 30)):
        out += g(path("M-2.8,-1.4 L0,-10 L2.8,-1.4 Z", "#F29A4F", OL, 0.4) + rect(-4, -1.4, 8, 1.4, "#E06A52", 0.4), x, y)
    return out

def pop_cloud(bw, bh, s=1.0):
    out = ""
    for i in range(14):
        a = i / 14 * math.tau
        r = (bw / 2 + 10) * s
        x, y = bw / 2 + math.cos(a) * r, bh / 2 + math.sin(a) * r * 0.55
        out += ell(x, y, 16 * s, 12 * s, "#FFFFFF", OL, 0.5)
    for i in range(14):
        a = i / 14 * math.tau
        r = (bw / 2 + 10) * s
        out += ell(bw / 2 + math.cos(a) * r, bh / 2 + math.sin(a) * r * 0.55, 14 * s, 10 * s, "#FFFFFF")
    out += f'<text x="{bw/2}" y="{bh/2+8}" font-family="Jua, sans-serif" font-size="{24*s:.1f}" fill="#F2B84B" stroke="#3A2E2A" stroke-width="0.8" text-anchor="middle">뿅!</text>'
    return out

def balloons(x, y, cols=("#F29A9A", "#F7D07A", "#8CC7EE")):
    out = ""
    for i, c in enumerate(cols):
        bx, by = x + (i - 1) * 6, y - 26 - (i % 2) * 4
        out += path(f"M{x},{y} Q{bx-1},{by+12} {bx},{by+6}", "none", "#7A6E62", 0.4) + ell(bx, by, 4, 5, c, OL, 0.45) + ell(bx - 1.4, by - 2, 1, 1.4, "rgba(255,255,255,.6)") + path(f"M{bx-0.8},{by+5} l0.8,1.2 l0.8,-1.2 z", c)
    return out

def ribbon(bw, bh):
    d = bw / 2
    return (path(f"M{d-26},{bh+8} Q{d},{bh+14} {d+26},{bh+8}", "none", RED, 1.6) + path(f"M{d},{bh+11} l-5,-4 l0,8 z M{d},{bh+11} l5,-4 l0,8 z", RED, OL, 0.35)
            + balloons(-4, bh + 4) + balloons(bw + 4, bh + 4, ("#B7A1D9", "#8DB596", "#F29A9A"))
            + "".join(rect(10 + (i * 37) % (bw - 20), 30 + (i * 23) % 100, 2, 3, ["#F29A9A", "#F7D07A", "#8CC7EE", "#8DB596"][i % 4], 0.4, None, 0, f' transform="rotate({i*31} {10+(i*37)%(bw-20)} {30+(i*23)%100})"') for i in range(16)))

def folding(bw, bh, prog=0.5):
    """building squashing down (scaleY) toward its baseline"""
    return prog

def truck(kind="cinema"):
    c = POPUP[kind]["sign"]; lbl = POPUP[kind]["label"]
    out = ell(0, 1, 46, 4, "rgba(40,40,40,.18)")
    out += rect(-44, -40, 64, 36, "#FFFDF6", 3, OL, 0.6) + rect(-44, -40, 64, 6, c, 3, OL, 0.6)
    out += rect(-40, -32, 56, 18, shade(c, 0.8), 1.4, OL, 0.4)
    # opened side hatch (awning)
    out += path("M-46,-34 L22,-34 L28,-46 L-40,-46 Z", c, OL, 0.6) + "".join(path(f"M{-40+i*8.5},-46 l8.5,0 l-1.2,12 l-8.5,0 z", "#FFFFFF" if i % 2 else c, OL, 0.25) for i in range(8))
    out += path("M-46,-34 " + " ".join(f"q{4.25},4 8.5,0" for _ in range(8)), shade(c, 0.2), OL, 0.4)
    out += f'<text x="-12" y="-19" font-family="Jua, sans-serif" font-size="9" fill="{shade(c,-0.2)}" text-anchor="middle">{lbl}</text>'
    out += rect(-42, -14, 60, 8, "#E2C29A", 1, OL, 0.4)
    out += path("M20,-4 L20,-30 L32,-30 L42,-16 L42,-4 Z", c, OL, 0.6) + path("M23,-27 L31,-27 L38,-17 L23,-17 Z", "#BFE3F2", OL, 0.35)
    for wx in (-30, 6, 32):
        out += ell(wx, -3, 6, 6, "#3A3F45", OL, 0.5) + ell(wx, -3, 2.6, 2.6, "#B9C4CD")
    out += ell(41, -10, 1.6, 1.4, "#FFF3B8", OL, 0.3)
    return out
