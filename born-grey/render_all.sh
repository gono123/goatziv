#!/bin/sh
# Render every shot (720x1280, 4 samples) in two parallel queues balanced by frame count.
# Already-rendered frames are skipped, so this can be re-run after an interruption.
cd "$(dirname "$0")"
python3 - <<'P' > out/queues.txt
import json
sh = json.load(open("out/timeline.json"))["shots"]
n = {s["id"]: round(s["end"] * 24) - round(s["start"] * 24) for s in sh}
q = [[], []]; tot = [0, 0]
for sid in sorted(n, key=lambda k: -n[k]):
    i = tot.index(min(tot)); q[i].append(sid); tot[i] += n[sid]
for x in q: print(" ".join(x))
P
run_queue() {
  for s in $1; do LP_NUM_THREADS=2 ./run_blender.sh render.py $s --samples ${SAMPLES:-4} | grep -E "SHOT|rror" ; done
}
run_queue "$(sed -n 1p out/queues.txt)" > out/render_q1.log 2>&1 &
run_queue "$(sed -n 2p out/queues.txt)" > out/render_q2.log 2>&1 &
wait
echo ALL DONE
