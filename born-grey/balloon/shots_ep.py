"""Balloon episode shots: one function per [marker] in lines.py."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from ep_common import *


def grandpa(loc=(0, 0, 0), rot=0, face="smug"):
    g = C.Side("grandpa", loc, rot, dict(skin_key="pale", face=face, skin="#fae2c8", top="#8d6e63", pants="#5d4037",
                                         shoes="#3a3a3a", hair="#e0e0e0", hair_style="short"), scale=1.0)
    g.colored(True)
    return g


def rise(o, f0, f1, dz, dx=0.0):
    o.keyframe_insert("location", frame=f0)
    o.location.z += dz; o.location.x += dx
    o.keyframe_insert("location", frame=f1)


def birds(n=6, center=(0, 10, 30), f1=200, seed=2):
    rnd = random.Random(seed)
    m = mat("#263238", wash=False)
    for i in range(n):
        r = empty("bird", (center[0] + rnd.uniform(-12, 12), center[1] + rnd.uniform(-4, 8), center[2] + rnd.uniform(-5, 5)))
        for s in (-1, 1):
            w = box((1.2, 0.3, 0.12), (s * 0.55, 0, 0), m, r, rot=(0, -s * 20, 0))
        rise(r, 1, f1, 0, 18)


def free_balloon(color, loc, size=1.0):
    return balloon(color, loc, size, None, string_to=(loc[0], loc[1], loc[2] - 4.5 * size))


# ---------------------------------------------------------------- the world
def town(S):
    street()
    cols = ["pink", "yellow", "blue", "green", "orange"]
    for i, x in enumerate((-12, -5, 2, 9)):
        c = (C.adult if i % 2 else C.kid)(i, (x, -9, 0.5), face="happy")
        c.walk(1, S.n + 10, (x - 4, -9, 0.5), (x + 5, -9, 0.5), stride=10, arms=False)
        hold_balloon(c, cols[i], pose=False)
    wide(S, (0, -9, 5), 28, 9)


def hospital_(S):
    hospital()
    m = C.mom((4, 2, 2.0), rot=-30, face="happy"); m.colored(True); V1.sit(m, 1)
    d = doctor((-1.2, -0.5, 0), rot=-20, face="happy")
    balloon("pink", (0.9, -0.4, 6.2), 0.5, None, string_to=(0.3, -0.6, 3.0))
    B.sparkle_burst((0.6, -0.6, 4.5), 3, n=10, color="#ffd1ea", spread=1.5)
    push(S, (1, 0, 4), 14, 32)


def mood(S):
    street()
    h = C.hero((0, 0, 0.5), face="happy")
    q = max(4, S.n // 4)
    hold_balloon(h, "pink", swaps=[(q, "yellow"), (2 * q, "purple"), (3 * q, "orange")])
    push(S, (0.6, 0, 5.5), 12, 32)


def mad_red(S):
    yard()
    k = C.kid(1, (0, 0, 0.2), face="angry")
    hold_balloon(k, "pink", swaps=[(S.word("red"), "red")])
    push(S, (0.5, 0, 5), 11, 32)


def sad_blue(S):
    yard()
    k = C.kid(2, (0, 0, 0.2), face="sad")
    hold_balloon(k, "pink", swaps=[(S.word("blue"), "blue")])
    push(S, (0.5, 0, 5), 11, 32)


def teacher_(S):
    room(wall="#e8f5e9")
    box((10, 0.2, 5), (0, 7.6, 7), mat("#2e7d32"), name="board")
    text("2 + 2 = ?", (0, 7.4, 7), mat("#ffffff", wash=False), size=1.0)
    t = teacher((1.4, 0, 0), rot=-30, face="side_eye"); t.pose(1, "point")
    k = C.kid(3, (-1.4, -0.5, 0), rot=30, face="nervous")
    hold_balloon(k, "yellow")
    push(S, (0, 0, 5), 14, 30)


def lie_green(S):
    room(wall="#e8f5e9")
    k = C.kid(3, (0, 0, 0), face="nervous")
    hold_balloon(k, "yellow", swaps=[(S.word("green"), "green")])
    push(S, (0.6, 0, 5.2), 11, 32)


def grandpa_(S):
    street()
    g = grandpa((0, 0, 0.5), face="smug")
    hold_balloon(g, "purple", h=9, size=3.0)
    cam(S, (2, -22, 7), (1, -19, 8), (1, 0, 8), lens=30)


def grandpa_door(S):
    street()
    B.house(0, 10, w=12, d=8, h=8, wall="#e8d5b5")
    g = grandpa((0, 4.5, 0.5), rot=0, face="puffed")
    g.root.rotation_euler.z = math.radians(180)
    balloon("purple", (0, 4.5, 11), 4.0, None, string_to=(0.4, 4.0, 2.5))
    push(S, (0, 4, 7), 22, 30)


def sign_rule(S):
    street()
    sign("NEVER LET GO\nOF YOUR\nBALLOON", (0, 0, 6.5), w=11, size=0.9)
    free_balloon("pink", (4.5, 0.5, 11), 1.0)
    cam(S, (2, -13, 4.5), (-1, -11, 5), (0, 0, 6.8), lens=34)


def rule_grip(S):
    street()
    h = C.hero((0, 0, 0.5), face="determined")
    hold_balloon(h, "pink")
    cam(S, (1.8, -5, 3.4), (1.6, -4.2, 3.6), (1.0, 0, 3.4), lens=40)


def float_away(S):
    street(DUSK, 2.0)
    a = C.adult(4, (0, 0, 2), face="scared")
    hold_balloon(a, "orange")
    float_up(a, 1, S.n, 14)
    cam(S, (0, -20, 3), (0, -20, 6), (0, 0, 8), (0, 0, 14), lens=30)


def hero(S):
    street()
    h = C.hero((0, 0, 0.5), face="calm")
    hold_balloon(h, "pink")
    push(S, (0.6, 0, 5.4), 12, 32)


def hero_knot(S):
    street()
    h = C.hero((0, 0, 0.5), face="smug")
    hold_balloon(h, "pink")
    B.sparkle_burst((1.2, -0.6, 3.0), 3, n=10, color="#ffd1ea", spread=1.0)
    cam(S, (1.6, -6, 4.2), (1.4, -5, 4.0), (0.8, 0, 3.6), lens=36)


def milo_(S):
    yard()
    m = milo((0, 0, 0.2), face="happy")
    hold_balloon(m, "blue", h=6)
    push(S, (0.4, 0, 3.6), 10, 34)


def milo_jump(S):
    yard()
    m = milo((0, 0, 0.2), face="laugh")
    hold_balloon(m, "blue", h=6)
    f = 1
    while f < S.n:
        m.move(f, (0, 0, 0.2)); m.move(f + 5, (0, 0, 1.6)); m.legs(f + 5, 20); m.legs(f + 10, 0); f += 10
    m.move(f, (0, 0, 0.2))
    push(S, (0.4, 0, 3.6), 11, 34)


# ---------------------------------------------------------------- the fair
def fair_(S):
    fair()
    m = C.mom((-3, -2, 0), face="happy"); m.colored(True)
    h = C.hero((0, -2, 0), face="happy")
    k = milo((2.6, -2, 0), face="laugh")
    for c, col, f in ((m, "yellow", 0), (h, "pink", 3), (k, "blue", 6)):
        c.walk(1, S.n, (c.root.location.x - 4, -2, 0), (c.root.location.x + 4, -2, 0), stride=10, arms=False)
        hold_balloon(c, col, pose=False)
    wide(S, (0, -2, 6), 26, 7)


def cotton(S):
    fair()
    booth(0, 4, "#ec407a")
    for x in (-2, 0, 2):
        cotton_candy(None, (x, 1.3, 4.2))
    k = milo((1.5, -1.5, 0), rot=150, face="little_o"); turn180(k)
    hold_balloon(k, "blue", h=6)
    push(S, (0.5, 0, 4), 13, 32)


def two_hands(S):
    fair()
    k = milo((0, 0, 0), face="happy")
    k.pose(S.word("both"), "hold")
    cotton_candy(None, (0, -2.2, 2.5))
    free_balloon("blue", (0.6, 0, 6.6), 1.0)
    push(S, (0, -0.5, 3.4), 10, 34)


def let_go(S):
    fair()
    k = milo((0, 0, 0), face="surprised"); k.pose(1, "hold")
    b = free_balloon("blue", (0.6, 0, 6.6), 1.0)
    rise(b, 4, S.n, 6, 1)
    k.head_turn(8, 0, -25)
    push(S, (0, 0, 4), 10, 34)


def lift(S):
    fair()
    k = milo((0, 0, 0.1), face="scared"); k.pose(1, "point_up")
    hold_balloon(k, "blue", h=6, pose=False)
    float_up(k, 3, S.n, 7)
    cam(S, (0, -10, 2), (0, -10, 3), (0, 0, 3), (0, 0, 7), lens=32)


def up_rides(S):
    fair()
    k = milo((10, 30, 16), face="scared"); k.pose(1, "point_up")
    hold_balloon(k, "blue", h=6, pose=False)
    float_up(k, 1, S.n, 14)
    cam(S, (0, -20, 2), (0, -20, 3), (8, 30, 18), (8, 30, 26), lens=28)


def up_clouds(S):
    sky_set(DAY, 3.2, n=12, seed=4, z=40)
    k = milo((0, 0, 36), face="scared")
    hold_balloon(k, "blue", h=6)
    float_up(k, 1, S.n, 8)
    cam(S, (0, -18, 34), (0, -18, 40), (0, 0, 38), (0, 0, 46), lens=28)


def mom_scream(S):
    fair()
    m = C.mom((0, 0, 0), face="shocked"); m.colored(True); m.pose(1, "scared")
    m.head_turn(1, 0, -25)
    hold_balloon(m, "yellow", pose=False)
    push(S, (0.4, 0, 5), 10, 34)


def nobody(S):
    fair()
    for i, x in enumerate((-6, -3, 0, 3, 6)):
        c = (C.adult if i % 2 else C.kid)(i, (x, (i % 2) * 2, 0), face="sad")
        c.head_turn(1, 0, -20)
    wide(S, (0, 0, 4), 22, 4)


def hero_look(S):
    fair()
    h = C.hero((0, 0, 0), face="determined")
    hold_balloon(h, "pink")
    h.head_turn(4, 15, -25)
    push(S, (0.8, 0, 5.6), 11, 32)


def hero_think(S):
    fair()
    h = C.hero((0, 0, 0), face="side_eye")
    hold_balloon(h, "pink")
    h.set_face(S.word("faster"), "determined")
    push(S, (0, 0, 4.8), 7, 38)


def more(S):
    fair()
    booth(3, 6, "#ec407a")
    balloon_bunch(None, (3, 6, 10), n=16, hand=(3, 5, 4))
    h = C.hero((-1.5, -1, 0), face="determined")
    push(S, (0.5, 2, 5.5), 15, 30)


def stand(S):
    fair()
    booth(6, 6, "#ec407a")
    balloon_bunch(None, (6, 6, 10), n=16, hand=(6, 5, 4))
    h = C.hero((-6, -1, 0), face="determined")
    h.walk(1, S.n, (-8, -1, 0), (3, 2, 0), run=True)
    cam(S, (-6, -16, 5), (2, -14, 5), (-4, 0, 5), (4, 2, 5), lens=30)


def grab_all(S):
    fair()
    h = C.hero((0, 0, 0), face="smug"); h.pose(1, "idle")
    balloon_bunch(h.sh[1], (0.9, 0, 6.5), n=18, seed=3)
    push(S, (0.4, 0, 6.5), 17, 30)


def mom_no(S):
    fair()
    m = C.mom((0, 0, 0), face="angry"); m.colored(True); m.pose(1, "wag")
    push(S, (0, 0, 5.2), 9, 36)


def hero_sorry(S):
    fair()
    h = C.hero((0, 0, 0), face="nervous"); h.pose(1, "idle")
    balloon_bunch(h.sh[1], (0.9, 0, 6.5), n=18, seed=3)
    h.set_face(S.word("mom"), "wink")
    push(S, (0.4, 0, 6), 14, 32)


# ---------------------------------------------------------------- flying
def flyer(loc, face="determined", n=18):
    h = C.hero(loc, face=face); h.pose(1, "idle")
    balloon_bunch(h.sh[1], (0.9, 0, 6.5), n=n, seed=3)
    return h


def jump(S):
    fair()
    h = flyer((0, 0, 0), "determined")
    h.legs(1, 0); h.move(1, (0, 0, 0)); h.move(6, (0, 0, -0.4)); h.legs(6, 30); h.move(12, (0, 0, 5)); h.legs(12, -10)
    h.move(S.n, (0, 0, 8))
    cam(S, (0, -16, 3), (0, -16, 5), (0, 0, 6), (0, 0, 9), lens=28)


def fly(S):
    fair()
    h = flyer((0, 0, 8), "happy")
    float_up(h, 1, S.n, 10)
    cam(S, (8, -18, 4), (6, -16, 8), (0, 0, 12), (0, 0, 18), lens=30)


def higher(S):
    fair()
    h = flyer((10, 25, 34), "happy")
    float_up(h, 1, S.n, 6)
    cam(S, (16, -2, 40), (14, 0, 44), (10, 30, 30), (10, 30, 34), lens=26)


def birds_(S):
    sky_set(DAY, 3.2, n=8, seed=7, z=50)
    h = flyer((0, 0, 50), "laugh")
    birds(6, (0, 4, 54), S.n + 20)
    float_up(h, 1, S.n, 3)
    push(S, (0.5, 0, 55), 22, 30)


def cloud_hero(S):
    sky_set(DAY, 3.2, n=6, seed=8, z=70)
    for x in range(-12, 13, 4):
        cloud((x, 0, 66), 2.6, seed=x)
    h = flyer((0, 2, 58), "surprised")
    float_up(h, 1, S.n, 12)
    cam(S, (0, -20, 70), (0, -20, 72), (0, 2, 68), lens=30)


def find(S):
    sky_set(DAY, 3.2, n=10, seed=9, z=80)
    h = flyer((-2, 0, 80), "surprised")
    cloud((10, 20, 78), 3.0)
    h.head_turn(1, -30, 0)
    cam(S, (-6, -18, 84), (-4, -16, 84), (2, 8, 82), lens=30)


def milo_cloud(S):
    sky_set(DAY, 3.2, n=8, seed=10, z=80)
    cloud((0, 0, 79), 3.2)
    k = milo((0, 0, 81), face="happy"); V1.sit(k, 1)
    cotton_candy(k.sh[0], (0, -0.6, -1.6))
    push(S, (0, 0, 83), 11, 32)


def milo_hi(S):
    sky_set(DAY, 3.2, n=8, seed=10, z=80)
    cloud((0, 0, 79), 3.2)
    k = milo((0, 0, 81), face="laugh"); k.pose(2, "wave")
    push(S, (0, 0, 83), 8, 36)


def hold_hand(S):
    sky_set(DAY, 3.2, n=8, seed=11, z=80)
    cloud((0, 1, 79), 3.2)
    k = milo((1.0, 0, 81), rot=-30, face="happy"); k.pose(1, "hold")
    h = flyer((-1.2, -0.2, 81), "happy"); h.root.rotation_euler.z = math.radians(30)
    h.key_rot(h.sh[0], 1, -60)
    push(S, (0, 0, 84), 15, 30)


def pop(S):
    sky_set(DAY, 3.2, n=8, seed=12, z=80)
    h = C.hero((-1.2, 0, 80), face="determined"); h.pose(1, "idle")
    bs = balloon_bunch(h.sh[1], (0.9, 0, 6.5), n=12, seed=3)
    k = milo((1.0, 0, 80), face="surprised")
    step = max(2, (S.n - 6) // len(bs))
    for i, b in enumerate(bs):
        f = 4 + i * step
        b.hide_render = False; b.keyframe_insert("hide_render", frame=1)
        b.hide_render = True; b.keyframe_insert("hide_render", frame=f)
        for ch in b.children_recursive:
            ch.hide_render = False; ch.keyframe_insert("hide_render", frame=1)
            ch.hide_render = True; ch.keyframe_insert("hide_render", frame=f)
    B.sparkle_burst((0, -0.5, 88), 4, n=14, color="#ffffff", spread=3)
    push(S, (0, 0, 84), 17, 30)


def down(S):
    fair()
    h = C.hero((-1.2, 0, 24), face="happy"); h.pose(1, "idle")
    balloon_bunch(h.sh[1], (0.9, 0, 6.5), n=3, seed=3)
    k = milo((1.0, 0, 24), face="happy"); k.pose(1, "hold")
    for c in (h, k):
        float_up(c, 1, S.n, -8, wobble=False)
    cam(S, (0, -18, 22), (0, -18, 16), (0, 0, 26), (0, 0, 20), lens=30)


def land(S):
    fair()
    h = C.hero((-1.2, 0, 4), face="happy"); h.pose(1, "idle")
    balloon_bunch(h.sh[1], (0.9, 0, 6.5), n=2, seed=3)
    k = milo((1.0, 0, 4), face="happy")
    for c in (h, k):
        float_up(c, 1, min(S.n, 14), -4, wobble=False)
    m = C.mom((0, 4, 0), rot=180, face="surprised"); m.colored(True); turn180(m)
    push(S, (0, 1, 4), 15, 30)


def mom_hug(S):
    fair()
    m = C.mom((0, 0.6, 0), face="sad"); m.colored(True); m.pose(1, "hands_face")
    m.set_face(S.word("hard"), "happy")
    h = C.hero((-1.3, -0.6, 0), rot=-20, face="happy")
    k = milo((1.2, -0.6, 0), rot=20, face="happy")
    push(S, (0, 0, 4.4), 14, 30)


def mom_red(S):
    fair()
    m = C.mom((0, 0, 0), face="happy"); m.colored(True)
    hold_balloon(m, "yellow", swaps=[(S.word("red"), "red")])
    m.set_face(S.word("red"), "angry")
    push(S, (0.6, 0, 6), 13, 32)


def ending(S):
    street()
    k = milo((1.1, 0, 0.5), face="happy")
    hold_balloon(k, "blue", h=6)
    B.sparkle_burst((1.6, -0.6, 2.4), 3, n=8, color="#bbdefb", spread=0.8)
    h = C.hero((-1.2, 0, 0.5), face="happy")
    hold_balloon(h, "pink")
    push(S, (0, 0, 4.4), 14, 30)


def ending_candy(S):
    street()
    h = C.hero((-1.2, 0, 0.5), face="happy"); h.pose(1, "hold")
    cotton_candy(h.sh[0], (0, -0.6, -2.2))
    hold_balloon(h, "pink", pose=False)
    k = milo((1.1, 0, 0.5), face="laugh"); k.pose(1, "hold")
    free_balloon("blue", (1.1, -1.2, 6.8), 1.0)
    h.set_face(S.word("him") if S.word("him") > 1 else S.n - 12, "wink")
    push(S, (0, 0, 4.4), 13, 30)


ALIASES = {"hospital": hospital_, "teacher": teacher_, "grandpa": grandpa_, "milo": milo_, "fair": fair_, "birds": birds_}


def shot_funcs():
    return shot_table(globals(), ALIASES)
