"""v2 narration: clone the user's own ElevenLabs "roblox" voice with Chatterbox, then time every word.

    clone/bin/python voice.py            -> voice/lines/*.wav (cached), out/vo.wav
    python3 voice.py --align             -> out/timeline.json (needs faster-whisper; run after the first step)

Steps: generate each sentence -> trim -> time-stretch to ~4.3 words/s of speech (the reference pace) ->
join with short gaps -> faster-whisper word timestamps -> shot cuts on the [marker] words.
"""
import hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lines import SCRIPT, HOLD

OUT = os.path.join(HERE, "out")
LINES = os.path.join(HERE, "voice", "lines")
REF = os.path.join(HERE, "voice", "ref_roblox.wav")
SR = 24000
FPS = 24
TARGET_WPS = 4.3      # words per second of speech, before gaps
GAP = 0.12            # between sentences: the reference narration barely pauses
LEAD = 0.25
os.makedirs(LINES, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

MARK = re.compile(r"\[(\w+)\]")


def clean(line):
    return re.sub(r"\s+", " ", MARK.sub("", line)).strip()


def key(text):
    return hashlib.sha1(f"cb1|{text}".encode()).hexdigest()[:12]


def generate():
    import torch, torchaudio
    from chatterbox.tts import ChatterboxTTS
    m = ChatterboxTTS.from_pretrained(device="cpu")
    torch.manual_seed(7)
    for i, line in enumerate(SCRIPT):
        text = clean(line)
        raw = os.path.join(LINES, f"{key(text)}_raw.wav")
        fin = os.path.join(LINES, f"{key(text)}.wav")
        if not os.path.exists(raw):
            w = m.generate(text, audio_prompt_path=REF, exaggeration=0.6, cfg_weight=0.4)
            torchaudio.save(raw, w, m.sr)
        if not os.path.exists(fin):
            trim = fin + ".trim.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-ac", "1", "-ar", str(SR), "-af",
                            "silenceremove=start_periods=1:start_threshold=-42dB,areverse,silenceremove=start_periods=1:start_threshold=-42dB,areverse",
                            trim], check=True)
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", trim],
                                       capture_output=True, text=True).stdout)
            words = len(text.split())
            ratio = min(1.0, (words / TARGET_WPS) / dur)      # only ever speed up
            subprocess.run(["rubberband", "-q", "-3", "-t", f"{ratio:.4f}", trim, fin], check=True)
            os.remove(trim)
        print(i, text[:60], flush=True)
    # join
    import numpy as np, soundfile as sf
    parts = [np.zeros(int(LEAD * SR), np.float32)]
    for line in SCRIPT:
        a, sr = sf.read(os.path.join(LINES, f"{key(clean(line))}.wav"), dtype="float32")
        assert sr == SR, sr
        parts.append(a)
        hold = sum(v for k, v in HOLD.items() if k in line)
        parts.append(np.zeros(int((GAP + hold) * SR), np.float32))
    parts.append(np.zeros(int(1.0 * SR), np.float32))
    vo = np.concatenate(parts)
    vo = vo / (np.abs(vo).max() + 1e-9) * 0.9
    sf.write(os.path.join(OUT, "vo.wav"), vo, SR)
    print("vo.wav", round(len(vo) / SR, 1), "s")


def align():
    """Word times from faster-whisper, matched back to the script words, then shots from the markers."""
    import difflib
    import numpy as np
    from faster_whisper import WhisperModel
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(OUT, "vo.wav"), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, np.float32)
    total = len(audio) / 16000
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio, word_timestamps=True, beam_size=5, initial_prompt="grey Pip Prism Color Bank")
    heard = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower()).replace("gray", "grey")
    # script tokens, remembering which ones start a shot
    tokens, starts = [], {}
    for li, line in enumerate(SCRIPT):
        pending = None
        for tok in line.split():
            mk = MARK.fullmatch(tok)
            if mk:
                pending = mk.group(1)
                continue
            if pending:
                starts[len(tokens)] = pending
                pending = None
            tokens.append({"w": tok, "line": li})
    sm = difflib.SequenceMatcher(a=[norm(t["w"]) for t in tokens], b=[norm(h[0]) for h in heard], autojunk=False)
    for a0, b0, n in sm.get_matching_blocks():
        for k in range(n):
            tokens[a0 + k]["s"], tokens[a0 + k]["e"] = heard[b0 + k][1], heard[b0 + k][2]
    # fill unmatched words by interpolation
    known = [i for i, t in enumerate(tokens) if "s" in t]
    for i, t in enumerate(tokens):
        if "s" in t:
            continue
        prev = max([k for k in known if k < i], default=None)
        nxt = min([k for k in known if k > i], default=None)
        t0 = tokens[prev]["e"] if prev is not None else LEAD
        t1 = tokens[nxt]["s"] if nxt is not None else total - 1.0
        gaps = (nxt if nxt is not None else len(tokens)) - (prev if prev is not None else -1)
        pos = i - (prev if prev is not None else -1)
        t["s"] = t0 + (t1 - t0) * (pos - 0.5) / gaps
        t["e"] = t["s"] + 0.2
    matched = len(known) / len(tokens)
    # shots: each starts at its marker word (a few frames early, so the picture leads the word)
    idx = sorted(starts)
    shots = []
    for j, i in enumerate(idx):
        st = max(0.0, tokens[i]["s"] - 0.08) if j else 0.0
        shots.append({"id": starts[i], "start": round(st, 3), "first_word": i})
    for j, s in enumerate(shots):
        s["end"] = shots[j + 1]["start"] if j + 1 < len(shots) else round(total, 3)
        last = shots[j + 1]["first_word"] if j + 1 < len(shots) else len(tokens)
        s["words"] = [{"w": tokens[k]["w"], "s": round(tokens[k]["s"], 3), "e": round(tokens[k]["e"], 3)} for k in range(s["first_word"], last)]
        s["text"] = " ".join(w["w"] for w in s["words"])
    json.dump({"fps": FPS, "duration": round(total, 3), "shots": shots}, open(os.path.join(OUT, "timeline.json"), "w"), indent=1)
    lens = [s["end"] - s["start"] for s in shots]
    print(f"{len(shots)} shots, {len(tokens)} words, {total:.1f}s, {len(tokens) / total:.2f} w/s, "
          f"shot avg {sum(lens) / len(lens):.2f}s (min {min(lens):.2f}, max {max(lens):.2f}), words matched {matched:.0%}")


if __name__ == "__main__":
    align() if "--align" in sys.argv else generate()
