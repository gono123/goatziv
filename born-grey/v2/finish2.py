"""v2 finish: sound effects + original dreamy bed + one-word captions -> two MP4s.

    tts/bin/python finish2.py
      out/born_grey_v2_preview.mp4  voice + sound effects + an original slow dreamy track (to review)
      out/born_grey_v2_upload.mp4   voice + sound effects only: add the song in YouTube's Shorts editor

Style (../STYLE_GUIDE.md): one lowercase word at a time, no punctuation, white bold geometric sans
with a black outline and soft shadow, ~72% down; music steady, ~8 dB under the voice; ~1 hit per shot.
"""
import json, os, re, subprocess
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, lfilter, resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
TL = json.load(open(os.path.join(OUT, "timeline.json")))
FPS = TL["fps"]
SR = 48000
DUR = TL["duration"]
N = int(DUR * SR) + SR
rng = np.random.default_rng(11)
SH = {s["id"]: s for s in TL["shots"]}


def tt(d): return np.arange(int(d * SR)) / SR
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, f / (SR / 2), "low", output="sos"), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f / (SR / 2), "high", output="sos"), x, axis=0)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a / (SR / 2), b / (SR / 2)], "band", output="sos"), x, axis=0)
def noise(d): return rng.standard_normal(int(d * SR))


def put(bus, sig, t, gain=1.0, pan=0.0):
    i = int(max(0, t) * SR)
    if i >= len(bus) or len(sig) == 0:
        return
    sig = sig[: len(bus) - i]
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    bus[i:i + len(sig), 0] += sig * gain * l
    bus[i:i + len(sig), 1] += sig * gain * r


def reverb(x, wet=0.35, size=1.3, decay=0.86):
    out = np.zeros_like(x)
    for ch, combs in enumerate(([1557, 1617, 1491, 1422, 1277], [1356, 1188, 1116, 1601, 1453])):
        y = np.zeros(len(x))
        for D in combs:
            D = int(D * size * SR / 44100); a = np.zeros(D + 1); a[0] = 1; a[D] = -decay
            y += lfilter([1], a, x[:, ch])
        for D in (556, 441, 341):
            D = int(D * SR / 44100); b = np.zeros(D + 1); b[0] = -0.5; b[D] = 1; a = np.zeros(D + 1); a[0] = 1; a[D] = -0.5
            y = lfilter(b, a, y)
        out[:, ch] = y * 0.1
    return x * (1 - wet) + out * wet


# ----------------------------------------------------------------------------- dreamy bed (original)
BPM = 72
BEAT = 60 / BPM
PROG = [  # D  Bm  G  A   (I vi IV V), slow and warm
    (50, [62, 66, 69, 74]), (47, [62, 66, 71, 74]), (43, [59, 62, 67, 71]), (45, [61, 64, 69, 73])]


def guitar(m, d=2.5, vel=1.0):
    """Clean chorus-y electric pluck."""
    t = tt(d); f = hz(m)
    y = sum((0.8 ** k) * np.sin(2 * np.pi * f * k * t * (1 + 0.0015 * np.sin(2 * np.pi * 0.7 * t))) * np.exp(-t * (1.6 + 0.8 * k)) for k in range(1, 7))
    return lp(y * np.minimum(1, t / 0.006), 3500) * vel * 0.22


def pad(notes, d, vel=1.0):
    t = tt(d)
    y = sum(np.sin(2 * np.pi * hz(m) * (1 + dt) * t) for m in notes for dt in (-0.004, 0.004)) / (2 * len(notes))
    e = np.minimum(1, t / 1.2) * np.minimum(1, (d - t) / 1.2)
    return lp(y * e, 1500) * vel * 0.35


def bassn(m, d, vel=1.0):
    t = tt(d)
    return np.sin(2 * np.pi * hz(m) * t) * np.minimum(1, t / 0.02) * np.exp(-t * 0.8) * vel * 0.32


def kick(vel=1.0):
    t = tt(0.35); f = 45 + 70 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10) * vel * 0.5


def brush(vel=1.0):
    t = tt(0.25)
    return bp(noise(0.25), 2500, 9000) * np.exp(-t * 18) * vel * 0.12


def bed():
    mus = np.zeros((N, 2))
    bar = 4 * BEAT
    t, k = 0.0, 0
    arp = [0, 2, 1, 3, 2, 1, 3, 2]
    while t < DUR:
        root, ch = PROG[k % 4]
        put(mus, pad(ch, bar + 1.2), t, 1.0)
        put(mus, bassn(root, bar), t, 1.0)
        for i in range(8):
            put(mus, guitar(ch[arp[i]] + (12 if i in (3, 6) else 0), 2.2, 0.9 if i % 2 == 0 else 0.7), t + i * BEAT / 2, pan=0.25 if i % 2 else -0.25)
        for b in range(4):
            if b in (0, 2):
                put(mus, kick(0.8), t + b * BEAT)
            put(mus, brush(1.0 if b in (1, 3) else 0.5), t + b * BEAT, pan=0.2)
        t += bar; k += 1
    mus = reverb(mus, wet=0.45, size=1.5)
    e = np.minimum(1, np.arange(N) / (SR * 1.5))[:, None] * np.minimum(1, (DUR * SR - np.arange(N)) / (SR * 2.5)).clip(0, 1)[:, None]
    return mus * e


# ----------------------------------------------------------------------------- sound effects
def whoosh(d=0.35):
    t = tt(d); n = noise(d); out = np.zeros_like(n); seg = int(SR * 0.02)
    for i in range(0, len(n), seg):
        p = i / len(n); fc = 500 + 2500 * np.sin(np.pi * p)
        out[i:i + seg] = bp(n[i:i + seg + 300], fc * 0.7, fc * 1.3)[: len(n[i:i + seg])]
    return out * np.sin(np.pi * t / d) ** 2 * 0.35


def pop():
    t = tt(0.12); return np.sin(2 * np.pi * np.cumsum(500 + 2400 * t / 0.12) / SR) * np.exp(-t * 30) * 0.35


def chime(n=10, spread=0.8):
    y = np.zeros(int((spread + 1.2) * SR))
    for _ in range(n):
        f = hz(int(rng.choice([86, 88, 90, 93, 95, 98])))
        t = tt(1.0); s = np.sin(2 * np.pi * f * t) * np.exp(-t * 4) * 0.12
        i = int(rng.uniform(0, spread) * SR); y[i:i + len(s)] += s
    return y


def impact(vel=1.0):
    t = tt(0.5); return (np.sin(2 * np.pi * (60 + 60 * np.exp(-t * 20)) * t) * np.exp(-t * 9) + lp(noise(0.5), 900) * np.exp(-t * 25) * 0.5) * vel * 0.6


def crack():
    t = tt(1.4)
    y = hp(noise(1.4), 2500) * np.exp(-t * 25) * 0.8 + sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 3) * 0.08 for f in (2200, 3150, 4400))
    return y + np.sin(2 * np.pi * 70 * t) * np.exp(-t * 12) * 0.5


def knock3():
    y = np.zeros(int(0.9 * SR))
    for k in range(3):
        t = tt(0.2); s = np.sin(2 * np.pi * (150 - 60 * t) * t) * np.exp(-t * 32) + lp(noise(0.2), 1200) * np.exp(-t * 60) * 0.5
        i = int(k * 0.24 * SR); y[i:i + len(s)] += s * 0.8
    return y


def siren(d):
    t = tt(d); f = np.where((t // 0.42) % 2 == 0, 740.0, 990.0); f = lp(f, 25)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.3) * 0.16


def rain_bed(d, vel=1.0):
    t = tt(d)
    return bp(noise(d), 500, 9000) * 0.12 * np.minimum(1, t / 0.5) * np.minimum(1, (d - t) / 0.5) * vel


def scrubs(d):
    y = np.zeros(int(d * SR)); k = 0
    while k * 0.33 < d - 0.3:
        s = bp(noise(0.25), 1500, 6000) * np.sin(np.pi * tt(0.25) / 0.25) * 0.25
        i = int(k * 0.33 * SR); y[i:i + len(s)] += s; k += 1
    return y


def clunk():
    t = tt(1.0); return np.sin(2 * np.pi * 80 * t) * np.exp(-t * 14) + (np.sin(2 * np.pi * 620 * t) + np.sin(2 * np.pi * 1530 * t)) * np.exp(-t * 5) * 0.15


def rumble(d):
    t = tt(d); return lp(noise(d), 150, 4) * 3 * np.minimum(1, t / 0.3) * np.exp(-t * 0.7)


def sfx_track():
    fx = np.zeros((N, 2))
    for j, s in enumerate(TL["shots"]):
        if j and j % 2 == 0:              # a soft whoosh on every other cut (the reference: ~1 hit per shot)
            put(fx, whoosh(), s["start"] - 0.18, 0.7, pan=rng.uniform(-0.4, 0.4))
    def at(sid, word=None, off=0.0):
        s = SH[sid]
        if word:
            for w in s["words"]:
                if word in w["w"].lower():
                    return w["s"] + off
        return s["start"] + off
    def span(a, b):
        return SH[a]["start"], SH[b]["end"]
    put(fx, pop(), at("drop_yellow", "yellow"))
    put(fx, chime(8, 0.6), at("grandma_sock", "sock"))
    put(fx, chime(10, 0.8), at("prism_shield", "hurts"), 0.8)
    put(fx, impact(0.7), at("sign_rule"))
    a, b = span("inspectors_march", "inspector_close")
    for k in range(int((b - a) / 0.5)):
        put(fx, impact(0.25), a + k * 0.5)
    put(fx, scrubs(SH["scrub"]["end"] - SH["scrub"]["start"]), SH["scrub"]["start"])
    put(fx, impact(1.0), at("inspector_close", "forever"))
    put(fx, crack(), at("crack_sound", "crack"))
    a, b = span("rain_drop", "kids_stare"); put(fx, rain_bed(b - a, 0.8), a)
    put(fx, chime(24, 1.4), at("pink_reveal"), 1.2)
    put(fx, impact(0.5), at("sandwich", "dropped", 0.3))
    a, b = span("sirens", "pip_scrub"); put(fx, siren(b - a), a)
    put(fx, scrubs(SH["pip_scrub"]["end"] - SH["pip_scrub"]["start"]), SH["pip_scrub"]["start"])
    put(fx, impact(0.6), at("home_door", "locked"))
    put(fx, impact(0.8), at("blackout"))
    put(fx, knock3(), at("knock", "knock"))
    put(fx, impact(0.9), at("prism_point", "wash"))
    put(fx, clunk(), at("lever_pull", "opened"))
    put(fx, rumble(3.0), at("dome_split"))
    a, b = span("rain_city", "prism_grey"); put(fx, rain_bed(b - a, 1.1), a)
    put(fx, chime(20, 2.0), at("wash_town"), 0.9)
    put(fx, chime(10, 0.6), at("pip_shoelace_blue", "blue"))
    put(fx, chime(8, 0.5), at("ending", "suits"), 0.8)
    return reverb(fx, wet=0.12, size=0.8)


# ----------------------------------------------------------------------------- captions
def ts(t):
    t = max(0.0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def captions():
    words = [w for s in TL["shots"] for w in s["words"]]
    ev = []
    for i, w in enumerate(words):
        txt = re.sub(r"[^\w'’-]", "", w["w"]).lower()
        if not txt:
            continue
        end = words[i + 1]["s"] if i + 1 < len(words) else w["e"] + 0.6
        end = min(end, w["e"] + 0.5) if i + 1 < len(words) and words[i + 1]["s"] - w["e"] > 0.6 else end
        ev.append((w["s"], max(end, w["s"] + 0.12), txt))
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: W,Montserrat Bold Static,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,4.5,4,2,40,40,500,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    path = os.path.join(OUT, "captions.ass")
    open(path, "w").write(head + "".join(f"Dialogue: 0,{ts(a)},{ts(b)},W,,0,0,0,,{t}\n" for a, b, t in ev))
    return path, len(ev)


# ----------------------------------------------------------------------------- assemble
def frames_seq():
    seq = os.path.join(OUT, "seq"); os.makedirs(seq, exist_ok=True)
    for f in os.listdir(seq):
        os.remove(os.path.join(seq, f))
    k, missing = 0, {}
    for s in TL["shots"]:
        n = round(s["end"] * FPS) - round(s["start"] * FPS)
        last = None
        for i in range(1, n + 1):
            p = os.path.join(OUT, "frames", s["id"], f"{i:04d}.png")
            if os.path.exists(p):
                last = p
            else:
                missing[s["id"]] = missing.get(s["id"], 0) + 1
            src = p if os.path.exists(p) else last
            if src is None:
                raise SystemExit(f"no frames for {s['id']}")
            k += 1
            os.symlink(src, os.path.join(seq, f"{k:06d}.png"))
    if missing:
        print("WARNING padded:", missing)
    return seq, k


def main():
    vo, vsr = sf.read(os.path.join(OUT, "vo.wav"), dtype="float32")
    vo = resample_poly(vo, SR, vsr).astype(np.float64); vo = vo / (np.abs(vo).max() + 1e-9) * 0.85
    v = np.zeros((N, 2)); v[:len(vo), 0] = vo[:N]; v[:len(vo), 1] = vo[:N]
    fx = sfx_track(); fx = fx / (np.abs(fx).max() + 1e-9) * 0.55
    mus = bed(); mus = mus / (np.abs(mus).max() + 1e-9)
    def rms(x): return np.sqrt(np.mean(x ** 2) + 1e-12)
    mus *= rms(v[:, 0]) / rms(mus[:, 0]) * 10 ** (-8 / 20)       # music ~8 dB under the voice, steady
    L = int(DUR * SR)
    for name, mix in (("preview", v + fx + mus), ("upload", v + fx)):
        mix = np.tanh(mix[:L] * 1.05)
        sf.write(os.path.join(OUT, f"mix_{name}.wav"), mix.astype(np.float32), SR)
    cap, nw = captions()
    seq, n = frames_seq()
    fonts = os.path.join(HERE, "fonts")
    for name in ("preview", "upload"):
        out = os.path.join(OUT, f"born_grey_v2_{name}.mp4")
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(seq, "%06d.png"),
                        "-i", os.path.join(OUT, f"mix_{name}.wav"), "-vf", f"scale=1080:1920:flags=lanczos,ass={cap}:fontsdir={fonts}",
                        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
        print(out)
    print(f"{n} frames ({n / FPS:.1f}s), {nw} caption words")


if __name__ == "__main__":
    main()
