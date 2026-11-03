# MY TODO

Things only you can do. The game works without them, using placeholders. This list grows as the
build goes on, and each item gets click-by-click steps.

## Using your own map (optional, later)
The game builds its map from code. To replace it with a hand-built one:
1. Put your map in a Model or Folder named exactly `Map`, inside `Workspace`.
2. Select each machine. In the Properties window, add an Attribute named `EquipmentId` with a value
   from `src/shared/Config/Equipment.luau`, such as `Dumbbells`.
3. In the Tags section of the Properties window, add the tag `Equipment`.
Claude Code can walk you through this when you get there.
