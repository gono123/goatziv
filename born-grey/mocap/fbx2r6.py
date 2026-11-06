"""Convert Mixamo FBX animations (mixamo/*.fbx, "Without Skin") into R6 clips (clips/mx_<name>.json, 24 fps).
Run with Blender's Python (bpy). Same output format as bvh2r6.py."""
import glob, json, os, re, sys
import numpy as np
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from bvh2r6 import frame_of, quat_between, quat_from_mat

BONES = {"Hips": "Hips", "LeftUpLeg": "LeftUpLeg", "RightUpLeg": "RightUpLeg", "LeftFoot": "LeftFoot", "RightFoot": "RightFoot",
         "LeftArm": "LeftArm", "RightArm": "RightArm", "LeftHand": "LeftHand", "RightHand": "RightHand", "Neck": "Neck", "Head": "Head"}


def convert(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=path, automatic_bone_orientation=False)
    arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
    names = {}
    for b in arm.pose.bones:
        base = re.sub(r"^mixamorig\d*:", "", b.name)
        if base in BONES:
            names[base] = b.name
    act = arm.animation_data.action
    f0, f1 = (int(x) for x in act.frame_range)
    fps_src = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
    sc_ = bpy.context.scene
    frames, first, leg_len = [], None, None
    t = 0.0
    while f0 + t * fps_src <= f1:
        sc_.frame_set(int(round(f0 + t * fps_src)))
        M = arm.matrix_world
        P = {k: np.array(M @ arm.pose.bones[v].head) for k, v in names.items()}
        Rh = np.array((M @ arm.pose.bones[names["Head"]].matrix).to_3x3().normalized())
        if leg_len is None:
            leg_len = np.linalg.norm(P["LeftUpLeg"] - P["LeftFoot"]) * 1.06
        sc = 2.0 / leg_len
        pelvis_r = P["RightUpLeg"] - P["LeftUpLeg"]
        chest_r = P["RightArm"] - P["LeftArm"]
        up = (P["LeftArm"] + P["RightArm"]) / 2 - P["Hips"]
        r2 = np.array([-pelvis_r[0], -pelvis_r[1], 0.0])
        yaw = np.degrees(np.arctan2(r2[1], r2[0]))
        cy, sy = np.cos(np.radians(yaw)), np.sin(np.radians(yaw))
        Yaw = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])
        body = frame_of(up, -(pelvis_r + chest_r) / 2)
        head_rel = body.T @ Rh
        if first is None:
            first = {"pos": P["Hips"].copy(), "head0": head_rel.copy(), "hip_h": P["Hips"][2]}
        limb = lambda a, b: quat_between(np.array([0, 0, -1.0]), body.T @ (P[b] - P[a]))
        frames.append({
            "pos": [round(float((P["Hips"][0] - first["pos"][0]) * sc), 4), round(float((P["Hips"][1] - first["pos"][1]) * sc), 4)],
            "bob": round(float((P["Hips"][2] - first["hip_h"]) * sc), 4), "yaw": round(float(yaw), 2),
            "body": [round(float(v), 5) for v in quat_from_mat(Yaw.T @ body)],
            "neck": [round(float(v), 5) for v in quat_from_mat(head_rel @ first["head0"].T)],
            "arm_r": [round(float(v), 5) for v in limb("RightArm", "RightHand")],
            "arm_l": [round(float(v), 5) for v in limb("LeftArm", "LeftHand")],
            "leg_r": [round(float(v), 5) for v in limb("RightUpLeg", "RightFoot")],
            "leg_l": [round(float(v), 5) for v in limb("LeftUpLeg", "LeftFoot")],
        })
        t += 1 / 24
    def ang(q1, q2):
        return 2 * np.degrees(np.arccos(min(1, abs(float(np.dot(q1, q2))))))
    energy = [0.0] + [sum(ang(np.array(a[k]), np.array(b[k])) for k in ("arm_r", "arm_l", "leg_r", "leg_l", "body")) for a, b in zip(frames, frames[1:])]
    return {"fps": 24, "source": "Mixamo: " + os.path.basename(path), "frames": frames, "energy": [round(e, 2) for e in energy]}


for p in sorted(glob.glob(os.path.join(HERE, "mixamo", "*.fbx"))):
    cid = "mx_" + re.sub(r"\W+", "_", os.path.basename(p)[:-4].lower()).strip("_")
    c = convert(p)
    json.dump(c, open(os.path.join(HERE, "clips", cid + ".json"), "w"))
    f = c["frames"]
    print(f"CLIP {cid}: {len(f)} frames ({len(f) / 24:.1f}s), travels {np.hypot(*f[-1]['pos']):.1f}, energy {np.mean(c['energy']):.1f}")
