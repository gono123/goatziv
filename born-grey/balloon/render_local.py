"""Render the whole film on your own PC (GPU) and build a silent MP4, using only Blender.

    blender -b --python born-grey/v2/render_local.py
    blender -b --python born-grey/v2/render_local.py -- --res 1080x1920 --samples 16 --mblur

Every shot runs in its own Blender process (frames already on disk are skipped, so you can stop and
restart). Then Blender's video editor joins the frames in order into out/balloon_silent.mp4.
Upload that file to the Google Drive "gneef" folder: captions, voice, sound effects and music are added
in the cloud session.
"""
import json, os, subprocess, sys, time
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
res = argv[argv.index("--res") + 1] if "--res" in argv else "1080x1920"
samples = argv[argv.index("--samples") + 1] if "--samples" in argv else "16"
mblur = "--mblur" in argv or "--res" not in argv
only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
outdir = argv[argv.index("--outdir") + 1] if "--outdir" in argv else "out"
_tl = os.path.join(HERE, "out", "timeline.json")
tl = json.load(open(_tl if os.path.exists(_tl) else os.path.join(HERE, "timeline.json")))
FPS = tl["fps"]
blender = bpy.app.binary_path
runner = [blender, "-b", "--python"] if blender else [sys.executable]   # bpy-as-a-module fallback (Linux/cloud)
t0 = time.time()
shots = [s for s in tl["shots"] if not only or s["id"] in only]
for k, s in enumerate(shots):
    n = round(s["end"] * FPS) - round(s["start"] * FPS)
    d = os.path.join(HERE, outdir, "frames", s["id"])
    have = len(os.listdir(d)) if os.path.isdir(d) else 0
    if have >= n:
        continue
    cmd = runner + [os.path.join(HERE, "render2.py"), "--", s["id"], "--res", res, "--samples", samples, "--outdir", outdir] + (["--mblur"] if mblur else [])
    print(f"[{k + 1}/{len(shots)}] {s['id']} ({n} frames) ...", flush=True)
    subprocess.run(cmd, check=True)
print(f"rendered in {(time.time() - t0) / 60:.1f} min", flush=True)

# join every shot's frames, in order, into one silent video
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
w, h = (int(x) for x in res.split("x"))
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
sc.render.fps = FPS
# the frames are already final colours: no "AgX" film look on top (it halves the saturation)
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
se = sc.sequence_editor_create()
strips = se.strips if hasattr(se, "strips") else se.sequences   # Blender 5 renamed sequences -> strips
frame = 1
for s in shots:
    n = round(s["end"] * FPS) - round(s["start"] * FPS)
    d = os.path.join(HERE, outdir, "frames", s["id"])
    files = sorted(os.listdir(d))[:n]
    st = strips.new_image(s["id"], os.path.join(d, files[0]), channel=1, frame_start=frame)
    for f in files[1:]:
        st.elements.append(f)
    if len(files) < n:                      # hold the last frame if a shot came up short
        st.frame_final_duration = n
    frame += n
sc.frame_start, sc.frame_end = 1, frame - 1
try:
    sc.render.image_settings.media_type = "VIDEO"      # Blender 5: pick "video" before the format
except (AttributeError, TypeError):
    pass
sc.render.image_settings.file_format = "FFMPEG"
sc.render.ffmpeg.format = "MPEG4"
sc.render.ffmpeg.codec = "H264"
sc.render.ffmpeg.constant_rate_factor = "HIGH"
sc.render.ffmpeg.audio_codec = "NONE"
sc.render.filepath = os.path.join(HERE, outdir, "balloon_silent.mp4")
sc.render.use_sequencer = True
bpy.ops.render.render(animation=True)
print("DONE ->", sc.render.filepath, f"{(frame - 1) / FPS:.1f}s")
