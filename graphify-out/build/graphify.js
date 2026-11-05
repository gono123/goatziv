// Builds a knowledge graph of the repo: files, shared engine modules, globals, CLI modes, scenes, cast, docs.
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const ROOT = path.resolve(process.argv[2] || '.');
const OUT = path.join(ROOT, 'graphify-out');
const SKIP = new Set(['.git', 'node_modules', 'models', 'out', 'graphify-out']);
const PROJECTS = fs.readdirSync(ROOT).filter((d) => fs.existsSync(path.join(ROOT, d, 'index.html')));

function walk(dir, acc = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP.has(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, acc); else acc.push(path.relative(ROOT, p));
  }
  return acc;
}
const files = walk(ROOT).sort();
const sha = (f) => crypto.createHash('sha1').update(fs.readFileSync(path.join(ROOT, f))).digest('hex');
const read = (f) => fs.readFileSync(path.join(ROOT, f), 'utf8');
const stripComments = (src) => src.replace(/\/\*[\s\S]*?\*\//g, '').split('\n').map((l) => l.replace(/^\s*\/\/.*$/, '').replace(/([;{}),])\s*\/\/.*$/, '$1')).join('\n');
const header = (src) => { const out = []; for (const l of src.split('\n')) { if (/^\s*\/\//.test(l)) out.push(l.replace(/^\s*\/\/\s?/, '')); else if (out.length || l.trim()) break; } return out.join(' ').replace(/\s+/g, ' ').trim(); };

// ---- dedupe the engine: engine/* in each project is a copy; collapse identical copies into one node
const engineByRel = {};
for (const f of files) {
  const m = f.match(/^([^/]+)\/engine\/(.+)$/);
  if (!m || !PROJECTS.includes(m[1])) continue;
  (engineByRel[m[2]] ||= []).push({ proj: m[1], f, h: sha(f) });
}
const engineIdentical = Object.entries(engineByRel).every(([, cs]) => cs.length === PROJECTS.length && new Set(cs.map((c) => c.h)).size === 1);
const canon = (f) => { const m = f.match(/^([^/]+)\/engine\/(.+)$/); if (m && PROJECTS.includes(m[1])) { const cs = engineByRel[m[2]]; if (new Set(cs.map((c) => c.h)).size === 1) return 'engine/' + m[2]; } return f; };

const nodes = new Map(), edges = [];
const node = (id, o) => { if (!nodes.has(id)) nodes.set(id, { id, ...o }); else Object.assign(nodes.get(id), o); return nodes.get(id); };
const edge = (s, t, rel, o = {}) => { if (s === t) return; const k = s + '|' + t + '|' + rel; const ex = edges.find((e) => e.k === k); if (ex) { ex.weight += o.weight || 1; return; } edges.push({ k, source: s, target: t, rel, weight: o.weight || 1, confidence: o.confidence || 'EXTRACTED', note: o.note }); };

function groupOf(id) {
  if (id.startsWith('engine/audio/')) return 'engine · audio';
  if (id.startsWith('engine/video/') || id === 'engine/subs.js' || id === 'engine/data/geo.js') return 'engine · picture';
  if (id.startsWith('engine/tools/') || id === 'engine/render.js') return 'engine · render + tools';
  if (id.startsWith('engine/fonts/')) return 'engine · fonts';
  if (id.startsWith('engine/')) return 'engine · core';
  return null;
}

// ---- project + file nodes
node('repo', { label: 'goatziv (What If channel)', kind: 'project', group: 'channel' });
for (const p of PROJECTS) { node('proj:' + p, { label: p, kind: 'project', group: 'episode · ' + p }); edge('repo', 'proj:' + p, 'contains'); }
const fileInfo = {};
for (const f of files) {
  const id = canon(f);
  const ext = path.extname(f);
  if (ext === '.txt' && f.includes('/fonts/')) continue; // licences ride along with their font
  const proj = PROJECTS.find((p) => f.startsWith(p + '/'));
  const isEngine = id.startsWith('engine/');
  let kind = ext === '.js' ? 'module' : ext === '.md' ? 'doc' : ext === '.ttf' ? 'font' : ext === '.html' ? 'page' : 'config';
  const n = node(id, { label: path.basename(id), path: id, kind, group: isEngine ? groupOf(id) : proj ? 'episode · ' + proj : 'writing room' });
  if (isEngine) { n.copies = (n.copies || []).concat(f); }
  else if (proj) edge('proj:' + proj, id, 'contains');
  else edge('repo', id, 'contains');
  if (ext === '.js' || ext === '.md' || ext === '.html' || ext === '.json') {
    const src = read(f);
    n.lines = src.split('\n').length;
    if (ext === '.js') n.summary = header(src).slice(0, 400);
    if (ext === '.md') n.summary = (src.match(/^#\s+(.+)$/m) || [, src.split('\n')[0]])[1].slice(0, 200);
    fileInfo[f] = { id, src, proj };
  }
}
if (engineIdentical) { node('engine', { label: 'engine/ (shared copy)', kind: 'project', group: 'engine · core', summary: `Byte-identical in ${PROJECTS.join(' and ')}` }); for (const p of PROJECTS) edge('proj:' + p, 'engine', 'vendors', { note: 'full copy of engine/' }); for (const id of nodes.keys()) if (id.startsWith('engine/') && !id.startsWith('engine/fonts/')) edge('engine', id, 'contains'); }

// ---- globals: who defines globalThis.X, who reads it
const defines = {}; // global -> [fileId]
for (const [f, { id, src }] of Object.entries(fileInfo)) {
  if (!f.endsWith('.js')) continue;
  const code = stripComments(src);
  for (const m of code.matchAll(/globalThis\.([A-Za-z_$][\w$]*)\s*=(?!=)/g)) (defines[m[1]] ||= new Set()).add(id);
  for (const m of code.matchAll(/\(globalThis\.([A-Za-z_$][\w$]*)\s*=\s*\{\}\)/g)) (defines[m[1]] ||= new Set()).add(id);
  for (const m of code.matchAll(/window\.([A-Za-z_$][\w$]*)\s*=(?!=)/g)) (defines[m[1]] ||= new Set()).add(id);
}
for (const [g, set] of Object.entries(defines)) { for (const id of set) { const n = nodes.get(id); n.provides = [...new Set([...(n.provides || []), g])]; } }

const resolveReq = (fromFile, spec) => {
  if (!spec.startsWith('.')) return null;
  let p = path.normalize(path.join(path.dirname(fromFile), spec));
  if (!p.endsWith('.js')) p += '.js';
  return fs.existsSync(path.join(ROOT, p)) ? canon(p) : 'missing:' + p;
};
const apiUse = {}; // owner file -> {member -> count}
const scopeDefs = (g, proj) => { const all = [...(defines[g] || [])]; const own = all.filter((d) => d.startsWith(proj + '/')); return own.length ? own : all.filter((d) => !PROJECTS.some((p) => d.startsWith(p + '/'))); };
for (const [f, { id, src, proj }] of Object.entries(fileInfo)) {
  if (!f.endsWith('.js')) continue;
  const code = stripComments(src);
  // Node requires
  const alias = {};
  for (const m of code.matchAll(/(?:const|let|var)\s+(\{[^}]*\}|[\w$]+)\s*=\s*require\(\s*['"`]([^'"`]+)['"`]\s*\)/g)) {
    const t = resolveReq(f, m[2]); if (!t) continue;
    if (t.startsWith('missing:')) { node(t, { label: path.basename(t) + ' (generated)', kind: 'generated', group: 'generated output' }); }
    edge(id, t, 'requires');
    if (!m[1].startsWith('{')) alias[m[1]] = t;
  }
  for (const m of code.matchAll(/require\(\s*['"]([^'"]+)['"]\s*\)/g)) { const t = resolveReq(f, m[1]); if (t && !t.startsWith('missing:')) edge(id, t, 'requires'); }
  // globals read
  for (const m of code.matchAll(/(?:const|let|var)?\s*([\w$]+)\s*=\s*globalThis\.([A-Za-z_$][\w$]*)\b(?!\s*=[^=])/g)) alias[m[1]] = 'G:' + m[2];
  for (const m of code.matchAll(/globalThis\.([A-Za-z_$][\w$]*)\b(?!\s*=[^=])/g)) {
    const g = m[1]; if (!defines[g]) continue;
    for (const d of scopeDefs(g, proj)) edge(id, d, 'uses global', { note: g });
  }
  // member usage per alias -> API surface stats
  for (const [a, tgt] of Object.entries(alias)) {
    const gname = tgt.startsWith('G:') ? tgt.slice(2) : Object.entries(defines).find(([, s]) => s.has(tgt))?.[0];
    if (!gname) continue;
    const ownerId = tgt.startsWith('G:') ? scopeDefs(gname, proj)[0] : tgt; if (!ownerId) continue;
    const re = new RegExp('(?<![\\w$.])' + a.replace(/\$/g, '\\$') + '\\.([A-Za-z_$][\\w$]*)', 'g');
    for (const m of code.matchAll(re)) { if (m[1].length < 2 && /[a-z]/.test(m[1])) continue; const b = (apiUse[ownerId] ||= {}); b[m[1]] = (b[m[1]] || 0) + 1; if (ownerId !== id) { const e = edges.find((e) => e.source === id && e.target === ownerId); if (e) e.calls = (e.calls || 0) + 1; } }
  }
  // dynamic tool dispatch in render.js
  if (id === 'engine/render.js') {
    const tm = code.match(/const TOOLS = (\{[^}]+\})/);
    if (tm) { const T = Function('return ' + tm[1])(); const byFile = {}; for (const [mode, file] of Object.entries(T)) (byFile[file] ||= []).push(mode); for (const [file, modes] of Object.entries(byFile)) edge(id, 'engine/tools/' + file + '.js', 'dispatches', { note: 'modes: ' + modes.join(', ') }); }
    const modes = [...new Set([...code.matchAll(/mode === '([\w-]+)'/g)].map((m) => m[1]))];
    nodes.get(id).modes = modes;
    if (/player\.js/.test(code)) edge(id, 'engine/video/player.js', 'injects', { note: 'preview mode adds it to index.html' });
  }
}
nodes.forEach((n) => { if (apiUse[n.id]) n.api = Object.entries(apiUse[n.id]).sort((a, b) => b[1] - a[1]).slice(0, 12); });

// ---- index.html script order
for (const p of PROJECTS) {
  const html = read(p + '/index.html'); let i = 0;
  for (const m of html.matchAll(/<script src="([^"]+)"/g)) edge(p + '/index.html', canon(p + '/' + m[1]), 'loads', { note: 'order ' + ++i });
}
// ---- package.json scripts
for (const p of PROJECTS) {
  const pk = JSON.parse(read(p + '/package.json'));
  for (const [name, cmd] of Object.entries(pk.scripts || {})) for (const m of cmd.matchAll(/node ([\w/.-]+\.js)/g)) edge(p + '/package.json', canon(p + '/' + m[1]), 'npm run ' + name);
}
// ---- generated files (from "generated by" headers and known writers)
for (const [f, { id, src }] of Object.entries(fileInfo)) {
  const g = src.match(/generated by ([\w./-]+\.js)/); if (g) edge(canon(path.join(path.dirname(f), g[1])), id, 'generates', { confidence: 'EXTRACTED' });
}

// ---- content layer: scenes, cast, script/upload docs
const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const titles = read('titles/batch-01.md').split('\n').map((l) => l.match(/^\d+\.\s+(.+)$/)).filter(Boolean).map((m) => m[1]);
for (const p of PROJECTS) {
  const lines = read(p + '/lines.js'), film = read(p + '/film.js'), lib = read(p + '/film-lib.js'), score = read(p + '/score.js');
  const title = (score.match(/^\/\/\s*(WHAT IF[^(]+\?)/) || [])[1];
  const pretty = title ? title.toLowerCase().replace(/\b\w/g, (c) => c.toUpperCase()).replace(/(\d+)X\b/g, '$1x') : p;
  node('proj:' + p, { label: pretty, summary: `Episode film project (${p}/). ${(score.match(/\(([^)]*min[^)]*)\)/) || [])[1] || ''}` });
  const s = slug(pretty);
  for (const dir of ['scripts', 'youtube']) if (nodes.has(`${dir}/${s}.md`)) edge(`${dir}/${s}.md`, 'proj:' + p, dir === 'scripts' ? 'is script of' : 'is upload kit of', { confidence: 'INFERRED', note: 'matched by title slug' });
  const ti = titles.findIndex((t) => slug(t) === s); if (ti >= 0) edge('titles/batch-01.md', 'proj:' + p, 'pitched as #' + (ti + 1), { confidence: 'INFERRED' });
  // scenes from lines.js, with line counts and speakers
  const scenes = [...lines.matchAll(/\['([\w-]+)',\s*\[([\s\S]*?)\]\]/g)].map((m) => ({ id: m[1], body: m[2] }));
  const fnSrc = {};
  const sceneMap = (film.match(/const SCENES = \{([^}]+)\}/) || [])[1] || '';
  const fnFor = Object.fromEntries(sceneMap.split(',').map((x) => x.trim()).filter(Boolean).map((x) => { const [k, v] = x.split(':').map((y) => y.trim()); return [k, v || k]; }));
  const castKeys = Object.keys(Function('return ' + (lib.match(/L\.CAST = (\{[\s\S]*?\n  \});/) || [, '{}'])[1])());
  const castNames = { S: 'sam', M: 'mia', L: 'leo', B: 'black', K: 'keeper' };
  for (const k of castKeys) node(`cast:${p}:${k}`, { label: k, kind: 'character', group: 'cast · ' + p });
  scenes.forEach((sc, i) => {
    const sid = `scene:${p}:${sc.id}`;
    const said = [...sc.body.matchAll(/(['"])((?:\\.|(?!\1).)*)\1/g)].map((m) => m[2]);
    const fn = fnFor[sc.id] || sc.id;
    const fm = film.match(new RegExp('function ' + fn + '\\(ctx, t, s\\) \\{([\\s\\S]*?)\\n  \\}\\n'));
    node(sid, { label: `${i + 1}. ${sc.id}`, kind: 'scene', group: 'scenes · ' + p, order: i + 1, summary: said.slice(0, 3).map((x) => x.replace(/^[A-Z]:/, '')).join(' '), lines: said.length });
    edge(p + '/film.js', sid, 'draws scene');
    edge(p + '/lines.js', sid, 'scripts scene');
    if (i > 0) edge(`scene:${p}:${scenes[i - 1].id}`, sid, 'next scene');
    const who = new Set(said.map((x) => (x.match(/^([A-Z]):/) || [])[1]).filter(Boolean).map((c) => castNames[c]).filter((c) => castKeys.includes(c)));
    for (const w of who) edge(sid, `cast:${p}:${w}`, 'speaks in', { confidence: 'EXTRACTED' });
    if (fm) for (const k of castKeys) if (new RegExp(`C\\.${k}\\b|'${k}'`).test(fm[1]) && !who.has(k)) edge(sid, `cast:${p}:${k}`, 'shows', { confidence: 'EXTRACTED' });
  });
  for (const k of castKeys) edge(p + '/film-lib.js', `cast:${p}:${k}`, 'defines character');
}

// ---- engine fonts: which code names them
const fontFiles = [...nodes.values()].filter((n) => n.kind === 'font');
for (const [f, { id, src }] of Object.entries(fileInfo)) for (const fn of fontFiles) { const fam = path.basename(fn.id, '.ttf').replace(/-(Regular|Bold|\d+)$/, ''); if (src.includes(path.basename(fn.id))) edge(id, fn.id, 'uses font'); else if (src.includes(`'${fam}`) && f.endsWith('.js')) edge(id, fn.id, 'uses font', { confidence: 'INFERRED', note: 'names the family ' + fam }); }

// ---- reachability: which engine modules does each episode actually run?
const out = {}; edges.forEach((e) => { if (['requires', 'loads', 'dispatches', 'injects', 'uses global', 'npm run'].some((r) => e.rel.startsWith(r))) (out[e.source] ||= []).push(e.target); });
for (const p of PROJECTS) {
  const seen = new Set(); const st = [p + '/index.html', p + '/song.js', p + '/timing.js', p + '/package.json'];
  while (st.length) { const x = st.pop(); if (seen.has(x)) continue; seen.add(x); (out[x] || []).forEach((y) => st.push(y)); }
  for (const id of seen) { const n = nodes.get(id); if (n && id.startsWith('engine/')) n.usedBy = [...new Set([...(n.usedBy || []), p])]; }
}
// ---- metrics: degree, communities = group, god nodes, bridges
const E = edges.map(({ k, ...e }) => e);
const deg = {}; E.forEach((e) => { deg[e.source] = (deg[e.source] || 0) + 1; deg[e.target] = (deg[e.target] || 0) + 1; });
const N = [...nodes.values()].map((n) => ({ ...n, degree: deg[n.id] || 0 }));
fs.mkdirSync(OUT, { recursive: true });
const graph = { generated: new Date().toISOString().slice(0, 10), root: path.basename(ROOT), projects: PROJECTS, engineIdentical, nodes: N, edges: E };
fs.writeFileSync(path.join(OUT, 'graph.json'), JSON.stringify(graph, null, 1));
console.log(`nodes ${N.length}, edges ${E.length}, engine identical: ${engineIdentical}`);
