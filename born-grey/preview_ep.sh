#!/bin/sh
export BPY_PYTHON=${BPY_PYTHON:-/tmp/claude-0/-home-user-goatziv/0b705d1b-0c52-50d1-bff7-7e58e46be9b9/scratchpad/prod/venv/bin/python}
# Preview one frame (2/3 through) of every shot of an episode, 2 at a time.  sh preview_ep.sh <ep> [shot ...]
cd "$(dirname "$0")/$1"; shift
mkdir -p out/preview; : > out/preview_errors.log
ids="$*"; [ -z "$ids" ] && ids=$(python3 -c "import json;print(' '.join(x['id'] for x in json.load(open('out/timeline.json'))['shots']))")
for s in $ids; do echo $s; done | xargs -P 2 -I{} sh -c '
  n=$(python3 -c "import json;d=[x for x in json.load(open(\"out/timeline.json\"))[\"shots\"] if x[\"id\"]==\"{}\"][0];print(round(d[\"end\"]*24)-round(d[\"start\"]*24))")
  ../run_blender.sh render2.py {} --res 270x480 --samples 2 --frames $((2*n/3+1)) > out/pv_{}.log 2>&1
  grep -q "^SHOT" out/pv_{}.log && echo "ok {}" || { echo "FAIL {}"; { echo "== {}"; grep -E "Error|line [0-9]+" out/pv_{}.log | tail -4; } >> out/preview_errors.log; }'
