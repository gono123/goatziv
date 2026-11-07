"""Moon episode shots (scary): one function per [marker] in lines.py."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from ep_common import *

SKY_MOON = (-6, 90, 46)


def night_room(wall="#3a4660"):
    bedroom(True, wall=wall)


def sky_moon(r=14, eyes=False, f_eyes=None, mood="calm", loc=SKY_MOON):
    return moon(loc, r, eyes, f_eyes, mood)


def house_night(x=0, y=10, lit=True):
    h = B.house(x, y, w=12, d=8, h=8, wall="#9fa8c9")
    if lit:
        for wx in (-3.8, 3.8):
            box((2.0, 0.2, 2.0), (x + wx, y - 4.25, 4.4), mat("#ffe082", emit=2.5, wash=False))
    return h


def shades(ch):
    m = mat("#111111", rough=0.2, wash=False)
    for s in (-1, 1):
        box((0.46, 0.1, 0.3), (s * 0.27, -0.66, 0.86), m, ch.neck)
    box((0.2, 0.08, 0.08), (0, -0.66, 0.9), m, ch.neck)


def kids_on_moon(n=10, seed=1, face="laugh", y0=8):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        k = C.kid(i, (rnd.uniform(-12, 12), rnd.uniform(y0, y0 + 14), 0), rot=rnd.uniform(-60, 60), face=face)
        k.colored(True)
        out.append(k)
    return out


def ground_eyes(f_open, y=14, r=5):
    em = mat("#101010", wash=False)
    out = []
    for s in (-1, 1):
        e = sphere(r, (s * r * 1.5, y, 0.05), em, scale=(1, 0.6, 0.02))
        sphere(r * 0.3, (s * r * 1.5 + r * 0.3, y - r * 0.2, 0.12), mat("#ffffff", emit=3, wash=False), scale=(1, 0.6, 0.02))
        e.scale = (1, 0.02, 0.02); e.keyframe_insert("scale", frame=f_open)
        e.scale = (1, 0.6, 0.02); e.keyframe_insert("scale", frame=f_open + 10)
        out.append(e)
    return out


# ---------------------------------------------------------------- the world
def town(S):
    night_street()
    for x in (-24, 8):
        house_night(x, 30)
    wide(S, (0, 20, 14), 30, 4, lens=24, pan=4)


def full_moon(S):
    S2.look(NIGHT, 0.0, 300); colour(); stars()
    moon((0, 40, 10), 10)
    cam(S, (0, -4, 4), (0, -2, 6), (0, 40, 10), lens=40)


def beam_(S):
    night_street(moon_=False)
    sky_moon(10, loc=(0, 60, 70))
    house_night(0, 12)
    beam(0, 12, 70, 5, 8, f_on=S.word("shines"))
    wide(S, (0, 12, 12), 34, 5, lens=24, pan=3)


def float_(S):
    night_street(moon_=False)
    k = C.kid(2, (0, 0, 0.5), face="scared"); k.pose(1, "scared")
    beam(0, 0, 60, 2.6, 4)
    float_up(k, 3, S.n, 6)
    cam(S, (0, -14, 3), (0, -14, 6), (0, 0, 5), (0, 0, 9), lens=30)


def gone(S):
    night_room()
    curtains(None, "#5c6bc0")[0].location.x = -9.5
    box((8, 0.3, 6), (-5, 7.65, 10), mat("#0d1b3a", emit=0.2), name="nightwindow")
    beam(-5, 4, 30, 2.2, 3)
    cam(S, (2, -10, 6), (1, -8, 6), (-5, 4, 4), lens=30)


def curtains_(S):
    night_room("#4a5578")
    cs = curtains(None, "#3949ab")
    for c, s in zip(cs, (-1, 1)):
        c.location.x = -5 + s * 6.2; c.keyframe_insert("location", frame=1)
        c.location.x = -5 + s * 2.1; c.keyframe_insert("location", frame=12)
    m = C.mom((-5, 4.5, 0), rot=180, face="nervous"); m.colored(True); turn180(m); m.pose(1, "pull")
    cam(S, (2, -9, 6), (1, -7.5, 6), (-4, 4, 6), lens=30)


def foil(S):
    night_room("#4a5578")
    box((8.4, 0.3, 6.4), (-5, 7.5, 10), mat("#cfd8dc", metal=1.0, rough=0.25, wash=False), name="foil")
    d = dad((-3.6, 5.4, 0), rot=180, face="determined"); turn180(d); d.pose(1, "hold")
    push(S, (-4, 4, 6), 14, 30)


def grandma_(S):
    room(DARK, wall="#5d4c3e", floor="#3e3226", light=0.2)
    B.point((0, -2, 9), 300, (1, 0.8, 0.6), 2)
    box((10, 4, 1.2), (0, 2, 0.6), mat("#6d4c41"))
    g = C.grandma((0, 1.5, 1.2), face="asleep"); g.colored(True); V1.sit(g, 1)
    shades(g)
    push(S, (0, 1, 4.6), 10, 34)


def sign_rule(S):
    night_street()
    sign("NEVER LOOK\nAT THE MOON", (0, 0, 6.5), w=11, size=0.95)
    B.point((0, -4, 8), 600, (1, 0.95, 0.9), 2)
    cam(S, (2, -13, 4.5), (-1, -11, 5), (0, 0, 6.6), lens=34)


def rule_look(S):
    night_street()
    k = C.kid(1, (0, 0, 0.5), face="scared"); k.pose(1, "hands_face")
    push(S, (0, 0, 4.4), 9, 36)


def moon_eye(S):
    S2.look(NIGHT, 0.0, 300); colour(); stars()
    moon((0, 30, 10), 10, eyes=True, f_eyes=S.word("looks"))
    cam(S, (0, -6, 9), (0, -2, 9.5), (0, 30, 10), lens=40)


def hero(S):
    night_room()
    h = C.hero((0, 0, 0), face="nervous"); h.pose(1, "shield")
    push(S, (0, 0, 4.6), 10, 34)


def hero_bed(S):
    night_room()
    h = C.hero((-6.5, 3, 1.6), rot=0, face="scared"); V1.sit(h, 1)
    box((6, 4.8, 3.6), (-6.5, 2.6, 3.2), mat("#7e57c2"), name="blanket_up")
    push(S, (-6.5, 2, 5), 10, 34)


def pip_(S):
    yard()
    p = C.pip((0, 0, 0.2), face="smug", lace=None); p.colored(True); p.pose(1, "hips")
    push(S, (0, 0, 4), 9, 36)


def pip_laugh(S):
    yard()
    p = C.pip((0, 0, 0.2), face="laugh", lace=None); p.colored(True); p.pose(1, "point_up")
    sphere(1.2, (5, 20, 26), mat("#9e9e9e", rough=1))
    push(S, (0, 0, 4), 11, 34)


# ---------------------------------------------------------------- pip
def pip_window(S):
    night_room()
    curtains(S.word("opened"))
    p = C.pip((-5, 5.2, 0), rot=180, face="smug", lace=None); p.colored(True); turn180(p); p.pose(1, "pull")
    cam(S, (1, -8, 6), (0, -6.5, 6), (-4, 5, 6), lens=30)


def pip_look(S):
    night_room()
    p = C.pip((0, 0, 0), face="little_o", lace=None); p.colored(True)
    p.head_turn(1, 0, -15)
    B.point((0, -3, 7), 800, MOONLIGHT, 1)
    push(S, (0, 0, 4.2), 6, 40)


def pip_beam(S):
    night_street(moon_=False)
    sky_moon(10, loc=(0, 60, 70))
    house_night(0, 12)
    beam(0, 12, 70, 5, 8, f_on=2)
    wide(S, (0, 12, 10), 30, 4, lens=26, pan=2)


def pip_float(S):
    night_street(moon_=False)
    house_night(0, 12)
    beam(0, 6, 60, 3, 5)
    p = C.pip((0, 6, 4), face="scared", lace=None); p.colored(True); p.pose(1, "scared")
    float_up(p, 1, S.n, 7)
    cam(S, (4, -10, 4), (3, -9, 7), (0, 6, 6), (0, 6, 10), lens=30)


def pip_up(S):
    night_street(moon_=False)
    sky_moon(10, loc=(0, 70, 60))
    p = C.pip((0, 10, 14), face="scared", lace=None); p.colored(True); p.pose(1, "arms_out")
    float_up(p, 1, S.n, 12)
    beam(0, 10, 60, 3, 5)
    cam(S, (0, -16, 2), (0, -16, 3), (0, 10, 16), (0, 10, 26), lens=28)


def pip_dot(S):
    S2.look(NIGHT, 0.0, 300); colour(); stars()
    moon((0, 80, 40), 12)
    p = C.pip((0, 60, 14), face="scared", lace=None); p.colored(True)
    p.root.scale = (0.6,) * 3
    float_up(p, 1, S.n, 18, wobble=False)
    cam(S, (0, -4, 4), (0, -4, 5), (0, 80, 30), lens=34)


def mom(S):
    room(DARK, wall="#6d5a7a", light=0.4)
    B.point((0, -2, 10), 500, (1, 0.85, 0.7), 2)
    m = C.mom((-1.2, 0.5, 0), rot=-20, face="sad"); m.colored(True)
    h = C.hero((1.2, -0.2, 0), rot=20, face="sad")
    push(S, (0, 0, 4.4), 14, 30)


def nobody(S):
    night_room()
    h = C.hero((-5, 4.8, 0), rot=180, face="sad"); turn180(h)
    curtains(None, "#3949ab")[0].location.x = -9.5
    sky_moon(6, loc=(-5, 40, 16))
    cam(S, (2, -8, 5), (1, -6.5, 5.5), (-5, 5, 6), lens=30)


def month(S):
    night_room()
    h = C.hero((-6.5, 3, 1.6), face="nervous"); V1.sit(h, 1)
    box((6, 4.8, 1.6), (-6.5, 2.6, 2.4), mat("#7e57c2"))
    text("3:12", (6, 6.8, 6), mat("#ff5252", emit=3, wash=False), size=1.0)
    push(S, (-5, 2, 4.8), 12, 32)


def calendar(S):
    room(wall="#d7ccc8")
    cal = box((6, 0.2, 7), (0, 7.6, 8), mat("#ffffff"), name="cal")
    text("NOVEMBER", (0, 7.4, 10.8), mat("#c62828", wash=False), size=0.7)
    for k in range(20):
        box((0.9, 0.1, 0.7), (-2.4 + (k % 5) * 1.2, 7.45, 9.4 - (k // 5) * 1.0), mat("#eeeeee"))
    sphere(0.32, (1.2, 7.35, 7.4), mat("#fff59d", emit=1.5, wash=False), scale=(1, 0.3, 1))
    for k in range(16):
        a = k / 16 * math.tau
        sphere(0.07, (1.2 + math.cos(a) * 0.6, 7.3, 7.4 + math.sin(a) * 0.5), mat("#d50000", wash=False))
    cam(S, (0, -1, 8.4), (0.4, 1.5, 7.8), (0, 7.6, 8.4), (1.2, 7.6, 7.4), lens=36)


# ---------------------------------------------------------------- hero goes up
def hero_window(S):
    night_room()
    curtains(S.word("opened"))
    h = C.hero((-5, 5.2, 0), rot=180, face="determined"); turn180(h); h.pose(1, "pull")
    cam(S, (1, -8, 6), (0, -6.5, 6), (-4, 5, 6), lens=30)


def hero_look(S):
    night_room()
    h = C.hero((0, 0, 0), face="determined")
    h.head_turn(1, 0, -15)
    B.point((0, -3, 7), 900, MOONLIGHT, 1)
    push(S, (0, 0, 4.8), 6, 40)


def moon_eye2(S):
    S2.look(NIGHT, 0.0, 300); colour(); stars()
    moon((0, 24, 10), 10, eyes=True, f_eyes=2)
    cam(S, (0, -4, 9), (0, 0, 9.5), (0, 24, 10), lens=44)


def hero_beam(S):
    night_room()
    h = C.hero((0, 0, 0), face="shocked"); h.pose(1, "shield")
    beam(0, 0, 30, 2.4, 3.2, f_on=2)
    push(S, (0, 0, 4.4), 13, 30)


def hero_float(S):
    night_room()
    h = C.hero((0, 0, 0.1), face="scared"); h.pose(1, "arms_out")
    beam(0, 0, 30, 2.4, 3.2)
    float_up(h, 2, S.n, 4)
    cam(S, (0, -12, 3), (0, -12, 5), (0, 0, 4), (0, 0, 7), lens=30)


def hero_up(S):
    night_street(moon_=False)
    house_night(0, 12)
    beam(0, 12, 70, 3, 5)
    h = C.hero((0, 12, 9), face="scared"); h.pose(1, "arms_out")
    float_up(h, 1, S.n, 12)
    cam(S, (8, -10, 6), (8, -10, 10), (0, 12, 12), (0, 12, 20), lens=28)


def hero_stars(S):
    space(150)
    h = C.hero((0, 0, 0), face="surprised"); h.pose(1, "arms_out")
    float_up(h, 1, S.n, 6)
    moon((4, 60, 18), 14)
    cam(S, (0, -12, -2), (0, -12, 2), (0, 0, 4), (0, 0, 8), lens=30)


# ---------------------------------------------------------------- the moon
def moon_land(S):
    moon_surface()
    h = C.hero((0, 0, 6), face="surprised"); h.pose(1, "arms_out")
    float_up(h, 1, min(S.n, 18), -6, wobble=False)
    h.pose(min(S.n, 18), "idle")
    wide(S, (0, 0, 3), 16, 4, lens=30, pan=4)


def dark(S):
    moon_surface()
    h = C.hero((0, 0, 0), face="scared")
    cam(S, (0, -40, 18), (0, -36, 16), (0, 0, 2), lens=30)


def voices(S):
    moon_surface()
    h = C.hero((0, 0, 0), face="little_o")
    h.head_turn(4, 40, 0)
    push(S, (0, 0, 4.6), 8, 36)


def kids(S):
    moon_surface()
    cyl(14, 0.4, (0, 16, -0.1), mat("#8f8c84", rough=1), r2=12)
    ks = kids_on_moon(10, 2)
    for i, k in enumerate(ks[:5]):
        k.move(1, tuple(k.root.location)); k.move(8 + i, (k.root.location.x, k.root.location.y, 2.5)); k.move(18 + i, tuple(k.root.location))
    wide(S, (0, 14, 3), 24, 9, lens=28)


def pip_found(S):
    moon_surface()
    p = C.pip((0, 0, 0), face="happy", lace=None); p.colored(True)
    kids_on_moon(4, 5, y0=10)
    push(S, (0, 0, 4), 11, 32)


def pip_hi(S):
    moon_surface()
    p = C.pip((0, 0, 0), face="laugh", lace=None); p.colored(True); p.pose(2, "wave")
    push(S, (0, 0, 4), 8, 36)


def moon_face(S):
    moon_surface()
    ground_eyes(S.word("eyes") - 6)
    h = C.hero((-1.6, -2, 0), face="scared"); h.pose(1, "scared")
    p = C.pip((1.6, -2, 0), face="scared", lace=None); p.colored(True)
    cam(S, (0, -16, 12), (0, -15, 16), (0, 8, 0), lens=26)
    B.shake(bpy.context.scene.camera, 1, S.word("eyes"), 0.15)


def moon_sad(S):
    space(120)
    moon((0, 40, 0), 12, eyes=True, mood="sad")
    cam(S, (0, -6, 0), (0, -2, 0.5), (0, 40, 0), lens=36)


def lonely(S):
    space(120)
    moon((0, 30, 0), 12, eyes=True, mood="sad")
    cam(S, (3, 0, -1), (2, 4, 0), (0, 30, 0), lens=36)


def hero_idea(S):
    moon_surface()
    h = C.hero((0, 0, 0), face="determined")
    push(S, (0, 0, 4.8), 7, 38)


def deal(S):
    moon_surface()
    h = C.hero((0, 0, 0), face="determined"); h.pose(1, "point_up")
    kids_on_moon(6, 7, face="surprised", y0=4)
    cam(S, (4, -12, 3), (3, -10, 3), (0, 2, 5), lens=28)


def sleepover(S):
    moon_surface()
    for i, x in enumerate(range(-8, 9, 4)):
        box((2.4, 5, 0.6), (x, 6, 0.3), mat(["#ef5350", "#42a5f5", "#66bb6a", "#ffca28", "#ab47bc"][i % 5]))
        box((1.6, 1.0, 0.5), (x, 8.2, 0.8), mat("#ffffff"))
    ks = kids_on_moon(5, 9, face="happy", y0=1)
    for k in ks:
        k.pose(1, "cheer")
    wide(S, (0, 6, 2), 18, 8, lens=28)


def moon_smile(S):
    space(120)
    moon((0, 40, 0), 12, eyes=True, mood="smile")
    B.sparkle_burst((0, 26, 0), 3, n=16, color="#fff59d", spread=6)
    cam(S, (0, -6, 0), (0, -2, 0), (0, 40, 0), lens=36)


def beam_down(S):
    street(DUSK, 1.8)
    for i, x in enumerate((-6, 0, 6)):
        beam(x, 0, 60, 2.2, 3)
        k = C.kid(i, (x, 0, 12), face="happy") if i != 1 else C.pip((x, 0, 12), face="happy", lace=None)
        k.colored(True)
        float_up(k, 1, S.n, -11.5, wobble=False)
    wide(S, (0, 0, 7), 28, 6)


def town_back(S):
    street(DUSK, 2.4)
    for i, x in enumerate((-5, 3)):
        a = C.adult(i, (x, 0.8, 0.5), face="sad"); a.pose(1, "hands_face")
        k = C.kid(i + 3, (x + 1.8, -0.6, 0.5), rot=-60, face="happy")
    m = C.mom((-1, 2.5, 0.5), face="sad"); m.colored(True); m.pose(1, "hands_face")
    h = C.hero((0.6, 1.2, 0.5), face="happy")
    wide(S, (0, 0, 4.5), 20, 6, pan=4)


def ending(S):
    S2.look(NIGHT, 0.0, 300); colour(); stars()
    moon((0, 40, 6), 12, eyes=True, mood="smile")
    for i, x in enumerate((-4, 0, 4)):
        k = (C.hero((x, 27.6, 18), face="happy") if i == 1 else C.kid(i, (x, 27.6, 17.4), face="laugh"))
        k.pose(1, "wave")
    cam(S, (0, -6, 4), (0, -3, 5), (0, 40, 10), lens=34)


def ending_sun(S):
    street(DAY, 3.4)
    root = empty("sun", (6, 70, 30))
    sphere(9, (0, 0, 0), mat("#ffb300", emit=3.0, wash=False), root, seg=32)
    for s in (-1, 1):
        sphere(1.4, (s * 3.0, -8.6, 1.6), mat("#3e2723", wash=False), root, scale=(1, 0.3, 1.3))
    for k in range(7):
        t = (k - 3) / 3
        sphere(0.45, (t * 2.8, -8.7, -2.4 - (1 - t * t) * 1.0), mat("#3e2723", wash=False), root, scale=(1, 0.3, 1))
    h = C.hero((0, 0, 0.5), face="shocked")
    h.head_turn(1, 0, -15)
    h.set_face(S.word("too"), "nervous")
    cam(S, (1.5, -9, 3), (1.2, -8, 3.2), (0.5, 0, 5), (2, 20, 12), lens=30)


ALIASES = {"beam": beam_, "float": float_, "curtains": curtains_, "grandma": grandma_, "pip": pip_, "mom": mom, "hero": hero}


def shot_funcs():
    return shot_table(globals(), ALIASES)
