"""Voiceover: Kokoro TTS per line -> out/vo/<n>.wav, out/vo.wav and out/timeline.json.

timeline.json holds every shot's start/end (seconds), each line's timing, caption chunks
(2-4 words each, snapped to the pauses in the real audio) and a 24 fps mouth envelope.

    KOKORO_DIR=/path/with/kokoro-v1.0.onnx+voices-v1.0.bin  python voice.py
"""
import json, os, re, sys, hashlib
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lines import SHOTS, VOICES

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
VO = os.path.join(OUT, "vo")
os.makedirs(VO, exist_ok=True)
KDIR = os.environ.get("KOKORO_DIR", os.path.join(HERE, "models"))
SR = 24000
FPS = 24
GAP_LINE = 0.28      # pause between lines in a shot
GAP_SPEAKER = 0.42   # pause when the speaker changes
GAP_SHOT = 0.45      # pause between shots
LEAD_IN = 0.35       # silence before the first word

kokoro = Kokoro(os.path.join(KDIR, "kokoro-v1.0.onnx"), os.path.join(KDIR, "voices-v1.0.bin"))


def synth(speaker, text):
    v = VOICES[speaker]
    key = hashlib.sha1(f"{v['voice']}|{v['speed']}|{text}".encode()).hexdigest()[:16]
    path = os.path.join(VO, f"{key}.wav")
    if not os.path.exists(path):
        audio, sr = kokoro.create(text, voice=v["voice"], speed=v["speed"], lang="en-us")
        assert sr == SR
        audio = np.asarray(audio, dtype=np.float32)
        # trim leading/trailing silence so our own gaps control the pacing
        env = np.abs(audio) > 0.01
        idx = np.flatnonzero(env)
        if len(idx):
            a, b = max(0, idx[0] - int(0.02 * SR)), min(len(audio), idx[-1] + int(0.06 * SR))
            audio = audio[a:b]
        sf.write(path, audio, SR)
    audio, _ = sf.read(path, dtype="float32")
    return path, audio


def pauses(audio, min_len=0.07):
    """Silent stretches inside a line: list of (start, end) seconds."""
    hop = int(0.01 * SR)
    rms = np.sqrt(np.convolve(audio ** 2, np.ones(hop) / hop, mode="same"))[::hop]
    quiet = rms < 0.012
    out, s = [], None
    for i, q in enumerate(quiet):
        if q and s is None:
            s = i
        if not q and s is not None:
            if (i - s) * 0.01 >= min_len:
                out.append((s * 0.01, i * 0.01))
            s = None
    return out


def chunks_for(text, audio):
    """Split a line into caption chunks and time them against the audio."""
    words = text.split()
    # build chunks: break after punctuation, or every 3 words (4 if the last one is tiny)
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r"[.,?!;:]$", w) or len(cur) >= 3:
            chunks.append(cur)
            cur = []
    if cur:
        if chunks and len(cur) == 1 and len(chunks[-1]) < 4 and not re.search(r"[.?!]$", chunks[-1][-1]):
            chunks[-1] += cur
        else:
            chunks.append(cur)
    dur = len(audio) / SR
    weight = lambda c: sum(len(w) + 2 for w in c) + (6 if re.search(r"[.,?!]$", c[-1]) else 0)
    total = sum(weight(c) for c in chunks)
    gaps = pauses(audio)
    t, out = 0.0, []
    for i, c in enumerate(chunks):
        end = t + dur * weight(c) / total
        left = len(chunks) - 1 - i
        if left == 0:
            end = dur
        elif gaps:
            # snap the boundary to the middle of the nearest pause, if one is close
            mids = [(a + b) / 2 for a, b in gaps]
            m = min(mids, key=lambda x: abs(x - end))
            if abs(m - end) < 0.35 and t + 0.15 < m < dur - 0.2 * left:
                end = m
        out.append({"text": " ".join(c), "start": round(t, 3), "end": round(end, 3)})
        t = end
    return out


def mouth(audio):
    hop = SR // FPS
    n = int(np.ceil(len(audio) / hop))
    env = [float(np.sqrt(np.mean(audio[i * hop:(i + 1) * hop] ** 2))) for i in range(n)]
    peak = max(env) or 1
    return [round(min(1.0, e / peak * 1.4), 3) for e in env]


def main():
    t = LEAD_IN
    shots, pieces = [], [np.zeros(int(LEAD_IN * SR), np.float32)]
    prev_speaker = None
    for si, (sid, lines, *opt) in enumerate(SHOTS):
        hold = (opt[0] if opt else {}).get("hold", 0.0)
        if si:
            gap = GAP_SHOT
            pieces.append(np.zeros(int(gap * SR), np.float32))
            t += gap
        start = t
        out_lines = []
        for li, (spk, text) in enumerate(lines):
            if li:
                gap = GAP_SPEAKER if spk != prev_speaker else GAP_LINE
                pieces.append(np.zeros(int(gap * SR), np.float32))
                t += gap
            path, audio = synth(spk, text)
            d = len(audio) / SR
            cks = chunks_for(text, audio)
            for c in cks:
                c["start"] = round(c["start"] + t, 3)
                c["end"] = round(c["end"] + t, 3)
            out_lines.append({"speaker": spk, "text": text, "start": round(t, 3), "end": round(t + d, 3),
                              "wav": os.path.relpath(path, HERE), "chunks": cks, "mouth": mouth(audio)})
            pieces.append(audio)
            t += d
            prev_speaker = spk
        if hold:
            pieces.append(np.zeros(int(hold * SR), np.float32))
            t += hold
        shots.append({"id": sid, "start": round(start, 3), "lines": out_lines})
    # each shot lasts until the next one starts; the last gets a tail for the ending beat
    for i, s in enumerate(shots):
        s["end"] = shots[i + 1]["start"] if i + 1 < len(shots) else round(t + 1.6, 3)
    total = shots[-1]["end"]
    pieces.append(np.zeros(int((total - t) * SR) + 1, np.float32))
    vo = np.concatenate(pieces)
    sf.write(os.path.join(OUT, "vo.wav"), vo, SR)
    json.dump({"fps": FPS, "duration": total, "shots": shots}, open(os.path.join(OUT, "timeline.json"), "w"), indent=1)
    words = sum(len(l[1].split()) for _, ls, *o in SHOTS for l in ls)
    print(f"{len(shots)} shots, {words} words, {total:.1f}s ({words / total:.2f} words/s)")
    for s in shots:
        print(f"  {s['id']:<12} {s['start']:6.2f} -> {s['end']:6.2f}  ({s['end'] - s['start']:.1f}s)")


if __name__ == "__main__":
    main()
