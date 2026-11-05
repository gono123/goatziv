"""One frame from the middle of every shot of each reference video -> ref/shots/<id>/NNN_<t>.jpg, ref/sheets/<id>_<k>.jpg"""
import os, subprocess, sys
from PIL import Image, ImageDraw
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ref")
for vid in sys.argv[1:]:
    cuts = [0.0] + [float(x) for x in open(f"{R}/cuts/{vid}.txt").read().split()]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{R}/proxy/{vid}.mp4"], capture_output=True, text=True).stdout)
    cuts.append(dur)
    os.makedirs(f"{R}/shots/{vid}", exist_ok=True)
    mids = [(a + b) / 2 for a, b in zip(cuts, cuts[1:]) if b - a > 0.15]
    files = []
    for i, t in enumerate(mids):
        p = f"{R}/shots/{vid}/{i:03d}_{t:06.2f}.jpg"
        if not os.path.exists(p):
            subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", f"{R}/proxy/{vid}.mp4", "-frames:v", "1", "-q:v", "3", p])
        files.append((t, p))
    cols, rows, w, h = 8, 5, 160, 284
    for k in range(0, len(files), cols * rows):
        S = Image.new("RGB", (cols * w, rows * (h + 14)), "white"); d = ImageDraw.Draw(S)
        for j, (t, p) in enumerate(files[k:k + cols * rows]):
            x, y = (j % cols) * w, (j // cols) * (h + 14)
            S.paste(Image.open(p).resize((w, h)), (x, y + 14)); d.text((x + 3, y + 1), f"{t:.1f}s", fill="black")
        S.save(f"{R}/sheets/{vid}_{k // (cols * rows)}.jpg", quality=85)
    print(vid, len(files), "shots")
