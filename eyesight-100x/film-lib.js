// Shared pieces for the film: the cast, the world (sky, sea, sand, cliff, town), props (plane, kite,
// board, keypad, phone) and the LENS: the magnifier that opens on a far-away detail.
(function () {
  const U = globalThis.U, G = globalThis.G, Ch = globalThis.Ch, S = globalThis.SCORE;
  const { clamp, ease, lerp } = U;
  const W = G.W, H = G.H;
  const L = (globalThis.FL = {});

  L.INK = '#2A2320';
  L.CAST = {
    theo: { skin: '#E8B48E', hair: '#5A3A22', hairStyle: 'quiff', outfit: 'hoodie', shirt: '#E0703E', bottoms: 'pants', pants: '#27305C', build: 'slim', shoes: '#F4EDE0' },
    grandpa: { skin: '#D9A07A', hair: '#E4E1DA', hairStyle: 'bald', facialHair: 'beard', outfit: 'shirt', shirt: '#3D7A74', bottoms: 'pants', pants: '#6B5B4B', glasses: 'round', glassesColor: '#6B4A2A' },
    nova: { skin: '#8D5A3B', hair: '#1C1410', hairStyle: 'ponytail', outfit: 'tee', shirt: '#D8352A', bottoms: 'shorts', shorts: '#F2B84B', print: 'GUARD', printColor: '#FFFFFF' },
    black: { skin: '#F0C9A8', hair: '#151515', hairStyle: 'short', outfit: 'suit', robe: '#1C1C22', trim: '#8B1E2B', glasses: 'sun', glassesColor: '#111111' },
    teacher: { skin: '#F3D2B3', hair: '#A8A8A8', hairStyle: 'bun', outfit: 'dress', shirt: '#7E5BA6', glasses: 'square' },
    friend: { skin: '#A86E4B', hair: '#2A1A12', hairStyle: 'curly', outfit: 'tee', shirt: '#3FA89B', bottoms: 'shorts', shorts: '#27305C' },
    boy: { skin: '#E6B48C', hair: '#C8902E', hairStyle: 'short', outfit: 'tee', shirt: '#F2B84B', bottoms: 'shorts', shorts: '#3D7A74' },
    woman: { skin: '#C68B61', hair: '#6B3A1E', hairStyle: 'long', outfit: 'shirt', shirt: '#E8718D', bottoms: 'pants', pants: '#3A3F5C' },
    tourist: { skin: '#F3D2B3', hair: '#C9A26B', hairStyle: 'buzz', outfit: 'shirt', shirt: '#F2B84B', bottoms: 'shorts', shorts: '#8A6A4A', headwear: 'cap', headwearColor: '#3D7A74' },
    cop: { skin: '#A86E4B', hair: '#1C1410', hairStyle: 'short', outfit: 'shirt', shirt: '#2C3E70', bottoms: 'pants', pants: '#1E2440', headwear: 'cap', headwearColor: '#1E2440' },
  };
  globalThis.CAST = L.CAST;

  // ---- timing helpers ----
  L.u = (t, t0, t1) => clamp((t - t0) / (t1 - t0));
  L.pop = (t, t0, d = 0.35) => (t < t0 ? 0 : ease.outBack(clamp((t - t0) / d), 1.8));
  L.fade = (t, t0, d = 0.4) => clamp((t - t0) / d);
  L.after = (t, t0) => t >= t0;

  // ---- the world ----
  L.sky = (ctx, top, bot, y1 = H) => { const g = ctx.createLinearGradient(0, 0, 0, y1); g.addColorStop(0, top); g.addColorStop(1, bot); ctx.fillStyle = g; ctx.fillRect(0, 0, W, y1); };
  L.sun = (ctx, x, y, r, col = '#F2B84B') => G.ellipse(ctx, x, y, r, r, { fill: col, lw: 4, seed: 11 });
  L.cloud = (ctx, x, y, s, seed) => { for (const [dx, dy, r] of [[-60, 10, 46], [0, -10, 60], [64, 8, 44], [20, 20, 50]]) G.ellipse(ctx, x + dx * s, y + dy * s, r * s, r * 0.8 * s, { fill: '#FBF8F1', lw: 3, seed: seed + dx, stroke: 'rgba(42,35,32,0.5)' }); };
  L.sea = (ctx, y0, t, { col = '#3D8A9A', y1 = H + 20, x0 = -40, x1 = W + 40 } = {}) => {
    G.poly(ctx, [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], { fill: col, lw: 4, seed: 21, hatch: { color: 'rgba(255,255,255,0.12)', gap: 14, angle: 0 } });
    for (let i = 0; i < 14; i++) { const yy = y0 + 18 + (i % 5) * ((y1 - y0) / 5.5), xx = ((i * 271 + t * 22 * (1 + (i % 3))) % (x1 - x0 + 200)) + x0 - 100; G.line(ctx, [[xx, yy], [xx + 36, yy - 6], [xx + 72, yy]], { color: 'rgba(255,255,255,0.55)', lw: 3, seed: 30 + i }); }
  };
  L.sand = (ctx, y0, { col = '#E8D9BC', y1 = H + 20 } = {}) => G.poly(ctx, [[-40, y0], [W + 40, y0 + 10], [W + 40, y1], [-40, y1]], { fill: col, lw: 4, seed: 22, hatch: { color: 'rgba(140,100,50,0.14)', gap: 9 } });
  L.cliff = (ctx, x, y, w, { side = 'right', col = '#8A7A5C', grass = '#5E8F5A', h = H - y + 40 } = {}) => {
    const e = side === 'right' ? x : x + w;
    const pts = side === 'right' ? [[x + 40, y], [x + w + 60, y], [x + w + 60, y + h], [x - 30, y + h], [x + 10, y + h * 0.5]] : [[x - 60, y], [x + w - 40, y], [x + w - 10, y + h * 0.5], [x + w + 30, y + h], [x - 60, y + h]];
    G.poly(ctx, pts, { fill: col, lw: 5, seed: 23, hatch: { color: 'rgba(0,0,0,0.16)', gap: 8, angle: 1.1 } });
    G.poly(ctx, side === 'right' ? [[x + 30, y - 12], [x + w + 60, y - 18], [x + w + 60, y + 18], [x + 40, y + 22]] : [[x - 60, y - 18], [x + w - 30, y - 12], [x + w - 40, y + 22], [x - 60, y + 18]], { fill: grass, lw: 4, seed: 24 });
    return e;
  };
  L.hill = (ctx, x, y, w, h, col = '#7FA86A', seed = 40) => G.poly(ctx, [[x, y], [x + w * 0.3, y - h * 0.8], [x + w * 0.55, y - h], [x + w * 0.8, y - h * 0.7], [x + w, y]], { fill: col, lw: 4, seed, hatch: { color: 'rgba(0,0,0,0.12)', gap: 9 } });
  L.town = (ctx, y, seed = 50, { n = 9, x0 = -20, x1 = W + 20, cols = ['#E9B98A', '#D98A6A', '#F1D9A8', '#C9D6C2', '#E8C3B9'] } = {}) => {
    const w = (x1 - x0) / n;
    for (let i = 0; i < n; i++) { const hh = 120 + G.rnd(seed, i) * 140, x = x0 + i * w; G.rrect(ctx, x, y - hh, w + 4, hh + 60, 4, { fill: cols[i % cols.length], lw: 4, seed: seed + i }); G.poly(ctx, [[x - 8, y - hh], [x + w / 2 + 2, y - hh - 50], [x + w + 12, y - hh]], { fill: '#B5553A', lw: 4, seed: seed + 20 + i }); for (let k = 0; k < 2; k++) G.rrect(ctx, x + 22 + k * (w / 2), y - hh + 40, w / 4, 36, 3, { fill: '#5B6F8A', lw: 3, seed: seed + 40 + i * 2 + k }); }
  };
  L.tower = (ctx, x, y, s = 1) => { // a lifeguard tower: legs, hut, red flag
    G.line(ctx, [[x - 60 * s, y], [x - 40 * s, y - 160 * s]], { lw: 6 }); G.line(ctx, [[x + 60 * s, y], [x + 40 * s, y - 160 * s]], { lw: 6 });
    G.rrect(ctx, x - 70 * s, y - 250 * s, 140 * s, 95 * s, 6, { fill: '#F6F0E2', lw: 5, seed: 61 });
    G.poly(ctx, [[x - 85 * s, y - 250 * s], [x, y - 300 * s], [x + 85 * s, y - 250 * s]], { fill: '#D8352A', lw: 5, seed: 62 });
    G.line(ctx, [[x + 70 * s, y - 250 * s], [x + 70 * s, y - 360 * s]], { lw: 4 }); G.poly(ctx, [[x + 70 * s, y - 360 * s], [x + 130 * s, y - 340 * s], [x + 70 * s, y - 320 * s]], { fill: '#D8352A', lw: 3, seed: 63 });
  };

  // ---- props ----
  L.plane = (ctx, x, y, s, flip = 1) => {
    ctx.save(); ctx.translate(x, y); ctx.scale(s * flip, s);
    G.ellipse(ctx, 0, 0, 160, 30, { fill: '#F6F0E2', lw: 5, seed: 70 });
    G.poly(ctx, [[110, -10], [175, -90], [200, -90], [170, -5]], { fill: '#D97757', lw: 5, seed: 71 });
    G.poly(ctx, [[-20, 5], [60, 5], [-40, 90], [-80, 90]], { fill: '#E0D8C6', lw: 5, seed: 72 });
    for (let i = 0; i < 6; i++) G.ellipse(ctx, -100 + i * 32, -6, 7, 8, { fill: '#5B6F8A', lw: 2, seed: 73 + i });
    G.poly(ctx, [[-160, -4], [-130, -22], [-118, -4]], { fill: '#5B6F8A', lw: 3, seed: 80 });
    ctx.restore();
  };
  L.kite = (ctx, x, y, s, t, seed = 90) => {
    G.poly(ctx, [[x, y - 70 * s], [x + 48 * s, y], [x, y + 90 * s], [x - 48 * s, y]], { fill: '#D8352A', lw: 4, seed, hatch: { color: 'rgba(0,0,0,0.12)', gap: 8 } });
    G.line(ctx, [[x, y - 70 * s], [x, y + 90 * s]], { lw: 2.5, seed: seed + 1 }); G.line(ctx, [[x - 48 * s, y], [x + 48 * s, y]], { lw: 2.5, seed: seed + 2 });
    const tail = []; for (let i = 0; i <= 8; i++) tail.push([x + Math.sin(t * 4 + i * 0.8) * 16 * s, y + 90 * s + i * 22 * s]);
    G.line(ctx, tail, { lw: 3, seed: seed + 3 });
    for (let i = 2; i <= 8; i += 3) { const [bx, by] = tail[i]; G.poly(ctx, [[bx - 10 * s, by - 6 * s], [bx + 10 * s, by + 6 * s], [bx + 10 * s, by - 6 * s], [bx - 10 * s, by + 6 * s]], { fill: '#F2B84B', lw: 2, seed: seed + 5 + i }); }
  };
  L.string = (ctx, a, b, sag = 40) => { const pts = []; for (let i = 0; i <= 12; i++) { const k = i / 12; pts.push([lerp(a[0], b[0], k), lerp(a[1], b[1], k) + Math.sin(Math.PI * k) * sag]); } G.line(ctx, pts, { lw: 2, color: 'rgba(42,35,32,0.8)', seed: 99 }); };
  L.board = (ctx, x, y, s, rot = 0, col = '#F08A24') => { ctx.save(); ctx.translate(x, y); ctx.rotate(rot); G.ellipse(ctx, 0, 0, 90 * s, 20 * s, { fill: col, lw: 4, seed: 100 }); G.line(ctx, [[-70 * s, 0], [70 * s, 0]], { lw: 2, color: 'rgba(255,255,255,0.7)', seed: 101 }); ctx.restore(); };
  L.keypad = (ctx, cx, cy, s, t, { pressT = -1, cover = 0 } = {}) => {
    G.rrect(ctx, cx - 150 * s, cy - 190 * s, 300 * s, 380 * s, 18 * s, { fill: '#B9BEC6', lw: 5, seed: 110 });
    G.rrect(ctx, cx - 120 * s, cy - 165 * s, 240 * s, 80 * s, 8 * s, { fill: '#2E4A3A', lw: 3, seed: 111 });
    const n = pressT < 0 ? 0 : Math.min(4, Math.floor((t - pressT) / 0.35) + 1);
    G.text(ctx, '• '.repeat(n).trim() || ' ', cx, cy - 112 * s, { size: 52 * s, align: 'center', color: '#9FF0B8', fam: 'Inter', weight: 800, boil: 0 });
    const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'];
    keys.forEach((k, i) => { const kx = cx + ((i % 3) - 1) * 80 * s, ky = cy - 30 * s + Math.floor(i / 3) * 62 * s; const hit = n > 0 && i === [3, 7, 1, 9][Math.min(3, n - 1)] && (t - pressT) % 0.35 < 0.18; G.rrect(ctx, kx - 32 * s, ky - 24 * s, 64 * s, 48 * s, 8 * s, { fill: hit ? '#F2B84B' : '#EDEFF2', lw: 3, seed: 120 + i }); G.text(ctx, k, kx, ky + 12 * s, { size: 30 * s, align: 'center', fam: 'Inter', weight: 700, boil: 0 }); });
    if (cover > 0) { ctx.save(); ctx.globalAlpha = cover; G.ellipse(ctx, cx + 20 * s, cy + 50 * s, 150 * s, 120 * s, { fill: '#C68B61', lw: 5, seed: 130 }); for (let f = 0; f < 4; f++) G.line(ctx, [[cx - 80 * s + f * 48 * s, cy - 40 * s], [cx - 70 * s + f * 48 * s, cy + 40 * s]], { lw: 3, color: 'rgba(42,35,32,0.5)', seed: 131 + f }); ctx.restore(); }
  };
  L.label = (ctx, str, x, y, { size = 46, color = L.INK, align = 'center', alpha = 1, fam = 'Permanent Marker', rot = 0 } = {}) => { if (alpha <= 0) return; ctx.save(); ctx.translate(x, y); ctx.rotate(rot); G.text(ctx, str, 0, 0, { size, color, align, alpha, fam, weight: 400 }); ctx.restore(); };
  L.stampText = (ctx, t, t0, str, x, y, o = {}) => { const k = L.pop(t, t0, 0.3); if (k <= 0) return; ctx.save(); ctx.translate(x, y); ctx.scale(k, k); ctx.rotate(o.rot || 0); G.text(ctx, str, 0, 0, { size: o.size || 120, align: 'center', fam: o.fam || 'Bungee', weight: 400, color: o.color || '#E0703E', stroke: L.INK, strokeW: o.strokeW || 10 }); ctx.restore(); };
  L.card = (ctx, t, t0, x, y, w, h, draw, { rot = 0, seed = 140, fill = '#F6F0E2' } = {}) => {
    const k = L.pop(t, t0, 0.4); if (k <= 0) return;
    ctx.save(); ctx.translate(x + w / 2, y + h / 2); ctx.scale(k, k); ctx.rotate(rot);
    G.tornPaper(ctx, -w / 2, -h / 2, w, h, { fill, seed, shadow: true });
    ctx.save(); ctx.beginPath(); ctx.rect(-w / 2 + 14, -h / 2 + 14, w - 28, h - 28); ctx.clip(); draw(ctx, w - 28, h - 28); ctx.restore();
    ctx.restore();
  };

  // ---- the LENS ----
  // opens at t0 with an overshoot on a target (tx, ty) far away, magnified into a circle at (cx, cy)
  L.lens = (ctx, t, t0, t1, o, content) => {
    if (t < t0 || t >= t1) return;
    const { tx, ty, cx, cy, r } = o;
    const k = ease.outBack(clamp((t - t0) / 0.32), 1.6) * (1 - ease.inQuad(clamp((t - (t1 - 0.25)) / 0.25)));
    if (k <= 0.001) return;
    const rr = r * k, X = lerp(tx, cx, ease.outCubic(clamp((t - t0) / 0.32))), Y = lerp(ty, cy, ease.outCubic(clamp((t - t0) / 0.32)));
    // the target reticle
    G.ellipse(ctx, tx, ty, 16, 16, { fill: null, stroke: '#F6F0E2', lw: 6, seed: 150 }); G.ellipse(ctx, tx, ty, 16, 16, { fill: null, stroke: L.INK, lw: 2.5, seed: 151 });
    // the cone from the target to the lens
    const a = Math.atan2(Y - ty, X - tx), p = a + Math.PI / 2;
    ctx.save(); ctx.globalAlpha = 0.85;
    ctx.fillStyle = 'rgba(246,240,226,0.28)'; ctx.beginPath(); ctx.moveTo(tx, ty); ctx.lineTo(X + Math.cos(p) * rr, Y + Math.sin(p) * rr); ctx.lineTo(X - Math.cos(p) * rr, Y - Math.sin(p) * rr); ctx.closePath(); ctx.fill();
    G.line(ctx, [[tx, ty], [X + Math.cos(p) * rr, Y + Math.sin(p) * rr]], { lw: 2.5, color: L.INK, seed: 152 }); G.line(ctx, [[tx, ty], [X - Math.cos(p) * rr, Y - Math.sin(p) * rr]], { lw: 2.5, color: L.INK, seed: 153 });
    ctx.restore();
    // the glass
    ctx.save(); ctx.fillStyle = 'rgba(20,10,20,0.25)'; ctx.beginPath(); ctx.arc(X + 10, Y + 14, rr + 18, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    ctx.save(); ctx.beginPath(); ctx.arc(X, Y, rr, 0, Math.PI * 2); ctx.clip();
    ctx.translate(X, Y); ctx.scale(k, k); content(ctx, r); ctx.restore();
    ctx.save(); ctx.globalAlpha = 0.35; ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 10; ctx.beginPath(); ctx.arc(X, Y, rr * 0.82, Math.PI * 1.1, Math.PI * 1.45); ctx.stroke(); ctx.restore();
    G.ellipse(ctx, X, Y, rr + 8, rr + 8, { fill: null, stroke: '#F6F0E2', lw: 16, seed: 154 });
    G.ellipse(ctx, X, Y, rr + 16, rr + 16, { fill: null, stroke: L.INK, lw: 5, seed: 155 });
    G.ellipse(ctx, X, Y, rr, rr, { fill: null, stroke: L.INK, lw: 4, seed: 156 });
    if (o.tag) L.label(ctx, o.tag, X, Y + rr + 62, { size: 34, alpha: clamp((t - t0 - 0.2) * 4), fam: 'Patrick Hand' });
  };
  L.lensT = (id) => S.lens.find((l) => l.id === id).t;

  // ---- an eye icon (for diagrams) ----
  L.eye = (ctx, x, y, s, { look = 0, iris = '#3D7A74', glow = 0 } = {}) => {
    if (glow > 0) G.rays(ctx, x, y, { n: 18, r0: 120 * s, r1: 230 * s, color: `rgba(242,184,75,${0.5 * glow})`, lw: 10, seed: 160 });
    G.poly(ctx, [[x - 120 * s, y], [x - 60 * s, y - 60 * s], [x + 60 * s, y - 60 * s], [x + 120 * s, y], [x + 60 * s, y + 60 * s], [x - 60 * s, y + 60 * s]], { fill: '#FBF8F1', lw: 5, seed: 161 });
    G.ellipse(ctx, x + look * 30 * s, y, 46 * s, 46 * s, { fill: iris, lw: 4, seed: 162 });
    G.ellipse(ctx, x + look * 30 * s, y, 20 * s, 20 * s, { fill: '#1A1414', lw: 2, seed: 163 });
    G.ellipse(ctx, x + look * 30 * s - 12 * s, y - 14 * s, 8 * s, 8 * s, { fill: '#FFFFFF', lw: 0, seed: 164, stroke: null });
  };
  // a dark smudge over the centre of a view: macular degeneration (central vision lost, edges stay)
  L.smudge = (ctx, x, y, r, a = 1) => { const g = ctx.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, `rgba(40,34,38,${0.92 * a})`); g.addColorStop(0.55, `rgba(70,62,66,${0.75 * a})`); g.addColorStop(1, 'rgba(70,62,66,0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); };
  // warm light / tension light over a scene
  L.light = (ctx, cx, cy, inner, outer, mode = 'multiply', a = 1) => { const g = ctx.createRadialGradient(cx, cy, 50, cx, cy, Math.max(W, H)); g.addColorStop(0, inner); g.addColorStop(1, outer); ctx.save(); ctx.globalCompositeOperation = mode; ctx.globalAlpha = a; ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); ctx.restore(); };
})();
