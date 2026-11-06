"""Fit a 3D LUT that undoes the washed-out colours of a joined video, from frames of the same shots
rendered with correct colours (out/frames_nomocap). -> out/fix_agx.cube (apply with ffmpeg lut3d)."""
import json, os, subprocess
import numpy as np
from PIL import Image
from scipy.spatial import cKDTree
from scipy.ndimage import uniform_filter
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"))
tl = json.load(open("timeline.json"))
A, Bv = [], []
for s in tl["shots"]:
    d = f"frames_nomocap/{s['id']}"
    if not os.path.isdir(d): continue
    n = round(s["end"] * 24) - round(s["start"] * 24); k = max(1, n // 2)
    t = (round(s["start"] * 24) + k - 1) / 24 + 0.01
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", "born_grey_v3_silent.mp4", "-frames:v", "1", "-vf", "scale=180:320",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    if len(raw) != 180 * 320 * 3: continue
    A.append(np.frombuffer(raw, np.uint8).reshape(-1, 3) / 255.0)
    Bv.append(np.asarray(Image.open(f"{d}/{k:04d}.png").convert("RGB").resize((180, 320), Image.BILINEAR)).reshape(-1, 3) / 255.0)
A = np.concatenate(A); Bv = np.concatenate(Bv)
N = 17
idx = np.clip(np.round(A * (N - 1)).astype(int), 0, N - 1)
flat = idx[:, 0] * N * N + idx[:, 1] * N + idx[:, 2]
order = np.argsort(flat); fs = flat[order]; bs = Bv[order]
starts = np.r_[0, np.flatnonzero(np.diff(fs)) + 1]; ends = np.r_[starts[1:], len(fs)]
lut = np.zeros((N ** 3, 3)); cnt = np.zeros(N ** 3)
for s0, e0 in zip(starts, ends):
    lut[fs[s0]] = np.median(bs[s0:e0], axis=0); cnt[fs[s0]] = e0 - s0
grid = np.stack(np.meshgrid(*[np.linspace(0, 1, N)] * 3, indexing="ij"), -1).reshape(-1, 3)
good = cnt >= 8
dist, nn = cKDTree(grid[good]).query(grid, k=8)
w = 1 / (dist + 1e-3)
corr = ((lut[good] - grid[good])[nn] * w[..., None]).sum(1) / w.sum(1)[:, None]
full = np.clip(np.where(good[:, None], lut, grid + corr), 0, 1).reshape(N, N, N, 3)
full = np.stack([uniform_filter(full[..., c], size=3, mode="nearest") for c in range(3)], -1)
with open("fix_agx.cube", "w") as f:
    f.write(f"LUT_3D_SIZE {N}\n")
    for b in range(N):
        for g in range(N):
            for r in range(N):
                f.write("%.5f %.5f %.5f\n" % tuple(full[r, g, b]))
print("pixels", len(A), "bins", int(good.sum()), "-> fix_agx.cube")
