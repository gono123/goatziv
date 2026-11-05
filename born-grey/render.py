"""Render one shot with Blender (bpy).

    python render.py <shot_id> [--preview] [--res 720x1280] [--samples 12] [--frames a,b,c]

--preview renders the first, middle and last frame to out/preview/. Otherwise every frame goes to
out/frames/<shot_id>/0001.png ... (frame count from out/timeline.json).
"""
import argparse, json, os, sys, time
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
import blib as B
import shots as SH

ap = argparse.ArgumentParser()
ap.add_argument("shot")
ap.add_argument("--preview", action="store_true")
ap.add_argument("--res", default="720x1280")
ap.add_argument("--samples", type=int, default=12)
ap.add_argument("--frames", default="")
a = ap.parse_args([x for x in sys.argv[1:]])

tl = json.load(open(os.path.join(HERE, "out", "timeline.json")))
data = next(s for s in tl["shots"] if s["id"] == a.shot)
S = SH.Shot(data, tl["fps"])
w, h = (int(x) for x in a.res.split("x"))
sc = B.reset((w, h), a.samples)
SH.SHOT_FUNCS[a.shot](S)
sc.frame_start, sc.frame_end = 1, S.n
print(f"BUILD {time.time() - T0:.1f}s objects={len(bpy.data.objects)} mats={len(bpy.data.materials)}")
t = time.time()
if a.preview or a.frames:
    os.makedirs(os.path.join(HERE, "out", "preview"), exist_ok=True)
    frames = [int(x) for x in a.frames.split(",")] if a.frames else [1, max(1, S.n // 2), S.n]
    # particles need the frames before; step through them
    for f in frames:
        for g in range(1, f + 1, 1 if bpy.data.particles else f):
            sc.frame_set(g)
        sc.frame_set(f)
        sc.render.filepath = os.path.join(HERE, "out", "preview", f"{a.shot}_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
else:
    out = os.path.join(HERE, "out", "frames", a.shot)
    os.makedirs(out, exist_ok=True)
    sc.render.filepath = os.path.join(out, "")
    sc.render.use_overwrite = False
    bpy.ops.render.render(animation=True)
print(f"SHOT {a.shot} frames={S.n} time={time.time() - t:.1f}s")
