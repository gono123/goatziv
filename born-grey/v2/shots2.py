"""Born Grey v2: 84 short shots (~1.5 s each), one per marker in lines.py. See ../STYLE_GUIDE.md.

Every shot: a set, a moving camera, faces chosen for the words, and props that show the rule.
S.n = frames, S.f(t) = frame of an absolute time, S.w(i) = (start, end) frames of word i of the shot.
"""
import math, random
import bpy
from mathutils import Vector
import blib as B
from blib import mat, box, cyl, sphere, text, empty
import shots as V1           # v1 set builders (bank, school, room, picnic, car, town_grid...)
import cast as C

GREY = V1.GREY_SKY
STORM = V1.STORM
BLUE = V1.BLUE_SKY
NIGHT = dict(top=(0.10, 0.04, 0.22), bottom=(0.30, 0.18, 0.45))


class Shot:
    def __init__(self, d, fps=24):
        self.d, self.fps, self.t0 = d, fps, d["start"]
        self.n = max(1, round(d["end"] * fps) - round(d["start"] * fps))

    def f(self, t):
        return max(1, int(round((t - self.t0) * self.fps)) + 1)

    def w(self, i):
        ws = self.d["words"]
        i = max(0, min(len(ws) - 1, i if i >= 0 else len(ws) + i))
        return self.f(ws[i]["s"]), self.f(ws[i]["e"])

    def word(self, needle, default=0):
        for i, x in enumerate(self.d["words"]):
            if needle.lower() in x["w"].lower():
                return self.w(i)[0]
        return self.w(default)[0]


# ----------------------------------------------------------------------------- helpers

def look(sky=GREY, sun=2.6, town=0.0):
    V1.base(sky, sun_e=sun, town=town)


def cam(S, a, b, la, lb=None, lens=32, lens_b=None):
    """A camera that is always moving (the reference never holds a static frame)."""
    c, t = B.camera(lens)
    B.cam_key(c, t, 1, a, la, lens)
    B.cam_key(c, t, S.n, b, lb or la, lens_b or lens)
    return c, t


def sign(lines_, loc, w=7, h=None, board="#ffffff", ink="#d81b2b", post=True, rot=0, size=0.9, parent=None):
    h = h or (0.6 + 1.15 * size * len(lines_.split("\n")))
    r = empty("sign", loc, parent)
    r.rotation_euler.z = math.radians(rot)
    box((w + 0.3, 0.18, h + 0.3), (0, 0.02, 0), mat("#c62828" if ink != "#d81b2b" else "#b71c1c", wash=False), r, name="signedge")
    box((w, 0.2, h), (0, 0, 0), mat(board, rough=0.5, wash=False), r, name="signboard")
    text(lines_, (0, -0.14, 0), mat(ink, wash=False), size=size, parent=r, extrude=0.02, font="Bungee-Regular.ttf")
    if post:
        cyl(0.14, loc[2], (0, 0.1, -loc[2] / 2 - h / 2 + 0.2), mat("#555555", wash=False), r)
    return r


def street_set(sky=GREY, town=0.0, dome=True, sun=2.6):
    look(sky, sun, town)
    B.ground(600)
    B.street(160)
    if dome:
        B.dome()


def yard_set(sky=GREY, town=0.0, dome=True):
    look(sky, 2.4, town)
    V1.school(30)
    if dome:
        B.dome()
    for x in (14, 17):    # the bins
        cyl(1.3, 3.4, (x, -4, 1.7), mat("#4f6b52", rough=0.6), name="bin")
        cyl(1.4, 0.3, (x, -4, 3.5), mat("#3c5240", rough=0.6), name="lid")


def bank_set(sky=GREY, town=0.0):
    look(sky, 2.6, town)
    B.ground(600)
    V1.bank(0, 14)


def jar(loc, color, h=1.4, r=0.45, label=None, parent=None):
    g = cyl(r, h, loc, mat("#e8f2ff", rough=0.05, alpha=0.35, wash=False), parent, name="jar")
    cyl(r * 0.85, h * 0.7, (loc[0], loc[1], loc[2] - h * 0.12), mat(color, emit=2.2, wash=False), parent, name="paint")
    cyl(r * 1.05, 0.2, (loc[0], loc[1], loc[2] + h / 2), mat("#b0b0b0", metal=0.8, rough=0.3, wash=False), parent, name="lid")
    if label:
        text(label, (loc[0], loc[1] - r - 0.03, loc[2] - 0.1), mat("#222222", wash=False), size=0.18, parent=parent, extrude=0.0)
    return g


RAINBOW = ["#ff2d55", "#ff9500", "#ffe600", "#34c759", "#00c7ff", "#5856d6", "#ff2dc8", "#8e5cff", "#00e0a8"]


def vault_set(names=False):
    """Inside the Color Bank: shelves of glowing colour jars, a counter, a rainbow sign."""
    look(GREY, 1.2)
    box((60, 60, 0.2), (0, 0, -0.1), mat("#cfcac0", rough=0.3), name="marble")
    box((60, 0.5, 26), (0, 14, 13), mat("#b9b3a8", rough=0.8), name="vaultwall")
    for row in range(5):
        z = 2.5 + row * 3.4
        box((40, 1.6, 0.25), (0, 12.6, z - 0.9), mat("#7a5a3a"), name="shelf")
        for k in range(17):
            x = -19 + k * 2.4
            jar((x, 12.6, z), RAINBOW[(k + row * 3) % len(RAINBOW)],
                label=(["TOMMY", "ANNA", "LEO", "MIA", "SAM", "ZOE", "BEN", "IVY", "MAX"][(k + row) % 9] if names else None))
    B.letters("COLOR BANK", (0, 12.2, 20.5), 2.6, RAINBOW, extrude=0.15)
    box((18, 3, 4), (0, 2, 2), mat("#5d4632", rough=0.5), name="counter")
    box((18.4, 3.4, 0.3), (0, 2, 4.1), mat("#d4af37", metal=0.9, rough=0.3, wash=False), name="countertop")
    B.point((0, -4, 14), 1200, (1, 0.95, 0.9), 4)


def home_set(sky=GREY):
    look(sky, 0.9)
    V1.room()


def top_set():
    look(STORM, 1.6)
    box((30, 30, 1), (0, 0, -0.5), mat("#8b95a1", metal=0.6, rough=0.35, wash=False), name="platform")
    for x in range(-14, 15, 4):
        box((0.3, 0.3, 3), (x, -14.5, 1.5), mat("#6c7580", wash=False))
    box((29, 0.3, 0.3), (0, -14.5, 3), mat("#6c7580", wash=False))
    B.dome()
    box((4, 3, 3), (0, 4, 1.5), mat("#4b5563", metal=0.4, wash=False), name="leverbase")
    piv = empty("leverpiv", (0, 4, 3))
    piv.rotation_euler.x = math.radians(-35)
    cyl(0.25, 6, (0, 0, 3), mat("#c0c6cc", metal=0.9, rough=0.2, wash=False), piv, name="stick")
    sphere(0.8, (0, 0, 6.2), mat("#e11d2e", rough=0.3, wash=False), piv, name="knob")
    sign("DO NOT\nOPEN", (4.4, 3.0, 6.4), w=6.6, size=0.95, post=True)
    return piv


def rain(center, size, z=24, rate=900, lifetime=14, speed=-48):
    return B.rain(center, size=size, z=z, rate=rate, lifetime=lifetime, speed=speed)


def bubbles(loc, f0, n=10):
    rnd = random.Random(f0)
    m = mat("#f2f8ff", rough=0.05, alpha=0.6, wash=False)
    for i in range(n):
        o = sphere(rnd.uniform(0.15, 0.35), loc, m, name="bubble")
        p0 = Vector(loc) + Vector((rnd.uniform(-1, 1), rnd.uniform(-0.6, 0.2), rnd.uniform(-1, 1)))
        o.location = p0; o.keyframe_insert("location", frame=f0)
        o.location = p0 + Vector((rnd.uniform(-0.5, 0.5), 0, rnd.uniform(1.5, 3))); o.keyframe_insert("location", frame=f0 + 40)


def brush(parent):
    """A big grey scrub brush held in a hand (parent = shoulder pivot)."""
    r = empty("brush", (0, -0.5, -2.0), parent)
    cyl(0.12, 2.2, (0, -0.9, 0), mat("#3a3a3a", wash=False), r, rot=(90, 0, 0))
    box((1.6, 0.6, 0.5), (0, -2.0, 0), mat("#777b80", wash=False), r, name="brushhead")
    box((1.5, 0.5, 0.35), (0, -2.0, -0.4), mat("#d8d8d8", wash=False), r, name="bristles")
    return r


def lineup(n, y=0, spacing=4.2, faces=None, start=0, **kw):
    out = []
    for i in range(n):
        x = (i - (n - 1) / 2) * spacing
        out.append(C.townie(start + i, (x, y + (i % 2) * 1.2, 0.5), rot=0, face=(faces[i % len(faces)] if faces else "calm"), **kw))
    return out


# ============================================================================ the 84 shots

def aerial(S):
    look(GREY); B.ground(900); V1.town_grid(3); B.street(160); B.dome()
    cam(S, (0, -95, 60), (8, -80, 46), (0, 10, 28), (0, 10, 18), 24)


def greyhair(S):
    street_set()
    a = C.townie(1, (-1.2, 0, 0.5), rot=10, face="calm"); b = C.townie(4, (1.6, 1.0, 0.5), rot=-15, face="side_eye")
    a.idle(1, S.n); b.idle(1, S.n, phase=2)
    cam(S, (-1.5, -9.5, 6.2), (1.5, -8.6, 6.0), (0.2, 0.5, 5.2), lens=38)


def greyclothes(S):
    street_set()
    for i, (x, y) in enumerate([(-5, -10), (0, -9), (5, -10.5)]):
        c = C.townie(i, (x, y, 0.5), face="calm")
        c.walk(1, S.n + 20, (x - 2, y, 0.5), (x + 6, y, 0.5), stride=10)
    cam(S, (-2, -21, 3.2), (3, -20, 3.0), (0, -9.5, 3.0), lens=34)


def greyeyes(S):
    street_set()
    c = C.townie(2, (0, 0, 0.5), face="calm")
    c.idle(1, S.n)
    cam(S, (0.3, -5.2, 5.3), (0.1, -4.4, 5.25), (0, 0, 5.2), lens=50)


def bank_ext(S):
    bank_set()
    for i in range(5):
        C.townie(i, (2.0 - i * 0.2, 6 - i * 3.4 - 2, 1.2), rot=180, face="calm").idle(1, S.n, phase=i)
    cam(S, (14, -38, 4), (9, -30, 3.5), (0, 8, 12), lens=30)


def bank_int(S):
    vault_set()
    clerk = C.townie(3, (0, 5, 0), rot=180, face="smug"); clerk.root.rotation_euler.z = 0
    for i in range(3):
        C.townie(i, (-3 + i * 3, -2.5, 0), rot=180, face="calm")
    cam(S, (-8, -16, 6), (6, -15, 7), (0, 8, 8), lens=26)


def test_a(S):
    yard_set()
    k = C.townie(2, (0, 0, 0.2), face="happy")
    k.pose(1, "hold"); V1.paper(k.sh[0], (0, -0.6, -2.3))
    k.move(1, (0, 0, 0.2)); k.move(8, (0, 0, 1.0)); k.move(14, (0, 0, 0.2))
    cam(S, (2, -12, 4.6), (1, -10, 4.4), (0, 0, 3.6), lens=40)


def drop_yellow(S):
    yard_set()
    k = C.townie(2, (0, 0, 0.2), face="little_o")
    k.pose(1, "hold")
    j = cyl(0.45, 0.9, (0, -0.6, -2.3), mat("#dfefff", rough=0.05, alpha=0.35, wash=False), k.sh[1], name="jar")
    sphere(0.22, (0, 0, -0.2), mat("#ffe600", emit=7.0, wash=False), j, name="drop")
    B.point((1.5, -3, 2.6), 80, (1, 0.9, 0.2), 0.5)
    k.set_face(S.word("yellow"), "laugh")
    cam(S, (2.2, -7.5, 4.4), (1.6, -6.2, 4.2), (0.8, -1.6, 3.6), lens=40)


def grandma_sock(S):
    street_set()
    g = C.grandma((0, 0, 0.5), face="laugh")
    g.pose(1, "point_up")
    s = empty("sock", (0, -0.3, -2.4), g.sh[1])
    box((0.45, 0.45, 1.4), (0, 0, -0.5), mat("#ffd400", emit=0.5, wash=False), s)
    box((0.45, 0.9, 0.45), (0, -0.25, -1.2), mat("#ffd400", emit=0.5, wash=False), s)
    B.sparkle_burst((1.5, -0.6, 8.5), 6, n=10, color="#fff38a", spread=2)
    cam(S, (-3, -14, 4), (-2, -12, 5), (0.6, 0, 5.2), lens=36)


def mailman_walk(S):
    street_set()
    V1.car(-4, -4.5, "#c0392b")
    sold = box((3.2, 0.1, 1.6), (-4, -6.8, 4.5), mat("#ffffff", wash=False), name="sold")
    text("SOLD", (0, -0.08, 0), mat("#e02424", wash=False), size=1.0, parent=sold, extrude=0.02)
    m = C.mailman((-14, -10, 0.5))
    m.walk(1, S.n, (-14, -10, 0.5), (2, -10, 0.5), stride=10)
    cam(S, (-12, -26, 5), (0, -24, 5), (-8, -8, 3.4), (2, -8, 3.6), lens=30)


def mailman_wave(S):
    street_set()
    m = C.mailman((0, 0, 0.5), face="happy")
    m.pose(1, "wave"); m.idle(1, S.n, arms=False)
    m.set_face(S.word("healthy"), "wink")
    cam(S, (1.5, -11, 5.2), (0.8, -8.5, 5.0), (0, 0, 4.6), lens=38)


def prism_reveal(S):
    bank_set()
    p = C.prism((0, 2, 1.2), face="smug")
    p.pose(1, "hips"); p.idle(1, S.n, arms=False)
    for k, c in enumerate([(1, 0.2, 0.4), (0.2, 0.6, 1), (1, 0.9, 0.1), (0.3, 1, 0.4)]):
        B.point((math.cos(k * 1.57) * 3, -1 + math.sin(k * 1.57) * 2, 6), 400, c, 1)
    cam(S, (0, -26, 1.8), (0, -18, 2.2), (0, 2, 7), (0, 2, 6.5), lens=28)


def prism_shield(S):
    bank_set()
    C.prism((0, 4, 1.2), face="laugh").pose(1, "arms_out")
    for i, (x, y, fc) in enumerate([(-3.5, -6, "shocked"), (3.5, -6.5, "side_eye"), (0, -9, "scared")]):
        t = C.townie(i, (x, y, 0.5), rot=180 + (12 if x < 0 else -12), face=fc)
        t.pose(1, "shield"); t.root.rotation_euler.z = math.radians(180 + (12 if x < 0 else -12))
    B.point((0, 2, 7), 2500, (1, 0.8, 1), 3)
    cam(S, (6, -22, 6), (4, -19, 5.5), (0, -4, 5), lens=32)


def umbrella_up(S):
    street_set()
    C.townie(0, (2, -4, 0.5), face="calm").head_turn(1, 0, -30)
    cam(S, (0, -14, 3), (0, -14, 3.5), (0, 0, 8), (0, 40, 120), lens=24)


def dome_aerial(S):
    look(GREY); B.ground(1200); V1.town_grid(3); B.street(160); B.dome()
    cam(S, (0, -360, 120), (40, -400, 140), (0, 0, 110), lens=24)


def sign_rain(S):
    street_set()
    sign("NO RAIN\nRAIN WASHES\nCOLOR AWAY!", (0, 0, 6), w=10, size=0.95)
    text("- THE COLOR BANK", (0, -0.2, 3.3), mat("#333333", wash=False), size=0.5, extrude=0.01)
    cam(S, (-3, -14, 5), (2, -12, 5.6), (0, 0, 5.8), lens=34)


def dry_street(S):
    street_set()
    sign("DAYS WITHOUT RAIN:\n36,500", (6, -8, 5.5), w=11, board="#1f2a1f", ink="#7dff7a", size=0.8)
    for i in range(3):
        c = C.townie(i, (-10 + i * 5, -10 - i, 0.5), face="calm")
        c.walk(1, S.n + 10, (-12 + i * 5, -10 - i, 0.5), (-6 + i * 5, -10 - i, 0.5), stride=11)
    cam(S, (-8, -30, 6), (4, -28, 5), (0, -8, 4), lens=28)


def sign_rule(S):
    street_set()
    sign("BY ORDER OF THE\nCOLOR BANK:\nNO UNPAID COLOR", (0, 0, 6.5), w=12, size=0.85)
    cam(S, (2, -13, 4.5), (-1, -11, 5), (0, 0, 6.3), lens=34)


def inspectors_march(S):
    street_set(sky=NIGHT, sun=0.8)
    ins = []
    for i, x in enumerate((-3.5, 0, 3.5)):
        c = C.inspector("insp%d" % i, (x, 20, 0.5))
        c.walk(1 + i * 2, S.n, (x, 18, 0.5), (x, 4, 0.5), stride=12, swing=24)
        ins.append(c)
    V1.blink(V1.emis(ins[0].siren.data.materials[0]), 1, S.n, 12)
    V1.flash_light((0, 6, 9), 1, S.n, period=12, energy=2500)
    cam(S, (0, -12, 1.5), (0, -14, 1.3), (0, 10, 5.5), lens=26)


def inspector_mop(S):
    street_set(sky=NIGHT, sun=0.8)
    c = C.inspector("insp", (0, 0, 0.5))
    c.pose(1, "hold"); brush(c.sh[1])
    V1.blink(V1.emis(c.siren.data.materials[0]), 1, S.n, 10)
    cam(S, (-2, -9, 1.5), (-1, -8, 1.2), (0, 0, 5.5), lens=30)


def scrub(S):
    street_set(sky=NIGHT, sun=1.0)
    v = C.townie(5, (0, 0, 0.5), face="scared")
    v.wash_keys([(1, -0.5), (S.n, 7.0)])          # colour scrubbed off, feet to head
    insp = C.inspector("insp", (2.6, -1.4, 0.5), rot=-60)
    brush(insp.sh[1]); scrub_arm(insp, S.n)
    bubbles((1.0, -1.0, 4), 2, 14)
    cam(S, (1.5, -10, 5), (0.5, -8, 4.8), (0.6, 0, 4), lens=34)


def scrub_arm(c, n):
    f = 1
    while f < n:
        c.key_rot(c.sh[1], f, -70); c.key_rot(c.sh[1], f + 4, -105)
        f += 8


def inspector_close(S):
    street_set(sky=NIGHT, sun=0.6)
    c = C.inspector("insp", (0, 0, 0.5))
    V1.blink(V1.emis(c.siren.data.materials[0]), 1, S.n, 8)
    V1.flash_light((0, -3, 8), 1, S.n, period=8, energy=1500)
    cam(S, (0.6, -7.5, 6.2), (0.3, -6.0, 6.1), (0, 0, 5.8), lens=45)


def hero_school(S):
    yard_set()
    h = C.hero((0, -4, 0.2), colored=False, face="side_eye")
    h.idle(1, S.n)
    for i, (x, y) in enumerate([(-7, 2), (7, 3)]):
        C.townie(i, (x, y, 0.2), rot=180, face="calm").idle(1, S.n, phase=i)
    cam(S, (2, -17, 4.5), (1, -14, 4.6), (0, -4, 3.8), lens=34)


def hero_lunch(S):
    yard_set()
    V1.picnic(0, 0)
    h = C.hero((0, -2.6, 0.15), colored=False, face="puffed")
    V1.sit(h, 1)
    box((3, 2, 0.15), (0, -1.2, 3.5), mat("#8f9399"), name="tray")
    sphere(0.6, (-0.6, -1.2, 3.8), mat("#9a9ea4", rough=0.9), scale=(1, 1, 0.5), name="mush")
    box((0.9, 0.9, 0.9), (0.7, -1.2, 4.0), mat("#a5a8ad"), name="cube")
    h.head_turn(1, 0, 25)
    cam(S, (1.6, -9.5, 6.6), (1.0, -8.2, 6.3), (0, -1.6, 4.2), lens=36)


def mom_paint(S):
    home_set()
    h = C.hero((-1.5, 0, 0), rot=-20, colored=False, face="side_eye")
    h.pose(1, "arms_out")
    m = C.mom((3.0, -1.2, 0), rot=60, face="happy")
    m.pose(1, "roll")
    roller = empty("roller", (0, -0.4, -2.2), m.sh[1])
    cyl(0.12, 1.8, (0, 0, 0), mat("#333333"), roller)
    cyl(0.5, 1.6, (0, -0.2, 1.0), mat("#8a8d92", rough=0.9), roller, rot=(0, 90, 0))
    f = 1
    while f < S.n:
        m.key_rot(m.sh[1], f, -70); m.key_rot(m.sh[1], f + 9, -125); f += 18
    cam(S, (2, -17, 6.2), (0.5, -14, 6.0), (0.5, 0, 3.8), lens=30)


def mom_close(S):
    home_set()
    m = C.mom((0, 1, 0), face="happy")
    m.idle(1, S.n)
    m.set_face(S.word("says"), "wink")
    cam(S, (0.6, -4.5, 5.4), (0.3, -3.8, 5.3), (0, 1, 5.2), lens=42)


def hero_shrug(S):
    home_set()
    h = C.hero((0, 0, 0), colored=False, face="side_eye")
    h.pose(1, "hips"); h.pose(6, "arms_out"); h.pose(S.n, "hips")
    cam(S, (1, -11, 5), (0.5, -9.5, 4.8), (0, 0, 3.8), lens=36)


def mom_rule(S):
    home_set()
    m = C.mom((0, 1, 0), face="determined")
    m.pose(1, "point_up")
    cam(S, (-1, -9, 5.2), (-0.5, -8, 5.0), (0, 1, 4.8), lens=36)


def mom_wag(S):
    home_set()
    m = C.mom((0, 1, 0), face="angry")
    f = 1
    while f < S.n:
        m.key_rot(m.sh[1], f, -150, 12); m.key_rot(m.sh[1], f + 4, -150, 12, 18); f += 8
    cam(S, (1.2, -4.6, 5.6), (0.8, -4.0, 5.5), (0, 1, 5.2), lens=42)


def run_rule(S):
    street_set(sky=STORM)
    rain((0, -9), (60, 20), rate=2000)
    h = C.hero((-14, -9, 0.5), colored=False, face="scared")
    h.walk(1, S.n, (-14, -9, 0.5), (8, -9, 0.5), run=True)
    cam(S, (-12, -28, 4.5), (6, -28, 4.5), (-12, -9, 3.6), (8, -9, 3.6), lens=30)


def dont_look_up(S):
    street_set(sky=STORM)
    rain((0, 0), (20, 20), rate=1500)
    h = C.hero((0, 0, 0.5), colored=False, face="nervous")
    h.pose(1, "scared"); h.head_turn(1, 0, 30)
    cam(S, (0, -9, 9), (0, -8, 8), (0, 0, 4), lens=34)


def pip_intro(S):
    yard_set()
    p = C.pip((0, 0, 0.2), face="happy")
    p.pose(1, "wave"); p.idle(1, S.n, arms=False)
    cam(S, (1.2, -9, 4.4), (0.6, -7.5, 4.2), (0, 0, 3.6), lens=36)


def pip_shoelace(S):
    yard_set()
    p = C.pip((0, 0, 0.2), face="happy")
    p.idle(1, S.n)
    B.point((0.4, -2.5, 0.8), 120, (0.3, 0.6, 1), 0.4)
    cam(S, (1.8, -3.6, 0.9), (1.0, -3.0, 0.8), (0.4, -0.3, 0.6), lens=42)


def pip_proud(S):
    yard_set()
    p = C.pip((0, 0, 0.2), face="smug")
    p.pose(1, "hips")
    B.sparkle_burst((0.43, -0.6, 0.6), 4, n=10, color="#8fc8ff", spread=1.5)
    cam(S, (-1.5, -8, 3.2), (-0.8, -7, 3.6), (0, 0, 3.0), lens=36)


def recess(S):
    yard_set()
    ball = sphere(0.7, (-6, -4, 0.9), mat("#c0592b"), name="ball")
    for f in range(1, S.n, 12):
        ball.location.z = 0.9; ball.keyframe_insert("location", frame=f)
        ball.location.z = 4.5; ball.keyframe_insert("location", frame=f + 6)
    kids = [C.townie(i, (x, y, 0.2), rot=r, face=fc) for i, (x, y, r, fc) in
            enumerate([(-9, -2, 30, "laugh"), (-3, -6, -40, "happy"), (6, -1, 10, "happy"), (10, -9, -20, "laugh")])]
    for k in kids:
        k.idle(1, S.n, amp=0.25, period=12)
    C.hero((2, -8, 0.2), colored=False, face="calm")
    C.pip((4.5, -7.5, 0.2), rot=-30, face="happy")
    cam(S, (-4, -30, 9), (4, -28, 8), (0, -4, 3), lens=28)


def crack_sound(S):
    yard_set()
    h = C.hero((0, 0, 0.2), colored=False, face="calm")
    h.faces((S.word("crack"), "surprised"))
    h.head_turn(S.word("crack"), 0, -30)
    cam(S, (0.8, -5.5, 5.3), (0.4, -4.8, 5.0), (0, 0, 5.0), lens=40)


def crack_dome(S):
    yard_set()
    B.world(top=(0.25, 0.27, 0.31), bottom=(0.6, 0.62, 0.66))
    rnd = random.Random(1)
    crack_m = mat("#ffffff", emit=7, wash=False)
    pts = [Vector((0, 60, 230))]
    for i in range(14):
        pts.append(pts[-1] + Vector((rnd.uniform(-14, 14), rnd.uniform(-10, 10), rnd.uniform(-1, 1))))
    for i in range(len(pts) - 1):
        seg = B._beam(pts[i], pts[i + 1], 2.4, crack_m, None)
        seg.scale = (1, 1, 0.001); seg.keyframe_insert("scale", frame=1 + i)
        seg.scale = (1, 1, 1); seg.keyframe_insert("scale", frame=3 + i)
    cam(S, (1, -14, 3), (1, -14, 3), (0, 60, 225), (0, 60, 229), 22, 26)


def rain_drop(S):
    yard_set(sky=STORM)
    h = C.hero((0, 0, 0.2), colored=False, face="surprised")
    h.head_turn(1, 0, -35)
    d = sphere(0.35, (0, -0.2, 30), mat("#cfe6ff", rough=0.05, alpha=0.6, wash=False), scale=(1, 1, 1.4), name="drop")
    d.keyframe_insert("location", frame=1)
    d.location.z = 6.3; d.keyframe_insert("location", frame=S.n)
    B._linear(d, "location")
    cam(S, (0.5, -4.5, 4.8), (0.3, -4.0, 4.6), (0, 0, 6.5), lens=34)


def rain_me(S):
    yard_set(sky=STORM)
    h = C.hero((0, -6, 0.2), colored=False, face="shocked")
    rain((0, -6), (3, 3), z=25, rate=500, lifetime=16, speed=-45)
    cyl(1.8, 0.02, (0, -6, 0.22), mat("#5a6c80", rough=0.05, wash=False), name="puddle")
    for i, (x, y) in enumerate([(-9, -2), (8, 0), (-5, -14), (11, -12)]):
        C.townie(i, (x, y, 0.2), rot=math.degrees(math.atan2(0 - x, -(-6 - y))), face="little_o")
    cam(S, (0, -26, 14), (0, -21, 8), (0, -6, 6), (0, -6, 4.5), lens=30)


def _wash_hero(S, h, z_from, z_to, f0=1, f1=None):
    h.wash_keys([(f0, z_from), (f1 or S.n, z_to)])


def wash_face(S):
    yard_set(sky=STORM)
    h = C.hero((0, 0, 0.2), colored=False, face="shocked")
    rain((0, 0), (3.4, 3.4), z=22, rate=500, lifetime=16)
    _wash_hero(S, h, 6.6, 4.1)
    cam(S, (0.4, -4.2, 5.5), (0.2, -3.6, 5.4), (0, 0, 5.1), lens=42)


def wash_shirt(S):
    yard_set(sky=STORM)
    h = C.hero((0, 0, 0.2), colored=False, face="little_o")
    rain((0, 0), (3.4, 3.4), z=22, rate=500, lifetime=16)
    _wash_hero(S, h, 4.3, 3.2)
    h.pose(1, "look_hands")
    cam(S, (0.8, -6, 4.4), (0.4, -5.2, 4.2), (0, 0, 3.8), lens=38)


def wash_tie(S):
    yard_set(sky=STORM)
    h = C.hero((0, 0, 0.2), colored=False, face="surprised")
    rain((0, 0), (3.4, 3.4), z=22, rate=500, lifetime=16)
    _wash_hero(S, h, 3.9, 2.9)
    cam(S, (0.3, -3.4, 3.8), (0.1, -2.8, 3.6), (0, 0, 3.5), lens=45)


def wash_full(S):
    yard_set(sky=STORM)
    h = C.hero((0, 0, 0.2), colored=False, face="surprised")
    h.wash_keys([(1, 3.0), (S.n, -0.6)])       # face, shirt and tie already washed
    rain((0, 0), (3.4, 3.4), z=22, rate=500, lifetime=16)
    h.pose(1, "look_hands")
    cam(S, (0.5, -9, 4.2), (0.5, -11, 4.0), (0, 0, 3.0), lens=36)


def pink_reveal(S):
    yard_set(sky=STORM)
    h = C.hero((0, 0, 0.2), colored=True, face="laugh")
    h.pose(1, "look_hands"); h.pose(6, "arms_up"); h.pose(S.n, "arms_up")
    B.sparkle_burst((0, -0.8, 3.5), 5, n=20, spread=4)
    B.point((0, -6, 6), 400, (1, 0.6, 0.85), 2)
    cam(S, (0.5, -14, 3.6), (0.5, -11, 4.2), (0, 0, 3.4), lens=36)


def kids_stare(S):
    yard_set()
    C.hero((0, -14, 0.2), colored=True, face="nervous")
    for i, (x, y, fc) in enumerate([(-4.5, -2, "shocked"), (0, 0, "surprised"), (4.5, -1, "shocked"), (-8, 3, "little_o"), (8, 2, "shocked")]):
        C.townie(i, (x, y, 0.2), rot=math.degrees(math.atan2(0 - x, -(-14 - y))), face=fc)
    cam(S, (3.5, -15, 6.2), (2.8, -13, 6.0), (0, 0, 4.4), lens=34)


def sandwich(S):
    yard_set()
    k = C.townie(2, (0, 0, 0.2), face="shocked")
    k.pose(1, "hold")
    sw = empty("sandwich", (0, -2.3, 2.6))
    box((1.0, 1.0, 0.18), (0, 0, 0), mat("#e8c98a"), sw); box((1.05, 1.05, 0.1), (0, 0, 0.14), mat("#5aa04a"), sw)
    box((1.0, 1.0, 0.18), (0, 0, 0.28), mat("#e8c98a"), sw)
    sw.keyframe_insert("location", frame=3); sw.keyframe_insert("rotation_euler", frame=3)
    sw.location = (0.2, -2.6, 0.35); sw.rotation_euler = (0.7, 0.3, 0.2)
    sw.keyframe_insert("location", frame=13); sw.keyframe_insert("rotation_euler", frame=13)
    k.pose(3, "hold"); k.pose(6, "idle")
    cam(S, (2.8, -12, 4.2), (2.0, -10.5, 4.0), (0, -1, 3.6), lens=34)


def sirens(S):
    yard_set(sky=NIGHT)
    c = C.inspector("insp", (0, 0, 0.2))
    V1.blink(V1.emis(c.siren.data.materials[0]), 1, S.n, 8)
    V1.flash_light((0, -3, 8), 1, S.n, period=8, energy=3000)
    cam(S, (0.4, -3.2, 6.6), (0.2, -2.6, 6.5), (0, 0, 6.5), lens=40)


def inspectors_run(S):
    yard_set(sky=NIGHT)
    ins = []
    for i in range(4):
        c = C.inspector("in%d" % i, (-12 + i * 3, 10, 0.2))
        c.walk(1, S.n, (-14 + i * 4, 12 - i, 0.2), (-4 + i * 4, -4 - i, 0.2), run=True)
        ins.append(c)
    V1.blink(V1.emis(ins[0].siren.data.materials[0]), 1, S.n, 8)
    V1.flash_light((0, 0, 10), 1, S.n, period=8, energy=4000)
    cam(S, (8, -20, 3), (4, -18, 3.5), (-6, 4, 4), (0, 0, 4), lens=28)


def pip_push(S):
    yard_set(sky=STORM)
    h = C.hero((15.5, -6.5, 0.2), rot=20, colored=True, face="scared")
    p = C.pip((13, -8.5, 0.2), rot=-50, face="determined")
    p.pose(1, "hold"); p.move(1, (13, -8.5, 0.2)); p.move(6, (14, -7.8, 0.2))
    h.move(1, (15.5, -6.5, 0.2)); h.move(8, (15.5, -1.5, 0.2))
    cam(S, (8, -16, 4), (9, -15, 4), (15, -5, 3), lens=30)


def pip_whisper(S):
    yard_set(sky=STORM)
    p = C.pip((0, 0, 0.2), face="determined")
    p.talk(S.w(0)[0], [0.6, 0.8, 0.6, 0.3, 0.1])
    cam(S, (0.5, -3.9, 4.7), (0.3, -3.4, 4.6), (0, 0, 4.4), lens=44)


def pip_caught(S):
    yard_set(sky=NIGHT)
    p = C.pip((0, 0, 0.2), face="scared")
    p.pose(1, "scared")
    for i, x in enumerate((-2.4, 2.4)):
        c = C.inspector("ic%d" % i, (x, 0.4, 0.2), rot=90 if x < 0 else -90)
        c.pose(1, "hold")
    p.move(1, (0, 0, 0.2)); p.move(S.n, (0, 0, 1.6))
    V1.flash_light((0, -4, 9), 1, S.n, period=10, energy=2500)
    cam(S, (1, -11, 4), (0.5, -9.5, 4.2), (0, 0, 3.6), lens=34)


def pip_scrub(S):
    yard_set(sky=NIGHT)
    p = C.pip((0, 0, 0.2), face="sad")
    c = C.inspector("isc", (2.6, -1.2, 0.2), rot=-60)
    brush(c.sh[1]); scrub_arm(c, S.n)
    bubbles((0.8, -0.8, 3.4), 2, 16)
    V1.flash_light((0, -4, 9), 1, S.n, period=10, energy=2000)
    cam(S, (1.5, -9, 4.2), (0.8, -7.5, 4.0), (0.6, 0, 3.2), lens=34)


def shoelace_grey(S):
    yard_set(sky=NIGHT)
    p = C.pip((0, 0, 0.2), face="sad", lace=None)
    lace = box((0.7, 0.08, 0.06), (0, -0.55, -1.78), mat("#1e88ff", invert=True), p.hip[1], name="lace")
    lace["wash_line"] = 0.0; lace.keyframe_insert('["wash_line"]', frame=1)
    lace["wash_line"] = 0.0; lace.keyframe_insert('["wash_line"]', frame=max(2, S.n // 3))
    lace["wash_line"] = 300.0; lace.keyframe_insert('["wash_line"]', frame=S.n * 2 // 3)
    B.point((0.6, -2.6, 1.5), 150, (1, 0.9, 0.95), 0.5)
    cam(S, (1.8, -3.6, 0.9), (1.0, -3.0, 0.8), (0.4, -0.3, 0.6), lens=42)


def hero_run_home(S):
    street_set()
    h = C.hero((-16, -9, 0.5), colored=True, face="scared")
    h.walk(1, S.n, (-16, -9, 0.5), (6, -9, 0.5), run=True)
    cam(S, (-14, -26, 4.5), (4, -26, 4.5), (-14, -9, 3.6), (6, -9, 3.6), lens=30)


def run_feet(S):
    street_set()
    h = C.hero((-6, -9, 0.5), colored=True, face="scared")
    h.walk(1, S.n, (-6, -9, 0.5), (6, -9, 0.5), run=True)
    cam(S, (-6, -17, 1.4), (6, -17, 1.4), (-6, -9, 1.2), (6, -9, 1.2), lens=34)


def run_back(S):
    street_set()
    h = C.hero((0, -10, 0.5), colored=True, face="scared")
    h.walk(1, S.n, (0, -12, 0.5), (0, 6, 0.5), run=True)
    for i in range(2):
        c = C.inspector("ib%d" % i, (-3 + i * 6, -30, 0.5))
        c.walk(1, S.n, (-3 + i * 6, -32, 0.5), (-3 + i * 6, -16, 0.5), run=True)
    cam(S, (0, -22, 5), (0, -8, 5), (0, -6, 3.6), (0, 10, 3.6), lens=30)


def home_door(S):
    home_set()
    m = C.mom((0, 0.6, 0), rot=0, face="scared")
    h = C.hero((0, -2.4, 0), rot=180, colored=True, face="nervous")
    m.pose(1, "idle"); m.pose(10, "hands_face"); m.root.location.z = -0.9
    cam(S, (8, -8, 6.2), (7, -7, 6.0), (0, -0.8, 4), lens=30)


def mom_secret1(S):
    home_set()
    m = C.mom((0, 0.6, -0.9), face="sad")
    C.hero((0, -2.4, 0), rot=180, colored=True, face="little_o")
    m.pose(1, "hands_face")
    m.talk(S.w(0)[0], [0.5, 0.7, 0.4, 0.6, 0.3] * max(1, S.n // 10))
    cam(S, (4.2, -8.8, 5.4), (3.8, -8.0, 5.3), (0, 0.6, 3.9), lens=42)


def mom_secret2(S):
    look(GREY, 1.4)
    box((40, 40, 0.2), (0, 0, -0.1), mat("#d9dee4"), name="floor")
    box((40, 0.5, 20), (0, 6, 10), mat("#c9d6de"), name="wall")
    crib = empty("crib", (0, 0, 0))
    box((4, 2.6, 0.3), (0, 0, 2.4), mat("#f0f0f0"), crib); [box((0.12, 0.12, 1.6), (x, y, 3.2), mat("#f0f0f0"), crib) for x in (-1.9, 1.9) for y in (-1.2, 1.2)]
    baby = C.townie(1, (0, 0, 2.2), face="asleep", scale=0.42); baby.colored(True)
    c = C.inspector("ib", (3.2, -1.5, 0), rot=-60)
    c.pose(1, "point")
    can = cyl(0.3, 1.0, (0, -1.0, -2.0), mat("#9e9e9e", metal=0.6), c.sh[1], rot=(90, 0, 0), name="spraycan")
    baby.wash_keys([(1, 1.5), (S.n, 5.2)])          # sprayed grey
    cam(S, (4, -9, 6), (3, -8, 5.6), (0, 0, 3), lens=34)


def bank_vats(S):
    vault_set(names=True)
    cam(S, (-6, 2, 7), (6, 3, 8), (-2, 12.6, 7), (4, 12.6, 9), lens=30)


def mom_secret3(S):
    home_set()
    m = C.mom((0, 0.6, -0.9), face="sad")
    m.pose(1, "hands_face")
    m.talk(S.w(0)[0], [0.4, 0.6, 0.3, 0.5] * max(1, S.n // 8))
    cam(S, (4.0, -8.4, 5.4), (3.6, -7.6, 5.3), (0, 0.6, 3.9), lens=44)


def blackout(S):
    look(NIGHT, 0.2)
    B.ground(300)
    hosp = empty("hospital", (0, 10, 0))
    box((24, 10, 14), (0, 0, 7), mat("#b6b9c0", rough=0.85), hosp)
    text("HOSPITAL", (0, -5.2, 12.2), mat("#dd2233", emit=2, wash=False), size=1.6, parent=hosp, extrude=0.05)
    wins = []
    for x in range(-9, 10, 3):
        for z in (3.5, 7.5):
            w = box((2, 0.3, 2), (x, 4.9, z), mat("#fff4c8", emit=3.0, wash=False), name="win")
            wins.append(w)
    m = wins[0].data.materials[0]
    e = m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    e.default_value = 3.0; e.keyframe_insert("default_value", frame=1)
    e.default_value = 3.0; e.keyframe_insert("default_value", frame=max(2, S.n // 3))
    e.default_value = 0.0; e.keyframe_insert("default_value", frame=S.n // 3 + 2)
    pink = B.point((3, 4.0, 3.5), 0, (1, 0.3, 0.7), 0.5)
    pink.data.energy = 0; pink.data.keyframe_insert("energy", frame=S.n // 3 + 3)
    pink.data.energy = 300; pink.data.keyframe_insert("energy", frame=S.n // 3 + 10)
    cam(S, (4, -22, 6), (2, -18, 6), (0, 10, 6), lens=30)


def knock(S):
    home_set()
    hinge = empty("hinge", (-3, 7.7, 0))
    box((6, 0.4, 9), (3, 0, 4.5), mat("#6e4b32"), hinge, name="door")
    sphere(0.3, (5.3, -0.4, 4.5), mat("#d4af37", metal=1, wash=False), hinge)
    for k in range(3):
        f = 2 + k * 6
        hinge.rotation_euler.z = 0; hinge.keyframe_insert("rotation_euler", frame=f)
        hinge.rotation_euler.z = math.radians(-1.5); hinge.keyframe_insert("rotation_euler", frame=f + 2)
        hinge.rotation_euler.z = 0; hinge.keyframe_insert("rotation_euler", frame=f + 4)
    B.point((0, 4, 8), 600, (1, 0.9, 0.8), 2)
    cam(S, (0.5, -3, 5), (0.2, -2.2, 5), (0, 7.5, 4.6), lens=34)


def prism_door(S):
    home_set()
    w = bpy.data.objects["backwall"]
    hole = box((6, 3, 9), (0, 8, 4.5), None, name="hole"); hole.hide_render = True; hole.hide_viewport = True
    mod = w.modifiers.new("hole", "BOOLEAN"); mod.object = hole; mod.operation = "DIFFERENCE"
    p = C.prism((0, 11.5, 0), face="smug"); p.colored(False)
    for x in (-4, 4):
        B.inspector("ins%d" % x, (x, 15, 0))
    B.ground(300, loc=(0, 0, -0.05))
    B.point((0, 10, 8), 1500, (1, 0.95, 0.9), 3)
    cam(S, (-3, -8, 4), (-2, -5, 4.4), (0, 9, 6), (0, 10, 6.5), lens=30)


def prism_point(S):
    home_set()
    p = C.prism((0, 3, 0), face="angry"); p.colored(False)
    p.pose(1, "idle"); p.pose(4, "point")
    p.talk(S.w(-3)[0], [0.6, 0.8, 0.7, 0.5, 0.3, 0.6, 0.4])
    cam(S, (0.4, -3.2, 6.0), (0.2, -2.6, 6.0), (0, 3, 6.6), lens=36)


def escape_squeeze(S):
    home_set()
    h = C.hero((-6, -2, 0), rot=90, colored=True, face="determined")
    h.root.scale = (0.9, 0.9, 0.7)
    h.walk(1, S.n, (-7, -1, 0), (7, -1, 0), run=False)
    import mocap as MC
    MC.play(h, MC.SNEAK, 1, S.n, offset=0, speed=1.3)       # Mixamo "Sneaking Forward"
    for x in (-1.6, 1.6):
        c = B.inspector("sq%d" % x, (x, -1, 0), rot=180)
        c.pose(1, "idle"); c.pose(S.n // 2, "hold")
    cam(S, (0, -12, 2), (2, -11, 2), (-2, -1, 2.2), (4, -1, 2.2), lens=30)


def stairs(S):
    look(STORM, 1.6)
    B.dome()
    for i in range(40):
        box((6, 3, 0.8), (0, i * 2.4, i * 1.6), mat("#9aa6b4", metal=0.5, rough=0.4, wash=False), name="step")
    h = C.hero((0, 0, 0.8), rot=180, colored=True, face="determined")
    for k in range(0, S.n + 1, 4):
        i = k / 4 * 0.7
        h.move(1 + k, (0, i * 2.4, 0.8 + i * 1.6))
    for k in range(1, S.n, 6):
        h.legs(k, 50 if (k // 6) % 2 else -50)
    cam(S, (14, -10, 3), (16, 2, 9), (0, 4, 5), (0, 16, 14), lens=26)


def lever_wide(S):
    top_set()
    C.hero((-1.0, -1.5, 0), rot=20, colored=True, face="determined")
    cam(S, (-12, -18, 8), (-9, -14, 6.5), (1, 3, 3.8), lens=28)


def lever_sign(S):
    top_set()
    cam(S, (4.0, -3.4, 6.6), (4.2, -2.6, 6.5), (4.4, 3.0, 6.4), lens=40)


def lever_pull(S):
    piv = top_set()
    h = C.hero((-0.5, 0.2, 0), rot=20, colored=True, face="determined")
    pull = 5
    h.pose(1, "pull")
    piv.keyframe_insert("rotation_euler", frame=pull)
    piv.rotation_euler.x = math.radians(40); piv.keyframe_insert("rotation_euler", frame=pull + 6)
    h.key_rot(h.sh[0], pull, -95); h.key_rot(h.sh[1], pull, -95)
    h.key_rot(h.sh[0], pull + 6, -20); h.key_rot(h.sh[1], pull + 6, -20)
    h.set_face(pull + 6, "laugh")
    B.sparkle_burst((0, 4, 3.5), pull + 6, n=16, color="#fff2a8", spread=4)
    V1.flash_light((0, 0, 10), pull + 6, S.n, color=(1, 0.2, 0.15), period=10, energy=3000)
    cam(S, (-7, -11, 5.5), (-5, -8, 4.5), (0.5, 3, 4), lens=30)


def dome_split(S):
    look(STORM, 1.4); B.ground(1400); V1.town_grid(3); B.street(160)
    halves = B.dome()
    for side, hv in zip((-1, 1), halves):
        hv.keyframe_insert("rotation_euler", frame=2); hv.keyframe_insert("location", frame=2)
        hv.rotation_euler.y = math.radians(side * 32); hv.location.x += side * 170
        hv.keyframe_insert("rotation_euler", frame=max(3, S.n)); hv.keyframe_insert("location", frame=max(3, S.n))
    cam(S, (0, -420, 170), (0, -380, 140), (0, 0, 90), lens=26)


def rain_city(S):
    look(STORM, 1.4); B.ground(1400); V1.town_grid(3); B.street(160)
    B.rain((0, 0), size=(360, 360), z=200, z0=40, rate=9000, lifetime=40, speed=-70, mesh_scale=5)
    cam(S, (0, -230, 110), (20, -200, 80), (0, 0, 20), lens=26)


def wash_town(S):
    street_set(sky=STORM, dome=False)
    rain((0, -4), (60, 40), z=30, rate=2500, lifetime=14, speed=-50)
    people = [C.townie(i, (x, y, 0.5), rot=r, face="little_o") for i, (x, y, r) in
              enumerate([(5, -5, -15), (-9, -2, 10), (9, 0, -10), (-2, 2, 0), (13, -9, -20), (-13, -9, 20)])]
    sc = bpy.context.scene
    sc["town_line"] = 100 - 30.0; sc.keyframe_insert('["town_line"]', frame=1)
    sc["town_line"] = 100 + 1.0; sc.keyframe_insert('["town_line"]', frame=S.n)
    for i, p in enumerate(people):
        p.set_face(S.n * 2 // 3 + i, "laugh"); p.pose(S.n * 2 // 3 + i, "cheer")
    cam(S, (0, -30, 12), (0, -26, 8), (0, -4, 5), (0, -4, 4.5), lens=28)


def green_eyes(S):
    street_set(sky=STORM, town=300, dome=False)
    rain((0, 0), (6, 6), rate=600)
    c = C.townie(0, (0, 0, 0.5), face="green_eyes")
    cam(S, (0.3, -5.2, 5.3), (0.1, -4.4, 5.25), (0, 0, 5.2), lens=50)


def red_hair(S):
    street_set(sky=STORM, dome=False)
    rain((0, 0), (6, 6), rate=600)
    c = C.townie(4, (0, 0, 0.5), face="laugh", hair="#ff2d2d")
    c.wash_keys([(1, 6.8), (S.n, 4.6)])
    cam(S, (1.2, -5, 6.0), (0.6, -4.2, 5.8), (0, 0, 5.4), lens=40)


def mom_yellow(S):
    street_set(sky=STORM, dome=False)
    rain((0, 0), (8, 8), rate=900)
    m = C.mom((0, 0, 0.5), face="laugh")
    m.wash_keys([(1, 6.5), (S.n, -0.5)])
    m.pose(1, "idle"); m.pose(8, "cheer")
    cam(S, (1, -11, 4.2), (0.5, -9, 4.0), (0, 0, 3.4), lens=36)


def pip_color(S):
    yard_set(sky=STORM, dome=False)
    rain((0, 0), (8, 8), rate=900)
    p = C.pip((0, 0, 0.2), face="laugh")
    p.wash_keys([(1, 5.6), (S.n * 2 // 3, -0.5)])
    p.pose(1, "idle"); p.pose(10, "cheer")
    cam(S, (1, -9, 3.8), (0.5, -7.5, 3.6), (0, 0, 3.0), lens=36)


def pip_shoelace_blue(S):
    yard_set(sky=BLUE, town=300, dome=False)
    p = C.pip((0, 0, 0.2), face="happy"); p.colored(True)
    B.sparkle_burst((0.43, -0.6, 0.6), 3, n=10, color="#8fc8ff", spread=1.5)
    cam(S, (1.8, -3.6, 0.9), (1.0, -3.0, 0.8), (0.4, -0.3, 0.6), lens=42)


def prism_rain(S):
    bank_set(sky=STORM, town=300)
    rain((0, 0), (14, 14), z=28, rate=900, lifetime=14, speed=-50)
    p = C.prism((0, 0, 1.2), face="shocked"); p.colored(False)
    p.pose(1, "look_hands")
    cam(S, (0, -16, 5), (0, -13, 5.6), (0, 0, 6), lens=32)


def prism_wash(S):
    bank_set(sky=STORM, town=300)
    rain((0, 0), (14, 14), z=28, rate=900, lifetime=14, speed=-50)
    p = C.prism((0, 0, 1.2), face="scared")
    p.wash_keys([(1, 9.2), (S.n, -0.5)])
    p.pose(1, "look_hands")
    cam(S, (0, -14, 6), (0, -11, 6.2), (0, 0, 5.5), lens=34)


def prism_grey(S):
    bank_set(sky=STORM, town=300)
    p = C.prism((0, 0, 1.2), face="sad"); p.colored(True)
    for i, (x, y) in enumerate([(-7, -6), (7, -7), (-3, -10)]):
        C.townie(i, (x, y, 0.5), rot=180 + (15 if x < 0 else -15), face="laugh").colored(True)
    cam(S, (0, -20, 5), (0, -15, 5.6), (0, 0, 5.4), lens=32)


def bank_umbrellas(S):
    bank_set(sky=BLUE, town=300)
    sign("UMBRELLAS\n2 FOR 1", (0, -3, 7.5), w=9, board="#ffe14d", ink="#1f3a93", size=1.0, post=False)
    for i, x in enumerate((-10, -6, 6, 10)):
        cyl(2.2, 0.6, (x, -3, 4.6), mat(RAINBOW[i * 2]), r2=0.1, name="umbrella")
        cyl(0.08, 4.4, (x, -3, 2.4), mat("#333333"))
    cam(S, (10, -34, 5), (6, -28, 4.5), (0, 6, 9), lens=30)


def prism_desk(S):
    vault_set()
    bpy.context.scene["town_line"] = 300
    p = C.prism((0, 4.6, 0), rot=0, face="side_eye", scale=1.1); p.colored(True)
    tag = box((1.2, 0.1, 0.5), (0.6, -0.55, 3.4), mat("#ffffff", wash=False), p.body)
    text("PRISM", (0, -0.07, 0), mat("#222222", wash=False), size=0.28, parent=tag, extrude=0.0)
    cyl(1.2, 0.3, (-2.4, 2.4, 6.2), mat("#ff2d55"), r2=0.05)
    cam(S, (1.5, -6, 5.4), (0.8, -5, 5.2), (0, 3.5, 5.4), lens=38)


def ending(S):
    street_set(sky=BLUE, town=300, dome=False, sun=3.4)
    for x in (-30, 30):
        B.tree(x, 10)
    h = C.hero((2.5, -9, 0.5), colored=True, face="happy")
    p = C.prism((-6, 1.5, 0.5), rot=20, scale=1.0, face="sad")
    p.colored(True)
    bench = box((8, 2, 0.4), (-6, 1.6, 2.0), mat("#8a6a4a"))
    V1.sit(p, 1)
    h.idle(1, S.n, arms=False)
    h.head_turn(S.word("grey"), 30, 0); h.head_turn(S.word("suits"), 0, 0)
    h.set_face(S.word("suits"), "wink"); h.pose(S.word("suits"), "thumb")
    for i, (x, y) in enumerate([(8, 2), (12, -3)]):
        C.townie(i + 2, (x, y, 0.5), rot=200, face="happy").idle(1, S.n, phase=i)
    cam(S, (4, -28, 6), (3, -21, 5.6), (-1, -3, 4), (0, -4, 4.3), lens=32)


def shot_funcs():
    import re
    from lines import SCRIPT
    ids = re.findall(r"\[(\w+)\]", " ".join(SCRIPT))
    g = globals()
    missing = [k for k in ids if k not in g]
    assert not missing, missing
    return {k: g[k] for k in ids}
