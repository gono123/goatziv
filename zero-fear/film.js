// THE FILM: 27 scenes, one per block of the script, each a pure function of t. Scene and line times come
// from score.js (the measured voiceover); the heart monitor's spikes and Leo's tap ripples are the same
// events the song beeps and knocks on.
(function () {
  const U = globalThis.U, G = globalThis.G, Ch = globalThis.Ch, UI = globalThis.UI, Data = globalThis.Data, Subs = globalThis.Subs, S = globalThis.SCORE, Studio = globalThis.Studio, L = globalThis.FL;
  const { clamp, ease, lerp } = U;
  const W = G.W, H = G.H, C = L.CAST, INK = L.INK;
  let VO = null, SUBS = [];
  const talk = (t, who, rest = 'smile') => { if (!VO) return rest; const mo = Subs.mouth(VO, t, who); return mo.talking ? mo : rest; };
  const A = (scene, txt) => S.at(scene, txt);
  const person = (ctx, o) => Ch.person(ctx, o);
  const blinkAt = (t, seed) => ((t + seed * 1.7) % 3.7 < 0.12 ? 1 : 0);
  const head = (x, y, s) => [x, y - 404 * s]; // head centre of a standing person
  const chest = (x, y, s) => [x, y - 250 * s];
  const room = (ctx, wall, floor, fy = 820) => { G.bg(ctx, wall); G.poly(ctx, [[-20, fy], [W + 20, fy], [W + 20, H + 20], [-20, H + 20]], { fill: floor, lw: 4, seed: 7, hatch: { color: 'rgba(0,0,0,0.12)', gap: 14 } }); };
  const mon = (ctx, t, o = {}) => L.monitor(ctx, t, o.x ?? 1450, o.y ?? 70, o.w ?? 400, o.h ?? 190, o);

  // ================= the opening =================
  function spider(ctx, t, s) {
    room(ctx, '#E9E1D3', '#C9A87C', 860);
    const u = L.u(t, s.t0 + 0.4, s.t1);
    person(ctx, { x: 820, y: 1080, s: 1.5, pose: 'stand', style: C.sam, handR: [210, -300], look: 0.7, lookY: 0.3, eyes: blinkAt(t, 1) ? 'closed' : 'normal', mouth: t > A('spider', 'Not even') ? 'smirk' : 'smile', seed: 300 });
    // the spider drops on its thread, then walks along the arm
    const hx = 820 + 210 * 1.5, hy = 1080 - 300 * 1.5;
    const dropT = clamp((t - s.t0) / 1.0);
    const sx = t < A('spider', 'let it walk') ? hx : lerp(hx, 900, L.u(t, A('spider', 'let it walk'), s.t1)), sy = t < A('spider', 'let it walk') ? lerp(-60, hy - 26, ease.outCubic(dropT)) : lerp(hy - 26, 1080 - 330 * 1.5, L.u(t, A('spider', 'let it walk'), s.t1));
    if (t < A('spider', 'let it walk')) G.line(ctx, [[hx, -20], [sx, sy - 30]], { lw: 1.5, color: 'rgba(42,35,32,0.6)', amp: 0 });
    L.spider(ctx, sx, sy, 1.3, t);
    mon(ctx, t);
    if (t > A('spider', 'Scared')) L.label(ctx, 'scared? 0%', 400, 260, { size: 64, color: '#3D7A74', rot: -0.05 });
  }
  function haunted(ctx, t, s) {
    room(ctx, '#2A2340', '#1E1A2C', 860);
    const tLeap = A('haunted', 'monster leaps'), tTap = A('haunted', 'tap him');
    const leap = ease.outBack(L.u(t, tLeap, tLeap + 0.5));
    person(ctx, { x: lerp(1700, 1260, leap), y: 1040, s: 1.05, pose: 'stand', style: C.monster, handL: [-170, -470], handR: [170, -470], mouth: t > tTap + 0.6 ? 'o' : 'open', eyes: t > tTap + 0.6 ? 'wide' : 'normal', brows: t > tTap + 0.6 ? 'up' : 'determined', seed: 700 });
    const scared = t > A('haunted', 'shrieks');
    ['kid1', 'kid2'].forEach((k, i) => person(ctx, { x: 260 + i * 230, y: 1050, s: 0.9, pose: 'stand', style: C[k], eyes: scared ? 'wide' : 'normal', brows: scared ? 'worried' : 'neutral', mouth: scared ? 'open' : 'flat', handL: scared ? [-60, -420] : null, handR: scared ? [60, -420] : null, sweat: scared ? 1 : 0, seed: 710 + i * 20 }));
    person(ctx, { x: 960, y: 1050, s: 1.0, pose: 'stand', style: C.sam, handR: t > tTap ? [230, -340] : null, look: 1, mouth: talk(t, 'sam', 'smile'), seed: 300 });
    L.light(ctx, 1260, 500, '#FFFFFF', '#3A3570', 'multiply', 0.5);
    mon(ctx, t, { others: true });
  }
  function coaster(ctx, t, s) {
    L.sky(ctx, '#9FD3EA', '#F4EDE0', H);
    // the track climbing to the first drop
    const track = []; for (let i = 0; i <= 40; i++) { const x = -40 + i * 52; track.push([x, 980 - Math.sin(Math.min(1, i / 30) * Math.PI / 2) * 560 + (i > 30 ? (i - 30) ** 2 * 9 : 0)]); }
    G.line(ctx, track, { lw: 10, color: '#B5553A' }); for (let i = 0; i < 40; i += 2) G.line(ctx, [track[i], [track[i][0], H + 20]], { lw: 4, color: 'rgba(181,85,58,0.6)' });
    const cx = 1300, cy = 470;
    G.rrect(ctx, cx - 340, cy - 40, 680, 120, 30, { fill: '#D8352A', lw: 5, seed: 720 });
    const riders = ['kid1', 'kid2', 'sam', 'kid3'];
    riders.forEach((k, i) => {
      const sam = k === 'sam', x = cx - 255 + i * 170;
      person(ctx, { x, y: cy + 10, s: 0.55, pose: 'sit', style: C[k], gesture: sam ? null : 'cheer', t: t + i * 0.3, eyes: sam ? (t > A('coaster', 'You yawn') ? 'closed' : 'normal') : 'wide', mouth: sam ? (t > A('coaster', 'You yawn') && t < A('coaster', 'You yawn') + 1.6 ? 'o' : 'flat') : 'open', brows: sam ? 'neutral' : 'worried', handR: sam ? [70, -120] : undefined, shadow: false, seed: 730 + i * 20 });
      if (sam) { G.poly(ctx, [[x + 20, cy - 70], [x + 70, cy - 70], [x + 62, cy - 10], [x + 28, cy - 10]], { fill: '#F6F0E2', lw: 3, seed: 731 }); for (let p = 0; p < 4; p++) G.ellipse(ctx, x + 30 + p * 11, cy - 74, 8, 7, { fill: '#FBE9B0', lw: 2, seed: 732 + p }); }
    });
    G.rrect(ctx, cx - 340, cy + 10, 680, 70, 20, { fill: '#D8352A', lw: 5, seed: 721 });
    if (t > A('coaster', 'popcorn')) L.label(ctx, 'popcorn: still in the bag', 700, 220, { size: 50, rot: -0.04 });
    mon(ctx, t, { x: 60, y: 60, others: true });
  }
  // ================= the science and the rule =================
  function brain(ctx, t, s) {
    G.bg(ctx, '#F4EDE0');
    const tName = A('brain', 'Your name'), tAlm = A('brain', 'almonds'), tSnake = A('brain', 'See a snake'), tYou = A('brain', 'You?');
    if (t < tAlm) { person(ctx, { x: 960, y: 1080, s: 1.4, pose: 'stand', style: C.sam, gesture: 'wave', t, mouth: 'grin', eyes: 'happy', seed: 300 }); L.stampText(ctx, t, tName + 0.4, 'SAM', 960, 200, { size: 150, color: '#3D7A74' }); return; }
    // a brain, side view, with the two almond-shaped amygdalae
    G.ellipse(ctx, 700, 520, 360, 280, { fill: '#F2C4C8', lw: 6, seed: 800, hatch: { color: 'rgba(160,80,90,0.15)', gap: 12 } });
    for (let i = 0; i < 7; i++) G.line(ctx, [[420 + i * 80, 330 + (i % 2) * 40], [460 + i * 80, 440], [430 + i * 80, 560 + (i % 3) * 30]], { lw: 3, color: 'rgba(160,80,90,0.5)' });
    const glow = t > tSnake ? 0.5 + 0.5 * Math.sin(t * 12) : 0.4;
    for (const dx of [-30, 30]) G.ellipse(ctx, 760 + dx, 600, 26, 40, { fill: `rgba(224,112,62,${0.6 + 0.4 * glow})`, lw: 4, seed: 801 + dx });
    L.label(ctx, 'amygdala', 760, 700, { size: 44, color: '#B9532A', alpha: L.fade(t, A('brain', 'amygdala')) });
    if (t > tSnake && t < tYou) {
      L.snake(ctx, [[1200, 900], [1260, 860], [1320, 900], [1380, 860], [1440, 880]], t, { lw: 26 });
      G.line(ctx, [[1200, 840], [1000, 760], [800, 640]], { lw: 6, color: '#F2B84B' });
      const items = [[A('brain', 'heart races'), '♥ racing'], [A('brain', 'Adrenaline'), 'adrenaline!'], [A('brain', 'muscles'), 'muscles tense']];
      items.forEach(([tt, txt], i) => L.stampText(ctx, t, tt, txt, 1450, 260 + i * 130, { size: 64, color: '#D8352A', fam: 'Permanent Marker', strokeW: 0 }));
    }
    if (t > tYou) { ctx.fillStyle = 'rgba(244,237,224,0.85)'; ctx.fillRect(0, 0, W, H); person(ctx, { x: 960, y: 1080, s: 1.3, pose: 'stand', style: C.sam, mouth: 'flat', seed: 300 }); L.stampText(ctx, t, A('brain', 'Nothing'), 'NOTHING.', 960, 220, { size: 110, color: '#5B6F8A' }); }
  }
  function sm(ctx, t, s) {
    G.bg(ctx, '#EADFCB');
    L.card(ctx, t, A('sm', 'known only'), 200, 160, 620, 720, (c, w, h) => {
      G.text(c, 'CASE FILE', 0, -h / 2 + 70, { size: 52, align: 'center', fam: 'Bungee', weight: 400, color: '#B9532A' });
      G.text(c, 'patient: S.M.', -w / 2 + 40, -h / 2 + 170, { size: 44, fam: 'Gochi Hand', weight: 400 });
      if (t > A('sm', 'rare disease')) G.text(c, 'both amygdalae damaged', -w / 2 + 40, -h / 2 + 250, { size: 40, fam: 'Gochi Hand', weight: 400 });
      if (t > A('sm', 'handled snakes')) G.text(c, '✓ handled snakes', -w / 2 + 40, -h / 2 + 340, { size: 40, fam: 'Gochi Hand', weight: 400, color: '#3D7A74' });
      if (t > A('sm', 'haunted house')) G.text(c, '✓ poked a monster', -w / 2 + 40, -h / 2 + 420, { size: 40, fam: 'Gochi Hand', weight: 400, color: '#3D7A74' });
    }, { rot: -0.03, fill: '#FBF8F1' });
    if (t > A('sm', 'handled snakes') && t < A('sm', 'haunted house')) L.snake(ctx, [[1000, 700], [1100, 620], [1200, 700], [1300, 620], [1400, 660], [1480, 600]], t, { lw: 40 });
    if (t > A('sm', 'haunted house')) {
      const jumped = t > A('sm', 'actor jumped');
      person(ctx, { x: 1350, y: 1040 - (jumped ? 60 * Math.max(0, Math.sin((t - A('sm', 'actor jumped')) * 6)) : 0), s: 1.0, pose: 'stand', style: C.monster, handL: jumped ? [-170, -470] : [-120, -200], handR: jumped ? [170, -470] : [120, -200], eyes: jumped ? 'wide' : 'normal', mouth: jumped ? 'o' : 'open', brows: jumped ? 'up' : 'determined', seed: 700 });
      if (jumped) L.label(ctx, 'the ACTOR jumped', 1350, 300, { size: 54, color: '#D8352A', rot: 0.05 });
    }
  }
  function rule(ctx, t, s) {
    G.bg(ctx, '#F4EDE0');
    L.stampText(ctx, t, s.t0 + 0.4, 'THE RULE', 960, 150, { size: 110, color: '#F2B84B' });
    if (t > A('rule', 'fear is gone')) { G.rrect(ctx, 260, 300, 560, 300, 30, { fill: '#27305C', lw: 6, seed: 810 }); L.label(ctx, 'FEAR', 540, 400, { size: 70, color: '#F6F0E2', fam: 'Bungee' }); G.rrect(ctx, 400, 450, 280, 100, 50, { fill: '#5B6F8A', lw: 5, seed: 811 }); G.ellipse(ctx, 450, 500, 40, 40, { fill: '#F6F0E2', lw: 4, seed: 812 }); L.label(ctx, 'OFF', 600, 520, { size: 46, color: '#F6F0E2', fam: 'Bungee' }); }
    if (t > A('rule', 'danger is not')) { G.poly(ctx, [[1380, 300], [1620, 640], [1140, 640]], { fill: '#F2B84B', lw: 6, seed: 813 }); L.label(ctx, '!', 1380, 610, { size: 160, fam: 'Bungee' }); L.label(ctx, 'DANGER: ON', 1380, 740, { size: 60, color: '#D8352A', fam: 'Bungee' }); }
    if (t > A('rule', 'alarm')) {
      ctx.fillStyle = 'rgba(244,237,224,0.92)'; ctx.fillRect(0, 230, W, 760);
      G.ellipse(ctx, 800, 560, 150, 150, { fill: '#D8352A', lw: 6, seed: 814 }); G.ellipse(ctx, 800, 560, 60, 60, { fill: '#F2B84B', lw: 4, seed: 815 });
      G.line(ctx, [[800, 710], [880, 820], [1060, 830]], { lw: 6 });
      const unplug = t > A('rule', 'unplugged') ? ease.outBack(L.u(t, A('rule', 'unplugged'), A('rule', 'unplugged') + 0.6)) : 0;
      G.rrect(ctx, 1060 + unplug * 120, 805, 70, 50, 8, { fill: '#B9BEC6', lw: 4, seed: 816 }); G.rrect(ctx, 1260, 790, 90, 80, 10, { fill: '#F6F0E2', lw: 4, seed: 817 });
      L.label(ctx, 'the alarm', 800, 330, { size: 56 });
      if (unplug > 0) L.label(ctx, 'unplugged', 1200, 700, { size: 56, color: '#D8352A' });
    }
  }
  function title(ctx, t, s) {
    G.bg(ctx, '#27305C');
    G.rays(ctx, 960, 540, { n: 36, r0: 150, r1: 1500, color: 'rgba(124,242,168,0.18)', lw: 20, seed: 9, spin: (t - s.t0) * 0.15 });
    const k = L.pop(t, S.ev.title, 0.35);
    ctx.save(); ctx.translate(960, 420); ctx.scale(k, k);
    G.text(ctx, 'WHAT IF YOU HAD', 0, 0, { size: 110, align: 'center', fam: 'Bungee', weight: 400, color: '#F6F0E2', stroke: INK, strokeW: 10 });
    G.text(ctx, 'ZERO FEAR?', 0, 160, { size: 170, align: 'center', fam: 'Bungee', weight: 400, color: '#7CF2A8', stroke: INK, strokeW: 12 });
    ctx.restore();
    mon(ctx, t, { x: 760, y: 700, w: 400, h: 190 });
  }
  // ================= the montage =================
  function speech(ctx, t, s) {
    const tMia = A('speech', 'Mia corners'), tExam = A('speech', 'exams');
    if (t < tMia) {
      room(ctx, '#3A2F4A', '#5A4A3A', 700);
      G.rrect(ctx, 0, 640, W, 80, 0, { fill: '#8A5A3A', lw: 5, seed: 820 });
      person(ctx, { x: 960, y: 700, s: 0.8, pose: 'stand', style: C.sam, gesture: 'mic', mouth: Math.sin(t * 8) > 0 ? 'open' : 'smile', seed: 300 });
      G.rrect(ctx, 900, 560, 120, 140, 10, { fill: '#6B4A2A', lw: 4, seed: 821 });
      for (let i = 0; i < 70; i++) { const r = Math.floor(i / 14), c = i % 14; G.ellipse(ctx, 70 + c * 135 + (r % 2) * 60, 800 + r * 60, 26, 26, { fill: ['#E0703E', '#3FA89B', '#F2B84B', '#E8718D', '#9FD3EA'][(i * 7) % 5], lw: 2, seed: 830 + i }); }
      if (t > A('speech', 'Five hundred')) L.stampText(ctx, t, A('speech', 'Five hundred'), '500 FACES', 960, 180, { size: 90, color: '#F2B84B' });
      if (t > A('speech', 'never shakes')) L.label(ctx, 'voice: steady', 1500, 400, { size: 50, color: '#7CF2A8' });
      return;
    }
    if (t < tExam) {
      room(ctx, '#E9E1D3', '#B98E62', 860);
      person(ctx, { x: 760, y: 1060, s: 1.1, pose: 'stand', style: C.sam, look: 1, mouth: 'smile', seed: 300 });
      person(ctx, { x: 1180, y: 1060, s: 1.1, pose: 'stand', style: C.mia, look: -1, gesture: 'shrug', brows: 'up', mouth: talk(t, 'mia', 'o'), seed: 340 });
      return;
    }
    G.bg(ctx, '#F4EDE0');
    L.card(ctx, t, tExam, 300, 140, 640, 760, (c, w, h) => {
      G.text(c, 'FINAL EXAM', 0, -h / 2 + 70, { size: 46, align: 'center', fam: 'Bungee', weight: 400 });
      for (let r = 0; r < 6; r++) for (let q = 0; q < 6; q++) if ((r + q) % 3) G.rrect(c, -200 + q * 66, -h / 2 + 140 + r * 66, 60, 60, 2, { fill: '#FBF8F1', lw: 3, seed: 840 + r * 6 + q });
      L.label(c, 'like a crossword', 0, h / 2 - 50, { size: 40, fam: 'Gochi Hand' });
    }, { rot: -0.03 });
    person(ctx, { x: 1400, y: 1060, s: 1.1, pose: 'stand', style: C.sam, mouth: 'smile', eyes: 'happy', gesture: 'thumbsUp', seed: 300 });
    if (t > A('speech', 'sweaty')) L.label(ctx, '✗ sweaty hands', 1400, 300, { size: 46, color: '#3D7A74' });
    if (t > A('speech', 'blank mind')) L.label(ctx, '✗ blank mind', 1400, 380, { size: 46, color: '#3D7A74' });
  }
  function space(ctx, t, s) {
    room(ctx, '#DCE6E2', '#B9C3B6', 860);
    const tYou = A('space', 'You?'), tBack = A('space', 'stepping back'), tLeo = A('space', 'Leo tugs');
    // normal: an arm's length (top) vs Sam: about half (bottom)
    const close = t > tYou;
    const strangerX = close ? 1060 : 1300, back = t > tBack ? ease.outCubic(L.u(t, tBack, tBack + 1)) * 200 : 0;
    person(ctx, { x: 760, y: 1040, s: 1.0, pose: 'stand', style: C.sam, look: 1, mouth: 'smile', seed: 300 });
    person(ctx, { x: strangerX + back, y: 1040, s: 1.0, pose: 'stand', style: C.kid3, look: -1, eyes: close ? 'wide' : 'normal', brows: close ? 'worried' : 'neutral', mouth: close ? 'wavy' : 'smile', seed: 760 });
    G.line(ctx, [[820, 560], [strangerX + back - 60, 560]], { lw: 5, color: close ? '#D8352A' : '#3D7A74', step: 14 });
    L.label(ctx, close ? 'you: about half' : "an arm's length", (760 + strangerX + back) / 2, 520, { size: 46, color: close ? '#D8352A' : '#3D7A74' });
    if (t > tLeo) person(ctx, { x: 420, y: 1040, s: 1.0, pose: 'stand', style: C.leo, handR: [260, -260], look: 1, mouth: talk(t, 'leo', 'flat'), brows: 'worried', seed: 360 });
  }
  function zoo(ctx, t, s) {
    room(ctx, '#3F5A46', '#6B5B3B', 880);
    G.rrect(ctx, 120, 200, 700, 460, 12, { fill: 'rgba(159,211,234,0.35)', lw: 6, seed: 850 }); L.label(ctx, 'REPTILE HOUSE', 470, 160, { size: 46, color: '#F6F0E2', fam: 'Bungee' });
    const hold = t > A('zoo', 'hold the python');
    person(ctx, { x: 1200, y: 1050, s: 1.1, pose: 'stand', style: C.sam, mouth: 'grin', eyes: 'happy', handL: [-150, -300], handR: [150, -300], seed: 300 });
    if (hold) { const y = 1050 - 330 * 1.1; L.snake(ctx, [[1200 - 260, y + 60], [1200 - 160, y - 10], [1200 - 60, y - 40], [1200 + 60, y - 40], [1200 + 160, y - 10], [1200 + 250, y + 30], [1200 + 320, y - 30]], t, { lw: 38 }); }
    else L.snake(ctx, [[260, 600], [360, 560], [460, 600], [560, 560], [640, 580]], t, { lw: 30 });
    person(ctx, { x: 520, y: 1050, s: 1.0, pose: 'stand', style: C.keeper, gesture: t > A('zoo', 'begs') ? 'shrug' : 'point', look: 1, eyes: t > A('zoo', 'begs') ? 'wide' : 'normal', brows: t > A('zoo', 'begs') ? 'worried' : 'neutral', sweat: t > A('zoo', 'begs') ? 1 : 0, mouth: talk(t, 'keeper', 'smile'), seed: 770 });
  }
  function skate(ctx, t, s) {
    L.sky(ctx, '#BFE3F0', '#F4EDE0', H);
    G.poly(ctx, [[-20, 900], [W + 20, 900], [W + 20, H + 20], [-20, H + 20]], { fill: '#9A9AA2', lw: 4, seed: 860 });
    // the ramp
    const rp = []; for (let i = 0; i <= 20; i++) { const u = i / 20; rp.push([200 + u * 900, 900 - (1 - Math.cos(u * Math.PI / 2)) * 0 - (u < 0.5 ? 0 : 0)]); }
    G.poly(ctx, [[1000, 900], [1500, 900], [1500, 380], [1460, 380], [1440, 600], [1300, 820]], { fill: '#C9B48E', lw: 5, seed: 861 });
    const tGo = A('skate', 'First go'), tCrack = S.ev.crack, tCast = A('skate', 'broken wrist');
    if (t < tGo) { person(ctx, { x: 700, y: 900, s: 0.9, pose: 'stand', style: C.sam, look: 1, lookY: -0.4, mouth: 'smile', seed: 300 }); L.board(ctx, 760, 905, 0.6, 0, '#27305C'); }
    else if (t < tCrack) {
      const u = L.u(t, tGo, tCrack); const x = lerp(1100, 1480, u), y = 900 - Math.sin(u * Math.PI * 0.9) * 560;
      person(ctx, { x, y, s: 0.8, pose: 'stand', style: C.sam, rot: u * 2.6, handL: [-160, -380], handR: [160, -380], eyes: 'wide', mouth: 'o', shadow: false, seed: 300 });
      L.board(ctx, x + 80, y + 40, 0.5, u * 4, '#27305C');
    } else if (t < tCast) {
      person(ctx, { x: 1180, y: 900, s: 0.85, pose: 'floor', style: C.sam, eyes: 'closed', brows: 'worried', mouth: 'wavy', seed: 300 });
      G.star(ctx, 1260, 760, 90, { fill: '#F2B84B' }); L.label(ctx, 'CRACK', 1260, 660, { size: 90, color: '#D8352A', fam: 'Bungee' });
    } else {
      G.bg(ctx, '#F4EDE0');
      person(ctx, { x: 700, y: 1060, s: 1.2, pose: 'stand', style: C.sam, handR: [120, -230], mouth: 'flat', brows: 'worried', seed: 300 });
      G.rrect(ctx, 700 + 120 * 1.2 - 40, 1060 - 230 * 1.2 - 30, 90, 70, 20, { fill: '#FBF8F1', lw: 5, seed: 862 });
      L.card(ctx, t, A('skate', 'six weeks'), 1100, 240, 560, 560, (c, w, h) => { G.text(c, 'HEALING', 0, -h / 2 + 60, { size: 44, align: 'center', fam: 'Bungee', weight: 400 }); for (let d = 0; d < 42; d++) { const x = -210 + (d % 7) * 70, y = -h / 2 + 110 + Math.floor(d / 7) * 56; G.rrect(c, x, y, 60, 48, 4, { fill: '#FBF8F1', lw: 2, seed: 870 + d }); G.line(c, [[x + 8, y + 8], [x + 52, y + 40]], { lw: 3, color: '#D8352A' }); } L.label(c, '≈ 6 weeks', 0, h / 2 - 30, { size: 40, fam: 'Gochi Hand' }); }, { rot: 0.03 });
      if (t > A('skate', 'Fearless or not')) L.label(ctx, 'fearless or not', 700, 220, { size: 56 });
    }
  }
  function bridge(ctx, t, s) {
    L.sky(ctx, '#9FD3EA', '#E6EFD8', H);
    G.poly(ctx, [[-20, 560], [420, 520], [420, H + 20], [-20, H + 20]], { fill: '#7F8F6A', lw: 5, seed: 880 });
    G.poly(ctx, [[1500, 520], [W + 20, 560], [W + 20, H + 20], [1500, H + 20]], { fill: '#7F8F6A', lw: 5, seed: 881 });
    G.poly(ctx, [[420, 1080], [700, 900], [1000, 980], [1300, 880], [1500, 1080]], { fill: '#5E7A5A', lw: 4, seed: 882 });
    // the glass bridge: see-through
    ctx.save(); ctx.globalAlpha = 0.35; G.rrect(ctx, 400, 520, 1120, 30, 4, { fill: '#BFE3F0', lw: 4, seed: 883 }); ctx.restore(); G.line(ctx, [[400, 520], [1520, 520]], { lw: 3 });
    const tStroll = A('bridge', 'stroll'), tViews = A('bridge', 'By morning');
    ['kid1', 'kid2'].forEach((k, i) => person(ctx, { x: 600 + i * 240, y: 530, s: 0.42, pose: 'floor', style: C[k], eyes: 'closed', brows: 'worried', mouth: 'wavy', shadow: false, seed: 790 + i * 20 }));
    if (t > A('bridge', 'Adults crawl')) L.label(ctx, 'crawling...', 720, 380, { size: 40 });
    const w = Ch.walk(t, { x0: 440, speed: 60, t0: tStroll, stride: 260 });
    person(ctx, { ...(t > tStroll ? w : { x: 440, pose: 'stand' }), y: 520, s: 0.5, style: C.sam, handR: [60, -330], mouth: 'smile', eyes: 'happy', shadow: false, seed: 300 });
    if (t > tStroll) G.ellipse(ctx, (t > tStroll ? w.x : 440) + 30, 520 - 0.5 * 330, 12, 12, { fill: '#D8352A', lw: 2, seed: 884 });
    if (t > A('bridge', 'films it')) {
      L.card(ctx, t, A('bridge', 'films it'), 1160, 90, 620, 360, (c, w2, h2) => { c.fillStyle = '#20232C'; c.fillRect(-w2 / 2, -h2 / 2, w2, h2); G.text(c, '▶', 0, -30, { size: 100, align: 'center', color: '#F6F0E2', fam: 'Inter', weight: 800, boil: 0 }); Data.counter(c, { x: 0, y: 110, from: 0, to: 2000000, t, t0: tViews, t1: s.t1 - 0.3, size: 56, color: '#F2B84B', suffix: ' views', fam: 'Bungee' }); }, { rot: 0.03 });
    }
    mon(ctx, t, { x: 60, y: 60 });
  }
  function message(ctx, t, s) {
    G.bg(ctx, '#2A2836');
    const chat = [{ t: A('message', 'We pay'), who: 'them', text: 'We pay. Big. 💰' }, { t: A('message', 'Why waste'), who: 'them', text: 'Why waste a gift like yours?' }];
    UI.phone(ctx, 620, 540, 900, (c, w, h, tt) => { c.fillStyle = '#F3F1EE'; c.fillRect(0, 0, w, h); UI.header(c, w, 'Mr. Black', { kicker: 'STUNT CHANNEL · 9M subscribers' }); UI.chat(c, w, chat, tt, { y0: 200, size: 30 }); }, t, { rot: -0.03 });
    person(ctx, { x: 1420, y: 1060, s: 1.25, pose: 'stand', style: C.black, crossArms: t < chat[0].t, mouth: talk(t, 'black', 'smirk'), seed: 390 });
    if (t > A('message', 'biggest stunt')) L.label(ctx, 'the biggest stunt channel', 1420, 250, { size: 44, color: '#F2B84B' });
    L.light(ctx, 1420, 400, '#FFFFFF', '#6A72B0', 'multiply', 0.5);
  }
  // ================= the cost =================
  function cost(ctx, t, s) {
    G.bg(ctx, '#E9E1D3');
    const tBody = A('cost', 'body screams'), tBrain = A('cost', 'brain knows'), tRush = A('cost', 'clash'), tHalf = A('cost', 'only get half');
    L.label(ctx, 'why a roller coaster is fun', 960, 130, { size: 56, alpha: L.fade(t, A('cost', 'fun for a reason')) });
    if (t > tBody) L.card(ctx, t, tBody, 160, 240, 480, 420, (c, w, h) => { G.text(c, 'BODY', 0, -h / 2 + 70, { size: 54, align: 'center', fam: 'Bungee', weight: 400 }); G.text(c, 'DANGER!', 0, 40, { size: 70, align: 'center', fam: 'Bungee', weight: 400, color: '#D8352A' }); }, { rot: -0.04, seed: 141 });
    if (t > tBrain) L.card(ctx, t, tBrain, 720, 240, 480, 420, (c, w, h) => { G.text(c, 'BRAIN', 0, -h / 2 + 70, { size: 54, align: 'center', fam: 'Bungee', weight: 400 }); G.text(c, "you're safe", 0, 40, { size: 60, align: 'center', fam: 'Gochi Hand', weight: 400, color: '#3D7A74' }); }, { rot: 0.03, seed: 142 });
    if (t > tRush) L.card(ctx, t, tRush, 1280, 240, 480, 420, (c, w, h) => { G.text(c, '= RUSH', 0, 20, { size: 80, align: 'center', fam: 'Bungee', weight: 400, color: '#F2B84B', stroke: INK, strokeW: 6 }); }, { rot: -0.02, seed: 143 });
    if (t > tHalf) {
      ctx.fillStyle = 'rgba(233,225,211,0.9)'; ctx.fillRect(0, 200, W, 760);
      G.rrect(ctx, 620, 380, 600, 260, 30, { fill: '#F6F0E2', lw: 6, seed: 890 }); G.rrect(ctx, 1220, 460, 40, 100, 8, { fill: '#F6F0E2', lw: 5, seed: 891 });
      G.rrect(ctx, 640, 400, 280, 220, 18, { fill: '#7CF2A8', lw: 0, stroke: null, seed: 892 });
      L.label(ctx, 'you get half', 920, 760, { size: 60 });
      if (t > A('cost', 'No spark')) L.label(ctx, 'no thrill · no spark', 920, 860, { size: 48, color: '#5B6F8A' });
    }
  }
  function faceOf(ctx, x, y, s, scared, blank) {
    person(ctx, { x, y, s, pose: 'stand', style: C.mia, eyes: scared && !blank ? 'wide' : 'normal', brows: scared && !blank ? 'worried' : 'neutral', mouth: scared && !blank ? 'wavy' : 'flat', sweat: scared && !blank ? 1 : 0, seed: 340 });
  }
  function faces(ctx, t, s) {
    G.bg(ctx, '#F4EDE0');
    const tBlank = A('faces', 'frightened face'), tMia = A('faces', 'Mia trembles'), tWeek = A('faces', "doesn't speak"), tRule = A('faces', 'make yourself a rule');
    if (t < tMia) {
      L.label(ctx, 'the amygdala also reads fear in faces', 960, 140, { size: 50, alpha: L.fade(t, A('faces', 'spot fear')) });
      ctx.save(); ctx.beginPath(); ctx.rect(120, 220, 800, 650); ctx.clip(); faceOf(ctx, 520, 1500, 2.4, true, false); ctx.restore(); G.rrect(ctx, 120, 220, 800, 650, 8, { fill: null, lw: 6, seed: 895 });
      L.label(ctx, 'what everyone sees', 520, 935, { size: 42 });
      if (t > tBlank) { ctx.save(); ctx.beginPath(); ctx.rect(1000, 220, 800, 650); ctx.clip(); ctx.filter = 'grayscale(0.7)'; faceOf(ctx, 1400, 1500, 2.4, true, true); ctx.filter = 'none'; ctx.restore(); G.rrect(ctx, 1000, 220, 800, 650, 8, { fill: null, lw: 6, seed: 896 }); L.label(ctx, 'what you see: blank', 1400, 935, { size: 42, color: '#5B6F8A' }); }
      return;
    }
    if (t < tRule) {
      room(ctx, '#E9E1D3', '#B98E62', 860);
      faceOf(ctx, 1150, 1060, 1.1, true, false);
      person(ctx, { x: 700, y: 1060, s: 1.1, pose: 'stand', style: C.sam, gesture: t < tWeek ? 'thumbsUp' : null, mouth: t < tWeek ? 'grin' : 'flat', brows: t > tWeek ? 'worried' : 'neutral', seed: 300 });
      if (t > A('faces', 'looks totally fine')) L.label(ctx, '"you look totally fine!"', 700, 300, { size: 46 });
      if (t > tWeek) { ctx.fillStyle = 'rgba(42,35,32,0.25)'; ctx.fillRect(950, 0, 970, H); L.label(ctx, 'one week of silence', 1400, 300, { size: 48, color: '#F6F0E2' }); }
      return;
    }
    G.bg(ctx, '#27305C');
    person(ctx, { x: 960, y: 1080, s: 1.4, pose: 'stand', style: C.sam, gesture: 'think', mouth: talk(t, 'sam', 'flat'), brows: 'determined', seed: 300 });
    L.label(ctx, "I can't feel it. So I have to think it.", 960, 160, { size: 62, color: '#7CF2A8', alpha: L.fade(t, A('faces', "I can't feel")) });
  }
  // ================= Leo =================
  function leo(ctx, t, s) {
    G.bg(ctx, '#F4EDE0');
    const tScared = A('leo', 'scared of everything'), tChair = A('leo', 'chair'), tDeal = A('leo', 'made you a deal');
    const lx = 960, ly = 1080, ls = 1.4;
    if (t < tChair) {
      person(ctx, { x: lx, y: ly, s: ls, pose: 'stand', style: C.leo, mouth: 'smile', eyes: blinkAt(t, 2) ? 'closed' : 'normal', brows: t > tScared ? 'worried' : 'neutral', seed: 360 });
      L.stampText(ctx, t, s.t0 + 0.5, 'LEO', 960, 160, { size: 130, color: '#E0703E' });
      const items = [[A('leo', 'Dogs'), 'dogs', 420, 380], [A('leo', 'Thunder'), 'thunder', 1500, 380], [A('leo', 'The dark'), 'the dark', 420, 700], [A('leo', 'heights'), 'HEIGHTS', 1500, 700]];
      items.forEach(([tt, txt, x, y], i) => L.stampText(ctx, t, tt, txt, x, y, { size: i === 3 ? 90 : 64, color: i === 3 ? '#D8352A' : '#5B6F8A', fam: 'Permanent Marker', strokeW: 0, rot: (i % 2 ? 0.06 : -0.06) }));
      return;
    }
    if (t < tDeal) {
      room(ctx, '#E9E1D3', '#B98E62', 900);
      G.rrect(ctx, 820, 760, 220, 30, 6, { fill: '#8A5A3A', lw: 5, seed: 900 }); G.line(ctx, [[840, 790], [840, 900]], { lw: 6 }); G.line(ctx, [[1020, 790], [1020, 900]], { lw: 6 });
      person(ctx, { x: 1250, y: 980, s: 1.0, pose: 'stand', style: C.leo, crossArms: true, brows: 'worried', mouth: 'wavy', look: -1, seed: 360 });
      G.ellipse(ctx, 930, 140, 30, 40, { fill: '#F6F0E2', lw: 4, seed: 901 }); L.label(ctx, 'nope.', 1250, 420, { size: 54, rot: 0.05 });
      return;
    }
    // the deal: two taps on the chest
    G.bg(ctx, '#F4EDE0');
    const [cx, cy] = chest(lx, ly, ls);
    const tapping = L.tapCount(t) > 0;
    person(ctx, { x: lx, y: ly, s: ls, pose: 'stand', style: C.leo, handR: tapping ? [40, -270] : null, mouth: talk(t, 'leo', 'smile'), brows: 'up', seed: 360 });
    L.taps(ctx, t, cx + 20, cy, 1.4);
    if (t > A('leo', 'Two taps on my chest')) L.label(ctx, 'two taps = I\'m scared', 960, 140, { size: 66, color: '#E0703E' });
    if (t > A('leo', 'and you stop')) L.label(ctx, '...and you stop.', 1500, 520, { size: 54, rot: 0.04 });
  }
  function tell(ctx, t, s) {
    room(ctx, '#DCE6E2', '#9AA8A0', 860);
    person(ctx, { x: 640, y: 1060, s: 1.15, pose: 'stand', style: C.sam, look: 1, mouth: talk(t, 'sam', 'smile'), seed: 300 });
    const [cx, cy] = chest(1280, 1060, 1.15);
    person(ctx, { x: 1280, y: 1060, s: 1.15, pose: 'stand', style: C.leo, look: -1, mouth: talk(t, 'leo', 'flat'), handR: L.tapCount(t) > 0 ? [40, -270] : null, seed: 360 });
    L.taps(ctx, t, cx + 20, cy, 1.15);
    if (t > A('tell', "can't read his face")) L.label(ctx, '(to you: just a face)', 1280, 300, { size: 44, color: '#5B6F8A' });
  }
  // ================= the crane =================
  const BEAM_Y = 260;
  function docks(ctx, t, { night = 0 } = {}) {
    L.sky(ctx, '#A9C8DE', '#E9D9C3', H);
    L.sea(ctx, 880, t, { col: '#4A6A80' });
    G.poly(ctx, [[-20, 860], [W + 20, 860], [W + 20, 900], [-20, 900]], { fill: '#8A7A6A', lw: 4, seed: 905 });
    for (let i = 0; i < 6; i++) G.rrect(ctx, 1200 + i * 120, 760 - (i % 2) * 60, 110, 100 + (i % 2) * 60, 4, { fill: ['#D8352A', '#3D7A74', '#F2B84B'][i % 3], lw: 4, seed: 906 + i });
    L.crane(ctx, 300, BEAM_Y, 1);
  }
  function crane(ctx, t, s) {
    docks(ctx, t);
    const tLive = A('crane', 'stream goes live'), tTug = S.ev.unclip, tHalf = A('crane', 'halfway');
    const sx = t < tHalf ? lerp(380, 900, L.u(t, A('crane', 'Cameras'), tTug)) : 900;
    person(ctx, { x: sx, y: BEAM_Y - 34, s: 0.32, pose: 'stand', style: C.sam, handL: [-170, -300], handR: [170, -300], shadow: false, mouth: 'flat', seed: 300 });
    // the safety line: clipped to the belt, then loose and falling
    const belt = [sx, BEAM_Y - 34 - 150 * 0.32];
    if (t < tTug) G.line(ctx, [belt, [sx - 100, BEAM_Y - 20], [330, BEAM_Y - 10]], { lw: 3, color: '#F2B84B' });
    else { const f = ease.inQuad(L.u(t, tTug, tTug + 1.2)); G.line(ctx, [[330, BEAM_Y - 10], [400 + f * 50, BEAM_Y + 200 * f + 40], [460 + f * 80, BEAM_Y + 500 * f + 60]], { lw: 3, color: '#F2B84B' }); }
    for (let i = 0; i < 3; i++) L.camera(ctx, 900 + i * 300, 780, 0.8, t > tLive, t + i);
    person(ctx, { x: 640, y: 870, s: 0.7, pose: 'stand', style: C.black, gesture: t > tTug - 0.3 && t < tTug + 0.8 ? 'point' : 'phone', mouth: talk(t, 'black', 'smirk'), seed: 390 });
    L.label(ctx, '40 m', 220, 520, { size: 60, color: '#D8352A', alpha: L.fade(t, A('crane', 'forty meters')) });
    L.label(ctx, '30 cm wide', 760, 330, { size: 44, alpha: L.fade(t, A('crane', 'Thirty centimeters')) });
    if (t > tLive) { G.rrect(ctx, 1640, 60, 200, 70, 14, { fill: '#D8352A', lw: 4, seed: 907 }); L.label(ctx, '● LIVE', 1740, 112, { size: 40, color: '#FFFFFF', fam: 'Bungee' }); }
    if (t > tTug) L.label(ctx, 'unclipped!', 520, 420, { size: 56, color: '#D8352A', alpha: L.fade(t, tTug + 0.3) });
    mon(ctx, t, { x: 1450, y: 160, w: 400, h: 170 });
  }
  function leoClimb(t, s) { // Leo's height on the ladder (0..1 of 30 m), frozen once he stops
    const tUp = A('ladder', "He's climbing"), tStop = A('ladder', 'Then he stops');
    return ease.inOutQuad(L.u(t, tUp, tStop)) * 0.75;
  }
  function ladder(ctx, t, s) {
    docks(ctx, t);
    const lx = 330, top = BEAM_Y, bottom = 870;
    L.ladder(ctx, lx, top, bottom, 60);
    const h = leoClimb(t, s), ly = lerp(bottom, top + 120, h / 0.75 * 0.78);
    const slip = t > A('ladder', 'slipping') ? Math.sin(t * 30) * 4 : 0;
    person(ctx, { x: lx + slip, y: ly + 80, s: 0.42, pose: 'stand', style: C.leo, handL: [-60, -470], handR: [60, -470], eyes: 'closed', brows: 'worried', mouth: talk(t, 'leo', 'wavy'), shadow: false, seed: 360 });
    person(ctx, { x: 900, y: BEAM_Y - 34, s: 0.32, pose: 'stand', style: C.sam, look: -1, lookY: 0.6, handL: [-170, -300], handR: [170, -300], shadow: false, mouth: 'o', seed: 300 });
    [[A('ladder', 'Ten meters'), '10 m', 0.25], [A('ladder', 'Twenty'), '20 m', 0.5], [A('ladder', 'Thirty'), '30 m', 0.75]].forEach(([tt, txt, k]) => { if (t > tt) L.label(ctx, txt, lx - 140, lerp(bottom, top, k) + 20, { size: 46, color: '#D8352A' }); });
    if (t > A('ladder', 'wind')) for (let i = 0; i < 6; i++) { const x = ((t * 500 + i * 330) % 2200) - 200; G.line(ctx, [[x, 300 + i * 70], [x + 160, 296 + i * 70]], { lw: 3, color: 'rgba(255,255,255,0.8)' }); }
    if (t > A('ladder', 'under three seconds')) L.label(ctx, 'a fall: under 3 seconds', 1100, 520, { size: 52, color: '#D8352A' });
    mon(ctx, t, { x: 1450, y: 60, w: 400, h: 170 });
  }
  function choice(ctx, t, s) {
    G.bg(ctx, '#1E2046');
    const tSplit = S.ev.choice, tTap = A('choice', 'taps his chest');
    if (t < A('choice', 'Ahead')) {
      // Leo's face, as Sam sees it: no fear to read
      ctx.save(); ctx.beginPath(); ctx.rect(560, 120, 800, 760); ctx.clip(); G.bg(ctx, '#A9C8DE'); person(ctx, { x: 960, y: 1500, s: 2.3, pose: 'stand', style: C.leo, mouth: 'flat', seed: 360 }); ctx.restore();
      G.rrect(ctx, 560, 120, 800, 760, 8, { fill: null, lw: 6, seed: 910 });
      if (t > A('choice', 'just...')) L.label(ctx, '...just a face', 960, 960, { size: 56, color: '#F6F0E2' });
      if (t > A('choice', 'earpiece')) { G.rrect(ctx, 80, 80, 420, 120, 26, { fill: '#2A2836', lw: 5, seed: 911 }); L.label(ctx, 'Mr. Black', 290, 158, { size: 44, color: '#F6F0E2' }); }
      mon(ctx, t, { x: 1450, y: 60, w: 400, h: 170 });
      return;
    }
    // the split: the views ahead, Leo behind
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W / 2 - 6, H); ctx.clip(); G.bg(ctx, '#2A2836');
    G.rrect(ctx, 160, 220, 640, 360, 20, { fill: '#20232C', lw: 6, seed: 912 }); Data.counter(ctx, { x: 480, y: 420, from: 600000, to: 1000000, t, t0: A('choice', 'Ahead'), t1: tSplit, size: 70, color: '#F2B84B', fam: 'Bungee' }); L.label(ctx, 'watching', 480, 500, { size: 40, color: '#F6F0E2' });
    if (t > A('choice', 'The money')) L.label(ctx, '$$$', 480, 720, { size: 110, color: '#7CF2A8', fam: 'Bungee' });
    ctx.restore();
    ctx.save(); ctx.beginPath(); ctx.rect(W / 2 + 6, 0, W / 2, H); ctx.clip(); G.bg(ctx, '#A9C8DE');
    L.ladder(ctx, 1440, -20, H + 20, 90);
    const [cx, cy] = chest(1440, 1000, 1.0);
    person(ctx, { x: 1440, y: 1000, s: 1.0, pose: 'stand', style: C.leo, handL: [-70, -470], handR: t > tTap ? [40, -270] : [70, -470], eyes: 'closed', brows: 'worried', mouth: 'flat', shadow: false, seed: 360 });
    L.taps(ctx, t, cx + 20, cy, 1.0);
    ctx.restore();
    G.line(ctx, [[W / 2, 0], [W / 2, H]], { lw: 8 });
    if (t > tSplit) L.label(ctx, 'the views...', 480, 900, { size: 72, color: '#F2B84B', rot: -0.04 });
    if (t > A('choice', 'or Leo')) L.label(ctx, '...or Leo', 1440, 160, { size: 72, color: '#27305C', rot: 0.04 });
  }
  // ================= the rescue and the ending =================
  function rescue(ctx, t, s) {
    const tTalk = A('rescue', 'Leo. Look'), tThree = A('rescue', 'Three points'), tDown = A('rescue', 'talk him down');
    if (t < tTalk) {
      docks(ctx, t);
      const back = ease.inOutQuad(L.u(t, A('rescue', 'turn around'), A('rescue', 'crouch')));
      person(ctx, { x: lerp(900, 420, back), y: BEAM_Y - 34, s: 0.32, pose: 'stand', style: C.sam, look: -1, handL: [-170, -300], handR: [170, -300], shadow: false, mouth: 'flat', brows: 'determined', seed: 300 });
      L.ladder(ctx, 330, BEAM_Y, 870, 60);
      person(ctx, { x: 330, y: lerp(870, BEAM_Y + 120, 0.78) + 60, s: 0.32, pose: 'stand', style: C.leo, handL: [-60, -470], handR: [60, -470], eyes: 'closed', brows: 'worried', mouth: 'wavy', shadow: false, seed: 360 });
      if (t > A('rescue', 'Step. Breathe')) L.label(ctx, 'step · breathe · step', 960, 520, { size: 60, color: '#27305C' });
      return;
    }
    if (t < tDown) {
      G.bg(ctx, '#A9C8DE');
      L.ladder(ctx, 700, -20, H + 20, 110);
      person(ctx, { x: 700, y: 1100, s: 1.2, pose: 'stand', style: C.leo, handL: [-90, -470], handR: [90, -470], eyes: t > tThree ? 'normal' : 'closed', brows: 'worried', mouth: 'flat', look: 1, shadow: false, seed: 360 });
      person(ctx, { x: 1300, y: 1100, s: 1.2, pose: 'floor', style: C.sam, look: -1, mouth: talk(t, 'sam', 'smile'), brows: 'neutral', seed: 300 });
      if (t > tThree) {
        const hl = [[700 - 90 * 1.2, 1100 - 470 * 1.2], [700 + 90 * 1.2, 1100 - 470 * 1.2], [700 - 40 * 1.2, 1095]];
        hl.forEach(([x, y], i) => { if (t > tThree + 0.4 + i * 0.4) G.ellipse(ctx, x, y, 40, 40, { fill: null, stroke: '#7CF2A8', lw: 7, seed: 920 + i }); });
        L.label(ctx, '3 points of contact', 1300, 200, { size: 60, color: '#27305C' });
      }
      return;
    }
    docks(ctx, t);
    L.ladder(ctx, 330, BEAM_Y, 870, 60);
    const down = ease.inOutQuad(L.u(t, tDown, A('rescue', 'is your voice') + 1));
    person(ctx, { x: 330, y: lerp(lerp(870, BEAM_Y + 120, 0.78) + 60, 870, down), s: 0.32, pose: 'stand', style: C.leo, handL: [-60, -470], handR: [60, -470], brows: 'worried', mouth: 'flat', shadow: false, seed: 360 });
    person(ctx, { x: 330, y: lerp(BEAM_Y + 10, 760, down), s: 0.32, pose: 'stand', style: C.sam, handL: [-60, -470], handR: [60, -470], mouth: Math.sin(t * 7) > 0 ? 'open' : 'smile', shadow: false, seed: 300 });
    if (t > A('rescue', 'One rung')) L.label(ctx, 'one rung at a time', 960, 520, { size: 56, color: '#27305C' });
    if (t > A('rescue', 'only steady thing')) L.label(ctx, 'the only steady thing in the sky', 960, 620, { size: 46, color: '#3D7A74' });
  }
  function truth(ctx, t, s) {
    docks(ctx, t);
    const tCam = A('truth', 'pick up the camera'), tLine = A('truth', 'point it'), tGone = A('truth', 'channel is gone');
    person(ctx, { x: 420, y: 960, s: 0.7, pose: 'floor', style: C.leo, eyes: 'closed', mouth: 'wavy', seed: 360 });
    person(ctx, { x: 880, y: 980, s: 0.85, pose: 'stand', style: C.sam, handR: t > tCam ? [140, -330] : null, mouth: talk(t, 'sam', 'flat'), brows: 'determined', look: 1, seed: 300 });
    if (t > tCam) L.camera(ctx, 880 + 140 * 0.85 + 30, 980 - 330 * 0.85, 0.7, true, t);
    person(ctx, { x: 1400, y: 980, s: 0.85, pose: 'stand', style: C.black, mouth: t > tLine ? 'o' : 'smirk', brows: t > tLine ? 'worried' : 'neutral', look: -1, seed: 390 });
    if (t > tLine) { G.line(ctx, [[1100, 980], [1200, 900], [1260, 960], [1320, 920]], { lw: 4, color: '#F2B84B' }); L.label(ctx, 'unclipped. on purpose.', 1180, 560, { size: 50, color: '#D8352A' }); }
    if (t > A('truth', "don't shout")) L.label(ctx, 'no shouting · no shoving · just the truth', 960, 150, { size: 46, color: '#27305C', alpha: L.fade(t, A('truth', "don't shout")) });
    if (t > tGone) L.card(ctx, t, tGone, 1280, 200, 520, 300, (c, w, h) => { c.fillStyle = '#20232C'; c.fillRect(-w / 2, -h / 2, w, h); G.text(c, 'This channel', 0, -20, { size: 40, align: 'center', color: '#F6F0E2', fam: 'Inter', weight: 700, boil: 0 }); G.text(c, 'no longer exists', 0, 40, { size: 40, align: 'center', color: '#F6F0E2', fam: 'Inter', weight: 700, boil: 0 }); }, { rot: 0.03 });
  }
  function lesson(ctx, t, s) {
    G.bg(ctx, '#F4EDE0');
    L.stampText(ctx, t, A('lesson', 'no video'), 'NO VIDEO IS WORTH', 960, 360, { size: 90, color: '#27305C' });
    L.stampText(ctx, t, A('lesson', 'no video') + 0.6, 'A HOSPITAL BED', 960, 500, { size: 110, color: '#D8352A' });
    if (t > A('lesson', 'safety gear')) L.label(ctx, "they're not the one who'd fall.", 960, 720, { size: 58, alpha: L.fade(t, A('lesson', "not the one")) });
  }
  function brave(ctx, t, s) {
    G.bg(ctx, '#2A2836');
    const comments = ['LEO 🙌', 'Leo is the real hero', 'that climb though', 'LEO LEO LEO', 'brave = Leo', 'so proud of Leo'];
    comments.forEach((c, i) => { const tt = A('brave', 'comments fill') + 0.4 + i * 0.5; if (t < tt) return; const k = L.pop(t, tt); ctx.save(); ctx.translate(200 + (i % 2) * 760, 200 + Math.floor(i / 2) * 150); ctx.scale(k, k); G.rrect(ctx, 0, -50, 680, 100, 24, { fill: '#F6F0E2', lw: 4, seed: 930 + i }); G.text(ctx, c, 30, 16, { size: 44, fam: 'Patrick Hand', weight: 400 }); ctx.restore(); });
    if (t > A('brave', 'Not feeling nothing')) { ctx.fillStyle = 'rgba(42,40,54,0.9)'; ctx.fillRect(0, 640, W, 300); L.label(ctx, 'brave: feeling everything, and climbing anyway', 960, 800, { size: 54, color: '#7CF2A8' }); }
  }
  function ending(ctx, t, s) {
    L.sky(ctx, '#F2B84B', '#E8718D', H);
    L.sun(ctx, 1500, 700, 140, '#FFE08A'); L.sea(ctx, 820, t, { col: '#C77A5E' });
    G.poly(ctx, [[-20, 900], [W + 20, 900], [W + 20, H + 20], [-20, H + 20]], { fill: '#8A6A5A', lw: 4, seed: 940 });
    const tHug = A('end', 'when he hugs'), tGrin = A('end', 'He grins');
    const hug = t > tHug;
    person(ctx, { x: hug ? 880 : 760, y: 1000, s: 1.0, pose: 'stand', style: C.sam, look: 1, handR: hug ? [200, -300] : null, mouth: talk(t, 'sam', t > S.ev.jump ? 'grin' : 'smile'), eyes: t > S.ev.jump ? 'happy' : 'normal', seed: 300 });
    person(ctx, { x: hug ? 1080 : 1160, y: 1000, s: 1.0, pose: 'stand', style: C.leo, look: -1, handL: hug ? [-200, -300] : null, mouth: talk(t, 'leo', t > tGrin ? 'grin' : 'smile'), eyes: 'happy', seed: 360 });
    if (t > A('end', "I can't feel it")) L.label(ctx, "I can't feel it. So I have to think it.", 960, 170, { size: 54, color: '#27305C', alpha: L.fade(t, A('end', "I can't feel it")) * (t < tGrin + 0.3 ? 1 : 0) });
    if (t > A('end', "both of us")) L.label(ctx, "Then I'll feel it for both of us.", 960, 170, { size: 54, color: '#B9532A' });
    if (t > S.ev.jump - 0.05) { const k = U.pulse(t, S.ev.jump, 3); L.label(ctx, '♥', 980, 560 - k * 40, { size: 110 + k * 90, color: '#D8352A', fam: 'Inter' }); }
    mon(ctx, t, { x: 1450, y: 260, w: 400, h: 170 });
    L.light(ctx, 1500, 700, '#FFF4DA', '#C77A5E', 'multiply', 0.45);
  }
  function sting(ctx, t, s) {
    room(ctx, '#1A1C30', '#14152A', 900);
    G.rrect(ctx, 760, 180, 400, 720, 10, { fill: '#5A4A3A', lw: 6, seed: 950 }); G.ellipse(ctx, 1110, 560, 14, 14, { fill: '#F2B84B', lw: 3, seed: 951 });
    const slide = ease.outCubic(L.u(t, s.t0 + 0.3, s.t0 + 1.8));
    G.rrect(ctx, lerp(820, 700, slide), 880, 280, 140, 6, { fill: '#F6F0E2', lw: 4, seed: 952 });
    if (t > A('sting', 'One line')) L.card(ctx, t, A('sting', 'We know'), 460, 260, 1000, 420, (c) => { G.text(c, "We know what you can't feel.", 0, -20, { size: 52, align: 'center', fam: 'Gochi Hand', weight: 400 }); G.text(c, 'We need you.', 0, 70, { size: 64, align: 'center', fam: 'Gochi Hand', weight: 400, color: '#B9532A' }); }, { rot: -0.02, fill: '#FBF8F1' });
    L.light(ctx, 960, 900, '#FFFFFF', '#3A3570', 'multiply', 0.45);
  }
  function cta(ctx, t, s) {
    G.bg(ctx, '#27305C');
    G.rays(ctx, 960, 560, { n: 36, r0: 150, r1: 1500, color: 'rgba(124,242,168,0.16)', lw: 20, seed: 9, spin: (t - s.t0) * 0.12 });
    L.stampText(ctx, t, S.ev.cta, 'WHAT IF?', 960, 220, { size: 140, color: '#7CF2A8' });
    L.label(ctx, 'the first scary thing you\'d try?', 960, 360, { size: 54, color: '#F6F0E2', alpha: L.fade(t, A('cta', 'Tell us')) });
    if (t > A('cta', 'Tell us')) { G.rrect(ctx, 560, 450, 800, 150, 30, { fill: '#F6F0E2', lw: 5, seed: 960 }); G.text(ctx, '💬  tell us in the comments', 960, 545, { size: 50, align: 'center', fam: 'Patrick Hand', weight: 400 }); }
    const kl = L.pop(t, A('cta', 'hit like') + 0.2), ks = L.pop(t, A('cta', 'hit like') + 0.9);
    if (kl > 0) { ctx.save(); ctx.translate(740, 760); ctx.scale(kl, kl); G.rrect(ctx, -170, -60, 340, 120, 60, { fill: '#F6F0E2', lw: 5, seed: 961 }); G.text(ctx, '👍 Like', 0, 20, { size: 56, align: 'center', fam: 'Bungee', weight: 400 }); ctx.restore(); }
    if (ks > 0) { ctx.save(); ctx.translate(1180, 760); ctx.scale(ks, ks); G.rrect(ctx, -220, -60, 440, 120, 60, { fill: '#D8352A', lw: 5, seed: 962 }); G.text(ctx, 'SUBSCRIBE', 0, 20, { size: 56, align: 'center', fam: 'Bungee', weight: 400, color: '#FFFFFF' }); ctx.restore(); }
    if (t > A('cta', 'Part Two')) L.label(ctx, 'Part Two: who sent the envelope?', 960, 920, { size: 46, color: '#F2B84B' });
  }

  const SCENES = { spider, haunted, coaster, brain, sm, rule, title, speech, space, zoo, skate, bridge, message, cost, faces, leo, tell, crane, ladder, choice, rescue, truth, lesson, brave, end: ending, sting, cta };
  Studio.film({
    fadeOut: 1.4,
    async init() { VO = await Studio.loadJSON('out/voice.json'); SUBS = Subs.fromVoice(VO, { maxWords: 7 }); },
    draw(ctx, t) {
      const sc = S.sceneAt(t);
      G.setStyle('paper');
      const u = clamp((t - sc.t0) / (sc.t1 - sc.t0));
      const z = 1 + 0.035 * ease.inOutQuad(u);
      const hit = [S.ev.title, S.ev.crane, S.ev.rescue, S.ev.cta].filter((c) => t >= c && t - c < 0.6).pop();
      const shake = hit !== undefined ? 10 * Math.exp(-(t - hit) * 9) : 0;
      ctx.save();
      ctx.translate(W / 2 + U.noise1(t * 30, 1) * shake, H / 2 + U.noise1(t * 30, 2) * shake); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
      SCENES[sc.id](ctx, t, sc);
      ctx.restore();
      const d = t - sc.t0;
      if (d < 0.18 && sc.t0 > 0 && hit === undefined) { ctx.fillStyle = `rgba(244,237,224,${0.8 * (1 - d / 0.18)})`; ctx.fillRect(0, 0, W, H); }
      if (hit !== undefined && t - hit < 0.18) { ctx.fillStyle = `rgba(255,255,255,${0.75 * (1 - (t - hit) / 0.18)})`; ctx.fillRect(0, 0, W, H); }
      if (t < 0.6) { ctx.fillStyle = `rgba(0,0,0,${1 - t / 0.6})`; ctx.fillRect(0, 0, W, H); }
      Subs.draw(ctx, t, SUBS, { style: 'karaoke', size: 50, y: 1010 });
    },
  });
})();
