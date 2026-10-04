import json, os, sys, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
sys.path.insert(0, '.'); import script

REPO = '/home/user/jianying_project_eye2eye'
OUT = 'out'; os.makedirs(f'{OUT}/slides', exist_ok=True); os.makedirs(f'{OUT}/frames', exist_ok=True)
W, H = 1920, 1080
BG, INK, MUTED = (250, 248, 244), (28, 28, 30), (110, 110, 118)
ORANGE, BLUE, GREEN = (227, 155, 45), (59, 123, 224), (58, 174, 132)
FI = 'fonts/inter/extras/ttf/'
def F(w, s): return ImageFont.truetype(FI + f'Inter-{w}.ttf', s)
def ZH(s, bold=False): return ImageFont.truetype('fonts/NotoSansSC-' + ('Bold' if bold else 'Regular') + '.otf', s)

THUMB = {
    'shelf': '8fdebbe70b23804adc677805e6e0266b_6766667-sdr709.png',
    'shelf2': '38c143f19b6126fbc393f39ff5af2839_2466666-sdrp3.jpg',
    'avp': '5d2ceb16ff2ee5a7a01e08437b642035_1300000-sdr709.jpg',
    'ocean': '0a3bd3df20490d03974ae9b8831081ae_7533334-sdr709.jpg',
    'ocean2': '0a3bd3df20490d03974ae9b8831081ae_12666666-sdr709.png',
    'pip_ux': 'subdraft/8220B51E-9E28-4182-934E-65A122A1759D/draft_cover.jpg',
}

def cover(img, w=W, h=H):
    r = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))

def fit(img, box):
    x0, y0, x1, y1 = box
    r = min((x1 - x0) / img.width, (y1 - y0) / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    return img, (x0 + (x1 - x0 - img.width) // 2, y0 + (y1 - y0 - img.height) // 2)

def wrap(d, text, font, maxw):
    lines, cur = [], ''
    for w in text.split(' '):
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def base(section=None, title=None):
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    if section:
        d.text((120, 92), section.upper(), font=F('SemiBold', 26), fill=ORANGE)
    if title:
        d.text((120, 128), title, font=F('Bold', 56), fill=INK)
    return im, d

def fig_slide(name, section, title, fig, box=(120, 240, 1800, 930), crop=None, focus=None, img=None):
    im, d = base(section, title)
    f = img or Image.open(f'fig/{fig}.png').convert('RGB')
    if crop: f = f.crop(crop)
    if focus:  # 淡化非聚焦区域并描边
        veil = Image.new('RGB', f.size, (255, 255, 255))
        mask = Image.new('L', f.size, 170); ImageDraw.Draw(mask).rectangle(focus, fill=0)
        f = Image.composite(veil, f, mask)
        ImageDraw.Draw(f).rounded_rectangle(focus, radius=24, outline=ORANGE, width=12)
    f, pos = fit(f, box); im.paste(f, pos); return im

def text_block(d, xy, text, font, fill, maxw, lh):
    x, y = xy
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill); y += lh
    return y

SL = {}
# --- title ---
im = cover(Image.open(f"{REPO}/{THUMB['avp']}").convert('RGB'))
im = ImageEnhance.Brightness(im).enhance(0.38); d = ImageDraw.Draw(im)
d.text((120, 300), 'Seeing Eye to Eye', font=F('Bold', 120), fill='white')
y = text_block(d, (124, 460), 'Enabling Cognitive Alignment Through Shared First-Person Perspective in Human–AI Collaboration', F('Medium', 44), (235, 235, 235), 1300, 62)
d.rectangle((124, y + 30, 224, y + 36), fill=ORANGE)
d.text((124, y + 64), 'Zhuyu Teng, Pei Chen, Yichen Cai, Ruoqing Lu, Zhaoqu Jiang, Jiayang Li, Weitao You, Lingyun Sun', font=F('Regular', 30), fill=(220, 220, 220))
d.text((124, y + 110), 'Zhejiang University  ·  CHI 2026, Barcelona', font=F('Regular', 30), fill=(200, 200, 200))
SL['title'] = im

# --- motivation ---
for key, sec, title, quote, pts, col in [
    ('gulf_comm', 'Motivation · Gulf 1', 'The Communication Gulf',
     '“Which one? The blue one… no, on the left of the second shelf…”',
     ['Users must translate what they see and do into words.',
      'Rich, parallel physical intent (looking, pointing, holding) is squeezed into one linear verbal channel.',
      'Result: over-verbalization and attention mismatch.'], BLUE),
    ('gulf_under', 'Motivation · Gulf 2', 'The Understanding Gulf',
     'The AI sees the book, but not the hesitation.',
     ['Implicit embodied cues (gaze dwell, a pause, a hovering hand) go unnoticed.',
      'Personal rules agreed earlier are forgotten: common ground drifts.',
      'Result: intervention blindness and generic, one-size-fits-all advice.'], GREEN)]:
    im, d = base(sec, title)
    d.rounded_rectangle((120, 290, 900, 720), radius=36, fill=(255, 255, 255), outline=col, width=5)
    text_block(d, (180, 360), quote, F('SemiBold', 50), col, 660, 72)
    y = 330
    for p in pts:
        d.ellipse((1000, y + 18, 1018, y + 36), fill=col)
        y = text_block(d, (1050, y), p, F('Regular', 40), INK, 740, 56) + 40
    SL[key] = im

im, d = base('Research Question')
y = text_block(d, (220, 380), 'How might we exploit a shared first-person perspective to achieve continuous cognitive alignment in human–AI collaboration?', F('SemiBold', 66), INK, 1480, 92)
d.rectangle((220, 330, 340, 338), fill=ORANGE)
SL['rq'] = im

# --- framework / system ---
SL['fig2'] = fig_slide('fig2', 'Framework', 'Eye2Eye: a perceive – align – reflect loop', 'fig2')
SL['fig3_human'] = fig_slide('fig3_human', 'Framework · Component I', 'Joint Attention: human cues ↔ AI cues', 'fig3')
SL['fig5'] = fig_slide('fig5', 'Framework · Component II', 'Accumulated Common Ground: dynamic object cards', 'fig5')
SL['fig6'] = fig_slide('fig6', 'Framework · Component III', 'Reflective Situated Feedback: four strategies', 'fig6')
f4 = Image.open('fig/fig4.png').convert('RGB')
SL['fig4_I'] = fig_slide('', 'System · Apple Vision Pro', 'Always-on perception, event-driven triggering', None, img=f4, crop=(0, 0, 1760, 1545), box=(120, 230, 1800, 930))
SL['fig4_II'] = fig_slide('', 'System', 'Retrieve & revise object cards (similarity > λ)', None, img=f4, crop=(0, 1530, 2824, 2120), box=(120, 260, 1800, 930))
SL['fig4_III'] = fig_slide('', 'System', 'Feedback strategy → AR overlay + voice (≈ 4–5 s)', None, img=f4, crop=(1740, 0, 2824, 1545), box=(120, 230, 1800, 930))
SL['fig7'] = fig_slide('fig7', 'Generalization', 'Procedural · Classification · Inspection', 'fig7', box=(120, 300, 1800, 900))

# --- results ---
im, d = base('User Study', 'Eye2Eye vs. Baseline (same headset, same models)')
for i, (big, small) in enumerate([('60', 'participants\nbetween-subjects'), ('3', 'tasks: coffee machine,\nbook sorting, circuit board'), ('2,338', 'interaction turns\nanalysed with mixed-effects models')]):
    x = 120 + i * 580
    d.rounded_rectangle((x, 330, x + 520, 820), radius=32, fill=(255, 255, 255))
    d.text((x + 50, 380), big, font=F('Bold', 150), fill=ORANGE)
    d.multiline_text((x + 54, 600), small, font=F('Regular', 38), fill=INK, spacing=14)
SL['study'] = im
im, d = base('Results', 'Less friction, fewer errors')
for i, (big, small) in enumerate([('−58%', 'likelihood of errors\nper interaction turn'), ('−50%', 'clarification turns'), ('−23%', 'interaction turns\n(procedural task)')]):
    x = 120 + i * 580
    d.rounded_rectangle((x, 330, x + 520, 820), radius=32, fill=(255, 255, 255))
    d.text((x + 50, 390), big, font=F('Bold', 140), fill=BLUE)
    d.multiline_text((x + 54, 600), small, font=F('Regular', 38), fill=INK, spacing=14)
d.text((120, 880), 'Generalized linear mixed-effects models; all p ≤ .002.', font=F('Regular', 28), fill=MUTED)
SL['numbers'] = im
f8 = Image.open('fig/fig8.png').convert('RGB'); f8 = f8.crop((0, 0, int(f8.width * 0.615), int(f8.height * 0.955)))
f9 = Image.open('fig/fig9.png').convert('RGB'); f9 = f9.crop((int(f9.width * 0.415), 0, f9.width, f9.height))
im, d = base('Results', 'Errors grow slower · higher fluency, co-presence & trust')
a, pa = fit(f8, (80, 260, 1010, 930)); im.paste(a, pa)
b, pb = fit(f9, (1040, 260, 1840, 930)); im.paste(b, pb)
SL['fig89'] = im
im, d = base()
d.text((120, 330), 'Seeing Eye to Eye', font=F('Bold', 110), fill=INK)
d.rectangle((124, 480, 224, 486), fill=ORANGE)
d.text((124, 520), 'Zhuyu Teng, Pei Chen*, Yichen Cai, Ruoqing Lu,', font=F('Regular', 36), fill=INK)
d.text((124, 568), 'Zhaoqu Jiang, Jiayang Li, Weitao You, Lingyun Sun', font=F('Regular', 36), fill=INK)
d.text((124, 640), 'College of Computer Science and Technology, Zhejiang University', font=F('Regular', 32), fill=MUTED)
d.text((124, 740), 'CHI ’26 · April 13–17, 2026 · Barcelona, Spain', font=F('SemiBold', 34), fill=INK)
d.text((124, 792), 'doi.org/10.1145/3772318.3791059', font=F('Regular', 32), fill=BLUE)
SL['end'] = im
for k, v in SL.items(): v.save(f'{OUT}/slides/{k}.png')

# --- footage placeholder ---
def placeholder(s):
    _, mat, desc, th = s['vis']
    if th:
        im = cover(Image.open(f'{REPO}/{THUMB[th]}').convert('RGB'))
        im = ImageEnhance.Brightness(im).enhance(0.55)
    else:
        im = Image.new('RGB', (W, H), (30, 32, 38))
        dd = ImageDraw.Draw(im)
        for x in range(80, W - 80, 40): dd.line((x, 80, x + 20, 80), fill=(90, 90, 100), width=3); dd.line((x, H - 80, x + 20, H - 80), fill=(90, 90, 100), width=3)
    d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((80, 80, 80 + 1100, 300), radius=20, fill=(0, 0, 0, 150))
    bw = d.textlength('原片素材 FOOTAGE', font=ZH(28, True))
    d.rounded_rectangle((110, 108, 110 + bw + 36, 156), radius=12, fill=ORANGE)
    d.text((128, 110), '原片素材 FOOTAGE', font=ZH(28, True), fill='white')
    d.text((110, 170), mat, font=ZH(44, True), fill='white')
    d.text((110, 236), desc, font=ZH(30), fill=(225, 225, 225))
    return im

def with_label(im, label):
    if not label: return im
    im = im.copy(); d = ImageDraw.Draw(im, 'RGBA'); f = F('SemiBold', 30)
    w = d.textlength(label, font=f)
    d.rounded_rectangle((W - 100 - w - 48, 90, W - 100, 146), radius=28, fill=(*BLUE, 235))
    d.text((W - 100 - w - 24, 98), label, font=f, fill='white')
    return im

# --- timeline ---
import re
def split_text(txt, maxc=80):
    parts = [p for p in re.split(r'(?<=[.?!:])\s+', txt) if p]
    out = []
    for p in parts:
        while len(p) > maxc:
            cs = [m.end() for m in re.finditer(r',\s', p)] or [m.end() for m in re.finditer(r'\s', p)]
            k = min(cs, key=lambda c: abs(c - len(p) / 2))
            out.append(p[:k].strip()); p = p[k:].strip()
        out.append(p)
    return out
def chunk(st, dur, sp, txt):
    ps = split_text(txt); n = sum(len(p) for p in ps); res = []
    for p in ps:
        d = dur * len(p) / n; res.append((st, st + d, sp, p)); st += d
    return res

meta = json.load(open('tts/meta.json'))
SR = 24000; GAP, HEAD, TAIL = 0.35, 0.45, 0.4
t = 0.0; cues = []; shots = []; clips = []
for s in script.S:
    start = t; cur = t + (0.8 if s['id'] == '0.1' else HEAD)
    for i, l in enumerate(s['lines']):
        fn = f"tts/{s['id']}_{i}_{l[0]}.wav"; dur = meta[fn]
        clips.append((cur, fn)); cues += chunk(cur, dur, l[0], l[1]); cur += dur + GAP
    end = cur - (GAP if s['lines'] else 0) + TAIL
    if s['sec'] == 'Demo' and s['vis'][0] == 'footage': end += 0.8  # 留出动作/AR 反馈的画面时间
    end = max(end, start + s['min'])
    s['start'], s['end'] = round(start, 2), round(end, 2)
    frame = SL[s['vis'][1]] if s['vis'][0] == 'slide' else placeholder(s)
    p = f"{OUT}/frames/{s['id']}.png"; with_label(frame, s['label'] if s['vis'][0] == 'footage' else '').save(p)
    shots.append((p, end - start)); t = end
TOTAL = t
print('TOTAL', round(TOTAL, 1), 's')

mix = np.zeros(int((TOTAL + 1) * SR), np.float32)
for st, fn in clips:
    a, sr = sf.read(fn, dtype='float32'); assert sr == SR
    i = int(st * SR); mix[i:i + len(a)] += a
mix = mix[:int(TOTAL * SR)]; mix *= 0.89 / max(1e-6, np.abs(mix).max())
sf.write(f'{OUT}/narration_full.wav', mix, SR)

def ts(x, sep=','):
    h, m = divmod(x, 3600); m, s = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace('.', sep)
tag = {'N': '', 'AI': 'AI: ', 'U': 'USER: '}
with open(f'{OUT}/subtitles_en.srt', 'w') as f:
    for i, (a, b, sp, txt) in enumerate(cues, 1):
        f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{tag[sp]}{txt}\n\n")
with open(f'{OUT}/sub.ass', 'w') as f:
    f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 0\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: N,Inter,44,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,4,0,0,2,200,200,56,1\n"
            "Style: AI,Inter,44,&H00FFE9C2,&H00FFFFFF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,4,0,0,2,200,200,56,1\n"
            "Style: U,Inter,44,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,0,1,0,0,100,100,0,0,4,0,0,2,200,200,56,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    for a, b, sp, txt in cues:
        f.write(f"Dialogue: 0,{ts(a, '.')[1:-1]},{ts(b, '.')[1:-1]},{sp},,0,0,0,,{tag[sp]}{txt}\n")
with open(f'{OUT}/concat.txt', 'w') as f:
    for p, du in shots: f.write(f"file '{os.path.abspath(p)}'\nduration {du:.3f}\n")
    f.write(f"file '{os.path.abspath(shots[-1][0])}'\n")
json.dump([{k: s[k] for k in ('id', 'sec', 'vis', 'lines', 'label', 'start', 'end')} for s in script.S], open(f'{OUT}/timeline.json', 'w'), ensure_ascii=False, indent=1)
