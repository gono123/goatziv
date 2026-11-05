# Rebuilding the graph

From the repo root:

```bash
node graphify-out/build/graphify.js . && node graphify-out/build/report.js graphify-out && node graphify-out/build/html.js graphify-out
```

- `graphify.js` → `graph.json` (files, shared engine, globals, CLI modes, scenes, cast, docs)
- `report.js` → `GRAPH_REPORT.md`
- `html.js` → `graph.html` (interactive; loads d3 from cdnjs)
