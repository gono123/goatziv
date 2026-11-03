# PROGRESS

**Where things stand:** S1 to S4 and the owner changes (clicks only, upgrades, daily brainrot spin) are done. Still waiting at CHECKPOINT A: the owner plays and looks at the map (TESTING.md: S2, S3, S4, Owner changes). Next after that: S5 (poses).

## How the code works (summary)
1. Rojo maps `src/shared` to `ReplicatedStorage.Shared`, `src/server` to `ServerScriptService.Server`, `src/client` to `StarterPlayerScripts.Client`.
2. Server boot (`init.server.luau`): require every service in `ORDER`, call `Init(services)` on each, build the world, then call `Start()` on each.
3. Client boot (`init.client.luau`): require controllers and call `Init`. Controllers build their own ScreenGuis.
4. Services talk through the `services` table, never by requiring each other. This avoids require cycles.
5. Remotes are declared once in `src/shared/Remotes.luau`. The server creates them, clients wait for them.
6. `DataService` owns saved data. `TEMPLATE` lists every field and `reconcile` back-fills new fields into old saves.
7. Training: a ProximityPrompt starts a session. Each client click sends RequestRep. The server enforces the cooldown and adds Aura.
8. Evolution: Aura added (`aura` is the spendable balance, `cycleAura` sets the stage), `CheckStage` runs, `ApplyLook` scales the R15 body, `StageUp` fires the client cutscene. Glow Reset is available from Gigasigma.
9. All tuning numbers are in `src/shared/Config/`. Pure maths is in `src/shared/Formula.luau` and `src/shared/Logic/`, and is unit tested outside Roblox with Lune.
10. Run `scripts/check.ps1` (Windows) or `scripts/check.sh` before each commit: format, lint, unit tests, Rojo build.

## Finished tasks
- 2026-11-04 S1 Tooling, tests, CI (e782efa)
- 2026-11-04 S2 Refactor, UI kit, effects, sounds (34e9290)
- 2026-11-04 S3 Debug panel (34e9290)
- 2026-11-04 S4 World: MapBuilder, zones, props, gates (34e9290)
- 2026-11-04 Owner changes: clicks only, upgrades, daily brainrot spin (1d60716)
