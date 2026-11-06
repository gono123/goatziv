#!/bin/sh
# Render every v2 shot (720x1280, 4 samples) in two queues balanced by frame count. Re-runnable: skips done frames.
cd "$(dirname "$0")"
python3 - <<'P' > out/queues.txt
import json
sh = json.load(open("out/timeline.json"))["shots"]
n = {s["id"]: round(s["end"] * 24) - round(s["start"] * 24) for s in sh}
q = [[], []]; tot = [0, 0]
for sid in sorted(n, key=lambda k: -(n[k] + 300)):     # +300: per-shot setup cost
    i = tot.index(min(tot)); q[i].append(sid); tot[i] += n[sid] + 300
for x in q: print(" ".join(x))
P
run_queue() {
  for s in $1; do LP_NUM_THREADS=2 ../run_blender.sh render2.py $s --samples ${SAMPLES:-4} | grep -E "^SHOT|Error|rror:" ; done
}
run_queue "$(sed -n 1p out/queues.txt)" > out/render_q1.log 2>&1 &
run_queue "$(sed -n 2p out/queues.txt)" > out/render_q2.log 2>&1 &
wait
echo ALL DONE
