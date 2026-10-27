// THE FILM: 28 scenes, one per block of the script, each a pure function of t. Scene and line times come
// from score.js (the measured voiceover); the lens pops are the same events the song plays tings on.
(function () {
  const U = globalThis.U, G = globalThis.G, Ch = globalThis.Ch, UI = globalThis.UI, Data = globalThis.Data, Subs = globalThis.Subs, S = globalThis.SCORE, Studio = globalThis.Studio, L = globalThis.FL;
  const { clamp, ease, lerp } = U;
  const W = G.W, H = G.H, C = L.CAST, INK = L.INK;
  let VO = null, SUBS = [];
  const talk = (t, who, rest = 'smile') => { if (!VO) return rest; const mo = Subs.mouth(VO, t, who); return mo.talking ? mo : rest; };
  const A = (scene, txt) => S.at(scene, txt);
  const E = (scene, txt) => S.end(scene, txt);
  const P = (o) => Ch.person(o.ctx, o);
  const person = (ctx, o) => Ch.person(ctx, o);
  const blinkAt = (t, seed) => { const p = (t + seed * 1.7) % 3.7; return p < 0.12 ? 1 : 0; };

  // ================= the opening: the beach, the Moon, the hill =================
  function beach(ctx, t, s) {
    L.sky(ctx, '#9FD3EA', '#F4EDE0', 640);
    L.cloud(ctx, 300, 180, 1, 1); L.cloud(ctx, 1500, 130, 0.8, 2);
    L.sea(ctx, 600, t); L.sand(ctx, 760);
    const px = lerp(2150, -250, L.u(t, s.t0, s.t1 + 1.5)), py = 230;
    L.plane(ctx, px, py, 0.55, -1);
    person(ctx, { x: 980, y: 1000, s: 1.05, pose: 'stand', style: C.theo, lookY: -1, look: 0.4, eyes: t > L.lensT('plane') ? 'wide' : 'normal', mouth: t > L.lensT('pilot') ? 'grin' : 'o', blink: blinkAt(t, 1), seed: 300 });
    L.lens(ctx, t, L.lensT('plane'), L.lensT('pilot') - 0.05, { tx: px + 60, ty: py - 25, cx: 1420, cy: 470, r: 210, tag: 'the tail' }, (c, r) => {
      c.fillStyle = '#AFDCEE'; c.fillRect(-r, -r, 2 * r, 2 * r);
      G.poly(c, [[-260, 120], [-60, -150], [60, -150], [-20, 140]], { fill: '#D97757', lw: 6, seed: 170 });
      G.text(c, 'GULL', -40, -10, { size: 64, align: 'center', fam: 'Bungee', weight: 400, color: '#F6F0E2', stroke: INK, strokeW: 6, rot: -0.2 });
      G.text(c, 'AIR', -60, 60, { size: 56, align: 'center', fam: 'Bungee', weight: 400, color: '#F6F0E2', stroke: INK, strokeW: 6 });
    });
    L.lens(ctx, t, L.lensT('pilot'), s.t1, { tx: px - 80, ty: py - 8, cx: 1420, cy: 470, r: 210, tag: 'the pilot' }, (c, r) => {
      c.fillStyle = '#F6F0E2'; c.fillRect(-r, -r, 2 * r, 2 * r);
      G.rrect(c, -150, -150, 300, 230, 40, { fill: '#BFE3F0', lw: 8, seed: 171 });
      c.save(); c.beginPath(); c.roundRect(-150, -150, 300, 230, 40); c.clip();
      person(c, { x: 0, y: 330, s: 0.95, pose: 'stand', style: { ...C.tourist, headwear: 'cap', headwearColor: '#27305C', shirt: '#F6F0E2' }, gesture: 'wave', mouth: 'grin', eyes: 'happy', t, shadow: false, seed: 320 });
      c.restore();
    });
  }
  function moon(ctx, t, s) {
    L.sky(ctx, '#2E2A5C', '#D98A6A', H);
    for (let i = 0; i < 40; i++) G.star(ctx, G.rnd(i, 1) * W, G.rnd(i, 2) * 500, 3 + G.rnd(i, 3) * 4, { fill: '#F6F0E2' });
    G.ellipse(ctx, 1500, 200, 46, 46, { fill: '#F3EBD2', lw: 4, seed: 180 });
    L.sea(ctx, 700, t, { col: '#2F5E78' }); L.sand(ctx, 840, { col: '#C9B48E' });
    person(ctx, { x: 600, y: 1010, s: 1.0, pose: 'stand', style: C.theo, lookY: -1, look: 0.9, eyes: 'wide', mouth: 'o', blink: blinkAt(t, 2), seed: 300 });
    L.lens(ctx, t, L.lensT('moon'), s.t1, { tx: 1500, ty: 200, cx: 1250, cy: 520, r: 260, tag: 'no telescope' }, (c, r) => {
      c.fillStyle = '#11163A'; c.fillRect(-r, -r, 2 * r, 2 * r);
      G.ellipse(c, 0, 0, 230, 230, { fill: '#E9E2CC', lw: 5, seed: 181, hatch: { color: 'rgba(0,0,0,0.08)', gap: 10 } });
      const cr = [[-80, -60, 46], [60, -100, 30], [90, 50, 56], [-40, 90, 34], [-130, 40, 22], [20, -10, 18], [140, -30, 16]];
      cr.forEach(([x, y, rr], i) => { if (t < L.lensT('moon') + 0.2 + i * 0.12) return; G.ellipse(c, x, y, rr, rr * 0.85, { fill: '#CFC6AC', lw: 3, seed: 182 + i }); G.ellipse(c, x + rr * 0.15, y + rr * 0.12, rr * 0.7, rr * 0.55, { fill: '#BDB397', lw: 0, stroke: null, seed: 190 + i }); });
      if (t > A('moon', 'Craters') + 0.9) { G.poly(c, [[-200, 140], [-150, 90], [-110, 130], [-60, 70], [-20, 140]], { fill: '#A79D82', lw: 3, seed: 200 }); }
      if (t > A('moon', 'Craters') + 1.6) { c.save(); c.globalAlpha = 0.55; c.fillStyle = '#11163A'; c.beginPath(); c.ellipse(140, 0, 120, 232, 0, -Math.PI / 2, Math.PI / 2); c.lineTo(230, 230); c.lineTo(230, -230); c.fill(); c.restore(); }
    });
  }
  function hill(ctx, t, s) {
    L.sky(ctx, '#A9D8EC', '#F4EDE0', 700);
    L.hill(ctx, 1150, 640, 800, 230, '#93B97A', 41); L.hill(ctx, -100, 700, 900, 160, '#7FA86A', 42);
    L.sea(ctx, 690, t); L.sand(ctx, 780);
    // the tiny man on the far hill
    G.ellipse(ctx, 1560, 418, 4, 4, { fill: '#E8B48E', lw: 1.5, seed: 210 }); G.line(ctx, [[1560, 422], [1560, 436]], { lw: 3, color: '#3D7A74' });
    const pt = A('hill', 'points');
    person(ctx, { x: 520, y: 1010, s: 0.95, pose: 'stand', style: C.friend, gesture: t > pt + 0.3 ? 'point' : null, look: 1, mouth: talk(t, 'friend', 'smile'), seed: 330 });
    person(ctx, { x: 980, y: 1010, s: 1.0, pose: 'stand', style: C.theo, look: 1, lookY: -0.3, eyes: t > A('hill', 'squint') ? 'happy' : 'normal', brows: t > A('hill', 'squint') ? 'determined' : 'neutral', mouth: t > L.lensT('mustard') ? 'grin' : 'flat', seed: 300 });
    L.lens(ctx, t, L.lensT('man'), s.t1, { tx: 1560, ty: 428, cx: 1420, cy: 690, r: 230, tag: '2 km away' }, (c, r) => {
      c.fillStyle = '#B9DDE6'; c.fillRect(-r, -r, 2 * r, 2 * r);
      G.poly(c, [[-r, 120], [r, 90], [r, r], [-r, r]], { fill: '#93B97A', lw: 4, seed: 211 });
      person(c, { x: 0, y: 330, s: 0.9, pose: 'stand', style: { ...C.tourist, headwear: 'none', shirt: '#3D7A74' }, handR: [40, -380], mouth: Math.sin(t * 9) > 0 ? 'open' : 'flat', look: 0.3, seed: 340 });
      // the sandwich (in his hand, at mouth height)
      const sx = 60, sy = 330 - 380 * 0.9;
      G.rrect(c, sx - 36, sy - 22, 76, 18, 6, { fill: '#E9C27A', lw: 3, seed: 212 }); G.rrect(c, sx - 34, sy - 6, 72, 10, 3, { fill: '#E8718D', lw: 2, seed: 213 }); G.rrect(c, sx - 36, sy + 4, 76, 18, 6, { fill: '#E9C27A', lw: 3, seed: 214 });
      if (t > L.lensT('mustard')) { const d = clamp((t - L.lensT('mustard')) * 1.5); G.rrect(c, sx - 34, sy - 2, 72, 8, 3, { fill: '#F2C21B', lw: 0, stroke: null, seed: 215 }); for (let i = 0; i < 3; i++) G.ellipse(c, sx - 20 + i * 22, sy + 24 + d * (18 + i * 10), 5, 8, { fill: '#F2C21B', lw: 1.5, seed: 216 + i }); }
    });
  }
  // ================= Theo, the number plate, the dots, the rule, the title =================
  function plate(ctx, t, s) {
    G.bg(ctx, '#F4EDE0');
    const t2 = A('plate', 'British');
    if (t < t2) {
      G.rays(ctx, 960, 560, { n: 30, r0: 200, r1: 1400, color: 'rgba(242,184,75,0.3)', lw: 18, seed: 5, spin: t * 0.1 });
      person(ctx, { x: 960, y: 1060, s: 1.35, pose: 'stand', style: C.theo, gesture: 'wave', t, mouth: 'grin', eyes: 'happy', seed: 300 });
      L.stampText(ctx, t, A('plate', 'Theo') + 0.5, 'THEO', 960, 200, { size: 150 });
      return;
    }
    // the road: 20 m vs 2 km
    G.poly(ctx, [[-20, 520], [W + 20, 520], [W + 20, 760], [-20, 760]], { fill: '#6E6A6E', lw: 4, seed: 220 });
    for (let i = 0; i < 12; i++) G.rrect(ctx, i * 170 + 20, 632, 90, 14, 4, { fill: '#F6F0E2', lw: 0, stroke: null, seed: 221 + i });
    // the car with the plate, far right
    G.rrect(ctx, 1620, 520, 220, 120, 26, { fill: '#3FA89B', lw: 5, seed: 230 }); G.rrect(ctx, 1660, 470, 140, 70, 18, { fill: '#BFE3F0', lw: 4, seed: 231 });
    G.rrect(ctx, 1680, 590, 100, 28, 4, { fill: '#F2D14B', lw: 3, seed: 232 });
    G.eye && null;
    L.eye(ctx, 260, 400, 0.6, { look: 1 });
    const k1 = L.fade(t, t2 + 0.4);
    G.line(ctx, [[360, 400], [lerp(360, 560, k1), 400]], { lw: 5, color: '#B9532A' });
    L.label(ctx, '20 m', 470, 370, { size: 44, alpha: k1, color: '#B9532A' });
    L.label(ctx, 'normal: the driving test', 300, 300, { size: 34, alpha: k1, fam: 'Patrick Hand' });
    if (t > A('plate', 'You?')) {
      L.eye(ctx, 260, 860, 0.6, { look: 1, glow: 1 });
      const k2 = ease.outCubic(L.fade(t, A('plate', 'You?') + 0.2, 1.2));
      G.line(ctx, [[360, 860], [lerp(360, 1600, k2), 860]], { lw: 6, color: '#E0703E' });
      L.label(ctx, '2 km', lerp(360, 1600, k2) - 90, 830, { size: 60, color: '#E0703E' });
      L.label(ctx, 'you', 300, 980, { size: 40, fam: 'Patrick Hand' });
      L.lens(ctx, t, L.lensT('plate'), s.t1, { tx: 1730, ty: 604, cx: 1260, cy: 330, r: 170 }, (c, r) => {
        c.fillStyle = '#3FA89B'; c.fillRect(-r, -r, 2 * r, 2 * r);
        G.rrect(c, -150, -45, 300, 90, 10, { fill: '#F2D14B', lw: 5, seed: 233 });
        G.text(c, 'TH30 SEE', 0, 24, { size: 62, align: 'center', fam: 'Inter', weight: 800, boil: 0 });
      });
    }
  }
  const E_BITS = ['11111', '10000', '11110', '10000', '11111'];
  function letterGrid(ctx, x, y, size, cells, tFine) {
    // sample the letter E into `cells` x `cells` squares: a coarse grid blurs it, a fine grid shows detail
    const cs = size / cells;
    for (let i = 0; i < cells; i++) for (let j = 0; j < cells; j++) {
      const u = (i + 0.5) / cells, v = (j + 0.5) / cells;
      const bx = Math.floor(u * 7) - 1, by = Math.floor(v * 7) - 1;
      let on = bx >= 0 && bx < 5 && by >= 0 && by < 5 && E_BITS[by][bx] === '1' ? 1 : 0;
      if (cells < 10) on = clamp(on * 0.6 + 0.25 * G.rnd(i, j, 3));
      ctx.fillStyle = `rgba(42,35,32,${on})`; ctx.fillRect(x + i * cs, y + j * cs, cs + 0.5, cs + 0.5);
    }
    G.rrect(ctx, x, y, size, size, 6, { fill: null, lw: 5, seed: 240 + cells });
  }
  function acuity(ctx, t, s) {
    G.bg(ctx, '#F4EDE0');
    L.label(ctx, 'normal eyes', 520, 230, { size: 56 });
    letterGrid(ctx, 300, 290, 440, 6);
    L.label(ctx, 'detail ≈ 1/60 of a degree', 520, 830, { size: 40, fam: 'Patrick Hand', alpha: L.fade(t, s.t0 + 1.2) });
    if (t > A('acuity', 'Yours?')) {
      L.label(ctx, 'yours', 1400, 230, { size: 56, color: '#E0703E' });
      const k = ease.outCubic(L.fade(t, A('acuity', 'Yours?') + 0.2, 1.5));
      letterGrid(ctx, 1180, 290, 440, Math.round(lerp(6, 120, k)));
      L.stampText(ctx, t, A('acuity', 'hundred'), '×100 finer', 1400, 860, { size: 70 });
    }
  }
  function rule(ctx, t, s) {
    G.bg(ctx, '#F4EDE0');
    const t2 = A('rule', 'spot trouble');
    if (t < t2) {
      L.stampText(ctx, t, s.t0 + 0.4, 'THE RULE', 960, 170, { size: 110, color: '#F2B84B' });
      if (t > A('rule', 'eyes got')) { L.eye(ctx, 560, 520, 1.3, { glow: 1 }); L.stampText(ctx, t, A('rule', 'eyes got') + 0.8, 'EYES ×100', 560, 800, { size: 80 }); }
      if (t > A('rule', 'legs')) {
        // two sneakers
        for (const dx of [-70, 70]) { G.rrect(ctx, 1360 + dx - 60, 470, 70, 120, 20, { fill: '#27305C', lw: 5, seed: 250 + dx }); G.rrect(ctx, 1360 + dx - 70, 570, 130, 60, 26, { fill: '#F6F0E2', lw: 5, seed: 252 + dx }); }
        L.stampText(ctx, t, A('rule', 'legs') + 0.4, 'LEGS ×1', 1360, 800, { size: 80, color: '#5B6F8A' });
      }
      return;
    }
    // the distance: you see it now, you get there... at walking speed
    L.sky(ctx, '#BFE3F0', '#F4EDE0', 760); G.poly(ctx, [[-20, 760], [W + 20, 760], [W + 20, H + 20], [-20, H + 20]], { fill: '#C9D6A8', lw: 4, seed: 260 });
    G.line(ctx, [[200, 900], [1720, 900]], { lw: 4, color: 'rgba(42,35,32,0.6)', step: 18 });
    L.label(ctx, '2 km', 960, 870, { size: 52 });
    // trouble, far right
    G.poly(ctx, [[1720, 560], [1800, 700], [1640, 700]], { fill: '#F2B84B', lw: 5, seed: 261 }); L.label(ctx, '!', 1720, 690, { size: 90, fam: 'Bungee' });
    const w = Ch.walk(t, { x0: 220, speed: 22, t0: t2, stride: 260 });
    person(ctx, { ...w, y: 900, s: 0.7, style: C.theo, look: 1, eyes: 'normal', brows: 'worried', mouth: 'flat', seed: 300 });
    if (t > A('rule', 'still reach')) { L.label(ctx, 'ETA: 25 min', w.x, 470, { size: 46, color: '#B9532A', alpha: L.fade(t, A('rule', 'still reach')) }); }
  }
  function title(ctx, t, s) {
    G.bg(ctx, '#27305C');
    G.rays(ctx, 960, 540, { n: 36, r0: 150, r1: 1500, color: 'rgba(242,184,75,0.25)', lw: 20, seed: 9, spin: (t - s.t0) * 0.15 });
    const k = L.pop(t, S.ev.title, 0.35);
    ctx.save(); ctx.translate(960, 520); ctx.scale(k, k);
    L.eye(ctx, 0, -230, 1.2, { glow: 1, look: Math.sin(t * 2) * 0.3 });
    G.text(ctx, 'WHAT IF YOUR EYESIGHT', 0, 0, { size: 96, align: 'center', fam: 'Bungee', weight: 400, color: '#F6F0E2', stroke: INK, strokeW: 10 });
    G.text(ctx, 'WAS 100× SHARPER?', 0, 140, { size: 120, align: 'center', fam: 'Bungee', weight: 400, color: '#E0703E', stroke: INK, strokeW: 12 });
    ctx.restore();
  }
  // ================= the montage =================
  function classroom(ctx, t, s) {
    G.bg(ctx, '#EADFCB');
    G.rrect(ctx, 120, 120, 760, 360, 10, { fill: '#2F4A3E', lw: 6, seed: 270 });
    G.text(ctx, 'Optics 101', 500, 250, { size: 64, align: 'center', fam: 'Gochi Hand', weight: 400, color: '#F6F0E2' });
    G.poly(ctx, [[-20, 700], [W + 20, 700], [W + 20, H + 20], [-20, H + 20]], { fill: '#B98E62', lw: 4, seed: 271, hatch: { color: 'rgba(0,0,0,0.12)', gap: 12 } });
    // the teacher at her desk (far), her notes on it
    const tk = A('class', 'Okay, class');
    person(ctx, { x: 560, y: 760, s: 0.62, pose: 'stand', style: C.teacher, eyes: t > tk ? 'wide' : 'normal', look: t > tk ? 1 : 0, brows: t > tk ? 'up' : 'neutral', mouth: talk(t, 'teacher', 'flat'), seed: 350 });
    G.rrect(ctx, 380, 700, 360, 90, 8, { fill: '#8A5A3A', lw: 5, seed: 272 });
    G.rrect(ctx, 600, 684, 70, 22, 3, { fill: '#FBF8F1', lw: 2.5, seed: 273 });
    // Theo at the back (big, close to us), at his desk
    const tn = A('class', 'Never'), tm = A('class', 'Mostly');
    person(ctx, { x: 1450, y: 900, s: 1.0, pose: 'sit', style: C.theo, look: -1, lookY: -0.2, headRot: t > tn && t < tm ? Math.sin(t * 16) * 0.12 : 0, mouth: t > tm && t < tm + 1.5 ? 'smirk' : t > tk ? 'o' : 'flat', eyes: t > tk ? 'wide' : 'normal', blush: t > tk ? 0.6 : 0, seed: 300 });
    G.rrect(ctx, 1220, 880, 480, 200, 10, { fill: '#C79A6A', lw: 5, seed: 274 });
    if (t > A('class', 'never need glasses') && t < A('class', 'read the teacher')) L.label(ctx, 'glasses: never needed', 1450, 300, { size: 50, color: '#3D7A74', rot: -0.04 });
    L.lens(ctx, t, L.lensT('notes'), A('class', 'Minus'), { tx: 635, ty: 692, cx: 1000, cy: 330, r: 200, tag: "the teacher's notes" }, (c, r) => {
      c.fillStyle = '#FBF8F1'; c.fillRect(-r, -r, 2 * r, 2 * r);
      for (let i = 0; i < 8; i++) G.line(c, [[-r, -130 + i * 40], [r, -130 + i * 40]], { lw: 1.5, color: 'rgba(61,122,116,0.4)' });
      ['QUIZ ANSWERS', '1. B   2. D', '3. A   4. C'].forEach((line, i) => G.text(c, line, -130, -100 + i * 70, { size: 40, fam: 'Gochi Hand', weight: 400, color: '#B9532A' }));
    });
    L.lens(ctx, t, L.lensT('pores'), tk - 0.1, { tx: 560, ty: 520, cx: 1000, cy: 330, r: 220 }, (c, r) => {
      c.fillStyle = C.teacher.skin; c.fillRect(-r, -r, 2 * r, 2 * r);
      for (let i = 0; i < 70; i++) G.ellipse(c, (G.rnd(i, 7) - 0.5) * 2 * r, (G.rnd(i, 8) - 0.5) * 2 * r, 3, 2.5, { fill: '#D9A98C', lw: 0, stroke: null, seed: 280 + i });
      G.ellipse(c, 0, 40, 70, 50, { fill: '#E7BC9E', lw: 4, seed: 290 });
      if (t > A('class', 'grey hair')) { const pts = []; for (let i = 0; i < 10; i++) pts.push([-r + 30 + i * 22, -r + 60 + Math.sin(i * 0.9) * 14]); G.line(c, pts, { lw: 4, color: '#D8D8D8' }); L.label(c, 'one grey hair', 40, -100, { size: 34, fam: 'Patrick Hand' }); }
    });
  }
  function stadium(ctx, t, s) {
    G.bg(ctx, '#BFE3F0');
    G.poly(ctx, [[-20, 760], [W + 20, 760], [W + 20, H + 20], [-20, H + 20]], { fill: '#5FA85A', lw: 4, seed: 300, hatch: { color: 'rgba(255,255,255,0.15)', gap: 40, angle: 0 } });
    for (let r = 0; r < 6; r++) { G.poly(ctx, [[-20, 160 + r * 100], [W + 20, 160 + r * 100], [W + 20, 250 + r * 100], [-20, 250 + r * 100]], { fill: r % 2 ? '#C9CED6' : '#B4BBC6', lw: 3, seed: 301 + r }); for (let i = 0; i < 40; i++) { if (r === 0 && i > 30) continue; G.ellipse(ctx, 20 + i * 48 + (r % 2) * 24, 190 + r * 100, 14, 16, { fill: ['#E0703E', '#3FA89B', '#F2B84B', '#E8718D', '#5B6F8A'][(i + r) % 5], lw: 2, seed: 310 + i + r * 40 }); } }
    G.ellipse(ctx, 980, 900, 9, 9, { fill: '#FFFFFF', lw: 2, seed: 302 });
    person(ctx, { x: 1700, y: 360, s: 0.55, pose: 'sit', style: C.theo, look: -1, lookY: 1, eyes: 'normal', brows: 'determined', mouth: 'smile', shadow: false, seed: 300 });
    L.label(ctx, 'cheapest seat', 1700, 120, { size: 40, fam: 'Patrick Hand', alpha: L.fade(t, s.t0 + 0.5) });
    L.lens(ctx, t, L.lensT('ball'), s.t1, { tx: 980, ty: 900, cx: 860, cy: 480, r: 230, tag: 'the stitching' }, (c, r) => {
      c.fillStyle = '#5FA85A'; c.fillRect(-r, -r, 2 * r, 2 * r);
      const spin = t * 0.6;
      G.ellipse(c, 0, 0, 170, 170, { fill: '#FBF8F1', lw: 5, seed: 303 });
      for (let i = 0; i < 6; i++) { const a = spin + i * Math.PI / 3, rr = i === 5 ? 0 : 105; const x = Math.cos(a) * rr, y = Math.sin(a) * rr; const pts = []; for (let k = 0; k < 5; k++) pts.push([x + Math.cos(a + k * 1.2566) * 38, y + Math.sin(a + k * 1.2566) * 38]); G.poly(c, pts, { fill: '#2A2320', lw: 3, seed: 304 + i }); for (let k = 0; k < 5; k++) { const [p0, p1] = [pts[k], pts[(k + 1) % 5]]; G.line(c, [[p0[0] * 1.15 - x * 0.15, p0[1] * 1.15 - y * 0.15], [p1[0] * 1.15 - x * 0.15, p1[1] * 1.15 - y * 0.15]], { lw: 2, color: 'rgba(42,35,32,0.6)', step: 8 }); } }
    });
  }
  function birds(ctx, t, s) {
    L.sky(ctx, '#BFE3F0', '#E6EFD8', H);
    G.poly(ctx, [[-20, 820], [W + 20, 800], [W + 20, H + 20], [-20, H + 20]], { fill: '#8DB46E', lw: 4, seed: 320 });
    G.line(ctx, [[1300, 180], [1900, 230]], { lw: 14, color: '#6B4A2A' });
    Ch.bird(ctx, { x: 1560, y: 196, s: 0.5, color: '#E0703E', t, facing: -1 });
    ['friend', 'boy', 'tourist'].forEach((k, i) => {
      const x = 280 + i * 260;
      person(ctx, { x, y: 1000, s: 0.8, pose: 'stand', style: C[k], handL: [-30, -330], handR: [30, -330], look: 1, lookY: -0.6, seed: 360 + i * 20 });
      G.rrect(ctx, x - 44, 1000 - 0.8 * 420, 88, 40, 12, { fill: '#2A2320', lw: 3, seed: 321 + i });
    });
    person(ctx, { x: 1120, y: 1000, s: 0.9, pose: 'stand', style: C.theo, look: 1, lookY: -0.7, mouth: talk(t, 'narrator', 'smile') === 'smile' ? 'smile' : 'open', seed: 300 });
    L.label(ctx, 'no binoculars', 1120, 540, { size: 36, fam: 'Patrick Hand', alpha: L.fade(t, s.t0 + 0.8) * (t < L.lensT('feathers') ? 1 : 0) });
    L.lens(ctx, t, L.lensT('feathers'), s.t1, { tx: 1560, ty: 180, cx: 1450, cy: 560, r: 230 }, (c, r) => {
      c.fillStyle = '#E6EFD8'; c.fillRect(-r, -r, 2 * r, 2 * r);
      Ch.bird(c, { x: 0, y: 90, s: 2.4, color: '#E0703E', t, facing: -1 });
      for (let i = 0; i < 26; i++) G.line(c, [[-60 + (i % 9) * 16, -10 + Math.floor(i / 9) * 22], [-50 + (i % 9) * 16, 4 + Math.floor(i / 9) * 22]], { lw: 2, color: 'rgba(42,35,32,0.5)' });
      Data.counter(c, { x: 0, y: -150, from: 1, to: 1205, t, t0: L.lensT('feathers') + 0.3, t1: s.t1 - 0.4, size: 56, prefix: 'feathers: ', fam: 'Bungee' });
    });
  }
  function fovea(ctx, t, s) {
    G.bg(ctx, '#F4EDE0');
    const tJump = A('fovea', 'eyes jump'), tTen = A('fovea', 'ten thousand'), tHead = A('fovea', 'Headaches');
    if (t < tJump) {
      // the eye in cross-section: the fovea, a tiny pit of sharp vision
      G.ellipse(ctx, 600, 520, 300, 300, { fill: '#FBF8F1', lw: 6, seed: 400 });
      G.ellipse(ctx, 320, 520, 60, 130, { fill: '#BFE3F0', lw: 5, seed: 401 });
      G.line(ctx, [[640, 230], [880, 420], [890, 520], [880, 620], [640, 810]], { lw: 8, color: '#E8718D' });
      const k = L.pop(t, A('fovea', 'tiny spot'));
      if (k > 0) { G.ellipse(ctx, 892, 520, 24 * k, 24 * k, { fill: '#E0703E', lw: 4, seed: 402 }); L.label(ctx, 'the fovea', 1010, 470, { size: 44 }); }
      G.line(ctx, [[60, 520], [892, 520]], { lw: 2.5, color: 'rgba(42,35,32,0.45)', step: 14 });
      if (t > A('fovea', 'thumb')) {
        // a thumb at arm's length: about 2 degrees of sharp vision
        G.rrect(ctx, 1400, 360, 120, 260, 60, { fill: '#E8B48E', lw: 5, seed: 403 }); G.rrect(ctx, 1420, 380, 80, 70, 30, { fill: '#F6D6C0', lw: 3, seed: 404 });
        G.rrect(ctx, 1340, 560, 260, 300, 60, { fill: '#E8B48E', lw: 5, seed: 405 });
        if (t > A('fovea', 'tiny patch')) { G.ellipse(ctx, 1460, 410, 70, 70, { fill: null, stroke: '#E0703E', lw: 7, seed: 406 }); L.label(ctx, '≈ 2°', 1640, 400, { size: 64, color: '#E0703E' }); }
      }
      return;
    }
    if (t < tHead) {
      // a view, blurred except for one sharp spot that jumps 3-4 times a second
      const vx = 260, vy = 140, vw = 1400, vh = 720;
      const view = (c, sharp) => { L.sky(c, '#9FD3EA', '#F4EDE0', vy + vh * 0.55); L.sea(c, vy + vh * 0.5, t, { y1: vy + vh * 0.75 }); L.sand(c, vy + vh * 0.72); L.cloud(c, vx + 300, vy + 120, 1, 1); L.plane(c, vx + 1000, vy + 140, 0.4, -1); person(c, { x: vx + 700, y: vy + vh - 20, s: 0.7, pose: 'stand', style: C.friend, gesture: 'wave', t, seed: 330 }); if (sharp && t > tTen) for (let i = 0; i < 400; i++) c.fillRect(vx + G.rnd(i, 1) * vw, vy + G.rnd(i, 2) * vh, 2, 2); };
      ctx.save(); ctx.beginPath(); ctx.rect(vx, vy, vw, vh); ctx.clip();
      ctx.filter = 'blur(10px)'; view(ctx, false); ctx.filter = 'none';
      const n = Math.floor((t - tJump) * 3.5), j = (t - tJump) * 3.5 - n;
      const p0 = [vx + 200 + G.rnd(n, 11) * (vw - 400), vy + 120 + G.rnd(n, 12) * (vh - 240)], p1 = [vx + 200 + G.rnd(n + 1, 11) * (vw - 400), vy + 120 + G.rnd(n + 1, 12) * (vh - 240)];
      const q = j < 0.8 ? p0 : [lerp(p0[0], p1[0], (j - 0.8) / 0.2), lerp(p0[1], p1[1], (j - 0.8) / 0.2)];
      ctx.save(); ctx.beginPath(); ctx.arc(q[0], q[1], 110, 0, Math.PI * 2); ctx.clip(); view(ctx, true); ctx.restore();
      ctx.restore();
      G.rrect(ctx, vx, vy, vw, vh, 8, { fill: null, lw: 6, seed: 410 });
      G.ellipse(ctx, q[0], q[1], 110, 110, { fill: null, stroke: '#E0703E', lw: 6, seed: 411 });
      L.label(ctx, '3–4 jumps a second', 960, 950, { size: 44, alpha: t < tTen ? 1 : 0 });
      if (t > tTen) { L.stampText(ctx, t, tTen + 1.2, '×10,000 DETAIL', 960, 960, { size: 74, color: '#E8718D' }); }
      return;
    }
    // headaches
    L.light(ctx, 960, 500, '#FFFFFF', '#E8C3B9');
    person(ctx, { x: 960, y: 1080, s: 1.6, pose: 'stand', style: C.theo, gesture: 'facepalm', eyes: 'closed', brows: 'worried', mouth: 'wavy', seed: 300 });
    const th = 0.5 + 0.5 * Math.sin(t * 9);
    for (let i = 0; i < 8; i++) { const a = -Math.PI / 2 + (i - 3.5) * 0.32, r0 = 300, r1 = 360 + th * 40; G.line(ctx, [[960 + Math.cos(a) * r0, 380 + Math.sin(a) * r0], [960 + Math.cos(a) * (r0 + r1) / 2 + 10, 380 + Math.sin(a) * (r0 + r1) / 2], [960 + Math.cos(a) * r1, 380 + Math.sin(a) * r1]], { lw: 7, color: '#D8352A' }); }
    L.label(ctx, 'every single day', 1500, 220, { size: 50, alpha: L.fade(t, A('fovea', 'Every single')), rot: 0.06 });
  }
  function harbor(ctx, t, s) {
    L.sky(ctx, '#A9D8EC', '#F4EDE0', 560);
    L.sea(ctx, 520, t, { col: '#3B7F95' });
    // the ship far out
    const sx = 1500, sy = 500;
    G.poly(ctx, [[sx - 90, sy], [sx + 90, sy], [sx + 70, sy + 30], [sx - 70, sy + 30]], { fill: '#5B6F8A', lw: 3, seed: 420 }); G.rrect(ctx, sx - 30, sy - 40, 60, 40, 3, { fill: '#F6F0E2', lw: 3, seed: 421 }); G.rrect(ctx, sx + 40, sy - 14, 14, 10, 1, { fill: '#F2D14B', lw: 1.5, seed: 422 });
    G.poly(ctx, [[-20, 760], [W + 20, 760], [W + 20, H + 20], [-20, H + 20]], { fill: '#9A7A5A', lw: 5, seed: 423, hatch: { color: 'rgba(0,0,0,0.15)', gap: 22, angle: 1.57 } });
    for (let i = 0; i < 6; i++) G.rrect(ctx, 80 + i * 330, 700, 26, 90, 4, { fill: '#6B4A2A', lw: 3, seed: 424 + i });
    person(ctx, { x: 820, y: 1000, s: 0.95, pose: 'stand', style: C.theo, look: 1, lookY: -0.3, eyes: t > L.lensT('sign') ? 'happy' : 'normal', mouth: 'smile', seed: 300 });
    const viral = A('harbor', 'clip goes');
    person(ctx, { x: 360, y: 1010, s: 0.9, pose: 'stand', style: C.tourist, gesture: 'phone', look: 1, mouth: t > L.lensT('sign') ? 'o' : 'smile', eyes: t > L.lensT('sign') ? 'wide' : 'normal', seed: 380 });
    if (t > A('harbor', 'tourist')) { G.ellipse(ctx, 440, 640, 10, 10, { fill: '#D8352A', lw: 2, seed: 425, alpha: Math.sin(t * 8) > 0 ? 1 : 0.2 }); L.label(ctx, 'REC', 490, 650, { size: 30, fam: 'Bungee' }); }
    L.lens(ctx, t, L.lensT('sign'), viral - 0.1, { tx: sx + 47, ty: sy - 9, cx: 1300, cy: 270, r: 190, tag: 'a sign far out at sea' }, (c, r) => {
      c.fillStyle = '#F6F0E2'; c.fillRect(-r, -r, 2 * r, 2 * r);
      G.rrect(c, -160, -80, 320, 160, 10, { fill: '#F2D14B', lw: 6, seed: 426 });
      G.text(c, 'CAUTION', 0, -18, { size: 52, align: 'center', fam: 'Bungee', weight: 400 }); G.text(c, 'WET PAINT', 0, 46, { size: 44, align: 'center', fam: 'Bungee', weight: 400 });
    });
    if (t > viral) {
      L.card(ctx, t, viral, 1140, 120, 620, 380, (c, w, h) => {
        c.fillStyle = '#20232C'; c.fillRect(-w / 2, -h / 2, w, h);
        G.text(c, '▶', 0, -30, { size: 110, align: 'center', color: '#F6F0E2', fam: 'Inter', weight: 800, boil: 0 });
        Data.counter(c, { x: 0, y: 120, from: 0, to: 2000000, t, t0: viral + 0.3, t1: s.t1 - 0.3, size: 60, color: '#F2B84B', suffix: ' views', fam: 'Bungee' });
      }, { rot: 0.03 });
    }
  }
  function message(ctx, t, s) {
    G.bg(ctx, '#2A2836');
    const chat = [
      { t: A('message', 'I have a job'), who: 'them', text: 'I have a job.' },
      { t: A('message', 'Sit in a café'), who: 'them', text: 'Sit in a café. Read a few phones. A few bank cards.' },
      { t: A('message', 'Nobody gets hurt'), who: 'them', text: 'Nobody gets hurt.' },
      { t: A('message', 'easy'), who: 'them', text: "Doesn't that sound easy? 💰" },
    ];
    UI.phone(ctx, 620, 540, 900, (c, w, h, tt) => {
      c.fillStyle = '#F3F1EE'; c.fillRect(0, 0, w, h);
      UI.header(c, w, 'Mr. Black', { kicker: 'unknown number' });
      UI.chat(c, w, chat, tt, { y0: 200, size: 30 });
    }, t, { rot: -0.03 });
    const tb = A('message', 'Mr. Black');
    person(ctx, { x: 1420, y: 1060, s: 1.25, pose: 'stand', style: C.black, crossArms: t < chat[0].t, mouth: talk(t, 'black', 'smirk'), alpha: L.fade(t, tb), seed: 390 });
    if (t > A('message', 'Polite')) L.label(ctx, 'polite', 1150, 330, { size: 46, rot: -0.08, color: '#F6F0E2' });
    if (t > A('message', 'Rich')) L.label(ctx, 'rich', 1720, 330, { size: 46, rot: 0.08, color: '#F2B84B' });
    L.light(ctx, 1420, 400, '#FFFFFF', '#6A72B0', 'multiply', 0.5);
  }
  // ================= the cost =================
  function cost(ctx, t, s) {
    G.bg(ctx, '#E9E1D3');
    const tSun = A('cost', 'Sunsets'), tFace = A('cost', 'Faces'), tRest = A('cost', 'never rest'), tBeau = A('cost', 'beautiful');
    if (t < tRest) {
      L.label(ctx, "you can't switch it off", 960, 140, { size: 56, alpha: L.fade(t, A('cost', 'switch')) });
      L.card(ctx, t, A('cost', 'Peeling'), 120, 240, 520, 520, (c, w, h) => { c.fillStyle = '#9FB8C8'; c.fillRect(-w / 2, -h / 2, w, h); for (let i = 0; i < 9; i++) { const x = -180 + (i % 3) * 160, y = -160 + Math.floor(i / 3) * 150; G.poly(c, [[x, y], [x + 70, y + 10], [x + 40, y + 60], [x + 10, y + 40]], { fill: '#E9E1D3', lw: 3, seed: 430 + i }); } L.label(c, 'peeling paint', 0, h / 2 - 40, { size: 36, fam: 'Patrick Hand' }); }, { rot: -0.04, seed: 141 });
      L.card(ctx, t, A('cost', 'Cracks'), 700, 240, 520, 520, (c, w, h) => { c.fillStyle = '#B9BEC6'; c.fillRect(-w / 2, -h / 2, w, h); G.poly(c, [[-w / 2, 40], [w / 2, 40], [w / 2, 110], [-w / 2, 110]], { fill: '#8E949E', lw: 4, seed: 440 }); G.line(c, [[-100, 40], [-60, 70], [-80, 90], [-30, 110]], { lw: 3 }); G.line(c, [[60, 40], [90, 60], [70, 80], [110, 110]], { lw: 3 }); L.label(c, 'cracks in bridges', 0, h / 2 - 40, { size: 36, fam: 'Patrick Hand' }); }, { rot: 0.03, seed: 142 });
      L.card(ctx, t, A('cost', 'Mold'), 1280, 240, 520, 520, (c, w, h) => { G.rrect(c, -170, -150, 340, 300, 90, { fill: '#E9C27A', lw: 5, seed: 450 }); G.rrect(c, -140, -110, 280, 240, 70, { fill: '#F6E7C8', lw: 3, seed: 451 }); for (let i = 0; i < 12; i++) G.ellipse(c, -60 + G.rnd(i, 3) * 140, -60 + G.rnd(i, 4) * 140, 6, 6, { fill: '#6FA36A', lw: 1.5, seed: 452 + i }); L.label(c, 'mold, before anyone sees it', 0, h / 2 - 40, { size: 32, fam: 'Patrick Hand' }); }, { rot: -0.02, seed: 143 });
      return;
    }
    if (t < tSun) {
      person(ctx, { x: 960, y: 1080, s: 1.6, pose: 'stand', style: C.theo, eyes: 'wide', brows: 'worried', mouth: 'flat', blink: 0, seed: 300 });
      for (let i = 0; i < 2; i++) G.ellipse(ctx, 960 + (i ? 50 : -50) * 1.6 * 0.5, 1080 - 1.6 * 368, 30, 10, { fill: 'rgba(90,60,90,0.35)', lw: 0, stroke: null, seed: 460 + i });
      if (t > tBeau) L.label(ctx, '...detailed.', 1500, 260, { size: 60, alpha: L.fade(t, A('cost', 'detailed')) });
      return;
    }
    // a sunset that turns into dust, and a face that turns into a map
    const k = L.u(t, tSun + 0.4, tSun + 2.2);
    ctx.save(); ctx.beginPath(); ctx.rect(80, 160, 840, 700); ctx.clip();
    L.sky(ctx, '#F2B84B', '#E8718D', 860); L.sun(ctx, 500, 640, 140, '#FFE08A'); L.sea(ctx, 700, t, { col: '#7A5C8A' });
    for (let i = 0; i < 900 * k; i++) { ctx.fillStyle = 'rgba(60,40,40,0.55)'; ctx.fillRect(80 + G.rnd(i, 21) * 840, 160 + G.rnd(i, 22) * 700, 3, 3); }
    ctx.restore(); G.rrect(ctx, 80, 160, 840, 700, 8, { fill: null, lw: 6, seed: 470 });
    L.label(ctx, 'sunsets → dust', 500, 940, { size: 46 });
    if (t > tFace) {
      const kf = L.u(t, tFace + 0.3, tFace + 1.8);
      ctx.save(); ctx.beginPath(); ctx.rect(1000, 160, 840, 700); ctx.clip(); G.bg(ctx, '#F6F0E2');
      ctx.globalAlpha = 1 - kf; person(ctx, { x: 1420, y: 1240, s: 1.5, pose: 'stand', style: C.friend, mouth: 'smile', seed: 330 }); ctx.globalAlpha = 1;
      for (let r = 1; r <= 9; r++) G.ellipse(ctx, 1420, 520, r * 30 * kf + 2, r * 36 * kf + 2, { fill: null, stroke: `rgba(61,122,116,${0.7 * kf})`, lw: 3, seed: 480 + r });
      ctx.restore(); G.rrect(ctx, 1000, 160, 840, 700, 8, { fill: null, lw: 6, seed: 471 });
      L.label(ctx, 'faces → maps', 1420, 940, { size: 46 });
    }
  }
  // ================= Grandpa =================
  function beachView(c, x, y, w, h, t) { c.save(); c.beginPath(); c.rect(x, y, w, h); c.clip(); c.translate(x, y); c.scale(w / W, h / H); L.sky(c, '#9FD3EA', '#F4EDE0', 640); L.cloud(c, 400, 180, 1, 1); L.sea(c, 600, t); L.sand(c, 760); L.kite(c, 1500, 220, 1, t); person(c, { x: 960, y: 1000, s: 0.9, pose: 'stand', style: C.friend, gesture: 'wave', t, seed: 330 }); c.restore(); G.rrect(c, x, y, w, h, 8, { fill: null, lw: 6, seed: 490 }); }
  function grandpa(ctx, t, s) {
    G.bg(ctx, '#F4EDE0');
    const tMac = A('grandpa', 'macular'), tMost = A('grandpa', 'see the most');
    if (t < tMac) {
      person(ctx, { x: 620, y: 1060, s: 1.35, pose: 'stand', style: C.grandpa, mouth: 'smile', eyes: blinkAt(t, 3) ? 'closed' : 'normal', seed: 500 });
      L.stampText(ctx, t, s.t0 + 0.6, 'GRANDPA SAM', 620, 160, { size: 90, color: '#3D7A74' });
      if (t > A('grandpa', 'lifeguard')) G.photo && L.card(ctx, t, A('grandpa', 'lifeguard'), 1120, 220, 560, 600, (c, w, h) => { L.sky(c, '#9FD3EA', '#F4EDE0'); L.tower(c, 120, 220, 0.8); person(c, { x: -80, y: 260, s: 0.75, pose: 'stand', style: { ...C.grandpa, hairStyle: 'short', hair: '#5A3A22', facialHair: 'none', glasses: 'none', outfit: 'tee', shirt: '#D8352A', bottoms: 'shorts', shorts: '#F2B84B' }, crossArms: true, mouth: 'grin', seed: 510 }); L.label(c, 'lifeguard, 1979', 0, h / 2 - 30, { size: 34, fam: 'Gochi Hand' }); }, { rot: 0.04, fill: '#FBF8F1' });
      return;
    }
    if (t < tMost) {
      beachView(ctx, 260, 120, 1400, 720, t);
      const k = L.u(t, tMac + 0.3, tMac + 2.5);
      L.smudge(ctx, 960, 480, 380 * k, 1);
      L.label(ctx, 'macular degeneration', 960, 940, { size: 52 });
      if (t > A('grandpa', 'wipes out')) { L.label(ctx, 'centre: gone', 960, 480, { size: 44, color: '#F6F0E2', alpha: L.fade(t, A('grandpa', 'wipes out') + 0.5) }); L.label(ctx, 'edges: stay', 1500, 200, { size: 40, alpha: L.fade(t, A('grandpa', 'edges') - 0.2) }); }
      return;
    }
    beachView(ctx, 80, 200, 860, 480, t); beachView(ctx, 980, 200, 860, 480, t); L.smudge(ctx, 1410, 440, 240, 1);
    L.label(ctx, 'you: the most', 510, 780, { size: 52, color: '#E0703E' });
    if (t > A('grandpa', 'the least')) L.label(ctx, 'Grandpa: the least', 1410, 780, { size: 52, color: '#3D7A74' });
  }
  function cliffTop(ctx, t, { warm = 0 } = {}) {
    L.sky(ctx, warm ? '#F2B84B' : '#9FD3EA', warm ? '#E8718D' : '#F4EDE0', 760);
    if (warm) L.sun(ctx, 420, 600, 120, '#FFE08A');
    L.sea(ctx, 640, t, { col: warm ? '#C77A5E' : '#3D8A9A' });
    L.cliff(ctx, 760, 700, 1200, { side: 'right' });
  }
  function cliff(ctx, t, s) {
    cliffTop(ctx, t);
    const tSay = A('cliff', "can't see the gulls"), tProm = A('cliff', 'If I can see');
    for (let i = 0; i < 3; i++) Ch.bird(ctx, { x: 300 + i * 220 + Math.sin(t + i) * 40, y: 260 + i * 50 + Math.sin(t * 1.3 + i) * 20, s: 0.35, color: '#F6F0E2', t: t + i, flap: true, facing: 1 });
    const kx = 900 + Math.sin(t * 0.7) * 60, ky = 220 + Math.sin(t * 1.1) * 30;
    L.kite(ctx, kx, ky, 1, t);
    const gp = [1180, 700], th = [1560, 700];
    person(ctx, { x: gp[0], y: gp[1], s: 0.85, pose: 'stand', style: C.grandpa, handL: [-175, -470], look: -0.6, lookY: -0.8, mouth: talk(t, 'grandpa', 'smile'), seed: 500 });
    L.string(ctx, [gp[0] - 0.85 * 175, gp[1] - 0.85 * 470], [kx, ky + 90], 80);
    const promise = t > tProm;
    person(ctx, { x: th[0], y: th[1], s: 0.85, pose: 'stand', style: C.theo, gesture: t > A('cliff', 'And you do') && !promise ? 'point' : null, sx: 1, look: promise ? -0.6 : -1, lookY: promise ? 0 : -0.6, mouth: talk(t, 'theo', 'smile'), eyes: promise ? 'normal' : 'happy', brows: promise ? 'determined' : 'neutral', seed: 300 });
    if (t > A('cliff', 'Every wing')) L.label(ctx, 'every wing...', 520, 520, { size: 44, alpha: L.fade(t, A('cliff', 'Every wing')), rot: -0.05 });
    if (t > A('cliff', 'Every wave')) L.label(ctx, '...every wave', 560, 600, { size: 44, alpha: L.fade(t, A('cliff', 'Every wave')), rot: 0.04 });
    if (promise) { L.light(ctx, 1560, 400, '#FFFFFF', '#E8C3B9', 'multiply', 0.6); L.label(ctx, 'If I can see it... it\'s mine to fix.', 960, 140, { size: 58, color: '#E0703E', alpha: L.fade(t, tProm) }); }
  }
  // ================= the crisis =================
  function roof(ctx, t, s) {
    const tWoman = A('roof', 'Below you'), tEar = A('roof', "voice in your ear");
    if (t < tWoman) {
      L.sky(ctx, '#A9D8EC', '#F4EDE0', 700); L.sea(ctx, 560, t); L.town(ctx, 860, 51);
      G.poly(ctx, [[-20, 840], [W + 20, 840], [W + 20, H + 20], [-20, H + 20]], { fill: '#B5553A', lw: 5, seed: 520, hatch: { color: 'rgba(0,0,0,0.15)', gap: 18 } });
      person(ctx, { x: 960, y: 900, s: 0.95, pose: 'floor', style: C.theo, look: 0.3, lookY: 0.4, brows: 'worried', mouth: 'flat', seed: 300 });
      G.ellipse(ctx, 960 + 70 * 0.95, 900 - 0.95 * 230, 9, 12, { fill: '#2A2320', lw: 2, seed: 521 });
      L.label(ctx, "Mr. Black's job", 960, 160, { size: 60, color: '#B9532A', alpha: L.fade(t, A('roof', "Black's job")) });
      L.label(ctx, '2 km from the beach', 1500, 520, { size: 40, fam: 'Patrick Hand', alpha: L.fade(t, A('roof', 'café roof')) });
      return;
    }
    // the street below: a cash machine
    G.bg(ctx, '#D9CBB4');
    G.rrect(ctx, 200, 140, 1520, 760, 10, { fill: '#E9B98A', lw: 6, seed: 530 });
    G.rrect(ctx, 820, 330, 300, 420, 14, { fill: '#5B6F8A', lw: 6, seed: 531 }); G.rrect(ctx, 860, 370, 220, 120, 8, { fill: '#9FD3EA', lw: 4, seed: 532 }); G.text(ctx, 'CASH', 970, 450, { size: 40, align: 'center', fam: 'Bungee', weight: 400, color: '#F6F0E2' });
    person(ctx, { x: 700, y: 1000, s: 0.9, pose: 'stand', style: C.woman, handR: [160, -300], look: 1, mouth: 'flat', seed: 540 });
    if (t > A('roof', 'Her card')) G.rrect(ctx, 840, 545, 60, 38, 5, { fill: '#F2B84B', lw: 3, seed: 533 });
    if (t > A('roof', 'Her keys')) { G.ellipse(ctx, 640, 860, 16, 16, { fill: null, stroke: '#B9BEC6', lw: 5, seed: 534 }); G.line(ctx, [[652, 870], [690, 900]], { lw: 6, color: '#B9BEC6' }); }
    L.lens(ctx, t, L.lensT('pin'), s.t1, { tx: 960, ty: 620, cx: 1420, cy: 500, r: 260, tag: 'her PIN' }, (c, r) => { c.fillStyle = '#5B6F8A'; c.fillRect(-r, -r, 2 * r, 2 * r); L.keypad(c, 0, 20, 1, t, { pressT: L.lensT('pin') + 0.4 }); });
    if (t > tEar) {
      G.rrect(ctx, 120, 120, 520, 150, 30, { fill: '#2A2836', lw: 5, seed: 535 });
      G.ellipse(ctx, 200, 195, 30, 40, { fill: '#1C1C22', lw: 3, seed: 536 });
      for (let i = 0; i < 3; i++) G.line(ctx, [[250 + i * 22, 165 - i * 8], [262 + i * 22, 195], [250 + i * 22, 225 + i * 8]], { lw: 4, color: `rgba(242,184,75,${0.4 + 0.3 * Math.sin(t * 10 + i)})` });
      G.text(ctx, 'Mr. Black', 450, 210, { size: 46, align: 'center', fam: 'Permanent Marker', weight: 400, color: '#F6F0E2' });
    }
    L.light(ctx, 960, 500, '#FFFFFF', '#6A72B0', 'multiply', 0.45);
  }
  function seaWide(ctx, t, { boyX = 1500, boyY = 470, boardOff = 0, rip = 1, guardLook = 1 } = {}) {
    L.sky(ctx, '#A9D8EC', '#F4EDE0', 420);
    L.sea(ctx, 380, t, { col: '#3D8A9A', y1: 700 });
    // the rip: a darker, flatter channel heading out to sea
    if (rip) { ctx.save(); ctx.globalAlpha = 0.55 * rip; G.poly(ctx, [[1380, 700], [1560, 700], [1600, 400], [1420, 400]], { fill: '#24546A', lw: 0, stroke: null, seed: 550 }); ctx.restore(); }
    L.sand(ctx, 690, { y1: 800 });
    L.tower(ctx, 600, 780, 0.6);
    G.ellipse(ctx, 600 + guardLook * 6, 780 - 0.6 * 205, 9, 9, { fill: '#8D5A3B', lw: 2, seed: 551 });
    L.town(ctx, 1100, 52, { n: 8 });
    G.poly(ctx, [[-20, 1010], [W + 20, 1010], [W + 20, H + 20], [-20, H + 20]], { fill: '#C9785A', lw: 5, seed: 552, hatch: { color: 'rgba(0,0,0,0.12)', gap: 18 } });
    // the boy, tiny
    L.board(ctx, boyX + boardOff, boyY + 6, 0.18, 0.1);
    G.ellipse(ctx, boyX, boyY - 6, 5, 5, { fill: '#E6B48C', lw: 1.5, seed: 553 });
  }
  function sea(ctx, t, s) {
    const tDrift = A('sea', 'Drifting'), tSlip = A('sea', 'slips');
    const by = 470 - L.u(t, tDrift, s.t1) * 60, bx = 1490 + L.u(t, tDrift, s.t1) * 20;
    const off = t > tSlip ? ease.outCubic(L.u(t, tSlip, tSlip + 2)) * 40 : 0;
    seaWide(ctx, t, { boyX: bx, boyY: by, boardOff: off, rip: t > A('sea', 'darker') ? L.fade(t, A('sea', 'darker'), 1) : 0.15 });
    L.lens(ctx, t, L.lensT('boy'), s.t1, { tx: bx, ty: by, cx: 1080, cy: 330, r: 230, tag: 'a small boy' }, (c, r) => {
      c.fillStyle = t > A('sea', 'darker') ? '#24546A' : '#3D8A9A'; c.fillRect(-r, -r, 2 * r, 2 * r);
      for (let i = 0; i < 6; i++) G.line(c, [[-r + ((i * 90 + t * 30) % (2 * r)), -100 + i * 40], [-r + 40 + ((i * 90 + t * 30) % (2 * r)), -106 + i * 40]], { lw: 3, color: 'rgba(255,255,255,0.4)' });
      L.board(c, off * 4, 120, 1.3, 0.08);
      person(c, { x: 0, y: 200, s: 0.55, pose: 'stand', style: C.boy, handL: [-150, -290], handR: [150, -290], eyes: 'wide', brows: 'worried', mouth: 'o', seed: 560 });
      c.fillStyle = 'rgba(36,84,106,0.9)'; c.fillRect(-r, 120, 2 * r, r);
    });
    if (t > A('sea', 'rip current')) { L.label(ctx, 'RIP CURRENT', 1700, 560, { size: 40, color: '#D8352A', alpha: L.fade(t, A('sea', 'rip current')) }); for (let i = 0; i < 3; i++) { const yy = 680 - ((t * 80 + i * 90) % 260); G.line(ctx, [[1480, yy + 20], [1490, yy], [1500, yy + 20]], { lw: 4, color: '#F6F0E2' }); } }
    if (t > A('sea', 'wrong way')) L.label(ctx, '← looking the wrong way', 760, 600, { size: 34, fam: 'Patrick Hand', alpha: L.fade(t, A('sea', 'wrong way')) });
    if (t > A('sea', 'Two kilometers')) { G.line(ctx, [[960, 1040], [1480, 520]], { lw: 5, color: '#F2B84B', step: 16 }); L.label(ctx, '2 km', 1280, 820, { size: 60, color: '#F2B84B' }); }
    if (t > A('sea', 'six minutes')) L.stampText(ctx, t, A('sea', 'six minutes') + 1, '6:00+', 1700, 900, { size: 90, color: '#D8352A' });
    L.light(ctx, 1200, 400, '#FFFFFF', '#8A90C0', 'multiply', 0.25 + 0.1 * Math.sin(t * 2.6));
  }
  function choice(ctx, t, s) {
    G.bg(ctx, '#1E2046');
    const tSplit = S.ev.split;
    const pinFull = t > A('choice', 'see the PIN'), boyFull = t > A('choice', 'see the boy');
    if (pinFull) L.lens(ctx, t, A('choice', 'see the PIN'), s.t1 + 1, { tx: 960, ty: 560, cx: 520, cy: 470, r: 300 }, (c, r) => { c.fillStyle = '#5B6F8A'; c.fillRect(-r, -r, 2 * r, 2 * r); L.keypad(c, 0, 20, 1.15, t, { pressT: A('choice', 'see the PIN') }); });
    if (boyFull) L.lens(ctx, t, A('choice', 'see the boy'), s.t1 + 1, { tx: 960, ty: 560, cx: 1400, cy: 470, r: 300 }, (c, r) => { c.fillStyle = '#24546A'; c.fillRect(-r, -r, 2 * r, 2 * r); person(c, { x: 0, y: 260, s: 0.75, pose: 'stand', style: C.boy, handL: [-150, -300], handR: [150, -300], eyes: 'wide', brows: 'worried', mouth: 'o', seed: 560 }); c.fillStyle = 'rgba(36,84,106,0.92)'; c.fillRect(-r, 150, 2 * r, r); });
    if (!pinFull) { L.label(ctx, 'Theo?', 960, 420, { size: 90, color: '#F6F0E2', alpha: L.fade(t, s.t0 + 0.4) }); L.label(ctx, 'The numbers. Now.', 960, 560, { size: 70, color: '#F2B84B', alpha: L.fade(t, A('choice', 'The numbers')) }); }
    if (t > tSplit) L.label(ctx, 'the money...', 520, 880, { size: 70, color: '#F2B84B', rot: -0.04 });
    if (t > A('choice', 'or the boy')) L.label(ctx, '...or the boy', 1400, 880, { size: 70, color: '#F6F0E2', rot: 0.04 });
  }
  // ================= the rescue =================
  function call(ctx, t, s) {
    const tCall = A('call', 'one person'), tAns = A('call', 'Grandpa. Kite');
    if (t < tCall) {
      G.bg(ctx, '#D9CBB4'); L.light(ctx, 960, 400, '#FFFFFF', '#E8C3B9');
      const tDrop = S.ev.drop;
      person(ctx, { x: 960, y: 1080, s: 1.5, pose: 'stand', style: C.theo, eyes: 'normal', brows: 'determined', mouth: talk(t, 'theo', 'flat'), handR: t < tDrop + 0.4 ? [110, -470] : [150, -200], seed: 300 });
      const fy = t < tDrop + 0.4 ? 1080 - 1.5 * 470 : lerp(1080 - 1.5 * 470, 1060, ease.inQuad(L.u(t, tDrop + 0.4, tDrop + 0.85)));
      G.ellipse(ctx, 960 + 1.5 * 120, fy, 14, 18, { fill: '#1C1C22', lw: 3, seed: 570 });
      if (t > A('call', 'If I can see')) L.label(ctx, "If I can see it... it's mine to fix.", 960, 140, { size: 58, color: '#E0703E', alpha: L.fade(t, A('call', 'If I can see')) });
      return;
    }
    // split: Theo calling / Grandpa answering on the cliff
    G.bg(ctx, '#F4EDE0');
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W / 2 - 6, H); ctx.clip(); G.bg(ctx, '#D9CBB4'); person(ctx, { x: 480, y: 1080, s: 1.3, pose: 'stand', style: C.theo, gesture: 'phone', look: 1, brows: 'determined', mouth: talk(t, 'theo', 'flat'), seed: 300 }); ctx.restore();
    ctx.save(); ctx.beginPath(); ctx.rect(W / 2 + 6, 0, W / 2, H); ctx.clip(); ctx.translate(W / 2 - 300, 0); cliffTop(ctx, t); ctx.translate(-(W / 2 - 300), 0);
    person(ctx, { x: 1440, y: 1080, s: 1.2, pose: 'stand', style: C.grandpa, gesture: 'phone', look: -1, eyes: t > tAns ? 'wide' : 'normal', brows: t > tAns ? 'determined' : 'neutral', mouth: 'flat', seed: 500 }); ctx.restore();
    G.line(ctx, [[W / 2, 0], [W / 2, H]], { lw: 8 });
    if (t > tAns) L.stampText(ctx, t, tAns + 0.2, 'KITE. UP. NOW.', 960, 170, { size: 80, color: '#D8352A' });
  }
  function bay(ctx, t, { kx, ky, boyX = 1500, boyY = 640, warm = 0 }) {
    L.sky(ctx, '#A9D8EC', '#F4EDE0', 560);
    L.sea(ctx, 520, t, { col: '#3D8A9A' });
    ctx.save(); ctx.globalAlpha = 0.5; G.poly(ctx, [[boyX - 80, 860], [boyX + 80, 860], [boyX + 110, 540], [boyX - 50, 540]], { fill: '#24546A', lw: 0, stroke: null, seed: 580 }); ctx.restore();
    L.sand(ctx, 860);
    L.cliff(ctx, -40, 380, 360, { side: 'left' });
    person(ctx, { x: 160, y: 380, s: 0.42, pose: 'stand', style: C.grandpa, handR: [110, -470], look: 1, lookY: -1, shadow: false, seed: 500 });
    L.string(ctx, [160 + 0.42 * 110, 380 - 0.42 * 470], [kx, ky + 60], 60);
    L.kite(ctx, kx, ky, 0.7, t);
    L.board(ctx, boyX, boyY + 6, 0.3, 0.1); G.ellipse(ctx, boyX, boyY - 8, 8, 8, { fill: '#E6B48C', lw: 2, seed: 581 });
  }
  function kite(ctx, t, s) {
    const tL = A('kite', 'Left'), tStop = A('kite', 'Stop'), tCant = A('kite', "can't see the boy"), tHang = A('kite', 'hangs');
    const climb = ease.outCubic(L.u(t, S.ev.kite, S.ev.kite + 2.2));
    let kx = lerp(260, 600, climb), ky = lerp(330, 170, climb);
    kx += ease.inOutQuad(L.u(t, tL, tStop)) * (1500 - 600) + ease.outBack(L.u(t, tStop, tStop + 0.8)) * 0;
    if (t > tCant && t < tHang) {
      // Grandpa's view: the boy is lost in the smudge, but the big red kite is in the corner of his eye
      bay(ctx, t, { kx, ky }); L.smudge(ctx, 1500, 640, 330, 1);
      L.label(ctx, "Grandpa's eyes", 960, 120, { size: 52, color: '#3D7A74' });
      if (t > A('kite', 'can see his kite')) { G.ellipse(ctx, kx, ky, 110, 120, { fill: null, stroke: '#F2B84B', lw: 7, seed: 590 }); }
      return;
    }
    bay(ctx, t, { kx, ky });
    if (t > tL && t < tStop) L.label(ctx, '← left... more', 960, 120, { size: 52, color: '#D8352A' });
    if (t > tStop && t < tCant) L.label(ctx, 'STOP. Hold it there.', 960, 120, { size: 52, color: '#D8352A' });
    if (t > tHang) { G.line(ctx, [[kx, ky + 100], [1500, 620]], { lw: 4, color: '#F2B84B', step: 14 }); L.label(ctx, 'right above him', 1700, 400, { size: 44, color: '#B9532A', alpha: L.fade(t, tHang) }); }
  }
  function nova(ctx, t, s) {
    const tGrab = A('nova', 'grabs'), tLesson = A('nova', 'real lesson');
    if (t < tGrab) {
      L.sky(ctx, '#A9D8EC', '#F4EDE0', 640); L.sea(ctx, 600, t); L.sand(ctx, 760);
      L.tower(ctx, 1450, 900, 1.1);
      person(ctx, { x: 820, y: 1010, s: 1.05, pose: 'stand', style: C.nova, gesture: 'phone', look: t > A('nova', 'Follow') ? 1 : 0, eyes: t > A('nova', 'Follow') ? 'wide' : 'normal', brows: 'determined', mouth: 'flat', seed: 600 });
      L.stampText(ctx, t, A('nova', 'Her name') + 0.3, 'NOVA', 820, 200, { size: 100, color: '#D8352A' });
      if (t > A('nova', 'Follow')) L.label(ctx, '"Follow the red kite."', 1400, 300, { size: 50, color: '#B9532A' });
      return;
    }
    if (t < tLesson) {
      const p = L.u(t, tGrab, tLesson);
      bay(ctx, t, { kx: 1500, ky: 170 });
      // Nova on the rescue board: out with the current, then cutting sideways to the boy
      const path = [[900, 900], [1150, 700], [1350, 640], [1460, 640]];
      const seg = Math.min(2, Math.floor(p * 3)), f = p * 3 - seg, a = path[seg], b = path[seg + 1];
      const nx = lerp(a[0], b[0], f), ny = lerp(a[1], b[1], f);
      L.board(ctx, nx, ny + 10, 0.55, -0.1, '#D8352A');
      G.ellipse(ctx, nx, ny - 14, 12, 12, { fill: C.nova.skin, lw: 2.5, seed: 610 }); G.rrect(ctx, nx - 12, ny - 4, 24, 16, 4, { fill: '#D8352A', lw: 2, seed: 611 });
      G.line(ctx, path.slice(0, seg + 1).concat([[nx, ny]]), { lw: 3, color: 'rgba(246,240,226,0.9)', step: 12 });
      if (t > A('nova', 'rides it out')) L.label(ctx, 'rides it out...', 1000, 460, { size: 48, color: '#27305C' });
      if (t > A('nova', 'cuts sideways')) L.label(ctx, '...then sideways', 1300, 400, { size: 48, color: '#B9532A' });
      return;
    }
    // the lesson: a top-down beach
    G.bg(ctx, '#F4EDE0');
    L.stampText(ctx, t, tLesson + 0.2, 'REAL LIFE', 960, 130, { size: 80, color: '#3D7A74' });
    G.poly(ctx, [[200, 220], [1720, 220], [1720, 740], [200, 740]], { fill: '#3D8A9A', lw: 5, seed: 620 });
    G.poly(ctx, [[200, 740], [1720, 740], [1720, 900], [200, 900]], { fill: '#E8D9BC', lw: 5, seed: 621 });
    G.poly(ctx, [[860, 740], [1060, 740], [1020, 260], [900, 260]], { fill: '#24546A', lw: 0, stroke: null, seed: 622 });
    for (let i = 0; i < 4; i++) { const yy = 700 - ((t * 60 + i * 120) % 440); G.line(ctx, [[940, yy + 26], [960, yy], [980, yy + 26]], { lw: 5, color: '#F6F0E2' }); }
    L.label(ctx, 'rip', 960, 330, { size: 40, color: '#F6F0E2' });
    const tPar = A('nova', 'parallel'), tBack = A('nova', 'come back');
    const sw = [960, 520];
    if (t > A('nova', 'pulls you out')) { G.ellipse(ctx, sw[0], sw[1], 18, 18, { fill: '#F2B84B', lw: 3, seed: 623 }); L.label(ctx, "don't fight it", 960, 610, { size: 34, color: '#F6F0E2' }); }
    if (t > tPar) { const k = ease.inOutQuad(L.u(t, tPar, tPar + 1.5)); G.line(ctx, [[980, 520], [lerp(980, 1420, k), 520]], { lw: 7, color: '#F2B84B' }); if (k > 0.95) G.poly(ctx, [[1420, 500], [1450, 520], [1420, 540]], { fill: '#F2B84B', lw: 3, seed: 624 }); L.label(ctx, 'swim parallel to the shore', 1300, 470, { size: 38, color: '#F6F0E2' }); }
    if (t > tBack) { const k = ease.inOutQuad(L.u(t, tBack, tBack + 1.2)); G.line(ctx, [[1440, 540], [1440, lerp(540, 800, k)]], { lw: 7, color: '#F2B84B' }); L.label(ctx, 'then back in', 1600, 820, { size: 38 }); }
  }
  // ================= the ending =================
  function saved(ctx, t, s) {
    L.sky(ctx, '#A9D8EC', '#F4EDE0', 600); L.sea(ctx, 560, t); L.sand(ctx, 700);
    const tFur = A('saved', 'furious'), tCheer = A('saved', 'whole beach');
    L.board(ctx, 1500 + (t - s.t0) * 12, 590, 0.4, 0.2);
    person(ctx, { x: 960, y: 900, s: 0.8, pose: 'floor', style: C.boy, eyes: t > tFur ? 'normal' : 'closed', brows: t > tFur ? 'determined' : 'worried', mouth: t > tFur ? 'wavy' : 'o', look: t > tFur ? 1 : 0, seed: 560 });
    if (t > tFur) { L.label(ctx, 'my board!', 1250, 520, { size: 46, rot: 0.08, color: '#D8352A' }); G.line(ctx, [[1080, 540], [1400, 590]], { lw: 3, step: 14 }); }
    person(ctx, { x: 680, y: 920, s: 0.85, pose: 'stand', style: C.nova, mouth: 'smile', eyes: 'happy', crossArms: true, seed: 600 });
    if (t > tCheer) {
      const crowd = [['friend', 180], ['tourist', 380], ['woman', 1250], ['teacher', 1700]];
      crowd.forEach(([k, x], i) => person(ctx, { x, y: 1040, s: 0.8, pose: 'stand', style: C[k], gesture: i % 2 ? 'clap' : 'cheer', t: t + i * 0.2, eyes: 'happy', mouth: 'open', seed: 700 + i * 20 }));
      person(ctx, { x: 1470, y: 1000, s: 0.95, pose: 'stand', style: C.grandpa, gesture: 'cheer', t, eyes: 'happy', mouth: 'grin', seed: 500 });
      L.kite(ctx, 1540, 200, 0.8, t);
    }
  }
  function police(ctx, t, s) {
    G.bg(ctx, '#E9E1D3');
    const tPin = A('police', 'Cover your PIN');
    if (t < tPin) {
      const flash = Math.sin(t * 10) > 0;
      G.rrect(ctx, 60, 640, 680, 230, 40, { fill: '#F6F0E2', lw: 5, seed: 723 }); G.rrect(ctx, 180, 560, 400, 110, 30, { fill: '#9FD3EA', lw: 5, seed: 724 }); G.rrect(ctx, 60, 740, 680, 50, 6, { fill: '#2C3E70', lw: 3, seed: 725 });
      G.rrect(ctx, 300, 520, 80, 40, 8, { fill: flash ? '#D8352A' : '#7A2A2A', lw: 3, seed: 721 }); G.rrect(ctx, 380, 520, 80, 40, 8, { fill: flash ? '#2A3A7A' : '#3D6FD8', lw: 3, seed: 722 });
      G.ellipse(ctx, 180, 880, 50, 50, { fill: '#2A2320', lw: 3, seed: 726 }); G.ellipse(ctx, 620, 880, 50, 50, { fill: '#2A2320', lw: 3, seed: 727 });
      person(ctx, { x: 300, y: 1040, s: 0.95, pose: 'stand', style: C.black, mouth: 'wavy', brows: 'worried', handL: [-40, -170], handR: [40, -170], seed: 390 });
      person(ctx, { x: 560, y: 1040, s: 0.95, pose: 'stand', style: C.cop, mouth: 'flat', crossArms: true, seed: 720 });
      L.card(ctx, t, A('police', 'His car'), 820, 200, 320, 320, (c) => { G.rrect(c, -120, -20, 240, 80, 20, { fill: '#1C1C22', lw: 4, seed: 730 }); G.rrect(c, -70, -60, 140, 50, 14, { fill: '#5B6F8A', lw: 3, seed: 731 }); G.ellipse(c, -70, 64, 22, 22, { fill: '#2A2320', lw: 3, seed: 732 }); G.ellipse(c, 70, 64, 22, 22, { fill: '#2A2320', lw: 3, seed: 733 }); L.label(c, 'car', 0, 130, { size: 34 }); }, { rot: -0.05, seed: 144 });
      L.card(ctx, t, A('police', 'His plate'), 1180, 200, 320, 320, (c) => { G.rrect(c, -130, -40, 260, 80, 8, { fill: '#F2D14B', lw: 4, seed: 734 }); G.text(c, 'BLK 247', 0, 18, { size: 50, align: 'center', fam: 'Inter', weight: 800, boil: 0 }); L.label(c, 'plate', 0, 130, { size: 34 }); }, { rot: 0.04, seed: 145 });
      L.card(ctx, t, A('police', 'His face'), 1540, 200, 320, 320, (c) => { person(c, { x: 0, y: 330, s: 0.7, pose: 'stand', style: C.black, mouth: 'smirk', shadow: false, seed: 390 }); L.label(c, 'face', 0, 130, { size: 34 }); }, { rot: -0.03, seed: 146 });
      if (t > A('police', 'All read')) L.label(ctx, 'read from 2 km away', 1360, 640, { size: 56, color: '#E0703E' });
      return;
    }
    L.stampText(ctx, t, tPin + 0.1, 'COVER YOUR PIN', 960, 170, { size: 90, color: '#3D7A74' });
    L.keypad(ctx, 960, 620, 1.3, t, { cover: L.fade(t, tPin + 0.6, 0.6) });
  }
  function sunset(ctx, t, s) {
    cliffTop(ctx, t, { warm: 1 });
    L.kite(ctx, 640 + Math.sin(t * 0.6) * 40, 240, 0.9, t);
    // a family hugging the boy, tiny, on the beach below
    for (let i = 0; i < 3; i++) G.ellipse(ctx, 320 + i * 22, 820 - (i === 1 ? 0 : 6), 7, 7, { fill: '#5A3A22', lw: 2, seed: 740 + i });
    G.poly(ctx, [[300, 830], [380, 830], [372, 870], [308, 870]], { fill: '#E8718D', lw: 2, seed: 744 });
    const tGrip = A('sunset', 'grips');
    person(ctx, { x: 1180, y: 700, s: 0.9, pose: 'floor', style: C.grandpa, handR: t > tGrip ? [230, -150] : null, look: 1, mouth: talk(t, 'grandpa', 'smile'), eyes: 'happy', seed: 500 });
    person(ctx, { x: 1420, y: 700, s: 0.9, pose: 'floor', style: C.theo, look: -0.8, lookY: -0.2, mouth: t > A('sunset', 'gold water') ? 'smile' : 'flat', eyes: t > A('sunset', 'Beautiful') ? 'happy' : 'normal', seed: 300 });
    if (t > A('sunset', 'gold water')) L.label(ctx, 'gold water', 380, 600, { size: 46, alpha: L.fade(t, A('sunset', 'gold water')), color: '#F6F0E2' });
    if (t > A('sunset', 'A red kite')) L.label(ctx, 'a red kite', 640, 120, { size: 46, alpha: L.fade(t, A('sunset', 'A red kite')) });
    if (t > A('sunset', 'family')) L.label(ctx, 'a family, hugging', 340, 960, { size: 42, alpha: L.fade(t, A('sunset', 'family')), color: '#F6F0E2' });
    L.light(ctx, 420, 600, '#FFF4DA', '#C77A5E', 'multiply', 0.55);
  }
  function real(ctx, t, s) {
    G.bg(ctx, '#2F4A3E');
    const tPhys = A('real', 'Light spreads'), tPizza = A('real', 'Eyes...');
    if (t < tPhys) {
      L.stampText(ctx, t, s.t0 + 0.3, 'IS ANY OF THIS REAL?', 960, 160, { size: 80, color: '#F2B84B' });
      const rows = [[A('real', 'Macular'), '✓  macular degeneration: real'], [A('real', 'Rip currents'), '✓  rip currents: real'], [A('real', 'Physics says'), '✗  eyes 100× sharper: physics says no']];
      rows.forEach(([tt, txt], i) => L.label(ctx, txt, 960, 380 + i * 160, { size: 56, color: i < 2 ? '#9FE3B0' : '#F2A08A', alpha: L.fade(t, tt), fam: 'Gochi Hand' }));
      return;
    }
    if (t < tPizza) {
      // light through a pupil spreads into rings: a few millimetres is already near the limit
      G.line(ctx, [[200, 300], [200, 460]], { lw: 8, color: '#F6F0E2' }); G.line(ctx, [[200, 520], [200, 680]], { lw: 8, color: '#F6F0E2' });
      for (let i = 0; i < 6; i++) G.line(ctx, [[-20, 380 + i * 20], [200, 380 + i * 20 + (i - 2.5) * 6]], { lw: 3, color: 'rgba(242,184,75,0.8)' });
      for (let r = 1; r <= 6; r++) { const k = clamp((t - tPhys) * 1.2 - r * 0.2); if (k <= 0) continue; ctx.save(); ctx.globalAlpha = k * (1 - r * 0.12); G.ellipse(ctx, 200, 490, r * 90, r * 90, { fill: null, stroke: '#F2B84B', lw: 4, seed: 750 + r }); ctx.restore(); }
      L.label(ctx, 'pupil', 200, 760, { size: 40, color: '#F6F0E2' });
      if (t > A('real', 'few millimeters')) L.label(ctx, 'normal pupil: ~3 mm', 1300, 360, { size: 54, color: '#F6F0E2' });
      if (t > A('real', 'near the limit')) L.label(ctx, '(already near the limit)', 1300, 440, { size: 40, color: '#C9D6C2' });
      if (t > A('real', 'hundred times wider')) L.label(ctx, '100× sharper → 100× wider', 1300, 600, { size: 54, color: '#F2B84B' });
      if (t > A('real', 'thirty centimeters')) L.stampText(ctx, t, A('real', 'thirty centimeters') + 0.3, '≈ 30 cm', 1300, 760, { size: 100, color: '#E0703E' });
      return;
    }
    // Theo with pizza-sized eyes, trying binoculars
    G.bg(ctx, '#F4EDE0');
    person(ctx, { x: 960, y: 1100, s: 1.3, pose: 'stand', style: C.theo, mouth: 'smile', seed: 300 });
    const hy = 1100 - 1.3 * 404, k = L.pop(t, A('real', 'pizzas'), 0.5);
    for (const dx of [-1, 1]) { if (k <= 0) break; const ex = 960 + dx * 175, er = 165 * k; G.ellipse(ctx, ex, hy - 10, er, er, { fill: '#E9A65A', lw: 6, seed: 760 + dx }); G.ellipse(ctx, ex, hy - 10, er * 0.86, er * 0.86, { fill: '#F2D14B', lw: 3, seed: 762 + dx }); for (let i = 0; i < 5; i++) G.ellipse(ctx, ex + Math.cos(i * 1.3 + dx) * er * 0.5, hy - 10 + Math.sin(i * 1.3 + dx) * er * 0.5, 16 * k, 16 * k, { fill: '#C0392B', lw: 2, seed: 770 + i + dx * 10 }); G.ellipse(ctx, ex + 20, hy - 10, 46 * k, 46 * k, { fill: '#1A1414', lw: 3, seed: 780 + dx }); }
    if (t > A('real', 'birdwatching')) { G.rrect(ctx, 540, hy + 180, 120, 60, 14, { fill: '#2A2320', lw: 3, seed: 790 }); L.label(ctx, 'binoculars?', 600, hy + 300, { size: 44, rot: -0.06 }); }
  }
  function sting(ctx, t, s) {
    L.sky(ctx, '#0B0E26', '#2E2A5C', H);
    for (let i = 0; i < 60; i++) G.star(ctx, G.rnd(i, 1) * W, G.rnd(i, 2) * 700, 2 + G.rnd(i, 3) * 4, { fill: '#F6F0E2' });
    G.ellipse(ctx, 1460, 220, 50, 50, { fill: '#F3EBD2', lw: 4, seed: 800 });
    G.poly(ctx, [[-20, 860], [W + 20, 840], [W + 20, H + 20], [-20, H + 20]], { fill: '#151830', lw: 4, seed: 801 });
    person(ctx, { x: 640, y: 1000, s: 0.95, pose: 'stand', style: C.theo, lookY: -1, look: 1, eyes: t > A('sting', 'moves') ? 'wide' : 'normal', mouth: 'o', seed: 300 });
    L.lens(ctx, t, L.lensT('moon2'), s.t1, { tx: 1460, ty: 220, cx: 1180, cy: 560, r: 260 }, (c, r) => {
      c.fillStyle = '#0B0E26'; c.fillRect(-r, -r, 2 * r, 2 * r);
      G.ellipse(c, 0, 0, 230, 230, { fill: '#E9E2CC', lw: 5, seed: 802 });
      [[-80, -60, 46], [90, 50, 56], [-40, 90, 34]].forEach(([x, y, rr], i) => G.ellipse(c, x, y, rr, rr * 0.85, { fill: '#CFC6AC', lw: 3, seed: 803 + i }));
      if (t > A('sting', 'moves')) { const mx = lerp(-120, 120, L.u(t, A('sting', 'moves'), s.t1)); G.ellipse(c, mx, -10, 10, 7, { fill: '#1A1414', lw: 2, seed: 806 }); G.line(c, [[mx - 40, -10], [mx - 12, -10]], { lw: 2, color: 'rgba(26,20,20,0.5)' }); }
    });
    L.light(ctx, 1200, 500, '#FFFFFF', '#3A3570', 'multiply', 0.4);
  }
  function cta(ctx, t, s) {
    G.bg(ctx, '#27305C');
    G.rays(ctx, 960, 560, { n: 36, r0: 150, r1: 1500, color: 'rgba(242,184,75,0.2)', lw: 20, seed: 9, spin: (t - s.t0) * 0.12 });
    L.stampText(ctx, t, S.ev.cta, 'WHAT IF?', 960, 220, { size: 140, color: '#E0703E' });
    L.label(ctx, 'normal eyes... or pizza eyes?', 960, 360, { size: 56, color: '#F6F0E2', alpha: L.fade(t, S.ev.cta + 0.4) });
    if (t > A('cta', 'Tell us')) { G.rrect(ctx, 560, 470, 800, 150, 30, { fill: '#F6F0E2', lw: 5, seed: 810 }); G.text(ctx, '💬  which superpower next?', 960, 565, { size: 50, align: 'center', fam: 'Patrick Hand', weight: 400 }); }
    if (t > A('cta', 'Hit like')) { const kl = L.pop(t, A('cta', 'Hit like') + 0.2), ks = L.pop(t, A('cta', 'subscribe') + 0.1);
      if (kl > 0) { ctx.save(); ctx.translate(740, 760); ctx.scale(kl, kl); G.rrect(ctx, -170, -60, 340, 120, 60, { fill: '#F6F0E2', lw: 5, seed: 811 }); G.text(ctx, '👍 Like', 0, 20, { size: 56, align: 'center', fam: 'Bungee', weight: 400 }); ctx.restore(); }
      if (ks > 0) { ctx.save(); ctx.translate(1180, 760); ctx.scale(ks, ks); G.rrect(ctx, -220, -60, 440, 120, 60, { fill: '#D8352A', lw: 5, seed: 812 }); G.text(ctx, 'SUBSCRIBE', 0, 20, { size: 56, align: 'center', fam: 'Bungee', weight: 400, color: '#FFFFFF' }); ctx.restore(); } L.label(ctx, 'Part Two: something on the Moon...', 960, 920, { size: 44, color: '#F2B84B', alpha: L.fade(t, A('cta', 'Part Two')) }); }
  }

  const SCENES = { beach, moon, hill, plate, acuity, rule, title, class: classroom, stadium, birds, fovea, harbor, message, cost, grandpa, cliff, roof, sea, choice, call, kite, nova, saved, police, sunset, real, sting, cta };
  Studio.film({
    fadeOut: 1.4,
    async init() { VO = await Studio.loadJSON('out/voice.json'); SUBS = Subs.fromVoice(VO, { maxWords: 7 }); },
    draw(ctx, t) {
      const sc = S.sceneAt(t);
      G.setStyle(sc.id === 'real' && t < A('real', 'Eyes...') ? 'chalk' : 'paper');
      // a slow push-in on every scene, and a flash + shake on the big hits
      const u = clamp((t - sc.t0) / (sc.t1 - sc.t0));
      const z = 1 + 0.035 * ease.inOutQuad(u);
      const hit = [S.ev.title, S.ev.choice, S.ev.kite, S.ev.saved, S.ev.cta].filter((c) => t >= c && t - c < 0.6).pop();
      const shake = hit !== undefined ? 10 * Math.exp(-(t - hit) * 9) : 0;
      ctx.save();
      ctx.translate(W / 2 + U.noise1(t * 30, 1) * shake, H / 2 + U.noise1(t * 30, 2) * shake); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
      SCENES[sc.id](ctx, t, sc);
      ctx.restore();
      // the first frames of a scene: a quick dip from paper (a soft cut)
      const d = t - sc.t0;
      if (d < 0.18 && sc.t0 > 0 && hit === undefined) { ctx.fillStyle = `rgba(244,237,224,${0.8 * (1 - d / 0.18)})`; ctx.fillRect(0, 0, W, H); }
      if (hit !== undefined && t - hit < 0.18) { ctx.fillStyle = `rgba(255,255,255,${0.75 * (1 - (t - hit) / 0.18)})`; ctx.fillRect(0, 0, W, H); }
      if (t < 0.6) { ctx.fillStyle = `rgba(0,0,0,${1 - t / 0.6})`; ctx.fillRect(0, 0, W, H); }
      Subs.draw(ctx, t, SUBS, { style: 'karaoke', size: 50, y: 1010 });
    },
  });
})();
