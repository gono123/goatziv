"""Render one v2 shot.  python render2.py <shot> [--frames a,b] [--res WxH] [--samples N]"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import bpy
import blib as B
import shots2 as SH
import mocap as MC

ap = argparse.ArgumentParser()
ap.add_argument("shot"); ap.add_argument("--frames", default=""); ap.add_argument("--res", default="720x1280"); ap.add_argument("--samples", type=int, default=4)
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]   # works with python+bpy and with blender -b --python
ap.add_argument("--mblur", action="store_true")
ap.add_argument("--outdir", default="out")
a = ap.parse_args(argv)
_tl = os.path.join(HERE, "out", "timeline.json")
tl = json.load(open(_tl if os.path.exists(_tl) else os.path.join(HERE, "timeline.json")))
d = next(s for s in tl["shots"] if s["id"] == a.shot)
S = SH.Shot(d, tl["fps"])
w, h = (int(x) for x in a.res.split("x"))
sc = B.reset((w, h), a.samples)
MC.install()
SH.shot_funcs()[a.shot](S)
if not os.environ.get("NO_MOCAP"):
    MC.auto(S)
    MC.camera_life(S)
sc.frame_start, sc.frame_end = 1, S.n
if a.mblur:
    sc.render.use_motion_blur = True
    try:
        sc.render.motion_blur_shutter = 0.5
    except AttributeError:
        pass
t = time.time()
if a.frames:
    os.makedirs(os.path.join(HERE, "out", "preview"), exist_ok=True)
    for f in [int(x) for x in a.frames.split(",")]:
        for g in range(1, f + 1, 1 if bpy.data.particles else max(1, f)):
            sc.frame_set(g)
        sc.frame_set(f)
        sc.render.filepath = os.path.join(HERE, "out", "preview", f"{a.shot}_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
else:
    out = os.path.join(HERE, a.outdir, "frames", a.shot)
    os.makedirs(out, exist_ok=True)
    sc.render.filepath = os.path.join(out, "")
    sc.render.use_overwrite = False
    bpy.ops.render.render(animation=True)
print(f"SHOT {a.shot} frames={S.n} time={time.time() - t:.1f}s")
