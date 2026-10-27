# What If You Had Zero Fear? (animated)

A 16:9 2D animated short of `scripts/what-if-you-had-zero-fear.md`, made with the animation-studio
plugin: every frame is drawn on a canvas in code and the score is synthesized in code. The narrator
is a deep male storyteller voice (Kokoro TTS, `am_onyx` blended with `am_michael`, played back at
0.93x for depth).

| file | what it is |
| --- | --- |
| `lines.js` | the narration, split into 32 scenes |
| `make-timing.js` → `timing.js` | measures each spoken line so the film is timed to the real voice |
| `score.js` | the timeline: scene and line times, the hits, the music's moods |
| `song.js` | the voiceover and the score → `out/music.wav` |
| `kit.js`, `film.js` | the cast, the props and the 32 scenes |
| `tts/kokoro.py` | adapter so the engine can use `kokoro-onnx` |
| `engine/` | the plugin's vendored engine (not edited) |

## Rebuild

Needs Node 22+, ffmpeg, Chrome/Chromium (`CHROME_PATH`; add `--no-sandbox` when running as root),
`pip install kokoro-onnx soundfile`, and the Kokoro v1.0 ONNX files (`kokoro-v1.0.onnx`,
`voices-v1.0.bin` from the kokoro-onnx GitHub releases) in `tts/models/`.

```bash
node make-timing.js            # synthesize + measure every line (cached in out/.vo-cache)
node song.js                   # voice + music -> out/music.wav
node engine/render.js video    # frames -> out/video.mp4
node engine/render.js mux      # -> out/what-if-you-had-zero-fear.mp4
./review.sh sheet 12.5 @crack  # stills at given times, tiled into out/sheet.png
```
