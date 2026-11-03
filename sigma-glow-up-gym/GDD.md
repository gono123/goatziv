# Sigma Glow-Up Gym — Game Design Document

*Version 0.1 · Working title · Roblox · November 2026*

---

## 1. Overview

**One-line pitch:** Train at the gym, farm Aura, evolve through ridiculous glow-up transformations, then step on stage and *mog* other players in crowd-judged Pose-Offs.

| | |
|---|---|
| **Genre** | Training simulator + social party competition (meme/brainrot skin) |
| **Platform** | Roblox, mobile-first (≈ most players on phones), also PC/console |
| **Target audience** | Core 9–15; works for 16+ through Pose-Off competition and rating |
| **Session length** | 10–25 minutes, with hourly server event as a "stay a bit longer" anchor |
| **Server size** | 24 players (enough for a live audience at Pose-Offs, not too crowded on mobile) |
| **Content maturity** | Aim for *Minimal / Mild* (cartoon, no violence, no gambling) |

### Why this game, why now
- **Meme fuel:** "aura," "mog," "sigma," "glow-up," "locked in" and "winter arc" are core Gen Alpha / Gen Z slang. The game turns that language into mechanics instead of just pasting a meme character in.
- **Proven base, new hook:** training sims are a proven Roblox loop (numbers go up, visible body change), but the genre is saturated. The **Pose-Off** (crowd-judged, chat-free competition) and **transformation cutscenes** are the differentiators and the clip machines.
- **Fits the 2026 algorithm:** Roblox's Recommended-for-You now weighs 28-day retention, first-play bounce and play-through. The design front-loads a transformation in under 90 seconds (low bounce) and uses streaks, weekly seasons and hourly events for D2–D28 return.
- **Chat-restricted world:** age-gated chat means many kids can't type to each other. Pose-Offs, voting and emotes create social play with zero chat needed.
- **Original IP:** all characters, poses, the Titan and branding are ours, so no licensing disputes and full ownership if it grows.

### Design pillars
1. **Every rep feels juicy.** Big numbers, screen shake, "PERFECT" pops, Aura flying into your bar.
2. **Your body is the flex.** Progress is visible on your avatar, not hidden in a menu.
3. **Being watched is the point.** Pose-Offs and the Titan event turn solo grinding into a show.
4. **Absurd, never mean.** Comedy exaggeration (jawlines, cosmic glow), never real body-shaming or diet messaging.

---

## 2. Core Loops

### Moment-to-moment (seconds)
```
Tap on the timing bar → rep lands (Perfect / Good / Miss) → Aura flies into bar → combo grows
```

### Session loop (minutes)
```
Train → Aura bar fills → TRANSFORMATION cutscene → unlock new equipment + pose
   ↑                                                         ↓
   └──── Pose-Off (win Drip + Rating) ←── Titan event every hour
```

### Meta loop (days/weeks)
```
Reach Gigasigma → GLOW RESET (keep permanent multiplier + Glow Shards)
→ climb faster → higher Mog Rating tier → weekly season rewards → new stage / pose pack each week
```

---

## 3. World & Map

One compact map (fast to load on low-end phones), split into zones that unlock with your stage:

| Zone | Unlocked at | Contents |
|---|---|---|
| **Starter Gym** | Noob | Dumbbells, bench, mirror wall (shows your current stage), tutorial arrows |
| **Iron Yard** | Chad | Squat racks, tire flips, outdoor scaffolding; parkour shortcut to the arena |
| **Mog Mansion** | Gigasigma | Meteor Press, gold mirrors, VIP lounge (gamepass) |
| **Cosmic Dojo** | Cosmic Mogger / Glow Reset 3 | Black Hole Bench, floating platforms, galaxy skybox |
| **Pose-Off Arena** | Always open | Stage with 4 pedestals, spotlight rig, audience bleachers with vote buttons |
| **Titan Plaza** | Always open | Where the Titan lands each hour; giant countdown clock visible from everywhere |
| **Drip Shop** | Always open | Cosmetics (sunglasses, chains, aura colors, entrances) |
| **Hall of Mog** | Always open | Leaderboard walls: top Aura, top Rating, top Titan damage this week |

**Map rule:** from spawn you can *see* the Arena spotlights and Titan clock. It shows players what's coming and pulls them in.

---

## 4. Progression

### 4.1 Currencies
| Currency | Earned by | Used for | Buyable with Robux? |
|---|---|---|---|
| **Aura** | Training reps, events | Reaching stages (not spent; it's a progress total) | Only indirectly through timed boosts |
| **Drip Tokens** | Pose-Offs, voting, Titan, quests, streak | Cosmetics, pose packs | Yes (packs) |
| **Glow Shards** | Glow Reset | Prestige cosmetics + permanent perk tree | **No** |
| **Mog Rating** | Pose-Offs | Rank tier and season rewards | **No** |

### 4.2 Evolution stages

Starting numbers. Tune after playtests. Rate assumes about 40 reps a minute with an average quality multiplier of 1.4.

| # | Stage | Aura needed (this cycle) | Stage multiplier | Unlocks | Target time to reach |
|---|---|---|---|---|---|
| 0 | **Noob** | 0 | ×1 | Dumbbells, Pose: *Lil Flex* | — |
| 1 | **Gym Rat** | 75 | ×1.5 | Bench, Pose-Offs, pose wheel | **< 90 seconds** |
| 2 | **Chad** | 1,000 | ×2.5 | Squat Rack, Iron Yard | ~5 min |
| 3 | **Sigma** | 30,000 | ×4 | Tire Flip, signature sunglasses | ~25 min (end of session 1) |
| 4 | **Gigasigma** | 500,000 | ×6 | Meteor Press, Mog Mansion, **Glow Reset** | Session 2–3 |
| 5 | **Cosmic Mogger** | 10,000,000 | ×10 | Black Hole Bench, galaxy aura | Day 4–7 |
| 6+ | *Added weekly in live-ops* | | | | |

### 4.3 Equipment

| Equipment | Unlock stage | Aura per rep (base) |
|---|---|---|
| Dumbbells | Noob | 1 |
| Bench | Gym Rat | 3 |
| Squat Rack | Chad | 10 |
| Tire Flip | Sigma | 30 |
| Meteor Press | Gigasigma | 100 |
| Black Hole Bench | Cosmic / Glow Reset 3 | 400 |

### 4.4 Aura formula
```
AuraPerRep = EquipmentBase
           × StageMultiplier
           × QualityMultiplier        (Perfect 2.0 · Good 1.0 · Miss 0.25)
           × (1 + 0.5 × GlowResets)   (permanent, additive)
           × ComboBonus               (1.0 → 1.5 at 20+ Perfect streak = "LOCKED IN")
           × Boosts                   (2x potion, Titan reward, spotter +20%, VIP +10%)
```

### 4.5 Glow Reset (rebirth)
- Available at **Gigasigma**. Resets stage and Aura to Noob.
- Keeps: Drip Tokens, cosmetics, poses, Rating, equipment *visual skins*.
- Gives: **+50% permanent Aura** (additive per reset) and **Glow Shards** (10 + 5 × reset number).
- **Glow Shard perk tree** (small permanent perks): faster timing bar recovery, +1 daily quest, Perfect window +5%, start each cycle at Gym Rat, exclusive aura trails.
- Reset cutscene: avatar deflates, then glows white. "The glow-up never ends."

### 4.6 Avatar transformation (the visible flex)
- Scale the R15 body per stage through Humanoid scale values (BodyWidthScale, BodyHeightScale, BodyDepthScale, HeadScale), roughly width 1.0 → 1.75 and height 1.0 → 1.25 by Cosmic.
  - **Verify in Studio** how far scripted scaling goes beyond avatar-editor limits. Fallback: a "muscle suit" layered accessory per stage.
- Stage accessories that stack: sweatband → chain → signature sunglasses → jawline glow → cosmic aura particles.
- **Original character design only.** Do not use the real "Gigachad" photo or anyone's real likeness.

---

## 5. Training (rep mini-game)

- Walk up to equipment → ProximityPrompt → your character snaps into the lift animation.
- **Timing bar:** a marker sweeps across a bar about every 1.5 seconds. **Tap anywhere** (mobile-friendly) when it's in:
  - **Gold zone** (narrow) = **PERFECT**: screen shake, "PERFECT!" pop, 2x Aura.
  - **Green zone** = **GOOD**: 1x.
  - Outside = **MISS**: 0.25x, plus a small funny grunt sound.
- **Combo:** consecutive Perfects build a combo. At 20+, you enter **LOCKED IN** mode: phonk-style beat kicks in, eyes glow, 1.5x Aura, and the gold zone widens slightly so the mode feels powerful.
- **Fatigue (light):** after about 3 minutes on one machine, a "Switch it up!" hint suggests a different machine for +10%. It keeps players moving and seeing the map.
- **Auto-Train (gamepass):** trains at 50% efficiency without input, so players can idle. It never earns Perfects or combos, so active play always wins.

---

## 6. Poses

### 6.1 Launch set (8 poses, all original names)
| Pose | How you get it | Vibe |
|---|---|---|
| Lil Flex | Start | Tiny single-arm flex |
| The Double Bi | Gym Rat | Classic double biceps |
| Side Eye | Chad | Slow head turn, unbothered stare |
| Locked In | Sigma | Hands steepled, eyes narrow, camera zoom |
| Mewing Moment | Pose-Off win #3 | Finger to lips, jaw tightens |
| Main Character | Drip Shop | Hair flip, wind machine effect |
| Cosmic Lat Spread | Gigasigma | Lats spread into wings of light |
| The Mog | 10 Pose-Off wins | Points at camera, everyone behind you shrinks |

- **Pose wheel:** radial menu with 8 slots, usable anywhere as an emote (social expression without chat).
- **New pose pack each week** in live-ops: 2 earnable, 1 premium.

---

## 7. Pose-Off (the signature mode)

### 7.1 Flow
1. **Queue:** step on a glowing pad at the arena. The match starts when 2–4 players are queued (10-second countdown).
   - **Low-population fill:** if fewer than 2 players have queued after 30 seconds, an NPC "Gym Bro" bot joins so nobody waits forever.
2. **Walk-out:** each contestant gets a 2-second spotlight entrance. Premium entrances are cosmetic.
3. **Three rounds,** about 20 seconds each:
   | Phase | Time | What happens |
   |---|---|---|
   | Prompt | 2 s | Big text: e.g. **"SHOW THE JAWLINE"**, **"MAXIMUM AURA"**, **"BE UNBOTHERED"** |
   | Pose | 5 s | Pick a pose from your wheel (+bonus if it matches the prompt's tag) **and** stop a power meter in the gold zone |
   | Showcase | 2 s each | Spotlight and camera orbit each contestant in their pose |
   | Crowd vote | 5 s | Audience taps 🔥 on their favorite. Contestants can't vote for themselves. |
4. **Final:** the winner does **The Mog**. A VFX "aura drain" pulls glowing particles from the losers into the winner. It's visual only; nobody actually loses currency.
5. **Results card:** placement, Rating change, Drip earned, and a button to re-queue instantly.

### 7.2 Scoring (per round, max 100)
- **Timing:** up to 40 (power meter accuracy)
- **Prompt match:** 20 if the pose's tag fits the prompt
- **Crowd:** up to 40 (your share of the audience votes × 40)
- **No audience?** An NPC crowd votes based on timing + equipped Drip, so solo servers still work.

### 7.3 Rewards
| Placement | Drip Tokens | Aura Surge | Rating |
|---|---|---|---|
| 1st | 30 | 3 min of your normal earning rate, instantly | + (Elo-lite) |
| 2nd | 15 | 1 min | ± |
| 3rd–4th | 5 | — | − (small) |
| **Audience voter** | +2 per round if you voted for the round's winner | — | — |

Voter rewards are important: they give non-competing players a reason to sit in the bleachers and watch, which makes Pose-Offs feel like a show.

### 7.4 Mog Rating & tiers
- Starts at 1,000. Elo-lite: beating higher-rated players gives more.
- Tiers: **Bronze Bro → Silver Sigma → Gold Goat → Diamond Mogger → Cosmic Legend.**
- Tier badge floats over your head everywhere in the game.
- **Weekly season:** soft reset toward 1,000. End-of-season rewards are a tier-colored aura and an exclusive pose for Diamond and above.

### 7.5 Fairness & anti-farming
- Pose-Off rewards **never depend on Robux**. Boosts don't affect Pose-Off scoring.
- Rewards against the same opponent drop after 3 matches per hour (stops alt farming).
- AFK contestants (no input in 2 rounds) get nothing and a queue cooldown.
- One vote per audience member per round. Vote-buttons are server-validated.

---

## 8. Hourly Server Event: Mog the Titan

**Every 60 minutes** (staggered per server based on server start) a giant gym-bro Titan stomps into Titan Plaza.

| Phase | Time | What happens |
|---|---|---|
| Warning | T-60 s | Siren, HUD countdown, ground shakes, arrow to the Plaza |
| Arrival | 10 s | Cinematic landing, Titan flexes, everyone's camera shakes |
| Pose Sync | 90 s | Prompts flash. Every player hits the timing bar together. Each Perfect fills a **server Sync Meter**. |
| The Mog | 10 s | If the meter is full, the whole server performs The Mog together and the Titan shrinks into a tiny guy and runs off crying (comedy). |
| Reward | — | Everyone gets Drip Tokens (more for higher personal contribution) + **15 minutes of 2x Aura server-wide** |

- **Weekly Titan skin rotation:** this is the **meme-swap pipeline**. When a new meme or slang word blows up, the Titan becomes it within a day (original design inspired by the trend, never a copied character).
- **"Summon Titan Now" developer product:** a player can pay to trigger the event early for the whole server. Their name gets announced and everyone benefits, which makes it a social purchase people love.

---

## 9. Social Systems

- **Spotter bonus:** training on a machine next to another player gives both +20% Aura. Friends get +30%. This pushes players together and encourages inviting friends.
- **Emote-first communication:** pose wheel, 🔥 reactions, and "GG" stickers. Everything works with chat disabled.
- **Friend invite reward:** when an invited friend reaches Chad, both get an exclusive "Gym Buddies" duo pose.
- **No trading at launch.** It invites scams, real-money trading and moderation load. Revisit after month 2 if wanted.
- **Later (week 3+):** **Gym Crews** of up to 4 players with a shared weekly crew leaderboard.

---

## 10. Retention Systems (built for D1 / D7 / D28)

| System | Detail | Targets |
|---|---|---|
| **Daily Protein Shake** | Login streak calendar; Day 7 gives an exclusive cosmetic. **1 free "missed day" per week** so a broken streak doesn't make players quit. | D1–D7 |
| **Daily Quests (3)** | e.g. "Land 50 Perfects", "Win 1 Pose-Off", "Vote in 5 rounds". Re-roll one per day free. | D1–D28 |
| **Weekly Season** | Mog Rating season + Aura leaderboard, rewards every Monday | D7–D28 |
| **Hourly Titan** | Gives "just one more" reason to stay | Session length |
| **Weekly Update** | New stage or pose pack + Titan skin every week | D7–D28 |
| **Gym Membership (offline Aura)** | Earn 10% of your rate while offline, capped at 8 hours; collect on return | D2+ |
| **Experience notifications** | Opt-in: "Your Gym Membership is full", "New Titan this week" | Returns |

---

## 11. Monetization

Prices are suggested starting points in Robux. Test and adjust.

### 11.1 Gamepasses (one-time)
| Pass | Price | Benefit |
|---|---|---|
| **VIP Gym Membership** | 199 | VIP lounge, gold name tag, +10% Aura, +1 daily quest |
| **Auto-Train** | 249 | Trains while idle at 50% efficiency |
| **2x Drip** | 299 | Double Drip Tokens from all sources |
| **Spotlight Entrance** | 149 | Choose custom Pose-Off walk-out effects |
| **Bigger Gym Membership** | 99 | Offline Aura cap 8 → 24 hours |

### 11.2 Developer products (repeatable)
| Product | Price | Benefit |
|---|---|---|
| 2x Aura (15 min) | 39 | Personal boost |
| 2x Aura (1 hour) | 99 | Personal boost |
| **Summon Titan Now** | 199 | Triggers the Titan for the whole server; buyer gets announced |
| Drip Token packs | 49 / 149 / 399 | Cosmetics currency |
| Premium pose pack | 99 | Weekly premium pose |

### 11.3 Monetization rules
- **Never sell:** stages, Mog Rating, Pose-Off advantages, or Glow Shards.
- **No paywall in the first 10 minutes.** The first shop prompt appears only after the Chad transformation.
- **No paid random items at launch.** If added later, show the odds clearly as Roblox requires.
- **Rewarded video ads:** once eligible (2,000+ monthly visitors, 13+ players only), add an optional "Watch for 10 min of 2x Aura" button. **Never** reward watching a scrolling feed. That pattern is banned for under-16 tiers after the Steal An Egg case.
- **Creator Rewards:** design so paying players stay engaged, since Roblox's payout program rewards active spenders.

---

## 12. First-Time User Experience (the first 5 minutes)

| Time | What the player sees |
|---|---|
| 0–5 s | Spawn as a skinny **Noob** facing glowing dumbbells. Big text: **"TAP TO LIFT"**. No menus, no popups. |
| 5–20 s | First reps. First Perfect gets an extra-big celebration. Aura counter flies into the bar. |
| 20–80 s | Bar to Gym Rat fills fast. "Almost there!" at 80%. |
| **~80 s** | **First TRANSFORMATION cutscene**, the hook. Avatar visibly bulks, sunglasses drop. |
| 80–120 s | Arrow to the Bench (new equipment). Pose wheel unlocks with *The Double Bi*. |
| 2–4 min | Spotlight beam from the arena + prompt: **"Try your first Pose-Off!"** (bots fill if needed; first match is tuned to be winnable). |
| ~5 min | **Chad** transformation. Daily quests and streak panel introduced. Titan countdown shown on HUD. |
| 5–10 min | First shop mention (soft, in context), Iron Yard unlocked, first quest completed. |

**Mobile UX:** tap anywhere for reps, big buttons (minimum 44 px), no text-heavy panels, and test on a low-end Android phone every build.

---

## 13. Art & Audio Direction

- **Style:** bright, chunky low-poly; exaggerated proportions; saturated gym colors (orange, teal, gold); readable at phone size.
- **VFX:** Aura particles color-shift by stage (white → blue → purple → gold → galaxy).
- **Transformation cutscene beat sheet (3 seconds):**
  1. 0.0 s: camera snaps to the face, world desaturates
  2. 0.5 s: bass drop, avatar puffs up in 2 quick steps
  3. 1.5 s: sunglasses fall from the sky onto the face (signature moment)
  4. 2.0 s: stage name slams on screen with screen shake
  5. 3.0 s: color returns, everyone nearby sees a shockwave ring
- **Audio:** use **only Roblox's licensed audio library** or original tracks. Phonk-style beats for LOCKED IN, comedic grunts for misses, crowd cheers in the arena.
- **UI:** big, bold, rounded; numbers abbreviated (1.2M, 3.4B).

---

## 14. Clip Moments & Marketing

### Built-in clip moments (design them on purpose)
1. The transformation cutscene, especially the sunglasses drop
2. The Mog finale in Pose-Offs (aura drain VFX)
3. A whole server posing together to shrink the Titan
4. LOCKED IN mode with eyes glowing and the beat dropping
5. Losing a Pose-Off by 1 vote

### Title ideas (test)
- **Sigma Glow-Up Gym**
- **+1 Aura Every Rep** (borrows the proven "+1 ___" naming pattern)
- **Mog Gym 💪**

### Icon concepts (A/B test 3)
1. Split image: skinny Noob vs Cosmic Mogger, "GLOW UP" text
2. Giant face with sunglasses mid-drop
3. Two players face to face on the Pose-Off stage, crowd behind

### Launch marketing
- **Shorts/TikTok:** post 1–2 clips a day in launch week (YouTube for under-13s, TikTok for 13+).
- Pitch clips to Roblox's official social channels and creator programs.
- **Ads:** about $10–20 a day for 3–5 days to get test traffic, then scale only if retention holds.
- **Seasonal hook:** a **"Winter Arc" event** in December. The self-improvement "winter arc" meme fits a glow-up gym perfectly.

---

## 15. Technical Design

### 15.1 Project structure (Rojo)
```
src/
  server/
    Services/
      DataService.lua        -- ProfileStore load/save, session locking
      TrainingService.lua    -- validates reps, calculates Aura
      EvolutionService.lua   -- stages, scaling, Glow Reset
      PoseOffService.lua     -- queue, rounds, scoring, voting, rating
      TitanService.lua       -- hourly event state machine
      QuestService.lua       -- daily quests + streak
      ShopService.lua        -- gamepasses, ProcessReceipt (idempotent)
      AnalyticsService.lua   -- funnel + economy events
  client/
    Controllers/
      HUDController.lua
      TrainingController.lua -- timing bar UI, tap input
      PoseWheelController.lua
      PoseOffController.lua
      CutsceneController.lua
  shared/
    Config/
      Stages.lua    Equipment.lua    Poses.lua    Prices.lua    Prompts.lua
    Remotes.lua
```
All tuning numbers live in `shared/Config`, so balance changes never touch logic.

### 15.2 Remotes
`RequestRep`, `SelectPose`, `JoinQueue`, `LeaveQueue`, `CastVote`, `ClaimStreak`, `ClaimQuest`, `RequestGlowReset`, `TitanSyncHit`

### 15.3 Server authority & anti-exploit
- The **server owns all currency and stats.** The client only sends "I tapped."
- **Rep validation:** the server knows when each timing cycle started. It computes where the marker was at receipt time, allows a latency tolerance, and decides Perfect/Good/Miss itself.
- **Rate limit:** at most 1 rep per ~0.6 seconds per player; extra requests are dropped.
- **Statistical flag:** more than 95% Perfects over 200 reps gets logged for review.
- Votes and Pose-Off scores are computed only on the server.
- `ProcessReceipt` must be idempotent: record purchase IDs in the profile before granting.

### 15.4 Save data schema
```lua
{
  version = 1,
  aura = 0,                -- current cycle
  lifetimeAura = 0,
  stage = 0,
  glowResets = 0,
  glowShards = 0,
  dripTokens = 0,
  perks = {},              -- Glow Shard perk tree
  ownedCosmetics = {},     -- [id] = true
  equipped = { glasses = nil, chain = nil, auraColor = nil, entrance = nil },
  ownedPoses = { "LilFlex" },
  poseWheel = { "LilFlex" }, -- up to 8
  mogRating = 1000,
  season = { id = 1, rating = 1000, bestTier = "Bronze" },
  streak = { count = 0, lastClaimDay = 0, freezesLeft = 1 },
  quests = { day = 0, list = {} },
  offline = { lastSeen = 0 },
  purchases = {},          -- processed receipt IDs
  stats = { reps = 0, perfects = 0, poseOffsPlayed = 0, poseOffWins = 0, titansMogged = 0 },
  firstJoin = 0,
}
```

---

## 16. Analytics & KPIs

### Funnel events (log each step)
1. Spawned
2. First rep
3. First Perfect
4. Reached Gym Rat
5. Opened pose wheel
6. Joined first Pose-Off
7. Reached Chad
8. Saw first Titan
9. Reached Sigma
10. Returned Day 2

### KPIs to watch
| Metric | Rough target (community rule of thumb, not official) |
|---|---|
| Icon click-through | Pick the best of 3 icons |
| First-play bounce (leave in < 1 min) | As low as possible; fix FTUE first if high |
| D1 retention | ~20%+ |
| Avg session length | 10+ min |
| **% of players who enter a Pose-Off** | **The key differentiator metric.** If low, the twist isn't landing. |
| D7 / D28 retention | Track weekly; this is what the algorithm now rewards |
| Payer conversion / revenue per player | Track, but don't optimize before retention |

### Economy events
Log Aura and Drip sources and sinks so inflation is visible and boosts can be tuned.

---

## 17. Build Plan (2 weeks, solo)

| Day | Build |
|---|---|
| 1 | Greybox map, 3 equipment pieces, timing-bar rep mini-game |
| 2 | ProfileStore saving, Aura, server-side rep validation |
| 3 | 6 stages, body scaling + accessories, transformation cutscene |
| 4 | Glow Reset, pacing pass using the Config tables |
| 5 | 8 poses + pose wheel |
| 6–7 | Pose-Off: queue, rounds, voting, scoring, rating, bots, results |
| 8 | Titan hourly event |
| 9 | Streak, quests, spotter bonus, offline Aura |
| 10 | Shop: gamepasses + dev products + idempotent receipts |
| 11 | FTUE polish, mobile UI, low-end phone performance |
| 12 | 3 icons, thumbnails, analytics funnel |
| 13 | Playtest with 5–10 kids/friends, bug fixes, anti-exploit checks |
| 14 | Soft launch with small ad budget, record and post clips |

---

## 18. Live-Ops Roadmap (first 8 weeks)

| Week | Update |
|---|---|
| 1 | Launch. Fix bugs daily. Post clips daily. |
| 2 | Pose Pack 1 + first Titan skin swap (trending meme) |
| 3 | **Gym Crews** + crew leaderboard |
| 4 | Season 1 ends; **"Winter Arc" December event** (limited cosmetics, double Titan) |
| 5 | New stage beyond Cosmic: **Ascended** + new equipment |
| 6 | **Duo Pose-Offs** (2v2) |
| 7 | Holiday event + Pose Pack 2 |
| 8 | Season 2 + review: double down on what the analytics say players love |

**Weekly rhythm:** new content drops on the same day and time each week (e.g. Saturday), with a countdown on the HUD all week.

---

## 19. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Training sims are saturated | Lead every icon, clip and title with Pose-Offs and transformations, not grinding. Watch the Pose-Off participation metric. |
| Slang ages fast ("sigma" may feel dated) | All names live in Config; rename stages/poses in minutes. Weekly Titan meme swap keeps it current. |
| Empty Pose-Offs in small servers | NPC bots and NPC crowd votes; voter rewards to fill bleachers |
| Exploiters | Server-authoritative reps, rate limits, statistical flags |
| Clones copying the game in weeks | Ship weekly, own the brand and characters, build community (Discord/YouTube) early |
| Body-image concerns | Keep it absurd and cartoonish (cosmic glow, comedy), no weight/diet messaging, no mocking real body types |
| Monetization backlash | No pay-to-win in Pose-Offs, no early paywalls, no paid randomness |

---

## 20. Pre-Build Checklist

- [ ] Search Roblox for "glow up gym", "aura gym", "mog", "pose off" to see what exists and how it performs
- [ ] Confirm how far Humanoid body scaling works in Studio (else use the muscle-suit fallback)
- [ ] Choose the final title after an icon/title test
- [ ] Fill in the Roblox content maturity questionnaire
- [ ] Set up Rojo + ProfileStore + Config tables before writing gameplay code
