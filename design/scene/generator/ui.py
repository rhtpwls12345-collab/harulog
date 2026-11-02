"""Bubble / tag CSS and the scene-section + pet-card UI markup (shared by the canvas boards and the ui/*.html deliverables)."""
from pets import pet, furvars, VIEWBOX, FURS, BREEDS

TOKENS = """
:root{--ink:#3B3128;--muted:#7A6E62;--line:#EADFCF;--bg:#FBF6EE;--surface:#FFFDF8;--surface-2:#F6EFE4;--sage:#5E9576;--sage-soft:#E6F0E6;--brown:#8A5A3C}
"""

BUBBLE_CSS = """
/* ===== 하루로그 말풍선 · 이름표 (bubble.css) ===== */
.tag{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:999px;background:rgba(59,49,40,.78);color:#fff;font:600 12px/1.5 'Gowun Dodum',system-ui,sans-serif;white-space:nowrap;box-shadow:0 1px 0 rgba(0,0,0,.12)}
.tag.pet{background:var(--brown,#8A5A3C);padding-left:6px}
.tag.pet::before{content:"";width:11px;height:11px;flex:none;background:no-repeat center/contain url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cg fill='%23FFE7C7'%3E%3Cellipse cx='6' cy='8.2' rx='2.6' ry='2.1'/%3E%3Ccircle cx='2.4' cy='5' r='1.2'/%3E%3Ccircle cx='4.6' cy='3' r='1.2'/%3E%3Ccircle cx='7.4' cy='3' r='1.2'/%3E%3Ccircle cx='9.6' cy='5' r='1.2'/%3E%3C/g%3E%3C/svg%3E")}
.tag.say{position:relative;max-width:240px;white-space:normal;padding:6px 11px;border-radius:14px;background:#FFFDF6;color:var(--ink,#3B3128);border:1.5px solid #3B3128;font:500 13px/1.4 'Gowun Dodum',system-ui,sans-serif;box-shadow:0 2px 0 rgba(59,49,40,.18);transform-origin:50% calc(100% + 7px);animation:say-pop .42s cubic-bezier(.2,1.4,.4,1) both}
.tag.say::after{content:"";position:absolute;left:50%;bottom:-6px;width:9px;height:9px;margin-left:-5px;background:inherit;border-right:1.5px solid #3B3128;border-bottom:1.5px solid #3B3128;transform:rotate(45deg);border-bottom-right-radius:2px}
.tag.say .mood{display:inline-block;width:14px;height:14px;vertical-align:-2px;margin-right:4px}
.tag.say.happy{background:#FFF4D6;border-color:#C9962E}.tag.say.happy::after{border-color:#C9962E}
.tag.say.tired{background:#EEF1F6;border-color:#7D8899;color:#4F5866;animation:say-pop .5s ease-out both,say-sway 2.4s ease-in-out .5s infinite}.tag.say.tired::after{border-color:#7D8899}
.tag.say.excited{background:#FFE6EA;border-color:#D9536F;animation:say-pop .42s cubic-bezier(.2,1.4,.4,1) both,say-wiggle .9s ease-in-out .42s 2}.tag.say.excited::after{border-color:#D9536F}
.tag.say.food{background:#FFF1E4;border-color:#C9734E}.tag.say.food::after{border-color:#C9734E}
@keyframes say-pop{0%{opacity:0;transform:translateY(6px) scale(.4)}60%{opacity:1;transform:translateY(-2px) scale(1.08)}100%{opacity:1;transform:none}}
@keyframes say-wiggle{0%,100%{transform:rotate(0)}25%{transform:rotate(-3deg)}75%{transform:rotate(3deg)}}
@keyframes say-sway{0%,100%{transform:translateY(0)}50%{transform:translateY(2px)}}
@media (prefers-reduced-motion:reduce){.tag.say{animation:none!important}}
"""

MOOD_ICON = {
    "happy": '<svg class="mood" viewBox="0 0 14 14" aria-hidden="true"><circle cx="7" cy="7" r="6" fill="#F2B84B"></circle><path d="M4.4 8.2q2.6 2.6 5.2 0" fill="none" stroke="#3B3128" stroke-width="1.2" stroke-linecap="round"></path><circle cx="5" cy="5.6" r=".8" fill="#3B3128"></circle><circle cx="9" cy="5.6" r=".8" fill="#3B3128"></circle></svg>',
    "tired": '<svg class="mood" viewBox="0 0 14 14" aria-hidden="true"><circle cx="7" cy="7" r="6" fill="#B9C4CD"></circle><path d="M4 6h2M8 6h2M5.4 9.4h3.2" stroke="#3B3128" stroke-width="1.2" stroke-linecap="round"></path></svg>',
    "excited": '<svg class="mood" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 1l1.6 3.6L12.4 5 9.6 7.6l.8 3.9L7 9.6l-3.4 1.9.8-3.9L1.6 5l3.8-.4z" fill="#F27A93" stroke="#3B3128" stroke-width=".8" stroke-linejoin="round"></path></svg>',
    "food": '<svg class="mood" viewBox="0 0 14 14" aria-hidden="true"><ellipse cx="7" cy="9" rx="6" ry="3" fill="#FFFFFF" stroke="#3B3128" stroke-width=".9"></ellipse><ellipse cx="7" cy="8.4" rx="3.4" ry="1.4" fill="#E99A6E"></ellipse><path d="M5 4.6q0-1.6 1-2.6M8 4.6q0-1.6 1-2.6" fill="none" stroke="#B9C4CD" stroke-width=".8" stroke-linecap="round"></path></svg>',
}

UI_CSS = """
/* ===== 장면 칸 · 반려동물 카드 (scene-section / pet-card) ===== */
.scene-box{border:1.5px dashed var(--line,#EADFCF);border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:12px;background:var(--surface,#FFFDF8)}
.scene-box h4{margin:0;font:400 16px/1.3 Jua,sans-serif;color:var(--ink,#3B3128);display:flex;align-items:center;gap:8px}
.scene-box h4 small{font:400 12px 'Gowun Dodum',sans-serif;color:var(--muted,#7A6E62)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-flex;align-items:center;gap:6px;min-height:40px;padding:6px 12px 6px 8px;border-radius:999px;border:1px solid var(--line,#EADFCF);background:var(--surface,#FFFDF8);color:var(--ink,#3B3128);font:14px 'Gowun Dodum',sans-serif;cursor:pointer}
.chip[aria-pressed="true"]{background:var(--sage,#5E9576);border-color:var(--sage,#5E9576);color:#fff}
.chip .ic{width:24px;height:24px;flex:none;border-radius:50%;display:grid;place-items:center;background:#F3EEE4}
.chip[aria-pressed="true"] .ic{background:rgba(255,255,255,.22)}
.chip.auto{border-style:dashed}
.chip.auto b{font-weight:700}
.motion-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:6px}.motion-grid .chip.auto{grid-column:span 2}
.motion-grid .chip{justify-content:flex-start}
.pet-chip .ic{width:30px;height:24px;border-radius:8px;background:#EEF4E8}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:40px;padding:8px 16px;border-radius:999px;border:1px solid var(--line,#EADFCF);background:var(--surface,#FFFDF8);color:var(--ink,#3B3128);font:14px 'Gowun Dodum',sans-serif;cursor:pointer}
.btn.sm{min-height:36px;padding:6px 12px;font-size:13px}
.btn.primary{background:var(--sage,#5E9576);border-color:var(--sage,#5E9576);color:#fff}
.btn.danger{color:#B4533F;border-color:#E8B4A8}
.pet-card{background:var(--surface,#FFFDF8);border:1px solid var(--line,#EADFCF);border-radius:20px;padding:18px;display:flex;flex-direction:column;gap:14px}
.pet-card h3{margin:0;font:400 20px Jua,sans-serif;color:var(--ink,#3B3128)}
.pet-card .hint{margin:0;font-size:13px;color:var(--muted,#7A6E62)}
.pet-row{display:flex;align-items:center;gap:12px;padding:10px 12px;border:1px solid var(--line,#EADFCF);border-radius:16px;background:#fff}
.pet-row .thumb{width:58px;height:46px;flex:none;border-radius:12px;background:#EEF4E8;display:grid;place-items:center}
.pet-row .who{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.pet-row .who b{font:400 17px Jua,sans-serif}
.pet-row .who span{font-size:12px;color:var(--muted,#7A6E62)}
.pet-form{border-top:1px solid var(--line,#EADFCF);padding-top:14px;display:grid;grid-template-columns:120px 1fr;gap:14px;align-items:start}
.pet-form .preview{grid-row:span 5;height:120px;border-radius:16px;background:#EEF4E8;display:grid;place-items:center}
.field{display:flex;flex-direction:column;gap:6px;min-width:0}
.field>label,.field>span{font-size:13px;color:var(--muted,#7A6E62)}
.input{min-height:42px;border:1px solid var(--line,#EADFCF);border-radius:12px;padding:8px 12px;font:15px 'Gowun Dodum',sans-serif;background:#fff;color:var(--ink,#3B3128)}
.seg{display:flex;gap:4px;padding:4px;border-radius:999px;background:#F3EEE4}
.seg button{flex:1;min-height:36px;border:0;border-radius:999px;background:transparent;font:14px 'Gowun Dodum',sans-serif;color:var(--ink,#3B3128);cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--sage,#5E9576);color:#fff}
.swatches{display:flex;gap:10px;flex-wrap:wrap}
.swatch{width:36px;height:36px;border-radius:50%;border:3px solid #fff;box-shadow:0 0 0 1px var(--line,#EADFCF);cursor:pointer}
.swatch[aria-pressed="true"]{box-shadow:0 0 0 2.5px var(--ink,#3B3128)}
.empty{display:flex;flex-direction:column;align-items:center;gap:6px;padding:18px;border-radius:16px;background:#F6EFE4;text-align:center}
.empty b{font:400 17px Jua,sans-serif}
.empty span{font-size:13px;color:var(--muted,#7A6E62)}
@media (max-width:480px){.pet-form{grid-template-columns:1fr}.pet-form .preview{grid-row:auto;height:110px}.motion-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
"""

def pet_svg(kind, breed, pose, fur, w=58, h=42, gear="collar"):
    body, _ = pet(kind, breed, pose, 0)
    if gear == "harness":
        body = body.replace('class="gear-harness" style="display:none"', 'class="gear-harness"').replace('<g class="gear-collar">', '<g class="gear-collar" style="display:none">')
    return f'<svg viewBox="{VIEWBOX}" width="{w}" height="{h}" aria-hidden="true" style="{furvars(fur)}">{body}</svg>'

ICON = {  # 24px action icons
    "auto": '<path d="M12 3l1.8 4.6L18.6 9l-4.8 1.4L12 15l-1.8-4.6L5.4 9l4.8-1.4z" fill="#F2B84B" stroke="#3B3128" stroke-width="1" stroke-linejoin="round"></path><circle cx="18" cy="17" r="1.6" fill="#F2B84B"></circle>',
    "strength": '<rect x="3" y="10" width="18" height="2.4" rx="1.2" fill="#9AA6B0"></rect><rect x="4" y="6.6" width="3" height="9.2" rx="1.2" fill="#E06A52" stroke="#3B3128" stroke-width=".8"></rect><rect x="17" y="6.6" width="3" height="9.2" rx="1.2" fill="#E06A52" stroke="#3B3128" stroke-width=".8"></rect>',
    "run": '<path d="M4 17c3-1 5-4 8-4s3 4 8 3" fill="none" stroke="#5E9576" stroke-width="2" stroke-linecap="round"></path><path d="M6 11h4M4 8h5" stroke="#9AA6B0" stroke-width="1.6" stroke-linecap="round"></path><ellipse cx="16" cy="9" rx="3.4" ry="2.4" fill="#F7D07A" stroke="#3B3128" stroke-width=".9"></ellipse>',
    "swim": '<circle cx="12" cy="9" r="3.4" fill="#E06A52" stroke="#3B3128" stroke-width=".9"></circle><path d="M3 15q2.25-2 4.5 0t4.5 0 4.5 0 4.5 0M3 19q2.25-2 4.5 0t4.5 0 4.5 0 4.5 0" fill="none" stroke="#4FA3CF" stroke-width="1.8" stroke-linecap="round"></path>',
    "yoga": '<rect x="3" y="16" width="18" height="3.4" rx="1.7" fill="#B7A1D9" stroke="#3B3128" stroke-width=".8"></rect><circle cx="12" cy="6.6" r="2.6" fill="#F5C9A0" stroke="#3B3128" stroke-width=".8"></circle><path d="M6 15q6-6 12 0" fill="none" stroke="#3B3128" stroke-width="1.6" stroke-linecap="round"></path>',
    "bike": '<circle cx="7" cy="15" r="4" fill="none" stroke="#3B3128" stroke-width="1.6"></circle><circle cx="17" cy="15" r="4" fill="none" stroke="#3B3128" stroke-width="1.6"></circle><path d="M7 15l4-6h5l1 6M11 9l-1-2h-2" fill="none" stroke="#5E9576" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>',
    "boxing": '<path d="M7 8q0-4 5-4h2q5 0 5 5v4q0 3-3 3H10q-3 0-3-3z" fill="#E06A52" stroke="#3B3128" stroke-width="1" stroke-linejoin="round"></path><rect x="8" y="16" width="9" height="4" rx="1" fill="#FFFFFF" stroke="#3B3128" stroke-width=".9"></rect>',
    "meeting": '<rect x="3" y="4" width="13" height="9" rx="2" fill="#FFFFFF" stroke="#3B3128" stroke-width="1"></rect><path d="M6 8h7M6 10.4h4" stroke="#6F8FB5" stroke-width="1.4" stroke-linecap="round"></path><path d="M12 15h6a2 2 0 0 1 2 2v1l-2 2v-2h-6z" fill="#F7D07A" stroke="#3B3128" stroke-width=".9" stroke-linejoin="round"></path>',
    "none": '<circle cx="12" cy="7.6" r="3" fill="#F5C9A0" stroke="#3B3128" stroke-width=".8"></circle><path d="M7 20q0-8 5-8t5 8" fill="#8CB8E0" stroke="#3B3128" stroke-width=".9"></path>',
}

def ic(k, s=18):
    return f'<span class="ic"><svg width="{s}" height="{s}" viewBox="0 0 24 24" aria-hidden="true">{ICON[k]}</svg></span>'

MOTIONS = [("strength", "근력 운동"), ("run", "달리기"), ("swim", "수영"), ("yoga", "요가"), ("bike", "사이클"), ("boxing", "복싱"), ("meeting", "회의·발표"), ("none", "기본 동작")]

def scene_section(selected="auto", auto_label="근력 운동", pets=(("콩이", "dog", "shiba", "#C98B5A", True), ("나비", "cat", "tuxedo", "#3A2E2A", False))):
    chips = f'<button type="button" class="chip auto" aria-pressed="{str(selected=="auto").lower()}">{ic("auto")}<span>자동: <b>{auto_label}</b></span></button>'
    chips += "".join(f'<button type="button" class="chip" aria-pressed="{str(selected==k).lower()}">{ic(k)}{lbl}</button>' for k, lbl in MOTIONS)
    pchips = "".join(f'<button type="button" class="chip pet-chip" aria-pressed="{str(on).lower()}"><span class="ic">{pet_svg(kind, br, "sit", fur, 30, 24)}</span>{name}</button>' for name, kind, br, fur, on in pets)
    return f'''<div class="scene-box" role="group" aria-label="장면">
<h4>장면 <small>기록에 맞춰 마을에서 재생돼요</small></h4>
<div class="field"><span>동작</span><div class="motion-grid" role="group" aria-label="동작">{chips}</div></div>
<div class="field"><span>함께 간 반려동물</span><div class="chips" role="group" aria-label="함께 간 반려동물">{pchips}</div></div>
</div>'''

def _pet_card(show_form=True, pets=(("콩이", "dog", "shiba", "#C98B5A", "목줄"), ("나비", "cat", "tuxedo", "#3A2E2A", "하네스")), form_kind="dog", form_breed="poodle", form_fur="#E8C79A", empty=False):
    br_label = {**{k: v for k, v in BREEDS["dog"]}, **{"cheese": "치즈 태비", "tuxedo": "턱시도", "calico": "삼색"}}
    if empty:
        rows = f'''<div class="empty"><div style="display:flex;align-items:flex-end;gap:4px">{pet_svg("dog", "mix", "lie", "#E8C79A", 120, 86)}{pet_svg("cat", "calico", "lie", "#F2EDE4", 110, 80)}</div>
<b>아직 함께 사는 친구가 없어요</b><span>강아지나 고양이를 등록하면 산책 기록에 같이 나와요</span></div>'''
    else:
        rows = "".join(f'''<div class="pet-row"><span class="thumb">{pet_svg(kind, br, "sit", fur, 54, 40)}</span><span class="who"><b>{name}</b><span>{"강아지" if kind=="dog" else "고양이"} · {br_label.get(br, "기본")} · {gear}</span></span><button type="button" class="btn sm">수정</button><button type="button" class="btn sm danger">삭제</button></div>''' for name, kind, br, fur, gear in pets)
    breeds = "".join(f'<button type="button" class="chip" aria-pressed="{str(k==form_breed).lower()}" style="padding:6px 12px">{lbl}</button>' for k, lbl in BREEDS[form_kind])
    sw = "".join(f'<button type="button" class="swatch" aria-label="털 색 {c}" aria-pressed="{str(c==form_fur).lower()}" style="background:{c}"></button>' for c in FURS)
    return f'''<section class="pet-card" aria-labelledby="petTitle">
<div style="display:flex;align-items:baseline;gap:8px"><h3 id="petTitle">반려동물</h3><span class="hint">{len(pets) if not empty else 0} / 3마리</span></div>
<p class="hint">이름이나 ‘산책’, ‘강아지’ 같은 말이 기록에 들어가면 마을에서 함께 다녀요.</p>
{rows}
{'<div class="pet-form">' if show_form else '<!--'}
<div class="preview" aria-hidden="true">{pet_svg(form_kind, form_breed, "sit", form_fur, 120, 92)}</div>
<div class="field"><label for="petName">이름</label><input id="petName" class="input" maxlength="10" placeholder="예: 콩이" value="몽실"></div>
<div class="field"><span>종류</span><div class="seg" role="group" aria-label="종류"><button type="button" aria-pressed="{str(form_kind=="dog").lower()}">강아지</button><button type="button" aria-pressed="{str(form_kind=="cat").lower()}">고양이</button></div></div>
<div class="field"><span>모습</span><div class="chips" role="group" aria-label="모습">{breeds}</div></div>
<div class="field"><span>털 색</span><div class="swatches" role="group" aria-label="털 색">{sw}</div></div>
<div class="field"><span>산책 장비</span><div class="chips" role="group" aria-label="산책 장비"><button type="button" class="chip" aria-pressed="true" style="padding:6px 12px">목줄</button><button type="button" class="chip" aria-pressed="false" style="padding:6px 12px">하네스</button><span style="flex:1"></span><button type="button" class="btn primary">추가</button></div></div>
{'</div>' if show_form else '-->'}
</section>'''


def pet_card(*a, **k):
    import re
    return re.sub(r"<!--.*?-->", "", _pet_card(*a, **k), flags=re.S)
