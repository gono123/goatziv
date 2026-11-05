"""Transcribe reference videos with word timestamps -> ref/analysis/<id>.words.json + <id>.txt"""
import json, os, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
HERE = os.path.dirname(os.path.abspath(__file__))
m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=4)
for vid in sys.argv[1:]:
    src = os.path.join(HERE, "ref", "proxy", vid + ".wav")
    # decode with ffmpeg ourselves (faster-whisper's PyAV path breaks on this PyAV version)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, np.float32)
    segs, info = m.transcribe(audio, word_timestamps=True, vad_filter=False, beam_size=5)
    words, lines = [], []
    for s in segs:
        lines.append(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}")
        for w in s.words:
            words.append({"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)})
    json.dump(words, open(os.path.join(HERE, "ref", "analysis", vid + ".words.json"), "w"))
    open(os.path.join(HERE, "ref", "analysis", vid + ".txt"), "w").write("\n".join(lines))
    print(vid, len(words), "words", round(info.duration, 1), "s")
