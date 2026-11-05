# Born Grey — Blender short

"In This World, Everyone Is Born Grey 🩷", a ~129 s vertical Short starring the channel's pink-suit hero,
built entirely from code with Blender (bpy), Kokoro TTS and a synthesized score.

| Step | Command | Output |
|---|---|---|
| Voiceover + timing | `KOKORO_DIR=<dir with kokoro-v1.0.onnx, voices-v1.0.bin> python voice.py` | `out/vo.wav`, `out/timeline.json` |
| Preview stills | `./preview_all.sh && python3 sheet.py` | `out/preview/`, `out/test/sheet_*.png` |
| Render | `BPY_PYTHON=<python with bpy 5.0> ./render_all.sh` | `out/frames/<shot>/####.png` |
| Music + SFX + mix | `python music.py` | `out/mix.wav` |
| Captions + video | `python finish.py` | `out/born_grey.mp4` (1080x1920, 24 fps) |

Files: `lines.py` (script, voices), `blib.py` (materials, characters, props, cameras),
`shots.py` (the 24 shots), `render.py` (one shot), `music.py`, `finish.py`.

Notes
- Headless Eevee needs EGL: `apt install libegl1 libegl-mesa0 libgbm1`; `run_blender.sh` sets software GL.
- bpy 5.0 needs numpy<2, kokoro-onnx needs numpy>=2: use two Python environments.
- The grey-paint effect: washable materials read the object property `wash_line` / scene property
  `town_line` (see `blib.py` docstring). Keyframe them to wash characters or the whole town.
- Transparent materials are ~10x slower in software Eevee; the dome is ribs only.
