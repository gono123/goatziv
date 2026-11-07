"""Contact sheets of out/preview/*.png in script order -> out/sheet_<k>.png"""
import glob, json, os
from PIL import Image, ImageDraw
order = [s["id"] for s in json.load(open("out/timeline.json"))["shots"]]
files = []
for sid in order:
    fs = sorted(f for f in glob.glob(f"out/preview/{sid}_*.png") if f[len(f"out/preview/{sid}_"):-4].isdigit())
    if fs: files.append((sid, fs[-1]))
w, h, cols, rows = 200, 356, 10, 2
for k in range(0, len(files), cols * rows):
    S = Image.new("RGB", (w * cols, (h + 16) * rows), "white"); d = ImageDraw.Draw(S)
    for i, (sid, f) in enumerate(files[k:k + cols * rows]):
        x, y = (i % cols) * w, (i // cols) * (h + 16)
        S.paste(Image.open(f).convert("RGB").resize((w, h)), (x, y + 16)); d.text((x + 3, y + 2), f"{k+i+1}. {sid}", fill="black")
    S.save(f"out/sheet_{k // (cols * rows)}.png"); print(f"out/sheet_{k // (cols * rows)}.png")
