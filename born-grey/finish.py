"""Captions + final video.

    python finish.py            -> out/captions.ass, out/born_grey.mp4 (1080x1920, 24 fps)
    python finish.py --captions -> only the captions file

Captions: 2-4 words at a time, uppercase, white with a thick black outline, popping in. Colour
words are painted in their colour (GREY, PINK, YELLOW...), COLOR and PRISM in rainbow letters.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
TL = json.load(open(os.path.join(OUT, "timeline.json")))
FPS = TL["fps"]

RAINBOW = ["FF2D55", "FF9500", "FFE600", "34C759", "00C7FF", "5856D6", "FF2DC8"]
WORD_COLORS = {
    "grey": "BDBDBD", "greyest": "BDBDBD", "pink": "FF5FB8", "bubblegum": "FF5FB8", "yellow": "FFE600",
    "red": "FF4A4A", "green": "3DDC6A", "white": "FFFFFF", "gold": "FFD700",
}
RAINBOW_WORDS = {"color", "colors", "colorful", "prism", "prism?", "rainbow"}
BIG_WORDS = {"crack", "pink", "dude", "opened"}


def ass_color(hexrgb):
    r, g, b = hexrgb[0:2], hexrgb[2:4], hexrgb[4:6]
    return f"&H00{b}{g}{r}&"


def styled(word):
    up = word.upper()
    key = re.sub(r"[^a-z?]", "", word.lower())
    bare = key.rstrip("?")
    if bare in RAINBOW_WORDS or key in RAINBOW_WORDS:
        letters = []
        k = 0
        for ch in up:
            if ch.isalpha():
                letters.append(r"{\c" + ass_color(RAINBOW[k % len(RAINBOW)]) + "}" + ch)
                k += 1
            else:
                letters.append(ch)
        return "".join(letters) + r"{\c&H00FFFFFF&}"
    out = up
    if bare in WORD_COLORS:
        out = r"{\c" + ass_color(WORD_COLORS[bare]) + "}" + up + r"{\c&H00FFFFFF&}"
    if bare in BIG_WORDS:
        out = r"{\fscx118\fscy118}" + out + r"{\fscx100\fscy100}"
    return out


def ts(t):
    t = max(0.0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def captions():
    events = []
    lines = [l for s in TL["shots"] for l in s["lines"]]
    for i, L in enumerate(lines):
        nxt = lines[i + 1]["start"] if i + 1 < len(lines) else L["end"] + 1.0
        ch = L["chunks"]
        for j, c in enumerate(ch):
            start = c["start"]
            end = ch[j + 1]["start"] if j + 1 < len(ch) else min(nxt, L["end"] + 0.6)
            txt = " ".join(styled(w) for w in c["text"].split())
            pop = r"{\fscx80\fscy80\t(0,90,\fscx100\fscy100)}"
            events.append((start, end, pop + txt))
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter ExtraBold,112,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,1,0,1,9,5,2,70,70,640,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    body = "".join(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{t}\n" for a, b, t in events)
    path = os.path.join(OUT, "captions.ass")
    open(path, "w").write(head + body)
    print(f"{len(events)} captions -> {path}")
    return path


def frame_sequence():
    """Symlink every shot's frames into one numbered sequence; pad missing frames with the last one."""
    seq = os.path.join(OUT, "seq")
    os.makedirs(seq, exist_ok=True)
    for f in os.listdir(seq):
        os.remove(os.path.join(seq, f))
    k = 0
    missing = {}
    for s in TL["shots"]:
        n = round(s["end"] * FPS) - round(s["start"] * FPS)
        d = os.path.join(OUT, "frames", s["id"])
        last = None
        for i in range(1, n + 1):
            p = os.path.join(d, f"{i:04d}.png")
            if os.path.exists(p):
                last = p
            else:
                missing[s["id"]] = missing.get(s["id"], 0) + 1
            src = p if os.path.exists(p) else last
            if src is None:
                raise SystemExit(f"shot {s['id']} has no frames rendered yet")
            k += 1
            os.symlink(src, os.path.join(seq, f"{k:06d}.png"))
    if missing:
        print("WARNING: padded missing frames:", missing)
    return seq, k


def video(cap):
    seq, n = frame_sequence()
    out = os.path.join(OUT, "born_grey.mp4")
    vf = f"scale=1080:1920:flags=lanczos,ass={cap}"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(seq, "%06d.png"),
           "-i", os.path.join(OUT, "mix.wav"), "-vf", vf, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(f"{n} frames ({n / FPS:.1f}s) -> {out}")


if __name__ == "__main__":
    cap = captions()
    if "--captions" not in sys.argv:
        video(cap)
