#!/bin/sh
# Low-res preview of two frames (1/3 and 2/3 through) of every shot, then a contact sheet.
cd "$(dirname "$0")"
for s in $(python3 -c "import json;print(' '.join(x['id'] for x in json.load(open('out/timeline.json'))['shots']))"); do
  n=$(python3 -c "import json;d=[x for x in json.load(open('out/timeline.json'))['shots'] if x['id']=='$s'][0];print(round(d['end']*24)-round(d['start']*24))")
  ./run_blender.sh render.py $s --res 360x640 --samples 4 --frames $((n/3+1)),$((2*n/3+1)) | grep SHOT
done
