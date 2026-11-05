# Graph report: goatziv

Generated 2026-11-05 from `.` (146 nodes, 533 edges). Open `graph.html` to explore it; `graph.json` holds the raw graph.

## Summary

- **What the repo is:** the writing room and film studio of a "What If…?" YouTube channel. 2 finished episodes (`eyesight-100x/`, `zero-fear/`), each a self-contained film project where every frame is drawn in code and every sound is synthesised in code, plus title ideas, narration scripts and YouTube upload kits.
- **Shape:** 43 JS modules (7048 lines of shared engine, counted once), 55 scenes, 19 characters, 6 Markdown docs, 13 bundled fonts.
- **The engine is vendored, not shared.** `engine/` is copied into every episode, and the copies are byte-identical today. The graph collapses them into one set of `engine/*` nodes; each node lists its copies.
- **Modules talk through globals.** Browser files publish a namespace on `globalThis` (`U`, `G`, `Ch`, `UI`, `Data`, `Subs`, `Studio`, `SCORE`, `FL` …) and load in the order `index.html` lists them. Node-side files (`song.js`, `timing.js`, `engine/render.js`, `engine/audio/*`) use `require`. Several files (`util.js`, `music.js`, `score.js`, `lines.js`, `timeline.js`) run in both worlds.

## God nodes (most connected)

| Node | Degree | Why it matters |
|---|---:|---|
| `eyesight-100x/film.js` | 43 | all scenes of the episode, one function each |
| `zero-fear/film.js` | 42 | all scenes of the episode, one function each |
| `eyesight-100x/lines.js` | 33 | the narration, one entry per spoken line, grouped by scene |
| `zero-fear/lines.js` | 32 | the narration, one entry per spoken line, grouped by scene |
| `engine` | 31 | the vendored engine folder itself |
| `engine/render.js` | 28 | CLI entry point: drives headless Chrome, muxes, verifies, and dispatches to every `engine/tools/*` mode |
| `engine/video/boot.js` | 23 | the frame contract: `Studio.film()` on the film side, `window.renderAt()` on the renderer side; also loads the fonts |
| `eyesight-100x/film-lib.js` | 23 | the episode's cast, world and props |
| `zero-fear/film-lib.js` | 22 | the episode's cast, world and props |
| `engine/video/gfx.js` | 18 | hand-drawn drawing toolkit (`G`): almost every pixel passes through `G.ellipse`, `G.line`, `G.rrect`, `G.poly` |

## Heaviest call paths

Counted from member accesses on each imported namespace (for example `G.line(...)`).

| From | To | Calls |
|---|---|---:|
| `engine/video/chars.js` | `engine/video/gfx.js` | 530 |
| `eyesight-100x/film.js` | `eyesight-100x/film-lib.js` | 263 |
| `eyesight-100x/film.js` | `engine/video/gfx.js` | 214 |
| `zero-fear/film.js` | `zero-fear/film-lib.js` | 128 |
| `zero-fear/film.js` | `engine/video/gfx.js` | 117 |
| `zero-fear/film-lib.js` | `engine/video/gfx.js` | 83 |
| `engine/video/data.js` | `engine/video/gfx.js` | 66 |
| `eyesight-100x/film-lib.js` | `engine/video/gfx.js` | 55 |
| `engine/video/boot.js` | `engine/video/gfx.js` | 52 |
| `engine/video/gfx.js` | `engine/util.js` | 52 |

## Communities

- **scenes · eyesight-100x** (28): `23. saved`, `10. birds`, `3. hill`, `17. roof`, `8. class`, `11. fovea` …
- **scenes · zero-fear** (27): `2. haunted`, `3. coaster`, `9. space`, `12. bridge`, `22. truth`, `8. speech` …
- **engine · fonts** (13): `engine/fonts/Inter-400.ttf`, `engine/fonts/Inter-700.ttf`, `engine/fonts/Inter-800.ttf`, `engine/fonts/Bungee-Regular.ttf`, `engine/fonts/Caveat-Bold.ttf`, `engine/fonts/GochiHand-Regular.ttf` …
- **episode · eyesight-100x** (11): `eyesight-100x/film.js`, `eyesight-100x/lines.js`, `eyesight-100x/film-lib.js`, `eyesight-100x/score.js`, `eyesight-100x/index.html`, `proj:eyesight-100x` …
- **episode · zero-fear** (11): `zero-fear/film.js`, `zero-fear/lines.js`, `zero-fear/film-lib.js`, `zero-fear/score.js`, `zero-fear/index.html`, `proj:zero-fear` …
- **engine · render + tools** (11): `engine/render.js`, `engine/tools/plan.js`, `engine/tools/levels.js`, `engine/tools/qa.js`, `engine/tools/srt.js`, `engine/tools/analyze.js` …
- **cast · eyesight-100x** (10): `theo`, `grandpa`, `friend`, `tourist`, `black`, `boy` …
- **engine · picture** (9): `engine/video/boot.js`, `engine/video/gfx.js`, `engine/subs.js`, `engine/video/chars.js`, `engine/video/data.js`, `engine/video/ui.js` …
- **cast · zero-fear** (9): `sam`, `leo`, `black`, `kid1`, `kid2`, `kid3` …
- **engine · audio** (7): `engine/audio/dsp.js`, `engine/audio/instruments.js`, `engine/audio/voice.js`, `engine/audio/genres.js`, `engine/audio/mix.js`, `engine/audio/sing.js` …
- **writing room** (6): `titles/batch-01.md`, `scripts/what-if-you-had-zero-fear.md`, `scripts/what-if-your-eyesight-was-100x-sharper.md`, `youtube/what-if-you-had-zero-fear.md`, `youtube/what-if-your-eyesight-was-100x-sharper.md`, `README.md`
- **engine · core** (3): `engine`, `engine/util.js`, `engine/music.js`
- **channel** (1): `repo`

## How a film gets made (the pipeline the edges describe)

1. `titles/batch-01.md` pitches the episode → `scripts/<slug>.md` holds the narration.
2. `lines.js` splits the script into spoken lines per scene (speaker prefixes `S:`, `M:`, `L:` …).
3. `timing.js` voices every line through `engine/audio/voice.js`, measures it and **generates** `timeline.js`.
4. `score.js` reads `timeline.js` + `lines.js` and places scenes, events and music sections: the single source of timing.
5. `song.js` renders the soundtrack from the score with `engine/audio/{dsp,instruments,genres,mix,voice}`.
6. `index.html` loads engine + episode scripts in order; `film.js` draws each scene with `G`, `Ch`, `UI`, `Data`, `Subs` and `film-lib.js`.
7. `engine/render.js` renders frames in headless Chrome, muxes with the music, then `check`/`verify`; tools add posters, captions (`srt`), QA, pacing and format variants.
8. `youtube/<slug>.md` is the upload kit for the finished `out/<name>.mp4` (not committed).

## Episodes side by side

| | `eyesight-100x` | `zero-fear` |
|---|---:|---:|
| Title | What If Your Eyesight Was 100x Sharper? | What If You Had Zero Fear? |
| Scenes | 28 | 27 |
| Characters | 10 | 9 |
| Spoken lines | 205 | 219 |
| film.js lines | 671 | 478 |
| film-lib.js lines | 137 | 182 |
| Busiest character (scenes) | theo (17) | sam (16) |

## Surprising connections and gaps

- **Engine code no episode runs:** `engine/audio/analyze.js` (266 lines), `engine/audio/sing.js` (180 lines), `engine/tools/analyze.js` (42 lines). They are reached only by commands these films do not use (`render.js analyze`, sung lines).
- **Loaded but never called:** `engine/video/shots.js` is in both `index.html` files, yet neither film calls `Shots.*`: each `film.js` dispatches scenes through its own `SCENES` table and `score.sceneAt(t)`.
- **`package.json` name drift:** `eyesight-100x/package.json` is still named `my-film` (template default) while `zero-fear` was renamed.
- **Generated file in the graph:** `timing.js` → `timeline.js` ("do not edit"). Edit `lines.js` and rerun `node timing.js`; editing `timeline.js` by hand is overwritten.
- **Cross-episode edges:** none. Episodes never reference each other; everything shared lives in the vendored engine. A fix to `engine/` has to be copied into every episode by hand.
- **Scripts are one line each:** `scripts/*.md` hold the whole narration as a single paragraph; `lines.js` is the structured copy, and the two can drift apart.
- **Backlog:** 35 titles pitched in `titles/batch-01.md`, 2 produced (#2 and #7).

## Confidence

503 edges are **EXTRACTED** (read straight from code: `require`, `globalThis` reads, `<script>` tags, `npm` scripts, scene tables, speaker prefixes). 30 are **INFERRED** (doc ↔ episode matched by title slug, fonts matched by family name).

## Questions this graph can answer

- Which engine modules would a change to `G.line` ripple into? (follow `uses global` edges into `engine/video/gfx.js`)
- Which scenes does a character appear in, and where do they speak? (`shows` vs `speaks in`)
- What do I have to touch to start episode #3? (copy a project folder; edit `lines.js`, `score.js`, `film-lib.js`, `film.js`; rerun `timing.js`)
- Is the engine still identical across episodes? (rerun the builder; `engineIdentical` in `graph.json`)
