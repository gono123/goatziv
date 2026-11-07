#!/bin/sh
# Cloud fallback: render every shot of <ep> (720x1280, 4 samples) in two queues. Re-runnable: skips done frames.
export BPY_PYTHON=${BPY_PYTHON:-/tmp/claude-0/-home-user-goatziv/0b705d1b-0c52-50d1-bff7-7e58e46be9b9/scratchpad/prod/venv/bin/python}
cd "$(dirname "$0")/$1"
python3 - <<'P' > out/queues.txt
import json
sh = json.load(open("out/timeline.json"))["shots"]
n = {s["id"]: round(s["end"] * 24) - round(s["start"] * 24) for s in sh}
q = [[], []]; tot = [0, 0]
for sid in sorted(n, key=lambda k: -(n[k] + 300)):
    i = tot.index(min(tot)); q[i].append(sid); tot[i] += n[sid] + 300
for x in q: print(" ".join(x))
P
run_queue() {
  for s in $1; do LP_NUM_THREADS=2 ../run_blender.sh render2.py $s --samples ${SAMPLES:-4} | grep -E "^SHOT|Error|rror:" ; done
}
run_queue "$(sed -n 1p out/queues.txt)" > out/render_q1.log 2>&1 &
run_queue "$(sed -n 2p out/queues.txt)" > out/render_q2.log 2>&1 &
wait
echo ALL DONE $1
