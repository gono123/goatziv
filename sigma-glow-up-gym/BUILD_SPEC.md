# BUILD_SPEC.md — Sigma Glow-Up Gym, milestone by milestone

This is the build breakdown for Claude Code. Each milestone has **goal → files → exact
requirements → data / remotes → acceptance checklist → a prompt to paste into Claude Code**.
Work through them in order; each one builds on the last. Design reasoning lives in `GDD.md`;
coding rules live in `CLAUDE.md`.

## Status

| # | Milestone | Status |
|---|---|---|
| M0 | Project setup (Rojo, folders, boot scripts) | ✅ Done |
| M1 | Training loop: timing bar, server-validated reps, Aura, saving | ✅ Done |
| M2 | Evolution: 6 stages, body scaling, shades, aura particles, cutscene, HUD | ✅ Done |
| M3 | Glow Reset (rebirth) | ✅ Done (perk tree is M8) |
| M4 | Poses + pose wheel | ⬜ |
| M5 | Pose-Off arena (signature mode) | ⬜ |
| M6 | Boosts + hourly Titan event | ⬜ |
| M7 | Retention: streak, quests, spotter bonus, offline Aura | ⬜ |
| M8 | Glow Shard perk tree | ⬜ |
| M9 | Drip Shop + cosmetics | ⬜ |
| M10 | Monetization: gamepasses + developer products | ⬜ |
| M11 | First-time experience + mobile polish + real map | ⬜ |
| M12 | Analytics funnel + economy events | ⬜ |
| M13 | ProfileStore migration + anti-exploit hardening | ⬜ |
| M14 | Launch prep | ⬜ |
| — | Live-ops weekly template | ongoing |

## Master prompt steps (MASTER_PROMPT.md Part 8)

- [x] S1 Tooling, tests, CI
- [x] S2 Refactor, UI kit, effects, sounds
- [x] S3 Debug panel
- [x] S4 World: MapBuilder, zones, props, gates
- [x] Owner changes: clicks only, upgrades, daily brainrot spin (see DECISIONS.md)
- [ ] Checkpoint A
- [ ] S5 Poses (M4)
- [ ] S6 Pose-Off (M5)
- [ ] Checkpoint B
- [ ] S7 Boosts + Titan (M6)
- [ ] S8 Retention (M7)
- [ ] S9 Perk tree (M8)
- [ ] S10 Drip Shop (M9)
- [ ] S11 Monetization (M10)
- [ ] Checkpoint C
- [ ] S12 Tutorial, Hall of Mog, mobile pass (M11)
- [ ] S13 Analytics (M12)
- [ ] S14 ProfileStore + anomaly logging (M13)
- [ ] S15 Polish pass
- [ ] Checkpoint D
- [ ] S16 Launch docs

---

## How to work with Claude Code on this

1. On your computer: clone this repo, `cd sigma-glow-up-gym`, run `rokit install`, then `rojo serve`.
2. In Roblox Studio: new **Baseplate** place → install the **Rojo** plugin → Connect.
   - Game Settings → **Avatar → R15** (body scaling needs R15).
   - Game Settings → **Security → Enable Studio Access to API Services** (saving in Studio).
   - Publish the place once so DataStores work.
3. Start `claude` in the `sigma-glow-up-gym` folder. It reads `CLAUDE.md` automatically.
4. Paste the milestone prompt. Let it write code. Rojo syncs it into Studio live.
5. Playtest (Test tab → **Start** with *2 Players* for anything multiplayer). Copy any red errors
   from the **Output** window back into Claude Code.
6. Run the acceptance checklist. When it passes: ask Claude Code to tick the status table and commit.

Optional: connect Roblox's **Studio MCP server** to Claude Code so it can read Studio's Output and
run test snippets itself (check Roblox's Creator Docs for current setup steps).

---

## M0–M3 (done) — what exists

**Files**
```
default.project.json, rokit.toml
src/shared/Config/{Stages,Equipment,Training}.luau
src/shared/{Formula,NumberFormat,Remotes}.luau
src/server/init.server.luau, src/server/Greybox.luau
src/server/Services/{DataService,EvolutionService,TrainingService}.luau
src/client/init.client.luau
src/client/Controllers/{HUDController,TrainingController,CutsceneController}.luau
```

**How it works**
- `World/MapBuilder` (S4) builds the map and its equipment. Each machine is tagged `Equipment` and gets
  a ProximityPrompt ("Train") and a label.
- Triggering a prompt → `TrainingService:Begin` checks unlock + range, freezes the player
  (WalkSpeed/Jump 0), stores `cycleStart = workspace:GetServerTimeNow()`, fires `TrainingStarted`.
- Client draws the marker with `Formula.MarkerPosition(serverNow - cycleStart)` and sends
  `RequestRep(serverNowAtTap)`. Server clamps the timestamp, enforces `RepCooldown`, recomputes
  quality, updates combo (20 Perfects = LOCKED IN, wider gold zone, ×1.5), adds Aura.
- `EvolutionService:AddAura` → `CheckStage` (can jump multiple stages) → `ApplyLook`
  (R15 scale NumberValues relative to the avatar's own base, placeholder shades from Sigma, aura
  ParticleEmitter) → `StageUp` → client cutscene (desaturate, FOV punch, name slam).
- Glow Reset button appears from Gigasigma; double-tap to confirm; resets stage/Aura, +50% permanent,
  grants Glow Shards.
- Verified outside Studio: all files parse; formula + number formatting run correctly; simulated
  pacing at 60% Perfect: Gym Rat 0.8 min, Chad 3 min, Sigma 16 min, Gigasigma 59 min, Cosmic 3.9 h.

**Manual check still needed in Studio (do this first!)**
- [ ] Play solo: greybox equipment appears; Dumbbells prompt works; bar sweeps; taps give pop-ups.
- [ ] Gym Rat reached in under ~90 s with decent timing; cutscene plays; body visibly widens.
- [ ] Scaling: at Cosmic (set `data.aura` high via the command bar or temporarily lower thresholds)
      the avatar is clearly bigger. **If scale values clamp**, tell Claude Code: "implement the
      muscle-suit fallback from BUILD_SPEC M2-fallback".
- [ ] Stop button and re-pressing the prompt both stop training and restore movement.
- [ ] Rejoin: Aura and stage persist (needs API access enabled + published place).

**Tuning note:** Sigma arrives at ~16 min vs the GDD's ~25 min target. To slow it, raise
`Stages.List[4].auraRequired` from 30000 to ~45000.

### M2-fallback (only if body scaling clamps)
Create per-stage "muscle suit" accessories (exaggerated arm/chest/shoulder meshes) stored in
`ServerStorage.Physiques.<StageName>` and attached in `EvolutionService:ApplyLook` instead of (or
on top of) scale values. Remove the previous stage's suit on change.

---

## M4 — Poses + pose wheel

**Goal:** players own and perform poses as emotes anywhere; poses unlock by stage, wins or shop.

**Files**
- `src/shared/Config/Poses.luau` (new)
- `src/server/Services/PoseService.luau` (new; add to `ORDER` after EvolutionService)
- `src/client/Controllers/PoseWheelController.luau` (new)
- `DataService.luau` TEMPLATE, `Remotes.luau`

**Config: `Poses.luau`**
```lua
return {
	LilFlex       = { displayName = "Lil Flex",          tags = { "flex" },              unlock = { type = "start" },               animationId = nil },
	DoubleBi      = { displayName = "The Double Bi",     tags = { "flex", "classic" },   unlock = { type = "stage", value = 2 },    animationId = nil },
	SideEye       = { displayName = "Side Eye",          tags = { "unbothered" },        unlock = { type = "stage", value = 3 },    animationId = nil },
	LockedIn      = { displayName = "Locked In",         tags = { "unbothered", "aura" },unlock = { type = "stage", value = 4 },    animationId = nil },
	MewingMoment  = { displayName = "Mewing Moment",     tags = { "jawline" },           unlock = { type = "wins",  value = 3 },    animationId = nil },
	MainCharacter = { displayName = "Main Character",    tags = { "aura", "drip" },      unlock = { type = "shop",  price = 250 },  animationId = nil },
	CosmicLats    = { displayName = "Cosmic Lat Spread", tags = { "flex", "aura" },      unlock = { type = "stage", value = 5 },    animationId = nil },
	TheMog        = { displayName = "The Mog",           tags = { "jawline", "aura" },   unlock = { type = "wins",  value = 10 },   animationId = nil },
}
```
Also export `WheelSize = 8`, `PoseDuration = 2.5`, `PoseCooldown = 1`.

**Requirements**
- Data: `ownedPoses = { LilFlex = true }`, `poseWheel = { "LilFlex" }`, `stats.poseOffWins = 0`.
- `PoseService:RefreshUnlocks(player)` grants poses whose unlock condition is met (`start`,
  `stage` ≥ value or Glow-Reset-agnostic: use **highest stage ever reached** — add
  `data.bestStage`, updated in `EvolutionService:CheckStage`; `wins` ≥ `stats.poseOffWins`).
  Call it on load, on stage-up, after Pose-Off wins. Newly unlocked poses are auto-added to empty
  wheel slots and trigger `Notify("New pose: X!")`.
- `RequestPose(poseId)`: validate owned + cooldown; play the animation on the server-side Animator
  (so everyone sees it) for `PoseDuration`; freeze movement during the pose.
- **Placeholder until animations exist:** if `animationId` is nil, show a BillboardGui above the
  head with the pose name in big text for `PoseDuration` (so the system is testable now).
- `RequestSetWheel(slotIndex, poseId)`: validate slot 1..8 and ownership.
- Client: a round **POSE** button (bottom-right, 72 px) opens a radial wheel of 8 slots; tap a slot
  to pose; keyboard `G` toggles the wheel on PC. Long-press a slot → list of owned poses to assign.
- `PoseService:Perform(player, poseId)` must be callable by other services (Pose-Off uses it).

**Remotes:** `RequestPose(poseId)`, `RequestSetWheel(slot, poseId)`, `PoseSync(ownedPoses, poseWheel)` (S→C).

**Animation gotcha:** animations only play if they're owned by the experience owner (your user or
group). Publish them from Studio's Animation Editor under the same account/group as the game, then
paste the `rbxassetid://` ids into `Poses.luau`.

**Acceptance**
- [ ] New player has Lil Flex on the wheel; POSE button opens the wheel on mobile emulator.
- [ ] Reaching Gym Rat unlocks The Double Bi with a toast; it appears on the wheel.
- [ ] Other players see the pose (billboard placeholder or animation).
- [ ] Spamming pose requests is rate-limited; unowned pose ids are rejected.
- [ ] Glow Reset does not remove stage-unlocked poses.

**Prompt**
> Implement milestone M4 from BUILD_SPEC.md exactly (Poses config, PoseService, PoseWheelController,
> data fields incl. bestStage, remotes, billboard placeholder when animationId is nil). Follow
> CLAUDE.md rules. Then list what I should test in Studio.

---

## M5 — Pose-Off arena (the signature mode)

**Goal:** 2–4 players compete in 3 crowd-judged rounds; spectators vote and earn rewards;
works in empty servers via bots and NPC crowd.

**Files**
- `src/shared/Config/PoseOff.luau`, `src/shared/Config/Prompts.luau` (new)
- `src/server/Services/PoseOffService.luau` (new), `src/server/Services/RatingService.luau` (new)
- `src/server/ArenaGreybox.luau` (new; builds a stage if `workspace.PoseOffArena` is missing)
- `src/client/Controllers/PoseOffController.luau` (new)

**Config: `PoseOff.luau`**
```lua
return {
	MinPlayers = 2, MaxPlayers = 4,
	QueueCountdown = 10, BotFillAfter = 30,
	Rounds = 3,
	PromptTime = 2, PoseTime = 5, ShowcaseTimePer = 2, VoteTime = 5,
	FinaleTime = 4, ResultsTime = 5,
	MeterPeriod = 1.2,               -- power meter sweeps faster than training bar
	Score = { TimingMax = 40, PromptMatch = 20, CrowdMax = 40 },
	NpcCrowdVotes = 10,              -- used when fewer than 2 real spectators
	Rewards = {
		Drip = { 30, 15, 5, 5 },             -- by placement
		AuraSurgeSeconds = { 180, 60, 0, 0 }, -- seconds of the player's estimated Aura rate
		VoterDripPerCorrectRound = 2,
	},
	SameOpponentLimitPerHour = 3,    -- after this, rewards vs that opponent drop to 0
	AfkRoundsToForfeit = 2,
}
```
`Prompts.luau`: list of `{ text = "SHOW THE JAWLINE", tag = "jawline" }`, `"MAXIMUM AURA"→aura`,
`"BE UNBOTHERED"→unbothered`, `"FLEX ON THEM"→flex`, `"CLASSIC GYM BRO"→classic`, `"DRIP CHECK"→drip`.

**Arena (ArenaGreybox):** `Model PoseOffArena` near spawn with: `Stage` part, `Pedestal1..4`
(attachments where contestants are teleported, facing the bleachers), `QueuePad` (glowing neon part
with a BillboardGui "POSE-OFF: n/4"), `Bleachers` area, `SpotlightN` SpotLights per pedestal.

**State machine (server, one match at a time per server)**
```
Idle ──(queue ≥ MinPlayers)──► Countdown(10s; more can join up to Max)
   └─(1 queued for BotFillAfter s)──► add bot ──► Countdown
Countdown ──► Walkout (teleport to pedestals, freeze, 2s spotlight each)
Walkout ──► Round r = 1..3:
   Prompt(2s)  → broadcast prompt text
   Pose(5s)    → contestants send PoseOffSubmit(poseId, meterTapServerTime) once
   Showcase(2s × n) → PoseService:Perform for each in turn, camera hint to clients
   Vote(5s)    → spectators send PoseOffVote(contestantId) once per round
   Score round
Finale(4s) → winner performs The Mog (or best owned pose); "aura drain" VFX from losers to winner
Results(5s) → rewards, rating, results card ──► Idle (teleport contestants back to arena floor)
```
Contestants who leave mid-match forfeit (placed last, no rewards). Spectators = all players not
contesting who are within ~80 studs of the arena (or everyone, simpler — pick everyone).

**Scoring per round (max 100)**
- Timing: `TimingMax × (1 − |meterPos − 0.5| / 0.5)` using `Formula.MarkerPosition` with
  `MeterPeriod` (add an optional `period` argument to `Formula.MarkerPosition`). No submit = 0.
- Prompt match: `PromptMatch` if the pose's `tags` contain the round's prompt `tag`.
- Crowd: `CrowdMax × votesForYou / totalVotes`. If fewer than 2 real voters, generate
  `NpcCrowdVotes` virtual votes weighted by each contestant's (timing + prompt) score.
- Contestants cannot vote. Spectators get one vote per round; votes are validated server-side.
- Voter reward: `VoterDripPerCorrectRound` Drip when their vote matches the round's top scorer.

**Bots:** `Players:CreateHumanoidModelFromDescription(HumanoidDescription.new(), Enum.HumanoidRigType.R15)`
named "Gym Bro Bot", placed on a pedestal; picks a random pose matching the prompt 50% of the time;
timing score random in 12–34. Bots get no rewards and are excluded from Rating.

**Rating (RatingService)**
- `data.mogRating = 1000`, `data.season = { id = 1, rating = 1000, bestTier = "Bronze" }`.
- Multiplayer Elo: for each pair (i, j), expected `E = 1 / (1 + 10^((Rj − Ri)/400))`, actual 1/0.5/0
  by placement, `ΔRi += K × (S − E) / (n − 1)` with `K = 32`. Apply to `season.rating` too.
- Tiers: Bronze Bro < 1100 ≤ Silver Sigma < 1250 ≤ Gold Goat < 1400 ≤ Diamond Mogger < 1600 ≤ Cosmic Legend.
- Tier badge: BillboardGui over each player's head (server-created, updated on change).

**Rewards** via `EconomyService:AddDrip` (create a minimal `EconomyService` now with `AddDrip`
that updates `data.dripTokens` and syncs; M9 expands it). Aura surge = `seconds ×
estimatedRatePerSecond(player)` where the estimate = best unlocked machine base × stage multiplier ×
reset multiplier × 1 rep/s (put this helper in `Formula`). Track `stats.poseOffsPlayed`,
`stats.poseOffWins`; call `PoseService:RefreshUnlocks` after wins.

**Anti-farm:** per-player table of opponent userId → timestamps in the last hour; if a pair has met
≥ `SameOpponentLimitPerHour` times, both get 0 Drip/Aura (rating still moves). AFK
(no submit for `AfkRoundsToForfeit` rounds) = no rewards + 60 s queue cooldown.

**Remotes**
- C→S: `PoseOffJoinQueue()`, `PoseOffLeaveQueue()`, `PoseOffSubmit(poseId, tapTime)`, `PoseOffVote(userId)`
- S→C (FireAllClients): `PoseOffState(stateTable)` where `stateTable = { phase, endsAt (server time),
  round, prompt, contestants = { {userId, name, isBot} }, roundScores?, results? }`

**Client UI**
- Queue pad billboard shows count. In queue: small "In queue (2/4) — LEAVE" pill.
- Contestant: prompt banner, countdown, pose picker (their wheel), power meter (tap once), "LOCKED"
  after submit.
- Spectator: 🔥 vote buttons with contestant names during Vote; "+2 Drip" pop when correct.
- Results card: placement, score per round, rating Δ, Drip, **QUEUE AGAIN** button.

**Acceptance**
- [ ] 2-player local server test: both queue → countdown → 3 rounds → results; rewards correct.
- [ ] Solo test: after 30 s a bot joins; NPC crowd votes produce a sensible winner.
- [ ] Spectator (3rd test client) can vote once per round; correct votes give Drip.
- [ ] A contestant leaving mid-match doesn't break the match; they get last place.
- [ ] Sending forged `PoseOffSubmit` twice or for an unowned pose is ignored.
- [ ] Rating changes and tier badge updates; rating persists after rejoin.

**Prompt**
> Implement milestone M5 from BUILD_SPEC.md: PoseOff + Prompts config, ArenaGreybox,
> PoseOffService state machine, RatingService, minimal EconomyService.AddDrip, bots, NPC crowd,
> anti-farm, remotes and PoseOffController UI. Extend Formula.MarkerPosition with an optional
> period argument and add an estimatedRatePerSecond helper. Follow CLAUDE.md. Then give me a
> Studio test plan using Start Server with 3 players.

---

## M6 — Boosts + hourly "Mog the Titan" event

**Goal:** a single place that computes Aura boosts, and the hourly server-wide co-op event.

**Files:** `src/shared/Config/Titan.luau`, `src/server/Services/BoostService.luau`,
`src/server/Services/TitanService.luau`, `src/server/TitanGreybox.luau`,
`src/client/Controllers/TitanController.luau`

**BoostService**
- `BoostService:GetMultiplier(player)` = product of: personal 2x (if `data.boosts.aura2xUntil >
  os.time()`), server boost (`workspace:GetAttribute("ServerAuraBoostUntil")`), spotter (M7),
  VIP (M10). **TrainingService must pass this as `boostMultiplier`** in `Formula.AuraPerRep`.
- `BoostService:GrantPersonal(player, seconds)` extends from max(now, current end).
- `BoostService:GrantServer(seconds)` sets the workspace attribute.
- HUD shows active boosts with countdown chips (top-left).

**Titan config**
```lua
return {
	IntervalMinutes = 60, FirstEventMinutes = 15, -- first one sooner so new servers see it
	WarningSeconds = 60, ArrivalSeconds = 10, SyncSeconds = 90, MogSeconds = 10,
	SyncGoalPerPlayer = 25, -- Perfects needed per participating player
	SyncMeterPeriod = 1.4,
	Reward = { BaseDrip = 20, DripPerHit = 2, MaxHitsCounted = 40, ServerBoostSeconds = 900 },
	Skins = { "ClassicGymBro" }, -- weekly rotation; meme-swap pipeline adds entries here
}
```

**Flow:** `TitanGreybox` builds `workspace.TitanPlaza` (big circle + clock billboard visible from
spawn). `TitanService` schedules by `os.clock()` per server: Warning (siren, HUD countdown, arrow)
→ Arrival (Titan model, a big R15 rig scaled ×8 or a placeholder model from
`ServerStorage.TitanSkins.<Skin>`, lands with camera shake) → Sync (players within the plaza get a
timing bar; each Perfect = +1 to server meter; goal = `SyncGoalPerPlayer × participants`) → Mog
(if goal reached: everyone performs The Mog/their best pose, Titan shrinks ×0.1 and runs away;
if not reached: Titan laughs and leaves, smaller reward) → rewards: Drip by contribution, server boost.
- Remotes: `TitanState(state)` broadcast; `TitanSyncHit(tapTime)` C→S (validated like reps,
  cooldown 0.6 s).
- Developer product hook for later (M10): `TitanService:SummonNow(byPlayer)` — starts Warning
  immediately if no event within the next 10 minutes or currently running; announces buyer's name.

**Acceptance**
- [ ] With `FirstEventMinutes = 1` (test), the event runs end-to-end solo and with 2 players.
- [ ] Meter scales with participants; rewards scale with contribution; boost applies to reps.
- [ ] HUD countdown to next Titan is always visible; boost chip shows remaining time.

**Prompt**
> Implement milestone M6 from BUILD_SPEC.md (BoostService wired into TrainingService, Titan config,
> TitanGreybox, TitanService with SummonNow, TitanController with countdown + sync bar, boost chips
> in HUD). Follow CLAUDE.md.

---

## M7 — Retention systems

**Files:** `Config/Quests.luau`, `Config/Streak.luau`, `Services/QuestService.luau`,
`Services/StreakService.luau`, `Services/SpotterService.luau`, `Services/OfflineService.luau`,
`Controllers/DailyController.luau`

**Daily streak (Protein Shake)**
- Data: `streak = { count = 0, lastClaimDay = 0, freezesLeft = 1, freezeWeek = 0 }`.
- `day = math.floor(os.time() / 86400)` (UTC). Claimable if `day > lastClaimDay`.
  If `day == lastClaimDay + 1` → count+1. If `day == lastClaimDay + 2` and `freezesLeft > 0` →
  consume freeze, count+1. Otherwise count = 1. Freezes refill to 1 when the ISO week changes.
- Rewards (Config): day 1–6 Drip 10/15/20/25/30/40, day 7 exclusive cosmetic id `shake_chain` + 60 Drip,
  then loop with day 7 reward becoming 100 Drip.
- Panel pops automatically on join if claimable (after the FTUE, i.e. only if `bestStage ≥ 3`).

**Daily quests (3)**
- Config pool: `{ id, kind, target, drip }` with kinds `reps`, `perfects`, `poseOffWins`,
  `poseOffsPlayed`, `votes`, `titanHits`, `stageUps`. Example: `{ id="perfects50", kind="perfects", target=50, drip=25 }`.
- Pick 3 per day with a deterministic RNG `Random.new(userId * 1000 + day)`, no duplicate kinds.
- Data: `quests = { day = 0, list = { {id, progress, claimed} }, rerollsLeft = 1 }`.
- `QuestService:Progress(player, kind, amount)` — called by Training (reps/perfects), PoseOff, Titan.
- One free reroll per day.

**Spotter bonus**
- Every 2 s, for each training player, if another *training* player is within 12 studs: ×1.2; if
  that player is a friend: ×1.3 (cache `player:IsFriendsWith(other.UserId)` results in a table;
  it yields, so do it in `task.spawn` on join for each pair). Feeds `BoostService` as
  `SpotterMultiplier`. Show "SPOTTER +20%" chip.

**Offline Aura (Gym Membership)**
- Data: `offline = { lastSeen = 0 }`, saved on leave/autosave.
- On load: `elapsed = min(os.time() − lastSeen, capHours × 3600)`, cap 8 h (24 h with M10 pass).
  `aura = elapsed × 0.10 × estimatedRatePerSecond(player)`. Only if elapsed ≥ 5 min.
- Show "Your Gym Membership earned +X Aura while you were away" with a CLAIM button
  (grant on claim via `EvolutionService:AddAura`).

**Acceptance**
- [ ] Streak: simulate days by temporarily offsetting `day` via a Studio-only debug attribute.
- [ ] Quests progress live, claim once, reroll once, reset next day.
- [ ] Two players training side by side both show the spotter chip and earn more.
- [ ] Rejoin after waiting ≥ 5 min (or with a debug offset) shows offline claim.

**Prompt**
> Implement milestone M7 from BUILD_SPEC.md (streak with freeze, daily quests with deterministic
> picks and reroll, SpotterService feeding BoostService, OfflineService with claim UI,
> DailyController panel). Add a Studio-only debug day offset. Follow CLAUDE.md.

---

## M8 — Glow Shard perk tree

**Config `Perks.luau`:** `{ id, name, cost, maxLevel, effect }`:
- `perfectWindow` — +5% gold zone width per level, max 3, cost 20/40/80
- `quickStart` — start each Glow Reset cycle at Gym Rat, max 1, cost 50
- `extraQuest` — +1 daily quest, max 1, cost 60
- `offlineBoost` — +5% offline rate per level, max 3, cost 25/50/100
- `trailGlow` — cosmetic aura trail, max 1, cost 30

Data: `perks = { [id] = level }`. `RequestBuyPerk(id)`; server checks cost/max. Effects are read
where relevant (`Formula.GoldHalfWidth(lockedIn, perkLevel)`, Glow Reset, QuestService, OfflineService).
UI: Perk Tree panel opened from a 🌟 HUD button (visible after first Glow Reset).

**Acceptance:** buying deducts shards once; effects apply immediately and persist; can't exceed max.

**Prompt**
> Implement milestone M8 from BUILD_SPEC.md (Perks config, RequestBuyPerk, effects wired into
> Formula/EvolutionService/QuestService/OfflineService, perk tree UI). Follow CLAUDE.md.

---

## M9 — Drip Shop + cosmetics

**Config `Cosmetics.luau`:** `{ id, name, slot, price, source }` with slots `glasses`, `chain`,
`auraColor`, `entrance`, `trail`. `source`: `shop` | `streak` | `season` | `event` | `product`.
Launch catalog: 4 glasses, 4 chains, 6 aura colours, 3 entrances, 2 trails (~19 items).

- Data: `ownedCosmetics = {}`, `equipped = { glasses, chain, auraColor, entrance, trail }`.
- `EconomyService`: `AddDrip(player, n, source)`, `SpendDrip(player, n, sink) -> bool`.
- `CosmeticService:Apply(player)` on spawn/equip: glasses replace stage shades when equipped;
  `auraColor` overrides the stage colour; entrances used by Pose-Off walkout.
- Placeholder art: simple coloured Parts/ParticleEmitters until real meshes exist; keep ids stable.
- Shop UI: world shop counter (ProximityPrompt) + HUD bag button; tabs per slot; preview on avatar.

**Acceptance:** buy/equip/unequip; Drip deducted once; visible to others; persists.

**Prompt**
> Implement milestone M9 from BUILD_SPEC.md (Cosmetics config, EconomyService Add/Spend,
> CosmeticService, Drip Shop UI with preview). Follow CLAUDE.md.

---

## M10 — Monetization

**Config `Products.luau`** (fill ids after creating them in Creator Hub → your experience →
Monetization; keep 0 until then and skip prompts for id 0):
```lua
return {
	GamePasses = {
		VIP          = { id = 0, price = 199, perks = { auraMult = 1.10, extraQuest = 1, lounge = true } },
		AutoTrain    = { id = 0, price = 249 },
		DoubleDrip   = { id = 0, price = 299 },
		Spotlight    = { id = 0, price = 149 },
		BigMembership= { id = 0, price = 99, offlineCapHours = 24 },
	},
	Products = {
		Aura2x15m    = { id = 0, price = 39,  grant = { kind = "auraBoost", seconds = 900 } },
		Aura2x1h     = { id = 0, price = 99,  grant = { kind = "auraBoost", seconds = 3600 } },
		SummonTitan  = { id = 0, price = 199, grant = { kind = "summonTitan" } },
		DripSmall    = { id = 0, price = 49,  grant = { kind = "drip", amount = 300 } },
		DripMedium   = { id = 0, price = 149, grant = { kind = "drip", amount = 1000 } },
		DripLarge    = { id = 0, price = 399, grant = { kind = "drip", amount = 3000 } },
		PosePack     = { id = 0, price = 99,  grant = { kind = "pose", poseId = "MainCharacter" } },
	},
	FirstShopPromptStage = 3, -- never show purchase prompts before Chad
}
```
**ShopService**
- Cache gamepass ownership on join with `MarketplaceService:UserOwnsGamePassAsync` (pcall) and on
  `PromptGamePassPurchaseFinished`. Expose `ShopService:HasPass(player, name)`.
- One `MarketplaceService.ProcessReceipt` handler: data not loaded → `NotProcessedYet`;
  `data.purchases[PurchaseId]` exists → `PurchaseGranted`; else grant by `grant.kind`, record id
  (keep only last 100 ids), return `PurchaseGranted`. Any error → `NotProcessedYet`.
- AutoTrain: while training with no tap for 3 s, server auto-reps every 1.2 s at quality "Good" ×0.5
  (never Perfect, never combo). Toggle in HUD.
- VIP: `BoostService` multiplier 1.10, gold name tag, VIP lounge door (`workspace.VIPDoor`
  CanCollide false only for VIPs via client-side collision group or server teleport check).
- Store UI: HUD 🛒 button (hidden until `bestStage ≥ FirstShopPromptStage`).
- Rewarded video ads: **later**, once eligible (2,000+ monthly visitors, 13+ only). Check Roblox
  Creator Docs for the current rewarded-ad API; reward = 10 min 2x Aura; never tied to a feed.

**Acceptance (Studio test purchases are free)**
- [ ] Each product grants exactly once even if ProcessReceipt is called twice.
- [ ] Passes apply after purchase without rejoin; persist after rejoin.
- [ ] No purchase UI visible before Chad.
- [ ] Summon Titan triggers the event and announces the buyer.

**Prompt**
> Implement milestone M10 from BUILD_SPEC.md (Products config, ShopService with cached passes and
> idempotent ProcessReceipt, AutoTrain, VIP effects, store UI gated by stage). Follow CLAUDE.md and
> the monetization guardrails.

---

## M11 — First-time experience, mobile polish, real map

**FTUE script (TutorialController + `data.tutorialStep`)**
| Step | Trigger to advance | Guidance |
|---|---|---|
| 1 | spawn | Camera faces Dumbbells; beam/arrow to them; "TAP TO LIFT" |
| 2 | first rep | "Tap when the marker is on GOLD!" |
| 3 | first Perfect | Big extra celebration |
| 4 | reach Gym Rat | (cutscene) then arrow to Bench |
| 5 | first pose | POSE button pulses: "Show off your new pose!" |
| 6 | ~2–4 min or Chad | Spotlight beam from arena: "Try your first Pose-Off!" (first match tuned winnable: bot timing 8–20) |
| 7 | reach Chad | Show daily quests + streak; Titan countdown highlighted |
Skip all steps for returning players with `bestStage ≥ 3`.

**Mobile/perf checklist**
- Test in Studio Device emulator: iPhone SE, mid Android, tablet. Nothing overlaps the jump/thumbstick.
- All buttons ≥ 44 px; text readable at SE size.
- Part count for the map < ~5k; use StreamingEnabled; ParticleEmitter rates modest.

**Real map:** replace greybox with the zones from GDD §3 (Starter Gym, Iron Yard, Mog Mansion,
Cosmic Dojo, Arena, Titan Plaza, Drip Shop, Hall of Mog). Tag equipment `Equipment` + attribute
`EquipmentId`; Greybox auto-disables. Zone gates: invisible walls with billboard "Unlocks at X",
server-checked (`bestStage`).

**Hall of Mog leaderboards:** `OrderedDataStore`s for weekly Aura and season rating, refreshed every
5 min, shown on SurfaceGuis (top 10).

**Prompt**
> Implement milestone M11 from BUILD_SPEC.md (TutorialController with the step table, data.tutorialStep,
> zone gates, Hall of Mog OrderedDataStore boards, mobile layout fixes). Follow CLAUDE.md. Tell me
> exactly how to tag my own built equipment so Greybox switches off.

---

## M12 — Analytics

Use Roblox's built-in `AnalyticsService` (results appear in Creator Hub → Analytics).
- **Onboarding funnel** (`LogOnboardingFunnelStepEvent`): 1 Spawned, 2 FirstRep, 3 FirstPerfect,
  4 GymRat, 5 OpenedPoseWheel, 6 FirstPoseOff, 7 Chad, 8 SawTitan, 9 Sigma.
- **Economy** (`LogEconomyEvent`): every Drip/Glow Shard source and sink (via EconomyService only).
- **Custom events**: PoseOffJoined, PoseOffCompleted(placement), TitanParticipated(hits),
  GlowReset(number), ShopOpened, PurchasePrompted(product).
- `AnalyticsService` wrapper `src/server/Services/AnalyticsService.luau` (name it `Telemetry` to
  avoid clashing with the Roblox service name) so call sites are one line.

**KPIs to watch** (GDD §16): first-play bounce, D1 ~20%+, session 10+ min, **% of players who
enter a Pose-Off** (the key metric), D7/D28.

**Prompt**
> Implement milestone M12 from BUILD_SPEC.md: a Telemetry service wrapping Roblox AnalyticsService
> (funnel, economy, custom events) and wire every listed event. Follow CLAUDE.md.

---

## M13 — ProfileStore + anti-exploit hardening

- Replace DataService internals with **ProfileStore** (session locking, safe across servers).
  Keep the public API (`Get`, `IsLoaded`, `OnLoaded`) so no other service changes.
  Key format stays `player_<UserId>`; write a one-time migration from `PlayerData_v1` if any real
  players exist.
- Rate-limit **every** remote with a shared `RateLimiter.allow(player, remoteName, perSecond)`.
- Validate argument types on every remote (helper `Validate.number/str/oneOf`).
- Log (don't auto-ban) anomalies: perfect ratio > 95% over 200 reps, Aura gain/min > 3× the
  theoretical max for their stage, impossible teleports during training.
- Server-side sanity: training requires the character within `TrainRange` every 5 s (stop otherwise).

**Prompt**
> Implement milestone M13 from BUILD_SPEC.md: migrate DataService to ProfileStore behind the same API,
> add RateLimiter + Validate helpers to every remote, and the anomaly logging. Follow CLAUDE.md.

---

## M14 — Launch prep (mostly human tasks)

- [ ] Search Roblox for "glow up gym", "aura gym", "mog", "pose off"; note competitors.
- [ ] Final title (test: *Sigma Glow-Up Gym* / *+1 Aura Every Rep* / *Mog Gym*).
- [ ] 3 icons + 3 thumbnails (GDD §14); A/B test icons with Roblox's thumbnail/icon testing if available.
- [ ] Content maturity questionnaire (target Minimal/Mild).
- [ ] Description with keywords; social links; Discord/YouTube.
- [ ] Private playtest with 5–10 players; fix top issues.
- [ ] Soft launch: ads ~$10–20/day for 3–5 days; check D1, session length, Pose-Off %.
- [ ] Record 5+ clips (transformation, Pose-Off loss by 1 vote, server Titan mog) → Shorts/TikTok.

---

## Live-ops weekly template (after launch)

Every week, same day/time (e.g. Saturday 10:00 ET), with a HUD countdown all week:
1. **Content:** 1 new pose pack (2 earnable + 1 premium) *or* 1 new stage/equipment.
2. **Titan skin swap:** add a skin to `Titan.Skins` inspired by the week's trending meme (original
   design, not a copied character).
3. **Season:** Monday rating soft reset (`rating = 1000 + (rating − 1000) × 0.5`) + tier rewards.
4. **Balance pass:** read Telemetry; adjust Config only.
5. **Changelog** in-game board + clips.

**Prompt template**
> Weekly update: add pose pack "<name>" with poses <A,B,C> (tags ...), add Titan skin "<Skin>",
> and bump the season id. Only touch Config and assets unless a system change is needed. Follow CLAUDE.md.
