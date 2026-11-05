// graph.html: interactive view of graph.json (self-contained apart from d3 from cdnjs)
const fs = require('fs'), path = require('path');
const OUT = path.resolve(process.argv[2] || 'graphify-out');
const g = JSON.parse(fs.readFileSync(path.join(OUT, 'graph.json'), 'utf8'));
const keep = ['id', 'label', 'kind', 'group', 'lines', 'summary', 'copies', 'provides', 'api', 'usedBy', 'degree', 'order', 'modes'];
const data = {
  projects: g.projects, generated: g.generated, engineIdentical: g.engineIdentical,
  nodes: g.nodes.map((n) => Object.fromEntries(keep.filter((k) => n[k] !== undefined).map((k) => [k, n[k]]))),
  edges: g.edges.map(({ source, target, rel, confidence, note, calls }) => ({ source, target, rel, confidence, ...(note ? { note } : {}), ...(calls ? { calls } : {}) })),
};
const json = JSON.stringify(data).replace(/</g, '\\u003c');
const count = (k) => g.nodes.filter((n) => n.kind === k).length;
const html = String.raw`<title>Goatziv Studio Map</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gochi+Hand&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
/* Layout: a storyboard desk. Graph stage on the left, an inspector card on the right (stacks on phones), findings below. */
:root {
  --bg: #EEF0F1; --surface: #FFFFFF; --ink: #1E2226; --muted: #5C646D; --line: #D3D8DE; --focus: #2F6FDB;
  --audio: #2F7A72; --picture: #D9622C; --tools: #4E6A8F; --core: #3A3330; --fonts: #8E98A3;
  --ep1: #7A55A8; --ep2: #A77A05; --writing: #CC4F72; --edge: rgba(30,34,38,.16); --edge-hi: rgba(30,34,38,.7);
  --f-display: 'Gochi Hand', 'Patrick Hand', 'Comic Sans MS', cursive;
  --f-body: 'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --f-mono: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #14171B; --surface: #1C2025; --ink: #E5E8EB; --muted: #9AA3AD; --line: #2E343B; --focus: #7AA7F5;
  --audio: #5BC2B6; --picture: #F08A55; --tools: #8FA9D1; --core: #D9CFC9; --fonts: #7D8792;
  --ep1: #B597E0; --ep2: #E2B53A; --writing: #EE8AA6; --edge: rgba(229,232,235,.14); --edge-hi: rgba(229,232,235,.75); color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #14171B; --surface: #1C2025; --ink: #E5E8EB; --muted: #9AA3AD; --line: #2E343B; --focus: #7AA7F5;
  --audio: #5BC2B6; --picture: #F08A55; --tools: #8FA9D1; --core: #D9CFC9; --fonts: #7D8792;
  --ep1: #B597E0; --ep2: #E2B53A; --writing: #EE8AA6; --edge: rgba(229,232,235,.14); --edge-hi: rgba(229,232,235,.75); color-scheme: dark }
* { box-sizing: border-box }
body { background: var(--bg); color: var(--ink); font: 15px/1.5 var(--f-body); margin: 0 }
.wrap { max-width: 1320px; margin: 0 auto; padding-block: 28px 56px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 22px }
header { display: flex; flex-wrap: wrap; align-items: end; justify-content: space-between; gap: 12px 32px }
h1 { font: 400 clamp(34px, 5vw, 50px)/1 var(--f-display); margin: 0; text-wrap: balance }
.lede { margin: 6px 0 0; color: var(--muted); max-width: 62ch }
.stats { display: flex; flex-wrap: wrap; gap: 6px 18px; font: 13px var(--f-mono); color: var(--muted); font-variant-numeric: tabular-nums }
.stats b { color: var(--ink); font-weight: 500 }
.controls { display: flex; flex-wrap: wrap; gap: 8px; align-items: center }
.chip { font: 500 13px var(--f-body); border: 1px solid var(--line); background: var(--surface); color: var(--muted); padding: 5px 11px 5px 9px; border-radius: 999px; cursor: pointer; display: inline-flex; align-items: center; gap: 7px }
.chip[aria-pressed="true"] { color: var(--ink); border-color: var(--ink) }
.chip i { width: 9px; height: 9px; border-radius: 50%; display: inline-block }
.chip[aria-pressed="false"] i { opacity: .35 }
select, input[type="search"] { font: 13px var(--f-body); color: var(--ink); background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 6px 10px }
input[type="search"] { min-width: 0; flex: 1 1 180px; max-width: 280px }
:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px }
.desk { display: grid; grid-template-columns: minmax(0, 1fr) 340px; gap: 16px; align-items: start }
@media (max-width: 900px) { .desk { grid-template-columns: minmax(0, 1fr) } }
.stage { position: relative; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; height: min(72vh, 760px); min-height: 380px; overflow: hidden }
.stage svg { width: 100%; height: 100%; display: block; cursor: grab; touch-action: none }
.stage .hint { position: absolute; left: 12px; bottom: 10px; font: 12px var(--f-mono); color: var(--muted); pointer-events: none }
.stage .reset { position: absolute; right: 10px; top: 10px }
.tip { position: absolute; pointer-events: none; background: var(--ink); color: var(--bg); font: 12px var(--f-mono); padding: 3px 7px; border-radius: 5px; white-space: nowrap; transform: translate(-50%, -130%) }
.legend { display: flex; flex-wrap: wrap; gap: 4px 14px; font-size: 12px; color: var(--muted) }
.legend span { display: inline-flex; align-items: center; gap: 6px }
.legend i { width: 18px; border-top: 2px solid var(--muted); display: inline-block }
.legend i.dash { border-top-style: dashed }
aside { background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 18px; min-width: 0; max-height: min(72vh, 760px); overflow: auto }
@media (max-width: 900px) { aside { max-height: none } }
aside h2 { font: 600 17px/1.3 var(--f-body); margin: 0; word-break: break-word }
.kind { font: 500 11px var(--f-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); display: flex; gap: 8px; align-items: center; margin-bottom: 6px }
.kind i { width: 10px; height: 10px; border-radius: 50% }
aside p { margin: 8px 0 0; color: var(--muted); font-size: 14px }
aside h3 { font: 500 11px var(--f-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin: 18px 0 6px }
.kv { display: grid; grid-template-columns: auto 1fr; gap: 2px 12px; font-size: 13px; margin-top: 10px }
.kv dt { color: var(--muted) } .kv dd { margin: 0; font-family: var(--f-mono); font-size: 12px; word-break: break-word }
.links { list-style: none; margin: 0; padding: 0; display: grid; gap: 2px }
.links button { all: unset; cursor: pointer; display: flex; gap: 8px; align-items: baseline; width: 100%; padding: 3px 6px; margin: 0 -6px; border-radius: 6px; font-size: 13px }
.links button:hover, .links button:focus-visible { background: var(--bg) }
.links .rel { font: 11px var(--f-mono); color: var(--muted); flex: none; min-width: 84px }
.links .nm { font-family: var(--f-mono); font-size: 12px; word-break: break-all }
.links .ct { margin-left: auto; font: 11px var(--f-mono); color: var(--muted); font-variant-numeric: tabular-nums }
.api { display: grid; gap: 3px }
.api div { display: grid; grid-template-columns: 96px 1fr 34px; gap: 8px; align-items: center; font: 12px var(--f-mono) }
.api span.bar { height: 6px; border-radius: 3px; background: var(--muted); opacity: .55 }
.api em { font-style: normal; color: var(--muted); text-align: right; font-variant-numeric: tabular-nums }
.notes { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px }
.note { background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 18px 20px; min-width: 0 }
.note h2 { font: 400 26px/1.1 var(--f-display); margin: 0 0 10px }
.note ul, .note ol { margin: 0; padding-left: 20px; display: grid; gap: 7px; font-size: 14px }
.note li::marker { color: var(--muted) }
code { font: 12.5px var(--f-mono); background: var(--bg); padding: 1px 4px; border-radius: 4px }
.tbl { overflow-x: auto } table { border-collapse: collapse; width: 100%; font-size: 13px }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--line); font-variant-numeric: tabular-nums }
th { font: 500 11px var(--f-mono); letter-spacing: .05em; text-transform: uppercase; color: var(--muted) }
td.n { text-align: right; font-family: var(--f-mono) }
@media (prefers-reduced-motion: reduce) { * { transition: none !important } }
</style>

<div class="wrap">
  <header>
    <div>
      <h1>Goatziv Studio Map</h1>
      <p class="lede">The What If channel repo as a graph: the shared film engine, the two episode projects, their scenes and cast, and the writing room. Click any node to see what it is and what it touches.</p>
    </div>
    <div class="stats" id="stats"></div>
  </header>

  <div class="controls" role="group" aria-label="Filters">
    <span id="layers" style="display:contents"></span>
    <select id="ep" aria-label="Episode"></select>
    <input id="q" type="search" placeholder="Find a file, scene or character" aria-label="Find a node">
  </div>

  <div class="desk">
    <div style="display:grid;gap:8px;min-width:0">
      <div class="stage" id="stage"><svg id="svg" role="img" aria-label="Dependency and content graph"></svg><button class="chip reset" id="fit" type="button" aria-pressed="true">Fit</button><div class="hint">drag to pan · pinch or scroll to zoom</div><div class="tip" id="tip" hidden></div></div>
      <div class="legend" id="legend"></div>
    </div>
    <aside id="panel" aria-live="polite"></aside>
  </div>

  <div class="notes">
    <section class="note">
      <h2>How a film gets made</h2>
      <ol>
        <li><code>titles/batch-01.md</code> pitches it; <code>scripts/&lt;slug&gt;.md</code> holds the narration.</li>
        <li><code>lines.js</code> splits it into spoken lines per scene, with speaker prefixes.</li>
        <li><code>timing.js</code> voices each line with <code>engine/audio/voice.js</code> and writes <code>timeline.js</code>.</li>
        <li><code>score.js</code> places scenes, events and music from those measured times.</li>
        <li><code>song.js</code> synthesises the soundtrack; <code>film.js</code> draws every scene.</li>
        <li><code>engine/render.js</code> renders in headless Chrome, muxes, checks and verifies.</li>
        <li><code>youtube/&lt;slug&gt;.md</code> is the upload kit for the finished film.</li>
      </ol>
    </section>
    <section class="note">
      <h2>Worth knowing</h2>
      <ul id="findings"></ul>
    </section>
    <section class="note">
      <h2>Episodes side by side</h2>
      <div class="tbl"><table id="eps"></table></div>
    </section>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>
const DATA = ${json};
(function () {
  const $ = (s) => document.querySelector(s);
  const byId = new Map(DATA.nodes.map((n) => [n.id, n]));
  const P = DATA.projects;
  const short = (id) => id.replace(/^engine\//, 'engine/').replace(/^proj:/, '');
  const epOf = (id) => P.find((p) => id.startsWith(p + '/') || id.includes(':' + p + ':') || id === 'proj:' + p);
  const tok = {}; const readTok = () => { const cs = getComputedStyle(document.documentElement); ['audio','picture','tools','core','fonts','ep1','ep2','writing','ink','muted','surface','bg','line','edge','edge-hi','focus'].forEach((k) => tok[k] = cs.getPropertyValue('--' + k).trim()); };
  readTok();
  const hue = (n) => { const g = n.group || ''; if (g.includes('audio')) return tok.audio; if (g.includes('picture')) return tok.picture; if (g.includes('render')) return tok.tools; if (g.includes('fonts')) return tok.fonts; if (g.includes('engine')) return tok.core; if (g.includes(P[0])) return tok.ep1; if (g.includes(P[1])) return tok.ep2; if (g === 'writing room') return tok.writing; return tok.ink; };
  const LAYERS = [
    { key: 'engine', label: 'Engine', test: (n) => n.id === 'engine' || (n.id.startsWith('engine/') && n.kind !== 'font'), color: 'picture', on: true },
    { key: 'episode', label: 'Episode code', test: (n) => !!epOf(n.id) && !['scene', 'character'].includes(n.kind), color: 'ep1', on: true },
    { key: 'content', label: 'Scenes and cast', test: (n) => ['scene', 'character'].includes(n.kind), color: 'ep2', on: true },
    { key: 'docs', label: 'Writing room', test: (n) => n.kind === 'doc' || n.id === 'repo', color: 'writing', on: true },
    { key: 'fonts', label: 'Fonts', test: (n) => n.kind === 'font', color: 'fonts', on: false },
  ];
  const state = { layers: Object.fromEntries(LAYERS.map((l) => [l.key, l.on])), ep: 'all', q: '', sel: null };
  try { const s = JSON.parse(localStorage.getItem('studio-map') || 'null'); if (s) { Object.assign(state.layers, s.layers || {}); if (s.ep) state.ep = s.ep; } } catch (e) {}
  const save = () => { try { localStorage.setItem('studio-map', JSON.stringify({ layers: state.layers, ep: state.ep })); } catch (e) {} };

  // stats
  const cnt = (k) => DATA.nodes.filter((n) => n.kind === k).length;
  $('#stats').innerHTML = [['nodes', DATA.nodes.length], ['edges', DATA.edges.length], ['modules', cnt('module')], ['scenes', cnt('scene')], ['characters', cnt('character')]].map(([k, v]) => '<span><b>' + v + '</b> ' + k + '</span>').join('');

  // controls
  const layersEl = $('#layers');
  LAYERS.forEach((l) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'chip'; b.id = 'layer-' + l.key; b.innerHTML = '<i></i>' + l.label; b.setAttribute('aria-pressed', state.layers[l.key]); b.onclick = () => { state.layers[l.key] = !state.layers[l.key]; b.setAttribute('aria-pressed', state.layers[l.key]); save(); apply(); }; l.btn = b; layersEl.appendChild(b); });
  const paintChips = () => LAYERS.forEach((l) => l.btn.querySelector('i').style.background = tok[l.color]);
  paintChips();
  $('#ep').innerHTML = '<option value="all">Both episodes</option>' + P.map((p) => '<option value="' + p + '">' + byId.get('proj:' + p).label + '</option>').join('');
  $('#ep').value = state.ep; $('#ep').onchange = (e) => { state.ep = e.target.value; save(); apply(); };
  $('#q').oninput = (e) => { state.q = e.target.value.trim().toLowerCase(); apply(); };
  $('#q').onkeydown = (e) => { if (e.key === 'Enter') { const m = nodes.find((n) => n._vis && match(n)); if (m) select(m.id, true); } };
  const match = (n) => state.q && (n.id.toLowerCase().includes(state.q) || (n.label || '').toLowerCase().includes(state.q));

  // legend
  $('#legend').innerHTML = '<span><i></i>extracted from code</span><span><i class="dash"></i>inferred (title or font-name match)</span><span>node size = connections</span>';

  // graph
  const nodes = DATA.nodes.map((n) => ({ ...n }));
  const links = DATA.edges.map((e) => ({ ...e }));
  const svg = d3.select('#svg'); const root = svg.append('g');
  const linkG = root.append('g'), nodeG = root.append('g'), labelG = root.append('g');
  const r = (n) => n.kind === 'project' ? 11 : n.kind === 'scene' ? 3.5 + Math.sqrt(n.degree) * .7 : n.kind === 'character' ? 4 + Math.sqrt(n.degree) * .6 : 4 + Math.sqrt(n.degree) * 1.35;
  const link = linkG.selectAll('line').data(links).join('line').attr('stroke-width', (d) => d.calls ? Math.min(4, 0.8 + Math.log10(d.calls + 1)) : 0.8).attr('stroke-dasharray', (d) => d.confidence === 'INFERRED' ? '3 3' : null);
  const node = nodeG.selectAll('circle').data(nodes).join('circle').attr('r', r).attr('stroke-width', 1.5).style('cursor', 'pointer')
    .on('click', (ev, d) => { ev.stopPropagation(); select(d.id); })
    .on('mouseenter', (ev, d) => showTip(d)).on('mouseleave', () => { $('#tip').hidden = true; });
  const label = labelG.selectAll('text').data(nodes).join('text').text((d) => d.kind === 'module' || d.kind === 'page' || d.kind === 'config' ? d.label : d.label).attr('font-family', 'IBM Plex Mono, ui-monospace, monospace').attr('font-size', 10).attr('dy', (d) => -r(d) - 4).attr('text-anchor', 'middle').style('pointer-events', 'none');
  const sim = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id((d) => d.id).distance((l) => l.rel === 'next scene' ? 14 : l.rel === 'contains' ? 70 : l.rel.startsWith('npm') ? 90 : 46).strength((l) => l.rel === 'contains' ? 0.08 : l.rel === 'uses font' ? 0.15 : l.rel === 'next scene' ? 0.9 : 0.35))
    .force('charge', d3.forceManyBody().strength((d) => d.kind === 'scene' ? -40 : -170))
    .force('collide', d3.forceCollide().radius((d) => r(d) + 3))
    .force('x', d3.forceX(0).strength(0.04)).force('y', d3.forceY(0).strength(0.05))
    .stop();
  for (let i = 0; i < 420; i++) sim.tick();
  const drag = d3.drag().on('start', (ev, d) => { if (!ev.active) sim.alphaTarget(0.2).restart(); d.fx = d.x; d.fy = d.y; }).on('drag', (ev, d) => { d.fx = ev.x; d.fy = ev.y; }).on('end', (ev, d) => { if (!ev.active) sim.alphaTarget(0); d.fx = null; d.fy = null; });
  node.call(drag);
  sim.on('tick', draw);
  let k = 1;
  const zoom = d3.zoom().scaleExtent([0.2, 6]).on('zoom', (ev) => { root.attr('transform', ev.transform); k = ev.transform.k; paint(); });
  svg.call(zoom).on('click', () => select(null));
  function draw() {
    link.attr('x1', (d) => d.source.x).attr('y1', (d) => d.source.y).attr('x2', (d) => d.target.x).attr('y2', (d) => d.target.y);
    node.attr('cx', (d) => d.x).attr('cy', (d) => d.y); label.attr('x', (d) => d.x).attr('y', (d) => d.y);
  }
  function fit(animate) {
    const vis = nodes.filter((n) => n._vis); if (!vis.length) return;
    const [x0, x1] = d3.extent(vis, (n) => n.x), [y0, y1] = d3.extent(vis, (n) => n.y);
    const el = $('#stage'), W = el.clientWidth, H = el.clientHeight, pad = 40;
    const s = Math.min(3, (W - pad * 2) / Math.max(1, x1 - x0), (H - pad * 2) / Math.max(1, y1 - y0));
    const t = d3.zoomIdentity.translate(W / 2 - s * (x0 + x1) / 2, H / 2 - s * (y0 + y1) / 2).scale(s);
    (animate ? svg.transition().duration(450) : svg).call(zoom.transform, t);
  }
  $('#fit').onclick = () => fit(true);

  let nb = new Set();
  function apply() {
    nodes.forEach((n) => { const lay = LAYERS.find((l) => l.test(n)); const ep = epOf(n.id); n._vis = (!lay || state.layers[lay.key]) && (state.ep === 'all' || !ep || ep === state.ep); });
    links.forEach((l) => l._vis = l.source._vis && l.target._vis);
    paint();
  }
  function paint() {
    const sel = state.sel;
    node.attr('display', (d) => d._vis ? null : 'none')
      .attr('fill', (d) => d.kind === 'character' ? tok.surface : hue(d))
      .attr('stroke', (d) => d.id === sel ? tok.ink : d.kind === 'character' ? hue(d) : tok.surface)
      .attr('stroke-width', (d) => d.id === sel ? 3 : d.kind === 'character' ? 2 : 1.5)
      .attr('opacity', (d) => (sel && !nb.has(d.id)) || (state.q && !match(d)) ? 0.18 : 1);
    link.attr('display', (d) => d._vis ? null : 'none')
      .attr('stroke', (d) => sel && (d.source.id === sel || d.target.id === sel) ? tok['edge-hi'] : tok.edge)
      .attr('opacity', (d) => sel && !(d.source.id === sel || d.target.id === sel) ? 0.25 : 1);
    label.attr('display', (d) => {
      if (!d._vis) return 'none';
      if (d.id === sel || (sel && nb.has(d.id)) || match(d)) return null;
      if (sel || state.q) return 'none';
      const big = d.kind === 'project' || ((d.kind === 'module' || d.kind === 'page') && d.degree >= (k > 1.4 ? 0 : 9)) || (d.kind === 'doc' && k > 1.1);
      return big || k > 2.2 ? null : 'none';
    }).attr('fill', tok.ink).attr('font-weight', (d) => d.id === sel || d.kind === 'project' ? 600 : 400).attr('font-size', 10 / Math.sqrt(Math.max(1, k)));
  }
  function showTip(d) {
    const el = $('#tip'); const t = d3.zoomTransform(svg.node());
    el.textContent = d.kind === 'scene' || d.kind === 'character' ? d.label + ' · ' + epOf(d.id) : short(d.id);
    el.style.left = t.applyX(d.x) + 'px'; el.style.top = (t.applyY(d.y) - r(d) * t.k) + 'px'; el.hidden = false;
  }

  // inspector
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const KIND = { module: 'JS module', page: 'page', config: 'config', doc: 'doc', font: 'font', project: 'project', scene: 'scene', character: 'character' };
  function select(id, center) {
    state.sel = id; nb = new Set(id ? [id] : []);
    if (id) links.forEach((l) => { if (l.source.id === id) nb.add(l.target.id); if (l.target.id === id) nb.add(l.source.id); });
    paint(); panel(id);
    if (center && id) { const n = nodes.find((x) => x.id === id); const t = d3.zoomTransform(svg.node()); const el = $('#stage'); svg.transition().duration(450).call(zoom.translateTo, n.x, n.y); }
  }
  function linkList(list, dir) {
    return '<ul class="links">' + list.map((l) => { const o = dir === 'out' ? l.target : l.source; const nm = o.kind === 'scene' || o.kind === 'character' ? o.label : short(o.id);
      return '<li><button type="button" data-go="' + esc(o.id) + '"><span class="rel">' + esc(l.rel) + '</span><span class="nm">' + esc(nm) + '</span>' + (l.calls ? '<span class="ct">' + l.calls + ' calls</span>' : l.note && l.rel !== 'uses global' ? '<span class="ct">' + esc(l.note) + '</span>' : l.note ? '<span class="ct">' + esc(l.note) + '</span>' : '') + '</button></li>'; }).join('') + '</ul>';
  }
  function overview() {
    const top = nodes.filter((n) => !['scene', 'character'].includes(n.kind) && n.id !== 'engine' && n.id !== 'repo').sort((a, b) => b.degree - a.degree).slice(0, 8);
    return '<div class="kind">Overview</div><h2>Most connected files</h2><p>Each episode is a folder with its own copy of the engine' + (DATA.engineIdentical ? ' (identical today)' : '') + '. Pick one of these, or any node in the graph.</p><h3>Start here</h3><ul class="links">' +
      top.map((n) => '<li><button type="button" data-go="' + esc(n.id) + '"><span class="rel">' + n.degree + ' links</span><span class="nm">' + esc(short(n.id)) + '</span></button></li>').join('') + '</ul>';
  }
  function panel(id) {
    const el = $('#panel');
    if (!id) { el.innerHTML = overview(); return; }
    const n = nodes.find((x) => x.id === id);
    const out = links.filter((l) => l.source.id === id && l.target._vis !== undefined), inc = links.filter((l) => l.target.id === id);
    const groupBy = (arr) => arr.sort((a, b) => (b.calls || 0) - (a.calls || 0) || a.rel.localeCompare(b.rel));
    let h = '<div class="kind"><i style="background:' + hue(n) + '"></i>' + esc(KIND[n.kind] || n.kind) + ' · ' + esc(n.group || '') + '</div><h2>' + esc(n.kind === 'scene' || n.kind === 'character' ? n.label : short(n.id)) + '</h2>';
    if (n.summary) h += '<p>' + esc(n.summary) + '</p>';
    const kv = [];
    if (n.lines && n.kind !== 'scene') kv.push(['lines', n.lines]);
    if (n.kind === 'scene') kv.push(['spoken lines', n.lines], ['episode', epOf(n.id)]);
    if (n.provides) kv.push(['publishes', n.provides.join(', ')]);
    if (n.usedBy) kv.push(['run by', n.usedBy.join(', ')]);
    if (n.id.startsWith('engine/') && !n.usedBy && n.kind === 'module') kv.push(['run by', 'no episode']);
    if (n.copies) kv.push(['copies', n.copies.length + ' (one per episode)']);
    if (n.modes && n.modes.length) kv.push(['modes', n.modes.join(' ')]);
    if (kv.length) h += '<dl class="kv">' + kv.map(([a, b]) => '<dt>' + a + '</dt><dd>' + esc(b) + '</dd>').join('') + '</dl>';
    if (n.api && n.api.length) { const mx = n.api[0][1]; h += '<h3>Most-called members</h3><div class="api">' + n.api.map(([m, c]) => '<div><span>' + esc(m) + '</span><span class="bar" style="width:' + Math.max(4, c / mx * 100) + '%;background:' + hue(n) + '"></span><em>' + c + '</em></div>').join('') + '</div>'; }
    if (out.length) h += '<h3>Points to (' + out.length + ')</h3>' + linkList(groupBy(out), 'out');
    if (inc.length) h += '<h3>Pointed to by (' + inc.length + ')</h3>' + linkList(groupBy(inc), 'in');
    el.innerHTML = h;
  }
  $('#panel').addEventListener('click', (e) => { const b = e.target.closest('[data-go]'); if (b) { const id = b.dataset.go; const n = nodes.find((x) => x.id === id); if (n && !n._vis) { const lay = LAYERS.find((l) => l.test(n)); if (lay) { state.layers[lay.key] = true; lay.btn.setAttribute('aria-pressed', true); } state.ep = 'all'; $('#ep').value = 'all'; apply(); } select(id, true); } });

  // notes
  const never = DATA.nodes.filter((n) => n.kind === 'module' && n.id.startsWith('engine/') && !n.usedBy);
  const F = [
    'The engine is copied into every episode folder' + (DATA.engineIdentical ? ' and the copies are byte-identical today' : '') + '. A fix in one copy has to be made in the other by hand.',
    'Browser modules share code through globals (<code>U</code>, <code>G</code>, <code>Ch</code>, <code>UI</code>, <code>Subs</code>, <code>Studio</code>, <code>SCORE</code>) loaded in <code>index.html</code> order. Node tools use <code>require</code>.',
    'No episode runs ' + never.map((n) => '<code>' + esc(n.id.replace('engine/', '')) + '</code>').join(', ') + '. <code>video/shots.js</code> is loaded by both films but never called.',
    '<code>timeline.js</code> is generated by <code>timing.js</code>. Edit <code>lines.js</code> and rerun instead.',
    '<code>eyesight-100x/package.json</code> is still named <code>my-film</code>.',
    '2 of the 35 pitched titles are made: #2 and #7.',
  ];
  $('#findings').innerHTML = F.map((f) => '<li>' + f + '</li>').join('');
  const sc = (p) => DATA.nodes.filter((n) => n.id.startsWith('scene:' + p + ':'));
  const busiest = (p) => { const c = {}; DATA.edges.filter((e) => e.target.startsWith('cast:' + p + ':') && e.source.startsWith('scene:')).forEach((e) => c[e.target] = (c[e.target] || 0) + 1); const [kk, v] = Object.entries(c).sort((a, b) => b[1] - a[1])[0]; return byId.get(kk).label + ' (' + v + ' scenes)'; };
  const rows = [['Scenes', (p) => sc(p).length], ['Characters', (p) => DATA.nodes.filter((n) => n.id.startsWith('cast:' + p + ':')).length], ['Spoken lines', (p) => sc(p).reduce((a, n) => a + n.lines, 0)], ['film.js lines', (p) => byId.get(p + '/film.js').lines], ['Lead', busiest]];
  $('#eps').innerHTML = '<thead><tr><th></th>' + P.map((p) => '<th>' + esc(p) + '</th>').join('') + '</tr></thead><tbody>' + rows.map(([lab, f]) => '<tr><td>' + lab + '</td>' + P.map((p) => '<td class="' + (lab === 'Lead' ? '' : 'n') + '">' + esc(f(p)) + '</td>').join('') + '</tr>').join('') + '</tbody>';

  // theme changes repaint the graph
  const rethemed = () => { readTok(); paintChips(); paint(); if (state.sel) panel(state.sel); };
  try { matchMedia('(prefers-color-scheme: dark)').addEventListener('change', rethemed); } catch (e) {}
  new MutationObserver(rethemed).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  window.addEventListener('resize', () => fit(false));

  apply(); draw(); fit(false); panel(null);
})();
</script>
`;
fs.writeFileSync(path.join(OUT, 'graph.html'), html);
console.log('graph.html', (html.length / 1024).toFixed(0) + ' KB');
