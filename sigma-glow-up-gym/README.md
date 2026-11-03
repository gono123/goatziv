# Sigma Glow-Up Gym (Roblox)

Train → farm Aura → glow up through 6 absurd stages → mog other players in crowd-judged Pose-Offs.

| File | What it is |
|---|---|
| `GDD.md` | Full game design document (the *what* and *why*) |
| `BUILD_SPEC.md` | Milestone-by-milestone build breakdown with paste-ready Claude Code prompts |
| `CLAUDE.md` | Rules Claude Code follows in this folder (architecture, guardrails) |
| `src/` | Luau source, synced into Studio with Rojo |

## Quick start
1. Install [Rokit](https://github.com/rojo-rbx/rokit), then in this folder:
   ```bash
   rokit install
   rojo serve
   ```
2. Roblox Studio → new **Baseplate** → install the **Rojo** plugin → **Connect**.
3. Game Settings → Avatar → **R15**. Game Settings → Security → **Enable Studio Access to API Services**
   (publish the place once so saving works).
4. Press **Play**. A greybox gym appears; walk to the Dumbbells, press the prompt, tap on gold.

## Building the rest with Claude Code
Run `claude` in this folder and follow `BUILD_SPEC.md` from milestone **M4** onward. Each
milestone has an acceptance checklist to run in Studio before moving on.

## Tuning
All numbers live in `src/shared/Config/` (stage thresholds, equipment, timing windows, cooldowns).
