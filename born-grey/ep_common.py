"""Shared sets, props and cast for the Nov 7 episodes (balloon, robot, moon).
Built on the Born Grey toolkit (blib.py, v2/cast.py, v2/shots2.py, v2/mocap.py)."""
import math, os, random, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
for p in (ROOT, os.path.join(ROOT, "v2")):
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
DUSK = dict(top=(0.22, 0.14, 0.42), bottom=(0.95, 0.58, 0.45))
DARK = dict(top=(0.015, 0.02, 0.06), bottom=(0.05, 0.06, 0.14))
SPACE = dict(top=(0.0, 0.0, 0.015), bottom=(0.01, 0.01, 0.04))
CREEPY = dict(top=(0.10, 0.12, 0.20), bottom=(0.25, 0.28, 0.38))
MOONLIGHT = (0.75, 0.85, 1.0)


def colour():
    bpy.context.scene["town_line"] = 300.0


# ------------------------------------------------------------------ sets
def street(sky=DAY, sun=3.2):
    S2.look(sky, sun, 300); B.ground(600); B.street(160); colour()


def night_street(moon_=True):
    street(NIGHT, 0.35)
    B.point((0, -6, 18), 1800, MOONLIGHT, 6)
    stars()
    if moon_:
        moon((-30, 120, 70), 14)


def yard(sky=DAY, sun=3.0):
    S2.look(sky, sun, 300); V1.school(30); colour()


def room(sky=DAY, wall="#d8cbb8", floor="#9a7a5a", light=1.0):
    S2.look(sky, light, 300); V1.room(wall=wall, floor=floor); colour()


def bedroom(night=False, wall="#c5d5ea"):
    room(DARK if night else DAY, wall=wall, floor="#8a6a4a", light=0.25 if night else 1.0)
    box((7, 4.6, 1.4), (-6.5, 3, 0.9), mat("#6e4b32"), name="bed")
    box((7, 4.6, 0.6), (-6.5, 3, 1.9), mat("#7e57c2"), name="blanket")
    box((2.4, 1.6, 0.6), (-8.8, 4.3, 2.4), mat("#ffffff"), name="pillow")
    if night:
        B.point((-5, 4, 11), 500, MOONLIGHT, 3)


def curtains(f_open=None, color="#3949ab", back=8):
    """Curtains over the room window (x=-5). If f_open, they slide apart at that frame."""
    m = mat(color, rough=0.8)
    out = []
    for s in (-1, 1):
        c = box((4.4, 0.3, 7), (-5 + s * 2.1, back - 0.7, 10), m, name="curtain")
        if f_open:
            c.keyframe_insert("location", frame=f_open)
            c.location.x = -5 + s * 6.2
            c.keyframe_insert("location", frame=f_open + 10)
        out.append(c)
    return out


def hospital():
    room(wall="#e8f1f5", floor="#cfd8dc", light=1.3)
    box((6, 3.6, 2.2), (4, 2, 1.1), mat("#ffffff"), name="hbed")
    box((6, 0.3, 3.6), (4, 3.8, 2), mat("#90a4ae"), name="headboard")
    text("+", (-9, 7.6, 14), mat("#e53935", emit=1.2), size=3)


def fair(sky=DAY):
    S2.look(sky, 3.2, 300); colour()
    B.ground(600, "#7fbf6a")
    box((200, 10, 0.12), (0, 0, 0.02), mat("#d7c39a", rough=0.95), name="path")
    ferris((14, 40, 0), 16)
    stripes = ["#e53935", "#fdd835", "#1e88e5", "#8e24aa"]
    for i, x in enumerate((-30, -16, 24, 36)):
        booth(x, 14, stripes[i])
    for i in range(16):
        sphere(0.35, (-40 + i * 5.4, 9, 8 + math.sin(i) * 0.6), mat(stripes[i % 4], emit=2.5, wash=False))
    for x in (-42, 44):
        cyl(0.2, 9, (x, 9, 4.5), mat("#5d4037"))


def ferris(loc, r):
    root = empty("ferris", loc)
    m = mat("#eceff1", metal=0.4, rough=0.4)
    hub = Vector((0, 0, r + 3))
    for k in range(12):
        a = k / 12 * math.tau
        p = hub + Vector((math.cos(a) * r, 0, math.sin(a) * r))
        B._beam(hub, p, 0.25, m, root)
        q = hub + Vector((math.cos(a + math.tau / 12) * r, 0, math.sin(a + math.tau / 12) * r))
        B._beam(p, q, 0.35, m, root)
        box((1.8, 1.6, 1.6), p - Vector((0, 0, 1.2)), mat(["#e53935", "#fdd835", "#1e88e5", "#43a047"][k % 4]), root)
    for s in (-1, 1):
        B._beam(Vector((s * r * 0.6, 0, 0)), hub, 0.6, m, root)
    root.rotation_euler.y = 0
    return root


def booth(x, y, color):
    box((8, 5, 4), (x, y, 2), mat("#fafafa"), name="booth")
    for k in range(4):
        box((2, 5.4, 0.5), (x - 3 + k * 2, y, 6.4 - k * 0.0), mat(color if k % 2 == 0 else "#ffffff"), name="awning")


def sky_set(sky=DAY, sun=3.2, n=14, seed=1, z=0):
    """Up in the air: no ground, clouds around."""
    S2.look(sky, sun, 300); colour()
    rnd = random.Random(seed)
    for i in range(n):
        cloud((rnd.uniform(-60, 60), rnd.uniform(-10, 90), z + rnd.uniform(-25, 25)), rnd.uniform(1.5, 3.5))


def cloud(loc, s=2.0, seed=0):
    rnd = random.Random(seed + int(loc[0] * 7 + loc[2]))
    m = mat("#ffffff", rough=0.95)
    root = empty("cloud", loc)
    for k in range(6):
        sphere(s * rnd.uniform(0.8, 1.3), (rnd.uniform(-2.2, 2.2) * s, rnd.uniform(-0.6, 0.6) * s, rnd.uniform(-0.3, 0.6) * s), m, root,
               scale=(1.3, 1, 0.8), seg=16)
    return root


def stars(n=160, r=220, seed=3):
    rnd = random.Random(seed)
    m = mat("#ffffff", emit=6, wash=False)
    for i in range(n):
        a, e = rnd.uniform(0, math.tau), rnd.uniform(0.05, 1.3)
        p = (r * math.cos(a) * math.cos(e), abs(r * math.sin(a) * math.cos(e)) + 20, r * math.sin(e))
        sphere(rnd.uniform(0.3, 0.8), p, m, seg=6)


def space(n=200):
    S2.look(SPACE, 0.0, 300); colour()
    stars(n, 200)
    stars(n, 200, seed=9)


def moon_surface():
    S2.look(SPACE, 0.0, 300); colour()
    B.sun(2.4, rot=(60, 0, 20), color=MOONLIGHT)
    box((400, 400, 0.2), (0, 0, -0.1), mat("#b7b4aa", rough=0.95), name="moonground")
    rnd = random.Random(5)
    for i in range(30):
        x, y, r = rnd.uniform(-60, 60), rnd.uniform(-10, 120), rnd.uniform(1.5, 6)
        cyl(r, 0.25, (x, y, 0.02), mat("#8f8c84", rough=1), r2=r * 0.85)
    stars(150, 200)
    sphere(9, (50, 160, 40), mat("#3f7fd6", emit=0.6, wash=False))
    sphere(9.05, (50, 159.8, 40), mat("#5fbf5a", emit=0.4, wash=False), scale=(0.6, 0.6, 0.5))


# ------------------------------------------------------------------ props
def moon(loc, r=12, eyes=False, f_eyes=None, mood="calm", parent=None):
    """The full moon: glowing disc-ish sphere with craters; optional face."""
    root = empty("moon", loc, parent)
    sphere(r, (0, 0, 0), mat("#f4f0d8", emit=1.6, wash=False), root, seg=32)
    rnd = random.Random(2)
    for k in range(7):
        a, d = rnd.uniform(0, math.tau), rnd.uniform(0.2, 0.7) * r
        sphere(r * rnd.uniform(0.08, 0.16), (math.cos(a) * d, -r * 0.93, math.sin(a) * d), mat("#cfc9ae", emit=1.0, wash=False), root,
               scale=(1, 0.3, 1))
    if eyes:
        em = mat("#141414", wash=False)
        lids = []
        for s in (-1, 1):
            e = sphere(r * 0.17, (s * r * 0.36, -r * 0.97, r * 0.18), em, root, scale=(1, 0.3, 1.25))
            sphere(r * 0.05, (s * r * 0.36 + r * 0.04, -r * 1.02, r * 0.26), mat("#ffffff", emit=3, wash=False), e and root, scale=(1, 0.3, 1))
            lids.append(e)
            if f_eyes:
                e.scale = (1, 0.3, 0.02); e.keyframe_insert("scale", frame=f_eyes)
                e.scale = (1, 0.3, 1.25); e.keyframe_insert("scale", frame=f_eyes + 8)
        mouth_ = {"calm": None, "smile": 1, "sad": -1}[mood]
        if mouth_:
            for k in range(7):
                t = (k - 3) / 3
                sphere(r * 0.05, (t * r * 0.3, -r * 0.97, -r * 0.3 + mouth_ * (t * t - 1) * r * -0.12), em, root, scale=(1, 0.3, 1))
        if mood == "sad":
            for s in (-1, 1):
                sphere(r * 0.05, (s * r * 0.40, -r * 0.99, -r * 0.05), mat("#7fd3ff", emit=3, wash=False), root, scale=(1, 0.3, 1.6))
    return root


def beam(x, y, top=60, r=3.0, r_top=5.0, f_on=None, color="#fff6c8"):
    """A vertical light beam down from the moon onto (x, y)."""
    m = mat(color, emit=3.0, alpha=0.35, wash=False)
    o = cyl(r, top, (x, y, top / 2), m, r2=r_top, name="beam", verts=32)
    if f_on:
        o.scale = (0.01, 0.01, 1); o.keyframe_insert("scale", frame=f_on)
        o.scale = (1, 1, 1); o.keyframe_insert("scale", frame=f_on + 6)
    B.point((x, y, 6), 2500, (1, 0.96, 0.8), 2)
    return o


def float_up(ch, f0, f1, dz, wobble=True):
    r = ch.root
    z0 = r.location.z
    r.keyframe_insert("location", frame=f0)
    r.location.z = z0 + dz
    r.keyframe_insert("location", frame=f1)
    if wobble:
        ch.key_rot(r, f0, 0, 0, math.degrees(r.rotation_euler.z))
        ch.key_rot(r, f1, 0, 8, math.degrees(r.rotation_euler.z) + 25)
    ch.legs(f0, 15); ch.legs(f0 + 8, -10); ch.legs(f1, 10)


def bob(obj, f0, f1, amp=0.3, period=30, axis=2):
    base = obj.location[axis]
    f = f0
    while f <= f1:
        obj.location[axis] = base + amp * math.sin((f - f0) / period * math.tau)
        obj.keyframe_insert("location", index=axis, frame=f)
        f += period // 4


BALLOON = {"pink": "#ff6fb5", "red": "#e53935", "blue": "#1e88e5", "green": "#43a047", "yellow": "#fdd835",
           "purple": "#8e24aa", "orange": "#fb8c00", "white": "#f5f5f5"}


def balloon(color="pink", loc=(0, 0, 0), size=1.0, parent=None, string_to=None, swaps=()):
    """A balloon. string_to: a local point (in parent space) the string hangs down to.
    swaps: [(frame, color), ...] the balloon changes colour at those frames (mood)."""
    root = empty("balloon", loc, parent)
    cols = [(1, color)] + list(swaps)
    bodies = []
    for i, (f, c) in enumerate(cols):
        o = sphere(1.1 * size, (0, 0, 0), mat(BALLOON.get(c, c), rough=0.25, emit=0.15), root, scale=(1, 1, 1.18), seg=24)
        sphere(0.13 * size, (-0.38 * size, -1.0 * size, 0.5 * size), mat("#ffffff", emit=0.8, wash=False), o, scale=(1, 0.4, 1.5), seg=8)
        bodies.append((f, o))
        cyl(0.16 * size, 0.3 * size, (0, 0, -1.35 * size), mat(BALLOON.get(c, c)), o, r2=0.05)
    for i, (f, o) in enumerate(bodies):
        nxt = bodies[i + 1][0] if i + 1 < len(bodies) else None
        o.hide_render = i != 0; o.keyframe_insert("hide_render", frame=1)
        if i:
            o.hide_render = False; o.keyframe_insert("hide_render", frame=f)
        if nxt:
            o.hide_render = True; o.keyframe_insert("hide_render", frame=nxt)
    if string_to is not None:
        a = Vector((0, 0, -1.45 * size))
        b = Vector(string_to) - Vector(loc)
        B._beam(a, b, 0.05, mat("#f5f5f5", wash=False), root)
    return root


def hold_balloon(ch, color="pink", h=5.2, size=1.0, swaps=(), pose=True):
    """The character holds a balloon on a string in the left hand (balloon rides with the arm)."""
    if pose:
        ch.pose(1, "idle")
    hand = (0, 0, -2.0)
    loc = (0.9, 0, -2.0 + h)
    return balloon(color, loc, size, ch.sh[1], string_to=hand, swaps=swaps)


def balloon_bunch(parent, top=(0, 0, 9), n=12, seed=1, colors=None, hand=(0, 0, -2.0), spread=2.6):
    rnd = random.Random(seed)
    cs = colors or list(BALLOON.keys())
    out = []
    for i in range(n):
        p = (top[0] + rnd.uniform(-spread, spread), top[1] + rnd.uniform(-1, 1), top[2] + rnd.uniform(-1.4, 1.8))
        out.append(balloon(cs[i % len(cs)], p, 0.8, parent, string_to=hand))
    return out


def cotton_candy(parent, loc=(0, -0.6, -2.4)):
    r = empty("candy", loc, parent)
    cyl(0.08, 2.0, (0, 0, 0.6), mat("#ffffff"), r)
    sphere(0.9, (0, 0, 1.9), mat("#f8a5d0", rough=1), r, scale=(1, 1, 1.15))
    return r


def robot(loc=(0, 0, 0), rot=0, eye="#40c4ff", dented=False, scale=1.0, body="#b0bec5", name="robot"):
    """A friendly boxy robot (about kid-sized). Returns a dict: root, head, eyes{color: [objs]}, chest."""
    root = empty(name, loc)
    root.rotation_euler.z = math.radians(rot)
    root.scale = (scale,) * 3
    m = mat(body, metal=0.55, rough=0.35)
    dark = mat("#37474f", metal=0.4, rough=0.4)
    for s in (-1, 1):
        cyl(0.35, 1.6, (s * 0.6, 0, 0.8), dark, root)
        box((0.9, 1.2, 0.4), (s * 0.6, -0.15, 0.2), m, root)
    torso = box((2.4, 1.6, 2.2), (0, 0, 2.7), m, root, bevel=0.12, name="torso")
    chest = box((1.4, 0.1, 0.9), (0, -0.82, 2.8), mat("#263238", rough=0.2), root, name="chest")
    arms = []
    for s in (-1, 1):
        a = empty("arm", (s * 1.45, 0, 3.4), root)
        cyl(0.25, 1.6, (0, 0, -0.8), dark, a)
        sphere(0.38, (0, 0, -1.7), m, a)
        a.rotation_euler.y = math.radians(-s * 12)
        arms.append(a)
    head = empty("rhead", (0, 0, 4.0), root)
    box((2.0, 1.6, 1.5), (0, 0, 0.85), m, head, bevel=0.15, name="rhead")
    cyl(0.06, 0.8, (0.5 if dented else 0, 0, 2.0), dark, head, rot=(0, 25 if dented else 0, 0))
    sphere(0.18, (0.67 if dented else 0, 0, 2.4), mat("#ff5252", emit=3, wash=False), head)
    eyes = {}
    for c in {eye, "#40c4ff", "#ff1744"}:
        eyes[c] = [sphere(0.28, (s * 0.48, -0.78, 0.95), mat(c, emit=5, wash=False), head, scale=(1, 0.4, 1)) for s in (-1, 1)]
        for o in eyes[c]:
            o.hide_render = c != eye
            o.keyframe_insert("hide_render", frame=1)
    box((0.9, 0.06, 0.12), (0, -0.82, 0.45), dark, head, name="rmouth")
    if dented:
        box((0.6, 0.2, 0.4), (-0.7, -0.75, 1.3), mat("#78909c", metal=0.5), head, rot=(0, 20, 0), name="dent")
        box((0.5, 0.05, 0.5), (0.6, -0.84, 2.3), mat("#8d6e63", rough=0.9), root, rot=(0, 0, 0), name="patch")
    return dict(root=root, head=head, eyes=eyes, chest=chest, arms=arms, eye=eye)


def robot_eyes(r, frame, color):
    for c, objs in r["eyes"].items():
        for o in objs:
            o.hide_render = c != color
            o.keyframe_insert("hide_render", frame=frame)


def robot_say(r, f0, word="NOPE", f1=None, color="#69f0ae"):
    """Text lights up on the robot's chest screen."""
    t = text(word, (0, -0.07, -0.05), mat(color, emit=4, wash=False), size=0.42, parent=r["chest"], extrude=0.0)
    t.hide_render = True; t.keyframe_insert("hide_render", frame=1)
    t.hide_render = False; t.keyframe_insert("hide_render", frame=max(1, f0))
    if f1:
        t.hide_render = True; t.keyframe_insert("hide_render", frame=f1)
    head_tilt(r, f0, 0, 12)
    return t


def head_tilt(r, f, yaw=0, roll=0, pitch=0):
    h = r["head"]
    h.keyframe_insert("rotation_euler", frame=max(1, f - 3))
    h.rotation_euler = (math.radians(pitch), math.radians(roll), math.radians(yaw))
    h.keyframe_insert("rotation_euler", frame=f + 3)


def robot_walk(r, f0, f1, a, b):
    root = r["root"]
    root.location = a; root.keyframe_insert("location", frame=f0)
    root.location = b; root.keyframe_insert("location", frame=f1)
    for k, arm in enumerate(r["arms"]):
        f = f0
        while f <= f1:
            arm.rotation_euler.x = math.radians(25 * (1 if (f // 8 + k) % 2 else -1))
            arm.keyframe_insert("rotation_euler", frame=f)
            f += 8


def robot_arm(r, f, side=1, x=-90, y=0):
    a = r["arms"][0 if side < 0 else 1]
    a.keyframe_insert("rotation_euler", frame=max(1, f - 4))
    a.rotation_euler = (math.radians(x), math.radians(y), 0)
    a.keyframe_insert("rotation_euler", frame=f + 2)


def big_screen(lines_, loc=(0, 6, 9), w=16, h=9, ink="#40c4ff", size=1.1, bg="#0d1b2a"):
    root = empty("screen", loc)
    box((w + 0.6, 0.6, h + 0.6), (0, 0.2, 0), mat("#263238"), root)
    box((w, 0.2, h), (0, -0.2, 0), mat(bg, emit=0.6, wash=False), root)
    text(lines_, (0, -0.35, 0), mat(ink, emit=4, wash=False), size=size, parent=root, extrude=0.0)
    return root


# ------------------------------------------------------------------ cast
def milo(loc=(0, 0, 0), rot=0, face="happy"):
    c = C.Side("milo", loc, rot, dict(skin_key="light", face=face, skin="#ffd6aa", top="#4fc3f7", pants="#1565c0",
                                      shoes="#333333", hair="#8d5524", hair_style="short"), scale=0.62)
    c.colored(True)
    return c


def dad(loc=(0, 0, 0), rot=0, face="calm"):
    return C.adult(3, loc, rot, face=face, top="#6d4c41", pants="#37474f", tie="#2e7d32")


def doctor(loc=(0, 0, 0), rot=0, face="happy"):
    return C.adult(2, loc, rot, face=face, top="#ffffff", pants="#90a4ae", tie="#0288d1")


def teacher(loc=(0, 0, 0), rot=0, face="side_eye"):
    return C.adult(1, loc, rot, face=face, top="#8e24aa", pants="#4a148c", tie="#fdd835")


def turn180(c):
    c.root.rotation_euler.z = math.radians(180)
    return c


def crowd(n, y=6, x0=-14, dx=4.2, face="calm", kids=True, start=0, rot=0, z=0.2, spread=0.0):
    rnd = random.Random(n + start)
    out = []
    for i in range(n):
        p = (x0 + i * dx, y + rnd.uniform(-spread, spread), z)
        c = (C.kid if kids else C.adult)(start + i, p, rot, face=face)
        if kids:
            c.colored(True)
        out.append(c)
    return out


def shot_table(g, aliases=None):
    """Map each [marker] in lines.py to a function in the episode module g (globals())."""
    import re
    from lines import SCRIPT
    ids = re.findall(r"\[(\w+)\]", " ".join(SCRIPT))
    out = {}
    for k in ids:
        f = (aliases or {}).get(k, g.get(k))
        assert callable(f), k
        out[k] = f
    return out


def push(S, tgt=(0, 0, 4.4), d=10, lens=34, side=0.3, up=0.6, dolly=1.4):
    """Standard slow push-in on a target from the front (-Y)."""
    x, y, z = tgt
    return cam(S, (x + side, y - d, z + up), (x + side * 0.5, y - d + dolly, z + up * 0.7), tgt, lens=lens)


def wide(S, tgt=(0, 0, 4), d=26, h=9, lens=28, pan=8):
    x, y, z = tgt
    return cam(S, (x - pan, y - d, h), (x + pan * 0.4, y - d + 3, h - 1), tgt, lens=lens)


def desk(x=0, y=2):
    box((7, 3.4, 0.3), (x, y, 3.0), mat("#8d6e63"), name="desk")
    for dx in (-3.1, 3.1):
        box((0.4, 3, 3.0), (x + dx, y, 1.5), mat("#6d4c41"))


def tv(lines_, loc=(0, 7, 6), ink="#40c4ff", w=10, h=6, size=0.9, bg="#0d1b2a"):
    return big_screen(lines_, loc, w, h, ink, size, bg)
