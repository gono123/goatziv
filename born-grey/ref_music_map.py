"""Where does the music change in each reference video, and which song is playing?

Slides 6 s windows of each video's music stem (voice removed) against the songs we own (music/*.wav),
on chroma (harmony) features, allowing any time offset. A window that matches nothing is another song.
    sep/bin/python ref_music_map.py -> ref/analysis/music_map.json + printed timeline
"""
import glob, json, os
import numpy as np, librosa
R = os.path.dirname(os.path.abspath(__file__))
SR, HOP = 11025, 512           # ~46 ms per chroma frame
def chroma(path):
    y, _ = librosa.load(path, sr=SR, mono=True)
    c = librosa.feature.chroma_cqt(y=y, sr=SR, hop_length=HOP)
    c = c / (np.linalg.norm(c, axis=0) + 1e-9)
    rms = librosa.feature.rms(y=y, hop_length=HOP)[0]
    return c, rms
songs = {}
for p in sorted(glob.glob(f"{R}/music/*.wav")):
    songs[os.path.basename(p)[:-4]] = chroma(p)[0]
fps = SR / HOP
W = int(6 * fps); STEP = int(2 * fps)
out = {}
for d in sorted(glob.glob(f"{R}/ref/stems/htdemucs/*")):
    vid = os.path.basename(d)
    if vid in songs: continue
    c, rms = chroma(f"{d}/no_vocals.wav")
    rows = []
    for s in range(0, c.shape[1] - W, STEP):
        A = c[:, s:s + W]
        best = ("?", 0.0, 0.0)
        for name, S in songs.items():
            # correlate the window against every offset of the song (all 12 transpositions too)
            for tr in (0,):
                At = np.roll(A, tr, axis=0)
                sim = np.array([np.mean(np.sum(At * S[:, k:k + W], 0)) for k in range(0, S.shape[1] - W, 4)])
                k = int(sim.argmax())
                if sim[k] > best[1]:
                    best = (name, float(sim[k]), k * 4 / fps)
        level = float(20 * np.log10(np.mean(rms[s:s + W]) + 1e-9))
        rows.append({"t": round(s / fps, 1), "song": best[0] if best[1] > 0.83 else "OTHER", "sim": round(best[1], 3), "song_t": round(best[2], 1), "db": round(level, 1)})
    out[vid] = rows
    # print compact runs
    runs = []
    for r in rows:
        if runs and runs[-1][0] == r["song"]:
            runs[-1][2] = r["t"] + 6
        else:
            runs.append([r["song"], r["t"], r["t"] + 6, r["song_t"]])
    print(vid, " | ".join(f"{a}:{b:.0f}-{c:.0f}s" + (f"(@{e:.0f}s)" if a != "OTHER" else "") for a, b, c, e in runs))
json.dump(out, open(f"{R}/ref/analysis/music_map.json", "w"), indent=1)
