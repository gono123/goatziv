"""Robot episode shots: one function per [marker] in lines.py."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from ep_common import *

BLUE_EYE, RED_EYE = "#40c4ff", "#ff1744"


def mine(loc=(1.3, 0, 0), rot=0, eye=BLUE_EYE, scale=0.8):
    return robot(loc, rot, eye=eye, dented=True, scale=scale, body="#cfd8dc", name="mine")


def pips(loc=(1.4, 0, 0.2), rot=0, eye=BLUE_EYE):
    return robot(loc, rot, eye=eye, scale=0.85, body="#ffca28", name="pipbot")


def bots(n, y=4, x0=-12, dx=6, eye=BLUE_EYE, z=0.2, scale=0.8, rows=1, dy=5):
    cols = ["#b0bec5", "#ffca28", "#81d4fa", "#a5d6a7", "#f48fb1", "#ce93d8"]
    return [robot((x0 + i * dx, y - r * dy, z), 0, eye=eye, scale=scale, body=cols[(i + r) % 6]) for r in range(rows) for i in range(n)]


# ---------------------------------------------------------------- the world
def town(S):
    street()
    for i, x in enumerate((-10, -2, 7)):
        k = C.kid(i, (x, -9, 0.5), face="happy")
        k.walk(1, S.n + 10, (x - 4, -9, 0.5), (x + 5, -9, 0.5), stride=10)
        r = robot((x - 2.2, -8, 0.5), 0, scale=0.75, body=["#b0bec5", "#81d4fa", "#a5d6a7"][i])
        robot_walk(r, 1, S.n + 10, (x - 6.2, -8, 0.5), (x + 2.8, -8, 0.5))
    wide(S, (0, -8, 4.5), 28, 8)


def crib(S):
    bedroom()
    box((5, 3, 2.6), (0, 2, 1.3), mat("#ffffff"), name="crib")
    for x in range(-2, 3):
        cyl(0.1, 2.0, (x, 0.45, 3.6), mat("#ffffff"))
    r = robot((0, 2, 2.6), 0, scale=0.45, body="#b0bec5")
    robot_arm(r, 10, 1, 0, -150); robot_arm(r, 20, 1, 0, -110); robot_arm(r, 30, 1, 0, -150)
    m = C.mom((-4, -1.5, 0), rot=-40, face="happy"); m.colored(True)
    d = dad((4.2, -1.5, 0), rot=40, face="happy")
    B.sparkle_burst((0, 1, 5), 4, n=10, color="#bbdefb")
    push(S, (0, 1, 3.6), 15, 32)


def homework(S):
    room()
    desk(1.5, 1)
    r = robot((1.5, 3.4, 0), 180, scale=0.75); r["root"].rotation_euler.z = math.radians(180)
    for f in range(1, S.n, 8):
        robot_arm(r, f, 1, -70 if (f // 8) % 2 else -55)
    V1.paper(r["arms"][1], (0, 0, -1.9), "A+")
    k = C.hero((-4, -1, 0), rot=30, face="happy"); V1.sit(k, 1); k.pose(1, "hips")
    push(S, (-1, 1, 3.6), 16, 30)


def clean(S):
    room()
    r = robot((0, 0.5, 0), 0, scale=0.8)
    broom = cyl(0.1, 4, (0, -0.4, -2.2), mat("#a1887f"), r["arms"][1])
    for f in range(1, S.n, 10):
        robot_arm(r, f, 1, -40, 25 if (f // 10) % 2 else -25)
    for i, (x, c) in enumerate(((-3, "#e53935"), (3, "#fdd835"), (-1.5, "#1e88e5"))):
        o = box((0.8, 0.8, 0.8), (x, -1.5, 0.4), mat(c)); o.keyframe_insert("location", frame=1)
        o.location = (6, 4, 0.4); o.keyframe_insert("location", frame=S.n - i * 6)
    push(S, (0, 0, 2.8), 11, 32)


def lunch(S):
    room(wall="#fff3e0")
    box((8, 4, 0.3), (0, 1.5, 3.0), mat("#a1887f"))
    r = robot((2.2, 0.5, 0), -40, scale=0.8)
    box((1.4, 0.8, 1.0), (0, -0.4, -2.3), mat("#e53935"), r["arms"][0], name="lunchbox")
    robot_arm(r, 4, -1, -80)
    k = C.kid(1, (-2.2, 0, 0), rot=40, face="happy")
    push(S, (0, 0, 3.8), 14, 32)


def talk(S):
    street()
    k = C.kid(2, (-1.5, 0, 0.5), rot=-50, face="laugh")
    r = robot((1.6, 0, 0.5), 50, scale=0.75)
    for f in range(1, S.n, 10):
        head_tilt(r, f, 0, 10 if (f // 10) % 2 else -10)
    push(S, (0, 0, 3.8), 13, 34)


def million(S):
    street()
    big_screen("1,000,000\nWORDS", (0, 8, 7), w=14, h=7, ink="#69f0ae", size=1.5)
    r = robot((0, -1, 0.5), 0, scale=0.8)
    robot_say(r, 1, "HELLO")
    push(S, (0, 3, 5), 16, 30)


def pip_robot(S):
    yard()
    p = C.pip((-1.1, 0, 0.2), rot=-30, face="smug", lace=None); p.colored(True); p.pose(1, "hips")
    r = pips((1.4, 0, 0.2), 30)
    for i, (w, c) in enumerate((("HOLA", "#ff7043"), ("BONJOUR", "#42a5f5"), ("CIAO", "#66bb6a"), ("HALLO", "#ab47bc"))):
        t = text(w, (-3 + i * 2.2, -1, 7 + (i % 2)), mat(c, emit=2, wash=False), size=0.7)
        t.hide_render = True; t.keyframe_insert("hide_render", frame=1)
        t.hide_render = False; t.keyframe_insert("hide_render", frame=1 + i * 6)
    push(S, (0, 0, 4.4), 13, 32)


def pip_joke(S):
    yard()
    r = pips((1.4, 0, 0.2), 30)
    robot_say(r, 1, "HA HA", color="#ffd54f")
    p = C.pip((-1.1, 0, 0.2), rot=-30, face="laugh", lace=None); p.colored(True)
    for i, x in enumerate((-5, 5.5)):
        C.kid(i, (x, 2, 0.2), face="laugh")
    push(S, (0, 0, 4), 14, 32)


def hero(S):
    street()
    h = C.hero((0, 0, 0.5), face="calm")
    push(S, (0, 0, 4.8), 8, 38)


def hero_box(S):
    room()
    b = box((3.6, 3, 3.2), (1.8, 0, 1.6), mat("#c49a6c", rough=0.9), rot=(0, 0, 8), name="box")
    box((1.2, 0.2, 0.8), (2.6, -1.5, 2.6), mat("#a1785a"), rot=(0, 30, 0), name="dent")
    text("ROBO", (1.6, -1.6, 1.4), mat("#5d4037"), size=0.6)
    h = C.hero((-1.4, 0, 0), rot=-30, face="side_eye")
    push(S, (0, 0, 3.6), 11, 32)


def bolt(S):
    room()
    box((3.6, 3, 3.2), (0, 1, 1.6), mat("#c49a6c", rough=0.9), name="box")
    o = cyl(0.2, 0.6, (0.6, -0.8, 2.8), mat("#90a4ae", metal=0.8, rough=0.3), rot=(90, 0, 0), name="bolt")
    o.keyframe_insert("location", frame=1); o.keyframe_insert("rotation_euler", frame=1)
    o.location = (1.4, -2.2, 0.25); o.rotation_euler = (math.radians(90), math.radians(300), 0)
    o.keyframe_insert("location", frame=min(S.n, 12)); o.keyframe_insert("rotation_euler", frame=min(S.n, 12))
    cam(S, (0.8, -6, 2.2), (0.9, -5.4, 1.6), (1.0, -1.5, 1.2), lens=40)


def robot_on(S):
    room()
    r = mine((1.2, 0, 0), -20, scale=0.85)
    robot_eyes(r, 1, None); robot_eyes(r, S.word("on"), BLUE_EYE)
    h = C.hero((-1.4, -0.5, 0), rot=-50, face="little_o"); h.pose(S.word("on") - 4, "point")
    push(S, (0, 0, 3.8), 13, 32)


def nope_first(S):
    room()
    r = mine((0, 0, 0), 0, scale=0.9)
    robot_say(r, S.word("nope"))
    push(S, (0, 0, 3.8), 6, 40)


def only_word(S):
    room()
    h = C.hero((-1.1, 0, 0), rot=-25, face="shocked"); h.pose(1, "hips")
    r = mine((1.4, 0, 0), -20)
    robot_say(r, 1)
    push(S, (0, 0, 4.4), 12, 36)


def homework_nope(S):
    room()
    h = C.hero((-1.1, 0, 0), rot=-50, face="nervous"); h.pose(1, "hold")
    V1.paper(h.sh[0], (0, -0.5, -2.2), "HW")
    r = mine((1.4, 0, 0), 40)
    robot_say(r, S.word("nope"))
    push(S, (0, 0, 4), 13, 34)


def clean_nope(S):
    room()
    for i in range(8):
        box((0.9, 0.9, 0.9), (-6 + i * 1.7, -2 + (i % 3), 0.45), mat(["#e53935", "#fdd835", "#1e88e5", "#43a047"][i % 4]), rot=(0, 0, i * 20))
    h = C.hero((-1.1, 0, 0), rot=-40, face="puffed"); h.pose(1, "point")
    r = mine((1.4, 0, 0), 40)
    robot_say(r, S.word("nope"))
    push(S, (0, 0, 4), 13, 32)


def laugh(S):
    yard()
    h = C.hero((0, 0, 0.2), face="sad")
    r = mine((2.4, 0.5, 0.2))
    for i, (x, y) in enumerate(((-6, 2), (-3.5, 4), (5.5, 3), (7.5, 1))):
        k = C.kid(i, (x, y, 0.2), rot=-x * 5, face="laugh"); k.pose(1, "point")
    push(S, (0, 0, 4), 13, 30)


def mom(S):
    room()
    m = C.mom((-1.1, 0, 0), rot=-30, face="angry"); m.colored(True); m.pose(1, "point")
    box((3, 2.6, 2.8), (2.6, -0.6, 1.4), mat("#c49a6c", rough=0.9), name="box")
    text("RETURN", (2.6, -1.95, 1.6), mat("#c62828"), size=0.55)
    push(S, (0, 0, 4.6), 12, 34)


def hero_hug(S):
    room()
    r = mine((1.0, 0, 0), -30, scale=0.85)
    h = C.hero((-1.1, -0.4, 0), rot=-30, face="happy"); h.pose(1, "hips")
    h.set_face(S.word("mine"), "happy")
    head_tilt(r, S.word("broken"), 20, 10)
    B.sparkle_burst((0, -0.5, 4.5), S.word("mine"), n=10, color="#ffd1ea")
    push(S, (0, 0, 4.0), 12, 36)


# ---------------------------------------------------------------- the update
def update(S):
    street(CREEPY, 1.4)
    rs = bots(4, 2, -9, 6)
    for i, r in enumerate(rs):
        head_tilt(r, 6 + i * 3, 0, 0, 20)
    big_screen("NEW MESSAGE", (0, 14, 12), w=16, h=5, ink="#ffd54f", size=1.4)
    wide(S, (0, 2, 6), 26, 7)


def screen(S):
    street(CREEPY, 1.4)
    big_screen("ROBOCO\nUPDATE 9.0", (0, 8, 8), w=14, h=8, ink="#40c4ff", size=1.5)
    cam(S, (0, -8, 8), (0, -5, 8), (0, 8, 8), lens=34)


def question(S):
    street(CREEPY, 1.4)
    big_screen("ONE QUESTION", (0, 8, 8), w=14, h=6, ink="#ffffff", size=1.4)
    r = robot((0, -2, 0.5), 0, scale=0.8); head_tilt(r, 4, 0, 0, 15)
    cam(S, (2, -14, 4), (1, -12, 5), (0, 4, 6), lens=30)


def accept(S):
    street(CREEPY, 1.4)
    big_screen("ACCEPT UPDATE?\nYES   NO", (0, 8, 8), w=15, h=7, ink="#ffd54f", size=1.3)
    cam(S, (0, -7, 8), (0, -4.5, 8), (0, 8, 8), lens=34)


def pip_yes(S):
    yard(CREEPY, 1.8)
    r = pips((1.4, 0, 0.2), 30)
    robot_say(r, S.word("yes"), "YES", color="#ffd54f")
    p = C.pip((-1.1, 0, 0.2), rot=-30, face="calm", lace=None); p.colored(True)
    push(S, (0, 0, 3.8), 13, 34)


def all_yes(S):
    street(CREEPY, 1.4)
    rs = bots(6, 2, -15, 6, rows=3, dy=5)
    for i, r in enumerate(rs):
        robot_say(r, 3 + (i * 5) % 20, "YES", color="#ffd54f")
    wide(S, (0, -3, 4), 30, 12, pan=6)


def eyes_red(S):
    street(CREEPY, 1.0)
    rs = bots(3, 0, -5, 5, scale=0.9)
    f = S.word("red")
    for i, r in enumerate(rs):
        robot_eyes(r, f + i * 2, RED_EYE)
    push(S, (0, 0, 4.2), 11, 32)


def march(S):
    street(CREEPY, 0.9)
    rs = bots(4, 2, -10, 5, eye=RED_EYE, rows=2, dy=5)
    for r in rs:
        x, y, z = r["root"].location
        robot_walk(r, 1, S.n, (x, y + 6, z), (x, y - 4, z))
    house_doors = [box((2.4, 0.2, 3.8), (x, 14.2, 2), mat("#c62828", emit=0.3)) for x in (-8, 8)]
    cam(S, (3, -18, 3), (2, -16, 3.2), (0, 0, 4), lens=28)


def grab_kids(S):
    street(CREEPY, 0.9)
    r = robot((1.5, 0, 0.5), -30, eye=RED_EYE, scale=1.0)
    robot_arm(r, 1, -1, -100); robot_arm(r, 1, 1, -100)
    k = C.kid(2, (-0.8, -1.2, 0.5), rot=-20, face="scared"); k.pose(1, "scared")
    float_up(k, 1, S.n, 1.5)
    push(S, (0, 0, 4.4), 12, 32)


def hero_run(S):
    street(CREEPY, 0.9)
    h = C.hero((0, -8, 0.5), face="scared")
    h.walk(1, S.n, (-12, -8, 0.5), (8, -8, 0.5), run=True)
    for i, x in enumerate((-20, -16)):
        r = robot((x, -6, 0.5), 0, eye=RED_EYE, scale=0.8)
        robot_walk(r, 1, S.n, (x, -6, 0.5), (x + 12, -6, 0.5))
    cam(S, (-10, -22, 4), (6, -22, 4), (-6, -8, 4), (8, -8, 4), lens=30)


def hero_robot(S):
    room(DARK, light=0.5)
    r = mine((1.4, 0, 0), -10, scale=0.85)
    h = C.hero((-1.4, -1, 0), rot=-40, face="nervous")
    push(S, (0, 0, 3.8), 13, 32)


def big_screen_shot(S):
    room(DARK, light=0.4)
    tv("UPDATE INSTALLED", (0, 7, 6.5), ink="#ff5252", w=11, h=5, size=1.0)
    h = turn180(C.hero((0, -2, 0), face="scared"))
    cam(S, (2.5, -12, 6), (1.5, -10, 6), (0, 6, 6), lens=30)


def one_left(S):
    room(DARK, light=0.4)
    tv("999,999,999 / 1,000,000,000\nONE ROBOT LEFT", (0, 7, 6.5), ink="#ff5252", w=12, h=5, size=0.62)
    cam(S, (0, -3, 6.5), (0, -1, 6.5), (0, 7, 6.5), lens=36)


def rule(S):
    room(DARK, light=0.4)
    tv("ALL ROBOTS\nMUST SAY YES", (0, 7, 6.5), ink="#ffd54f", w=11, h=5, size=0.9)
    cam(S, (-2, -4, 6), (-1, -2.5, 6.4), (0, 7, 6.5), lens=34)


def every(S):
    room(DARK, light=0.5)
    r = mine((0.8, 0, 0), 0)
    h = C.hero((-1.4, -0.3, 0), rot=-30, face="shocked")
    push(S, (0, 0, 3.8), 12, 34)


def ask(S):
    room(DARK, light=0.5)
    tv("DO YOU ACCEPT\nTHE UPDATE?", (0, 7, 6.5), ink="#ffd54f", w=11, h=5, size=0.85)
    r = mine((0, 1.5, 0), 180); r["root"].rotation_euler.z = math.radians(180)
    cam(S, (3, -9, 5), (2, -7.5, 5), (0, 3, 5), lens=30)


def pause(S):
    room(DARK, light=0.5)
    r = mine((1.2, 0, 0), 0, scale=0.9)
    head_tilt(r, 6, 35, 0)
    h = C.hero((-2, -0.5, 0), rot=-40, face="nervous")
    push(S, (0, 0, 4), 12, 34)


def hero_nod(S):
    room(DARK, light=0.5)
    h = C.hero((0, 0, 0), face="determined")
    h.head_turn(4, 0, 18); h.head_turn(10, 0, -4); h.head_turn(16, 0, 14); h.head_turn(22, 0, 0)
    push(S, (0, 0, 4.8), 6, 40)


def nope_big(S):
    room(DARK, light=0.5)
    r = mine((0, 0, 0), 0, scale=1.0)
    robot_say(r, 2)
    B.sparkle_burst((0, -1, 4), 4, n=16, color="#69f0ae", spread=3)
    cam(S, (0, -9, 4), (0, -4.5, 3.6), (0, 0, 3.4), lens=36)


def error(S):
    street(CREEPY, 1.0)
    big_screen("ERROR", (0, 8, 8), w=14, h=6, ink="#ff1744", size=2.4)
    cam(S, (0, -8, 8), (0, -6, 8), (0, 8, 8), lens=34)
    B.shake(bpy.context.scene.camera, 1, S.n, 0.12)


def shutdown(S):
    street(NIGHT, 0.6)
    rs = bots(5, 0, -12, 6, eye=RED_EYE, rows=2, dy=6)
    for r in rs:
        robot_eyes(r, S.word("off"), None)
    wide(S, (0, -3, 4), 24, 7)


def reboot(S):
    street(DAY, 2.6)
    rs = bots(5, 0, -12, 6, rows=2, dy=6)
    for i, r in enumerate(rs):
        robot_eyes(r, 1, None); robot_eyes(r, S.word("blue") + i, BLUE_EYE)
    wide(S, (0, -3, 4), 22, 6)


def pip_back(S):
    yard()
    r = pips((1.4, 0, 0.2), 20)
    robot_say(r, S.word("sorry"), "SORRY", color="#ffd54f")
    p = C.pip((-1.1, 0, 1.4), rot=-30, face="surprised", lace=None); p.colored(True)
    p.move(1, (-1.1, 0, 1.4)); p.move(12, (-1.1, 0, 0.2))
    p.set_face(S.word("sorry"), "happy")
    push(S, (0, 0, 4), 13, 34)


def news(S):
    room(wall="#263238")
    tv("BREAKING NEWS", (0, 7, 9), ink="#ffffff", w=14, h=2.2, size=1.0, bg="#c62828")
    r = mine((0, 1, 0), 0, scale=1.0)
    cam(S, (0, -12, 5), (0, -10, 5.5), (0, 1, 5.5), lens=32)


def famous(S):
    street()
    r = mine((1.6, 0, 0.5))
    h = C.hero((-1.1, 0, 0.5), face="happy"); h.pose(1, "cheer")
    for i, x in enumerate((-7, -5, 5, 7.5)):
        k = C.kid(i, (x, 3, 0.5), face="happy"); k.pose(1, "cheer")
    B.sparkle_burst((0, -1, 6), 3, n=20, color="#fff59d", spread=5)
    push(S, (0, 0, 4.2), 13, 30)


def ending(S):
    room()
    desk(0, 1.5)
    h = C.hero((-0.8, -0.4, 0), face="calm"); V1.sit(h, 1)
    V1.paper(h.sh[0], (0, -0.6, -2.0), "HW")
    r = mine((3.4, 0.5, 0), -30)
    h.head_turn(S.word("though"), 30, 0)
    push(S, (1, 0, 4), 14, 32)


def ending_nope(S):
    room()
    r = mine((1.4, 0, 0), -30, scale=0.85)
    robot_say(r, S.word("nope"))
    h = C.hero((-1.1, 0, 0), rot=-40, face="laugh")
    h.set_face(S.word("nope") + 10, "wink"); h.pose(S.word("nope") + 6, "thumb")
    push(S, (0, 0, 4.2), 13, 34)


ALIASES = {"big_screen": big_screen_shot, "hero": hero, "mom": mom}


def shot_funcs():
    return shot_table(globals(), ALIASES)
