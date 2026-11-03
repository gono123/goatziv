# Sigma Glow-Up Gym (Roblox)

Train → farm Aura → glow up through 6 absurd stages → mog other players in crowd-judged Pose-Offs.

| File | What it is |
|---|---|
| `MASTER_PROMPT.md` | Complete build instructions for Claude Code |
| `GDD.md` | Full game design document (the *what* and *why*) |
| `BUILD_SPEC.md` | Milestone-by-milestone build breakdown |
| `CLAUDE.md` | Rules Claude Code follows in this folder (architecture, guardrails) |
| `PROGRESS.md` | What is finished, and what comes next |
| `TESTING.md` | How to test each step in Studio |
| `MY_TODO.md` | Things only the owner can do |
| `DECISIONS.md` | Choices made where the docs left room |
| `src/` | Luau source, synced into Studio with Rojo |
| `tests/` | Unit tests that run outside Roblox with Lune |

## Quick start
1. Install [Rokit](https://github.com/rojo-rbx/rokit), then in this folder:
   ```bash
   rokit install
   rojo plugin install
   rojo serve
   ```
2. Roblox Studio → new **Baseplate** → Plugins tab → **Rojo** → **Connect**.
3. Game Settings → Avatar → **R15**. Game Settings → Security → **Enable Studio Access to API Services**
   (publish the place once so saving works).
4. Press **Play**. The whole map builds itself. Walk to the Dumbbells, press the prompt, tap on gold.

## Checks
Run `scripts/check.ps1` (Windows) or `scripts/check.sh`: format, lint, unit tests, Rojo build.

## Tuning
All numbers live in `src/shared/Config/` (stage thresholds, equipment, timing windows, map layout).
