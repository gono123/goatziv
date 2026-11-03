# DECISIONS

Choices made where the docs left room, so they can be reviewed later.

## Tuning
- **Stage thresholds:** Chad 1,000 to 1,200 and Sigma 30,000 to 45,000. The pacing test (60% Perfect player) now gives about 3.5 min to Chad and about 23 min to Sigma, inside the targets in MASTER_PROMPT Part 2.

## Tooling
- **Rojo upgraded to 7.7.1** (latest stable). The Studio Rojo plugin must match: `rojo plugin install` updates it.
- **Quest picks use a small built-in number generator** instead of `Random.new`. `Random` does not exist in Lune, and this way the unit tests exercise the same picks as the game.

## Save data
- **`purchases` is a list of receipt ids**, newest last, capped at 100. Roblox retries unfinished receipts, so very old ids are not needed.
