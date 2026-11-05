"""Measure voice and music of the reference videos from the demucs stems.
   python ref_audio.py  -> ref/analysis/audio.json + printed summary"""
import json, os, glob
import numpy as np, librosa
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ref")
KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
def db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
def key_of(y, sr):
    c = librosa.feature.chroma_cqt(y=y, sr=sr).mean(1)
    best = max(((np.corrcoef(np.roll(p, k), c)[0, 1], KEYS[k] + m) for p, m in ((MAJ, " major"), (MIN, " minor")) for k in range(12)))
    return best[1]
out = {}
for d in sorted(glob.glob(f"{R}/stems/htdemucs/*")):
    vid = os.path.basename(d)
    v, sr = librosa.load(f"{d}/vocals.wav", sr=22050, mono=True)
    m, _ = librosa.load(f"{d}/no_vocals.wav", sr=22050, mono=True)
    f0, vf, _ = librosa.pyin(v[: sr * 60], fmin=70, fmax=500, sr=sr, frame_length=2048)
    f0 = f0[~np.isnan(f0)]
    tempo = float(np.atleast_1d(librosa.beat.beat_track(y=m, sr=sr)[0])[0])
    # music level over time (5 s windows) and transient "hits" (likely sound effects) in the non-vocal stem
    win = sr * 5
    levels = [round(db(m[i:i + win]), 1) for i in range(0, len(m) - win, win)]
    on = librosa.onset.onset_detect(y=m, sr=sr, units="time", backtrack=False, delta=0.25)
    oenv = librosa.onset.onset_strength(y=m, sr=sr)
    strong = librosa.onset.onset_detect(onset_envelope=oenv, sr=sr, units="time", delta=1.2)
    cuts = [float(x) for x in open(f"{R}/cuts/{vid}.txt").read().split()]
    near = sum(1 for c in cuts if any(abs(c - s) < 0.12 for s in strong))
    cent = float(np.mean(librosa.feature.spectral_centroid(y=m, sr=sr)))
    thirds = [round(db(m[int(len(m) * k / 3): int(len(m) * (k + 1) / 3)]), 1) for k in range(3)]
    out[vid] = dict(voice_db=round(db(v), 1), music_db=round(db(m), 1), music_under_voice_db=round(db(v) - db(m), 1),
                    f0_median=round(float(np.median(f0)), 1), f0_p10=round(float(np.percentile(f0, 10)), 1), f0_p90=round(float(np.percentile(f0, 90)), 1),
                    tempo=round(tempo, 1), key=key_of(m, sr), centroid_hz=round(cent), music_level_thirds=thirds,
                    hits=len(strong), hits_per_min=round(len(strong) / (len(m) / sr) * 60, 1), cuts_with_hit=f"{near}/{len(cuts)}",
                    levels_5s=levels)
    print(vid, {k: out[vid][k] for k in out[vid] if k != "levels_5s"})
json.dump(out, open(f"{R}/analysis/audio.json", "w"), indent=1)
