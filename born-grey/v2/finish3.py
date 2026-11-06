"""v3 finish: the silent film rendered on the user's PC + voice, one-word captions, sound effects and music.

    tts/bin/python finish3.py out/born_grey_v3_silent.mp4
      out/born_grey_v3.mp4          Numbers -> Cry (instrumental, the reference pattern), ready to post
      out/born_grey_v3_nomusic.mp4  voice + effects only (to add a song in YouTube instead)
"""
import os, subprocess, sys
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
import finish2 as F

silent = sys.argv[1] if len(sys.argv) > 1 else os.path.join(F.OUT, "born_grey_v3_silent.mp4")
# optional colour correction first, e.g. --pre "lut3d=out/fix_agx.cube,eq=saturation=1.15"
PRE = sys.argv[sys.argv.index("--pre") + 1] + "," if "--pre" in sys.argv else ""
MUSIC = os.path.join(os.path.dirname(F.HERE), "music", "stems", "htdemucs")
TURN = "recess"                  # "Then, one Tuesday at recess..." : the story turns, the music changes
SR = F.SR
L = int(F.DUR * SR)

vo, vsr = sf.read(os.path.join(F.OUT, "vo.wav"), dtype="float32")
vo = resample_poly(vo, SR, vsr).astype(np.float64); vo = vo / (np.abs(vo).max() + 1e-9) * 0.85
v = np.zeros((L, 2)); n = min(L, len(vo)); v[:n, 0] = vo[:n]; v[:n, 1] = vo[:n]
fx = F.sfx_track()[:L]; fx = fx / (np.abs(fx).max() + 1e-9) * 0.55


def load(name):
    s, ssr = sf.read(os.path.join(MUSIC, name, "no_vocals.wav"), dtype="float32", always_2d=True)
    s = resample_poly(s, SR, ssr, axis=0).astype(np.float64)
    return s / (np.sqrt(np.mean(s ** 2)) + 1e-9)


def active_rms(x):
    hop = SR // 20
    fr = np.sqrt(np.mean(x[: len(x) // hop * hop].reshape(-1, hop) ** 2, axis=1))
    return float(np.median(fr[fr > fr.max() * 0.1]))


t_turn = F.SH[TURN]["start"] - 0.15
XF = 1.4
bed = np.zeros((L, 2))
a = load("numbers"); b = load("cry")
ia, ib = int((t_turn + XF) * SR), int(t_turn * SR)
seg = a[:ia]
env = np.minimum(1, np.arange(ia) / (0.8 * SR)) * np.clip((t_turn + XF - np.arange(ia) / SR) / XF, 0, 1)
bed[:ia] += seg[:ia] * env[:, None]
segb = b[: L - ib]
envb = np.minimum(1, np.arange(len(segb)) / (XF * SR))
bed[ib:ib + len(segb)] += segb * envb[:, None]
t = np.arange(L) / SR
bed *= np.clip((F.DUR - t) / 2.5, 0, 1)[:, None]
bed *= active_rms(v[:, 0]) / active_rms(bed[:, 0]) * 10 ** (-8 / 20)      # ~8 dB under the voice

cap, nw = F.captions()
for name, mix in (("born_grey_v3", v + fx + bed), ("born_grey_v3_nomusic", v + fx)):
    wav = os.path.join(F.OUT, f"mix_{name}.wav")
    sf.write(wav, np.tanh(mix * 1.05).astype(np.float32), SR)
    out = os.path.join(F.OUT, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", silent, "-i", wav,
                    "-vf", f"{PRE}ass={cap}:fontsdir={os.path.join(F.HERE, 'fonts')}", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(F.FPS),
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out)
print(f"music: Numbers until {t_turn:.1f}s, then Cry; {nw} caption words")
