"""The hero's face set: same drawing style as the face Roblox Studio exported (assets/build.py).

    python faces.py  ->  assets/faces/<name>.png (1200x800, the head's face texture) + assets/faces/sheet.png

Coordinates are in the Studio SurfaceGui's 300x200 units. "calm" is the original face, untouched.
talk_1..talk_3 are mouth-open steps for lip sync (calm eyes and brows).
"""
import math, os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "faces")
SKIN = (255, 189, 127)
DARK = (25, 20, 20)
WHITE = (255, 255, 255)
TONGUE = (226, 92, 102)
TEAR = (120, 200, 255)
K = 8            # draw at 8x the GUI units, then downsample to 4x (1200x800) for smooth edges


class Face:
    def __init__(self):
        self.img = Image.new("RGB", (300 * K, 200 * K), SKIN)
        self.d = ImageDraw.Draw(self.img)

    def oval(self, cx, cy, w, h, col=DARK):
        self.d.ellipse([(cx - w / 2) * K, (cy - h / 2) * K, (cx + w / 2) * K, (cy + h / 2) * K], fill=col)

    def rect(self, x0, y0, x1, y1, col=SKIN):
        self.d.rectangle([x0 * K, y0 * K, x1 * K, y1 * K], fill=col)

    def brow(self, cx, cy, deg, w=52, h=11):
        """Rounded bar; deg is clockwise like Roblox Rotation."""
        t = Image.new("RGBA", (int(w * K * 1.6), int(w * K * 1.6)), (0, 0, 0, 0))
        td = ImageDraw.Draw(t)
        ox, oy = t.width / 2, t.height / 2
        td.rounded_rectangle([ox - w * K / 2, oy - h * K / 2, ox + w * K / 2, oy + h * K / 2], radius=h * K / 2, fill=DARK)
        t = t.rotate(-deg, resample=Image.BICUBIC)
        self.img.paste(t, (int(cx * K - ox), int(cy * K - oy)), t)

    def stroke(self, pts, width=11, col=DARK):
        """Thick polyline with round caps (pts in GUI units)."""
        p = [(x * K, y * K) for x, y in pts]
        r = width * K / 2
        # a chain of overlapping discs: smooth joints and round caps
        for (x0, y0), (x1, y1) in zip(p, p[1:] + [p[-1]]):
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / (r * 0.25)))
            for i in range(n + 1):
                x, y = x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n
                self.d.ellipse([x - r, y - r, x + r, y + r], fill=col)

    def arc(self, cx, cy, rx, ry, a0, a1, width=11, n=40):
        """Arc of an ellipse, angles in degrees, 0 = right, 90 = down."""
        pts = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in
               [a0 + (a1 - a0) * i / n for i in range(n + 1)]]
        self.stroke(pts, width)

    def poly(self, pts, col=DARK):
        self.d.polygon([(x * K, y * K) for x, y in pts], fill=col)

    # --- features
    def eyes(self, w=34, h=50, dy=0, glint=True, look=0.0):
        for cx in (100, 200):
            self.oval(cx, 84 + dy, w, h)
            if glint:
                self.oval(cx + 6 + look, 70 + dy, 10, 14, WHITE)

    def brows(self, dy=0, tilt=6, w=52):
        """tilt > 0: inner ends up (the original has 6; big = worried); tilt < 0: inner ends down (angry)."""
        self.brow(98, 38 + dy, -tilt, w)
        self.brow(202, 38 + dy, tilt, w)

    def smile(self, w=1.0, depth=1.0, dy=0):
        # the original ")" turned sideways: a U with little upturned tips
        cx, cy = 150, 148 + dy
        self.arc(cx, cy - 6, 32 * w, 14 * depth, 10, 170, 11)
        self.stroke([(cx - 34 * w, cy - 4), (cx - 36 * w, cy - 9)], 9)
        self.stroke([(cx + 34 * w, cy - 4), (cx + 36 * w, cy - 9)], 9)

    def open_mouth(self, h=24, w=40, tongue=True, teeth=True, dy=0):
        """D-shaped open mouth: flat top, round bottom."""
        cx, top = 150, 138 + dy
        pts = [(cx - w, top)] + [(cx + w * math.cos(math.radians(a)), top + h * math.sin(math.radians(a))) for a in range(180, -1, -6)][::-1]
        pts = [(cx + w * math.cos(math.radians(a)), top + h * math.sin(math.radians(a))) for a in range(0, 181, 6)]
        # round off the top corners a little
        self.poly(pts)
        self.stroke([(cx - w, top), (cx + w, top)], 8)
        if teeth and h > 12:
            self.d.rounded_rectangle([(cx - w * 0.72) * K, (top + 1) * K, (cx + w * 0.72) * K, (top + min(8, h * 0.3)) * K], radius=2 * K, fill=WHITE)
        if tongue and h > 16:
            self.oval(cx, top + h * 0.78, w * 0.9, h * 0.55, TONGUE)
            self.rect(cx - w, top + h + 1, cx + w, top + h + 30)  # trim tongue below the lip line
            # redraw the lower lip edge over the trimmed tongue
            self.arc(cx, top, w, h, 15, 165, 4)

    def frown(self, w=1.0, dy=0):
        self.arc(150, 166 + dy, 26 * w, 12, 200, 340, 11)

    def done(self, name):
        img = self.img.resize((1200, 800), Image.LANCZOS)
        img.save(os.path.join(OUT, f"{name}.png"))
        return img


# --- extreme-expression pieces (the frightened reference: white eyes, tiny pupils, big toothy mouths)
OUTLINE = 3.2
PURPLE = (200, 120, 205)
SWEAT = (140, 215, 255)
VEIN = (215, 40, 40)


def sclera(f, cx, cy, w, h, px=0, py=0, pupil=9, glint=True):
    f.oval(cx, cy, w + OUTLINE * 2, h + OUTLINE * 2)
    f.oval(cx, cy, w, h, WHITE)
    f.oval(cx + px, cy + py, pupil, pupil * 1.1)
    if glint and pupil > 7:
        f.oval(cx + px + pupil * 0.22, cy + py - pupil * 0.25, pupil * 0.3, pupil * 0.3, WHITE)


def outlined_poly(f, pts, fill=DARK, width=OUTLINE):
    f.poly(pts, fill)
    f.stroke(pts + [pts[0]], width)


def teeth_row(f, x0, x1, y0, y1, n, clip=None):
    """n white blocks with dark gaps between x0..x1."""
    w = (x1 - x0) / n
    for k in range(n):
        f.d.rounded_rectangle([(x0 + k * w + 0.8) * K, y0 * K, (x0 + (k + 1) * w - 0.8) * K, y1 * K], radius=2.5 * K, fill=WHITE)


def big_mouth(f, pts, top_teeth=None, bottom_teeth=None, tongue=None):
    """Dark mouth polygon; teeth rows given as (x0, x1, y0, y1, n); tongue as (cx, cy, w, h)."""
    f.poly(pts)
    if tongue:
        f.oval(*tongue, PURPLE)
    if top_teeth:
        teeth_row(f, *top_teeth)
    if bottom_teeth:
        teeth_row(f, *bottom_teeth)
    # cover anything that spilled outside the mouth with skin, then outline
    mask = Image.new("L", f.img.size, 0)
    ImageDraw.Draw(mask).polygon([(x * K, y * K) for x, y in pts], fill=255)
    skin = Image.new("RGB", f.img.size, SKIN)
    inside = f.img.copy()
    f.img.paste(skin, (0, 0), Image.eval(mask, lambda v: 255 - v))
    # paste back everything that was drawn before the mouth (eyes, brows) outside the mouth area
    return inside, mask


class FaceX(Face):
    """Draw the mouth FIRST (big_mouth masks the canvas), then eyes, brows and extras."""
    def mouth(self, pts, **kw):
        big_mouth(self, pts, **kw)
        self.stroke(pts + [pts[0]], OUTLINE)

    def crease(self, pts, width=2.6):
        self.stroke(pts, width)

    def sweat(self, x, y, s=1.0):
        self.poly([(x, y - 9 * s), (x - 5 * s, y + 2 * s), (x + 5 * s, y + 2 * s)], SWEAT)
        self.oval(x, y + 3 * s, 10 * s, 10 * s, SWEAT)

    def vein(self, x, y):
        for a in (45, 135, 225, 315):
            r = math.radians(a)
            self.stroke([(x + 3 * math.cos(r), y + 3 * math.sin(r)), (x + 9 * math.cos(r), y + 9 * math.sin(r))], 3.2, VEIN)

    def tear_stream(self, x, y0, y1):
        self.stroke([(x, y0), (x - 2, (y0 + y1) / 2), (x + 1, y1)], 6, TEAR)


def build(out_dir=None, skin=None, original_calm=True):
    """Draw the whole set. out_dir/skin let side characters get the same faces in their own skin tone."""
    global OUT, SKIN
    if out_dir:
        OUT = out_dir
    if skin:
        SKIN = tuple(skin)
    os.makedirs(OUT, exist_ok=True)
    out = {}
    if original_calm:
        calm = Image.open(os.path.join(HERE, "assets", "face_calm_src.png")).convert("RGB").resize((1200, 800), Image.LANCZOS)
        calm.save(os.path.join(OUT, "calm.png")); out["calm"] = calm
    else:
        f = Face(); f.brows(); f.eyes(); f.smile(); out["calm"] = f.done("calm")

    # lip-sync steps (calm eyes and brows)
    for i, h in enumerate((9, 18, 28), 1):
        f = Face(); f.brows(); f.eyes(); f.open_mouth(h, 30 + i * 4, tongue=h > 16, teeth=h > 12); out[f"talk_{i}"] = f.done(f"talk_{i}")

    # HAPPY: huge grin, cheeks pushed up
    f = FaceX()
    f.mouth([(104, 132), (196, 132), (188, 156), (170, 174), (150, 180), (130, 174), (112, 156)],
            top_teeth=(112, 188, 132, 145, 6), tongue=(150, 172, 46, 18))
    f.brows(-8, 4); f.eyes(36, 50)
    f.crease([(96, 128), (101, 138)]); f.crease([(204, 128), (199, 138)])
    out["happy"] = f.done("happy")

    # LAUGH: ^ ^ eyes, mouth wide open, tears of joy
    f = FaceX()
    f.mouth([(100, 126), (200, 126), (194, 154), (176, 180), (150, 188), (124, 180), (106, 154)],
            top_teeth=(110, 190, 126, 140, 6), tongue=(150, 180, 52, 22))
    f.brows(-10, 6)
    for cx in (100, 200):
        f.arc(cx, 92, 20, 18, 200, 340, 12)
    f.tear_stream(76, 96, 118); f.tear_stream(224, 96, 118)
    out["laugh"] = f.done("laugh")

    # SURPRISED / SHOCKED: tiny pupils, brows way up, tall O
    f = FaceX()
    f.mouth([(130, 132), (150, 126), (170, 132), (176, 154), (170, 178), (150, 186), (130, 178), (124, 154)],
            tongue=(150, 178, 26, 12), top_teeth=(134, 166, 129, 136, 3))
    f.brows(-18, 0, 56)
    sclera(f, 100, 82, 44, 54, 0, 0, 10); sclera(f, 200, 82, 44, 54, 0, 0, 10)
    for x0, s in ((70, -1), (230, 1)):
        f.crease([(x0, 56), (x0 + 8 * s, 50)]); f.crease([(x0 - 2 * s, 70), (x0 + 6 * s, 66)])
    out["surprised"] = f.done("surprised")

    # FRIGHTENED (the reference): white eyes with pin pupils, screaming toothy mouth, purple tongue, stress lines, sweat
    f = FaceX()
    mouth = [(102, 130), (118, 122), (134, 126), (150, 121), (166, 126), (182, 121), (198, 130),
             (192, 152), (182, 172), (166, 188), (150, 191), (134, 188), (118, 172), (108, 152)]
    f.mouth(mouth, top_teeth=(110, 190, 124, 142, 5), bottom_teeth=(128, 172, 176, 186, 4), tongue=(150, 182, 46, 16))
    f.crease([(96, 124), (100, 142), (106, 158)]); f.crease([(204, 124), (200, 142), (194, 158)])
    f.brow(94, 30, -22, 58, 12); f.brow(206, 30, 22, 58, 12)
    sclera(f, 100, 84, 46, 50, 3, 2, 7, glint=False); sclera(f, 200, 84, 46, 50, -3, 2, 7, glint=False)
    for cx, s in ((100, -1), (200, 1)):
        f.crease([(cx + 28 * s, 76), (cx + 34 * s, 72)], 2.4)
        f.crease([(cx + 29 * s, 88), (cx + 36 * s, 88)], 2.4)
        f.crease([(cx - 14, 114), (cx, 118), (cx + 14, 114)], 2.4)   # bags under the eyes
    f.crease([(140, 50), (146, 56)], 2.2); f.crease([(160, 50), (154, 56)], 2.2)
    f.sweat(66, 60, 1.2); f.sweat(236, 70, 0.9)
    out["scared"] = f.done("scared")

    # ANGRY: steep V brows, narrowed eyes, gritted teeth, vein
    f = FaceX()
    m = [(108, 136), (192, 136), (196, 152), (192, 168), (108, 168), (104, 152)]
    f.mouth(m, top_teeth=(110, 190, 138, 152, 6), bottom_teeth=(110, 190, 152, 166, 6))
    f.stroke([(108, 152), (192, 152)], 2.6)
    sclera(f, 100, 88, 42, 36, 4, 2, 13); sclera(f, 200, 88, 42, 36, -4, 2, 13)
    f.poly([(76, 64), (124, 84), (124, 60)], SKIN); f.poly([(224, 64), (176, 84), (176, 60)], SKIN)  # brows press the eyelids
    f.stroke([(78, 70), (124, 82)], 4); f.stroke([(222, 70), (176, 82)], 4)
    f.brow(102, 60, 26, 60, 14); f.brow(198, 60, -26, 60, 14)
    f.crease([(98, 132), (102, 146), (100, 160)]); f.crease([(202, 132), (198, 146), (200, 160)])
    f.vein(238, 40)
    out["angry"] = f.done("angry")

    # SAD / CRYING: worried brows, big glossy eyes, wobbly open frown, tear streams
    f = FaceX()
    f.mouth([(116, 176), (124, 156), (138, 146), (162, 146), (176, 156), (184, 176), (168, 170), (150, 172), (132, 170)],
            tongue=(150, 172, 30, 10))
    f.brow(98, 36, -24, 54, 12); f.brow(202, 36, 24, 54, 12)
    for cx in (100, 200):
        f.oval(cx, 86, 40, 52)
        f.oval(cx + 7, 72, 14, 18, WHITE); f.oval(cx - 8, 98, 7, 8, WHITE)
    f.tear_stream(92, 112, 150); f.tear_stream(208, 112, 154)
    out["sad"] = f.done("sad")

    # DETERMINED: low hard brows, focused eyes, confident teeth grin to one side
    f = FaceX()
    f.mouth([(124, 140), (186, 134), (182, 150), (164, 160), (140, 158)], top_teeth=(128, 184, 136, 146, 4))
    f.brow(100, 52, 18, 58, 13); f.brow(200, 52, -18, 58, 13)
    f.eyes(36, 46, 4)
    f.poly([(80, 62), (122, 74), (122, 58)], SKIN); f.poly([(220, 62), (178, 74), (178, 58)], SKIN)
    f.crease([(190, 128), (194, 138)])
    out["determined"] = f.done("determined")

    # SMUG: half-lidded eyes, one brow up, lopsided smirk
    f = FaceX()
    f.brow(98, 40, 4, 52, 11); f.brow(202, 30, 14, 52, 11)
    f.eyes(36, 50, 2, look=3)
    f.rect(76, 54, 124, 80); f.rect(176, 54, 224, 80)
    f.stroke([(80, 80), (120, 80)], 7); f.stroke([(180, 80), (220, 80)], 7)
    f.arc(164, 140, 26, 10, 20, 160, 11); f.stroke([(188, 142), (194, 132)], 9)
    out["smug"] = f.done("smug")

    # NERVOUS: worried brows, shrinking pupils, wavy mouth, sweat
    f = FaceX()
    f.brow(98, 36, 14, 52, 11); f.brow(202, 36, -14, 52, 11)
    sclera(f, 100, 86, 40, 48, -6, 0, 12); sclera(f, 200, 86, 40, 48, -6, 0, 12)
    f.stroke([(118, 154), (130, 146), (142, 154), (154, 146), (166, 154), (178, 147)], 8)
    f.sweat(234, 54, 1.3); f.sweat(70, 70, 0.8)
    out["nervous"] = f.done("nervous")

    # --- the five from the reference catalogue that the first set lacked
    # SHOCKED (lopsided): one eye much bigger, tall rounded mouth outlined black with white inside
    f = FaceX()
    f.oval(150, 158, 34 + OUTLINE * 2, 46 + OUTLINE * 2); f.oval(150, 158, 34, 46, WHITE)
    f.brow(96, 34, -10, 48, 11); f.brow(206, 24, 8, 54, 11)
    f.oval(100, 86, 30, 44); f.oval(204, 84, 46, 62)
    f.oval(108, 72, 8, 11, WHITE); f.oval(214, 66, 12, 16, WHITE)
    out["shocked"] = f.done("shocked")
    # WINK: one eye a closed curve, lopsided grin
    f = FaceX()
    f.brow(98, 38, 4, 52, 11); f.brow(202, 32, 10, 52, 11)
    f.oval(100, 84, 34, 50); f.oval(106, 70, 10, 14, WHITE)
    f.arc(200, 86, 18, 10, 200, 340, 10)
    f.arc(158, 140, 30, 13, 15, 165, 11); f.stroke([(186, 142), (192, 132)], 9)
    out["wink"] = f.done("wink")
    # SIDE-EYE: pupils pushed right, flat mouth
    f = FaceX()
    f.brow(98, 40, 2, 52, 11); f.brow(202, 36, -6, 52, 11)
    sclera(f, 100, 86, 40, 40, 11, 0, 14); sclera(f, 200, 86, 40, 40, 11, 0, 14)
    f.rect(78, 62, 222, 70); f.stroke([(80, 68), (120, 68)], 5); f.stroke([(180, 68), (220, 68)], 5)
    f.stroke([(128, 150), (172, 148)], 9)
    out["side_eye"] = f.done("side_eye")
    # PUFFED: holding breath / pretending - closed eyes, puffed ")(" mouth
    f = FaceX()
    f.brows(-2, 10)
    for cx in (100, 200):
        f.stroke([(cx - 18, 86), (cx, 80), (cx + 18, 86)], 9)
    f.arc(134, 150, 10, 16, -70, 70, 9); f.arc(166, 150, 10, 16, 110, 250, 9)
    f.oval(110, 120, 22, 10, (255, 150, 140)); f.oval(190, 120, 22, 10, (255, 150, 140))
    out["puffed"] = f.done("puffed")
    # ASLEEP: lashes, open snore mouth, bubble
    f = FaceX()
    f.brows(2, 6)
    for cx in (100, 200):
        f.arc(cx, 82, 18, 9, 20, 160, 9)
        for dx in (-12, 0, 12):
            f.stroke([(cx + dx, 92), (cx + dx * 1.3, 99)], 4)
    f.oval(150, 152, 18, 12)
    f.oval(176, 132, 26 + OUTLINE * 2, 26 + OUTLINE * 2, (120, 150, 170)); f.oval(176, 132, 26, 26, (215, 235, 250)); f.oval(170, 126, 7, 7, WHITE)
    out["asleep"] = f.done("asleep")
    # LITTLE O: tiny red round mouth, curious
    f = FaceX()
    f.brows(-6, 2); f.eyes(34, 50)
    f.oval(150, 150, 16 + OUTLINE * 2, 18 + OUTLINE * 2); f.oval(150, 150, 16, 18, (200, 40, 50))
    out["little_o"] = f.done("little_o")

    # HYPNO: spiral eyes, flat small smile (controlled)
    f = FaceX()
    f.brows(0, 0, 50)
    for cx in (100, 200):
        f.oval(cx, 86, 46 + OUTLINE * 2, 46 + OUTLINE * 2); f.oval(cx, 86, 46, 46, WHITE)
        pts = [(cx + (1.2 + 0.85 * a) * math.cos(a), 86 + (1.2 + 0.85 * a) * math.sin(a)) for a in [i * 0.12 for i in range(0, 220)]]
        f.stroke(pts, 3.2)
    f.stroke([(132, 150), (168, 150)], 7)
    out["hypno"] = f.done("hypno")

    # BLINK
    f = Face(); f.brows()
    for cx in (100, 200):
        f.arc(cx, 80, 17, 9, 20, 160, 10)
    f.smile(); out["blink"] = f.done("blink")

    # contact sheet with labels
    names = list(out)
    cols = 5
    tw, th = 300, 200
    sheet = Image.new("RGB", (tw * cols, (th + 26) * math.ceil(len(names) / cols)), "white")
    sd = ImageDraw.Draw(sheet)
    for i, n in enumerate(names):
        x, y = (i % cols) * tw, (i // cols) * (th + 26)
        sheet.paste(out[n].resize((tw, th), Image.LANCZOS), (x, y + 26))
        sd.text((x + 8, y + 6), n, fill="black")
    sheet.save(os.path.join(OUT, "sheet.png"))
    print(len(names), "faces:", ", ".join(names))


SIDE_SKINS = {"light": (255, 214, 170), "tan": (222, 168, 110), "brown": (150, 96, 56), "pale": (250, 226, 200)}

if __name__ == "__main__":
    import sys
    if "--all" in sys.argv:   # side-character skin tones too
        for k, v in SIDE_SKINS.items():
            build(os.path.join(HERE, "assets", "faces_" + k), v, original_calm=False)
    build(os.path.join(HERE, "assets", "faces"), (255, 189, 127), original_calm=True)
