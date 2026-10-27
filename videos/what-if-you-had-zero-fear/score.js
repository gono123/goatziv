// WHAT IF YOU HAD ZERO FEAR? (16:9, ~5 min): a narrated 2D short. The narration leads: every line
// sits at a time worked out from its measured length (timing.js), every scene starts where its first
// line does, and every sound and picture hit below is read from those same times.
(function () {
  const node = typeof require !== 'undefined';
  const U = node ? require('./engine/util') : globalThis.U;
  const MU = node ? require('./engine/music') : globalThis.MUSIC;
  const { SCENES, VOICE } = node ? require('./lines') : globalThis.LINES;
  const DUR = node ? require('./timing') : globalThis.VO_DUR;
  const { m, makeClock, makeChords } = MU;

  const FPS = 30;
  const FORMAT = '16:9';
  const [W, H] = U.formatSize(FORMAT);
  const SAFE = U.safeArea(W, H);
  const STYLE = 'paper';

  // ---------- lay the narration out ----------
  const GAP = 0.2;        // breath between lines
  const SCENE_GAP = 0.6;  // extra air before a new scene
  const LEAD = { title: 1.4, brain: 0.6, speech: 0.4, leo: 0.6, crane: 1.2, taps: 0.6, turn: 0.4, psa: 0.4, envelope: 1.4, outro: 1.0 };
  const TAIL = { spider: 0.3, title: 1.2, outro: 4.5 };
  const SC = {};
  const vo = [];
  let cur = 0.8, k = 0;
  SCENES.forEach((s, si) => {
    if (si > 0) cur += SCENE_GAP;
    cur += LEAD[s.id] || 0;
    const t0 = si === 0 ? 0 : cur - 0.45; // the cut lands just before the first word
    const lines = s.lines.map(([text, who = 'narrator', pause]) => {
      const d = DUR[k++] || 2;
      const l = { t: +cur.toFixed(3), end: +(cur + d).toFixed(3), text, who };
      vo.push({ at: l.t, text, who, voice: VOICE });
      cur += d + (pause ?? GAP);
      return l;
    });
    cur += TAIL[s.id] || 0;
    SC[s.id] = { id: s.id, t0: +t0.toFixed(3), lines };
  });
  const ORDER = SCENES.map((s) => s.id);
  ORDER.forEach((id, i) => { SC[id].t1 = i + 1 < ORDER.length ? SC[ORDER[i + 1]].t0 : +(cur + 0.5).toFixed(3); });
  const DURATION = SC[ORDER[ORDER.length - 1]].t1;
  const L = (id, i) => SC[id].lines[i < 0 ? SC[id].lines.length + i : i];

  // ---------- the hits: every one of these is a sound AND a picture ----------
  const ev = {
    spiderLand: L('spider', 0).t + 0.9,
    lightsOut: L('haunted', 0).t + 1.1,
    monster: L('haunted', 1).t + 0.25,
    shriek: L('haunted', 2).t,
    tapShoulder: L('haunted', 3).t + 0.9,
    yawn: L('coaster', 2).t + 0.7,
    snake: L('brain', 3).t + 0.3,
    heart: L('brain', 4).t,
    nothing: L('brain', 8).t + 0.3,
    unplug: L('rule', 5).end + 0.05,
    title: L('title', 0).t + 0.15,
    applause: L('speech', 2).end + 0.1,
    crack: L('skate', 4).t,
    views: L('bridge', 5).t + 0.5,
    msg: L('black', 0).t + 0.4,
    blank: L('faces', 3).end - 0.5,
    dealTaps: [L('deal', 3).end + 0.25, L('deal', 3).end + 0.6],
    tellTaps: [L('tell', 2).end + 0.25, L('tell', 2).end + 0.6],
    live: L('crane', 5).t + 0.4,
    tug: L('crane', 6).t + 0.5,
    rattle: L('climb', 0).t + 0.3,
    slip: L('climb', 8).end - 0.4,
    finalTaps: [L('taps', 2).end + 0.3, L('taps', 2).end + 0.75],
    turn: L('turn', 0).t + 0.2,
    gone: L('truth', 7).t + 1.2,
    jump: L('hug', 8).t + 0.15,
    envelope: L('envelope', 0).t + 1.2,
    note: L('envelope', 3).t - 0.3,
    endCard: L('outro', 2).end + 0.6,
  };
  ev.climbMarks = [0, 1, 2].map((i) => L('climb', 4).t + 0.1 + i * (L('climb', 4).end - L('climb', 4).t) / 3);
  ev.steps = [0, 1, 2].map((i) => L('turn', 3).t + 0.05 + i * (L('turn', 3).end - L('turn', 3).t) / 3);

  // the music's clock: a slow 76 BPM bed under the voice; scenes map to bars
  const clock = makeClock({ bpm: 76, offset: 0 });
  const { T, BEAT, BAR } = clock;
  const barAt = (t) => t / BAR;
  // moods: each scene's bed (song.js turns these into parts)
  const MOOD = {
    spider: 'play', haunted: 'spooky', coaster: 'play', brain: 'curious', sm: 'curious', rule: 'still', title: 'title',
    speech: 'life', exams: 'life', space: 'life', zoo: 'life', skate: 'life', bridge: 'wonder', black: 'dark',
    cost: 'still', faces: 'sad', rule2: 'still', leo: 'tender', deal: 'tender', tell: 'sad',
    crane: 'tension', climb: 'tension', choice: 'tension', taps: 'silence', turn: 'rise', down: 'rise',
    truth: 'warm', psa: 'still', comments: 'warm', hug: 'warm', envelope: 'mystery', outro: 'end',
  };
  const PROG = {
    play: ['C', 'Am', 'F', 'G'], spooky: ['Am', 'Am', 'E', 'E'], curious: ['Am', 'F', 'C', 'G'], still: ['Am', 'F', 'Am', 'F'],
    title: ['F', 'G', 'C', 'C'], life: ['C', 'G', 'Am', 'F'], wonder: ['F', 'C', 'G', 'Am'], dark: ['Am', 'E', 'Am', 'E'],
    sad: ['Am', 'F', 'Dm', 'E'], tender: ['F', 'C', 'Dm', 'G'], tension: ['Am', 'Am', 'F', 'E'], silence: ['Am', 'Am', 'Am', 'Am'],
    rise: ['F', 'G', 'Am', 'C'], warm: ['C', 'F', 'Am', 'G'], mystery: ['Am', 'Dm', 'Am', 'E'], end: ['C', 'G', 'Am', 'F'],
  };
  const sceneAt = (t) => { let id = ORDER[0]; for (const s of ORDER) if (SC[s].t0 <= t) id = s; return id; };
  const nBars = Math.ceil(barAt(DURATION)) + 1;
  const rows = Array.from({ length: nBars }, (_, b) => { const id = sceneAt(T(b) + 0.01); const p = PROG[MOOD[id]]; return [b, 0, 4, p[b % 4]]; });
  const { chords, chordAt } = makeChords(clock, {
    C: { notes: ['E3', 'G3', 'C4'], bass: 'C2' }, G: { notes: ['D3', 'G3', 'B3'], bass: 'G1' }, Am: { notes: ['E3', 'A3', 'C4'], bass: 'A1' },
    F: { notes: ['F3', 'A3', 'C4'], bass: 'F1' }, Dm: { notes: ['F3', 'A3', 'D4'], bass: 'D2' }, E: { notes: ['E3', 'G#3', 'B3'], bass: 'E2' },
  }, rows);

  const markers = {
    spider: { t: ev.spiderLand, sync: 'av' },
    monster: { t: ev.monster, sync: 'av' },
    title: { t: ev.title, sync: 'av' },
    crack: { t: ev.crack, sync: 'av' },
    tap1: { t: ev.finalTaps[0], sync: 'av' },
    tap2: { t: ev.finalTaps[1], sync: 'av' },
    jump: { t: ev.jump, sync: 'av' },
    envelope: { t: ev.envelope, sync: 'v' },
    end: { t: ev.endCard, sync: 'av' },
    crane: SC.crane.t0, choice: SC.choice.t0, turn: SC.turn.t0, hug: SC.hug.t0,
  };
  const S = Object.fromEntries(ORDER.map((id) => [id, [SC[id].t0, SC[id].t1]]));

  const SCORE = { FPS, FORMAT, W, H, SAFE, STYLE, DURATION, clock, T, BEAT, BAR, m, chords, chordAt, vo, SC, ORDER, L, ev, MOOD, S, sceneAt, markers, VOICE };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
