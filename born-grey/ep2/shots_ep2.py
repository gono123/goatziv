"""Episode 2 shots ("Whoever Ties Your Tie Controls You"): one function per marker in lines.py.
Reuses the Born Grey toolkit (../blib.py, ../v2/cast.py, ../v2/shots2.py helpers, ../v2/mocap.py)."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for p in (ROOT, os.path.join(ROOT, "v2"), HERE):
    if p not in sys.path:
        sys.path.insert(0, p)
import bpy
from mathutils import Vector
import blib as B
from blib import mat, box, cyl, sphere, text, empty
import shots as V1
import cast as C
import shots2 as S2
from shots2 import Shot, cam, sign, BLUE, NIGHT

DAY = BLUE
EERIE = dict(top=(0.30, 0.36, 0.42), bottom=(0.62, 0.66, 0.68))   # the controlled school: cold, flat light
TIE_GLOW = "#ffd23f"


def colour():
    bpy.context.scene["town_line"] = 300.0      # this world is in full colour


def day_street():
    S2.look(DAY, 3.2, 300); B.ground(600); B.street(160); colour()


def yard(sky=DAY, sun=3.0):
    S2.look(sky, sun, 300); V1.school(30); colour()


def room(sky=DAY, wall="#d8cbb8", floor="#9a7a5a", light=1.0):
    S2.look(sky, light, 300); V1.room(wall=wall, floor=floor); colour()


def hall(sky=EERIE):
    """Assembly hall: a stage with red curtains and rows of chairs."""
    S2.look(sky, 0.8, 300); colour()
    box((60, 70, 0.2), (0, 0, -0.1), mat("#8a6a4a", rough=0.6), name="floor")
    box((60, 0.5, 26), (0, 22, 13), mat("#6b4f8f"), name="backwall")
    box((24, 8, 2.4), (0, 17, 1.2), mat("#5a3a22"), name="stage")
    for x in (-10, 10):
        box((6, 0.6, 18), (x, 19.5, 11), mat("#9e1b2f", rough=0.8), name="curtain")
    box((26, 0.6, 3), (0, 19.5, 19.5), mat("#9e1b2f", rough=0.8), name="valance")
    text("PICTURE DAY", (0, 21.5, 15), mat(TIE_GLOW, emit=1.5), size=2.2, extrude=0.1)
    for row in range(5):
        for k in range(9):
            x, y = -16 + k * 4, 6 - row * 4.4
            box((2.6, 2.4, 0.4), (x, y, 1.8), mat("#3d4b5c"), name="seat")
            box((2.6, 0.3, 2.4), (x, y + 1.2, 3.0), mat("#3d4b5c"), name="back")
    B.point((0, 8, 16), 2500, (1, 0.85, 0.6), 4)


def seated_kids(rows=4, cols=9, face="hypno", skip=(), lift=0.4):
    kids = []
    for row in range(rows):
        for k in range(cols):
            if (row, k) in skip:
                continue
            x, y = -16 + k * 4, 6 - row * 4.4
            c = C.kid(row * cols + k, (x, y - 0.4, lift), rot=180, face=face)
            c.root.rotation_euler.z = math.radians(180)
            V1.sit(c, 1)
            kids.append(c)
    return kids


def threads(src, kids, f_on=1, color=TIE_GLOW):
    """Glowing strings from Knotley's tie knot to every kid's tie knot."""
    bpy.context.view_layer.update()
    a = src.tie_objs[0].matrix_world.translation
    m = mat(color, emit=4.0, wash=False)
    for k in kids:
        if not getattr(k, "tie_objs", None):
            continue
        b = k.tie_objs[0].matrix_world.translation
        o = B._beam(a, b, 0.05, m, None)
        o.scale = (1, 1, 0.001); o.keyframe_insert("scale", frame=f_on)
        o.scale = (1, 1, 1); o.keyframe_insert("scale", frame=f_on + 6)


def tug(ch, f, n=2):
    """Knotley pulls his own tie: arm yanks down, tie blade swings."""
    for k in range(n):
        ch.key_rot(ch.sh[1], f + k * 10, -40, 0, 0); ch.key_rot(ch.sh[1], f + k * 10 + 4, -15, 0, 0)
        if getattr(ch, "tie_pivot", None):
            ch.tie_pivot.rotation_euler = (math.radians(-25), 0, 0); ch.tie_pivot.keyframe_insert("rotation_euler", frame=f + k * 10 + 4)
            ch.tie_pivot.rotation_euler = (0, 0, 0); ch.tie_pivot.keyframe_insert("rotation_euler", frame=f + k * 10 + 9)


def untie(ch, f):
    """The tie comes loose: the blade drops away and the knot disappears."""
    if not getattr(ch, "tie_objs", None):
        return
    knot, blade = ch.tie_objs
    for o in (knot, blade):
        o.hide_render = False; o.keyframe_insert("hide_render", frame=f - 1)
        o.hide_render = True; o.keyframe_insert("hide_render", frame=f + 8)
    ch.tie_pivot.keyframe_insert("rotation_euler", frame=f)
    ch.tie_pivot.rotation_euler = (math.radians(70), 0, math.radians(30)); ch.tie_pivot.keyframe_insert("rotation_euler", frame=f + 7)


# ============================================================================ shots

def town(S):
    day_street()
    for i, (x, y) in enumerate([(-8, -10), (-2, -11), (5, -9), (11, -12)]):
        c = C.adult(i, (x, y, 0.5), face="calm")
        c.walk(1, S.n + 10, (x - 3, y, 0.5), (x + 5, y, 0.5), stride=10)
    cam(S, (-6, -34, 9), (4, -30, 7), (0, -8, 4.5), lens=28)


def tie_close(S):
    day_street()
    c = C.adult(1, (0, 0, 0.5), face="calm")
    cam(S, (0.3, -4.2, 4.2), (0.15, -3.4, 4.1), (0, 0, 3.8), lens=42)


def remote(S):
    day_street()
    c = C.adult(2, (0, 0, 0.5), face="side_eye")
    r = box((0.9, 0.3, 1.8), (0, -0.6, -2.3), mat("#222222", rough=0.4), c.sh[1], name="remote")
    for k, z in enumerate((0.5, 0.1, -0.3)):
        cyl(0.13, 0.08, (0, -0.17, z), mat(["#e53935", "#43a047", "#1e88e5"][k], emit=1.5), r, rot=(90, 0, 0))
    c.pose(1, "point")
    cam(S, (2, -9, 4.8), (1.2, -7.5, 4.6), (0.3, 0, 3.8), lens=36)


def office():
    room(wall="#c9d3dc", floor="#6b6b6b")
    box((8, 3.5, 0.3), (2, 2, 3.2), mat("#5d4632"), name="desk")
    for x in (-1.5, 5.5):
        box((0.4, 3, 3.2), (x, 2, 1.6), mat("#5d4632"))
    box((2.6, 0.2, 1.8), (3, 2.6, 4.4), mat("#222222", rough=0.3), name="monitor")


def dad_boss(S):
    office()
    dad = C.adult(3, (-1.2, -1, 0), rot=20, face="nervous", tie="#2e7d32")
    boss = C.adult(0, (2.4, -2.0, 0), rot=-70, face="smug", top="#2b2b2b", pants="#1a1a1a", tie="#2e7d32")
    boss.pose(1, "point")
    cam(S, (1.5, -11, 5.4), (1.0, -9.6, 5.2), (0.5, -1.5, 4.4), lens=32)

def dad_yes(S):
    office()
    B.world(top=(0.06, 0.06, 0.16), bottom=(0.18, 0.16, 0.28))
    dad = C.adult(3, (0, -1, 0), face="asleep", tie="#2e7d32")
    V1.sit(dad, 1)
    clock = text("11:59 PM", (5, 7.5, 12), mat("#ff5252", emit=3), size=1.4)
    dad.head_turn(1, 0, 25)
    cam(S, (1.5, -9, 5.6), (0.8, -7.5, 5.2), (0, -1, 3.8), lens=36)


def grandma_tie(S):
    room(wall="#e6d5c3")
    g = C.Side("grandma", (0, 0.5, 0), 0, dict(skin_key="pale", face="smug", skin="#fae2c8", top="#b5838d", pants="#6d597a",
                                                 shoes="#3a3a3a", hair="#e8e8e8", hair_style="bun", tie="#7b1fa2"), scale=0.95)
    g.colored(True); g.pose(1, "hips")
    frame_ = box((3.4, 0.2, 2.6), (5, 7.6, 10), mat("#8d6e63"), name="frame")
    text("1976", (0, -0.12, -0.9), mat("#ffffff", emit=1), size=0.5, parent=frame_, extrude=0.0)
    cam(S, (-1.2, -9, 5.4), (-0.6, -7.6, 5.2), (0, 0.5, 4.3), lens=36)


def grandma_no(S):
    room(wall="#e6d5c3")
    g = C.Side("grandma", (-1.5, 0.5, 0), 20, dict(skin_key="pale", face="angry", skin="#fae2c8", top="#b5838d", pants="#6d597a",
                                                    shoes="#3a3a3a", hair="#e8e8e8", hair_style="bun", tie="#7b1fa2"), scale=0.95)
    g.colored(True); g.pose(1, "wag")
    doc = C.adult(2, (3.2, -1.2, 0), rot=-60, face="nervous", top="#ffffff", pants="#90a4ae", tie="#0288d1")
    doc.pose(1, "hold")
    cam(S, (1, -11, 5), (0.5, -9.5, 4.8), (0.6, 0, 4), lens=34)


def wedding(S):
    S2.look(DAY, 3.2, 300); B.ground(300, "#7fbf6a"); colour()
    for i, c_ in enumerate(("#f8bbd0", "#ffffff", "#f48fb1")):
        B.arch(5.6 - i * 0.5, 5.2 - i * 0.5, (0, 3 + i * 0.02, 0.2), mat(c_, emit=0.3), None)
    a = C.adult(0, (-1.3, 0, 0.2), rot=60, face="happy", top="#ffffff", pants="#ffffff", tie="#f06292")
    b = C.adult(4, (1.3, 0, 0.2), rot=-60, face="happy", top="#212121", pants="#212121", tie="#f06292")
    a.pose(1, "hands_face"); b.pose(1, "hands_face")
    B.sparkle_burst((0, -0.5, 5), 4, n=12, color="#ffd1ea")
    cam(S, (0, -12, 4.6), (0, -10, 4.8), (0, 0, 4), lens=34)


def married(S):
    room(wall="#ffe0b2")
    a = C.adult(0, (-1.6, 0, 0), face="happy", top="#ffffff", pants="#ffffff", tie="#f06292")
    b = C.adult(4, (1.6, 0, 0), face="happy", top="#212121", pants="#212121", tie="#f06292")
    for c in (a, b):
        f = 1
        while f < S.n:                      # nod together
            c.head_turn(f, 0, 12); c.head_turn(f + 5, 0, -4); f += 10
    cam(S, (0, -10, 5.4), (0, -8.6, 5.2), (0, 0, 4.6), lens=36)


def sign_rule(S):
    day_street()
    sign("NEVER LET A\nSTRANGER TOUCH\nYOUR TIE", (0, 0, 6.5), w=12, size=0.85)
    cam(S, (2, -13, 4.5), (-1, -11, 5), (0, 0, 6.3), lens=34)


def stranger(S):
    day_street()
    k = C.adult(1, (0, 0, 0.5), face="scared")
    s_ = C.adult(5, (2.2, -1.6, 0.5), rot=-55, face="smug", top="#263238", pants="#263238", tie="#000000")
    s_.pose(1, "point")
    k.pose(1, "scared")
    cam(S, (-1.5, -9, 4.8), (-0.8, -8, 4.6), (0.6, -0.5, 4.2), lens=34)


def hero_mirror(S):
    room(wall="#d0e3f0")
    box((3.4, 0.3, 6), (0, 2.8, 4.6), mat("#cfd8dc", metal=1.0, rough=0.05, wash=False), name="mirror")
    h = C.hero((0, -0.5, 0), rot=0, face="determined")
    h.pose(1, "hands_face")
    cam(S, (1.2, -7.5, 5.6), (0.8, -6.5, 5.4), (0, -0.5, 4.6), lens=36)


def hero_knot(S):
    room(wall="#d0e3f0")
    h = C.hero((0, 0, 0), face="smug")
    h.pose(1, "hips")
    B.sparkle_burst((0, -0.7, 3.8), 4, n=10, color="#ffd1ea", spread=1.5)
    cam(S, (0.4, -5.6, 4.6), (0.2, -4.8, 4.4), (0, 0, 4.0), lens=40)


def mom_teach(S):
    room()
    m = C.mom((1.5, -0.3, 0), rot=60, face="happy"); m.colored(True)
    h = C.hero((-1.4, -0.3, 0), rot=-60, face="happy", scale=None) if False else C.hero((-1.4, -0.3, 0), rot=-60, face="happy")
    h.root.scale = (0.7, 0.7, 0.7)
    m.pose(1, "hands_face")
    cam(S, (0, -10, 4.6), (0, -8.6, 4.4), (0, 0, 3.6), lens=34)


def mom_rule(S):
    room()
    m = C.mom((0, 1, 0), face="determined"); m.colored(True)
    m.pose(1, "wag")
    cam(S, (1.2, -4.6, 5.6), (0.8, -4.0, 5.5), (0, 1, 5.2), lens=42)


def pip_intro(S):
    yard()
    p = C.pip((0, 0, 0.2), face="happy", lace=None); p.colored(True)
    p.pose(1, "wave")
    cam(S, (1.2, -9, 4.4), (0.6, -7.5, 4.2), (0, 0, 3.6), lens=36)


def pip_mess(S):
    yard()
    p = C.pip((0, 0, 0.2), face="nervous", lace=None); p.colored(True)
    # a tangled spaghetti tie: a bundle of twisted red strands on his chest
    rnd = random.Random(4)
    m = mat("#c62828", rough=0.5)
    pts = [Vector((0, -0.55, 3.8))]
    for i in range(12):
        pts.append(pts[-1] + Vector((rnd.uniform(-0.35, 0.35), -0.02, rnd.uniform(-0.25, 0.1))))
    for a, b in zip(pts, pts[1:]):
        B._beam(a, b, 0.13, m, p.body)
    cam(S, (0.6, -6.4, 4.4), (0.3, -5.6, 4.2), (0, 0, 3.6), lens=38)


def new_principal(S):
    yard(EERIE, 2.0)
    k = C.knotley((0, 4, 0.2), face="happy")
    k.walk(1, S.n, (0, 10, 0.2), (0, 2, 0.2), stride=12)
    for i, (x, y) in enumerate([(-6, -4), (6, -5)]):
        C.kid(i, (x, y, 0.2), rot=180, face="little_o").root.rotation_euler.z = math.radians(180)
    cam(S, (0, -16, 2.2), (0, -14, 2.0), (0, 4, 6), lens=30)


def knotley_smile(S):
    yard(EERIE, 2.0)
    k = C.knotley((0, 0, 0.2), face="happy")
    cam(S, (0.3, -5.2, 7.6), (0.15, -4.4, 7.5), (0, 0, 7.3), lens=44)


def picture_day(S):
    yard(EERIE, 2.0)
    sign("PICTURE DAY\nFREE PERFECT KNOTS", (6, -2, 7), w=12, board="#fff8e1", ink="#6a1b9a", size=0.85)
    k = C.knotley((-3, 0, 0.2), rot=20, face="happy")
    k.pose(1, "point")
    cam(S, (-1, -18, 5.5), (1, -16, 5.5), (1, 0, 5.5), lens=30)


def knotley_offer(S):
    yard(EERIE, 2.0)
    k = C.knotley((0, 0, 0.2), face="wink")
    k.pose(1, "arms_out")
    cam(S, (0.6, -8, 6), (0.3, -7, 5.8), (0, 0, 6.4), lens=34)


def line_up(S):
    yard(EERIE, 2.0)
    k = C.knotley((0, 4, 0.2), rot=180, face="happy"); k.root.rotation_euler.z = math.radians(180)
    k.pose(1, "hands_face")
    for i in range(6):
        c = C.kid(i, (0, 1.2 - i * 2.6, 0.2), rot=180, face="happy"); c.root.rotation_euler.z = math.radians(180)
    cam(S, (9, -10, 6), (8, -8, 5.6), (0, -3, 3.5), lens=30)


def pip_line(S):
    yard(EERIE, 2.0)
    p = C.pip((0, 0, 0.2), face="happy", lace=None, tie="#c62828"); p.colored(True)
    for i, x in enumerate((-3.5, 3.5)):
        C.kid(i + 2, (x, 1.5, 0.2), face="happy")
    cam(S, (0.8, -8, 4), (0.4, -7, 3.8), (0, 0, 3.4), lens=36)


def hero_no(S):
    yard(EERIE, 2.0)
    h = C.hero((0, 0, 0.2), face="determined")
    h.pose(1, "hips")
    f = 4
    while f < S.n:
        h.head_turn(f, 20, 0); h.head_turn(f + 4, -20, 0); f += 8
    cam(S, (0.6, -6, 5.2), (0.3, -5.2, 5.0), (0, 0, 4.6), lens=40)


def next_morning(S):
    yard(EERIE, 1.4)
    for i in range(8):
        c = C.kid(i, (-10 + (i % 4) * 6.5, -2 - (i // 4) * 5, 0.2), face="hypno")
    cam(S, (-4, -26, 9), (4, -24, 8), (0, -4, 3), lens=28)


def march(S):
    yard(EERIE, 1.4)
    for row in range(3):
        for k in range(4):
            x = -6 + k * 4
            c = C.kid(row * 4 + k, (x, -2 - row * 3, 0.2), face="hypno")
            c.walk(1, S.n, (x, -2 - row * 3, 0.2), (x, 8 - row * 3, 0.2), stride=12, swing=20)
    cam(S, (0, -22, 3), (0, -19, 3.2), (0, 2, 3.4), lens=30)


def no_laugh(S):
    yard(EERIE, 1.4)
    for i, (x, y) in enumerate([(-3, 0), (0.5, 1), (4, 0)]):
        C.kid(i + 3, (x, y, 0.2), face="hypno")
    ball = sphere(0.7, (-6, -3, 0.9), mat("#c0592b"), name="ball")    # the ball lies still: nobody plays
    cam(S, (2, -12, 4.4), (1, -10.5, 4.2), (0, 0, 3.6), lens=34)


def pip_empty(S):
    yard(EERIE, 1.4)
    p = C.pip((0, 0, 0.2), face="hypno", lace=None, tie="#c62828"); p.colored(True)
    cam(S, (0.4, -5.6, 4.6), (0.2, -4.8, 4.5), (0, 0, 4.2), lens=42)


def knotley_tug(S):
    yard(EERIE, 1.4)
    k = C.knotley((0, 4, 0.2), face="smug")
    tug(k, 4, 2)
    cam(S, (0.6, -2, 6.4), (0.3, -0.8, 6.2), (0, 4, 6.2), lens=40)


def heads_turn(S):
    yard(EERIE, 1.4)
    kids = [C.kid(i, (-9 + (i % 5) * 4.5, -1 - (i // 5) * 4, 0.2), face="hypno") for i in range(10)]
    for c in kids:
        c.head_turn(1, 0, 0); c.head_turn(4, 0, 0); c.head_turn(8, 60, 0)    # all at once
    cam(S, (0, -20, 6), (0, -17, 5.6), (0, -3, 4), lens=30)


def hero_alone(S):
    yard(EERIE, 1.4)
    for i in range(6):
        c = C.kid(i, (-7 + (i % 3) * 7, 1 - (i // 3) * 5, 0.2), face="hypno")
        c.head_turn(1, 60, 0)
    h = C.hero((0, -6, 0.2), face="nervous")
    h.head_turn(1, -30, 0); h.head_turn(S.n, 30, 0)
    cam(S, (0, -18, 5), (0, -15, 4.8), (0, -4, 4), lens=32)


def knotley_notice(S):
    yard(EERIE, 1.4)
    k = C.knotley((0, 0, 0.2), face="side_eye")
    k.head_turn(1, 0, 0); k.head_turn(8, -35, 10)
    cam(S, (1, -7, 7.2), (0.5, -6, 7), (0, 0, 7), lens=40)


def knotley_close(S):
    yard(EERIE, 1.4)
    k = C.knotley((0, 0, 0.2), face="happy")
    k.pose(1, "point")
    k.talk(S.w(0)[0], [0.6, 0.8, 0.5, 0.7, 0.4, 0.6, 0.3, 0.7, 0.5] * max(1, S.n // 18))
    cam(S, (0.5, -7.5, 7.2), (0.3, -6.4, 7.1), (0, 0, 7.2), lens=40)


def run(S):
    yard(EERIE, 1.6)
    h = C.hero((-14, -6, 0.2), face="scared")
    h.walk(1, S.n, (-14, -6, 0.2), (8, -6, 0.2), run=True)
    k = C.knotley((-24, -2, 0.2), face="happy")
    k.walk(1, S.n, (-26, -2, 0.2), (-10, -2, 0.2), stride=12)
    cam(S, (-12, -24, 4.5), (6, -24, 4.5), (-12, -6, 3.6), (8, -6, 3.6), lens=30)


def hide(S):
    room(sky=NIGHT, wall="#4e5b4e", floor="#3e3e3e", light=0.3)
    for x in (-2.4, 2.4):
        cyl(0.12, 6, (x, 2, 3), mat("#8d6e63"), rot=(0, 10 if x > 0 else -10, 0))
        box((1.6, 0.4, 0.6), (x, 2, 0.3), mat("#bdbdbd"))
    B.point((0, -1, 7), 150, (1, 0.9, 0.6), 0.4)
    h = C.hero((0, 0, 0), face="nervous")
    V1.sit(h, 1)
    cam(S, (0.8, -6.5, 4.4), (0.4, -5.6, 4.2), (0, 0, 3.6), lens=36)


def think(S):
    room(sky=NIGHT, wall="#4e5b4e", floor="#3e3e3e", light=0.3)
    B.point((0, -1, 7), 150, (1, 0.9, 0.6), 0.4)
    h = C.hero((0, 0, 0), face="little_o")
    V1.sit(h, 1)
    h.set_face(S.n // 2, "determined")
    bulb = sphere(0.45, (0.9, -0.3, 7.4), mat("#fff59d", emit=6, wash=False), name="idea")
    bulb.scale = (0.01,) * 3; bulb.keyframe_insert("scale", frame=S.n // 2)
    bulb.scale = (1,) * 3; bulb.keyframe_insert("scale", frame=S.n // 2 + 5)
    cam(S, (0.6, -5.4, 5), (0.3, -4.6, 4.8), (0, 0, 4.8), lens=38)


def threads_shot(S):
    hall()
    k = C.knotley((0, 17, 2.4), rot=0, face="smug")
    kids = seated_kids(3, 9)
    threads(k, kids, 2)
    cam(S, (14, -16, 14), (10, -14, 12), (0, 6, 4), lens=28)


def his_tie(S):
    hall()
    k = C.knotley((0, 17, 2.4), face="smug")
    cam(S, (0.5, 10.8, 7.4), (0.3, 11.4, 7.3), (0, 17, 7.0), lens=42)


def his_knot(S):
    hall()
    k = C.knotley((0, 17, 2.4), face="smug")
    k.pose(1, "hands_face")
    cam(S, (0.5, 11.4, 7.2), (0.3, 11.9, 7.1), (0, 17, 7.0), lens=44)


def hero_idea(S):
    room(sky=NIGHT, wall="#4e5b4e", floor="#3e3e3e", light=0.3)
    B.point((0, -1, 7), 150, (1, 0.9, 0.6), 0.4)
    h = C.hero((0, 0, 0), face="smug")
    h.pose(1, "hips")
    cam(S, (0.5, -4.4, 5.6), (0.25, -3.8, 5.4), (0, 0, 5.2), lens=40)


def assembly(S):
    hall()
    seated_kids(5, 9)
    cam(S, (-3, 15.5, 9.5), (3, 15.5, 9), (0, -2, 3.2), lens=26)


def stage(S):
    hall()
    k = C.knotley((0, 17, 2.4), face="happy")
    k.pose(1, "hands_face")
    seated_kids(2, 9)
    cam(S, (0, -4, 9.5), (0, -1, 9), (0, 17, 7.5), lens=30)


def crawl(S):
    hall()
    seated_kids(2, 9, skip=((0, 4), (1, 4)))
    h = C.hero((0, -6, 0), rot=180, face="determined")
    h.root.scale = (1, 1, 0.55)
    h.walk(1, S.n, (0.0, -8, 0), (0.0, 6, 0), stride=10)
    h.key_rot(h.body, 1, 50)
    cam(S, (8, -10, 2.4), (8, 2, 2.4), (0, -6, 1.2), (0, 6, 1.2), lens=26)


def behind(S):
    hall()
    k = C.knotley((0, 17, 2.4), face="happy")
    h = C.hero((0, 21, 2.4), rot=180, face="determined")
    cam(S, (5.5, 20.6, 7.4), (5.0, 20.8, 7.2), (0, 19.3, 6.2), lens=28)


def grab(S):
    hall()
    k = C.knotley((0, 17, 2.4), face="shocked")
    h = C.hero((0, 15.2, 2.4), rot=180, face="determined")
    h.pose(1, "hold")
    cam(S, (7.5, 15.8, 6.8), (6.8, 15.9, 6.6), (0, 16, 6.2), lens=32)


def untie_shot(S):
    hall()
    k = C.knotley((0, 17, 2.4), face="scared")
    untie(k, 3)
    cam(S, (0.6, 9.6, 7.4), (0.3, 10.2, 7.3), (0, 17, 7.8), lens=36)


def retie(S):
    hall()
    k = C.knotley((0, 17, 2.4), face="nervous")
    h = C.hero((0, 15.0, 2.4), rot=180, face="determined")
    f = 1
    while f < S.n:                        # quick tying hands
        h.key_rot(h.sh[0], f, -80, -15); h.key_rot(h.sh[1], f, -80, 15)
        h.key_rot(h.sh[0], f + 3, -95, -25); h.key_rot(h.sh[1], f + 3, -95, 25); f += 6
    for o in k.tie_objs:                  # the tie comes back, tied by the hero
        o.hide_render = True; o.keyframe_insert("hide_render", frame=1)
        o.hide_render = False; o.keyframe_insert("hide_render", frame=S.n // 2)
    cam(S, (7.5, 15.8, 6.8), (6.8, 15.9, 6.6), (0, 16, 6.4), lens=32)


def double(S):
    hall()
    k = C.knotley((0, 17, 2.4), face="nervous")
    B.sparkle_burst((0, 16.2, 6.4), 2, n=14, color=TIE_GLOW, spread=1.6)
    cam(S, (0.6, 9.6, 7.4), (0.3, 10.2, 7.3), (0, 17, 7.8), lens=36)


def freeze(S):
    hall()
    k = C.knotley((0, 17, 2.4), face="shocked")
    cam(S, (0, 9, 6), (0, 10, 6.4), (0, 17, 6.8), lens=34)


def knotley_ask(S):
    hall()
    k = C.knotley((0, 17, 2.4), rot=0, face="calm")
    k.talk(S.word("what"), [0.6, 0.8, 0.5, 0.7, 0.4, 0.6, 0.3, 0.7] * max(1, S.n // 16))
    cam(S, (1, 10.5, 8.2), (0.6, 11.2, 8.0), (0, 17, 8.4), lens=40)


def order(S):
    hall()
    h = C.hero((0, 14.5, 2.4), rot=0, face="determined")
    h.pose(1, "point")
    cam(S, (1.5, 8.5, 6.2), (1, 9.3, 6.0), (0, 14.5, 5.4), lens=36)


def untie_all(S):
    hall()
    kids = seated_kids(3, 9)
    k = C.knotley((-16, 8, 0), rot=90, face="nervous")
    k.walk(1, S.n, (-18, 8.2, 0), (16, 8.2, 0), run=True)
    for i, c in enumerate(kids[:9]):
        untie(c, 3 + i * max(1, S.n // 10))
    cam(S, (0, -14, 9), (0, -12, 8), (0, 4, 3), lens=28)


def pip_wake(S):
    hall()
    p = C.pip((0, 6, 0.4), rot=180, face="hypno", lace=None, tie="#c62828"); p.colored(True)
    p.root.rotation_euler.z = math.radians(180); V1.sit(p, 1)
    p.set_face(S.n // 2, "blink"); p.set_face(S.n // 2 + 3, "surprised")
    cam(S, (0.4, 10.4, 5.0), (0.2, 10.0, 4.9), (0, 5.6, 4.3), lens=42)


def pip_why(S):
    hall()
    p = C.pip((0, 6, 0.4), rot=180, face="side_eye", lace=None); p.colored(True)
    p.root.rotation_euler.z = math.radians(180); V1.sit(p, 1)
    p.talk(S.word("why"), [0.6, 0.8, 0.5, 0.7, 0.4, 0.6, 0.5] * max(1, S.n // 14), rest="side_eye")
    cam(S, (0.9, 10.8, 5.2), (0.6, 10.3, 5.0), (0, 5.6, 4.3), lens=40)


def cafeteria_set():
    S2.look(DAY, 2.0, 300); colour()
    box((50, 50, 0.2), (0, 0, -0.1), mat("#cfd8dc", rough=0.4), name="floor")
    box((50, 0.5, 20), (0, 8, 10), mat("#ffe0b2"), name="wall")
    box((14, 3, 3.6), (0, 3, 1.8), mat("#90a4ae", metal=0.6, rough=0.3), name="counter")
    text("CAFETERIA", (0, 7.6, 12), mat("#e65100", emit=0.6), size=1.8, extrude=0.1)
    B.point((0, -2, 12), 1500, (1, 0.95, 0.85), 4)


def pancakes_stack(loc, n=5):
    for i in range(n):
        cyl(0.9, 0.22, (loc[0], loc[1], loc[2] + i * 0.24), mat("#e0a458", rough=0.6), verts=24)
    cyl(0.35, 0.18, (loc[0], loc[1], loc[2] + n * 0.24 + 0.05), mat("#fff59d"), verts=16)


def cafeteria(S):
    cafeteria_set()
    k = C.knotley((0, 5, 0), face="happy")
    hat = cyl(0.65, 0.9, (0, 0, 1.9), mat("#ffffff"), k.head)
    k.pose(1, "wave")
    for i, x in enumerate((-5, 5)):
        C.kid(i, (x, -3, 0), rot=180, face="laugh").root.rotation_euler.z = math.radians(180)
    cam(S, (3, -12, 6), (2, -10, 5.8), (0, 3, 5), lens=30)


def pancakes(S):
    cafeteria_set()
    pancakes_stack((0, 1.6, 3.7))
    B.sparkle_burst((0, 1.6, 5.4), 3, n=10, color="#fff59d", spread=1.5)
    cam(S, (1.2, -2.4, 6.2), (0.8, -1.6, 5.8), (0, 1.6, 4.2), lens=40)


def ending(S):
    cafeteria_set()
    k = C.knotley((2.5, 3.5, 0), face="happy")
    cyl(0.65, 0.9, (0, 0, 1.9), mat("#ffffff"), k.head)
    h = C.hero((-1.5, -1.5, 0), face="happy")
    h.head_turn(S.word("honestly"), 30, 0); h.head_turn(S.word("nicer"), 0, 0)
    h.set_face(S.word("nicer"), "wink"); h.pose(S.word("nicer"), "thumb")
    pancakes_stack((3.5, 1.6, 3.7), 3)
    cam(S, (1, -14, 5.4), (0.6, -11, 5.2), (0.5, 1, 4.4), lens=32)


# markers that clash with helper names
ALIASES = {"threads": threads_shot, "untie": untie_shot}


def shot_funcs():
    import re
    from lines import SCRIPT
    ids = re.findall(r"\[(\w+)\]", " ".join(SCRIPT))
    g = globals()
    out = {}
    for k in ids:
        f = ALIASES.get(k, g.get(k))
        assert callable(f), k
        out[k] = f
    return out
