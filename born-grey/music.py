"""Original score + sound effects, cued from out/timeline.json, mixed with the voiceover.

    python music.py   ->  out/music.wav, out/sfx.wav, out/mix.wav (48 kHz stereo)

Everything is synthesized here (no samples), so it is ours to use. The score follows the story:
storybook music box (worldbuilding) -> low drone (inspectors) -> soft theme (school/home) ->
suspense riser (crack/rain) -> magical shimmer (the pink reveal) -> chase pulse (sirens) ->
tender pad (mom's secret) -> driving ostinato (knock/escape/lever) -> triumphant tutti (dome opens) ->
playful pizzicato (Mr. Prism's comeuppance).
"""
import json, os
import numpy as np
import soundfile as sf
from scipy.signal import lfilter, butter, sosfilt, resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SR = 48000
TL = json.load(open(os.path.join(OUT, "timeline.json")))
DUR = TL["duration"]
N = int(DUR * SR) + SR
rng = np.random.default_rng(7)

SHOT = {s["id"]: s for s in TL["shots"]}


def t_of(shot, line=None, chunk=None, edge="start"):
    s = SHOT[shot]
    if line is None:
        return s[edge]
    L = s["lines"][line]
    if chunk is None:
        return L[edge]
    return L["chunks"][chunk][edge]


# ----------------------------------------------------------------------------- buses
music = np.zeros((N, 2))
sfx = np.zeros((N, 2))


def put(bus, sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or len(sig) == 0:
        return
    sig = sig[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    if sig.ndim == 1:
        bus[i:i + len(sig), 0] += sig * gain * l * 1.414
        bus[i:i + len(sig), 1] += sig * gain * r * 1.414
    else:
        bus[i:i + len(sig)] += sig * gain


def tt(d):
    return np.arange(int(d * SR)) / SR


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env_adsr(n, a=0.01, d=0.1, s=0.7, r=0.2):
    e = np.ones(n) * s
    ai, di, ri = int(a * SR), int(d * SR), int(r * SR)
    ai = min(ai, n); e[:ai] = np.linspace(0, 1, ai)
    de = min(n, ai + di); e[ai:de] = np.linspace(1, s, de - ai)
    if ri and n > ri:
        e[-ri:] *= np.linspace(1, 0, ri)
    return e


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc / (SR / 2), "low", output="sos"), x, axis=0)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc / (SR / 2), "high", output="sos"), x, axis=0)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo / (SR / 2), hi / (SR / 2)], "band", output="sos"), x, axis=0)


# ----------------------------------------------------------------------------- instruments

def musicbox(m, dur=1.2, vel=1.0):
    t = tt(dur); f = hz(m)
    parts = [(1, 1.0, 2.2), (2.0, 0.28, 4.5), (3.01, 0.14, 6), (4.17, 0.08, 8), (5.43, 0.04, 11)]
    y = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * dk) for k, a, dk in parts)
    y *= np.minimum(1, t / 0.002)
    return y * vel * 0.35


def pluck(m, dur=0.8, vel=1.0, bright=1.0):
    t = tt(dur); f = hz(m)
    y = sum((1 / k) * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (4 + k * 3 / bright)) for k in range(1, 9))
    y *= np.minimum(1, t / 0.003)
    return y * vel * 0.4


def piano(m, dur=2.0, vel=1.0):
    t = tt(dur); f = hz(m)
    y = sum((0.9 ** k / k) * np.sin(2 * np.pi * f * k * (1 + 0.0004 * k * k) * t) * np.exp(-t * (1.2 + 0.9 * k)) for k in range(1, 10))
    y *= np.minimum(1, t / 0.004) * env_adsr(len(t), 0.004, 0.05, 1, 0.25)
    return y * vel * 0.35


def saw(f, t, nh=14):
    return sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, nh + 1)) * 0.6


def pad(notes, dur, vel=1.0, a=0.8, r=1.2, cutoff=1800, detune=0.006):
    t = tt(dur)
    y = np.zeros(len(t))
    for m in notes:
        f = hz(m)
        for d in (-detune, 0, detune):
            y += saw(f * (1 + d), t + rng.random(), nh=10)
    y = lp(y, cutoff)
    return y * env_adsr(len(t), a, 0.3, 0.9, r) * vel * 0.05


def bass(m, dur=0.5, vel=1.0):
    t = tt(dur); f = hz(m)
    y = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    y = np.tanh(1.5 * y) * env_adsr(len(t), 0.005, 0.1, 0.6, 0.08)
    return y * vel * 0.32


def timp(m, dur=1.4, vel=1.0):
    t = tt(dur); f = hz(m)
    y = np.sin(2 * np.pi * f * t * (1 + 0.06 * np.exp(-t * 20))) * np.exp(-t * 2.5)
    y += lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 30) * 0.4
    return y * vel * 0.5


def kick(vel=1.0):
    t = tt(0.4)
    f = 45 + 110 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * vel * 0.8


def tick(vel=1.0, hi=6000):
    t = tt(0.06)
    return hp(rng.standard_normal(len(t)), hi) * np.exp(-t * 80) * vel * 0.25


def tom(m=45, vel=1.0):
    t = tt(0.6); f = hz(m)
    return np.sin(2 * np.pi * f * t * (1 + 0.3 * np.exp(-t * 15))) * np.exp(-t * 7) * vel * 0.6


def noise(d):
    return rng.standard_normal(int(d * SR))


def swell(d, lo=300, hi=6000, vel=1.0):
    """Riser: band-passed noise sweeping up, plus a rising tone."""
    t = tt(d)
    n = noise(d)
    out = np.zeros_like(n)
    seg = int(SR * 0.05)
    for i in range(0, len(n), seg):
        p = i / len(n)
        fc = lo * (hi / lo) ** p
        out[i:i + seg] = bp(n[i:i + seg + 400], fc * 0.7, min(fc * 1.4, SR / 2 - 100))[: len(n[i:i + seg])]
    tone = np.sin(2 * np.pi * np.cumsum(200 * 4 ** (t / d)) / SR) * 0.15
    return (out * 0.5 + tone) * (t / d) ** 2 * vel


def reverb(x, wet=0.25, size=1.0):
    """Small Schroeder reverb, stereo."""
    out = np.zeros_like(x)
    for ch, combs in enumerate(([1557, 1617, 1491, 1422], [1277, 1356, 1188, 1116])):
        y = np.zeros(len(x))
        for D in combs:
            D = int(D * size * SR / 44100)
            a = np.zeros(D + 1); a[0] = 1; a[D] = -0.82
            y += lfilter([1], a, x[:, ch])
        for D in (556, 441):
            D = int(D * SR / 44100)
            b = np.zeros(D + 1); b[0] = -0.5; b[D] = 1
            a = np.zeros(D + 1); a[0] = 1; a[D] = -0.5
            y = lfilter(b, a, y)
        out[:, ch] = y * 0.12
    return x * (1 - wet) + out * wet


# ----------------------------------------------------------------------------- score

BPM = 96
BEAT = 60 / BPM
# D minor storybook theme (MIDI), eighth notes; None = rest
THEME = [74, 77, 81, 79, 77, 76, 74, 76, 77, 81, 86, 84, 81, 79, 81, None,
         82, 81, 79, 77, 76, 77, 79, 76, 74, 76, 77, 74, 73, 74, None, None]
THEME_MAJ = [74, 78, 81, 79, 78, 76, 74, 76, 78, 81, 86, 85, 81, 79, 81, None,
             83, 81, 79, 78, 76, 78, 79, 76, 74, 76, 78, 81, 79, 78, 74, None]
CHORDS_MIN = [[50, 57, 62, 65], [46, 53, 58, 62], [48, 55, 60, 64], [45, 52, 57, 61]]  # Dm Bb C A
CHORDS_MAJ = [[50, 57, 62, 66], [47, 54, 59, 62], [43, 50, 55, 59], [45, 52, 57, 61]]  # D Bm G A
ROOTS_MIN = [38, 34, 36, 33]
ROOTS_MAJ = [38, 35, 31, 33]


def storybook(t0, t1, theme=THEME, chords=CHORDS_MIN, roots=ROOTS_MIN, box=True, plk=True, pd=True, vel=1.0, bpm=BPM):
    beat = 60 / bpm
    bar = 4 * beat
    t, k = t0, 0
    while t < t1 - 0.05:
        ci = (k // 1) % 4
        d = min(bar, t1 - t)
        if pd:
            put(music, pad(chords[ci], d + 0.8, vel=0.8 * vel, a=0.4, r=0.8), t, pan=0)
        if plk:
            for b in range(4):
                tb = t + b * beat
                if tb < t1:
                    put(music, pluck(roots[ci] + (12 if b % 2 else 0), 0.6, vel=0.8 * vel), tb, pan=-0.2)
        if box:
            for e in range(8):
                te = t + e * beat / 2
                m = theme[(k * 8 + e) % len(theme)]
                if m is not None and te < t1:
                    put(music, musicbox(m, 1.3, vel=0.55 * vel), te, pan=0.25)
        t += bar
        k += 1


def drone(t0, t1, m=38, vel=1.0):
    d = t1 - t0
    put(music, pad([m, m + 7], d + 1.5, vel=1.4 * vel, a=1.5, r=1.5, cutoff=500), t0)
    t = t0
    while t < t1:  # tick-tock clock
        put(music, tick(0.7 * vel, 5000), t, pan=-0.4)
        put(music, tick(0.5 * vel, 3000), t + BEAT, pan=0.4)
        t += 2 * BEAT


def pulse(t0, t1, bpm=140, roots=(38, 38, 41, 36), vel=1.0):
    step = 60 / bpm / 2
    t, i = t0, 0
    while t < t1:
        put(music, bass(roots[(i // 8) % len(roots)], step * 0.9, vel=vel), t)
        if i % 4 == 0:
            put(music, kick(0.7 * vel), t)
        put(music, tick(0.35 * vel), t + step / 2, pan=0.3)
        t += step; i += 1


def tender(t0, t1):
    beat = 60 / 72
    bar = 4 * beat
    prog = [[50, 57, 62, 65], [46, 53, 58, 62], [41, 48, 53, 57], [48, 55, 60, 64]]  # Dm Bb F C
    t, k = t0, 0
    while t < t1 - 0.1:
        c = prog[k % 4]
        put(music, pad(c, min(bar, t1 - t) + 1.2, vel=0.9, a=1.0, r=1.2, cutoff=1200), t)
        for b, m in enumerate([c[0] + 12, c[2] + 12, c[3] + 12, c[2] + 12]):
            if t + b * beat < t1:
                put(music, piano(m, 2.0, vel=0.45), t + b * beat, pan=0.15)
        t += bar; k += 1


def ostinato(t0, t1, vel=1.0):
    step = 60 / 120 / 4
    pat = [38, 38, 50, 38, 38, 48, 38, 46]
    t, i = t0, 0
    while t < t1:
        p = (t - t0) / max(0.1, t1 - t0)
        put(music, pluck(pat[i % 8], 0.25, vel=(0.5 + 0.5 * p) * vel, bright=1.5), t, pan=-0.1)
        if i % 8 == 0:
            put(music, tom(45, 0.6 + 0.4 * p), t)
        if i % 8 == 4:
            put(music, tom(50, 0.5 + 0.4 * p), t)
        t += step; i += 1
    put(music, pad([50, 57, 62], t1 - t0, vel=0.9, a=2.5, r=0.3, cutoff=900), t0)


def triumph(t0, t1):
    storybook(t0, t1, theme=THEME_MAJ, chords=CHORDS_MAJ, roots=ROOTS_MAJ, vel=1.25, bpm=104)
    bar = 4 * 60 / 104
    t, k = t0, 0
    while t < t1:
        c = CHORDS_MAJ[k % 4]
        put(music, pad([x + 12 for x in c], bar + 0.5, vel=1.0, a=0.1, r=0.6, cutoff=4500), t)
        put(music, timp(c[0] - 12, 1.2, 0.8), t)
        t += bar; k += 1


def sparkle(t0, n=14, spread=0.9, vel=0.7):
    scale = [86, 88, 90, 93, 95, 98, 100, 102]
    for i in range(n):
        put(music, musicbox(int(rng.choice(scale)), 0.9, vel=vel * rng.uniform(0.5, 1)), t0 + rng.uniform(0, spread), pan=rng.uniform(-0.7, 0.7))


def stinger(t, chord=(50, 57, 62, 66), vel=1.0):
    for m in chord:
        put(music, piano(m + 12, 2.5, 0.6 * vel), t)
    put(music, timp(38, 1.6, vel), t)


# cue the score from the story
T = lambda s, e="start": SHOT[s][e]
storybook(0.0, T("inspectors"))
drone(T("inspectors"), T("school_grey"))
for k in range(int((T("school_grey") - T("inspectors")) / (BEAT))):
    put(music, timp(38 if k % 2 == 0 else 33, 0.8, 0.35), T("inspectors") + k * BEAT * 1.0)
storybook(T("school_grey"), T("crack"), plk=False, vel=0.8)
put(music, pad([74, 81], T("wash") - T("crack") + 0.5, vel=0.6, a=0.5, r=0.4, cutoff=3000), T("crack"))
put(music, swell(T("wash") - T("rain_me")), T("rain_me"), gain=0.5)
# the reveal
storybook(T("wash"), T("stare"), theme=THEME_MAJ, chords=CHORDS_MAJ, roots=ROOTS_MAJ, plk=False, vel=1.0, bpm=104)
sparkle(t_of("wash", 1, -1, "end") - 0.2, n=24, spread=1.4, vel=0.9)
stinger(t_of("wash", 1, -1, "end"), vel=0.8)
# silence, then a comic plonk on the sandwich
put(music, pluck(38, 0.6, 1.2), t_of("stare", 2, edge="start") + 9 / 24)
put(music, pluck(33, 0.9, 1.2), t_of("stare", 2, edge="start") + 9 / 24 + 0.22)
pulse(T("sirens"), T("mom_secret"))
tender(T("mom_secret"), T("knock"))
ostinato(T("knock"), t_of("lever", 1, -1, "start") + 4 / 24)
stinger(t_of("lever", 1, -1, "start") + 10 / 24, chord=(50, 57, 62, 65), vel=1.0)
triumph(T("dome_open"), T("prism_grey"))
sparkle(T("color_town") + 2.0, n=30, spread=3.0, vel=0.8)
# comeuppance: playful pizzicato in D major
storybook(T("prism_grey"), DUR - 1.2, theme=THEME_MAJ, chords=CHORDS_MAJ, roots=ROOTS_MAJ, pd=False, vel=0.9, bpm=112)
stinger(DUR - 1.5, vel=0.9)

# ----------------------------------------------------------------------------- sound effects

def rain_bed(t0, t1, vel=1.0):
    d = t1 - t0
    n = np.stack([noise(d), noise(d)], 1)
    n = bp(n, 400, 9000) * 0.12
    drops = np.zeros_like(n)
    for k in range(int(d * 60)):
        i = int(rng.uniform(0, d - 0.05) * SR)
        g = tt(0.03)
        drops[i:i + len(g), k % 2] += np.sin(2 * np.pi * rng.uniform(1500, 4000) * g) * np.exp(-g * 200) * 0.15
    e = np.minimum(1, tt(d) / 0.8)[:, None] * np.minimum(1, (d - tt(d)) / 0.6)[:, None]
    put(sfx, (n + drops) * e * vel, t0)


def crack_sfx(t):
    g = tt(1.6)
    y = hp(noise(1.6), 2500) * np.exp(-g * 25) * 0.8
    for f in (2200, 3150, 4400, 5900):
        y += np.sin(2 * np.pi * f * g) * np.exp(-g * 3) * 0.08
    y += np.sin(2 * np.pi * 70 * g) * np.exp(-g * 12) * 0.5
    put(sfx, y, t)


def knock_sfx(t, n=3):
    for k in range(n):
        g = tt(0.25)
        y = np.sin(2 * np.pi * (140 - 60 * g) * g) * np.exp(-g * 30) + lp(noise(0.25), 1200) * np.exp(-g * 60) * 0.5
        put(sfx, y * 0.9, t + k * 0.26)


def siren_sfx(t0, t1, vel=0.2):
    g = tt(t1 - t0)
    f = np.where((g // 0.45) % 2 == 0, 740, 990)
    f = lp(f.astype(float), 30)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    e = np.minimum(1, g / 1.0) * np.minimum(1, (t1 - t0 - g) / 0.5)
    put(sfx, y * e * vel, t0, pan=-0.3)


def steps(t0, t1, every=0.5, vel=0.5):
    t = t0
    while t < t1:
        g = tt(0.15)
        put(sfx, lp(noise(0.15), 600) * np.exp(-g * 40) * vel + np.sin(2 * np.pi * 90 * g) * np.exp(-g * 35) * vel, t)
        t += every


def whoosh(t, d=0.45, vel=0.35):
    put(sfx, swell(d, 400, 3000, 1.0)[::-1] * vel, t - d * 0.6)


def lever_sfx(t):
    for k in range(5):
        put(sfx, tick(0.8, 2500), t - 0.3 + k * 0.06)
    g = tt(1.2)
    y = np.sin(2 * np.pi * 80 * g) * np.exp(-g * 14) + (np.sin(2 * np.pi * 620 * g) + np.sin(2 * np.pi * 1530 * g)) * np.exp(-g * 5) * 0.15
    put(sfx, y, t)


def rumble(t0, d, vel=0.8):
    n = lp(noise(d), 160, 4) * 3
    g = tt(d)
    put(sfx, n * np.minimum(1, g / 0.3) * np.exp(-g * 0.8) * vel, t0)


def pop(t):
    g = tt(0.12)
    put(sfx, np.sin(2 * np.pi * np.cumsum(500 + 2500 * g / 0.12) / SR) * np.exp(-g * 30) * 0.4, t)


def thud(t, vel=0.5):
    g = tt(0.2)
    put(sfx, (np.sin(2 * np.pi * 110 * g) * np.exp(-g * 30) + lp(noise(0.2), 800) * np.exp(-g * 50) * 0.4) * vel, t)


def door_creak(t):
    g = tt(0.7)
    f = 300 + 200 * np.sin(g * 9) + 80 * rng.standard_normal(len(g)).cumsum() / SR
    put(sfx, bp(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)), 300, 2500) * np.exp(-g * 2) * 0.12, t)


rain_bed(T("umbrella", "start") + 2.0, T("inspectors"), vel=0.35)          # rain on the glass, far away
crack_sfx(t_of("crack", 0, -1))
rain_bed(T("rain_me"), T("stare"), vel=0.8)
rain_bed(T("dome_open"), T("ending"), vel=1.1)
rumble(T("dome_open") + 0.3, 3.0)
siren_sfx(t_of("sirens", 0, 0, "start") + 0.2, T("mom_secret"))
steps(T("inspectors") + 0.04, T("school_grey"), every=0.5, vel=0.45)
steps(T("sirens"), T("mom_secret"), every=0.25, vel=0.25)
knock_sfx(t_of("knock", 0, -1, "start"))
door_creak(t_of("knock", 0, edge="end") + 0.05)
lever_sfx(t_of("lever", 1, -1, "start") + 10 / 24)
pop(t_of("yellow_drop", 0, -1, "start"))
thud(t_of("stare", 2, edge="start") + 9 / 24, 0.6)
for s in ("grey_people", "prism", "umbrella", "school_grey", "crack", "sirens", "knock", "escape", "dome_open", "color_town", "ending"):
    whoosh(T(s), vel=0.22)

# ----------------------------------------------------------------------------- mix

vo, vsr = sf.read(os.path.join(OUT, "vo.wav"), dtype="float32")
vo = resample_poly(vo, SR, vsr).astype(np.float64)
vo = vo / (np.max(np.abs(vo)) + 1e-9) * 0.85
vo2 = np.zeros(N); vo2[:len(vo)] = vo[:N]
# duck the music under the voice
env = np.sqrt(lfilter([1], [1, -0.9995], vo2 ** 2) * 0.0005)
env = lfilter([1], [1, -0.9995], env) * 0.0005 * 2000
duck = 1 - 0.55 * np.clip(env / (np.percentile(env, 90) + 1e-9), 0, 1)

music = reverb(music, wet=0.3)
music = music / (np.max(np.abs(music)) + 1e-9)
sfx = reverb(sfx, wet=0.15)
mix = music * 0.30 * duck[:, None] + sfx * 0.55 + vo2[:, None] * 1.0
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
L = int((DUR) * SR)
sf.write(os.path.join(OUT, "music.wav"), (music[:L] * 0.9).astype(np.float32), SR)
sf.write(os.path.join(OUT, "sfx.wav"), (sfx[:L] / (np.max(np.abs(sfx)) + 1e-9) * 0.9).astype(np.float32), SR)
sf.write(os.path.join(OUT, "mix.wav"), mix[:L].astype(np.float32), SR)
print("mix", round(L / SR, 2), "s; peak", round(float(np.max(np.abs(mix))), 3))
