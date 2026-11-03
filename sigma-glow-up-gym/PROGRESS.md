# PROGRESS

**Where things stand (paused 2026-11-04, owner returns tomorrow):** S1 to S4 and the owner changes are built and pushed. Still at CHECKPOINT A. Do not start S5 until the owner reports a result.

**Do this first when the owner says "continue":**
1. Start `rojo serve` in `sigma-glow-up-gym` in the background. It stops when Claude Code closes.
2. Ask the owner to open the game in Studio, connect Rojo (Plugins, Rojo, Connect), press Stop if a game is running, then Play.
3. Open question: the owner cannot reach "the platform in the air". We assume this is the Cosmic Dojo. The launch pad is now open to everyone and has a tall purple column behind the Starter Gym. The owner's last Play started before that fix, so the fix is untested. Ask if they see the column and if stepping on the pad works.
4. Check results yourself in the newest `%LOCALAPPDATA%\Roblox\logs\*Studio*_last.log`. Look for `[SigmaGlowUpGym] Server started`, `FLog::CreatorWarning` and script errors. Compare Play times with commit times.
5. Then run the rest of Checkpoint A (TESTING.md: S2, S3, S4, Owner changes).

**Still open for the owner:**
- The game is opened from `build.rbxl` and is not published, so progress does not save. `rojo build` overwrites that file. They need File, Publish to Roblox As, then Game Settings, Security, Enable Studio Access to API Services.
- Should the Pose-Off power meter become clicks only too? Kept for now.
- Do they want a physical spin wheel in the world? Today the spin is the 🎰 button only.

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
