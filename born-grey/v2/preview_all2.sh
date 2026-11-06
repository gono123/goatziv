#!/bin/sh
# One low-res preview frame (2/3 through) of every v2 shot -> out/preview/, errors -> out/preview_errors.log
cd "$(dirname "$0")"
: > out/preview_errors.log
for s in $(python3 -c "import json;print(' '.join(x['id'] for x in json.load(open('out/timeline.json'))['shots']))"); do
  n=$(python3 -c "import json;d=[x for x in json.load(open('out/timeline.json'))['shots'] if x['id']=='$s'][0];print(round(d['end']*24)-round(d['start']*24))")
  ../run_blender.sh render2.py $s --res 360x640 --samples 3 --frames $((2*n/3+1)) > out/pv_$s.log 2>&1
  grep -q "^SHOT" out/pv_$s.log && echo "ok $s" || { echo "FAIL $s"; echo "== $s" >> out/preview_errors.log; grep -E "Error|line [0-9]+" out/pv_$s.log | tail -4 >> out/preview_errors.log; }
done
