// THE FILM: 32 scenes, one per beat of the story. Each scene draws from the times of its own lines
// (SC[id].lines[i].t) and the shared hits (ev), so the picture always lands on the words.
(function () {
  const U = globalThis.U, G = globalThis.G, Ch = globalThis.Ch, UI = globalThis.UI, Data = globalThis.Data, Subs = globalThis.Subs, S = globalThis.SCORE, Studio = globalThis.Studio, Shots = globalThis.Shots, K = globalThis.K;
  const { clamp, ease, lerp, pulse, tween } = U;
  const { SC, ev } = S;
  const W = G.W, H = G.H, INK = K.INK;
  let VO = null, SUBS = [];
  const at = (id, i) => S.L(id, i).t;
  const end = (id, i) => S.L(id, i).end;
  const talk = (who, t, idle = 'flat') => { const m = VO ? Subs.mouth(VO, t, who) : null; return m && m.talking ? m : idle; };
  const since = (t, t0) => Math.max(0, t - t0);
  const fadeIn = (t, t0, d = 0.3) => clamp((t - t0) / d);
  const ground = (ctx, y, color, seed = 5) => G.poly(ctx, [[-60, y], [W + 60, y], [W + 60, H + 60], [-60, H + 60]], { fill: color, lw: 5, seed, hatch: { color: 'rgba(0,0,0,0.10)', gap: 10 } });
  const sign = (ctx, str, x, y, w, h, o = {}) => { G.rrect(ctx, x, y, w, h, 10, { fill: o.fill || '#FBF7EE', lw: 5, seed: o.seed || 9 }); G.text(ctx, str, x + w / 2, y + h * 0.68, { size: o.size || h * 0.5, align: 'center', fam: o.fam || 'Bungee', weight: 400, color: o.color || INK }); };

  // ======================= COLD OPEN =======================
  function spider(ctx, t) {
    K.sky(ctx, '#BFE3E8', '#F4EDE0');
    G.ellipse(ctx, 1620, 170, 90, 90, { fill: K.GOLD, lw: 5, seed: 2 });
    ground(ctx, 860, '#8CC07A', 3);
    // a tree branch the spider drops from
    G.limb(ctx, [[1960, 120], [1400, 150], [980, 120]], { color: '#7A5534', lw: 40, outline: 5, seed: 11 });
    for (let i = 0; i < 6; i++) G.ellipse(ctx, 1000 + i * 150, 110 + (i % 2) * 40, 90, 50, { fill: '#5E9E5A', lw: 4, seed: 12 + i, hatch: { color: 'rgba(0,0,0,0.12)', gap: 8 } });
    const hand = [1205, 640];
    K.sam(ctx, { x: 900, y: 940, s: 1.15, handR: [255, -300], look: 0.6, lookY: 0.4, eyes: 'normal', mouth: t > at('spider', 2) ? 'smirk' : 'flat' });
    // drop on its thread, land on the palm at ev.spiderLand, then walk up the arm
    const drop = ease.outBounce(clamp((t - at('spider', 0)) / (ev.spiderLand - at('spider', 0))));
    const walk = ease.inOutQuad(clamp((t - at('spider', 2)) / 2.8));
    const sx = lerp(hand[0], 1040, walk), sy = lerp(lerp(130, hand[1] - 34, drop), 570, walk);
    if (walk < 0.05) G.line(ctx, [[hand[0], 130], [sx, sy - 40]], { color: 'rgba(60,60,60,0.7)', lw: 2, seed: 20 });
    K.spider(ctx, sx, sy, 0.75, t, { walk: walk > 0 && walk < 1, rot: walk > 0 ? -0.4 : 0 });
    // the fear meter: dead still at zero
    if (t > at('spider', 3)) {
      K.meter(ctx, 400, 360, 170, 0, { seed: 5 });
      K.stamp(ctx, 'ZERO', 400, 640, t, at('spider', 3) + 0.9, { size: 90, color: K.TEAL });
    }
  }
  function haunted(ctx, t) {
    K.room(ctx, '#3A2E4A', '#2A2233', 21);
    // cobwebs and a flickering bulb that dies
    const dead = t >= ev.lightsOut;
    const flick = !dead && t > at('haunted', 0) + 0.3 ? (Math.sin(t * 47) > 0.2 ? 1 : 0.25) : 1;
    G.line(ctx, [[960, 0], [960, 140]], { color: INK, lw: 4, seed: 22 });
    G.ellipse(ctx, 960, 170, 34, 40, { fill: dead ? '#55505A' : '#FFE9A0', lw: 4, seed: 23 });
    if (!dead) K.spot(ctx, 960, 200, 900, 0.35 * flick);
    for (const [x, y, r] of [[0, 0, 180], [W, 0, 220]]) for (let i = 0; i < 6; i++) G.line(ctx, [[x, y], [x + (x ? -1 : 1) * r * Math.cos(i * 0.3), y + r * Math.sin(i * 0.3)]], { color: 'rgba(230,230,240,0.35)', lw: 2, seed: 24 + i });
    const scared = t >= ev.monster;
    // two friends who shriek, and Sam
    K.person(ctx, { x: 520, y: 950, style: K.KID1, seed: 500, eyes: scared ? 'wide' : 'normal', mouth: scared ? 'open' : 'smile', brows: scared ? 'worried' : 'neutral', gesture: scared ? 'cheer' : null, sweat: scared ? 1 : 0, sx: 1, headX: scared ? U.noise1(t * 20, 1) * 6 : 0 });
    K.person(ctx, { x: 760, y: 960, style: K.KID2, seed: 520, eyes: scared ? 'wide' : 'normal', mouth: scared ? 'open' : 'flat', brows: scared ? 'worried' : 'neutral', gesture: scared ? 'facepalm' : null, sweat: scared ? 1 : 0 });
    const tapping = t >= ev.tapShoulder;
    // the monster leaps in from the dark on its hit
    if (scared) {
      const leap = ease.outBack(clamp((t - ev.monster) / 0.25));
      K.monster(ctx, lerp(1700, 1380, leap), 980 - Math.sin(clamp((t - ev.monster) / 0.25) * Math.PI) * 120, 1.25, t, { scared: tapping, look: tapping ? -1 : -0.5, arms: tapping ? 0.4 : 1 });
    }
    K.sam(ctx, { x: tapping ? 1120 : 1020, y: 960, sx: 1, handR: tapping ? [190, -330 + Math.sin(t * 12) * 6] : undefined, look: scared ? 1 : 0, mouth: talk('sam', t, 'flat') });
    // darkness: lights out until the monster's eyes; a little moonlight keeps faces readable
    if (dead) K.dark(ctx, scared ? 0.32 : 0.82);
    K.flash(ctx, t, ev.monster, 0.18);
    if (scared) K.stamp(ctx, 'AAAAH!', 620, 300, t, ev.shriek, { size: 120, color: K.GOLD, rot: -0.08 });
    if (scared) K.meter(ctx, 260, 220, 110, 0.97, { shake: 1, t, seed: 25, label: 'THEM' });
    if (tapping) K.meter(ctx, 1640, 220, 110, 0, { seed: 26, label: 'SAM' });
  }
  // a coaster track: x across the frame, y climbs to a crest then drops
  const trackY = (x) => (x < 1300 ? lerp(930, 300, ease.inOutQuad(clamp((x - 100) / 1200))) : lerp(300, 1100, ease.inQuad(clamp((x - 1300) / 500))));
  function coaster(ctx, t, s, o = {}) {
    K.sky(ctx, o.sky0 || '#9FD3F0', o.sky1 || '#F4EDE0');
    for (let i = 0; i < 4; i++) G.ellipse(ctx, 200 + i * 520, 160 + (i % 2) * 70, 120, 40, { fill: '#FFFFFF', lw: 3, seed: 30 + i });
    // supports and rails
    for (let x = 160; x < 1700; x += 120) G.line(ctx, [[x, trackY(x)], [x, 1100]], { color: '#A0522D', lw: 8, seed: 31 + x });
    const rail = []; for (let x = 60; x <= 1820; x += 30) rail.push([x, trackY(x)]);
    G.line(ctx, rail, { color: '#C0392B', lw: 14, seed: 40 });
    G.line(ctx, rail.map(([x, y]) => [x, y + 22]), { color: '#8E2A20', lw: 8, seed: 41 });
    // the car creeps up to the crest
    const u = o.u ?? ease.inOutQuad(clamp((t - s.t0) / (o.climb || 6)));
    const cx = lerp(380, 1260, u), cy = trackY(cx);
    const ang = Math.atan2(trackY(cx + 20) - trackY(cx - 20), 40);
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(ang);
    const riders = [{ style: K.KID1, seed: 600 }, { style: K.KID2, seed: 620 }, { style: K.ADULT, seed: 640 }];
    riders.forEach((r, i) => Ch.person(ctx, { x: -330 + i * 130, y: -40, pose: 'sit', s: 0.55, style: r.style, seed: r.seed, eyes: o.calm ? 'normal' : 'wide', mouth: o.calm ? 'smile' : 'open', brows: o.calm ? 'neutral' : 'worried', gesture: 'cheer', sweat: o.calm ? 0 : 1 }));
    const yawn = !o.calm && t > ev.yawn && t < ev.yawn + 2.2;
    Ch.person(ctx, { x: 70, y: -40, pose: 'sit', s: 0.55, style: K.SAM, seed: 100, eyes: o.bored ? 'sleep' : yawn ? 'closed' : 'normal', mouth: yawn ? 'o' : 'flat', handR: [60, -150] });
    // the popcorn bucket stays put
    G.poly(ctx, [[96, -150], [150, -150], [140, -80], [106, -80]], { fill: '#FFFFFF', lw: 4, seed: 45, hatch: { color: K.RED, gap: 10, angle: 1.57, lw: 5 } });
    for (let i = 0; i < 6; i++) G.ellipse(ctx, 102 + i * 9, -156 - (i % 2) * 6, 9, 8, { fill: '#FFF3C4', lw: 2, seed: 46 + i });
    G.rrect(ctx, -400, -60, 560, 70, 18, { fill: '#2E6FB5', lw: 6, seed: 47 });
    ctx.restore();
    if (!o.calm && t > at('coaster', 1)) K.stamp(ctx, 'AAAAAAH!', 520, 230, t, at('coaster', 1) + 0.2, { size: 100, color: K.GOLD, rot: -0.06 });
    if (yawn) K.label(ctx, '*yawn*', cx + 140, cy - 200, t, ev.yawn, { size: 60 });
  }

  // ======================= THE BRAIN =======================
  const brainShape = (cx, cy, s) => G.wobble(G.ellPts(cx, cy, 300 * s, 210 * s), 81, 14 * s);
  function brainDraw(ctx, cx, cy, s, t, glow, o = {}) {
    G.shape(ctx, brainShape(cx, cy, s), { fill: '#F2A7B5', lw: 6, seed: 82, hatch: { color: 'rgba(160,60,90,0.18)', gap: 12 } });
    for (let i = 0; i < 7; i++) {
      const pts = []; for (let k = 0; k < 8; k++) pts.push([cx + (-240 + i * 70 + Math.sin(k + i) * 20) * s, cy + (-160 + k * 45) * s]);
      G.line(ctx, pts, { color: 'rgba(150,50,80,0.45)', lw: 5 * s, seed: 83 + i });
    }
    // the two almonds
    for (const sd of [-1, 1]) {
      const ax = cx + sd * 70 * s, ay = cy + 60 * s;
      if (glow > 0) { const g = ctx.createRadialGradient(ax, ay, 5, ax, ay, 120 * s); g.addColorStop(0, `rgba(255,80,60,${0.8 * glow})`); g.addColorStop(1, 'rgba(255,80,60,0)'); ctx.fillStyle = g; ctx.fillRect(ax - 130 * s, ay - 130 * s, 260 * s, 260 * s); }
      ctx.save(); ctx.translate(ax, ay); ctx.rotate(sd * 0.5);
      G.ellipse(ctx, 0, 0, 22 * s, 38 * s, { fill: o.off ? '#9A9AA2' : glow > 0.3 ? '#FF5A3C' : '#C8875A', lw: 4, seed: 90 + sd });
      ctx.restore();
    }
  }
  function brain(ctx, t) {
    G.bg(ctx, '#F4EDE0');
    const i = (n) => t >= at('brain', n);
    if (!i(1)) {
      // 0: meet Sam
      G.rays(ctx, 960, 600, { n: 28, r0: 120, r1: 1400, color: 'rgba(224,112,62,0.18)', lw: 22, seed: 3, spin: t * 0.05 });
      K.sam(ctx, { x: 960, y: 1000, s: 1.25, mouth: 'smirk', gesture: 'wave' });
      K.stamp(ctx, 'SAM', 960, 260, t, at('brain', 0) + 0.45, { size: 160, color: K.ORANGE });
      return;
    }
    const glow = i(3) && !i(7) ? 0.6 + 0.4 * Math.sin(t * 18) : i(1) ? 0.25 : 0;
    brainDraw(ctx, 960, 420, 1, t, glow);
    if (i(2)) { K.label(ctx, 'the AMYGDALA', 960, 140, t, at('brain', 2), { size: 70, color: K.RED }); G.line(ctx, [[900, 170], [905, 440]], { color: K.RED, lw: 4, seed: 95 }); G.line(ctx, [[1020, 170], [1025, 440]], { color: K.RED, lw: 4, seed: 96 }); }
    if (i(3) && !i(7)) {
      const sl = clamp((t - ev.snake) / 0.6);
      K.snake(ctx, K.slither(-300 + 500 * sl, 300 + 500 * sl, 860, t), { tongue: Math.sin(t * 10) > 0 });
      for (let k = 0; k < 3; k++) if (t > ev.snake + 0.2) K.bolt(ctx, 640 + k * 50, 520 + k * 30, 0.8, K.GOLD, 97 + k);
    }
    const icons = [[4, 1240, 'HEART', '♥'], [5, 1480, 'ADRENALINE', '!'], [6, 1720, 'MUSCLES', '💪']];
    if (!i(7)) icons.forEach(([n, x, lab]) => {
      if (!i(n)) return;
      const k = K.stampK(t, at('brain', n));
      ctx.save(); ctx.translate(x, 640); ctx.scale(k, k);
      if (lab === 'HEART') G.heart(ctx, 0, -10, 3 + 0.5 * pulse(t, Math.floor(t * 2.4) / 2.4, 9));
      else if (lab === 'ADRENALINE') { G.shape(ctx, [[0, -90], [40, -10], [30, 30], [0, 44], [-30, 30], [-40, -10]], { fill: K.RED, lw: 5, seed: 98, closed: true }); }
      else { G.limb(ctx, [[-60, 30], [-10, -10], [10, -80]], { color: K.SAM.skin, lw: 40, outline: 5, seed: 99 }); G.ellipse(ctx, -16, -30, 34, 26, { fill: K.SAM.skin, lw: 5, seed: 100 }); }
      G.text(ctx, lab, 0, 110, { size: 36, align: 'center', fam: 'Bungee', weight: 400, color: INK });
      ctx.restore();
    });
    if (i(7) && !i(8)) {
      // most people: needles pinned
      [[560, K.KID1, 700], [960, K.ADULT, 720], [1360, K.KID2, 740]].forEach(([x, st, sd]) => { K.person(ctx, { x, y: 1000, s: 0.75, style: st, seed: sd, eyes: 'wide', mouth: 'open', brows: 'worried', sweat: 1 }); K.meter(ctx, x, 640, 80, 0.95, { shake: 1, t, seed: sd }); });
    }
    if (i(8)) {
      K.sam(ctx, { x: 1500, y: 1000, s: 1, mouth: 'flat' });
      K.meter(ctx, 1500, 640, 90, 0, { seed: 7 });
      brainDraw(ctx, 700, 520, 0.9, t, 0, { off: true });
      K.stamp(ctx, 'NOTHING.', 700, 900, t, ev.nothing, { size: 100, color: '#8A8A92' });
    }
  }
  function sm(ctx, t) {
    G.bg(ctx, '#E9E2D2');
    const i = (n) => t >= at('sm', n);
    if (!i(3)) {
      // a case file
      K.card(ctx, 360, 150, 1200, 760, t, SC.sm.t0, (c, w, h) => {
        G.rrect(c, 40, 40, 360, 440, 6, { fill: '#D8D0C0', lw: 4, seed: 110 });
        Ch.person(c, { x: 220, y: 600, s: 0.85, style: K.SM, seed: 700, mouth: 'smile' });
        G.text(c, 'CASE FILE', 460, 120, { size: 70, fam: 'Bungee', weight: 400, color: INK });
        G.text(c, 'Patient: "S.M."', 460, 220, { size: 58, fam: 'Patrick Hand', weight: 400 });
        if (t > at('sm', 2)) {
          G.text(c, 'Both amygdalae damaged', 460, 310, { size: 50, fam: 'Patrick Hand', weight: 400, color: K.RED });
          G.text(c, 'by a rare disease', 460, 370, { size: 50, fam: 'Patrick Hand', weight: 400, color: K.RED });
        }
      }, { rot: -0.02, seed: 111 });
      K.stamp(ctx, 'REAL', 1380, 820, t, at('sm', 1) + 1.2, { size: 120, color: K.RED, rot: -0.2 });
      return;
    }
    if (!i(4)) {
      // she handles snakes
      Ch.person(ctx, { x: 960, y: 980, s: 1.1, style: K.SM, seed: 700, mouth: 'smile', eyes: 'happy', handL: [-150, -300], handR: [150, -300] });
      K.snake(ctx, Array.from({ length: 16 }, (_, k) => [800 + k * 22, 660 + Math.sin(k * 0.8 + t * 3) * 30]), { tongue: true, lw: 30 });
      return;
    }
    // ...and pokes a monster, who jumps
    K.room(ctx, '#3A2E4A', '#2A2233', 112);
    K.spot(ctx, 960, 400, 900, 0.3);
    const poke = at('sm', 4) + 1.4;
    const jumped = t > poke + 0.3;
    K.monster(ctx, 1220, 980 - (jumped ? Math.max(0, Math.sin(clamp((t - poke - 0.3) / 0.5) * Math.PI)) * 160 : 0), 1, t, { scared: jumped, look: -1, arms: jumped ? 1 : 0.5 });
    Ch.person(ctx, { x: 800, y: 980, s: 1, style: K.SM, seed: 700, mouth: 'grin', eyes: 'happy', gesture: t > poke - 0.5 ? 'point' : null });
    if (jumped) K.stamp(ctx, '!!', 1250, 420, t, poke + 0.3, { size: 140, color: K.GOLD });
  }
  function rule(ctx, t) {
    G.bg(ctx, '#F4EDE0');
    const i = (n) => t >= at('rule', n);
    if (!i(3)) {
      K.label(ctx, 'YOUR RULE', 960, 190, t, SC.rule.t0, { size: 90, fam: 'Bungee', color: INK });
      K.card(ctx, 260, 330, 620, 380, t, at('rule', 1), (c, w, h) => { G.text(c, 'FEAR', w / 2, 170, { size: 110, align: 'center', fam: 'Bungee', weight: 400, color: '#8A8A92' }); G.text(c, 'gone', w / 2, 290, { size: 80, align: 'center', fam: 'Patrick Hand', weight: 400 }); }, { rot: -0.03, seed: 120 });
      K.card(ctx, 1040, 330, 620, 380, t, at('rule', 2), (c, w, h) => { G.text(c, 'DANGER', w / 2, 170, { size: 110, align: 'center', fam: 'Bungee', weight: 400, color: K.RED }); G.text(c, 'still here', w / 2, 290, { size: 80, align: 'center', fam: 'Patrick Hand', weight: 400 }); }, { rot: 0.03, seed: 121 });
      if (i(1)) G.line(ctx, [[300, 520], [840, 470]], { color: INK, lw: 10, seed: 122, alpha: fadeIn(t, at('rule', 1) + 0.8) });
      return;
    }
    // the alarm on the wall, and its plug pulled
    K.room(ctx, '#EADFCB', '#C9B79A', 123);
    const ring = !i(5);
    const wob = ring ? Math.sin(t * 40) * 0.08 : 0;
    ctx.save(); ctx.translate(960, 380); ctx.rotate(wob);
    G.ellipse(ctx, 0, 0, 170, 170, { fill: K.RED, lw: 7, seed: 124, hatch: { color: 'rgba(0,0,0,0.12)', gap: 12 } });
    G.ellipse(ctx, 0, 0, 70, 70, { fill: '#C9C2B4', lw: 5, seed: 125 });
    G.text(ctx, 'FEAR ALARM', 0, 250, { size: 54, align: 'center', fam: 'Bungee', weight: 400, color: INK });
    ctx.restore();
    if (ring) for (let k = 0; k < 3; k++) { const r = 210 + ((t * 300 + k * 80) % 240); ctx.strokeStyle = `rgba(216,72,59,${1 - (r - 210) / 240})`; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(960, 380, r, -0.6, 0.6); ctx.stroke(); ctx.beginPath(); ctx.arc(960, 380, r, Math.PI - 0.6, Math.PI + 0.6); ctx.stroke(); }
    // the cable to the socket
    const pulled = t >= ev.unplug;
    const px = pulled ? 1280 + ease.outBack(clamp((t - ev.unplug) / 0.3)) * 160 : 1280;
    G.line(ctx, [[960, 550], [1000, 760], [1200, 790], [px, 780]], { color: INK, lw: 8, seed: 126 });
    G.rrect(ctx, px, 750, 70, 60, 8, { fill: '#F4F1EA', lw: 5, seed: 127 });
    G.rrect(ctx, 1500, 720, 110, 140, 10, { fill: '#FBF7EE', lw: 5, seed: 128 });
    for (const dx of [-18, 18]) G.rrect(ctx, 1555 + dx - 5, 770, 10, 34, 3, { fill: INK, lw: 0, seed: 129 });
    if (pulled) { K.flash(ctx, t, ev.unplug, 0.12); K.stamp(ctx, 'UNPLUGGED', 960, 950, t, ev.unplug, { size: 90, color: '#8A8A92' }); }
    if (i(3) && !i(4)) K.label(ctx, 'fear  =  the alarm', 960, 900, t, at('rule', 4), { size: 64 });
  }
  function title(ctx, t) {
    G.bg(ctx, '#1E1B2E');
    G.rays(ctx, 960, 560, { n: 36, r0: 140, r1: 1600, color: 'rgba(242,184,75,0.16)', lw: 22, seed: 9, spin: t * 0.08 });
    K.stars(ctx, t, 90, 4, 0.8);
    K.sam(ctx, { x: 960, y: 1020, s: 1.15, crossArms: true, mouth: 'smirk', look: 0.2 });
    const k = K.stampK(t, ev.title);
    if (k > 0) {
      ctx.save(); ctx.translate(960, 230); ctx.scale(k, k); ctx.rotate(-0.03);
      G.text(ctx, 'WHAT IF YOU HAD', 0, -40, { size: 96, align: 'center', fam: 'Bungee', weight: 400, color: '#FBF7EE', stroke: INK, strokeW: 10 });
      G.text(ctx, 'ZERO FEAR?', 0, 110, { size: 170, align: 'center', fam: 'Bungee', weight: 400, color: K.ORANGE, stroke: INK, strokeW: 12 });
      ctx.restore();
    }
    K.flash(ctx, t, ev.title, 0.25);
    if (t > at('title', 1)) { K.meter(ctx, 330, 700, 110, 0, { seed: 8 }); K.label(ctx, '...and what is life like?', 1500, 760, t, at('title', 1) + 0.3, { size: 54, color: '#FBF7EE' }); }
  }

  // ======================= LIFE WITHOUT FEAR =======================
  function speech(ctx, t) {
    const i = (n) => t >= at('speech', n);
    if (!i(3)) {
      K.room(ctx, '#7A3B3B', '#5A4636', 130);
      // curtains, stage, podium
      for (const sd of [0, 1]) G.poly(ctx, [[sd ? W - 260 : 0, 0], [sd ? W : 260, 0], [sd ? W : 260, 700], [sd ? W - 260 : 0, 700]], { fill: '#A23A3A', lw: 5, seed: 131 + sd, hatch: { color: 'rgba(0,0,0,0.2)', gap: 30, angle: 1.57, lw: 6 } });
      G.rrect(ctx, 260, 560, 1400, 60, 6, { fill: '#8A5A3A', lw: 5, seed: 133 });
      K.spot(ctx, 960, 300, 600, 0.4);
      K.sam(ctx, { x: 960, y: 580, s: 0.85, gesture: 'mic', mouth: talk('narrator', t, 'smile'), look: Math.sin(t * 0.7) * 0.6 });
      G.rrect(ctx, 880, 430, 160, 150, 8, { fill: '#6A4A2A', lw: 5, seed: 134 });
      // 500 heads in rows
      for (let r = 0; r < 5; r++) for (let c = 0; c < 26; c++) {
        const x = -40 + c * 78 + (r % 2) * 39, y = 700 + r * 85;
        const tone = ['#E2AE86', '#A86E4B', '#F3D2B3', '#8D5A3B', '#C98A62'][(c + r * 3) % 5];
        G.ellipse(ctx, x, y, 34, 38, { fill: tone, lw: 4, seed: 135 + r * 30 + c });
        G.ellipse(ctx, x, y - 22, 34, 18, { fill: ['#2A1A10', '#5A3A22', '#C8742F', '#1A1A1A'][(c * 7 + r) % 4], lw: 3, seed: 136 + r * 30 + c });
      }
      if (i(1)) K.stamp(ctx, '500 FACES', 960, 170, t, at('speech', 1) + 0.1, { size: 110, color: K.GOLD });
      if (i(2)) K.meter(ctx, 1580, 300, 100, 0, { seed: 137 });
      return;
    }
    // Mia corners you after
    K.room(ctx, '#D9E4E8', '#A8B4B8', 138);
    for (let k = 0; k < 5; k++) G.rrect(ctx, 80 + k * 380, 200, 300, 520, 8, { fill: '#7A9CC6', lw: 5, seed: 139 + k });
    K.sam(ctx, { x: 700, y: 960, s: 1, look: 1, mouth: 'flat', gesture: 'shrug' });
    K.mia(ctx, { x: 1180, y: 960, s: 1, sx: -1, look: -1, eyes: 'wide', brows: 'up', mouth: talk('mia', t, 'o') });
  }
  function exams(ctx, t) {
    K.room(ctx, '#E6EEF0', '#B9A88C', 140);
    K.stamp(ctx, '+ PLUS', 300, 170, t, SC.exams.t0 + 0.4, { size: 90, color: '#3D9A50', rot: -0.05 });
    // background kids sweating
    [[1500, K.KID1, 501], [1750, K.KID2, 521]].forEach(([x, st, sd]) => { Ch.person(ctx, { x, y: 820, pose: 'sit', s: 0.7, style: st, seed: sd, eyes: 'wide', brows: 'worried', mouth: 'wavy', sweat: 1, handR: [60, -150 + Math.sin(t * 9) * 8] }); });
    Ch.person(ctx, { x: 800, y: 820, pose: 'sit', s: 1, style: K.SAM, seed: 100, mouth: 'smirk', eyes: 'normal', handR: [150, -110 + Math.sin(t * 5) * 6], look: 0.5, lookY: 0.8 });
    G.rrect(ctx, 520, 700, 760, 40, 6, { fill: '#8A5A3A', lw: 5, seed: 141 });
    // the exam is a crossword
    ctx.save(); ctx.translate(980, 600); ctx.rotate(-0.05);
    G.rrect(ctx, -140, -80, 280, 110, 4, { fill: '#FFFFFF', lw: 4, seed: 142 });
    for (let r = 0; r < 3; r++) for (let c = 0; c < 8; c++) if ((r * 8 + c) % 5 !== 3) G.rrect(ctx, -120 + c * 30, -66 + r * 30, 26, 26, 2, { fill: (r * 8 + c) < (t - SC.exams.t0) * 6 ? '#F2B84B' : '#FFFFFF', lw: 2, seed: 143 + r * 8 + c });
    ctx.restore();
    if (t > at('exams', 1)) { K.label(ctx, 'no sweaty hands', 460, 360, t, at('exams', 1), { size: 54 }); K.label(ctx, 'no blank mind', 460, 430, t, at('exams', 1) + 0.9, { size: 54 }); }
  }
  function space(ctx, t) {
    K.room(ctx, '#EFE6D6', '#C9B79A', 150);
    const i = (n) => t >= at('space', n);
    K.stamp(ctx, '– MINUS', 330, 170, t, SC.space.t0 + 0.4, { size: 90, color: K.RED, rot: -0.05 });
    if (!i(2)) {
      // arm's length between two strangers
      K.person(ctx, { x: 640, y: 960, s: 1, style: K.ADULT, seed: 720, look: 1, handR: [300, -250] });
      K.person(ctx, { x: 1260, y: 960, s: 1, sx: -1, style: K.KID1, seed: 500, look: -1 });
      if (i(1)) { G.line(ctx, [[700, 520], [1200, 520]], { color: K.TEAL, lw: 6, seed: 151 }); K.label(ctx, "an arm's length", 950, 490, t, at('space', 1), { size: 56, color: K.TEAL }); }
      return;
    }
    // you stand half that, and people step back
    const back = i(3) ? ease.outCubic(clamp((t - at('space', 3)) / 0.8)) : 0;
    K.person(ctx, { x: 1180 + back * 220, y: 960, s: 1, sx: -1, style: K.KID1, seed: 500, look: -1, eyes: 'wide', brows: 'up', mouth: 'wavy', sweat: back });
    K.sam(ctx, { x: 960, y: 960, s: 1, look: 1, mouth: 'smile' });
    if (!i(3)) { G.line(ctx, [[1010, 520], [1140, 520]], { color: K.RED, lw: 6, seed: 152 }); K.label(ctx, 'half', 1075, 490, t, at('space', 2) + 0.3, { size: 56, color: K.RED }); }
    if (i(4)) {
      const tug = Math.sin(clamp((t - at('space', 4)) / 0.4) * Math.PI) * 30;
      K.leo(ctx, { x: 660 - tug, y: 960, look: 1, mouth: talk('leo', t, 'wavy'), brows: 'worried', handR: [240 + tug, -230] });
    }
  }
  function zoo(ctx, t) {
    const i = (n) => t >= at('zoo', n);
    K.room(ctx, '#2F4A3A', '#4A3A2A', 160);
    for (let k = 0; k < 8; k++) G.ellipse(ctx, k * 260, 120 + (k % 2) * 60, 180, 90, { fill: '#3E6B4A', lw: 4, seed: 161 + k, hatch: { color: 'rgba(0,0,0,0.15)', gap: 9 } });
    sign(ctx, 'REPTILE HOUSE', 620, 60, 680, 110, { fill: '#E8D9BC', seed: 162 });
    // glass tanks
    for (let k = 0; k < 3; k++) { G.rrect(ctx, 120 + k * 600, 250, 480, 300, 8, { fill: 'rgba(160,220,200,0.35)', lw: 6, seed: 163 + k }); }
    const keeperY = 960;
    if (!i(1)) {
      const w = Ch.walk(t, { x0: 300, speed: 220, t0: SC.zoo.t0, stride: 240 });
      K.sam(ctx, { ...w, x: Math.min(w.x, 900), pose: w.x < 900 ? 'walk' : 'stand', y: 960, mouth: 'smile' });
      Ch.person(ctx, { x: 1400, y: keeperY, s: 1, style: K.KEEPER, seed: 730, mouth: 'smile' });
      return;
    }
    const beg = i(2);
    K.sam(ctx, { x: 900, y: 960, mouth: 'grin', eyes: 'happy', handL: [-120, -250], handR: [120, -250] });
    // the python across the shoulders, getting longer and wrapping
    const pts = []; const len = 22;
    for (let k = 0; k < len; k++) { const u = k / (len - 1); const a = u * Math.PI * 1.6; pts.push([900 + Math.cos(a + Math.PI) * 170 + u * 60, 960 - 250 * K.KID - 10 + Math.sin(a) * -60 + Math.sin(t * 3 + k) * 6]); }
    K.snake(ctx, pts, { lw: 38, tongue: Math.sin(t * 8) > 0, color: '#C9A43A' });
    Ch.person(ctx, { x: 1400, y: keeperY, s: 1, sx: -1, style: K.KEEPER, seed: 730, eyes: beg ? 'wide' : 'normal', brows: beg ? 'worried' : 'neutral', mouth: talk('keeper', t, beg ? 'wavy' : 'smile'), gesture: beg ? 'dua' : 'thumbsUp', sweat: beg ? 1 : 0 });
    if (i(3)) ['PLEASE.', 'PUT.', 'THE PYTHON.', 'DOWN.'].forEach((w, k) => K.stamp(ctx, w, 1420, 330, t, at('zoo', 3) + k * ((end('zoo', 3) - at('zoo', 3)) / 4), { size: 80, color: K.GOLD, alpha: t < at('zoo', 3) + (k + 1) * ((end('zoo', 3) - at('zoo', 3)) / 4) || k === 3 ? 1 : 0 }));
  }
  function skate(ctx, t) {
    const i = (n) => t >= at('skate', n);
    if (t < ev.crack + 0.6) {
      K.sky(ctx, '#BFE3E8', '#F4EDE0');
      ground(ctx, 900, '#B8B4AC', 170);
      // the ramp: a big quarter pipe on the left
      G.poly(ctx, [[0, 300], [80, 300], [140, 600], [300, 840], [520, 900], [0, 900]], { fill: '#D9C8A8', lw: 6, seed: 171, hatch: { color: 'rgba(0,0,0,0.1)', gap: 12 } });
      G.line(ctx, [[0, 300], [90, 300]], { color: '#8A8A90', lw: 10, seed: 172 });
      if (!i(1)) { K.sam(ctx, { x: 1300, y: 900, s: 1, mouth: 'smirk', gesture: 'thumbsUp' }); return; }
      // ride down, launch, crash on the crack
      const u = clamp((t - at('skate', 2)) / (ev.crack - at('skate', 2)));
      const path = (v) => (v < 0.5 ? [lerp(70, 520, ease.inQuad(v * 2)), lerp(290, 890, Math.sin(v * Math.PI))] : [lerp(520, 1250, (v - 0.5) * 2), 890 - Math.sin((v - 0.5) * 2 * Math.PI) * 260]);
      const [x, y] = path(u);
      const wob = i(3) ? Math.sin(t * 30) * 0.12 : 0;
      ctx.save(); ctx.translate(x, y); ctx.rotate(u > 0.5 ? -0.3 + (u - 0.5) * 1.6 + wob : 0.4 - u * 0.8 + wob);
      K.sam(ctx, { x: 0, y: -12, s: 0.75, mouth: 'flat', handL: [-160, -220], handR: [160, -220], legBend: i(3) ? 0.6 + Math.sin(t * 30) * 0.3 : 0.3 });
      G.rrect(ctx, -110, -14, 220, 18, 9, { fill: '#2E6FB5', lw: 4, seed: 173 });
      for (const wx of [-70, 70]) G.ellipse(ctx, wx, 8, 14, 14, { fill: '#F2B84B', lw: 3, seed: 174 });
      ctx.restore();
      if (i(2) && !i(3)) K.label(ctx, 'first go.', 1500, 300, t, at('skate', 2), { size: 70 });
      if (i(3) && t < ev.crack) K.label(ctx, 'head: calm   knees: NOT', 1400, 300, t, at('skate', 3) + 1.2, { size: 56 });
      if (t >= ev.crack) {
        K.flash(ctx, t, ev.crack, 0.15);
        G.rays(ctx, 1250, 760, { n: 18, r0: 60, r1: 800, color: 'rgba(242,184,75,0.7)', lw: 28, seed: 175 });
        K.stamp(ctx, 'CRACK!', 1250, 520, t, ev.crack, { size: 200, color: K.RED, rot: -0.1 });
      }
      return;
    }
    // X-ray: the broken wrist, then the healing calendar
    G.bg(ctx, '#14202A');
    ctx.save(); ctx.translate(820, 520); ctx.rotate(-0.3);
    for (const [y, l] of [[-40, 520], [40, 500]]) G.rrect(ctx, -l / 2 - 200, y - 20, l, 40, 20, { fill: '#DDEBF2', lw: 4, seed: 176 + y });
    for (let k = 0; k < 5; k++) G.rrect(ctx, 120 + (k % 3) * 40, -80 + k * 30, 36, 26, 8, { fill: '#DDEBF2', lw: 3, seed: 178 + k });
    G.line(ctx, [[-120, -64], [-100, -44], [-128, -30], [-104, -16]], { color: K.RED, lw: 7, seed: 183 });
    ctx.restore();
    K.label(ctx, 'BROKEN WRIST', 820, 860, t, ev.crack + 0.7, { size: 70, fam: 'Bungee', color: '#FBF7EE' });
    if (i(6)) {
      const weeks = Math.min(6, 1 + Math.floor((t - at('skate', 6)) * 2.2));
      K.card(ctx, 1260, 260, 460, 480, t, at('skate', 6), (c, w) => {
        G.text(c, 'WEEKS', w / 2, 90, { size: 60, align: 'center', fam: 'Bungee', weight: 400 });
        G.text(c, String(weeks), w / 2, 330, { size: 220, align: 'center', fam: 'Bungee', weight: 400, color: K.ORANGE });
      }, { seed: 184 });
    }
    if (i(7)) K.label(ctx, 'fearless or not.', 1490, 860, t, at('skate', 7), { size: 64, color: '#FBF7EE' });
  }
  function bridge(ctx, t) {
    const i = (n) => t >= at('bridge', n);
    if (!i(4)) {
      K.sky(ctx, '#8FC8E8', '#E8F2F0');
      // the valley far below
      G.poly(ctx, [[-60, 1100], [-60, 500], [300, 380], [520, 1100]], { fill: '#6B8F5A', lw: 5, seed: 190, hatch: { color: 'rgba(0,0,0,0.15)', gap: 10 } });
      G.poly(ctx, [[1980, 1100], [1980, 500], [1620, 380], [1400, 1100]], { fill: '#6B8F5A', lw: 5, seed: 191, hatch: { color: 'rgba(0,0,0,0.15)', gap: 10 } });
      G.line(ctx, [[600, 1080], [800, 1040], [1000, 1070], [1300, 1040]], { color: '#4A90C0', lw: 12, seed: 192 });
      for (let k = 0; k < 7; k++) G.ellipse(ctx, 560 + k * 130, 1000 - (k % 3) * 20, 40, 30, { fill: '#4E7A3A', lw: 3, seed: 193 + k });
      // the glass bridge
      ctx.fillStyle = 'rgba(190,235,250,0.45)'; ctx.fillRect(260, 430, 1400, 26);
      G.line(ctx, [[260, 430], [1660, 430]], { color: '#5A7A8A', lw: 5, seed: 200 });
      G.line(ctx, [[260, 456], [1660, 456]], { color: '#5A7A8A', lw: 3, seed: 201 });
      for (let x = 260; x <= 1660; x += 140) G.line(ctx, [[x, 430], [x, 340]], { color: '#5A7A8A', lw: 4, seed: 202 + x });
      G.line(ctx, [[260, 340], [1660, 340]], { color: '#5A7A8A', lw: 5, seed: 203 });
      if (i(1)) { G.line(ctx, [[1760, 450], [1760, 1000]], { color: K.RED, lw: 5, seed: 204 }); K.label(ctx, 'hundreds of m', 1720, 720, t, at('bridge', 1), { size: 44, color: K.RED, align: 'right' }); }
      // adults crawling on hands and knees
      if (i(2)) [[540, K.ADULT, 740], [820, K.KID2, 760]].forEach(([x, st, sd], k) => {
        const cx = x + Math.sin(t * 0.8 + k) * 10;
        Ch.person(ctx, { x: cx, y: 430, s: 0.42, rot: 1.25, style: st, seed: sd, eyes: 'closed', brows: 'worried', mouth: 'wavy', sweat: 1, handL: [-30, -60], handR: [30, -40] });
      });
      // you stroll, eating an apple
      if (i(3)) {
        const w = Ch.walk(t, { x0: 1000, speed: 70, t0: at('bridge', 3), stride: 140, s: 0.45 });
        K.sam(ctx, { ...w, y: 430, s: 0.45, mouth: Math.sin(t * 5) > 0.6 ? 'o' : 'smile', handR: [120, -330] });
        G.ellipse(ctx, w.x + 54, 430 - 150, 13, 12, { fill: '#D8202A', lw: 3, seed: 205 });
      }
      return;
    }
    // filmed, posted, two million views
    G.bg(ctx, '#EFE6D6');
    UI.phone(ctx, 960, 520, 820, (c, w, h) => {
      c.fillStyle = '#8FC8E8'; c.fillRect(0, 0, w, h * 0.45);
      c.fillStyle = 'rgba(190,235,250,0.7)'; c.fillRect(0, h * 0.3, w, 10);
      K.sam(c, { x: w * 0.5, y: h * 0.3, s: 0.32, mouth: 'smile' });
      G.text(c, 'kid STROLLS glass bridge 😳', 20, h * 0.52, { size: 24, fam: 'Inter', weight: 800, boil: 0 });
      Data.counter(c, { x: 20, y: h * 0.62, from: 0, to: 2000000, t, t0: ev.views, t1: ev.views + 1.6, size: 44, align: 'left', fam: 'Inter', weight: 800, suffix: ' views', color: K.RED });
      for (let k = 0; k < 4; k++) G.rrect(c, 20, h * 0.68 + k * 52, w - 40, 40, 8, { fill: '#EEEEEE', lw: 0, seed: 206 + k });
    }, t, { rot: 0.02 });
    if (t > ev.views + 1.6) K.stamp(ctx, '2,000,000', 1500, 320, t, ev.views + 1.6, { size: 90, color: K.RED, rot: 0.08 });
  }
  function black(ctx, t) {
    const i = (n) => t >= at('black', n);
    G.bg(ctx, '#2A2433');
    if (!i(1)) {
      UI.phone(ctx, 960, 540, 820, (c, w, h) => {
        c.fillStyle = '#F4F4F8'; c.fillRect(0, 0, w, h);
        UI.chat(c, w, [{ t: ev.msg, who: 'them', text: 'New message' }], t, { y0: 140, size: 26 });
      }, t, { dark: false });
      return;
    }
    // Mr. Black, in his studio of screens
    for (let k = 0; k < 6; k++) { const x = 160 + (k % 3) * 560, y = 120 + Math.floor(k / 3) * 330; G.rrect(ctx, x, y, 480, 280, 10, { fill: '#121018', lw: 5, seed: 210 + k }); ctx.fillStyle = `rgba(216,32,42,${0.25 + 0.2 * Math.sin(t * 3 + k)})`; ctx.fillRect(x + 14, y + 14, 452, 252); G.ellipse(ctx, x + 240, y + 140, 40, 40, { fill: '#FFFFFF', lw: 0, seed: 216 + k, alpha: 0.6 }); }
    K.black(ctx, { x: 960, y: 1080, s: 1.35, mouth: talk('black', t, 'smirk'), gesture: i(3) ? 'point' : 'akimbo' });
    K.stamp(ctx, 'MR. BLACK', 960, 140, t, at('black', 1) + 0.1, { size: 110, color: '#FBF7EE', stroke: '#D8202A' });
    if (i(2)) K.label(ctx, 'the biggest stunt channel online', 960, 230, t, at('black', 2) + 0.3, { size: 56, color: '#FBF7EE' });
    if (i(3)) K.stamp(ctx, '$$$', 1560, 700, t, at('black', 3) + 0.9, { size: 120, color: K.GOLD, rot: 0.1 });
  }

  // ======================= THE COST =======================
  function cost(ctx, t) {
    const i = (n) => t >= at('cost', n);
    if (!i(5)) {
      G.bg(ctx, '#F4EDE0');
      K.label(ctx, 'THE COST', 960, 150, t, SC.cost.t0, { size: 90, fam: 'Bungee' });
      if (i(1)) coasterMini(ctx, 960, 470, 0.55, t);
      if (i(2)) K.card(ctx, 200, 640, 560, 300, t, at('cost', 2), (c, w) => { G.text(c, 'BODY', w / 2, 120, { size: 80, align: 'center', fam: 'Bungee', weight: 400, color: K.RED }); G.text(c, '"DANGER!"', w / 2, 220, { size: 64, align: 'center', fam: 'Patrick Hand', weight: 400 }); }, { rot: -0.04, seed: 220 });
      if (i(3)) K.card(ctx, 1160, 640, 560, 300, t, at('cost', 3), (c, w) => { G.text(c, 'BRAIN', w / 2, 120, { size: 80, align: 'center', fam: 'Bungee', weight: 400, color: '#2E6FB5' }); G.text(c, '"we\'re safe"', w / 2, 220, { size: 64, align: 'center', fam: 'Patrick Hand', weight: 400 }); }, { rot: 0.04, seed: 221 });
      if (i(4)) { G.star(ctx, 960, 790, 90 + 20 * Math.sin(t * 12), { fill: K.GOLD, rot: t }); K.stamp(ctx, 'THE RUSH', 960, 990 - 60, t, at('cost', 4) + 0.2, { size: 70, color: K.ORANGE }); }
      return;
    }
    // you only get half: a ride with no spark
    coaster(ctx, t, { t0: at('cost', 5) }, { calm: true, bored: i(6), u: 0.95, sky0: '#C8C8C8', sky1: '#E8E8E8' });
    K.meter(ctx, 1640, 240, 110, 0, { seed: 222, label: 'THRILL' });
    if (i(6)) ['NO THRILL.', 'NO SPARK.', 'JUST... A RIDE.'].forEach((w, k) => K.label(ctx, w, 420, 200 + k * 80, t, at('cost', 6) + k * 0.9, { size: 64, fam: 'Bungee', color: '#6A6A72' }));
  }
  function coasterMini(ctx, x, y, s, t) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    const pts = []; for (let k = -500; k <= 500; k += 25) pts.push([k, -Math.cos(k / 160) * 120]);
    G.line(ctx, pts, { color: '#C0392B', lw: 14, seed: 230 });
    const cx = Math.sin(t * 1.2) * 420; G.rrect(ctx, cx - 80, -Math.cos(cx / 160) * 120 - 60, 160, 50, 14, { fill: '#2E6FB5', lw: 5, seed: 231 });
    ctx.restore();
  }
  function faces(ctx, t) {
    const i = (n) => t >= at('faces', n);
    G.bg(ctx, '#EDE6F0');
    if (!i(4)) {
      // the same frightened face, then how it looks to you
      if (i(1)) brainDraw(ctx, 960, 300, 0.5, t, 0, { off: true });
      const blank = clamp((t - ev.blank) / 0.6);
      K.card(ctx, 260, 520, 520, 460, t, at('faces', 2), (c, w) => { K.mia(c, { x: w / 2, y: 720, s: 1.2, eyes: 'wide', brows: 'worried', mouth: 'wavy', sweat: 1 }); G.text(c, 'what they feel', w / 2, 70, { size: 44, align: 'center', fam: 'Patrick Hand', weight: 400 }); }, { rot: -0.03, seed: 240 });
      if (i(3)) K.card(ctx, 1140, 520, 520, 460, t, at('faces', 3), (c, w) => {
        K.mia(c, { x: w / 2, y: 720, s: 1.2, eyes: blank > 0.5 ? 'closed' : 'wide', brows: blank > 0.5 ? 'neutral' : 'worried', mouth: blank > 0.5 ? 'flat' : 'wavy' });
        if (blank > 0) { c.save(); c.globalAlpha = blank; G.ellipse(c, w / 2, 720 - 330 * K.KID * 1.2 - 40, 62, 74, { fill: K.MIA.skin, lw: 0, seed: 242 }); c.restore(); }
        G.text(c, 'what you see', w / 2, 70, { size: 44, align: 'center', fam: 'Patrick Hand', weight: 400 });
      }, { rot: 0.03, seed: 241 });
      return;
    }
    // Mia before her exam
    K.room(ctx, '#E6EEF0', '#B9A88C', 243);
    const away = i(6);
    const tr = i(4) && !away ? U.noise1(t * 25, 3) * 5 : 0;
    K.mia(ctx, { x: 1100 + tr, y: 960, sx: away ? 1 : -1, look: away ? 1 : -1, eyes: away ? 'closed' : 'wide', brows: away ? 'determined' : 'worried', mouth: away ? 'flat' : 'wavy', sweat: away ? 0 : 1, crossArms: away });
    K.sam(ctx, { x: 760, y: 960, look: 1, mouth: i(5) && !away ? 'grin' : 'flat', gesture: i(5) && !away ? 'thumbsUp' : null });
    if (i(5) && !away) K.bubble(ctx, 'You look totally fine!', 600, 380, 740, 560, t, at('faces', 5), end('faces', 5) + 0.3, 44);
    if (away) K.card(ctx, 1380, 200, 380, 300, t, at('faces', 6) + 0.6, (c, w) => { G.text(c, '1 WEEK', w / 2, 130, { size: 70, align: 'center', fam: 'Bungee', weight: 400 }); G.text(c, 'of silence', w / 2, 210, { size: 50, align: 'center', fam: 'Patrick Hand', weight: 400 }); }, { seed: 244 });
    if (i(7)) K.dark(ctx, 0.35 * fadeIn(t, at('faces', 7), 1));
  }
  function rule2(ctx, t) {
    G.bg(ctx, '#3A3530');
    // a notebook, the rule written by hand
    K.card(ctx, 360, 160, 1200, 700, t, SC.rule2.t0, (c, w, h) => {
      for (let y = 140; y < h - 40; y += 70) G.line(c, [[40, y], [w - 40, y]], { color: 'rgba(80,120,200,0.35)', lw: 3, seed: 250 + y });
      G.line(c, [[120, 30], [120, h - 30]], { color: 'rgba(216,72,59,0.5)', lw: 3, seed: 251 });
      G.text(c, 'MY RULE', 160, 110, { size: 64, fam: 'Bungee', weight: 400, color: K.RED });
      const full = "I can't feel it.";
      const full2 = 'So I have to THINK it.';
      const tw = at('rule2', 1), dur = end('rule2', 1) - tw;
      const n1 = Math.floor(clamp((t - tw) / (dur * 0.45)) * full.length), n2 = Math.floor(clamp((t - tw - dur * 0.45) / (dur * 0.55)) * full2.length);
      if (n1 > 0) G.text(c, full.slice(0, n1), 160, 330, { size: 96, fam: 'Caveat', weight: 700 });
      if (n2 > 0) G.text(c, full2.slice(0, n2), 160, 470, { size: 96, fam: 'Caveat', weight: 700, color: '#2E6FB5' });
    }, { rot: -0.015, seed: 252, fill: '#FBF7EE' });
  }

  // ======================= LEO =======================
  function leo(ctx, t) {
    const i = (n) => t >= at('leo', n);
    K.room(ctx, '#E9DCC4', '#B98E62', 260);
    if (!i(3)) {
      G.rays(ctx, 960, 600, { n: 28, r0: 120, r1: 1400, color: 'rgba(63,168,155,0.18)', lw: 22, seed: 261, spin: t * 0.05 });
      K.leo(ctx, { x: 960, y: 980, s: 1.2, mouth: 'smile', gesture: 'wave' });
      K.stamp(ctx, 'LEO', 960, 230, t, at('leo', 0) + 0.3, { size: 150, color: K.TEAL });
      if (i(1)) G.photo ? K.card(ctx, 1320, 300, 420, 340, t, at('leo', 1), (c, w) => {
        K.sam(c, { x: 140, y: 300, s: 0.5, mouth: 'grin', eyes: 'happy' }); K.leo(c, { x: 280, y: 300, s: 0.48, mouth: 'grin', eyes: 'happy' });
        G.text(c, 'age 6', w / 2, 60, { size: 44, align: 'center', fam: 'Caveat', weight: 700 });
      }, { rot: 0.06, seed: 262 }) : null;
      return;
    }
    // scared of everything: one fear per word
    const fearT = [at('leo', 3), at('leo', 3) + (end('leo', 3) - at('leo', 3)) * 0.33, at('leo', 3) + (end('leo', 3) - at('leo', 3)) * 0.66, at('leo', 4)];
    K.leo(ctx, { x: 960, y: 980, s: 1.1, eyes: 'wide', brows: 'worried', mouth: 'wavy', sweat: 1, headX: U.noise1(t * 20, 4) * 4, handL: [-90, -260], handR: [90, -260] });
    if (t >= fearT[0] && !i(5)) Ch.dog(ctx, { x: 380, y: 900, s: 0.9, t, happy: 1, pose: 'sit', bark: Math.sin(t * 6) > 0.7 });
    if (t >= fearT[1] && !i(5)) { G.ellipse(ctx, 1500, 200, 180, 80, { fill: '#7A7A88', lw: 5, seed: 263 }); K.bolt(ctx, 1490, 260, 1.2, K.GOLD, 264); }
    if (t >= fearT[2] && !i(5)) { ctx.save(); ctx.globalAlpha = 0.5; ctx.fillStyle = '#0E0C18'; ctx.fillRect(1300, 420, 500, 400); ctx.restore(); G.text(ctx, 'the dark', 1550, 870, { size: 48, align: 'center', fam: 'Patrick Hand', weight: 400 }); }
    if (t >= fearT[3] && !i(5)) K.stamp(ctx, 'HEIGHTS', 960, 230, t, fearT[3] + 0.3, { size: 130, color: K.RED });
    if (i(5)) {
      // won't stand on a chair to change a bulb
      G.line(ctx, [[1300, 0], [1300, 180]], { color: INK, lw: 4, seed: 265 });
      G.ellipse(ctx, 1300, 210, 30, 36, { fill: '#55505A', lw: 4, seed: 266 });
      G.rrect(ctx, 1220, 760, 160, 30, 6, { fill: '#8A5A3A', lw: 5, seed: 267 });
      for (const dx of [1230, 1360]) G.line(ctx, [[dx, 790], [dx, 980]], { color: '#8A5A3A', lw: 10, seed: 268 + dx });
      K.label(ctx, 'NOPE.', 700, 300, t, at('leo', 5) + 1.4, { size: 90, fam: 'Bungee', color: K.RED });
    }
  }
  // two taps on the chest: a glowing ring on each tap
  function tapRings(ctx, x, y, t, taps) {
    for (const tt of taps) { if (t < tt) continue; const u = clamp((t - tt) / 0.7); ctx.strokeStyle = `rgba(216,72,59,${1 - u})`; ctx.lineWidth = 8; ctx.beginPath(); ctx.arc(x, y, 30 + u * 140, 0, Math.PI * 2); ctx.stroke(); }
  }
  // the hand target that taps the chest at each tap time
  const tapHand = (t, taps) => { const d = Math.min(...taps.map((tt) => Math.abs(t - tt - 0.02))); const k = 1 - clamp(d / 0.12); return [-14, -255 + 30 * (1 - k)]; };
  function deal(ctx, t) {
    const i = (n) => t >= at('deal', n);
    // a sepia memory: two six-year-olds
    K.sky(ctx, '#E8D2A8', '#D9BE90');
    ground(ctx, 880, '#B89A6A', 270);
    K.person(ctx, { x: 760, y: 920, s: 0.78, style: K.SAM, seed: 100, look: 1, mouth: 'smile' });
    const taps = ev.dealTaps;
    const tapping = i(1) && t < end('deal', 2) + 0.2 || (t > taps[0] - 0.3 && t < taps[1] + 0.4);
    K.person(ctx, { x: 1100, y: 920, s: 0.76, sx: -1, style: K.LEO, seed: 200, look: -1, mouth: talk('leo', t, 'smile'), brows: 'up', handR: tapping ? tapHand(t, [...taps, at('deal', 1) + 0.3, at('deal', 1) + 0.6]) : undefined });
    tapRings(ctx, 1100, 920 - 255 * 0.76, t, [...taps]);
    if (i(1)) K.label(ctx, '2 taps = "I\'m scared"', 960, 260, t, at('deal', 1) + 0.4, { size: 70, fam: 'Caveat' });
    if (i(3)) K.label(ctx, '...and you STOP.', 960, 360, t, at('deal', 3) + 0.6, { size: 70, fam: 'Caveat', color: K.RED });
    // an old photo edge
    ctx.save(); ctx.strokeStyle = 'rgba(90,60,30,0.6)'; ctx.lineWidth = 40; ctx.strokeRect(0, 0, W, H); ctx.restore();
  }
  function tell(ctx, t) {
    const i = (n) => t >= at('tell', n);
    K.room(ctx, '#C9D4DA', '#8A7A6A', 280);
    G.rrect(ctx, 1500, 200, 300, 260, 6, { fill: '#2A3A5A', lw: 6, seed: 281 });
    K.stars(ctx, t, 10, 282, 0.6);
    const goes = i(4);
    const w = goes ? Ch.walk(t, { x0: 700, speed: -220, t0: at('tell', 4) + 0.2, stride: 240 }) : null;
    K.sam(ctx, goes ? { ...w, x: Math.min(700, w.x), pose: 'walk', sx: -1, y: 960, mouth: 'flat' } : { x: 700, y: 960, look: 1, mouth: 'flat' });
    const taps = ev.tellTaps;
    K.leo(ctx, { x: 1150, y: 960, sx: -1, look: -1, eyes: 'normal', brows: 'worried', mouth: talk('leo', t, 'flat'), handR: t > taps[0] - 0.3 && t < taps[1] + 0.4 ? tapHand(t, taps) : undefined });
    tapRings(ctx, 1150, 960 - 255 * K.KID, t, taps);
    if (i(1) && !i(2)) K.label(ctx, "you can't read his face", 960, 200, t, at('tell', 1), { size: 60 });
  }

  // ======================= THE CRANE =======================
  const BEAM_Y = 430, MAST_X = 560, BEAM_END = 1820;
  function docks(ctx, t, o = {}) {
    K.sky(ctx, o.top || '#3A3560', o.bottom || '#E88A5A');
    K.stars(ctx, t, 40, 290, 0.5);
    for (let k = 0; k < 6; k++) G.rrect(ctx, 900 + k * 170, 760 - (k % 3) * 60, 150, 200, 4, { fill: ['#C0392B', '#2E6FB5', '#3FA89B', '#E0A33E'][k % 4], lw: 5, seed: 291 + k, hatch: { color: 'rgba(0,0,0,0.2)', gap: 14, angle: 1.57 } });
    K.waves(ctx, 930, t);
    K.crane(ctx, MAST_X, 960, BEAM_Y, BEAM_END);
    K.ladder(ctx, MAST_X + 80, 960, BEAM_Y + 90);
  }
  // camera drones around the beam
  const drones = (ctx, t) => [[900, 200], [1500, 180], [1300, 480]].forEach(([x, y], k) => K.cameraBot(ctx, x, y, 0.8, t, 300 + k * 7));
  function crane(ctx, t) {
    const i = (n) => t >= at('crane', n);
    docks(ctx, t);
    if (i(1)) { G.line(ctx, [[1860, BEAM_Y], [1860, 930]], { color: '#FBF7EE', lw: 4, seed: 310 }); K.label(ctx, '40 m', 1740, 700, t, at('crane', 1), { size: 54, color: '#FBF7EE' }); }
    if (i(2) && !i(4)) K.label(ctx, '30 cm wide', 1200, BEAM_Y - 70, t, at('crane', 2), { size: 54, color: '#FBF7EE' });
    if (i(3)) drones(ctx, t);
    // Sam and Mr. Black on the beam
    const out = i(9) ? ease.inOutQuad(clamp((t - at('crane', 9)) / 2)) : 0;
    const sx = lerp(760, 1100, out);
    const wk = out > 0 && out < 1;
    K.sam(ctx, { x: sx, y: BEAM_Y - 34, s: 0.5, pose: wk ? 'walk' : 'stand', walk: (t - at('crane', 9)) * 2.4, mouth: 'flat', handL: [-200, -230], handR: [200, -230] });
    K.black(ctx, { x: 640, y: BEAM_Y - 34, s: 0.62, mouth: talk('black', t, 'smirk'), gesture: i(5) ? 'phone' : null });
    // the safety line: clipped, then unclipped on the tug
    const clipped = i(4) && t < ev.tug;
    if (clipped) G.line(ctx, [[640 + 30, BEAM_Y - 140], [sx - 4, BEAM_Y - 34 - 230 * 0.5 * K.KID * 2 + 120]], { color: K.GOLD, lw: 5, seed: 311 });
    if (t >= ev.tug) { const fall = ease.outBounce(clamp((t - ev.tug) / 0.6)); G.line(ctx, [[670, BEAM_Y - 140], [700, BEAM_Y - 140 + fall * 260]], { color: K.GOLD, lw: 5, seed: 312 }); G.ellipse(ctx, 700, BEAM_Y - 140 + fall * 260, 10, 14, { fill: '#9A9AA2', lw: 3, seed: 313 }); }
    if (i(5)) K.live(ctx, 80, 80, t, { viewers: `👁 ${Data.number(Math.round(Data.count(t, ev.live, ev.live + 20, 1200, 980000)))}` });
    K.flash(ctx, t, ev.tug, 0.12);
    if (t > ev.tug) K.stamp(ctx, '*TUG*', 760, 160, t, ev.tug, { size: 90, color: K.GOLD });
  }
  function climb(ctx, t) {
    const i = (n) => t >= at('climb', n);
    // closer on the mast and the ladder
    ctx.save(); ctx.translate(960, 540); ctx.scale(1.6, 1.6); ctx.translate(-760, -500);
    docks(ctx, t, { top: '#2A2850', bottom: '#C8705A' });
    // wind streaks
    for (let k = 0; k < 14; k++) { const y = 200 + (k * 61) % 700, x = ((t * 900 + k * 300) % 2600) - 300; G.line(ctx, [[x, y], [x + 140, y - 6]], { color: 'rgba(255,255,255,0.4)', lw: 3, seed: 320 + k }); }
    const shake = i(0) && !i(1) ? Math.sin(t * 60) * 4 : 0;
    // Leo climbs: height 0..30 m over the counted line, then freezes
    const h = clamp((t - at('climb', 1)) / (end('climb', 4) - at('climb', 1)));
    const ly = lerp(960, BEAM_Y + 260, ease.inOutQuad(h)) + shake;
    const climbing = h > 0 && h < 1;
    const ph = (t - at('climb', 1)) * 6;
    const slip = i(8) ? U.noise1(t * 30, 9) * 8 : 0;
    if (i(1)) K.leo(ctx, { x: MAST_X + 80, y: ly, s: 0.55, look: 0, lookY: -0.6, eyes: i(5) ? 'wide' : 'normal', brows: 'worried', mouth: talk('leo', t, i(5) ? 'wavy' : 'flat'), sweat: i(5) ? 1 : 0, handL: [-60 + slip, -330 + (climbing ? Math.sin(ph) * 30 : 0)], handR: [60 - slip, -330 + (climbing ? Math.cos(ph) * 30 : 0)], knee: climbing ? [Math.max(0, Math.sin(ph)) * 0.6, Math.max(0, -Math.sin(ph)) * 0.6] : [0, 0] });
    // Sam far out on the beam
    K.sam(ctx, { x: 1100, y: BEAM_Y - 34, s: 0.5, look: -1, mouth: 'flat', handL: [-200, -230], handR: [200, -230] });
    ctx.restore();
    ev.climbMarks.forEach((tm, k) => { if (t >= tm && !i(5)) K.stamp(ctx, `${(k + 1) * 10} m`, 380, 260 + k * 150, t, tm, { size: 90, color: '#FBF7EE', stroke: INK }); });
    if (i(7) && !i(8)) K.card(ctx, 1300, 120, 520, 260, t, at('climb', 7) + 0.3, (c, w) => { G.text(c, '40 m fall', w / 2, 100, { size: 60, align: 'center', fam: 'Bungee', weight: 400 }); G.text(c, '< 3 seconds', w / 2, 190, { size: 60, align: 'center', fam: 'Patrick Hand', weight: 400, color: K.RED }); }, { seed: 330 });
    if (i(8)) K.vignette(ctx, 0.75);
  }
  function choice(ctx, t) {
    const i = (n) => t >= at('choice', n);
    if (!i(3)) {
      // Leo's face, close: terrified... and what Sam sees
      K.sky(ctx, '#2A2850', '#5A3A6A');
      const blank = i(2) ? clamp((t - at('choice', 2) - 0.6) / 0.8) : 0;
      ctx.save(); ctx.translate(960, 540); ctx.scale(2.6, 2.6); ctx.translate(-960, -460);
      K.leo(ctx, { x: 960, y: 760, eyes: blank > 0.5 ? 'closed' : 'wide', brows: blank > 0.5 ? 'neutral' : 'worried', mouth: blank > 0.5 ? 'flat' : 'wavy', sweat: 1 - blank, headX: U.noise1(t * 20, 5) * 3 * (1 - blank) });
      ctx.restore();
      if (blank > 0) { ctx.save(); ctx.globalAlpha = blank; ctx.fillStyle = 'rgba(40,36,60,0.55)'; ctx.fillRect(0, 0, W, H); ctx.restore(); K.label(ctx, '...just a face.', 960, 930, t, at('choice', 2) + 1.2, { size: 70, color: '#FBF7EE' }); }
      return;
    }
    // the choice: ahead the money, behind your friend
    K.sky(ctx, '#2A2850', '#C8705A');
    const split = W / 2;
    ctx.save(); ctx.fillStyle = 'rgba(216,32,42,0.18)'; ctx.fillRect(split, 0, W - split, H); ctx.fillStyle = 'rgba(63,168,155,0.2)'; ctx.fillRect(0, 0, split, H); ctx.restore();
    G.rrect(ctx, -40, 640, W + 80, 40, 4, { fill: '#E8A43A', lw: 5, seed: 340 });
    K.sam(ctx, { x: split, y: 640, s: 0.9, look: i(5) ? -1 : 1, mouth: 'flat', handL: [-200, -230], handR: [200, -230] });
    if (i(3) && !i(4)) { K.card(ctx, 1380, 120, 440, 220, t, at('choice', 3), (c, w) => { K.black(c, { x: 110, y: 330, s: 0.5, mouth: talk('black', t, 'smirk') }); G.text(c, 'in your ear', 300, 130, { size: 40, align: 'center', fam: 'Patrick Hand', weight: 400 }); }, { seed: 341, rot: 0.03 }); }
    if (i(4)) { K.stamp(ctx, 'VIEWS', 1500, 300, t, at('choice', 4) + 1.2, { size: 100, color: K.RED }); K.stamp(ctx, '$$$', 1500, 460, t, at('choice', 4) + 2.2, { size: 100, color: K.GOLD }); K.live(ctx, 1420, 520, t, { viewers: '1,000,000' }); }
    if (i(5)) { K.leo(ctx, { x: 360, y: 900, s: 0.8, lookY: -1, eyes: 'wide', brows: 'worried', mouth: 'wavy', sweat: 1, handL: [-60, -330], handR: [60, -330] }); K.ladder(ctx, 360, 1100, 640); K.stamp(ctx, 'LEO', 420, 300, t, at('choice', 5) + 0.7, { size: 100, color: K.TEAL }); }
    if (i(6)) K.vignette(ctx, 0.5 + 0.2 * fadeIn(t, at('choice', 6), 1));
  }
  function taps(ctx, t) {
    // silence. Leo's hand, his chest, two taps
    G.bg(ctx, '#1A1726');
    const lift = ease.outCubic(clamp((t - at('taps', 0)) / 1.4));
    ctx.save(); ctx.translate(960, 540); ctx.scale(2.2, 2.2); ctx.translate(-960, -560);
    const hand = t < ev.finalTaps[0] - 0.4 ? [lerp(110, 20, lift), lerp(-120, -230, lift)] : tapHand(t, ev.finalTaps);
    K.leo(ctx, { x: 960, y: 900, eyes: 'wide', brows: 'worried', mouth: 'wavy', sweat: 1, handR: [hand[0], hand[1] + U.noise1(t * 30, 6) * 4] });
    ctx.restore();
    // each tap: a ring and a heartbeat glow
    for (const tt of ev.finalTaps) { if (t < tt) continue; const u = clamp((t - tt) / 0.9); ctx.strokeStyle = `rgba(255,90,70,${1 - u})`; ctx.lineWidth = 14; ctx.beginPath(); ctx.arc(935, 540 + (900 - 255 * K.KID - 560) * 2.2, 60 + u * 420, 0, Math.PI * 2); ctx.stroke(); }
    K.flash(ctx, t, ev.finalTaps[0], 0.14, '255,90,70');
    K.flash(ctx, t, ev.finalTaps[1], 0.14, '255,90,70');
    ev.finalTaps.forEach((tt, k) => K.stamp(ctx, 'TAP', 420 + k * 1080, 300, t, tt, { size: 110, color: K.RED }));
  }
  function turn(ctx, t) {
    const i = (n) => t >= at('turn', n);
    if (!i(6)) {
      K.sky(ctx, '#2A2850', '#C8705A');
      G.rrect(ctx, -40, 640, W + 80, 40, 4, { fill: '#E8A43A', lw: 5, seed: 350 });
      // turn around, then step, breathe, step back to the ladder
      const turned = t >= ev.turn;
      const nStep = ev.steps.filter((s) => t >= s).length;
      const x = lerp(1300, 700, nStep / 3) - (i(4) ? 0 : 0);
      const crouch = i(4);
      K.sam(ctx, { x, y: 640, s: 0.9, sx: turned ? -1 : 1, mouth: talk('sam', t, 'flat'), eyes: 'normal', brows: 'determined', legBend: crouch ? 0.9 : 0, sy: crouch ? 0.82 : 1, handL: [-200, -230], handR: [200, -230] });
      K.ladder(ctx, 360, 1100, 640);
      K.leo(ctx, { x: 360, y: 980, s: 0.8, lookY: -1, eyes: 'wide', brows: 'worried', mouth: 'wavy', sweat: 1, handL: [-60, -330], handR: [60, -330] });
      if (i(2) && !i(4)) K.card(ctx, 1200, 120, 620, 220, t, at('turn', 2), (c, w) => { G.text(c, "can't feel it?", w / 2, 90, { size: 56, align: 'center', fam: 'Caveat', weight: 700 }); G.text(c, 'THINK it.', w / 2, 170, { size: 64, align: 'center', fam: 'Bungee', weight: 400, color: '#2E6FB5' }); }, { seed: 351 });
      ['STEP.', 'BREATHE.', 'STEP.'].forEach((w, k) => { if (t >= ev.steps[k] && !i(4)) K.stamp(ctx, w, 820 + k * 380, 860, t, ev.steps[k], { size: 80, color: '#FBF7EE', stroke: INK }); });
      return;
    }
    // three points of contact
    G.bg(ctx, '#F4EDE0');
    K.label(ctx, '3 POINTS OF CONTACT', 960, 150, t, at('turn', 6), { size: 84, fam: 'Bungee', color: K.TEAL });
    K.ladder(ctx, 960, 1080, 220, { w: 220, rung: 110 });
    const two = i(7) ? (t - at('turn', 7)) % 3 > 1.5 : false;
    const hands = [[-110, -520], [110, two ? -440 : -560]];
    K.leo(ctx, { x: 960, y: 900, s: 1, lookY: -1, eyes: 'normal', brows: 'determined', mouth: 'flat', handL: hands[0], handR: hands[1], knee: [two ? 0 : 0.5, 0] });
    const pts = [[960 - 110, 900 - 520], [960 + 110, 900 - (two ? 440 : 560)], [960 - 40, 900 - 20]];
    if (i(6)) pts.forEach(([x, y], k) => { if (t < at('turn', 6) + 0.4 * k) return; const p = 1 + 0.15 * Math.sin(t * 6 + k); ctx.strokeStyle = K.TEAL; ctx.lineWidth = 8; ctx.beginPath(); ctx.arc(x, y, 50 * p, 0, Math.PI * 2); ctx.stroke(); G.text(ctx, String(k + 1), x + 70, y + 20, { size: 60, fam: 'Bungee', weight: 400, color: K.TEAL }); });
    if (i(8)) K.stamp(ctx, 'ALWAYS THREE', 1500, 600, t, at('turn', 8) + 0.1, { size: 80, color: K.ORANGE, rot: 0.06 });
    if (i(9)) K.label(ctx, 'the oldest rule in climbing', 1500, 720, t, at('turn', 9) + 0.3, { size: 52 });
  }
  function down(ctx, t) {
    const i = (n) => t >= at('down', n);
    // night, the ladder, rung by rung
    K.sky(ctx, '#14122A', '#3A3560');
    K.stars(ctx, t, 120, 360, 1);
    G.ellipse(ctx, 1650, 180, 80, 80, { fill: '#F4EDCF', lw: 4, seed: 361 });
    K.crane(ctx, 760, 1200, 320, 1900);
    K.ladder(ctx, 840, 1200, 410);
    const u = clamp((t - at('down', 1)) / (SC.down.t1 - at('down', 1) - 0.3));
    const rung = Math.floor(u * 10);
    const ly = lerp(700, 1150, rung / 10 + ease.inOutQuad((u * 10) % 1) / 10);
    K.leo(ctx, { x: 840, y: ly, s: 0.6, lookY: -1, eyes: i(2) ? 'normal' : 'wide', brows: i(2) ? 'neutral' : 'worried', mouth: i(2) ? 'flat' : 'wavy', handL: [-60, -330], handR: [60, -330] });
    K.sam(ctx, { x: 960, y: 290, s: 0.55, sx: -1, legBend: 0.9, sy: 0.85, mouth: talk('narrator', t, 'smile'), look: -1, lookY: 1 });
    // the calm voice: soft rings travelling down
    for (let k = 0; k < 4; k++) { const r = ((t * 120 + k * 90) % 360); ctx.strokeStyle = `rgba(159,211,240,${0.6 * (1 - r / 360)})`; ctx.lineWidth = 5; ctx.beginPath(); ctx.arc(940, 260, 40 + r, 0.6, 2.4); ctx.stroke(); }
    if (i(2)) K.meter(ctx, 1500, 560, 110, lerp(0.95, 0.2, fadeIn(t, at('down', 2), 3)), { seed: 362, label: 'LEO' });
    if (i(3)) K.label(ctx, 'the only steady thing in the sky', 1450, 820, t, at('down', 3) + 0.5, { size: 50, color: '#FBF7EE' });
  }
  function truth(ctx, t) {
    const i = (n) => t >= at('truth', n);
    if (!i(7)) {
      docks(ctx, t, { top: '#2A2850', bottom: '#8A5A6A' });
      ctx.save(); ctx.fillStyle = 'rgba(0,0,0,0.25)'; ctx.fillRect(0, 0, W, H); ctx.restore();
      Ch.person(ctx, { x: 820, y: 960, pose: 'floor', s: 0.8, style: K.LEO, seed: 200, eyes: 'closed', mouth: 'wavy', brows: 'worried', sweat: 1 });
      K.sam(ctx, { x: 1120, y: 960, s: 0.9, sx: -1, mouth: talk('sam', t, 'flat'), gesture: i(1) ? 'phone' : null, brows: 'determined' });
      if (i(2)) K.live(ctx, 1220, 420, t);
      if (i(3)) { G.line(ctx, [[1380, 960], [1420, 800], [1460, 820]], { color: K.GOLD, lw: 6, seed: 370 }); G.ellipse(ctx, 1462, 822, 12, 16, { fill: '#9A9AA2', lw: 3, seed: 371 }); }
      if (i(4)) K.stamp(ctx, 'ON PURPOSE.', 1400, 260, t, at('truth', 4) + 0.6, { size: 90, color: K.RED });
      if (i(1)) K.black(ctx, { x: 1660, y: 980, s: 0.95, sx: -1, mouth: i(4) ? 'o' : 'flat', eyes: i(4) ? 'wide' : 'normal', sweat: i(4) ? 1 : 0, brows: i(4) ? 'worried' : 'neutral' });
      if (i(5)) K.label(ctx, 'no shouting. no shoving. just the truth.', 700, 200, t, at('truth', 5) + 0.5, { size: 52, color: '#FBF7EE' });
      return;
    }
    // channel gone
    G.bg(ctx, '#EFE6D6');
    UI.card(ctx, 360, 180, 1200, 680, 30, { fill: '#FFFFFF', stroke: '#DDDDDD' });
    G.ellipse(ctx, 520, 340, 90, 90, { fill: '#1C1C22', lw: 4, seed: 372 });
    UI.text(ctx, 'MR. BLACK STUNTS', 650, 330, { size: 54, weight: 800 });
    UI.text(ctx, '12.4M subscribers', 650, 390, { size: 34, color: '#777' });
    for (let k = 0; k < 4; k++) G.rrect(ctx, 420 + k * 280, 500, 250, 150, 10, { fill: '#C9C2B4', lw: 3, seed: 373 + k });
    K.stamp(ctx, 'CHANNEL GONE', 960, 620, t, ev.gone, { size: 120, color: K.RED, rot: -0.12 });
  }
  function psa(ctx, t) {
    G.bg(ctx, '#2E6FB5');
    K.card(ctx, 260, 140, 1400, 760, t, SC.psa.t0, (c, w, h) => {
      G.text(c, 'REMEMBER', w / 2, 140, { size: 90, align: 'center', fam: 'Bungee', weight: 400, color: '#2E6FB5' });
      G.text(c, 'No video is worth', w / 2, 300, { size: 80, align: 'center', fam: 'Patrick Hand', weight: 400 });
      G.text(c, 'a hospital bed.', w / 2, 400, { size: 80, align: 'center', fam: 'Patrick Hand', weight: 400 });
      if (t > at('psa', 1)) { G.text(c, 'Never drop your safety gear', w / 2, 560, { size: 62, align: 'center', fam: 'Patrick Hand', weight: 400, color: K.RED }); G.text(c, 'for views.', w / 2, 640, { size: 62, align: 'center', fam: 'Patrick Hand', weight: 400, color: K.RED }); }
    }, { seed: 380 });
  }
  function comments(ctx, t) {
    const i = (n) => t >= at('comments', n);
    G.bg(ctx, '#F4EDE0');
    const names = ['LEO 🙌', 'protect LEO', 'Leo is the real hero', 'LEO!!!', 'that kid Leo though', 'Leo climbed 30m TERRIFIED', 'brave = Leo', 'LEO LEO LEO'];
    const scroll = since(t, SC.comments.t0) * 70;
    UI.phone(ctx, 560, 540, 860, (c, w, h) => {
      c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, w, h);
      UI.text(c, 'Comments', 24, 90, { size: 30, weight: 800 });
      for (let k = 0; k < 14; k++) {
        const y = 140 + k * 92 - scroll % 92 - Math.floor(scroll / 92) * 0;
        if (y < 110 || y > h - 40) continue;
        G.ellipse(c, 44, y + 24, 22, 22, { fill: ['#E0703E', '#3FA89B', '#B79CFF', '#F2B84B'][k % 4], lw: 0, seed: 390 + k });
        UI.text(c, `@user${(k * 37) % 997}`, 80, y + 16, { size: 18, color: '#888' });
        UI.text(c, names[(k + Math.floor(scroll / 92)) % names.length], 80, y + 46, { size: 24, weight: 800 });
      }
    }, t);
    if (i(1)) K.stamp(ctx, 'LEO', 1360, 300, t, at('comments', 1), { size: 200, color: K.TEAL });
    if (i(3)) K.card(ctx, 1000, 520, 760, 380, t, at('comments', 3), (c, w) => {
      G.text(c, 'brave (adj.)', 40, 90, { size: 60, fam: 'Bungee', weight: 400, color: K.ORANGE });
      G.text(c, 'not feeling nothing...', 40, 190, { size: 54, fam: 'Caveat', weight: 700 });
      if (t > at('comments', 4) + 1.4) G.text(c, 'feeling EVERYTHING,', 40, 260, { size: 54, fam: 'Caveat', weight: 700, color: K.RED });
      if (t > at('comments', 4) + 2.6) G.text(c, 'and climbing anyway.', 40, 330, { size: 54, fam: 'Caveat', weight: 700 });
    }, { seed: 391, rot: 0.02 });
  }
  function hug(ctx, t) {
    const i = (n) => t >= at('hug', n);
    K.sky(ctx, '#F2A65A', '#F7D9A8');
    G.ellipse(ctx, 960, 760, 260, 260, { fill: '#F8C36A', lw: 0, seed: 400, alpha: 0.8 });
    ground(ctx, 880, '#7A9A5A', 401);
    const hugging = i(7);
    const close = hugging ? ease.inOutQuad(clamp((t - at('hug', 7)) / 0.8)) : 0;
    K.sam(ctx, { x: lerp(800, 900, close), y: 960, s: 1, sx: 1, look: 1, gesture: i(1) && !i(2) ? 'shrug' : null, mouth: talk('sam', t, hugging ? 'smile' : 'flat'), eyes: hugging ? 'closed' : 'normal', handR: hugging ? [200, -240] : undefined, handL: hugging ? [120, -230] : undefined });
    K.leo(ctx, { x: lerp(1160, 1030, close), y: 960, s: 1, sx: -1, look: -1, mouth: talk('leo', t, i(3) ? 'grin' : 'smile'), eyes: i(3) ? 'happy' : 'normal', handR: hugging ? [220, -240] : undefined, handL: hugging ? [120, -230] : undefined });
    // the heart jumps: the meter moves for the first time in years
    const jumped = t >= ev.jump;
    K.meter(ctx, 1600, 260, 110, jumped ? 0.18 + 0.12 * Math.exp(-(t - ev.jump) * 3) * Math.sin((t - ev.jump) * 30) : 0, { seed: 402, label: 'SAM' });
    if (jumped) { G.heart(ctx, 890, 520 - ease.outBack(clamp((t - ev.jump) / 0.4)) * 80, 1.2 * (1 + 0.3 * pulse(t, ev.jump, 6))); K.flash(ctx, t, ev.jump, 0.15, '255,200,200'); }
  }
  function envelope(ctx, t) {
    const i = (n) => t >= at('envelope', n);
    if (!i(3)) {
      // a dark hallway door; an envelope slides in under it
      G.bg(ctx, '#14122A');
      G.rrect(ctx, 600, 80, 720, 900, 8, { fill: '#3A2E2A', lw: 6, seed: 410, hatch: { color: 'rgba(0,0,0,0.25)', gap: 18, angle: 1.57 } });
      G.ellipse(ctx, 1240, 560, 22, 22, { fill: '#C9A23A', lw: 4, seed: 411 });
      ctx.save(); ctx.fillStyle = 'rgba(255,220,150,0.5)'; ctx.fillRect(600, 975, 720, 10); ctx.restore();
      ground(ctx, 980, '#2A2230', 412);
      const sl = ease.outCubic(clamp((t - ev.envelope) / 0.5));
      if (t >= ev.envelope) { G.rrect(ctx, lerp(820, 860, sl), lerp(985, 1000, sl), 280, 60, 4, { fill: '#F4EDE0', lw: 4, seed: 413 }); }
      if (i(1)) { K.label(ctx, 'no stamp.', 400, 400, t, at('envelope', 1), { size: 60, color: '#FBF7EE' }); K.label(ctx, 'no name.', 1520, 400, t, at('envelope', 1) + 0.8, { size: 60, color: '#FBF7EE' }); }
      return;
    }
    // the note
    G.bg(ctx, '#14122A');
    K.spot(ctx, 960, 500, 900, 0.25);
    K.card(ctx, 360, 260, 1200, 520, t, ev.note, (c, w, h) => {
      const msg1 = 'We know what you can\'t feel.', msg2 = 'We need you.';
      const n = Math.floor((t - ev.note - 0.3) * 18);
      G.text(c, msg1.slice(0, Math.max(0, n)), w / 2, 230, { size: 70, align: 'center', fam: 'Menlo, Consolas, monospace', weight: 700, boil: 0 });
      G.text(c, msg2.slice(0, Math.max(0, n - msg1.length - 4)), w / 2, 350, { size: 80, align: 'center', fam: 'Menlo, Consolas, monospace', weight: 700, color: K.RED, boil: 0 });
    }, { seed: 414, tape: false, fill: '#F4EDE0' });
  }
  function outro(ctx, t) {
    const i = (n) => t >= at('outro', n);
    G.bg(ctx, '#1E1B2E');
    G.rays(ctx, 960, 560, { n: 36, r0: 140, r1: 1600, color: 'rgba(242,184,75,0.14)', lw: 22, seed: 420, spin: t * 0.08 });
    K.sam(ctx, { x: 560, y: 1000, s: 1.05, mouth: 'smirk', crossArms: true });
    K.leo(ctx, { x: 1360, y: 1000, s: 1.05, sx: -1, mouth: 'grin', eyes: 'happy', gesture: t > ev.endCard ? 'thumbsUp' : 'wave' });
    G.text(ctx, 'What would YOU do', 960, 170, { size: 90, align: 'center', fam: 'Bungee', weight: 400, color: '#FBF7EE', stroke: INK, strokeW: 8 });
    G.text(ctx, 'with ZERO FEAR?', 960, 280, { size: 110, align: 'center', fam: 'Bungee', weight: 400, color: K.ORANGE, stroke: INK, strokeW: 10 });
    if (i(1)) K.card(ctx, 700, 360, 520, 200, t, at('outro', 1), (c, w) => { G.text(c, '💬 the first scary thing', w / 2, 90, { size: 44, align: 'center', fam: 'Patrick Hand', weight: 400 }); G.text(c, "you'd try?", w / 2, 150, { size: 44, align: 'center', fam: 'Patrick Hand', weight: 400 }); }, { seed: 421 });
    if (i(2)) {
      const tap = ev.endCard;
      UI.button(ctx, 800, 690, 260, 90, '👍 LIKE', t, { tTap: tap - 0.5, bg: '#3A3844', doneBg: '#2E6FB5' });
      UI.button(ctx, 1120, 690, 320, 90, 'SUBSCRIBE', t, { tTap: tap, bg: '#D8202A', doneBg: '#5A5560' });
      if (t >= tap) K.stamp(ctx, 'PART TWO', 960, 880, t, tap, { size: 100, color: K.GOLD });
      if (t > at('outro', 2) + 2) tapRings(ctx, 1360, 1000 - 220 * 1.05 / 0.82 * K.KID, t, [at('outro', 2) + 2.6, at('outro', 2) + 2.95]);
    }
  }

  const SCENE_FN = { spider, haunted, coaster: (ctx, t, s) => coaster(ctx, t, s), brain, sm, rule, title, speech, exams, space, zoo, skate, bridge, black, cost, faces, rule2, leo, deal, tell, crane, climb, choice, taps, turn, down, truth, psa, comments, hug, envelope, outro };
  const IN = { haunted: 'whip', coaster: 'whip', brain: 'paper', title: { type: 'iris', color: '#1E1B2E' }, speech: 'paper', exams: 'push', space: 'push', zoo: 'wipe', skate: 'wipe', bridge: 'whip', black: 'dip', cost: 'paper', faces: 'fade', rule2: 'fade', leo: 'paper', deal: { type: 'dip', color: '#E8D2A8' }, tell: 'fade', crane: { type: 'dip', color: '#000000' }, climb: 'cut', choice: 'cut', taps: 'cut', turn: 'cut', down: 'fade', truth: 'fade', psa: 'push', comments: 'push', hug: 'paper', envelope: { type: 'dip', color: '#000000', dur: 1 }, outro: 'iris' };
  const CAM = {
    spider: Shots.push(1, 1.06), haunted: (s) => Shots.combine(Shots.push(1, 1.05), Shots.shake(16, ev.monster, 5))(s), coaster: Shots.push(1, 1.08), brain: Shots.push(1, 1.04),
    rule: Shots.push(1, 1.04), title: Shots.push(1.05, 1), speech: Shots.push(1, 1.05), space: Shots.handheld(4), zoo: Shots.push(1, 1.05),
    skate: (s) => Shots.combine(Shots.handheld(4), Shots.shake(26, ev.crack, 6))(s), bridge: Shots.push(1, 1.06), black: Shots.push(1, 1.06), faces: Shots.push(1, 1.04),
    leo: Shots.push(1, 1.05), deal: Shots.push(1.02, 1.08), tell: Shots.push(1, 1.05), crane: Shots.push(1, 1.03), climb: (s) => Shots.combine(Shots.handheld(8), Shots.shake(14, ev.rattle, 4))(s),
    choice: Shots.handheld(6), taps: Shots.push(1, 1.1), turn: Shots.handheld(3), down: Shots.push(1, 1.05), truth: Shots.push(1, 1.04), comments: Shots.push(1, 1.03),
    hug: (s) => Shots.combine(Shots.push(1, 1.06), Shots.shake(10, ev.jump, 6))(s), envelope: Shots.push(1, 1.1), outro: Shots.push(1, 1.03),
  };
  const film = Shots.film(S.ORDER.map((id) => ({ at: SC[id].t0, draw: (ctx, t, s) => SCENE_FN[id](ctx, t, s), in: IN[id] || 'cut', cam: CAM[id] })), { end: S.DURATION });

  Studio.film({
    fadeOut: 1.5,
    async init() { VO = await Studio.loadJSON('out/voice.json'); SUBS = Subs.fromVoice(VO, { maxWords: 7, hold: 0.25 }); },
    draw(ctx, t) {
      film(ctx, t);
      Subs.draw(ctx, t, SUBS, { style: 'box', size: 46 });
    },
  });
})();
