"""Put a real song under the finished video, the way the reference channel does: one song under the whole
video, steady, ~8 dB under the narration (5-11 dB in the reference), fading out at the end.

    tts/bin/python add_song.py <song.wav> <name> [--db 8] [--start 0]
      -> out/born_grey_v2_<name>.mp4  (video stream copied from the upload version, new audio)
"""
import argparse, os, subprocess
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
import finish2 as F

ap = argparse.ArgumentParser()
ap.add_argument("song"); ap.add_argument("name")
ap.add_argument("--db", type=float, default=8.0, help="how far under the voice")
ap.add_argument("--start", type=float, default=0.0, help="where in the song to begin (s)")
a = ap.parse_args()

SR = F.SR
L = int(F.DUR * SR)
vo, vsr = sf.read(os.path.join(F.OUT, "vo.wav"), dtype="float32")
vo = resample_poly(vo, SR, vsr).astype(np.float64)
vo = vo / (np.abs(vo).max() + 1e-9) * 0.85
v = np.zeros((L, 2)); n = min(L, len(vo)); v[:n, 0] = vo[:n]; v[:n, 1] = vo[:n]
fx = F.sfx_track()[:L]; fx = fx / (np.abs(fx).max() + 1e-9) * 0.55

song, ssr = sf.read(a.song, dtype="float32", always_2d=True)
song = resample_poly(song, SR, ssr, axis=0).astype(np.float64)
s0 = int(a.start * SR)
song = song[s0:s0 + L]
if len(song) < L:
    song = np.concatenate([song, np.zeros((L - len(song), 2))])
t = np.arange(L) / SR
env = np.minimum(1, t / 0.8) * np.clip((F.DUR - t) / 2.5, 0, 1)
song *= env[:, None]


def active_rms(x):
    """Loudness of the voice while it is speaking (ignores the gaps)."""
    hop = SR // 20
    fr = np.sqrt(np.mean(x[: len(x) // hop * hop].reshape(-1, hop) ** 2, axis=1))
    return float(np.median(fr[fr > fr.max() * 0.1]))


song *= active_rms(v[:, 0]) / active_rms(song[:, 0]) * 10 ** (-a.db / 20)
mix = np.tanh((v + fx + song) * 1.05)
wav = os.path.join(F.OUT, f"mix_{a.name}.wav")
sf.write(wav, mix.astype(np.float32), SR)
out = os.path.join(F.OUT, f"born_grey_v2_{a.name}.mp4")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", os.path.join(F.OUT, "born_grey_v2_upload.mp4"), "-i", wav,
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
print(out)
