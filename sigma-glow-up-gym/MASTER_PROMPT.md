# MASTER PROMPT — Build "Sigma Glow-Up Gym" completely

> **To Claude Code:** this file is your complete instructions. Read it top to bottom before doing
> anything, then follow it part by part. It sits on top of `CLAUDE.md` (coding rules),
> `BUILD_SPEC.md` (milestone details) and `GDD.md` (game design). When this file adds detail beyond
> those documents, **this file wins**. When something is still unclear, decide using `GDD.md`, write
> the decision in `DECISIONS.md`, and keep going.

---

## PART 0 — Who you're working for and how to behave

- The owner of this project is a **beginner**. They can click things in Roblox Studio and copy/paste,
  but they don't code. Do everything that can be done from the terminal yourself.
- Talk simply. Short sentences. Numbered steps for anything they must click. No jargon without a
  one-line explanation.
- Don't ask questions you can answer yourself with sensible defaults from `GDD.md`. Only stop when
  (a) you hit a **testing checkpoint** (Part 9), or (b) you're truly blocked by something only the
  owner can do (Part 10).
- Work in small, safe steps: implement → self-check → commit → move on. Never leave the project in a
  broken state between commits.
- If you run out of context or stop partway, write **exactly** where you stopped and what's next at the
  top of `PROGRESS.md`, so "continue" picks up cleanly.
- Keep a running `PROGRESS.md`: one line per finished task with date and commit hash.

---

## PART 1 — Get the project and understand it

1. Look for the `sigma-glow-up-gym` folder in/under the current directory.
   - Not found → `git clone -b claude/quirky-gates-xxoqy9 https://github.com/gono123/goatziv.git`
     and use `goatziv/sigma-glow-up-gym`.
   - Found → `git checkout claude/quirky-gates-xxoqy9 && git pull`.
2. All work happens inside `sigma-glow-up-gym/`. Commit and push to branch
   `claude/quirky-gates-xxoqy9` only.
3. Read completely: `CLAUDE.md`, `BUILD_SPEC.md`, `GDD.md`, `README.md`, and **every file in `src/`**.
4. Write a 10-line summary for yourself in `PROGRESS.md` of how the existing code works
   (boot order, services, remotes, data template) so later milestones stay consistent.

---

## PART 2 — Tooling (set up everything for the owner)

1. Install **Rokit** if missing (official installer for the OS — check `rokit --version` first).
2. Update `rokit.toml` to contain (latest stable versions):
   - `rojo` (rojo-rbx/rojo), `selene` (Kampfkarren/selene), `stylua` (JohnnyMorganz/StyLua),
     `lune` (lune-org/lune). Run `rokit install`.
3. Create:
   - `selene.toml` → `std = "roblox"` (add rule tweaks only if needed; explain any in DECISIONS.md)
   - `stylua.toml` → `indent_type = "Tabs"`, `column_width = 120`, `quote_style = "AutoPreferDouble"`
   - `scripts/check.sh` **and** `scripts/check.ps1` (Windows) that run, in order:
     `stylua --check src tests`, `selene src`, `lune run tests/run`, `rojo build -o build.rbxl`.
     Exit non-zero on any failure.
4. **Unit tests with Lune** (`tests/`):
   - `tests/run.luau` discovers and runs every `tests/*.spec.luau`.
   - Pure modules are loaded by reading the source and running it with
     `luau.load(source, { environment = env })`, where `env` provides a fake
     `script` tree and `require = function(x) return x end`, so
     `require(script.Parent.Config.Training)` simply returns the injected config table.
     Provide stubs for `Color3.fromRGB`, `Vector3.new`, `math.clamp`.
   - Put all pure game logic in `src/shared/Logic/` (no Roblox services inside):
     `Formula` (move/keep), `Rating` (Elo), `Streak` (day math), `QuestPicker`, `PoseOffScoring`,
     `Economy` (cost checks), `Offline` (offline Aura calc). Services call these.
   - Tests to write (minimum): number abbreviation; marker position + quality zones; Aura formula;
     stage thresholds reachable in order; pacing simulation (60% Perfect player hits Gym Rat < 90 s,
     Chad 3–6 min, Sigma 18–30 min — **tune `Stages.luau` until this passes**); Elo sums to ~0 and
     tiers map correctly; streak continue/freeze/reset cases; quest picker deterministic + no duplicate
     kinds; Pose-Off scoring incl. NPC-crowd fallback; offline cap; purchase idempotency logic.
5. **GitHub Actions** `.github/workflows/sigma-ci.yml` (in the repo root, scoped to
   `sigma-glow-up-gym/**`): install Rokit tools and run the check script on push.
6. Run the check script. Everything must pass before Part 3.
7. Start `rojo serve` in a background terminal and keep it running.
8. Give the owner the **Studio first-run steps** (numbered, simple):
   1. Open Roblox Studio → New → **Baseplate**.
   2. Plugins → Manage Plugins / Toolbox → install **Rojo** → click **Rojo → Connect**.
   3. Home → **Game Settings** → Avatar → **R15** → Save.
   4. File → **Publish to Roblox** (create new game).
   5. Game Settings → Security → **Enable Studio Access to API Services** → Save.
   6. Press **Play**. Expected: coloured gym blocks, HUD at the top, pressing a block's prompt shows a
      tap bar.
   If the **Roblox Studio MCP server** is connected to you, use it to read Studio's Output and run
   checks yourself instead of asking.

---

## PART 3 — Engineering rules (in addition to CLAUDE.md)

**Server authority & safety**
- Every `OnServerEvent` handler starts with: data loaded? → `RateLimiter.allow(player, name, rate)` →
  type/NaN/range validation (`Validate` helper) → state check (e.g. not in a Pose-Off) → act.
- Create `src/server/Util/RateLimiter.luau` and `src/server/Util/Validate.luau` **now** (not M13),
  and use them for every remote from here on (retrofit the existing ones).
- Never give rewards twice: every reward path has a guard (claimed flags, match ids, receipt ids).

**State conflicts — handle all of these everywhere**
- Player leaves mid-action (training, queue, Pose-Off, Titan, purchase).
- Character dies/resets/respawns mid-action (re-apply look, clear sessions, restore WalkSpeed).
- Glow Reset while in queue/Pose-Off/Titan → block with a toast.
- Training while in a Pose-Off → stop training on teleport.
- Data not loaded yet → ignore requests silently.
- Two players doing the same thing at the same time (same machine station → allowed; each station
  supports one player: if occupied, toast "Station taken — try the next one").
- Server shutdown → BindToClose saves (already exists; keep it working).

**Architecture additions**
- `src/server/Services/EconomyService.luau` owns **all** currency changes:
  `AddAura` (moves here from EvolutionService, which keeps calling it), `AddDrip`, `SpendDrip`,
  `AddShards`, `SpendShards`. Each logs analytics (M12) and syncs the client once.
- `src/server/Services/EffectsService.luau` + `src/client/Controllers/EffectsController.luau`:
  one `PlayEffect(effectName, params)` remote (server → all/nearby clients) for visuals other players
  should see (stage-up shockwave, Mog beam, Titan stomp). Clients spawn the visuals locally.
- `src/shared/Config/Sounds.luau` + `src/client/Controllers/SoundController.luau` (Part 6).
- `src/shared/Config/Admins.luau` + Debug panel (Part 7).
- Keep `DataSync` lean: send only what the HUD needs; add a `version` counter.

**Performance budget**
- Map ≤ ~3,500 parts. `workspace.StreamingEnabled = true` (set in MapBuilder).
- No per-player server loops faster than 0.25 s. Batch timers into one loop per service.
- Particle rates modest; disable decorative particles on low graphics quality
  (`UserGameSettings().SavedQualityLevel` on client).

---

## PART 4 — UI design system (build first, use everywhere)

Create `src/client/UI/Theme.luau` and `src/client/UI/Components.luau`.

**Theme**
| Token | Value |
|---|---|
| Orange (primary) | `#FF8A1F` |
| Teal (secondary) | `#1FC7B6` |
| Gold (rewards/Perfect) | `#FFD23F` |
| Panel | `#1B1B26` at 8% transparency |
| Text | `#FFFFFF`, stroke `#000000` 2–3 px |
| Success / Danger | `#3DD68C` / `#E5484D` |
| Header font | `Enum.Font.FredokaOne` |
| Body font | `Enum.Font.GothamBold` |
| Corner radius | 14 px panels, 12 px buttons |

**Components** (functions returning instances): `Button(text, color, size)` (press tween to 0.94,
click sound, min 48 px tall), `IconButton(emoji, label)` (64×64 with label under),
`Panel(title)` (centered modal, 90% width on phone / max 560 px, close X 48 px, dim backdrop,
tap-outside closes), `ProgressBar`, `Chip(text, color)` (pill for boosts/timers), `Toast(text)`,
`Popup(text, color, scale)` (floating number), `Tabs(names)`, `ListItem`, `Badge(count)` (red
notification dot).
- Every ScreenGui: `ResetOnSpawn = false`, `ScreenInsets = Enum.ScreenInsets.DeviceSafeInsets`.
- Rebuild the existing HUD/Training/Cutscene UIs to use these components.

**Screen layout (phone first)**
```
┌──────────────────────────────────────────────┐
│ [boost chips]   STAGE NAME / AURA / bar  [⏱ Titan 12:34] │  top
│ [🛒][👕][📋][🌟]  (left column, 64px each)                │
│                                                  │
│               (world)                            │
│                                                  │
│          [ training bar + combo ]       [ POSE ] │  bottom
└──────────────────────────────────────────────┘
```
- Left column buttons: Shop 🛒 (hidden until Chad), Drip 👕, Quests 📋 (badge when claimable),
  Perks 🌟 (after first Glow Reset). Settings ⚙️ (music/SFX volume, low-effects mode).
- Quality text always includes words ("PERFECT!") — never colour-only feedback.

---

## PART 5 — Build the world in code (MapBuilder)

Replace `Greybox.luau` with `src/server/World/MapBuilder.luau` plus one module per zone in
`src/server/World/Zones/`. It builds the entire map on server start **unless** `workspace.Map`
already exists (so a hand-built map can replace it later). Equipment models are built from parts in
`src/server/World/Props/` (one builder function per prop). All dimensions/positions in
`src/shared/Config/World.luau`.

**Global**
- Baseplate: keep, recolour `#3A3F4B`, Material Concrete. Lighting: `ClockTime = 14`,
  `Technology = ShadowMap`, `Brightness = 2.5`, Atmosphere (density 0.25, haze 1), Bloom
  (intensity 0.4, threshold 1.2), ColorCorrection (saturation 0.1, contrast 0.05).
- `SpawnLocation` at (0, 0.5, 0) facing −Z, neon orange ring decal-style part around it.
- Signs: `BillboardGui` or `SurfaceGui` with FredokaOne, big readable text.

**Zones** (centre positions, Y = floor)
| Zone | Centre | Size | Look | Contents |
|---|---|---|---|---|
| Spawn Plaza | (0,0,0) | 50×50 | orange-trim concrete | spawn, welcome sign "SIGMA GLOW-UP GYM", arrow decals to Starter Gym |
| Starter Gym | (0,0,−70) | 90×60 | dark rubber-look floor (Slate, `#2B2B33`), half walls, mirror back wall (Glass, reflectance 0.4) | 3× Dumbbells, 3× Bench stations, motivational signs ("+1 AURA EVERY REP") |
| Iron Yard | (110,0,−70) | 90×70 | outdoor asphalt (`#30343A`), chain-link fences (Fence material or ForceField-transparent parts), floodlights | 3× Squat Rack, 3× Tire Flip; **gate: Chad** |
| Mog Mansion | (110,0,−180) | 80×60 | marble (Marble `#EDE6D6`), gold trims (Foil `#D4AF37`), chandeliers (PointLights) | 3× Meteor Press, VIP lounge room (door gated by VIP pass); **gate: Gigasigma** |
| Cosmic Dojo | (0,80,−210) | 70×70 floating | Neon purple edges, black glass floor, star particles | 3× Black Hole Bench; reached by a launch pad at (0,0,−120) (server checks unlock; teleports with a whoosh effect); **gate: Cosmic Mogger or 3 Glow Resets** |
| Pose-Off Arena | (−110,0,−70) | stage 44×20 raised 3 | glossy black stage, 4 pedestals with SpotLights (visible from spawn), 3-tier bleachers (60 wide), giant "POSE-OFF" neon sign | queue pad (neon, pulsing) in front, scoreboard SurfaceGui |
| Titan Plaza | (0,0,90) | circle r=55 | cracked concrete ring, warning stripes | 45-stud clock pillar with countdown SurfaceGui on all 4 sides (visible from spawn) |
| Drip Shop | (−60,0,40) | 24×18 building | pink/teal storefront, mannequins | counter ProximityPrompt "Shop" |
| Hall of Mog | (60,0,40) | wall 50×20 | gold frame | 3 SurfaceGui leaderboards (weekly Aura, season Rating, Titan hits) |

**Zone gates:** an invisible `GateWall` part (CanCollide true for locked players) at each zone entrance
with a sign "🔒 Unlocks at CHAD". Implement gating **server-side** by using `PhysicsService`
collision groups per player (put locked players' characters in group `Locked_<Zone>` that collides
with that gate; unlocked players don't) — and also block equipment use server-side (already done).

**Props (built from parts, each a Model with PrimaryPart "Base", tagged `Equipment`, attribute
`EquipmentId`)**
- Dumbbells: low rack + 2 dumbbells (cylinder handle + 2 cylinder plates each).
- Bench: padded bench (red), 2 uprights, barbell (long thin cylinder) with 2 plates each side.
- Squat Rack: 2 tall uprights, crossbar, barbell with big plates.
- Tire Flip: large black cylinder lying flat (tyre), inner hole illusion with a darker cylinder.
- Meteor Press: steel frame + glowing orange Neon sphere with PointLight and slow-spinning particles.
- Black Hole Bench: bench + black sphere with purple Neon ring and swirling ParticleEmitter.
- Each station has a floor marker (thin neon square) where the player stands; `TrainingService`
  moves the player onto it and faces them toward the prop.
- Equipment label above each: name, `+X Aura/rep`, and lock text if locked (client-side lock tint).

When MapBuilder exists, delete `Greybox.luau` and update `init.server.luau` and docs.

---

## PART 6 — Audio & VFX

**`Config/Sounds.luau`** (ids empty until the owner picks licensed audio — see Part 10):
`Click, RepPerfect, RepGood, RepMiss, LockedInLoop, StageUp, GlowReset, CrowdCheer, VoteTick,
PoseOffWin, Siren, TitanStomp, TitanDefeated, Purchase, QuestComplete, Music_Gym, Music_Arena`.
`SoundController.Play(name)` silently skips empty ids. Volume settings saved in data
(`settings = { music = 0.5, sfx = 0.8, lowEffects = false }`).

**VFX list** (all client-side via EffectsController unless noted)
- Perfect rep: small gold spark burst at the character's hands + popup + tiny camera shake.
- LOCKED IN: gold particles from the head + PointLight; bar border glows; LockedInLoop sound.
- Stage-up (seen by everyone nearby): expanding Neon ring (shockwave) at feet, 1 s; plus the owner's
  cutscene. Sunglasses **drop from above** onto the face at Sigma (tween the shades from +6 studs).
- Glow Reset: white flash, avatar shrinks back with a "deflate" tween, rising white particles.
- Pose-Off Mog finale: `Beam`s from each loser's chest to the winner (2 s, gold), loser avatars dim.
- Titan: stomp landing dust ring + strong shake; defeat = shrink to 0.1 + "run away" walk + poof.
- Purchase / quest complete: confetti burst on screen (UI particles via small frames).

---

## PART 7 — Debug / admin panel (for testing — build early)

- `Config/Admins.luau`: list of user ids; always include `game.CreatorId` (if the game is owned by a
  user) and allow everyone **in Studio** (`RunService:IsStudio()`).
- Toggle with **F8** or a small 🛠 button (admins only). Server re-checks admin on every command.
- Commands: +1K / +1M / +1B Aura; set stage 1–6; +1,000 Drip; +100 Shards; Glow Reset now;
  start Titan now; Titan skip phase; start Pose-Off with bots now; add bot to queue;
  debug day offset +1 (for streak/quests); reset my data; fast mode (all cooldowns ÷10, timers ÷5);
  grant any pose/cosmetic; simulate purchase of any product (Studio only).
- Every TESTING.md checklist should say which debug button to use to get there quickly.

---

## PART 8 — The build order (do all of it)

Do these in order. For **each** step: plan → implement → run the check script (Part 2) → review your
own diff for bugs + the Part 3 conflict list → write its TESTING.md section → tick it in
`BUILD_SPEC.md` + `PROGRESS.md` → commit → push → 3–5 line plain-English summary to the owner.

| Step | What | Source of details |
|---|---|---|
| **S1** | Tooling, tests, CI (Part 2) | this file |
| **S2** | Refactor: Logic modules, RateLimiter/Validate, EconomyService, EffectsService, Sounds, UI kit, rebuild existing UIs with the kit | Parts 3, 4, 6 |
| **S3** | Debug panel | Part 7 |
| **S4** | World: MapBuilder, zones, props, gates, station markers, lighting | Part 5 |
| ⏸ | **CHECKPOINT A** — owner plays and looks at the map | Part 9 |
| **S5** | M4 Poses + wheel | BUILD_SPEC M4 |
| **S6** | M5 Pose-Off arena + Rating (use the arena from S4 instead of ArenaGreybox) | BUILD_SPEC M5 |
| ⏸ | **CHECKPOINT B** — Pose-Off test with Start Server + 3 players | Part 9 |
| **S7** | M6 Boosts + Titan (use Titan Plaza from S4) | BUILD_SPEC M6 |
| **S8** | M7 Streak, quests, spotter, offline | BUILD_SPEC M7 |
| **S9** | M8 Perk tree | BUILD_SPEC M8 |
| **S10** | M9 Drip Shop + cosmetics (use the shop building from S4) | BUILD_SPEC M9 |
| **S11** | M10 Monetization | BUILD_SPEC M10 |
| ⏸ | **CHECKPOINT C** — test purchases in Studio | Part 9 |
| **S12** | M11 Tutorial (FTUE), Hall of Mog boards, mobile pass | BUILD_SPEC M11 |
| **S13** | M12 Analytics (Telemetry wrapper) | BUILD_SPEC M12 |
| **S14** | M13 ProfileStore + anomaly logging (RateLimiter/Validate already done) | BUILD_SPEC M13 |
| **S15** | Polish pass (Part 8b) | this file |
| ⏸ | **CHECKPOINT D** — full playthrough | Part 9 |
| **S16** | Launch docs (Part 11) | this file |

### Extra requirements per milestone (on top of BUILD_SPEC)

**M4 Poses**
- Pose wheel: 8 wedges in a circle (or 2×4 grid on very small screens), each with pose name + small
  icon emoji; locked slots greyed with 🔒. Long-press (0.5 s) a wedge → "Choose pose" list panel.
- Poses freeze movement for `PoseDuration` and can't be used while training (toast).
- Placeholder billboard text when `animationId` is nil: big pose name + 💪, scale-pop tween.

**M5 Pose-Off**
- Camera: contestants and spectators within 90 studs get a Scriptable orbit camera on the current
  showcase contestant (1.5 rad/s), returned to Custom after Showcase.
- Bleachers spectators see a vote bar with each contestant's name + avatar headshot
  (`Players:GetUserThumbnailAsync`, cached) and 🔥 button.
- Scoreboard SurfaceGui shows live round scores to everyone in the area.
- Results card shows: placement medal, per-round scores (timing / prompt / crowd), rating change with
  ▲▼, Drip earned, new tier if changed, **QUEUE AGAIN** button.
- Spectators who vote in all 3 rounds get a small "Hype Bro" bonus (+3 Drip).
- Match id per match; reward function guarded by match id.

**M6 Titan**
- HUD Titan countdown chip always visible top-right; pulses red in the last 60 s; tap → camera
  arrow toward Titan Plaza.
- Sync phase UI: big server meter at top ("SYNC 63%"), personal hits counter, prompt words flashing.
- If the meter fails: Titan "laughs" (emote), leaves; everyone still gets 25% of normal Drip.
- `SummonNow` respects a 10-minute minimum gap and can't start during an active event.

**M7 Retention**
- Daily panel: 7-day row of shake cups (claimed ✓ / today glowing / future dim), freeze ❄️ indicator.
- Quests panel: 3 cards with progress bars, CLAIM buttons, reroll 🎲 (1/day).
- Offline claim panel on join with big number and CLAIM (no auto-grant, so players feel it).
- Respect FTUE: none of these panels pop up until `bestStage ≥ 3`.

**M9 Cosmetics**
- Preview: when browsing, show the item on a ViewportFrame clone of the player's character.
- Items have rarity colours (Common grey, Rare blue, Epic purple, Legendary gold) — **purely
  cosmetic**, fixed prices, no random packs.

**M10 Monetization**
- Store panel tabs: Boosts, Passes, Drip. Each card: icon emoji, name, one-line benefit, Robux price.
- "Summon Titan" card shows "Everyone in the server gets rewards!".
- Never auto-open the store. Never show purchase prompts before Chad (`FirstShopPromptStage`).

**M11 FTUE & map**
- Guidance arrow: a `Beam` from the player to the target (client-side), plus a bouncing billboard
  arrow above the target.
- First Pose-Off for a new player: bot timing 8–20 so they likely win; give a one-time "First Pose-Off"
  bonus of 50 Drip.

### Part 8b — Polish pass (S15)
- Juice: button press tweens, number tick-up animations on Aura, bar fill tweens, idle bobbing on
  equipment labels, particle sparkle on claimable buttons.
- Feel: training bar slightly faster at higher stages? **No** — keep Period constant; instead make
  LOCKED IN feel great (sound + glow).
- Readability: test UI at 375×667 (iPhone SE) and 1920×1080; nothing overlaps Roblox's top bar,
  jump button or thumbstick.
- Performance: count parts; check client FPS with lowEffects on/off; no warnings spam in Output.
- Audit every remote one last time against Part 3.
- Make sure the game is fun without spending and without chat.

---

## PART 9 — Testing checkpoints

`TESTING.md` format for each step:
```
## S6 — Pose-Off
Setup: Test tab → Clients and Servers → 3 players → Start. (Or debug panel: "Start Pose-Off with bots".)
1. On Player1 and Player2, walk onto the glowing POSE-OFF pad.  Expect: pad shows 2/4, countdown 10.
2. ...
Pass if: ...
If something fails: copy the red text from the Output window and paste it to Claude Code.
```
At each ⏸ checkpoint: stop, show the owner **only** the sections to test now, wait for their result,
fix every reported issue (with a regression test in `tests/` if it's pure logic), then continue.
If the Studio MCP is connected, run the checks yourself and report results instead of asking.

---

## PART 10 — Things only the owner can do → `MY_TODO.md`

Write click-by-click instructions for each, and keep the game working without them (placeholders):
1. **Animations** (8 poses + 6 lift loops + Titan stomp/laugh): Studio → Avatar tab → Rig Builder
   (R15) → Animation Editor → pose keyframes → Publish (owned by the same user/group as the game)
   → copy the `rbxassetid://` id → paste ids to Claude Code (you then update `Poses.luau`/`Equipment.luau`).
   Include a short description of each pose so they know what to animate.
2. **Audio**: Creator Store → Audio → search terms for each `Sounds.luau` entry (e.g. "phonk loop",
   "crowd cheer", "air horn", "whoosh") → copy ids → paste to Claude Code.
3. **Game passes & developer products**: Creator Hub → Creations → the game → Monetization → create
   each from `Products.luau` with the given prices and descriptions (write the descriptions for them)
   → paste ids.
4. **Icon & thumbnails**: write 3 detailed image prompts/briefs (GDD §14) they can give to an artist.
5. **Experience settings**: description (write it for them), genre, max players 24, content
   maturity questionnaire, social links, private-server price.
6. **Testing on a real phone** (Roblox app → their game while it's private/friends-only).

---

## PART 11 — Launch docs (S16)

- `LAUNCH.md`: final title options + recommendation; store description (fun, simple, keywords:
  gym, aura, glow up, sigma, pose, simulator, obby-free); 5 short-video clip ideas with shot-by-shot
  instructions (transformation, losing by 1 vote, whole server mogging the Titan, LOCKED IN, Glow
  Reset); soft-launch ad plan ($10–20/day for 3–5 days); which Creator Hub Analytics numbers to watch
  (first-play bounce, D1, session length, Pose-Off participation %, D7) and **which Config values to
  change** if each is bad.
- `LIVEOPS.md`: weeks 1–8 from GDD §18 as ready-to-paste Claude Code prompts, plus the weekly
  meme-swap Titan skin process.
- Final: full codebase review for bugs/exploits/performance → fix → check script green → commit →
  push → final plain-English summary: what's done, what's on `MY_TODO.md`, exact next steps to publish.

---

## PART 12 — Definition of done (the whole project)

- [ ] Check script passes (format, lint, unit tests, Rojo build); CI green.
- [ ] Every step S1–S16 ticked in `PROGRESS.md` and `BUILD_SPEC.md`.
- [ ] All four checkpoints passed by the owner (or via Studio MCP).
- [ ] Game is fully playable with placeholders; `MY_TODO.md` lists everything left for the owner.
- [ ] No purchase prompt before Chad; nothing pay-to-win; works without chat; works on phone.
- [ ] `LAUNCH.md`, `LIVEOPS.md`, `TESTING.md`, `DECISIONS.md`, `MY_TODO.md` written.
- [ ] Everything committed and pushed to `claude/quirky-gates-xxoqy9`.

**Start now with PART 1.**
