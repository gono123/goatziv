"""The 24 shots of "Everyone Is Born Grey". Each shot builds its own scene from blib.

A shot function gets a Shot helper: S.n (frame count), S.f(t) (absolute seconds -> local frame),
S.line(i) (line i of this shot: start/end frames, mouth envelope), S.chunk(i, j).
"""
import math, random
import bpy
from mathutils import Vector
import blib as B
from blib import mat, box, cyl, sphere, text, empty

GREY_SKY = dict(top=(0.42, 0.45, 0.5), bottom=(0.66, 0.68, 0.71))
BLUE_SKY = dict(top=(0.18, 0.42, 0.95), bottom=(0.72, 0.85, 1.0))
STORM = dict(top=(0.22, 0.24, 0.28), bottom=(0.45, 0.47, 0.5))


class Shot:
    def __init__(self, data, fps=24):
        self.d = data
        self.fps = fps
        self.t0 = data["start"]
        self.n = max(1, round(data["end"] * fps) - round(data["start"] * fps))

    def f(self, t):
        return int(round((t - self.t0) * self.fps)) + 1

    def line(self, i):
        L = self.d["lines"][i]
        return dict(a=self.f(L["start"]), b=self.f(L["end"]), mouth=L["mouth"], chunks=[(self.f(c["start"]), self.f(c["end"]), c["text"]) for c in L["chunks"]])


def base(sky=GREY_SKY, sun_e=2.6, town=0.0):
    B.world(**sky)
    B.sun(sun_e, rot=(52, 0, 28), color=(0.95, 0.96, 1.0))
    bpy.context.scene["town_line"] = town


def town_grid(n=4, spacing=34, skip_center=True):
    """Blocks of houses for wide shots."""
    walls = ["#e8d5b5", "#b5d3e8", "#e8b5c8", "#c8e8b5", "#e8e1b5", "#d1b5e8"]
    roofs = ["#a33b2f", "#2f5ea3", "#3f8a3a", "#7a3fa3", "#a36b2f", "#2f8a8a"]
    rnd = random.Random(3)
    for gx in range(-n, n + 1):
        for gy in range(-n, n + 1):
            if skip_center and abs(gx) <= 0 and abs(gy) <= 0:
                continue
            x, y = gx * spacing, gy * spacing
            box((spacing - 12, spacing - 12, 0.3), (x, y, 0.15), mat("#b8bcc2"), name="block")
            for k in range(4):
                hx = x + (-6 if k % 2 else 6)
                hy = y + (-6 if k < 2 else 6)
                B.house(hx, hy, w=8, d=7, h=6 + rnd.random() * 5, wall=rnd.choice(walls), roof_c=rnd.choice(roofs), rot=rnd.choice([0, 90, 180, 270]))
            if rnd.random() < 0.5:
                B.tree(x + 12, y + 12, 0.8)


def bank(x=0, y=20):
    """The Color Bank: grey stone building with the only colour in town on its sign."""
    r = empty("bank", (x, y, 0))
    st = mat("#d9d6cf", rough=0.8)
    box((40, 16, 22), (0, 8, 11), st, r, name="bankbody")
    box((44, 18, 2), (0, 8, 23), mat("#bfbab0"), r, name="cornice")
    B.roof(44, 18, 6, (0, 8 - 9, 24), mat("#a8a39a"), r)
    for cx in (-15, -9, 9, 15):
        cyl(1.1, 16, (cx, -1.5, 9), mat("#efece6"), r, name="column")
    box((40, 6, 1.2), (0, -2, 0.6), mat("#c9c5bd"), r, name="step")
    box((10, 0.6, 12), (0, -0.2, 6), mat("#3a3226"), r, name="bankdoor")
    cols = ["#ff2d55", "#ff9500", "#ffe600", "#34c759", "#00c7ff", "#5856d6", "#ff2dc8"]
    box((34, 0.6, 5.4), (0, -0.6, 19.4), mat("#ffffff", rough=0.4, wash=False), r, name="signboard")
    B.letters("COLOR BANK", (0, -0.95, 17.6), 3.6, cols, parent=r, extrude=0.2)
    # a rainbow arch over the door
    for i, c in enumerate(cols[:6]):
        B.arch(8.2 - i * 0.6, 7.6 - i * 0.6, (0, -0.55 - i * 0.01, 12.0), mat(c, emit=1.4, wash=False), r)
    return r


def school(y=26):
    r = empty("school", (0, y, 0))
    box((60, 14, 16), (0, 7, 8), mat("#c97b63", rough=0.85), r, name="schoolbody")
    box((62, 15, 1.2), (0, 7, 16.6), mat("#8a5544"), r, name="schoolroof")
    for wx in range(-24, 25, 8):
        box((5, 0.4, 4), (wx, -0.1, 10.5), mat("#3c4a5a", rough=0.15), r, name="window")
        box((5, 0.4, 4), (wx, -0.1, 4), mat("#3c4a5a", rough=0.15), r, name="window")
    box((7, 0.6, 7), (0, -0.2, 3.5), mat("#6e4b32"), r, name="door")
    box((22, 0.8, 3.4), (0, -0.4, 14.2), mat("#f4f1e8"), r, name="signboard")
    text("SCHOOL", (0, -0.9, 14.2), mat("#2b3a55"), size=2.6, parent=r, extrude=0.1)
    # yard
    box((120, 90, 0.2), (0, -30, 0.1), mat("#9c9fa3", rough=0.95), name="yard")
    for x in range(-40, 41, 4):
        box((0.3, 0.3, 4), (x, -60, 2), mat("#7a7d80"), name="fence")
    box((84, 0.3, 0.3), (0, -60, 3.6), mat("#7a7d80"), name="fence")
    return r


def picnic(x, y):
    w = mat("#8a6a4a", rough=0.8)
    box((8, 3, 0.4), (x, y, 3.2), w, name="table")
    for dx in (-3.5, 3.5):
        box((0.4, 2.6, 3.2), (x + dx, y, 1.6), w, name="tleg")
    box((8, 1.2, 0.35), (x, y - 2.6, 1.9), w, name="bench")
    box((8, 1.2, 0.35), (x, y + 2.6, 1.9), w, name="bench")


def room(back=8, wall="#d8cbb8", floor="#9a7a5a"):
    box((40, 40, 0.2), (0, 0, -0.1), mat(floor, rough=0.7), name="floor")
    box((40, 0.5, 20), (0, back, 10), mat(wall, rough=0.9), name="backwall")
    box((0.5, 40, 20), (-14, 0, 10), mat(wall, rough=0.9), name="sidewall")
    box((0.5, 40, 20), (14, 0, 10), mat(wall, rough=0.9), name="sidewall")
    box((8, 0.3, 6), (-5, back - 0.3, 10), mat("#9fb6c8", rough=0.2, emit=0.4), name="window")
    box((8.6, 0.2, 0.4), (-5, back - 0.45, 7), mat("#f2f2f2"), name="sill")
    box((4, 0.2, 3), (6, back - 0.3, 11), mat("#6b8f5a"), name="picture")
    box((4.6, 0.15, 3.6), (6, back - 0.2, 11), mat("#6e4b32"), name="frame")
    box((6, 3, 3), (8, back - 2, 1.5), mat("#7a5a3a"), name="dresser")
    B.point((0, -4, 14), 900, (1, 0.93, 0.85), 3)


def car(x, y, color="#c0392b", rot=0):
    r = empty("car", (x, y, 0)); r.rotation_euler.z = math.radians(rot)
    m = mat(color, rough=0.35)
    box((9, 4.4, 2.2), (0, 0, 1.9), m, r, bevel=0.3, name="carbody")
    box((5, 4.0, 2.0), (-0.5, 0, 3.9), m, r, bevel=0.3, name="cabin")
    box((4.6, 4.1, 1.5), (-0.5, 0, 3.9), mat("#2c3e50", rough=0.1), r, name="glass")
    for wx in (-3, 3):
        for wy in (-2.2, 2.2):
            cyl(1.0, 0.8, (wx, wy, 1.0), mat("#1a1a1a"), r, rot=(90, 0, 0), name="wheel")
    return r


def paper(parent, loc, label="A+"):
    p = box((1.4, 0.05, 1.8), loc, mat("#f7f7f2", wash=False), parent, name="paper")
    text(label, (0, -0.06, 0.1), mat("#e02424", wash=False), size=0.9, parent=p, extrude=0.01)
    return p


def blink(node_input, f0, f1, period=10, lo=0.2, hi=6.0):
    f = f0
    while f <= f1:
        node_input.default_value = hi
        node_input.keyframe_insert("default_value", frame=f)
        node_input.default_value = lo
        node_input.keyframe_insert("default_value", frame=f + period // 2)
        f += period


def emis(m):
    return m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]


def flash_light(loc, f0, f1, color=(1, 0.1, 0.1), period=12, energy=4000):
    l = B.point(loc, energy, color, 2)
    f = f0
    while f <= f1:
        l.data.energy = energy; l.data.keyframe_insert("energy", frame=f)
        l.data.energy = 0; l.data.keyframe_insert("energy", frame=f + period // 2)
        f += period
    return l


def two_cams(S, cuts):
    """cuts: list of (frame, cam_object) -> timeline markers switching cameras."""
    sc = bpy.context.scene
    for f, cam in cuts:
        m = sc.timeline_markers.new("c%d" % f, frame=f)
        m.camera = cam


# ============================================================================ shots

def town_wide(S):
    base()
    B.ground(900)
    town_grid(3)
    B.street(160)
    B.dome()
    cam, t = B.camera(24)
    B.cam_key(cam, t, 1, (0, -95, 60), (0, 10, 30))
    B.cam_key(cam, t, S.n, (0, -80, 45), (0, 10, 18))


def grey_people(S):
    base()
    B.ground(600)
    B.street(160)
    B.dome()
    people = []
    for i, (y, x0, x1, ph) in enumerate([(-10, -22, 10, 0), (-6, 18, -12, 5), (-12.5, -30, -2, 9)]):
        c = B.townie(i + 1, (x0, y, 0.5))
        c.walk(1 + ph, S.n + 10, (x0, y, 0.5), (x1, y, 0.5), stride=10)
        people.append(c)
    cam, t = B.camera(32)
    B.cam_key(cam, t, 1, (-3, -34, 5.5), (0, -8, 4.2))
    B.cam_key(cam, t, S.n, (2, -31, 5.0), (0, -8, 4.0))


def bank_shot(S):
    base()
    B.ground(600)
    bank(0, 12)
    for i in range(6):
        c = B.townie(i, (2.0 - i * 0.2, 6 - i * 3.4 - 2, 1.2), rot=180 + (i % 2) * 8)
        c.idle(1, S.n, phase=i)
    cam, t = B.camera(30)
    B.cam_key(cam, t, 1, (14, -38, 6), (0, 8, 11))
    B.cam_key(cam, t, S.n, (10, -30, 5), (0, 8, 11.5))


def yellow_drop(S):
    base()
    B.ground(600)
    B.street(120, y0=-14)
    bank(0, 30)
    kid = B.townie(2, (0, 0, 0))
    kid.set_mouth("open", 1)
    kid.pose(1, "hold")
    paper(kid.sh[0], (0, -0.6, -2.3))
    jar = cyl(0.45, 0.9, (0, -0.6, -2.3), mat("#dfefff", rough=0.05, alpha=0.35, wash=False), kid.sh[1], name="jar")
    sphere(0.22, (0, 0, -0.2), mat("#ffe600", emit=6.0, wash=False), jar, name="drop")
    # little hop of joy on the punchline
    L = S.line(0)
    hop = L["chunks"][-1][0]
    for k in range(3):
        f = hop + k * 8
        kid.move(f, (0, 0, 0)); kid.move(f + 4, (0, 0, 0.9)); kid.move(f + 8, (0, 0, 0))
    kid.pose(hop, "hold"); kid.pose(hop + 4, "arms_up"); kid.pose(hop + 16, "hold")
    B.point((0, -3, 3), 60, (1, 0.9, 0.2), 0.5)
    cam, t = B.camera(42)
    B.cam_key(cam, t, 1, (2.5, -17, 4.6), (0, 0, 3.2))
    B.cam_key(cam, t, S.n, (1.5, -14.5, 4.4), (0, 0, 3.4))


def higgins(S):
    base()
    B.ground(600)
    B.street(160)
    car(-4, -4.5, "#c0392b")
    sold = box((3.2, 0.1, 1.6), (-4, -6.8, 4.5), mat("#ffffff", wash=False), name="sold")
    text("SOLD", (0, -0.08, 0), mat("#e02424", wash=False), size=1.0, parent=sold, extrude=0.02)
    cyl(0.08, 2.5, (-4, -6.75, 2.6), mat("#555555"), name="post")
    h = B.townie(5, (-18, -10, 0.5), cheeks="#ff2b2b", hair="#5a5a5a", face="open")
    L1 = S.line(1)
    h.walk(1, L1["a"] + 6, (-16, -10, 0.5), (4, -10, 0.5), stride=10)
    h.face_dir(L1["a"] + 8, 0)
    h.face_dir(L1["a"] + 12, -10)
    h.pose(L1["a"] + 10, "idle"); h.pose(L1["a"] + 16, "wave"); h.pose(S.n, "wave")
    h.idle(L1["a"] + 12, S.n, arms=False)
    cam, t = B.camera(34)
    B.cam_key(cam, t, 1, (-12, -32, 5.5), (-8, -6, 3.5))
    B.cam_key(cam, t, L1["a"] + 6, (2, -26, 5), (2, -8, 3.6))
    B.cam_key(cam, t, S.n, (4, -20, 4.8), (4, -9, 4.0))


def prism_shot(S):
    base()
    B.ground(600)
    bank(0, 14)
    p = B.prism((0, 2, 1.2))
    p.colored(False)  # invert material: "not washed" = full colour
    p.pose(1, "hips"); p.idle(1, S.n, arms=False)
    p.head_turn(1, 0, -5)
    L1 = S.line(1)
    p.pose(L1["a"], "hips"); p.pose(L1["a"] + 8, "arms_out"); p.pose(S.n, "arms_out")
    for i, (x, y) in enumerate([(-7, -6), (6, -7), (-3, -10), (9, -3)]):
        c = B.townie(i, (x, y, 0.5), rot=math.degrees(math.atan2(-x, 2 - y)) + 180 if False else 180 + (-15 if x > 0 else 15))
        c.pose(1, "idle")
        c.pose(L1["a"] + 4 + i * 2, "shield"); c.pose(S.n, "shield")
        c.head_turn(L1["a"] + 4 + i * 2, 0, 15)
    for k, c in enumerate([(1, 0.2, 0.4), (0.2, 0.6, 1), (1, 0.9, 0.1), (0.3, 1, 0.4)]):
        B.point((math.cos(k * 1.57) * 3, -1 + math.sin(k * 1.57) * 2, 5), 300, c, 1)
    cam, t = B.camera(30)
    B.cam_key(cam, t, 1, (0, -30, 2.5), (0, 2, 6))
    B.cam_key(cam, t, S.n, (0, -17, 2.2), (0, 2, 5.5))


def umbrella(S):
    base()
    B.ground(1200)
    town_grid(3)
    B.street(160)
    B.dome()
    # storm clouds sitting on top of the glass, rain that never gets in
    cm = mat("#4b4f56", rough=1, wash=False)
    rnd = random.Random(5)
    for i in range(40):
        a = rnd.random() * math.tau; rr = rnd.random() * 150
        box((50, 50, 14), (math.cos(a) * rr, math.sin(a) * rr, 252 + rnd.random() * 10), cm, bevel=5, name="cloud")
    B.rain((0, 0), size=(200, 200), z=275, z0=245, rate=2500, lifetime=10, speed=-60, mesh_scale=4)
    L1 = S.line(1)
    cam, t = B.camera(24)
    B.cam_key(cam, t, 1, (0, -20, 4), (0, 60, 90))
    B.cam_key(cam, t, L1["a"], (0, -330, 120), (0, 0, 120), 24)
    B.cam_key(cam, t, S.n, (0, -380, 140), (0, 0, 130))


def inspectors(S):
    base(sun_e=2.0)
    B.ground(600)
    B.street(160)
    B.dome()
    ins = []
    for i, x in enumerate((-3.5, 0, 3.5)):
        c = B.inspector("insp%d" % i, (x, 20 - abs(x) * 0.6, 0.5))
        c.walk(1 + i * 2, S.n, (x, 22 - abs(x) * 0.6, 0.5), (x, -2 - abs(x) * 0.6, 0.5), stride=12, swing=24)
        ins.append(c)
    blink(emis(ins[0].siren.data.materials[0]), 1, S.n, 12)
    flash_light((0, 6, 9), 1, S.n, period=12, energy=2500)
    L1 = S.line(1)
    for c in ins:
        c.pose(L1["a"] + 10, "idle")
    cam, t = B.camera(28)
    B.cam_key(cam, t, 1, (0, -16, 1.6), (0, 10, 5.5))
    B.cam_key(cam, t, S.n, (0, -19, 1.4), (0, 0, 5.0))


def school_grey(S):
    base()
    school(30)
    picnic(0, 0)
    h = B.hero((0, -2.6, 0.3), rot=0)
    sit(h, 1)
    h.set_mouth("flat", 1)
    h.brow(1, 4, -0.03)
    tray = box((3, 2, 0.15), (0, -1.2, 3.5), mat("#8f9399"), name="tray")
    sphere(0.6, (-0.6, -1.2, 3.8), mat("#9a9ea4", rough=0.9), scale=(1, 1, 0.5), name="mush")
    box((0.9, 0.9, 0.9), (0.7, -1.2, 4.0), mat("#a5a8ad"), name="cube")
    for i, (x, y) in enumerate([(-9, 4), (8, 6), (12, -6)]):
        k = B.townie(i, (x, y, 0.2), rot=180 + 20 * (i - 1))
        k.idle(1, S.n, phase=i * 2)
    L1 = S.line(1)
    h.head_turn(L1["a"], 0, 25)   # looks down at the grey lunch
    cam, t = B.camera(36)
    B.cam_key(cam, t, 1, (3, -16, 6), (0, -2, 4.2))
    B.cam_key(cam, t, L1["a"] - 1, (2.4, -13, 6), (0, -2, 4.2))
    B.cam_key(cam, t, L1["a"], (0.6, -6.5, 6.2), (0, -1.2, 3.7))
    B.cam_key(cam, t, S.n, (0.4, -5.6, 6.0), (0, -1.2, 3.7))
    # make the cut a hard cut
    for fc in B.all_fcurves(cam) + B.all_fcurves(t):
        for kp in fc.keyframe_points:
            if int(kp.co.x) == L1["a"] - 1:
                kp.interpolation = "CONSTANT"


def sit(c, frame):
    c.root.location.z += -0.15
    c.key_rot(c.hip[0], frame, -90); c.key_rot(c.hip[1], frame, -90)
    c.pose(frame, "sit_arms")


def mom_paint(S):
    base(sun_e=1.0)
    room()
    h = B.hero((-1.5, 0, 0), rot=-20)
    h.pose(1, "arms_out"); h.set_mouth("flat", 1); h.brow(1, 2)
    m = B.mom((3.0, -1.2, 0), rot=60)
    m.pose(1, "roll")
    roller = empty("roller", (0, -0.4, -2.2), m.sh[1])
    cyl(0.12, 1.8, (0, 0, 0), mat("#333333"), roller, rot=(0, 0, 0), name="handle")
    cyl(0.5, 1.6, (0, -0.2, 1.0), mat("#8a8d92", rough=0.9), roller, rot=(0, 90, 0), name="rollerhead")
    # roll up and down
    f = 1
    while f < S.n:
        m.key_rot(m.sh[1], f, -70); m.key_rot(m.sh[1], f + 9, -125)
        f += 18
    m.key_rot(m.sh[0], 1, -40)
    L = S.line(1)
    m.talk(L["a"], L["mouth"])
    m.head_turn(L["a"] - 3, -40, 0); m.head_turn(L["b"] + 4, -40); m.head_turn(L["b"] + 12, 0)
    L2 = S.line(2)
    h.head_turn(L2["a"], -25, 0); h.head_turn(S.n, -30, 0)
    cam, t = B.camera(30)
    B.cam_key(cam, t, 1, (2, -20, 6.5), (0.5, 0, 3.6))
    B.cam_key(cam, t, S.n, (1, -16, 6), (0.5, 0, 3.6))


def mom_rule(S):
    base(sun_e=1.0)
    room()
    m = B.mom((0, 2, 0), rot=0)
    m.pose(1, "idle")
    L = S.line(1)
    m.talk(L["a"], L["mouth"])
    m.brow(L["a"], -10, 0.03)
    f = L["a"]
    while f < L["b"]:
        m.key_rot(m.sh[1], f, -150, 12); m.key_rot(m.sh[1], f + 5, -150, 12, 18)
        f += 10
    m.pose(L["b"] + 4, "idle")
    m.idle(1, S.n, arms=False)
    h = B.hero((0.5, -4.5, 0), rot=180)
    h.colored(False)
    cam, t = B.camera(38)
    B.cam_key(cam, t, 1, (5.5, -12, 6.2), (-0.5, 2, 5.2))
    B.cam_key(cam, t, S.n, (4.8, -10, 6.0), (-0.5, 2, 5.2))


def schoolyard(n_kids=5, hero_loc=(0, -6, 0.2)):
    base()
    school(30)
    B.dome()
    kids = []
    spots = [(-9, -2), (8, 0), (-5, -14), (11, -12), (-13, -8), (5, -18)]
    for i in range(n_kids):
        x, y = spots[i]
        k = B.townie(i, (x, y, 0.2), rot=math.degrees(math.atan2(x - hero_loc[0], -(y - hero_loc[1]))) + 180)
        kids.append(k)
    h = B.hero(hero_loc)
    return h, kids


def crack(S):
    h, kids = schoolyard()
    B.world(top=(0.25, 0.27, 0.31), bottom=(0.6, 0.62, 0.66))
    for i, k in enumerate(kids):
        k.idle(1, S.n, phase=i)
    ball = sphere(0.7, (-9, -4, 0.9), mat("#c0592b"), name="ball")
    for f in range(1, S.n, 12):
        ball.location.z = 0.9; ball.keyframe_insert("location", frame=f)
        ball.location.z = 4.5; ball.keyframe_insert("location", frame=f + 6)
    L0 = S.line(0)
    hit = L0["chunks"][-1][0]  # "Crack."
    h.head_turn(hit, 0, -35)
    h.set_mouth("o", hit)
    for k in kids:
        k.head_turn(hit + 4, 0, -30)
    # the crack: bright jagged lines on the glass overhead
    rnd = random.Random(1)
    crack_m = mat("#ffffff", emit=6, wash=False)
    pts = [Vector((0, 60, 230))]
    for i in range(14):
        pts.append(pts[-1] + Vector((rnd.uniform(-14, 14), rnd.uniform(-10, 10), rnd.uniform(-1, 1))))
    for i in range(len(pts) - 1):
        seg = B._beam(pts[i], pts[i + 1], 2.2, crack_m, None)
        seg.scale = (1, 1, 0.001); seg.keyframe_insert("scale", frame=hit + i)
        seg.scale = (1, 1, 1); seg.keyframe_insert("scale", frame=hit + i + 2)
    cam, t = B.camera(30)
    B.cam_key(cam, t, 1, (2, -24, 5), (0, -4, 4))
    B.cam_key(cam, t, hit, (2, -24, 5), (0, -4, 4.2))
    B.cam_key(cam, t, hit + 14, (1, -14, 3), (0, 60, 230), 22)
    B.cam_key(cam, t, S.n, (1, -14, 3), (0, 60, 228), 26)


def rain_me(S):
    h, kids = schoolyard()
    h.colored(False)
    B.rain((0, -6), size=(3, 3), z=25, rate=500, lifetime=16, speed=-45)
    cyl(1.8, 0.02, (0, -6, 0.22), mat("#5a6c80", rough=0.05, wash=False), name="puddle")
    h.head_turn(1, 0, -35); h.set_mouth("o", 1)
    L = S.line(0)
    me = L["chunks"][-1][0]
    h.head_turn(me, 0, -35); h.head_turn(me + 8, 0, 0)
    h.set_mouth("o", me + 8)
    for i, k in enumerate(kids):
        k.idle(1, S.n, phase=i)
        k.head_turn(me, 0, 0)
    cam, t = B.camera(30)
    B.cam_key(cam, t, 1, (0, -26, 14), (0, -6, 6))
    B.cam_key(cam, t, S.n, (0, -21, 8), (0, -6, 4.5))


def wash(S):
    base()
    school(30)
    h = B.hero((0, 0, 0.2))
    B.rain((0, 0), size=(3.4, 3.4), z=22, rate=500, lifetime=16, speed=-45)
    cyl(2.2, 0.02, (0, 0, 0.22), mat("#5a6c80", rough=0.05, wash=False), name="puddle")
    L0, L1 = S.line(0), S.line(1)
    c0 = L0["chunks"]
    # wipe: face by end of "The grey ran down my face", shirt/tie by end of line 0, all by "pink".
    keys = [(1, 6.6), (c0[0][1] + 6, 4.2), (L0["b"], 2.6), (L1["chunks"][1][0], 1.6), (L1["chunks"][-1][1], -0.5)]
    for o in h.parts:
        for f, z in keys:
            o["wash_line"] = 100 - z
            o.keyframe_insert('["wash_line"]', frame=f)
    h.pose(1, "idle")
    h.pose(c0[0][1], "look_hands"); h.head_turn(c0[0][1], 0, 30)
    h.pose(L1["a"], "look_hands")
    h.pose(L1["chunks"][-1][1], "arms_out"); h.head_turn(L1["chunks"][-1][1], 0, 0)
    h.set_mouth("o", 1); h.set_mouth("open", L1["chunks"][-1][1])
    h.eyes_scale(L1["chunks"][-1][1] - 4, 1.0); h.eyes_scale(L1["chunks"][-1][1], 1.3); h.eyes_scale(L1["chunks"][-1][1] + 6, 1.0)
    B.sparkle_burst((0, -0.8, 3.5), L1["chunks"][-1][1], n=18, spread=4)
    B.point((0, -6, 6), 300, (1, 0.6, 0.85), 2)
    cam, t = B.camera(40)
    B.cam_key(cam, t, 1, (0.5, -5.5, 5.4), (0, 0, 4.7))
    B.cam_key(cam, t, L0["b"], (0.5, -8, 4.6), (0, 0, 3.6))
    B.cam_key(cam, t, S.n, (0.5, -14, 4.0), (0, 0, 3.0))


def stare(S):
    base()
    school(30)
    h = B.hero((0, -14, 0.2), rot=0)
    h.colored(True)
    kids = []
    for i, (x, y) in enumerate([(-4.5, -2), (0, 0), (4.5, -1), (-8, 3), (8, 2)]):
        k = B.townie(i, (x, y, 0.2), rot=math.degrees(math.atan2(0 - x, -(-14 - y))))
        k.set_mouth("o", 1); k.eyes_scale(1, 1.25)
        kids.append(k)
    L1 = S.line(1)
    kids[1].talk(L1["a"], L1["mouth"])
    kids[1].set_mouth("o", L1["b"] + 2)
    kids[1].pose(L1["a"], "point")
    kids[1].pose(L1["b"] + 6, "idle")
    # the sandwich drop
    L2 = S.line(2)
    sand = empty("sandwich", (4.5, -2.6, 2.4))
    box((1.0, 1.0, 0.18), (0, 0, 0.0), mat("#e8c98a"), sand)
    box((1.05, 1.05, 0.1), (0, 0, 0.14), mat("#5aa04a"), sand)
    box((1.0, 1.0, 0.18), (0, 0, 0.28), mat("#e8c98a"), sand)
    kids[2].pose(1, "hold")
    sand.keyframe_insert("location", frame=L2["a"])
    sand.location = (4.6, -2.8, 0.3); sand.rotation_euler = (0.6, 0.3, 0.2)
    sand.keyframe_insert("location", frame=L2["a"] + 9); sand.keyframe_insert("rotation_euler", frame=L2["a"] + 9)
    sand.rotation_euler = (0, 0, 0); sand.keyframe_insert("rotation_euler", frame=L2["a"])
    kids[2].pose(L2["a"], "idle")
    cam, t = B.camera(30)
    # over the hero's shoulder onto the crowd
    B.cam_key(cam, t, 1, (4.5, -23, 7.8), (0, 0, 3.6))
    B.cam_key(cam, t, S.n, (3.8, -20.5, 7.4), (0, 0, 3.8))


def sirens(S):
    base(sun_e=2.0)
    B.ground(600)
    B.street(220)
    B.dome()
    h = B.hero((-20, -9, 0.5)); h.colored(True)
    h.walk(1, S.n, (-24, -9, 0.5), (20, -9, 0.5), run=True)
    h.set_mouth("o", 1)
    for i in range(3):
        c = B.inspector("insp%d" % i, (-44 - i * 4, -6 + i * 2, 0.5))
        c.walk(1, S.n, (-46 - i * 4, -6 + i * 2.5, 0.5), (-4 - i * 4, -6 + i * 2.5, 0.5), stride=10, swing=30)
    flash_light((-30, -4, 10), 1, S.n, period=10, energy=5000)
    cam, t = B.camera(30)
    B.cam_key(cam, t, 1, (-20, -30, 5), (-22, -9, 4))
    B.cam_key(cam, t, S.n, (14, -30, 5), (16, -9, 4))


def mom_secret(S):
    base(sun_e=0.8)
    room()
    m = B.mom((0, 0.6, 0), rot=0)
    h = B.hero((0, -2.4, 0), rot=180)
    h.colored(True)
    L0, L1, L2, L3 = (S.line(i) for i in range(4))
    m.pose(1, "idle"); m.pose(L0["a"] + 10, "hands_face"); m.pose(S.n, "hands_face")
    m.root.location.z = -0.9  # kneels
    for i, L in enumerate((L1, L2, L3)):
        m.talk(L["a"], L["mouth"])
    m.brow(1, -12, 0.03)
    h.set_mouth("o", 1); h.set_mouth("flat", L2["a"]); h.eyes_scale(L3["a"], 1.25)
    # cameras: A wide, B on mom over the hero's shoulder, C on the hero
    camA, tA = B.camera(30, "A")
    B.cam_key(camA, tA, 1, (9, -9, 6.5), (0, -0.8, 4))
    B.cam_key(camA, tA, S.n, (8, -8, 6.2), (0, -0.8, 4))
    camB, tB = B.camera(42, "B")
    B.cam_key(camB, tB, 1, (4.4, -9.0, 5.6), (0, 0.6, 3.9))
    B.cam_key(camB, tB, S.n, (3.9, -8.0, 5.4), (0, 0.6, 3.9))
    camC, tC = B.camera(44, "C")
    B.cam_key(camC, tC, 1, (-2.6, 7.0, 6.0), (0, -2.4, 4.6))
    B.cam_key(camC, tC, S.n, (-2.2, 6.2, 5.8), (0, -2.4, 4.6))
    two_cams(S, [(1, camA), (L1["a"] - 2, camB), (L3["a"] - 2, camC), (L3["chunks"][-2][0], camB)])


def knock(S):
    base(sun_e=0.8)
    room(back=10)
    # front door in the back wall, opening inward
    hinge = empty("hinge", (-3, 9.7, 0))
    box((6, 0.4, 9), (3, 0, 4.5), mat("#6e4b32"), hinge, name="door")
    sphere(0.3, (5.3, -0.4, 4.5), mat("#d4af37", metal=1, wash=False), hinge)
    L0, L1 = S.line(0), S.line(1)
    hinge.rotation_euler.z = 0; hinge.keyframe_insert("rotation_euler", frame=L0["b"])
    hinge.rotation_euler.z = math.radians(-100); hinge.keyframe_insert("rotation_euler", frame=L0["b"] + 10)
    # cut a hole in the wall where the door is
    w = bpy.data.objects["backwall"]
    hole = box((6, 3, 9), (0, 10, 4.5), None, name="hole"); hole.hide_render = True; hole.hide_viewport = True
    mod = w.modifiers.new("hole", "BOOLEAN"); mod.object = hole; mod.operation = "DIFFERENCE"
    p = B.prism((0, 13.5, 0), rot=0)
    p.colored(False)
    p.talk(L1["a"], L1["mouth"])
    p.pose(1, "idle"); p.pose(L1["a"], "point"); p.pose(S.n, "point")
    p.brow(L1["a"], 22, -0.02)
    for x in (-4, 4):
        B.inspector("ins%d" % x, (x, 17, 0))
    B.ground(300, loc=(0, 0, -0.05))
    B.point((0, 12, 8), 1500, (1, 0.95, 0.9), 3)
    h = B.hero((2.5, -1, 0), rot=150); h.colored(True)
    cam, t = B.camera(30)
    B.cam_key(cam, t, 1, (-4, -10, 5.5), (0, 9, 5))
    B.cam_key(cam, t, S.n, (-3, -6, 5.3), (0, 10, 5.5))


def escape(S):
    base(sun_e=2.0)
    B.ground(600)
    B.street(200)
    L0, L1 = S.line(0), S.line(1)
    h = B.hero((-14, -9, 0.5)); h.colored(True)
    h.walk(1, L1["a"], (-14, -9, 0.5), (14, -9, 0.5), run=True)
    for x in (-1.8, 1.8):
        c = B.inspector("in%d" % x, (x * 1.4, -9 + (3 if x > 0 else -3), 0.5), rot=-90 if x < 0 else 90)
        c.pose(1, "idle"); c.pose(L0["a"] + 18, "point"); c.pose(L0["a"] + 26, "hold")
    # stairs up the dome (the second half of the shot)
    stairs = empty("stairs", (200, 0, 0))
    for i in range(40):
        box((6, 3, 0.8), (0, i * 2.4, i * 1.6), mat("#9aa6b4", metal=0.5, rough=0.4, wash=False), stairs, name="step")
    for i in range(0, 40, 3):
        box((0.3, 0.3, 4), (3.2, i * 2.4, i * 1.6 + 2), mat("#7d8794", wash=False), stairs)
    h2 = B.hero((200, 0, 0.8)); h2.colored(True)
    f0 = L1["a"]
    for k in range(0, S.n - f0 + 1, 4):
        i = k / 4 * 0.7
        h2.move(f0 + k, (200, i * 2.4, 0.8 + i * 1.6))
    h2.face_dir(f0, 180)
    for k in range(f0, S.n, 6):
        h2.legs(k, 50 if (k // 6) % 2 else -50)
        h2.key_rot(h2.sh[0], k, -50 if (k // 6) % 2 else 50)
        h2.key_rot(h2.sh[1], k, 50 if (k // 6) % 2 else -50)
    camA, tA = B.camera(30, "A")
    B.cam_key(camA, tA, 1, (-6, -28, 4.5), (-8, -9, 3.5))
    B.cam_key(camA, tA, L1["a"], (10, -28, 4.5), (12, -9, 3.5))
    camB, tB = B.camera(26, "B")
    B.cam_key(camB, tB, f0, (214, -10, 3), (200, 4, 5))
    B.cam_key(camB, tB, S.n, (216, 2, 9), (200, 16, 14))
    two_cams(S, [(1, camA), (L1["a"], camB)])


def lever(S):
    base(sky=STORM, sun_e=1.5)
    plat = box((30, 30, 1), (0, 0, -0.5), mat("#8b95a1", metal=0.6, rough=0.35, wash=False), name="platform")
    for x in range(-14, 15, 4):
        box((0.3, 0.3, 3), (x, -14.5, 1.5), mat("#6c7580", wash=False))
    box((29, 0.3, 0.3), (0, -14.5, 3), mat("#6c7580", wash=False))
    B.dome()
    lb = box((4, 3, 3), (0, 4, 1.5), mat("#4b5563", metal=0.4, wash=False), name="leverbase")
    piv = empty("leverpiv", (0, 4, 3))
    piv.rotation_euler.x = math.radians(-35)
    cyl(0.25, 6, (0, 0, 3), mat("#c0c6cc", metal=0.9, rough=0.2, wash=False), piv, name="stick")
    sphere(0.8, (0, 0, 6.2), mat("#e11d2e", rough=0.3, wash=False), piv, name="knob")
    sign = box((7, 0.2, 2.6), (4.2, 3.0, 6.4), mat("#ffffff", wash=False), name="sign")
    text("DO NOT\nOPEN", (0, -0.12, 0), mat("#e11d2e", wash=False), size=0.95, parent=sign, extrude=0.02)
    cyl(0.12, 5, (4.2, 3.1, 2.5), mat("#555555", wash=False))
    h = B.hero((-1.0, -1.5, 0)); h.colored(True)
    L0, L1 = S.line(0), S.line(1)
    h.face_dir(1, 20)
    h.head_turn(L0["chunks"][1][0], -35, -10)
    h.head_turn(L1["a"], 0, 0)
    pull = L1["chunks"][-1][0] + 4
    h.pose(1, "idle"); h.pose(L1["a"], "idle"); h.pose(L1["a"] + 6, "pull")
    h.move(L1["a"] + 6, (-1.0, -1.5, 0)); h.move(pull, (-0.5, 0.2, 0))
    piv.keyframe_insert("rotation_euler", frame=pull)
    piv.rotation_euler.x = math.radians(40); piv.keyframe_insert("rotation_euler", frame=pull + 6)
    h.key_rot(h.sh[0], pull, -95); h.key_rot(h.sh[1], pull, -95)
    h.key_rot(h.sh[0], pull + 6, -20); h.key_rot(h.sh[1], pull + 6, -20)
    h.set_mouth("open", 1); h.brow(pull - 6, 22, -0.03)
    B.sparkle_burst((0, 4, 3.5), pull + 6, n=16, color="#fff2a8", spread=4)
    flash_light((0, 0, 10), pull + 6, S.n, color=(1, 0.2, 0.15), period=10, energy=3000)
    cam, t = B.camera(30)
    B.cam_key(cam, t, 1, (-9, -14, 6), (1, 3, 3.8))
    B.cam_key(cam, t, pull - 2, (-7, -11, 5.5), (1, 3, 3.8))
    B.cam_key(cam, t, S.n, (-5, -8, 4.5), (0.5, 3, 4))


def dome_open(S):
    base(sky=STORM, sun_e=1.4)
    B.ground(1400)
    town_grid(3)
    B.street(160)
    halves = B.dome()
    f_open = 8
    for side, hv in zip((-1, 1), halves):
        hv.keyframe_insert("rotation_euler", frame=f_open)
        hv.keyframe_insert("location", frame=f_open)
        hv.rotation_euler.y = math.radians(side * 32)
        hv.location.x += side * 170
        hv.keyframe_insert("rotation_euler", frame=f_open + 40)
        hv.keyframe_insert("location", frame=f_open + 40)
    B.rain((0, 0), size=(360, 360), z=200, z0=150, rate=9000, f0=f_open, lifetime=50, speed=-70, mesh_scale=5)
    cam, t = B.camera(26)
    B.cam_key(cam, t, 1, (0, -420, 170), (0, 0, 90))
    B.cam_key(cam, t, S.n, (0, -330, 110), (0, 0, 40))


def color_town(S):
    base(sky=STORM, sun_e=2.0)
    B.ground(600)
    B.street(160)
    h = B.hero((0, -8, 0.5)); h.colored(True)
    m = B.mom((-4.5, -6, 0.5), rot=15)
    people = [B.townie(i, (x, y, 0.5), rot=r) for i, (x, y, r) in enumerate([(5, -5, -15), (-9, -2, 10), (9, 0, -10), (-2, 2, 0), (13, -9, -20), (-13, -9, 20)])]
    B.rain((0, -4), size=(60, 40), z=30, rate=2500, lifetime=14, speed=-50)
    sc = bpy.context.scene
    L0 = S.line(0)
    f0, f1 = L0["a"], L0["chunks"][2][1] + 10
    sc["town_line"] = 100 - 30.0; sc.keyframe_insert('["town_line"]', frame=f0)
    sc["town_line"] = 100 + 1.0; sc.keyframe_insert('["town_line"]', frame=f1)
    _, ramp, bg = B.world(**STORM)
    for c in [h, m] + people:
        c.idle(1, S.n, phase=random.random() * 6, arms=False)
    for i, c in enumerate([m] + people):
        c.set_mouth("flat", 1)
        c.pose(1, "idle")
        c.pose(f1 - 6 + i * 2, "cheer"); c.set_mouth("open", f1 - 4 + i * 2)
        c.pose(S.n, "cheer")
    h.pose(1, "idle"); h.pose(f1, "arms_up"); h.pose(S.n, "arms_up")
    B.sparkle_burst((-4.5, -6.8, 4), L0["chunks"][-1][0], n=12, color="#fff38a")
    cam, t = B.camera(28)
    B.cam_key(cam, t, 1, (0, -30, 12), (0, -4, 5))
    B.cam_key(cam, t, S.n, (0, -26, 7), (0, -4, 4.5))


def prism_grey(S):
    base(sky=STORM, sun_e=2.0, town=300)
    B.ground(600)
    bank(0, 16)
    p = B.prism((0, 0, 1.2))
    B.rain((0, 0), size=(14, 14), z=28, rate=900, lifetime=14, speed=-50)
    L0, L1 = S.line(0), S.line(1)
    for o in p.parts:
        o["wash_line"] = 100 - 8.5; o.keyframe_insert('["wash_line"]', frame=L0["chunks"][-1][0])
        o["wash_line"] = 100 - 0.0; o.keyframe_insert('["wash_line"]', frame=L1["a"] + 12)
    p.pose(1, "hips"); p.pose(L0["chunks"][-1][0], "look_hands"); p.pose(L1["a"] + 14, "idle")
    p.set_mouth("open", 1); p.set_mouth("o", L0["chunks"][-1][0]); p.set_mouth("flat", L1["a"] + 16)
    p.brow(L1["a"] + 16, -16, 0.04)
    p.head_turn(L0["chunks"][-1][0], 0, 25)
    p.head_turn(L1["a"] + 14, 0, 0)
    for i, (x, y) in enumerate([(-7, -6), (7, -7)]):
        c = B.townie(i, (x, y, 0.5), rot=180 + (15 if x < 0 else -15))
        c.set_mouth("open", 1)
    cam, t = B.camera(32)
    B.cam_key(cam, t, 1, (0, -20, 5), (0, 0, 5))
    B.cam_key(cam, t, S.n, (0, -12, 5.6), (0, 0, 5.4))


def ending(S):
    base(sky=BLUE_SKY, sun_e=3.4, town=300)
    B.ground(600)
    B.street(160)
    for x in (-30, 30):
        B.tree(x, 10)
    h = B.hero((2.5, -9, 0.5)); h.colored(True)
    p = B.prism((-6, 0.5, 0.5), rot=20, scale=1.0)
    for o in p.parts:
        o["wash_line"] = 300.0  # fully grey now
    bench = box((8, 2, 0.4), (-6, 1.0, 2.0), mat("#8a6a4a"))
    box((8, 0.4, 2), (-6, 2.0, 3.2), mat("#8a6a4a"))
    for dx in (-3.5, 3.5):
        box((0.4, 1.8, 1.8), (-6 + dx, 1.0, 0.9), mat("#5a4a3a"))
    sit(p, 1)
    p.set_mouth("flat", 1); p.brow(1, -16, 0.04)
    p.head_turn(1, 0, 15)
    for i, (x, y) in enumerate([(8, 2), (12, -3), (-15, -6)]):
        c = B.townie(i + 2, (x, y, 0.5), rot=200)
        c.idle(1, S.n, phase=i)
        c.set_mouth("open", 1)
    L0 = S.line(0)
    h.idle(1, S.n, arms=False)
    h.pose(1, "idle")
    h.head_turn(L0["chunks"][1][0], 35, 0)
    h.head_turn(L0["chunks"][-1][0], 0, 0)
    h.pose(L0["chunks"][-1][0], "thumb"); h.pose(S.n, "thumb")
    h.brow(L0["chunks"][-1][0], 18, 0)
    cam, t = B.camera(32)
    B.cam_key(cam, t, 1, (4, -30, 6), (-1, -3, 4))
    B.cam_key(cam, t, S.n, (3, -22, 5.6), (0, -4, 4.3))


SHOT_FUNCS = {
    "town_wide": town_wide, "grey_people": grey_people, "bank": bank_shot, "yellow_drop": yellow_drop,
    "higgins": higgins, "prism": prism_shot, "umbrella": umbrella, "inspectors": inspectors,
    "school_grey": school_grey, "mom_paint": mom_paint, "mom_rule": mom_rule, "crack": crack,
    "rain_me": rain_me, "wash": wash, "stare": stare, "sirens": sirens, "mom_secret": mom_secret,
    "knock": knock, "escape": escape, "lever": lever, "dome_open": dome_open, "color_town": color_town,
    "prism_grey": prism_grey, "ending": ending,
}
