"""Real motion (CMU mocap, see ../mocap/bvh2r6.py) on our blocky characters.

play(char, clip, f0, f1, ...)  keys the 6 joints from a clip, frame by frame (Euler keys, so later keys in a shot still work)
install()                      patches Char so walk/run use real gaits and every character is registered
auto(S)                        after a shot is built: give every character motion that fits its face/mood
                               (posed characters keep their pose and get body/head life only)
camera_life(S)                 a little handheld drift on the shot camera
"""
import json, math, os, random
import bpy
from mathutils import Quaternion, Euler, Vector
import blib as B

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(ROOT, "mocap", "clips")
_cache = {}
ALL = []
SKIP = 3

WALK, RUN, HAPPY_WALK = "02_01", "09_01", "82_12"
MOOD = {   # face -> (clip, arm amplitude)
    "scared": ("79_73", 1.0), "shocked": ("79_73", 0.8), "nervous": ("79_73", 0.6), "surprised": ("79_73", 0.6),
    "happy": ("79_69", 0.7), "laugh": ("13_14", 0.9), "wink": ("79_69", 0.5), "smug": ("18_08", 0.6),
    "angry": ("18_10", 0.9), "determined": ("18_10", 0.5), "sad": ("22_03", 0.5),
    "calm": ("18_08", 0.35), "side_eye": ("18_08", 0.3), "little_o": ("18_08", 0.4), "puffed": ("18_08", 0.3),
    "asleep": ("18_08", 0.1), "green_eyes": ("79_69", 0.4), "blink": ("18_08", 0.3),
}


def clip(cid):
    if cid not in _cache:
        _cache[cid] = json.load(open(os.path.join(CLIPS, cid + ".json")))
    return _cache[cid]


def best_offset(cid, n, seed=0):
    """Start of the liveliest stretch of length n (with a little randomness so crowds differ)."""
    c = clip(cid); e = c["energy"]; L = len(e)
    if L <= n + 1:
        return 0
    s = [sum(e[i:i + n]) for i in range(0, L - n, 3)]
    order = sorted(range(len(s)), key=lambda k: -s[k])
    return order[min(len(order) - 1, seed % 3)] * 3


def _slerp(q, amp):
    return Quaternion((1, 0, 0, 0)).slerp(Quaternion(q), max(0.0, min(1.0, amp)))


def _key(obj, frame, q, prev):
    e = q.to_euler("XYZ", prev) if prev is not None else q.to_euler("XYZ")
    obj.rotation_euler = e
    obj.keyframe_insert("rotation_euler", frame=frame)
    return e


def play(ch, cid, f0, f1, offset=None, amp=1.0, arm_amp=None, leg_amp=None, speed=1.0, body=True, neck=True,
         arms=True, legs=True, bob=0.0, seed=0, every=1):
    c = clip(cid); fr = c["frames"]; L = len(fr)
    n = f1 - f0 + 1
    off = best_offset(cid, int(n * speed), seed) if offset is None else offset
    arm_amp = amp if arm_amp is None else arm_amp
    leg_amp = amp if leg_amp is None else leg_amp
    prev = {}
    targets = []
    if body: targets.append(("body", ch.body, amp * 0.8))
    if neck: targets.append(("neck", ch.neck, amp * 0.8))
    if arms: targets += [("arm_r", ch.sh[0], arm_amp), ("arm_l", ch.sh[1], arm_amp)]
    if legs: targets += [("leg_r", ch.hip[0], leg_amp), ("leg_l", ch.hip[1], leg_amp)]
    for k in range(0, n, every):
        f = f0 + k
        i = SKIP + int(off + k * speed) % (L - SKIP)    # frame 0 of every CMU clip is a T-pose
        d = fr[i]
        for name, obj, a in targets:
            prev[name] = _key(obj, f, _slerp(d[name], a), prev.get(name))
        if bob:
            ch.body.location.z = max(-0.6, d["bob"]) * bob
            ch.body.keyframe_insert("location", frame=f)


def _has_keys(obj, path="rotation_euler"):
    return any(fc.data_path == path for fc in B.all_fcurves(obj))


def _face_at_start(ch):
    log = getattr(ch, "_face_log", None)
    if log:
        first = min(log, key=lambda x: x[0])
        return first[1]
    return "calm"


def install():
    if getattr(B.Char, "_mocap_installed", False):
        return
    B.Char._mocap_installed = True
    init0 = B.Char.__init__

    def init(self, *a, **k):
        init0(self, *a, **k)
        ALL.append(self)
    B.Char.__init__ = init

    walk0 = B.Char.walk

    def walk(self, f0, f1, a, b, stride=8, swing=32, run=False, arms=True):
        walk0(self, f0, f1, a, b, stride=stride, swing=swing, run=run, arms=arms)
        d = (Vector(b) - Vector(a)).length / max(1, (f1 - f0)) * 24      # studs per second
        cid = RUN if run else WALK
        c = clip(cid)
        f = c["frames"]
        clip_speed = math.hypot(f[-1]["pos"][0], f[-1]["pos"][1]) / (len(f) / 24)   # studs/s in the clip
        sp = max(0.6, min(1.8, d / max(0.1, clip_speed)))
        play(self, cid, f0, f1, offset=0, amp=1.0, speed=sp, neck=True, bob=0.6 if run else 0.4)
        self._walking = True
    B.Char.walk = walk

    try:
        import cast as C
        sf0 = C.Faces.set_face

        def set_face(self, frame, name):
            if not hasattr(self, "_face_log"):
                self._face_log = []
            self._face_log.append((frame, name))
            return sf0(self, frame, name)
        C.Faces.set_face = set_face
    except Exception:
        pass


def auto(S):
    """Motion for every character that the shot did not animate itself."""
    for i, ch in enumerate(ALL):
        if getattr(ch, "_walking", False):
            continue
        posed = _has_keys(ch.sh[0]) or _has_keys(ch.sh[1])
        moved = _has_keys(ch.root, "location")
        mood = _face_at_start(ch)
        cid, a = MOOD.get(mood, ("18_08", 0.35))
        if ch.name.startswith(("insp", "ins", "in", "ic", "isc", "ib", "sq")) and not hasattr(ch, "face_heads"):
            cid, a = "18_08", 0.2                       # inspectors: barely move, menacing
        legs_sitting = _has_keys(ch.hip[0])
        if posed:
            play(ch, cid, 1, S.n, amp=min(0.6, a + 0.2), arms=False, legs=False, seed=i)
        else:
            play(ch, cid, 1, S.n, amp=0.8, arm_amp=a, leg_amp=0.0 if moved or legs_sitting else 0.25,
                 legs=not legs_sitting, seed=i)


def camera_life(S, amp=0.05):
    cam = bpy.context.scene.camera
    if cam is None:
        return
    rnd = random.Random(int(S.t0 * 100))
    nz = [(rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)) for _ in range(S.n // 6 + 3)]
    dist = max(2.0, (cam.location - Vector(bpy.data.objects[cam["tgt"]].location)).length) if "tgt" in cam else 10
    a = amp * min(3.0, dist / 6)
    keys = list(range(0, S.n + 1, 6))
    base = []
    for k in keys:                       # sample the planned path first, then add the drift
        bpy.context.scene.frame_set(1 + k)
        base.append(cam.matrix_world.translation.copy())
    for k, b in zip(keys, base):
        x, y, z = nz[k // 6]
        cam.location = b + Vector((x, y * 0.5, z)) * a
        cam.keyframe_insert("location", frame=1 + k)
