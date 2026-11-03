# DECISIONS

Choices made where the docs left room, so they can be reviewed later.

## Tuning
- **Stage thresholds:** Gym Rat 150, Chad 8,000, Sigma 500,000, Gigasigma 6M, Cosmic Mogger 150M. Retuned for clicking and upgrades. `tests/pacing.spec.luau` assumes 3 clicks per second, buying upgrades as soon as possible, and no brainrot. It keeps Gym Rat under 90 s, Chad at 3 to 6 min and Sigma at 18 to 30 min.

## Tooling
- **Rojo upgraded to 7.7.1** (latest stable). The Studio Rojo plugin must match: `rojo plugin install` updates it.
- **Quest picks use a small built-in number generator** instead of `Random.new`. `Random` does not exist in Lune, and this way the unit tests exercise the same picks as the game.

## Save data
- **`purchases` is a list of receipt ids**, newest last, capped at 100. Roblox retries unfinished receipts, so very old ids are not needed.

## Remotes
- **`Util/Guard.connect`** wraps every client to server remote, so "data loaded, then rate limit" cannot be forgotten. Rates live in `Config/RateLimits`.

## World
- **`StreamingEnabled` and `Lighting.Technology` are set in `default.project.json`**, as well as in MapBuilder inside a `pcall`, because Roblox may not let scripts set them.
- **Gate collision groups are nested.** A part can only be in one group, so a player's group is the first gate they are locked out of, and that group also collides with every later gate.
- **The Arena and Titan Plaza are never streamed out**, so their lights and clock stay visible from spawn.
- **World smoke test:** `tests/world.spec.luau` runs the real MapBuilder against Lune's Roblox stand-in. A wrong property name fails the check without opening Studio. Client UI code does not get this check.

## Debug panel
- **"Grant any pose/cosmetic" is a single "grant all" button.** It gets you to the same testing state with less UI.

## Process
- **S2, S3 and S4 share one commit.** They changed the same boot files together, and splitting them would have left commits that do not run.

## Owner changes (2026-11-04), these override GDD, BUILD_SPEC and MASTER_PROMPT
The owner asked for three changes during Checkpoint A.

**1. Clicks only.** The timing bar, Perfect/Good/Miss, combo and LOCKED IN are gone from training. Every click is one rep, capped at 5 per second.

**2. Upgrades, bought with Aura.** `aura` is now a spendable balance, and the new `cycleAura` sets the stage, so buying never loses progress. Three upgrades: Stronger Reps, Lucky Reps, Brainrot Luck. Levels clear on Glow Reset, so the spending loop returns each cycle.

**3. Daily brainrot spin.** One free spin per UTC day, five rarities, odds always shown. Prizes last forever, one is equipped at a time, and a better prize equips itself. Duplicates pay Drip.
- **All brainrot characters are original.** CLAUDE.md forbids copyrighted meme characters.
- **Spins and brainrots are never sold.** Paid random items would need Roblox odds rules and would be pay-to-win. They also never affect Pose-Off scoring.

**What this means for later steps**
- **Pose-Off:** the power meter stays for now, because it is a separate contest. Ask the owner if it should become clicks too.
- **Titan (M6):** Sync has no Perfects any more. Count every click as a hit, with the same rate cap.
- **Quests (M7):** the `perfects` quests are removed.
- **Perks (M8):** `perfectWindow` has no meaning now. Replace it with a permanent Aura perk.
- **AutoTrain (M10):** reps at 50% value, still never as fast as clicking.
- **Anomaly logging (M13):** the "95% Perfect" flag no longer applies. Flag sustained clicking at the cap for long periods instead.
- **Tutorial (M11):** "Tap when the marker is on GOLD" and "first Perfect" steps become "click to lift" and "first upgrade".
