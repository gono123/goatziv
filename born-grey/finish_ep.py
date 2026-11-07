"""Finish one Nov 7 episode: picture + cloned voice + one-word captions + sound effects + instrumental music.

    tts/bin/python finish_ep.py <ep> [silent.mp4]
      <ep>/out/<ep>.mp4          music: the world song until the story's turn, then Cry (instrumental, ~8 dB under the voice)
      <ep>/out/<ep>_nomusic.mp4  voice + effects only (add a song in YouTube instead)
Without silent.mp4 the cloud-rendered frames in <ep>/out/frames are used.
"""
import json, os, subprocess, sys
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "v2"))
import finish2 as F

EP = sys.argv[1]
EPD = os.path.join(ROOT, EP)
sys.path.insert(0, EPD)
from lines import TURN

F.OUT = os.path.join(EPD, "out")
F.TL = json.load(open(os.path.join(F.OUT, "timeline.json")))
F.SH = {s["id"]: s for s in F.TL["shots"]}
F.DUR = F.TL["duration"]
F.N = int(F.DUR * F.SR) + F.SR
F.HERE = os.path.join(ROOT, "v2")
SR, L = F.SR, int(F.DUR * F.SR)
WORLD_SONG = {"moon": "six_forty_seven"}.get(EP, "numbers")
MUSIC = os.path.join(ROOT, "music", "stems", "htdemucs")


def at(sid, word=None, off=0.0):
    s = F.SH.get(sid)
    if s is None:
        return None
    if word:
        for w in s["words"]:
            if word in w["w"].lower():
                return w["s"] + off
    return s["start"] + off


def span(a, b):
    return F.SH[a]["start"], F.SH[b]["end"]


def put(fx, sig, t, g=1.0):
    if t is not None:
        F.put(fx, sig, t, g)


def sfx():
    fx = np.zeros((F.N, 2))
    for j, s in enumerate(F.TL["shots"]):
        if j and j % 2 == 0:
            F.put(fx, F.whoosh(), s["start"] - 0.18, 0.7, pan=F.rng.uniform(-0.4, 0.4))
    put(fx, F.impact(0.7), at("sign_rule"))
    if EP == "robot":
        put(fx, F.clunk(), at("bolt"))
        put(fx, F.chime(8, 0.6), at("robot_on", "on"))
        for sid in ("nope_first", "homework_nope", "clean_nope"):
            put(fx, F.pop(), at(sid, "nope"))
        put(fx, F.impact(0.6), at("update"))
        put(fx, F.impact(0.8), at("eyes_red", "red"))
        a, b = span("march", "grab_kids")
        for k in range(int((b - a) / 0.5)):
            put(fx, F.impact(0.25), a + k * 0.5)
        put(fx, F.siren(F.SH["hero_run"]["end"] - F.SH["hero_run"]["start"]), F.SH["hero_run"]["start"], 0.6)
        put(fx, F.chime(24, 1.4), at("nope_big"), 1.1)
        put(fx, F.impact(1.0), at("error"))
        put(fx, F.rumble(1.5), at("shutdown", "off"))
        put(fx, F.chime(16, 1.0), at("reboot", "blue"), 0.8)
        put(fx, F.chime(10, 0.8), at("famous"), 0.8)
        put(fx, F.pop(), at("ending_nope", "nope"))
    elif EP == "balloon":
        put(fx, F.chime(8, 0.6), at("mood"), 0.6)
        put(fx, F.pop(), at("mad_red", "red")); put(fx, F.pop(), at("sad_blue", "blue")); put(fx, F.pop(), at("lie_green", "green"))
        put(fx, F.impact(0.6), at("float_away", "float"))
        put(fx, F.impact(1.0), at("let_go", "go"))
        put(fx, F.rumble(1.5), at("lift"), 0.5)
        put(fx, F.impact(0.6), at("mom_scream"))
        put(fx, F.chime(20, 1.4), at("fly"), 1.0)
        put(fx, F.chime(10, 0.8), at("milo_hi"), 0.8)
        if "pop" in F.SH:
            a, b = span("pop", "pop")
            for k in range(6):
                put(fx, F.pop(), a + 0.25 + k * (b - a - 0.4) / 6, 0.9)
        put(fx, F.impact(0.5), at("land"))
        put(fx, F.pop(), at("mom_red", "red"))
        put(fx, F.chime(8, 0.5), at("ending_candy"), 0.8)
    elif EP == "moon":
        put(fx, F.rumble(2.0), at("beam", "shines"))
        put(fx, F.rumble(1.5), at("float"), 0.6)
        put(fx, F.impact(0.9), at("moon_eye", "looks"))
        put(fx, F.impact(0.8), at("pip_look", "looked"))
        put(fx, F.rumble(2.5), at("pip_beam"))
        put(fx, F.impact(0.6), at("calendar", "moon"))
        put(fx, F.impact(0.9), at("hero_look", "looked"))
        put(fx, F.impact(1.0), at("moon_eye2"))
        put(fx, F.rumble(2.0), at("hero_beam"))
        put(fx, F.chime(20, 1.6), at("hero_stars"), 0.8)
        put(fx, F.rumble(2.5), at("moon_face", "shook"))
        put(fx, F.impact(0.9), at("moon_face", "eyes"))
        put(fx, F.chime(16, 1.2), at("moon_smile"), 0.9)
        put(fx, F.chime(20, 1.6), at("beam_down"), 0.8)
        put(fx, F.impact(0.8), at("ending_sun", "too"))
    return F.reverb(fx, wet=0.12, size=0.8)


def load(name):
    s, ssr = sf.read(os.path.join(MUSIC, name, "no_vocals.wav"), dtype="float32", always_2d=True)
    s = resample_poly(s, SR, ssr, axis=0).astype(np.float64)
    return s / (np.sqrt(np.mean(s ** 2)) + 1e-9)


def active_rms(x):
    hop = SR // 20
    fr = np.sqrt(np.mean(x[: len(x) // hop * hop].reshape(-1, hop) ** 2, axis=1))
    return float(np.median(fr[fr > fr.max() * 0.1]))


vo, vsr = sf.read(os.path.join(F.OUT, "vo.wav"), dtype="float32")
vo = resample_poly(vo, SR, vsr).astype(np.float64); vo = vo / (np.abs(vo).max() + 1e-9) * 0.85
v = np.zeros((L, 2)); n = min(L, len(vo)); v[:n, 0] = vo[:n]; v[:n, 1] = vo[:n]
fx = sfx()[:L]; fx = fx / (np.abs(fx).max() + 1e-9) * 0.55

t_turn = F.SH[TURN]["start"] - 0.15
XF = 1.4
bed = np.zeros((L, 2))
a, b = load(WORLD_SONG), load("cry")
ia, ib = min(len(a), int((t_turn + XF) * SR)), int(t_turn * SR)
env = np.minimum(1, np.arange(ia) / (0.8 * SR)) * np.clip((t_turn + XF - np.arange(ia) / SR) / XF, 0, 1)
bed[:ia] += a[:ia] * env[:, None]
segb = b[: L - ib]
bed[ib:ib + len(segb)] += segb * np.minimum(1, np.arange(len(segb)) / (XF * SR))[:, None]
bed *= np.clip((F.DUR - np.arange(L) / SR) / 2.5, 0, 1)[:, None]
bed *= active_rms(v[:, 0]) / active_rms(bed[:, 0]) * 10 ** (-8 / 20)

cap, nw = F.captions()
fonts = os.path.join(ROOT, "v2", "fonts")
if len(sys.argv) > 2:
    vin = ["-i", sys.argv[2]]
else:
    seq, nf = F.frames_seq()
    vin = ["-framerate", str(F.FPS), "-i", os.path.join(seq, "%06d.png")]
for name, mix in ((EP, v + fx + bed), (EP + "_nomusic", v + fx)):
    wav = os.path.join(F.OUT, f"mix_{name}.wav")
    sf.write(wav, np.tanh(mix * 1.05).astype(np.float32), SR)
    out = os.path.join(F.OUT, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + vin + ["-i", wav,
                    "-vf", f"scale=1080:1920:flags=lanczos,ass={cap}:fontsdir={fonts}", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(F.FPS),
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out)
print(f"{EP}: {WORLD_SONG} until {t_turn:.1f}s, then Cry; {nw} caption words")
