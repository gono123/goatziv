// WHAT IF YOUR EYESIGHT WAS 100x SHARPER? (16:9, ~6 min). The voiceover's measured line times
// (timeline.js, from timing.js) are the spine: every scene, lens pop, hit and music section is placed
// from them, so the voice, the picture and the score cannot drift apart.
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

  // scenes and lines
  const SC = {}; TL.scenes.forEach((s) => { SC[s.id] = s; });
  const sceneAt = (t) => TL.scenes.find((s) => t >= s.t0 && t < s.t1) || TL.scenes[TL.scenes.length - 1];
  // the start (or end) of the first line in a scene containing `text`
  const at = (scene, text) => { const l = TL.lines.find((x) => x.scene === scene && x.text.includes(text)); if (!l) throw new Error(`no line "${text}" in ${scene}`); return l.at; };
  const end = (scene, text) => { const l = TL.lines.find((x) => x.scene === scene && x.text.includes(text)); return l.at + l.dur; };
  const vo = TL.lines.map((l) => ({ at: l.at, text: l.text, who: l.who, voice: VOICES[l.who].voice, rate: VOICES[l.who].rate }));

  // the moods of the music, per scene
  const MOOD = { beach: 'wonder', moon: 'wonder', hill: 'wonder', plate: 'wonder', acuity: 'wonder', rule: 'wonder', title: 'wonder',
    class: 'groove', stadium: 'groove', birds: 'groove', fovea: 'groove', harbor: 'groove', message: 'shady',
    cost: 'sad', grandpa: 'tender', cliff: 'tender', roof: 'tension', sea: 'tension', choice: 'tension',
    call: 'rescue', kite: 'rescue', nova: 'rescue', saved: 'warm', police: 'warm', sunset: 'warm',
    real: 'groove', sting: 'eerie', cta: 'groove' };
  const moodAt = (t) => MOOD[sceneAt(t).id];
  const NBARS = Math.ceil(DURATION / BAR) + 1;
  const PROG = { wonder: ['C', 'G', 'Am', 'F'], groove: ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7'], shady: ['Am', 'Am', 'F', 'E'], sad: ['Am', 'F', 'C', 'G'],
    tender: ['F', 'C', 'Dm', 'Bb'], tension: ['Am', 'Am', 'Bb', 'Am'], rescue: ['Am', 'F', 'C', 'G'], warm: ['F', 'C', 'G', 'Am'], eerie: ['Am', 'Bb', 'Am', 'Bb'] };
  const rows = [];
  for (let b = 0; b < NBARS; b++) { const md = moodAt(T(b) + 0.01); rows.push([b, 0, 4, PROG[md][b % 4]]); }
  const { chords, chordAt } = makeChords(clock, {
    C: { notes: ['E3', 'G3', 'C4'], bass: 'C2' }, G: { notes: ['D3', 'G3', 'B3'], bass: 'G1' }, Am: { notes: ['E3', 'A3', 'C4'], bass: 'A1' }, F: { notes: ['F3', 'A3', 'C4'], bass: 'F1' },
    Dm: { notes: ['D3', 'F3', 'A3'], bass: 'D2' }, Bb: { notes: ['D3', 'F3', 'Bb3'], bass: 'Bb1' }, E: { notes: ['E3', 'G#3', 'B3'], bass: 'E2' },
    Fmaj7: { notes: ['E3', 'A3', 'C4'], bass: 'F1' }, Em7: { notes: ['D3', 'G3', 'B3'], bass: 'E2' }, Dm7: { notes: ['C3', 'F3', 'A3'], bass: 'D2' }, Cmaj7: { notes: ['E3', 'G3', 'B3'], bass: 'C2' },
  }, rows);
  // contiguous mood runs in bars: [{ mood, from, to }]
  const runs = [];
  for (let b = 0; b < NBARS; b++) { const md = moodAt(T(b) + 0.01); if (runs.length && runs[runs.length - 1].mood === md) runs[runs.length - 1].to = b + 1; else runs.push({ mood: md, from: b, to: b + 1 }); }

  // LENS pops: the signature gimmick. A magnifier opens on a far-away detail, with a glassy ting.
  const lens = [
    { id: 'plane', t: at('beach', 'read the name') }, { id: 'pilot', t: at('beach', 'waving') },
    { id: 'moon', t: at('moon', 'Craters') }, { id: 'man', t: at('hill', 'A man') }, { id: 'mustard', t: at('hill', 'mustard') },
    { id: 'plate', t: at('plate', 'You?') }, { id: 'notes', t: at('class', 'read the teacher') }, { id: 'pores', t: at('class', 'pore') },
    { id: 'ball', t: at('stadium', 'stitching') }, { id: 'feathers', t: at('birds', 'count the feathers') }, { id: 'sign', t: at('harbor', 'warning sign') },
    { id: 'pin', t: at('roof', 'Her PIN') }, { id: 'boy', t: at('sea', 'A small boy') }, { id: 'moon2', t: at('sting', 'something') },
  ];
  // hits: transients on scene cuts, in the breath between lines (never on a word)
  const ev = {
    title: SC.title.t0, choice: SC.choice.t0, kite: SC.kite.t0, saved: SC.saved.t0, cta: SC.cta.t0,
    drop: at('call', 'drop the earpiece'), split: at('choice', 'The money'),
  };
  const markers = {
    title: { t: ev.title, sync: 'av' }, choice: { t: ev.choice, sync: 'av' }, kite: { t: ev.kite, sync: 'av' },
    saved: { t: ev.saved, sync: 'av' }, cta: { t: ev.cta, sync: 'av' }, boy: lens.find((l) => l.id === 'boy').t, rule: SC.rule.t0, cost: SC.cost.t0, real: SC.real.t0,
  };
  const S = {}; TL.scenes.forEach((s) => { S[s.id] = [s.t0, s.t1]; });

  const SCORE = { FPS, FORMAT, STYLE, W, H, SAFE, DURATION, clock, T, BEAT, BAR, S, SC, m, chords, chordAt, runs, vo, lens, ev, markers, at, end, sceneAt, moodAt, TL };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
