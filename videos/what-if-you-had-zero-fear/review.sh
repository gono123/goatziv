#!/bin/sh
# review.sh <name> <t...>: render stills at the given times and tile them into out/<name>.png
set -e
cd "$(dirname "$0")"
name=$1; shift
mkdir -p out/old
[ -d out/stills ] && mv out/stills "out/old/stills-$(date +%s)"
node engine/render.js stills "$@" 2>&1 | grep -vi warn | tail -1
ffmpeg -y -loglevel error -pattern_type glob -i 'out/stills/t_*.png' -vf "scale=960:540,tile=3x4:color=black" -frames:v 1 "out/$name.png"
