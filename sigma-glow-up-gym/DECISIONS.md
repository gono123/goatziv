# DECISIONS

Choices made where the docs left room, so they can be reviewed later.

## Tuning
- **Stage thresholds:** Chad 1,000 to 1,200 and Sigma 30,000 to 45,000. The pacing test (60% Perfect player) now gives about 3.5 min to Chad and about 23 min to Sigma, inside the targets in MASTER_PROMPT Part 2.

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
