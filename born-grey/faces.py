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


def build():
    os.makedirs(OUT, exist_ok=True)
    out = {}
    calm = Image.open(os.path.join(HERE, "assets", "face_calm_src.png")).convert("RGB").resize((1200, 800), Image.LANCZOS)
    calm.save(os.path.join(OUT, "calm.png")); out["calm"] = calm

    f = Face(); f.brows(-3); f.eyes(); f.open_mouth(26, 40); out["happy"] = f.done("happy")
    for i, h in enumerate((9, 16, 24), 1):          # lip sync steps
        f = Face(); f.brows(); f.eyes(); f.open_mouth(h, 30 + i * 3, tongue=h > 16, teeth=h > 12); out[f"talk_{i}"] = f.done(f"talk_{i}")
    f = Face(); f.brows(-12, 0); f.eyes(38, 56, -2); f.oval(150, 152, 26, 32); out["surprised"] = f.done("surprised")
    f = Face(); f.brows(-6, 16); f.eyes(36, 54, -1, look=-2)
    f.d.rounded_rectangle([118 * K, 140 * K, 182 * K, 162 * K], radius=6 * K, fill=DARK)
    f.d.rectangle([123 * K, 145 * K, 177 * K, 157 * K], fill=WHITE)
    for x in range(132, 176, 10):
        f.d.line([(x * K, 145 * K), (x * K, 157 * K)], fill=DARK, width=int(1.6 * K))
    out["scared"] = f.done("scared")
    f = Face(); f.brows(8, -22); f.eyes(34, 44, 4); f.frown(1.0); out["angry"] = f.done("angry")
    f = Face(); f.brows(-2, 18); f.eyes(34, 48, 2)
    f.poly([(212, 104), (206, 122), (209, 128), (215, 128), (218, 122)], TEAR); f.oval(212, 124, 12, 12, TEAR)
    f.frown(0.8, -2); out["sad"] = f.done("sad")
    f = Face(); f.brows(6, -14); f.eyes(34, 46, 2)
    f.arc(156, 140, 26, 10, 20, 160, 11); f.stroke([(182, 140), (186, 132)], 9); out["determined"] = f.done("determined")
    f = Face(); f.brows(-6)
    for cx in (100, 200):
        f.arc(cx, 92, 18, 16, 200, 340, 11)          # ^ ^ happy closed eyes
    f.open_mouth(30, 44); out["laugh"] = f.done("laugh")
    f = Face(); f.brows()
    for cx in (100, 200):
        f.arc(cx, 80, 17, 9, 20, 160, 10)            # closed eyes, lids down
    f.smile(); out["blink"] = f.done("blink")
    f = Face(); f.brows(2, 2); f.eyes(34, 50, 2, look=3); f.rect(78, 52, 222, 78)  # half-lidded
    for cx in (100, 200):
        f.stroke([(cx - 18, 79), (cx + 18, 79)], 7)
    f.arc(160, 142, 22, 9, 20, 160, 11); f.stroke([(180, 142), (184, 134)], 9); out["smug"] = f.done("smug")
    f = Face(); f.brows(-4, 12); f.eyes(34, 50)
    f.stroke([(122, 152), (134, 146), (146, 152), (158, 146), (170, 152), (180, 147)], 9); out["nervous"] = f.done("nervous")

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


if __name__ == "__main__":
    build()
