"""The reference music pattern: one song for the world and its rule, then another from the story's turn
(each from the start of its song), crossfaded, steady, ~8 dB under the voice. Instrumental versions.

    tts/bin/python add_songs.py <name> <song1.wav> [<turn_shot> <song2.wav> [<shot> <song3.wav> ...]] [--db 8]
      -> out/born_grey_v2_<name>.mp4   e.g.  add_songs.py v3 numbers.wav crack_sound cry.wav
"""
import os, subprocess, sys
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
import finish2 as F

args = sys.argv[1:]
db = 8.0
if "--db" in args:
    i = args.index("--db"); db = float(args[i + 1]); del args[i:i + 2]
name, parts = args[0], args[1:]
songs = [(None, parts[0])] + [(parts[i], parts[i + 1]) for i in range(1, len(parts) - 1, 2)]
SR = F.SR
L = int(F.DUR * SR)
starts = [0.0] + [F.SH[sid]["start"] - 0.15 for sid, _ in songs[1:]]
XF = 1.2                                     # crossfade seconds

bed = np.zeros((L, 2))
for k, ((sid, path), t0) in enumerate(zip(songs, starts)):
    t1 = starts[k + 1] if k + 1 < len(starts) else F.DUR
    s, ssr = sf.read(path, dtype="float32", always_2d=True)
    s = resample_poly(s, SR, ssr, axis=0).astype(np.float64)
    a, b = int(t0 * SR), int(min(F.DUR, t1 + XF) * SR)
    seg = s[: b - a]
    if len(seg) < b - a:
        seg = np.concatenate([seg, np.zeros((b - a - len(seg), 2))])
    t = np.arange(b - a) / SR
    env = np.minimum(1, t / (XF if k else 0.8))
    if k + 1 < len(starts):
        env *= np.clip((t1 + XF - t0 - t) / XF, 0, 1)
    seg = seg / (np.sqrt(np.mean(seg ** 2)) + 1e-9)          # every song at the same level
    bed[a:b] += seg * env[:, None]
t = np.arange(L) / SR
bed *= np.clip((F.DUR - t) / 2.5, 0, 1)[:, None]

vo, vsr = sf.read(os.path.join(F.OUT, "vo.wav"), dtype="float32")
vo = resample_poly(vo, SR, vsr).astype(np.float64); vo = vo / (np.abs(vo).max() + 1e-9) * 0.85
v = np.zeros((L, 2)); n = min(L, len(vo)); v[:n, 0] = vo[:n]; v[:n, 1] = vo[:n]
fx = F.sfx_track()[:L]; fx = fx / (np.abs(fx).max() + 1e-9) * 0.55


def active_rms(x):
    hop = SR // 20
    fr = np.sqrt(np.mean(x[: len(x) // hop * hop].reshape(-1, hop) ** 2, axis=1))
    return float(np.median(fr[fr > fr.max() * 0.1]))


bed *= active_rms(v[:, 0]) / active_rms(bed[:, 0]) * 10 ** (-db / 20)
mix = np.tanh((v + fx + bed) * 1.05)
wav = os.path.join(F.OUT, f"mix_{name}.wav")
sf.write(wav, mix.astype(np.float32), SR)
out = os.path.join(F.OUT, f"born_grey_v2_{name}.mp4")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", os.path.join(F.OUT, "born_grey_v2_upload.mp4"), "-i", wav,
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
print(out, "switches at", [round(x, 1) for x in starts])
