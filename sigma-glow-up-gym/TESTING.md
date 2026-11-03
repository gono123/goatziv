# TESTING

How to test each step in Roblox Studio. If something fails: copy the red text from the
**Output** window (View tab → Output) and paste it to Claude Code.

The **debug panel** gets you anywhere fast. Open it with the 🛠️ button on the left of the screen
(or F8). Everyone is an admin while testing in Studio.

## S2 — Refactor, UI kit, settings
Setup: Home tab → **Play**.
1. Look at the top of the screen. Expect: stage name, gold AURA number, progress bar.
2. Walk to the Dumbbells and press the prompt. Expect: tap bar at the bottom, STOP button.
3. Tap when the marker is on gold. Expect: "PERFECT! +2" floats up, small sparks at your hands, tiny camera shake.
4. Tap off-centre. Expect: "GOOD!" or "MISS!" words, not only colours.
5. Press the ⚙️ button. Expect: a window with Music, Sound effects and Low effects. Tap outside it. Expect: it closes.
6. Change Music to 20%, press Stop, press Play again. Expect: still 20% (only if API access is on).
7. Debug panel → **Stage 2**. Expect: cutscene, body grows smoothly, a ring expands at your feet.
8. Debug panel → **Stage 4**. Expect: sunglasses fall from above onto your face.
9. Debug panel → **Glow Reset now**. Expect: white flash, body shrinks back, GLOW RESET title.
Pass if: all of the above work and the Output window has no red text.

## S3 — Debug panel
Setup: **Play**.
1. Press 🛠️. Expect: a grid of buttons. Press it again (or X). Expect: it closes.
2. Press **+1K Aura**. Expect: the Aura number jumps by 1K.
3. Press **+1,000 Drip** and **+100 Shards**. Expect: no errors (the HUD shows these in later steps).
4. Press **Fast mode on/off**. Expect: a message "Fast mode ON". Reps can now be tapped much quicker.
5. Press **Start Titan**. Expect: a message "TitanService is not built yet" (that comes in S7).
6. Press **Reset my data**. Expect: you respawn as a Noob with 0 Aura.
Pass if: every button either works or says "not built yet", and there is no red text.

## S4 — The world
Setup: **Play**, then press the **Tab** key to see your stats if you like.
1. On spawn, look around. Expect: orange-trimmed plaza, "SIGMA GLOW-UP GYM" arch, neon arrows, the Starter Gym ahead.
   You should also see the POSE-OFF lights to the left and the tall Titan clock behind you.
2. Walk into the Starter Gym. Expect: dark floor, mirror wall, 3 Dumbbell and 3 Bench stations with labels.
3. Look at a Bench. Expect: its label says 🔒 GYM RAT and its floor square is red.
4. Press the prompt on a Dumbbell. Expect: you snap onto the neon square, facing the machine.
5. East of the gym is the **Iron Yard**. Walk at its gate. Expect: a red force field, "Unlocks at CHAD", and you can't pass.
6. Debug panel → **Stage 3**. Walk at the gate again. Expect: the force field is gone and you walk in. Try a Squat Rack.
7. Walk behind the Starter Gym onto the purple **Launch Pad**. Expect: a message that it is locked.
8. Debug panel → **Stage 6**, then step on the pad. Expect: you fly up to the Cosmic Dojo. Step on BACK DOWN to return.
9. North of the Iron Yard is **Mog Mansion**. Expect: marble, gold, a doorway you can walk through now.
10. Walk west to the **Pose-Off Arena**, then behind spawn to **Titan Plaza**, the **Drip Shop** and the **Hall of Mog**.
Two-player check: Test tab → **Clients and Servers** → 2 Players → Start. Both walk to the same Dumbbell station.
Expect: the second player sees "Station taken — try the next one".
Pass if: everything appears, gates block and unlock correctly, and there is no red text.
