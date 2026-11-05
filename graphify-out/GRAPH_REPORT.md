# Graph Report - goatziv  (2026-11-05)

## Corpus Check
- 82 files · ~181,821 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 3)

## Summary
- 1053 nodes · 2042 edges · 65 communities (33 shown, 32 thin omitted)
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 492 edges (avg confidence: 0.85)
- Token cost: 166,997 input · 0 output

## Community Hubs (Navigation)
- Eyesight: Synth Instruments & DSP
- Zero Fear: Synth Instruments & DSP
- Eyesight: Frame Renderer
- Eyesight: Drawing Primitives
- Zero Fear: Drawing Primitives
- Zero Fear Episode Story & Science
- Zero Fear: Film Scenes
- Eyesight: Film Scenes
- Eyesight Episode Story & Science
- Zero Fear: Renderer Config
- Eyesight: UI Widgets
- Zero Fear: UI Widgets
- Zero Fear: Audio Mix Bus
- Eyesight: Voice Synthesis
- Zero Fear: Voice Synthesis
- Eyesight: Character Drawings
- Eyesight: Soundtrack Song
- Zero Fear: Character Drawings
- Zero Fear: Soundtrack Song
- Eyesight: Audio Analysis
- Zero Fear: Audio Analysis
- Eyesight: npm Scripts
- Zero Fear: npm Scripts
- Eyesight: Mastering & Loudness
- Eyesight: Dialogue Timing
- Zero Fear: Render Pipeline
- Zero Fear: Dialogue Timing
- Audio Levels Tool (both)
- Eyesight: Camera Shots
- Zero Fear: Camera Shots
- Eyesight: Studio Boot & Assets
- Eyesight: Data Graphics
- Zero Fear: Studio Boot & Assets
- Zero Fear: Data Graphics
- Eyesight: Audio Mix Bus
- Eyesight: Preview Player
- Zero Fear: Preview Player
- Eyesight: Subtitles
- Zero Fear: Subtitles
- Zero Fear: Headless Chrome Control
- Eyesight: Music Genres
- Eyesight: Brand Colors
- Zero Fear: Music Genres
- Zero Fear: Brand Colors
- Sea & Map Scenes
- Eyesight: Cliff Sunset Scenes
- Zero Fear: Render Verification
- Eyesight: Grandpa Beach Scene

## God Nodes (most connected - your core abstractions)
1. `buf()` - 51 edges
2. `buf()` - 51 edges
3. `G` - 43 edges
4. `G` - 43 edges
5. `rng()` - 42 edges
6. `rng()` - 42 edges
7. `SVF` - 40 edges
8. `SVF` - 40 edges
9. `OnePole` - 31 edges
10. `OnePole` - 31 edges

## Surprising Connections (you probably didn't know these)
- `Chapters (21 timestamps, 0:00-6:51)` --semantically_similar_to--> `What If You Had Zero Fear? narration script`  [INFERRED] [semantically similar]
  youtube/what-if-you-had-zero-fear.md → scripts/what-if-you-had-zero-fear.md
- `titles/ directory (batches of video title ideas)` --references--> `Title ideas batch 01 (35 What If titles)`  [INFERRED]
  README.md → titles/batch-01.md
- `scripts/ directory (narration scripts, one per episode)` --references--> `What If You Had Zero Fear? narration script`  [INFERRED]
  README.md → scripts/what-if-you-had-zero-fear.md
- `What If You Had Zero Fear? narration script` --implements--> `What If You Had Zero Fear? (title #7)`  [INFERRED]
  scripts/what-if-you-had-zero-fear.md → titles/batch-01.md
- `Shared animation engine (util, music, gfx, chars, ui, shots, subs, geo, data, boot)` --conceptually_related_to--> `zero-fear.srt (English captions)`  [AMBIGUOUS]
  zero-fear/index.html → youtube/what-if-you-had-zero-fear.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Zero Fear episode production pipeline (title -> script -> film -> upload)** — titles_batch_01_what_if_you_had_zero_fear, scripts_what_if_you_had_zero_fear_script, zero_fear_index_film_page, youtube_what_if_you_had_zero_fear_upload_package [INFERRED 0.85]
- **Real science facts underpinning the Zero Fear story** — scripts_what_if_you_had_zero_fear_amygdala, scripts_what_if_you_had_zero_fear_patient_sm, scripts_what_if_you_had_zero_fear_fear_face_recognition, scripts_what_if_you_had_zero_fear_personal_space, scripts_what_if_you_had_zero_fear_bone_healing_six_weeks, scripts_what_if_you_had_zero_fear_three_points_of_contact [EXTRACTED 1.00]
- **Fear-blindness arc: can't read faces -> think it -> two taps** — scripts_what_if_you_had_zero_fear_fear_face_recognition, scripts_what_if_you_had_zero_fear_i_cant_feel_it_think_it, scripts_what_if_you_had_zero_fear_two_taps, scripts_what_if_you_had_zero_fear_leo, scripts_what_if_you_had_zero_fear_sam [INFERRED 0.85]
- **Red kite rip-current rescue flow** — scripts_what_if_your_eyesight_was_100x_sharper_theo, scripts_what_if_your_eyesight_was_100x_sharper_grandpa_sam, scripts_what_if_your_eyesight_was_100x_sharper_nova, scripts_what_if_your_eyesight_was_100x_sharper_rip_current, scripts_what_if_your_eyesight_was_100x_sharper_red_kite_rescue [EXTRACTED 1.00]
- **Real vision science claims in the film** — scripts_what_if_your_eyesight_was_100x_sharper_visual_acuity, scripts_what_if_your_eyesight_was_100x_sharper_fovea_sharp_spot, scripts_what_if_your_eyesight_was_100x_sharper_saccades, scripts_what_if_your_eyesight_was_100x_sharper_macular_degeneration, scripts_what_if_your_eyesight_was_100x_sharper_diffraction_limit [INFERRED 0.85]
- **Film page build layers: shared engine, per-film data, per-film scenes** — eyesight_100x_index, eyesight_100x_index_shared_engine, eyesight_100x_index_film_data, eyesight_100x_index_film_scenes [EXTRACTED 1.00]

## Communities (65 total, 32 thin omitted)

### Community 0 - "Eyesight: Synth Instruments & DSP"
Cohesion: 0.06
Nodes (95): adsr(), Allpass, Comb, expDecay(), OnePole, pingpong(), Pink, polyblep() (+87 more)

### Community 1 - "Zero Fear: Synth Instruments & DSP"
Cohesion: 0.06
Nodes (94): adsr(), Allpass, Comb, expDecay(), OnePole, pingpong(), Pink, polyblep() (+86 more)

### Community 2 - "Eyesight: Frame Renderer"
Cohesion: 0.05
Nodes (43): acquireLock(), attach(), barBeat(), cdp(), CHROME, cleanup(), countFrames(), DRAFT (+35 more)

### Community 5 - "Zero Fear Episode Story & Science"
Cohesion: 0.08
Nodes (34): scripts/ directory (narration scripts, one per episode), titles/ directory (batches of video title ideas), What If channel writing room, Amygdala (almond-shaped fear clusters), Broken bone heals in ~six weeks, Crane beam stunt (40 m up, safety line unclipped), Envelope cliffhanger / Part Two hook, Recognising fear in other faces (+26 more)

### Community 6 - "Zero Fear: Film Scenes"
Cohesion: 0.07
Nodes (8): crane(), docks(), faceOf(), faces(), ladder(), leoClimb(), rescue(), truth()

### Community 7 - "Eyesight: Film Scenes"
Cohesion: 0.08
Nodes (5): acuity(), bay(), kite(), letterGrid(), nova()

### Community 8 - "Eyesight Episode Story & Science"
Cohesion: 0.10
Nodes (23): eyesight-100x film page (index.html), Canvas #c (1920x1080), Per-film data scripts (timeline.js, lines.js, score.js), Per-film scene scripts (film-lib.js, film.js), Script: What If Your Eyesight Was 100x Sharper?, Diffraction limit / pupil size (pizza-sized eyes), Fovea / tiny sharp spot (thumb at arm's length), Grandpa Sam (former lifeguard with macular degeneration) (+15 more)

### Community 9 - "Zero Fear: Renderer Config"
Cohesion: 0.08
Nodes (21): CHROME, DRAFT, fs, HOOKS, http, inside(), launched, LOCK (+13 more)

### Community 12 - "Zero Fear: Audio Mix Bus"
Cohesion: 0.12
Nodes (12): Bus, fs, loadAudio(), lufs(), master(), masterOnce(), mixdown(), path (+4 more)

### Community 13 - "Eyesight: Voice Synthesis"
Cohesion: 0.19
Nodes (18): clean(), crypto, decode(), DEFAULT_VOICE, energy(), engines(), { execFileSync, spawnSync }, fit() (+10 more)

### Community 14 - "Zero Fear: Voice Synthesis"
Cohesion: 0.19
Nodes (19): clean(), crypto, decode(), DEFAULT_VOICE, energy(), engines(), { execFileSync, spawnSync }, fit() (+11 more)

### Community 16 - "Eyesight: Soundtrack Song"
Cohesion: 0.11
Nodes (14): ARP, buses, fx, GAIN, lead, mix, music, N (+6 more)

### Community 18 - "Zero Fear: Soundtrack Song"
Cohesion: 0.11
Nodes (14): ARP, buses, fx, GAIN, lead, mix, music, N (+6 more)

### Community 19 - "Eyesight: Audio Analysis"
Cohesion: 0.24
Nodes (15): analyse(), bands(), chroma(), decode(), fft(), mean(), median(), onsetEnvelope() (+7 more)

### Community 20 - "Zero Fear: Audio Analysis"
Cohesion: 0.24
Nodes (15): analyse(), bands(), chroma(), decode(), fft(), mean(), median(), onsetEnvelope() (+7 more)

### Community 21 - "Eyesight: npm Scripts"
Cohesion: 0.14
Nodes (13): description, name, private, scripts, board, build, check, music (+5 more)

### Community 22 - "Zero Fear: npm Scripts"
Cohesion: 0.14
Nodes (13): description, name, private, scripts, board, build, check, music (+5 more)

### Community 23 - "Eyesight: Mastering & Loudness"
Cohesion: 0.19
Nodes (7): fs, lufs(), master(), masterOnce(), path, TP_PHASES, truePeakAt()

### Community 24 - "Eyesight: Dialogue Timing"
Cohesion: 0.15
Nodes (8): fs, lines, OUT, path, scenes, spec, TL, vo

### Community 25 - "Zero Fear: Render Pipeline"
Cohesion: 0.21
Nodes (13): acquireLock(), barBeat(), countFrames(), evaluate(), finalName(), grab(), lintDeterminism(), main() (+5 more)

### Community 26 - "Zero Fear: Dialogue Timing"
Cohesion: 0.15
Nodes (8): fs, lines, OUT, path, scenes, spec, TL, vo

### Community 27 - "Audio Levels Tool (both)"
Cohesion: 0.18
Nodes (6): files, fs, path, files, fs, path

### Community 28 - "Eyesight: Camera Shots"
Cohesion: 0.23
Nodes (3): buffer(), Shots, transition()

### Community 30 - "Zero Fear: Camera Shots"
Cohesion: 0.23
Nodes (3): buffer(), Shots, transition()

### Community 31 - "Eyesight: Studio Boot & Assets"
Cohesion: 0.27
Nodes (3): Studio, probeAt(), renderAt()

### Community 33 - "Zero Fear: Studio Boot & Assets"
Cohesion: 0.27
Nodes (3): Studio, probeAt(), renderAt()

### Community 35 - "Eyesight: Audio Mix Bus"
Cohesion: 0.22
Nodes (5): Bus, loadAudio(), mixdown(), writeWav(), bus()

### Community 36 - "Eyesight: Preview Player"
Cohesion: 0.33
Nodes (6): drawTimeline(), pause(), play(), seek(), tick(), where()

### Community 37 - "Zero Fear: Preview Player"
Cohesion: 0.33
Nodes (6): drawTimeline(), pause(), play(), seek(), tick(), where()

### Community 40 - "Zero Fear: Headless Chrome Control"
Cohesion: 0.32
Nodes (8): attach(), cdp(), cleanup(), killChrome(), launch(), openWorker(), pageQuery(), sleep()

### Community 42 - "Eyesight: Brand Colors"
Cohesion: 0.48
Nodes (5): contrast(), dist(), lum(), rgb(), sat()

### Community 44 - "Zero Fear: Brand Colors"
Cohesion: 0.48
Nodes (5): contrast(), dist(), lum(), rgb(), sat()

### Community 46 - "Eyesight: Cliff Sunset Scenes"
Cohesion: 0.50
Nodes (4): call(), cliff(), cliffTop(), sunset()

## Ambiguous Edges - Review These
- `zero-fear.srt (English captions)` → `Shared animation engine (util, music, gfx, chars, ui, shots, subs, geo, data, boot)`  [AMBIGUOUS]
  zero-fear/index.html · relation: conceptually_related_to

## Knowledge Gaps
- **11 isolated node(s):** `What If You Had Zero Sense Of Pain? (title #15)`, `What If Your Emotions Were 10x Stronger? (title #27)`, `What If Your Empathy Was 100x Stronger? (title #34)`, `Mia (classmate)`, `thumbnail.jpg (1280x720)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 424 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SVF` connect `Zero Fear: Synth Instruments & DSP` to `Zero Fear: Audio Mix Bus`, `Zero Fear: Voice Synthesis`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **What connects `What If You Had Zero Sense Of Pain? (title #15)`, `What If Your Emotions Were 10x Stronger? (title #27)`, `What If Your Empathy Was 100x Stronger? (title #34)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Eyesight: Synth Instruments & DSP` be split into smaller, more focused modules?**
  _Cohesion score 0.0559228650137741 - nodes in this community are weakly interconnected._
- **Why does `SVF` connect `Eyesight: Synth Instruments & DSP` to `Eyesight: Voice Synthesis`, `Eyesight: Mastering & Loudness`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `Zero Fear: Synth Instruments & DSP` be split into smaller, more focused modules?**
  _Cohesion score 0.05658263305322129 - nodes in this community are weakly interconnected._
- **Why does `OnePole` connect `Zero Fear: Synth Instruments & DSP` to `Zero Fear: Audio Mix Bus`, `Zero Fear: Voice Synthesis`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `zero-fear.srt (English captions)` and `Shared animation engine (util, music, gfx, chars, ui, shots, subs, geo, data, boot)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._