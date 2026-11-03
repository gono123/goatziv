# PROGRESS

**Where things stand:** S1 done. Next: S2 (refactor + UI kit).

## How the code works (summary)
1. Rojo maps `src/shared` to `ReplicatedStorage.Shared`, `src/server` to `ServerScriptService.Server`, `src/client` to `StarterPlayerScripts.Client`.
2. Server boot (`init.server.luau`): require every service in `ORDER`, call `Init(services)` on each, build the world, then call `Start()` on each.
3. Client boot (`init.client.luau`): require controllers and call `Init`. Controllers build their own ScreenGuis.
4. Services talk through the `services` table, never by requiring each other. This avoids require cycles.
5. Remotes are declared once in `src/shared/Remotes.luau`. The server creates them, clients wait for them.
6. `DataService` owns saved data. `TEMPLATE` lists every field and `reconcile` back-fills new fields into old saves.
7. Training: a ProximityPrompt starts a session with a server timestamp. The client draws the marker from the synced clock and sends tap times. The server recomputes the marker position and decides the quality.
8. Evolution: Aura added, `CheckStage` runs, `ApplyLook` scales the R15 body, `StageUp` fires the client cutscene. Glow Reset is available from Gigasigma.
9. All tuning numbers are in `src/shared/Config/`. Pure maths is in `src/shared/Formula.luau` and `src/shared/Logic/`, and is unit tested outside Roblox with Lune.
10. Run `scripts/check.ps1` (Windows) or `scripts/check.sh` before each commit: format, lint, unit tests, Rojo build.

## Finished tasks
