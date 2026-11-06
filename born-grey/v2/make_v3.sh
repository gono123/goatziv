#!/bin/sh
# Full v3 build: render (with mocap) -> captions/SFX/bed -> Cry versions. Re-runnable (skips rendered frames).
cd "$(dirname "$0")"
P=/tmp/claude-0/-home-user-goatziv/0b705d1b-0c52-50d1-bff7-7e58e46be9b9/scratchpad/prod
BPY_PYTHON=$P/venv/bin/python ./render_all2.sh || exit 1
python3 - <<'P' || exit 1
import json, os
tl = json.load(open("out/timeline.json"))
miss = [s["id"] for s in tl["shots"] if len(os.listdir(f"out/frames/{s['id']}") if os.path.isdir(f"out/frames/{s['id']}") else []) < round(s["end"]*24) - round(s["start"]*24)]
print("incomplete:", miss); raise SystemExit(1 if miss else 0)
P
$P/tts/bin/python finish2.py | tail -3
$P/tts/bin/python add_song.py ../music/stems/htdemucs/cry/no_vocals.wav cry_instrumental | tail -1
$P/tts/bin/python add_song.py ../music/cry.wav cry_full --db 10 | tail -1
for v in preview upload cry_instrumental cry_full; do cp out/born_grey_v2_$v.mp4 out/born_grey_v3_$v.mp4; done
echo V3 DONE
