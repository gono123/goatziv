"""Contact sheet of out/preview/*.png -> out/test/sheet_<n>.png"""
import glob, os, sys
from PIL import Image, ImageDraw
files = sorted(glob.glob("out/preview/*.png"), key=lambda f: (os.path.getmtime(f)))
w, h, cols, rows = 240, 427, 8, 2
for k in range(0, len(files), cols * rows):
    S = Image.new("RGB", (w * cols, (h + 18) * rows), "white")
    d = ImageDraw.Draw(S)
    for i, f in enumerate(files[k:k + cols * rows]):
        x, y = (i % cols) * w, (i // cols) * (h + 18)
        S.paste(Image.open(f).convert("RGB").resize((w, h)), (x, y + 18))
        d.text((x + 4, y + 3), os.path.basename(f)[:-4], fill="black")
    S.save(f"out/test/sheet_{k // (cols * rows)}.png")
    print(f"out/test/sheet_{k // (cols * rows)}.png")
