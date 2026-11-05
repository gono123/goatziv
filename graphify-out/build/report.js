// GRAPH_REPORT.md from graph.json
const fs = require('fs'), path = require('path');
const OUT = path.resolve(process.argv[2] || 'graphify-out');
const g = JSON.parse(fs.readFileSync(path.join(OUT, 'graph.json'), 'utf8'));
const N = Object.fromEntries(g.nodes.map((n) => [n.id, n]));
const P = g.projects;
const md = [];
const by = (k) => g.nodes.filter((n) => n.kind === k);
const code = g.nodes.filter((n) => n.kind === 'module');
const loc = (ns) => ns.reduce((a, n) => a + (n.lines || 0), 0);
const engine = code.filter((n) => n.id.startsWith('engine/'));
md.push(`# Graph report: ${g.root}`, '', `Generated ${g.generated} from \`.\` (${g.nodes.length} nodes, ${g.edges.length} edges). Open \`graph.html\` to explore it; \`graph.json\` holds the raw graph.`, '');
md.push('## Summary', '');
md.push(`- **What the repo is:** the writing room and film studio of a "What If…?" YouTube channel. ${P.length} finished episodes (${P.map((p) => '`' + p + '/`').join(', ')}), each a self-contained film project where every frame is drawn in code and every sound is synthesised in code, plus title ideas, narration scripts and YouTube upload kits.`);
md.push(`- **Shape:** ${code.length} JS modules (${loc(engine)} lines of shared engine, counted once), ${by('scene').length} scenes, ${by('character').length} characters, ${by('doc').length} Markdown docs, ${by('font').length} bundled fonts.`);
md.push(`- **The engine is vendored, not shared.** \`engine/\` is copied into every episode, ${g.engineIdentical ? 'and the copies are byte-identical today' : 'and the copies have drifted'}. The graph collapses them into one set of \`engine/*\` nodes; each node lists its copies.`);
md.push(`- **Modules talk through globals.** Browser files publish a namespace on \`globalThis\` (\`U\`, \`G\`, \`Ch\`, \`UI\`, \`Data\`, \`Subs\`, \`Studio\`, \`SCORE\`, \`FL\` …) and load in the order \`index.html\` lists them. Node-side files (\`song.js\`, \`timing.js\`, \`engine/render.js\`, \`engine/audio/*\`) use \`require\`. Several files (\`util.js\`, \`music.js\`, \`score.js\`, \`lines.js\`, \`timeline.js\`) run in both worlds.`, '');

md.push('## God nodes (most connected)', '', '| Node | Degree | Why it matters |', '|---|---:|---|');
const why = {
  'engine/render.js': 'CLI entry point: drives headless Chrome, muxes, verifies, and dispatches to every `engine/tools/*` mode',
  'engine/video/gfx.js': 'hand-drawn drawing toolkit (`G`): almost every pixel passes through `G.ellipse`, `G.line`, `G.rrect`, `G.poly`',
  'engine/video/boot.js': 'the frame contract: `Studio.film()` on the film side, `window.renderAt()` on the renderer side; also loads the fonts',
  'engine/util.js': 'pure math helpers (`U`) shared by audio and video so both stay deterministic',
  'engine': 'the vendored engine folder itself',
};
for (const n of g.nodes.filter((n) => n.kind !== 'scene' && n.kind !== 'character').sort((a, b) => b.degree - a.degree).slice(0, 10)) {
  const w = why[n.id] || (n.id.endsWith('film.js') ? 'all scenes of the episode, one function each' : n.id.endsWith('lines.js') ? 'the narration, one entry per spoken line, grouped by scene' : n.id.endsWith('film-lib.js') ? "the episode's cast, world and props" : n.id.endsWith('score.js') ? 'the timing spine: scenes, events and music sections, from the measured voiceover' : n.summary || '');
  md.push(`| \`${n.id}\` | ${n.degree} | ${w} |`);
}
md.push('');

// heaviest call paths
md.push('## Heaviest call paths', '', 'Counted from member accesses on each imported namespace (for example `G.line(...)`).', '', '| From | To | Calls |', '|---|---|---:|');
for (const e of g.edges.filter((e) => e.calls).sort((a, b) => b.calls - a.calls).slice(0, 10)) md.push(`| \`${e.source}\` | \`${e.target}\` | ${e.calls} |`);
md.push('');

// communities
md.push('## Communities', '');
const groups = {};
g.nodes.forEach((n) => (groups[n.group] ||= []).push(n));
for (const [k, ns] of Object.entries(groups).sort((a, b) => b[1].length - a[1].length)) {
  const top = ns.sort((a, b) => b.degree - a.degree).slice(0, 6).map((n) => '`' + (n.kind === 'scene' || n.kind === 'character' ? n.label : n.id) + '`');
  md.push(`- **${k}** (${ns.length}): ${top.join(', ')}${ns.length > 6 ? ' …' : ''}`);
}
md.push('');

// pipeline
md.push('## How a film gets made (the pipeline the edges describe)', '');
md.push('1. `titles/batch-01.md` pitches the episode → `scripts/<slug>.md` holds the narration.');
md.push('2. `lines.js` splits the script into spoken lines per scene (speaker prefixes `S:`, `M:`, `L:` …).');
md.push('3. `timing.js` voices every line through `engine/audio/voice.js`, measures it and **generates** `timeline.js`.');
md.push('4. `score.js` reads `timeline.js` + `lines.js` and places scenes, events and music sections: the single source of timing.');
md.push('5. `song.js` renders the soundtrack from the score with `engine/audio/{dsp,instruments,genres,mix,voice}`.');
md.push('6. `index.html` loads engine + episode scripts in order; `film.js` draws each scene with `G`, `Ch`, `UI`, `Data`, `Subs` and `film-lib.js`.');
md.push('7. `engine/render.js` renders frames in headless Chrome, muxes with the music, then `check`/`verify`; tools add posters, captions (`srt`), QA, pacing and format variants.');
md.push('8. `youtube/<slug>.md` is the upload kit for the finished `out/<name>.mp4` (not committed).', '');

// episodes compared
md.push('## Episodes side by side', '', '| | ' + P.map((p) => '`' + p + '`').join(' | ') + ' |', '|---|' + P.map(() => '---:|').join(''));
const row = (label, f) => md.push(`| ${label} | ${P.map(f).join(' | ')} |`);
row('Title', (p) => N['proj:' + p].label);
row('Scenes', (p) => by('scene').filter((n) => n.id.startsWith('scene:' + p + ':')).length);
row('Characters', (p) => by('character').filter((n) => n.id.startsWith('cast:' + p + ':')).length);
row('Spoken lines', (p) => by('scene').filter((n) => n.id.startsWith('scene:' + p + ':')).reduce((a, n) => a + n.lines, 0));
row('film.js lines', (p) => N[p + '/film.js'].lines);
row('film-lib.js lines', (p) => N[p + '/film-lib.js'].lines);
row('Busiest character (scenes)', (p) => { const c = {}; g.edges.filter((e) => e.target.startsWith('cast:' + p + ':') && e.source.startsWith('scene:')).forEach((e) => (c[e.target] = (c[e.target] || 0) + 1)); const [k, v] = Object.entries(c).sort((a, b) => b[1] - a[1])[0]; return `${N[k].label} (${v})`; });
md.push('');

// surprises / gaps
md.push('## Surprising connections and gaps', '');
const never = engine.filter((n) => !n.usedBy || !n.usedBy.length);
md.push(`- **Engine code no episode runs:** ${never.map((n) => '`' + n.id + '` (' + n.lines + ' lines)').join(', ')}. They are reached only by commands these films do not use (\`render.js analyze\`, sung lines).`);
const loadedUnused = ['engine/video/shots.js'].filter((id) => !(N[id].api || []).length);
if (loadedUnused.length) md.push(`- **Loaded but never called:** ${loadedUnused.map((id) => '`' + id + '`').join(', ')} is in both \`index.html\` files, yet neither film calls \`Shots.*\`: each \`film.js\` dispatches scenes through its own \`SCENES\` table and \`score.sceneAt(t)\`.`);
md.push(`- **\`package.json\` name drift:** \`eyesight-100x/package.json\` is still named \`my-film\` (template default) while \`zero-fear\` was renamed.`);
md.push(`- **Generated file in the graph:** \`timing.js\` → \`timeline.js\` ("do not edit"). Edit \`lines.js\` and rerun \`node timing.js\`; editing \`timeline.js\` by hand is overwritten.`);
md.push(`- **Cross-episode edges:** none. Episodes never reference each other; everything shared lives in the vendored engine. A fix to \`engine/\` has to be copied into every episode by hand.`);
md.push(`- **Scripts are one line each:** \`scripts/*.md\` hold the whole narration as a single paragraph; \`lines.js\` is the structured copy, and the two can drift apart.`);
const remaining = (fs.readFileSync(path.join(path.dirname(OUT), 'titles/batch-01.md'), 'utf8').match(/^\d+\./gm) || []).length;
md.push(`- **Backlog:** ${remaining} titles pitched in \`titles/batch-01.md\`, ${P.length} produced (#${g.edges.filter((e) => e.rel.startsWith('pitched as')).map((e) => e.rel.split('#')[1]).sort((a, b) => a - b).join(' and #')}).`, '');

md.push('## Confidence', '', `${g.edges.filter((e) => e.confidence === 'EXTRACTED').length} edges are **EXTRACTED** (read straight from code: \`require\`, \`globalThis\` reads, \`<script>\` tags, \`npm\` scripts, scene tables, speaker prefixes). ${g.edges.filter((e) => e.confidence === 'INFERRED').length} are **INFERRED** (doc ↔ episode matched by title slug, fonts matched by family name).`, '');
md.push('## Questions this graph can answer', '');
md.push('- Which engine modules would a change to `G.line` ripple into? (follow `uses global` edges into `engine/video/gfx.js`)');
md.push('- Which scenes does a character appear in, and where do they speak? (`shows` vs `speaks in`)');
md.push('- What do I have to touch to start episode #3? (copy a project folder; edit `lines.js`, `score.js`, `film-lib.js`, `film.js`; rerun `timing.js`)');
md.push('- Is the engine still identical across episodes? (rerun the builder; `engineIdentical` in `graph.json`)', '');
fs.writeFileSync(path.join(OUT, 'GRAPH_REPORT.md'), md.join('\n'));
console.log(md.join('\n'));
