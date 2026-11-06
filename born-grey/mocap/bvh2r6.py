"""Convert CMU motion capture (BVH, 120 fps) into poses for our blocky R6 characters (24 fps).

    python bvh2r6.py              -> clips/<id>.json for every *.bvh here

A blocky character has rigid parts on 6 joints (body, neck, 2 shoulders, 2 hips), so each mocap frame is reduced to:
  root: ground position (studs, relative to the first frame), height bob, heading (deg)
  body: torso rotation relative to the heading         (quaternion w,x,y,z)
  neck: head rotation relative to the torso
  arm_r / arm_l / leg_r / leg_l: rotation that turns the hanging rest direction (0,0,-1) into the limb's
        direction (shoulder->wrist, hip->ankle), relative to the torso
Coordinates are Blender's (Z up, character facing -Y). Data: CMU Graphics Lab Motion Capture Database
(mocap.cs.cmu.edu), BVH conversion by B. Hahne; both free to use.
"""
import glob, json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "clips")
os.makedirs(OUT, exist_ok=True)


def parse(path):
    toks = open(path).read().split()
    i = 0
    joints, stack, chans_order = [], [], []
    while toks[i] != "MOTION":
        t = toks[i]
        if t in ("ROOT", "JOINT", "End"):
            name = toks[i + 1] if t != "End" else (joints[stack[-1]]["name"] + "_end")
            joints.append({"name": name, "parent": stack[-1] if stack else -1, "offset": None, "chans": []})
            stack.append(len(joints) - 1)
            i += 2
        elif t == "OFFSET":
            joints[stack[-1]]["offset"] = np.array([float(x) for x in toks[i + 1:i + 4]])
            i += 4
        elif t == "CHANNELS":
            n = int(toks[i + 1])
            joints[stack[-1]]["chans"] = toks[i + 2:i + 2 + n]
            chans_order.append(stack[-1])
            i += 2 + n
        elif t == "}":
            stack.pop()
            i += 1
        else:
            i += 1
    i += 1
    nf = int(toks[i + 1]); ft = float(toks[i + 4]); i += 5
    ncol = sum(len(j["chans"]) for j in joints)
    data = np.array([float(x) for x in toks[i:i + nf * ncol]]).reshape(nf, ncol)
    return joints, chans_order, data, ft


def rot(axis, deg):
    a = np.radians(deg); c, s = np.cos(a), np.sin(a)
    if axis == "X":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == "Y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def fk(joints, order, row):
    """Global positions + rotations of every joint for one frame (BVH space, Y up)."""
    col = 0
    local = {}
    for ji in order:
        j = joints[ji]
        pos = np.zeros(3); R = np.eye(3)
        for c in j["chans"]:
            v = row[col]; col += 1
            if c.endswith("position"):
                pos["XYZ".index(c[0])] = v
            else:
                R = R @ rot(c[0], v)
        local[ji] = (pos, R)
    G = [None] * len(joints)
    for ji, j in enumerate(joints):
        p, R = local.get(ji, (np.zeros(3), np.eye(3)))
        if j["parent"] < 0:
            G[ji] = (p + j["offset"], R)
        else:
            pp, PR = G[j["parent"]]
            G[ji] = (pp + PR @ j["offset"], PR @ R)
    return G


# BVH (x, y-up, z-forward) -> Blender (x, -z, y): the performer faces -Y like our characters
CONV = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float)


def quat_from_mat(M):
    w = np.sqrt(max(0, 1 + M[0, 0] + M[1, 1] + M[2, 2])) / 2
    x = np.sqrt(max(0, 1 + M[0, 0] - M[1, 1] - M[2, 2])) / 2
    y = np.sqrt(max(0, 1 - M[0, 0] + M[1, 1] - M[2, 2])) / 2
    z = np.sqrt(max(0, 1 - M[0, 0] - M[1, 1] + M[2, 2])) / 2
    x = np.copysign(x, M[2, 1] - M[1, 2]); y = np.copysign(y, M[0, 2] - M[2, 0]); z = np.copysign(z, M[1, 0] - M[0, 1])
    q = np.array([w, x, y, z]); return q / np.linalg.norm(q)


def quat_between(a, b):
    a = a / np.linalg.norm(a); b = b / np.linalg.norm(b)
    c = np.cross(a, b); d = float(np.dot(a, b))
    if d < -0.9999:
        return np.array([0.0, 1.0, 0.0, 0.0])
    q = np.array([1 + d, *c]); return q / np.linalg.norm(q)


def frame_of(up, right):
    """Orthonormal frame: columns = right (+X), back (+Y), up (+Z) for a body facing -Y."""
    up = up / np.linalg.norm(up)
    right = right - up * np.dot(right, up); right /= np.linalg.norm(right)
    back = np.cross(up, right)
    return np.stack([right, back, up], 1)


def convert(path):
    joints, order, data, ft = parse(path)
    idx = {j["name"]: k for k, j in enumerate(joints)}
    need = ["Hips", "LeftUpLeg", "RightUpLeg", "LeftFoot", "RightFoot", "LeftArm", "RightArm", "LeftHand", "RightHand", "Neck", "Head"]
    assert all(n in idx for n in need), [n for n in need if n not in idx]
    step = max(1, int(round((1 / 24) / ft)))
    frames = []
    first = None
    leg_len = None
    for fi in range(0, len(data), step):
        G = fk(joints, order, data[fi])
        P = {n: CONV @ G[idx[n]][0] for n in need}
        Rhead = CONV @ G[idx["Head"]][1] @ CONV.T
        if leg_len is None:
            leg_len = np.linalg.norm(P["LeftUpLeg"] - P["LeftFoot"]) * 1.06
        sc = 2.0 / leg_len                    # character legs are 2 studs
        pelvis_r = P["RightUpLeg"] - P["LeftUpLeg"]   # performer's right is screen-left (-X) when facing -Y
        chest_r = P["RightArm"] - P["LeftArm"]
        mid_sh = (P["LeftArm"] + P["RightArm"]) / 2
        up = mid_sh - P["Hips"]
        # heading: from the pelvis "right" vector projected on the ground
        r2 = np.array([-pelvis_r[0], -pelvis_r[1], 0.0])   # character +X is the performer's left
        yaw = np.degrees(np.arctan2(r2[1], r2[0]))
        cy, sy = np.cos(np.radians(yaw)), np.sin(np.radians(yaw))
        Yaw = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])
        body = frame_of(up, -(pelvis_r + chest_r) / 2)     # torso frame in world
        body_rel = Yaw.T @ body
        def limb(a, b):
            d_world = P[b] - P[a]
            d_local = body.T @ d_world
            return quat_between(np.array([0, 0, -1.0]), d_local)
        head_rel = body.T @ Rhead
        if first is None:
            first = {"pos": P["Hips"].copy(), "head0": head_rel.copy(), "hip_h": P["Hips"][2]}
        head_q = quat_from_mat(head_rel @ first["head0"].T)
        frames.append({
            "pos": [round(float((P["Hips"][0] - first["pos"][0]) * sc), 4), round(float((P["Hips"][1] - first["pos"][1]) * sc), 4)],
            "bob": round(float((P["Hips"][2] - first["hip_h"]) * sc), 4),
            "yaw": round(float(yaw), 2),
            "body": [round(float(v), 5) for v in quat_from_mat(body_rel)],
            "neck": [round(float(v), 5) for v in head_q],
            "arm_r": [round(float(v), 5) for v in limb("RightArm", "RightHand")],
            "arm_l": [round(float(v), 5) for v in limb("LeftArm", "LeftHand")],
            "leg_r": [round(float(v), 5) for v in limb("RightUpLeg", "RightFoot")],
            "leg_l": [round(float(v), 5) for v in limb("LeftUpLeg", "LeftFoot")],
        })
    # motion energy per frame (arms + legs), to find the liveliest stretch of a long clip
    def ang(q1, q2):
        return 2 * np.degrees(np.arccos(min(1, abs(float(np.dot(q1, q2))))))
    energy = [0.0] + [sum(ang(np.array(a[k]), np.array(b[k])) for k in ("arm_r", "arm_l", "leg_r", "leg_l", "body"))
                      for a, b in zip(frames, frames[1:])]
    return {"fps": 24, "source": os.path.basename(path), "frames": frames, "energy": [round(e, 2) for e in energy]}


if __name__ == "__main__":
    for p in sorted(glob.glob(os.path.join(HERE, "*.bvh"))):
        c = convert(p)
        cid = os.path.basename(p)[:-4]
        json.dump(c, open(os.path.join(OUT, cid + ".json"), "w"))
        f = c["frames"]
        dist = np.hypot(f[-1]["pos"][0], f[-1]["pos"][1])
        print(f"{cid}: {len(f)} frames ({len(f) / 24:.1f}s), travels {dist:.1f} studs, mean energy {np.mean(c['energy']):.1f}")
