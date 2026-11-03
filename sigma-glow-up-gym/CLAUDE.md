# CLAUDE.md — Sigma Glow-Up Gym

Instructions for Claude Code working in this folder. Read this first, then `BUILD_SPEC.md`
for the milestone you're implementing. The game design lives in `GDD.md`.

## What this is
A Roblox experience: train at a gym with a timing-bar mini-game, earn **Aura**, evolve through
6 ridiculous glow-up stages (Noob → Gym Rat → Chad → Sigma → Gigasigma → Cosmic Mogger), compete
in crowd-judged **Pose-Offs**, and join an hourly server event (**Mog the Titan**).
Mobile-first audience, mostly ages 9–15.

## Stack
- **Luau** scripts synced into Roblox Studio with **Rojo 7** (`rokit.toml` pins the version).
- No package manager yet. If adding packages later, use Wally and put them in `Packages/`.
- Data: `DataStoreService` via `DataService` (prototype). Migrating to ProfileStore is milestone M13.

## Commands
```bash
rokit install          # installs rojo from rokit.toml
rojo serve             # live-sync into Studio (Rojo plugin → Connect)
rojo build -o build.rbxl   # build a place file
```
Claude Code **cannot run Roblox Studio**. After each change the human playtests in Studio
(Play / Start Server + 2 Players) and pastes back Output-window errors. If the Roblox Studio
MCP server is connected, use it to read the Output and run test code instead.

## Layout (Rojo → Roblox)
| Folder | Becomes | Purpose |
|---|---|---|
| `src/shared/` | `ReplicatedStorage.Shared` | Config, pure math (`Formula`), `Remotes`, utils. Required by both sides. |
| `src/shared/Config/` | `ReplicatedStorage.Shared.Config` | **All tuning numbers.** Stages, Equipment, Training, later Poses/Prompts/Products/Quests. |
| `src/server/` | `ServerScriptService.Server` (Script) | `init.server.luau` boots services in order. |
| `src/server/Services/` | ModuleScripts | One service per system. |
| `src/client/` | `StarterPlayerScripts.Client` (LocalScript) | `init.client.luau` boots controllers. |
| `src/client/Controllers/` | ModuleScripts | One controller per UI/system. |

## Architecture rules (follow these exactly)
1. **Server is authoritative.** Clients only send *intent* (`RequestRep(tapTime)`, `PoseOffVote(userId)`,
   etc.). The server validates everything: type checks, NaN checks, cooldowns, range checks,
   unlock checks. Never trust a client number for currency, score or rewards.
2. **Services** are tables with `:Init(services)` (store references, no yielding) and `:Start()`
   (connect events, start loops). Add new services to `ORDER` in `src/server/init.server.luau`.
   Cross-service calls go through the `services` table (e.g. `services.EvolutionService:AddAura`),
   never through direct `require` of another service (avoids cycles).
3. **Controllers** are tables with `Init(...)`; add them to `src/client/init.client.luau`.
4. **Remotes:** every RemoteEvent name is declared once in `src/shared/Remotes.luau` with a comment
   showing its arguments and direction. Don't create remotes anywhere else.
5. **Config-driven:** no magic numbers in services. Put tunables in `src/shared/Config/*.luau`.
   Shared math goes in `src/shared/Formula.luau` (pure functions, no Roblox services).
6. **Data:** all saved fields go in `TEMPLATE` in `DataService.luau`. Adding a field there is enough;
   `reconcile` back-fills old saves. Bump nothing, never delete/rename saved fields without a migration.
   Mutate `DataService:Get(player)` directly, then call `EvolutionService:Sync(player)` if the client
   HUD needs it.
7. **Currency changes** go through one function per currency (`EvolutionService:AddAura`, later
   `EconomyService:AddDrip`) so analytics + sync happen in one place.
8. **Idempotent purchases:** `ProcessReceipt` records `PurchaseId` in the player's data before
   returning `PurchaseGranted`. Return `NotProcessedYet` if data isn't loaded.
9. **Mobile-first UI:** tap targets ≥ 44 px, `TextScaled` or large fonts, no hover-only interactions,
   test at phone resolution in Studio's device emulator.
10. **Performance:** no per-frame server loops per player; use `task.wait` loops at ≥ 0.25 s or events.
    Client `RenderStepped` only for visuals.

## Style
- Tabs for indentation, `PascalCase` modules/services, `camelCase` locals, `UPPER_SNAKE` constants.
- `local X = game:GetService("X")` at the top; `require` shared modules via
  `ReplicatedStorage:WaitForChild("Shared")`.
- Keep functions short; comment *why*, not *what*.
- Prefer plain Lua syntax in shared/config modules (no `+=`, `continue` or type annotations), so
  they can be syntax-checked and unit-tested outside Studio with a standard Lua runtime.

## Product guardrails (non-negotiable)
- **Never sell:** stages, Mog Rating, Pose-Off advantages, Glow Shards.
- **No paid random items** without clearly showing odds (Roblox policy).
- **Never reward watching any scrolling video/media feed** (banned for under-16 tiers).
- **No paywall prompts in the first 10 minutes** (first shop prompt only after reaching Chad).
- **Original IP only:** no real people's likeness (e.g. the real "Gigachad" photo), no copyrighted
  meme characters, only licensed audio from Roblox's library.
- Comedy exaggeration, never real body-shaming, weight-loss or diet messaging.
- Everything must work **without chat** (many players are chat-restricted).

## Current status
See the milestone table at the top of `BUILD_SPEC.md`. Milestones M1–M3 core are implemented.

## Definition of done (every milestone)
- Code follows the rules above; new tunables are in Config; new remotes are in `Remotes.luau`.
- `BUILD_SPEC.md` acceptance checklist for that milestone passes in a Studio playtest
  (human confirms, or via Studio MCP).
- Update the status column in `BUILD_SPEC.md`.
- Commit with a message like `M5: Pose-Off arena queue and rounds`.
