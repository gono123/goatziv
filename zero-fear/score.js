// WHAT IF YOU HAD ZERO FEAR? (16:9, ~7 min). The voiceover's measured line times (timeline.js, from
// timing.js) are the spine: every scene, heartbeat, tap, hit and music section is placed from them, so the
// voice, the picture and the score cannot drift apart.
(function () {
  const node = typeof require !== 'undefined';
  const U = node ? require('./engine/util') : globalThis.U;
  const MU = node ? require('./engine/music') : globalThis.MUSIC;
  const TL = node ? require('./timeline') : globalThis.TIMELINE;
  const { VOICES } = node ? require('./lines') : globalThis.LINES;
  const { m, makeClock, makeChords } = MU;

  const FPS = 30;
  const FORMAT = '16:9';
  const STYLE = 'paper';
  const [W, H] = U.formatSize(FORMAT);
  const SAFE = U.safeArea(W, H);
  const clock = makeClock({ bpm: 84, offset: 0 });
  const { T, BEAT, BAR } = clock;
  const DURATION = TL.DURATION;

  const SC = {}; TL.scenes.forEach((s) => { SC[s.id] = s; });
  const sceneAt = (t) => TL.scenes.find((s) => t >= s.t0 && t < s.t1) || TL.scenes[TL.scenes.length - 1];
  const line = (scene, text) => { const l = TL.lines.find((x) => x.scene === scene && x.text.includes(text)); if (!l) throw new Error(`no line "${text}" in ${scene}`); return l; };
  const at = (scene, text) => line(scene, text).at;
  const end = (scene, text) => { const l = line(scene, text); return l.at + l.dur; };
  const vo = TL.lines.map((l) => ({ at: l.at, text: l.text, who: l.who, voice: VOICES[l.who].voice, rate: VOICES[l.who].rate }));

  const MOOD = { spider: 'playful', haunted: 'playful', coaster: 'playful', brain: 'wonder', sm: 'wonder', rule: 'wonder', title: 'wonder',
    speech: 'groove', space: 'groove', zoo: 'groove', skate: 'groove', bridge: 'groove', message: 'shady',
    cost: 'sad', faces: 'sad', leo: 'tender', tell: 'tender', crane: 'tension', ladder: 'tension', choice: 'tension',
    rescue: 'rescue', truth: 'warm', lesson: 'warm', brave: 'warm', end: 'tender', sting: 'eerie', cta: 'groove' };
  const moodAt = (t) => MOOD[sceneAt(t).id];
  const NBARS = Math.ceil(DURATION / BAR) + 1;
  const PROG = { playful: ['C', 'Am', 'F', 'G'], wonder: ['C', 'G', 'Am', 'F'], groove: ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7'], shady: ['Am', 'Am', 'F', 'E'], sad: ['Am', 'F', 'C', 'G'],
    tender: ['F', 'C', 'Dm', 'Bb'], tension: ['Am', 'Am', 'Bb', 'Am'], rescue: ['Am', 'F', 'C', 'G'], warm: ['F', 'C', 'G', 'Am'], eerie: ['Am', 'Bb', 'Am', 'Bb'] };
  const rows = [];
  for (let b = 0; b < NBARS; b++) { const md = moodAt(T(b) + 0.01); rows.push([b, 0, 4, PROG[md][b % 4]]); }
  const { chords, chordAt } = makeChords(clock, {
    C: { notes: ['E3', 'G3', 'C4'], bass: 'C2' }, G: { notes: ['D3', 'G3', 'B3'], bass: 'G1' }, Am: { notes: ['E3', 'A3', 'C4'], bass: 'A1' }, F: { notes: ['F3', 'A3', 'C4'], bass: 'F1' },
    Dm: { notes: ['D3', 'F3', 'A3'], bass: 'D2' }, Bb: { notes: ['D3', 'F3', 'Bb3'], bass: 'Bb1' }, E: { notes: ['E3', 'G#3', 'B3'], bass: 'E2' },
    Fmaj7: { notes: ['E3', 'A3', 'C4'], bass: 'F1' }, Em7: { notes: ['D3', 'G3', 'B3'], bass: 'E2' }, Dm7: { notes: ['C3', 'F3', 'A3'], bass: 'D2' }, Cmaj7: { notes: ['E3', 'G3', 'B3'], bass: 'C2' },
  }, rows);
  const runs = [];
  for (let b = 0; b < NBARS; b++) { const md = moodAt(T(b) + 0.01); if (runs.length && runs[runs.length - 1].mood === md) runs[runs.length - 1].to = b + 1; else runs.push({ mood: md, from: b, to: b + 1 }); }

  // THE HEART MONITOR: the signature gimmick. Sam's heart holds a steady 70 bpm whatever happens; each beat
  // is a spike on screen and a soft beep in the song. In the last scene it finally jumps.
  const MONITOR = ['spider', 'haunted', 'coaster', 'title', 'bridge', 'crane', 'ladder', 'choice', 'end'];
  const jump = at('end', 'It jumps');
  const beats = [];
  for (const id of MONITOR) {
    const s = SC[id];
    let t = s.t0 + 0.4;
    while (t < s.t1 - 0.1) {
      const big = id === 'end' && t >= jump - 0.05 && t < jump + 0.75;
      beats.push({ t: +t.toFixed(3), big });
      const bpm = id === 'end' && t >= jump ? 96 : 70;
      t = id === 'end' && t < jump && t + 60 / bpm > jump ? jump : t + 60 / bpm;
    }
  }
  // Leo's two taps on his chest: the planted detail. Two knocks, a quarter-second apart.
  const tapPair = (t) => [+t.toFixed(3), +(t + 0.26).toFixed(3)];
  const taps = [
    ...tapPair(end('leo', 'Two taps on my chest') + 0.06),
    ...tapPair(at('tell', 'Twice') - 0.62),
    ...tapPair(at('choice', 'Twice') - 0.62),
  ];
  const ev = {
    title: SC.title.t0, crane: SC.crane.t0, choice: at('choice', 'The views...'), rescue: SC.rescue.t0, cta: SC.cta.t0,
    crack: at('skate', 'Crack'), unclip: at('crane', 'feel a tug'), jump,
  };
  const markers = {
    title: { t: ev.title, sync: 'av' }, crane: { t: ev.crane, sync: 'av' }, rescue: { t: ev.rescue, sync: 'av' }, cta: { t: ev.cta, sync: 'av' },
    crack: ev.crack, choice: ev.choice, jump: ev.jump, faces: SC.faces.t0, leo: SC.leo.t0,
  };
  const S = {}; TL.scenes.forEach((s) => { S[s.id] = [s.t0, s.t1]; });

  const SCORE = { FPS, FORMAT, STYLE, W, H, SAFE, DURATION, clock, T, BEAT, BAR, S, SC, m, chords, chordAt, runs, vo, beats, taps, MONITOR, ev, markers, at, end, sceneAt, moodAt, TL };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
