// THE KIT: the cast, the props and the little helpers every scene shares. Pure functions of t.
(function () {
  const U = globalThis.U, G = globalThis.G, Ch = globalThis.Ch;
  const { clamp, ease, lerp } = U;
  const K = {};
  const INK = '#2A2320';
  K.INK = INK;
  K.PAPER = '#F4EDE0';
  K.RED = '#D8483B';
  K.ORANGE = '#E0703E';
  K.TEAL = '#3FA89B';
  K.GOLD = '#F2B84B';
  K.NIGHT = '#1E1B2E';

  // ---------- the cast ----------
  K.SAM = { hairStyle: 'short', hair: '#3B2A20', skin: '#E2AE86', outfit: 'hoodie', shirt: '#E0703E', bottoms: 'pants', shorts: '#2E3A59', shoes: '#F4F1EA' };
  K.LEO = { hairStyle: 'curly', hair: '#C8742F', skin: '#F3D2B3', freckles: true, glasses: 'round', glassesColor: '#2A2320', outfit: 'tee', shirt: '#3FA89B', bottoms: 'pants', shorts: '#5A4A3A', build: 'slim', shoes: '#C23B3B' };
  K.MIA = { hairStyle: 'ponytail', hair: '#1E1A18', skin: '#A86E4B', outfit: 'tee', shirt: '#B79CFF', bottoms: 'skirt', shorts: '#27305C' };
  K.BLACK = { outfit: 'suit', robe: '#1C1C22', trim: '#B32020', glasses: 'sun', glassesColor: '#C9A23A', hairStyle: 'quiff', hair: '#111111', facialHair: 'stubble', skin: '#D9A47F', build: 'broad' };
  K.KEEPER = { outfit: 'shirt', shirt: '#6B8E3D', headwear: 'cap', headwearColor: '#4A6B2A', hairStyle: 'short', facialHair: 'beard', hair: '#7A5A3A', skin: '#C98A62', bottoms: 'shorts', shorts: '#8A7A5A' };
  K.SM = { hairStyle: 'long', hair: '#8A6A4A', skin: '#F0C9A8', outfit: 'shirt', shirt: '#E8E1CF', bottoms: 'pants', shorts: '#4A5A7A' };
  K.KID1 = { hairStyle: 'bun', hair: '#5A3A22', skin: '#C98A62', outfit: 'tee', shirt: '#F2B84B', bottoms: 'pants', shorts: '#3A4A6A' };
  K.KID2 = { hairStyle: 'buzz', hair: '#1A1A1A', skin: '#8D5A3B', outfit: 'hoodie', shirt: '#4A7BC0', bottoms: 'pants', shorts: '#2A2A30' };
  K.ADULT = { hairStyle: 'short', hair: '#6A5A4A', skin: '#F3D2B3', outfit: 'shirt', shirt: '#7A9CC6', bottoms: 'pants', shorts: '#3A3A44' };
  globalThis.CAST = { sam: K.SAM, leo: K.LEO, mia: K.MIA, black: K.BLACK, keeper: K.KEEPER };

  K.KID = 0.82; // kids are drawn smaller than grown-ups
  K.person = (ctx, o) => Ch.person(ctx, { pose: 'stand', s: K.KID, ...o });
  // Sam's face never shows fear: calm eyes, flat mouth, unless the scene says otherwise
  K.sam = (ctx, o) => K.person(ctx, { style: K.SAM, eyes: 'normal', mouth: 'flat', seed: 100, ...o });
  K.leo = (ctx, o) => K.person(ctx, { style: K.LEO, seed: 200, ...o });
  K.mia = (ctx, o) => K.person(ctx, { style: K.MIA, seed: 300, ...o });
  K.black = (ctx, o) => Ch.person(ctx, { pose: 'stand', s: 1.05, style: K.BLACK, mouth: 'smirk', seed: 400, ...o });

  // ---------- text ----------
  // a stamp: full size on its first frame (a clean hit), settling from 135% to 100%
  K.stampK = (t, t0) => (t < t0 ? 0 : 1 + 0.35 * (1 - ease.outCubic(clamp((t - t0) / 0.2))));
  K.stamp = (ctx, str, x, y, t, t0, o = {}) => {
    const k = K.stampK(t, t0);
    if (k <= 0) return;
    ctx.save(); ctx.translate(x, y); ctx.scale(k, k); ctx.rotate(o.rot || 0);
    G.text(ctx, str, 0, 0, { size: o.size || 110, align: 'center', fam: o.fam || 'Bungee', weight: 400, color: o.color || K.ORANGE, stroke: o.stroke ?? INK, strokeW: o.strokeW ?? 10, alpha: o.alpha });
    ctx.restore();
  };
  // a handwritten label that fades and drifts up into place
  K.label = (ctx, str, x, y, t, t0, o = {}) => {
    const a = clamp((t - t0) / 0.3);
    if (a <= 0) return;
    G.text(ctx, str, x, y + (1 - ease.outCubic(a)) * 20, { size: o.size || 54, align: o.align || 'center', fam: o.fam || 'Patrick Hand', weight: 400, color: o.color || INK, alpha: a * (o.alpha ?? 1), stroke: o.stroke, strokeW: o.strokeW });
  };
  // a card of paper with text, taped up
  K.card = (ctx, x, y, w, h, t, t0, draw, o = {}) => {
    const a = clamp((t - t0) / 0.35);
    if (a <= 0) return;
    ctx.save(); ctx.globalAlpha *= a; ctx.translate(x + w / 2, y + h / 2 + (1 - ease.outBack(a)) * 40); ctx.rotate(o.rot || 0); ctx.translate(-w / 2, -h / 2);
    G.tornPaper(ctx, 0, 0, w, h, { fill: o.fill || '#FBF7EE', seed: o.seed || 7 });
    if (o.tape !== false) G.tape(ctx, w / 2 - 60, -18, 120, 36, 0.04, (o.seed || 7) + 1);
    draw(ctx, w, h);
    ctx.restore();
  };

  // ---------- backgrounds ----------
  K.room = (ctx, wall, floor, seed = 1) => {
    G.bg(ctx, wall);
    G.poly(ctx, [[-40, 860], [1960, 860], [1960, 1120], [-40, 1120]], { fill: floor, lw: 5, seed, hatch: { color: 'rgba(0,0,0,0.10)', gap: 10 } });
  };
  K.sky = (ctx, top, bottom) => {
    const g = ctx.createLinearGradient(0, 0, 0, G.H);
    g.addColorStop(0, top); g.addColorStop(1, bottom);
    ctx.fillStyle = g; ctx.fillRect(-200, -200, G.W + 400, G.H + 400);
  };
  K.stars = (ctx, t, n = 80, seed = 3, alpha = 1) => {
    for (let i = 0; i < n; i++) {
      const x = G.rnd(seed, i) * G.W, y = G.rnd(seed, i, 2) * G.H * 0.7;
      const tw = 0.5 + 0.5 * Math.sin(t * 2 + i);
      ctx.fillStyle = `rgba(255,248,220,${alpha * (0.35 + 0.6 * tw)})`;
      ctx.fillRect(x, y, 3, 3);
    }
  };
  K.dark = (ctx, a) => { if (a <= 0) return; ctx.save(); ctx.fillStyle = `rgba(10,8,16,${a})`; ctx.fillRect(-200, -200, G.W + 400, G.H + 400); ctx.restore(); };
  K.flash = (ctx, t, t0, dur = 0.2, color = '255,255,255') => { if (t < t0 || t > t0 + dur) return; ctx.save(); ctx.fillStyle = `rgba(${color},${0.8 * (1 - (t - t0) / dur)})`; ctx.fillRect(-200, -200, G.W + 400, G.H + 400); ctx.restore(); };
  K.vignette = (ctx, a = 0.6, cx = G.W / 2, cy = G.H / 2) => {
    const g = ctx.createRadialGradient(cx, cy, 200, cx, cy, 1200);
    g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, `rgba(0,0,0,${a})`);
    ctx.fillStyle = g; ctx.fillRect(-200, -200, G.W + 400, G.H + 400);
  };
  // a soft spotlight cone from above
  K.spot = (ctx, x, y, r, a = 0.25) => {
    const g = ctx.createRadialGradient(x, y, 10, x, y, r);
    g.addColorStop(0, `rgba(255,240,200,${a})`); g.addColorStop(1, 'rgba(255,240,200,0)');
    ctx.fillStyle = g; ctx.fillRect(x - r, y - r, r * 2, r * 2);
  };

  // ---------- the recurring object: a fear meter ----------
  // value 0..1; Sam's always reads ZERO, everyone else's spikes
  K.meter = (ctx, x, y, r, value, o = {}) => {
    ctx.save(); ctx.translate(x, y);
    G.ellipse(ctx, 0, 0, r * 1.12, r * 1.12, { fill: o.face || '#FBF7EE', lw: 5, seed: (o.seed || 1) });
    const a0 = Math.PI * 1.15, a1 = Math.PI * 1.85;
    const seg = 24;
    for (let i = 0; i < seg; i++) {
      const u = i / seg, a = lerp(a0, a1, u), b = lerp(a0, a1, (i + 1) / seg);
      ctx.beginPath(); ctx.arc(0, 0, r * 0.82, a, b + 0.01); ctx.lineWidth = r * 0.22;
      ctx.strokeStyle = u < 0.33 ? '#6BBF7A' : u < 0.66 ? K.GOLD : K.RED; ctx.stroke();
    }
    const v = clamp(value) + (o.shake || 0) * Math.sin((o.t || 0) * 50) * 0.03;
    const a = lerp(a0, a1, clamp(v));
    G.line(ctx, [[0, 0], [Math.cos(a) * r * 0.86, Math.sin(a) * r * 0.86]], { color: INK, lw: Math.max(4, r * 0.07), seed: (o.seed || 1) + 2 });
    G.ellipse(ctx, 0, 0, r * 0.1, r * 0.1, { fill: INK, lw: 3, seed: (o.seed || 1) + 3 });
    G.text(ctx, o.label || 'FEAR', 0, r * 0.5, { size: r * 0.26, align: 'center', fam: 'Bungee', weight: 400, color: INK });
    ctx.restore();
  };

  // ---------- creatures and props ----------
  K.spider = (ctx, x, y, s, t, o = {}) => {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(o.rot || 0);
    for (let sd = -1; sd <= 1; sd += 2) for (let i = 0; i < 4; i++) {
      const ph = Math.sin(t * 14 + i * 1.6 + (sd > 0 ? Math.PI : 0)) * (o.walk ? 0.25 : 0.05);
      const a = (-0.9 + i * 0.6 + ph) * sd;
      const kx = sd * (34 + i * 3), ky = -16 + i * 10;
      G.line(ctx, [[sd * 10, i * 6 - 6], [kx, ky - 22], [kx + sd * 26 * Math.cos(a), ky + 30 + Math.sin(a) * 10]], { color: '#1B1820', lw: 6, seed: 30 + i + sd * 7, amp: 0.6 });
    }
    G.ellipse(ctx, 0, 16, 30, 34, { fill: '#2B2630', lw: 4, seed: 41, hatch: { color: 'rgba(255,255,255,0.12)', gap: 6 } });
    G.ellipse(ctx, 0, -20, 20, 18, { fill: '#2B2630', lw: 4, seed: 42 });
    for (const ex of [-7, 7]) G.ellipse(ctx, ex, -24, 5, 5, { fill: '#FFFFFF', lw: 0, seed: 43 });
    ctx.restore();
  };
  K.monster = (ctx, x, y, s, t, o = {}) => {
    ctx.save(); ctx.translate(x, y); ctx.scale(s * (o.sx || 1), s);
    const breathe = 1 + Math.sin(t * 3) * 0.02;
    ctx.scale(1, breathe);
    // arms up, claws out
    for (const sd of [-1, 1]) {
      const up = o.arms ?? 1;
      G.limb(ctx, [[sd * 90, -260], [sd * 170, -300 - 60 * up], [sd * 190, -380 - 90 * up]], { color: '#6A3D8F', lw: 44, outline: 5, seed: 50 + sd });
      for (let c = -1; c <= 1; c++) G.poly(ctx, [[sd * 190 + c * 16, -400 - 90 * up], [sd * 194 + c * 22, -440 - 90 * up], [sd * 200 + c * 12, -398 - 90 * up]], { fill: '#F4EDE0', lw: 3, seed: 60 + c });
    }
    G.shape(ctx, G.wobble(G.ellPts(0, -190, 150, 200), 51, 10), { fill: '#7B4BA3', lw: 6, seed: 52, hatch: { color: 'rgba(0,0,0,0.18)', gap: 9, angle: 0.6 } });
    for (const sd of [-1, 1]) G.poly(ctx, [[sd * 60, -360], [sd * 100, -460], [sd * 110, -350]], { fill: '#E8D9BC', lw: 5, seed: 53 + sd });
    const ey = o.scared ? 1.5 : 1;
    for (const sd of [-1, 1]) { G.ellipse(ctx, sd * 50, -270, 30 * ey, 34 * ey, { fill: '#FFF6C8', lw: 4, seed: 55 + sd }); G.ellipse(ctx, sd * 50 + (o.look || 0) * 10, -266, 11, 13, { fill: INK, lw: 0, seed: 57 }); }
    if (o.scared) {
      G.ellipse(ctx, 0, -175, 34, 42, { fill: '#3A1630', lw: 5, seed: 58 });
    } else {
      G.shape(ctx, [[-80, -200], [80, -200], [60, -140], [-60, -140]], { fill: '#3A1630', lw: 5, seed: 58, closed: true });
      for (let i = 0; i < 5; i++) G.poly(ctx, [[-64 + i * 32, -200], [-48 + i * 32, -170], [-32 + i * 32, -200]], { fill: '#FFFFFF', lw: 3, seed: 59 + i });
    }
    for (const sd of [-1, 1]) G.rrect(ctx, sd * 70 - 30, -20, 60, 30, 12, { fill: '#5A2F7A', lw: 5, seed: 64 + sd });
    ctx.restore();
  };
  // a snake along a path of points (the body follows the path, the head at the end)
  K.snake = (ctx, pts, o = {}) => {
    const lw = o.lw || 34;
    G.limb(ctx, pts, { color: o.color || '#7FA74A', lw, outline: 5, seed: o.seed || 70 });
    for (let i = 2; i < pts.length - 1; i += 2) G.ellipse(ctx, pts[i][0], pts[i][1], lw * 0.22, lw * 0.18, { fill: '#4E7A2A', lw: 0, seed: 71 + i });
    const [hx, hy] = pts[pts.length - 1], [px, py] = pts[pts.length - 2];
    const a = Math.atan2(hy - py, hx - px);
    ctx.save(); ctx.translate(hx, hy); ctx.rotate(a);
    G.ellipse(ctx, 6, 0, lw * 0.85, lw * 0.6, { fill: o.color || '#7FA74A', lw: 5, seed: 72 });
    G.ellipse(ctx, 12, -lw * 0.25, 5, 5, { fill: INK, lw: 0, seed: 73 });
    if (o.tongue) G.line(ctx, [[lw * 0.8, 0], [lw * 1.4, 0], [lw * 1.6, -6]], { color: K.RED, lw: 3, seed: 74 });
    ctx.restore();
  };
  // a snake that slithers: n points along a sine wave from (x0,y) to (x1,y)
  K.slither = (x0, x1, y, t, n = 18, amp = 26) => Array.from({ length: n }, (_, i) => { const u = i / (n - 1); return [lerp(x0, x1, u), y + Math.sin(u * 9 - t * 6) * amp * (0.4 + 0.6 * u)]; });
  K.heartIcon = (ctx, x, y, s, beat = 0, color = K.RED) => {
    const k = s * (1 + 0.18 * beat);
    G.heart(ctx, x, y, k);
    ctx.save(); ctx.globalCompositeOperation = 'source-atop'; ctx.restore();
    void color;
  };
  K.bolt = (ctx, x, y, s, color = K.GOLD, seed = 80) => G.poly(ctx, [[x, y], [x + 30 * s, y], [x + 8 * s, y + 50 * s], [x + 34 * s, y + 50 * s], [x - 14 * s, y + 120 * s], [x + 2 * s, y + 66 * s], [x - 22 * s, y + 66 * s]], { fill: color, lw: 4, seed });
  K.phone = (ctx, x, y, w, h, o = {}) => {
    G.rrect(ctx, x, y, w, h, w * 0.14, { fill: '#26242C', lw: 5, seed: o.seed || 90 });
    ctx.fillStyle = o.screen || '#DDEFF8'; ctx.fillRect(x + w * 0.08, y + h * 0.07, w * 0.84, h * 0.86);
  };
  K.live = (ctx, x, y, t, o = {}) => {
    const blink = Math.sin(t * 5) > -0.3 ? 1 : 0.3;
    G.rrect(ctx, x, y, 150, 56, 12, { fill: '#D8202A', lw: 4, seed: 91 });
    ctx.fillStyle = `rgba(255,255,255,${blink})`; ctx.beginPath(); ctx.arc(x + 28, y + 28, 10, 0, Math.PI * 2); ctx.fill();
    G.text(ctx, 'LIVE', x + 90, y + 40, { size: 34, align: 'center', fam: 'Bungee', weight: 400, color: '#FFFFFF', boil: 0 });
    if (o.viewers) G.text(ctx, o.viewers, x + 170, y + 40, { size: 34, align: 'left', fam: 'Inter', weight: 800, color: o.color || '#FFFFFF', boil: 0 });
  };
  // the old dock crane: a lattice mast at mx with a beam reaching right at height by
  K.crane = (ctx, mx, base, top, beamTo, o = {}) => {
    const c = o.color || '#E8A43A', w = 90;
    G.poly(ctx, [[mx - w / 2, base], [mx + w / 2, base], [mx + w / 2, top], [mx - w / 2, top]], { fill: null, stroke: INK, lw: 6, seed: 120 });
    G.line(ctx, [[mx - w / 2, base], [mx - w / 2, top]], { color: c, lw: 14, seed: 121 });
    G.line(ctx, [[mx + w / 2, base], [mx + w / 2, top]], { color: c, lw: 14, seed: 122 });
    for (let y = base, i = 0; y > top; y -= 70, i++) G.line(ctx, [[mx - w / 2, y], [mx + w / 2, y - 70]], { color: c, lw: 8, seed: 123 + i });
    // the beam
    G.rrect(ctx, mx - 220, top - 34, beamTo - mx + 220, 34, 4, { fill: c, lw: 5, seed: 140, hatch: { color: 'rgba(0,0,0,0.15)', gap: 12 } });
    for (let x = mx - 200, i = 0; x < beamTo - 20; x += 60, i++) G.line(ctx, [[x, top - 30], [x + 30, top - 4]], { color: 'rgba(0,0,0,0.35)', lw: 4, seed: 141 + i });
    // cab and counterweight
    G.rrect(ctx, mx - 70, top, 140, 90, 8, { fill: '#C9C2B4', lw: 5, seed: 150 });
    G.rrect(ctx, mx - 50, top + 18, 50, 40, 4, { fill: '#9FD3F0', lw: 4, seed: 151 });
    G.rrect(ctx, mx - 260, top - 10, 80, 90, 6, { fill: '#5A5560', lw: 5, seed: 152 });
  };
  // a ladder from (x, y0) up to (x, y1)
  K.ladder = (ctx, x, y0, y1, o = {}) => {
    const w = o.w || 70;
    G.line(ctx, [[x - w / 2, y0], [x - w / 2, y1]], { color: '#8A8A90', lw: 8, seed: 160 });
    G.line(ctx, [[x + w / 2, y0], [x + w / 2, y1]], { color: '#8A8A90', lw: 8, seed: 161 });
    for (let y = y0, i = 0; y > y1; y -= (o.rung || 46), i++) G.line(ctx, [[x - w / 2, y], [x + w / 2, y]], { color: '#8A8A90', lw: 6, seed: 162 + i });
  };
  K.waves = (ctx, y, t, color = '#3D6E8A') => {
    const pts = []; for (let x = -100; x <= G.W + 100; x += 40) pts.push([x, y + Math.sin(x * 0.01 + t * 1.5) * 10]);
    G.poly(ctx, [...pts, [G.W + 100, G.H + 100], [-100, G.H + 100]], { fill: color, lw: 5, seed: 170, hatch: { color: 'rgba(255,255,255,0.12)', gap: 14 } });
  };
  K.cameraBot = (ctx, x, y, s, t, seed = 180) => {
    ctx.save(); ctx.translate(x, y + Math.sin(t * 2 + seed) * 8); ctx.scale(s, s);
    G.rrect(ctx, -40, -26, 80, 52, 10, { fill: '#3A3844', lw: 4, seed });
    G.ellipse(ctx, 0, 0, 18, 18, { fill: '#9FD3F0', lw: 4, seed: seed + 1 });
    ctx.fillStyle = Math.sin(t * 6 + seed) > 0 ? '#FF3030' : '#801818'; ctx.beginPath(); ctx.arc(28, -16, 6, 0, Math.PI * 2); ctx.fill();
    for (const sd of [-1, 1]) G.line(ctx, [[sd * 30, -26], [sd * 60, -46]], { color: INK, lw: 4, seed: seed + 2 });
    for (const sd of [-1, 1]) G.ellipse(ctx, sd * 64, -48, 26 * Math.abs(Math.sin(t * 40 + sd)), 5, { fill: 'rgba(200,200,210,0.7)', lw: 2, seed: seed + 3 });
    ctx.restore();
  };
  // speech bubble that pops in at t0 and out at t1
  K.bubble = (ctx, text, x, y, tx, ty, t, t0, t1, size = 40) => G.bubble(ctx, text, x, y, tx, ty, t, t0, t1, { size });

  globalThis.K = K;
})();
