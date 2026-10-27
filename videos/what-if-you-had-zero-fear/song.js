// THE SOUND: the narration (a deep Kokoro storyteller), a score that follows each scene's mood, and
// a sound on every hit in score.js. The music ducks under the voice.
//   node song.js      (STEMS=1 writes stems, LUFS=-14 sets loudness)
const path = require('path');
process.env.PYTHONPATH = [path.join(__dirname, 'tts'), process.env.PYTHONPATH].filter(Boolean).join(path.delimiter);
const { SR, Bus, reverb } = require('./engine/audio/dsp');
const I = require('./engine/audio/instruments');
const MIX = require('./engine/audio/mix');
const Voice = require('./engine/audio/voice');
const sc = require('./score');
const { T, BEAT, BAR, DURATION, m, ev, chordAt, MOOD, sceneAt, L, SC } = sc;

const N = Math.ceil(DURATION * SR);
const bus = () => new Bus(N);
const pad = bus(), bass = bus(), keys = bus(), drums = bus(), strings = bus(), fx = bus(), verb = bus();
const rng = ((s) => () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296))(7);

// ---------- the score: one bar at a time, in the mood of the scene it falls in ----------
const BED = {
  // pad gain, bass?, drums ('lofi' | 'pulse' | 'heart' | null), keys ('marimba' | 'box' | 'pizz' | 'epiano' | null), strings?
  play: [0.5, true, 'lofi', 'marimba', false],
  spooky: [0.6, true, null, 'pizz', false],
  curious: [0.55, true, null, 'epiano', false],
  still: [0.45, false, null, null, false],
  title: [0.7, true, null, null, true],
  life: [0.5, true, 'lofi', 'epiano', false],
  wonder: [0.6, true, null, 'box', true],
  dark: [0.6, true, 'pulse', null, false],
  sad: [0.5, false, null, 'box', true],
  tender: [0.5, false, null, 'box', false],
  tension: [0.65, true, 'heart', null, true],
  silence: [0, false, null, null, false],
  rise: [0.6, true, null, null, true],
  warm: [0.6, true, 'lofi', 'box', true],
  mystery: [0.5, true, null, 'box', false],
  end: [0.55, true, 'lofi', 'marimba', false],
};
const nBars = Math.ceil(DURATION / BAR);
for (let b = 0; b < nBars; b++) {
  const t0 = T(b);
  if (t0 > DURATION - 0.5) break;
  const mood = MOOD[sceneAt(t0 + 0.01)];
  const [pg, hasBass, dr, kk, str] = BED[mood];
  const c = chordAt(t0 + 0.01);
  if (pg > 0) for (const n of c.notes) { const { L: l, R: r } = I.padNote(n, BAR + 0.4, { cutoff: 1400, attack: 0.6, release: 1.2 }); pad.addStereo(l, r, t0, 0.07 * pg); }
  if (hasBass) bass.addMono(I.bass(c.bass + 12, BAR * 0.9, { bright: 0.2 }), t0, 0.35);
  if (str) for (const n of c.notes) { const { L: l, R: r } = I.strings(n + 12, BAR + 0.2, { attack: 0.5, release: 1 }); strings.addStereo(l, r, t0, 0.05); }
  for (let beat = 0; beat < 4; beat++) {
    const tb = T(b, beat);
    if (dr === 'lofi') {
      if (beat === 0 || beat === 2.5) drums.addMono(I.kick({ punch: 0.6 }), tb, 0.35);
      if (beat === 1 || beat === 3) drums.addMono(I.snare({ tone: 0.3, decay: 0.12 }), tb, 0.16);
      drums.addMono(I.hat(false, b * 4 + beat), tb, 0.06); drums.addMono(I.hat(false, b * 4 + beat + 99), tb + BEAT / 2, 0.04);
      if (beat === 2) drums.addMono(I.kick({ punch: 0.6 }), tb + BEAT / 2, 0.25);
    } else if (dr === 'pulse') {
      drums.addMono(I.kick({ punch: 0.4, tail: 0.6 }), tb, beat % 2 ? 0.18 : 0.3);
    } else if (dr === 'heart' && (beat === 0 || beat === 2)) {
      drums.addMono(I.heartbeat(), tb, 0.55);
    }
    if (kk) {
      const n = c.notes[(beat + b) % c.notes.length] + 12;
      if (kk === 'marimba') { keys.addMono(I.marimba(n), tb, 0.14, -0.2); keys.addMono(I.marimba(n + (beat % 2 ? 7 : 12)), tb + BEAT / 2, 0.09, 0.2); }
      else if (kk === 'box') { const x = I.musicBox(n + 12, { decay: 1.2 }); keys.addMono(x, tb, 0.1, 0.15); verb.addMono(x, tb, 0.08); }
      else if (kk === 'pizz') { if (beat % 2 === 0) keys.addMono(I.pizz(n - 12), tb, 0.22); }
      else if (kk === 'epiano' && beat % 2 === 0) keys.addMono(I.epiano(n, BEAT * 1.6, { decay: 0.8 }), tb, 0.1);
    }
  }
}
// the turnaround: a slow string swell when Sam turns around, a timpani at the crane
const { L: swL, R: swR } = I.strings(m('A3'), 3.2, { attack: 1.8, release: 1 });
strings.addStereo(swL, swR, ev.turn - 1.6, 0.12);
fx.addMono(I.timpani(m('A1'), { decay: 1.4 }), SC.crane.t0 + 0.4, 0.5);

// ---------- the hits ----------
const hit = (x, t, g = 0.5, pan = 0) => fx.addMono(x, t, g, pan);
hit(I.pop(900), ev.spiderLand, 0.35);
hit(I.tvClick(), ev.lightsOut, 0.5);
hit(I.subBoom(0.9, 90, 40), ev.monster, 0.6); hit(I.crash(3), ev.monster, 0.3); hit(I.bwomp(), ev.monster, 0.3);
hit(I.woodTick(1.4), ev.tapShoulder, 0.35); hit(I.woodTick(1.4), ev.tapShoulder + 0.2, 0.3);
hit(I.noiseSweep(1.2, 6000, 3000, { q: 4 }), ev.snake, 0.12, -0.4);
hit(I.heartbeat(), ev.heart, 0.6); hit(I.heartbeat(), ev.heart + 0.55, 0.5);
hit(I.thud(70, 0.3), ev.nothing, 0.4);
hit(I.tvClick(), ev.unplug, 0.6); hit(I.bwomp(), ev.unplug + 0.03, 0.3);
hit(I.subBoom(1.4, 80, 34), ev.title, 0.55); hit(I.crash(5), ev.title, 0.35); hit(I.thud(80, 0.12), ev.title, 0.5);
// applause after the speech
for (let k = 0; k < 60; k++) hit(I.clap({ decay: 0.08 }), ev.applause + rng() * 1.6, 0.05 + rng() * 0.04, rng() * 1.6 - 0.8);
for (let k = 0; k < 4; k++) hit(I.pop(1200 + k * 200), L('zoo', 3).t + k * ((L('zoo', 3).end - L('zoo', 3).t) / 4), 0.25);
hit(I.thwack(), ev.crack, 0.7); hit(I.woodTick(2.2), ev.crack + 0.01, 0.5); hit(I.subBoom(0.5, 120, 50), ev.crack, 0.4);
for (let k = 0; k < 10; k++) hit(I.pop(1000 + k * 140), ev.views + k * 0.16, 0.12);
hit(I.ting(m('E6')), ev.views + 1.6, 0.3);
hit(I.ting(m('A5')), ev.msg, 0.35);
hit(I.noiseSweep(1, 200, 2000, { q: 2 }), ev.blank - 0.4, 0.08);
for (const tt of [...ev.dealTaps, ...ev.tellTaps]) hit(I.heartbeat(), tt, 0.55);
hit(I.ting(m('C6')), ev.live, 0.25);
hit(I.thwack(), ev.tug, 0.45); hit(I.subBoom(0.6, 70, 40), ev.tug, 0.3);
for (let k = 0; k < 8; k++) hit(I.woodTick(0.6 + rng() * 0.3), ev.rattle + k * 0.09, 0.25, 0.3);
for (const tt of ev.climbMarks) hit(I.timpani(m('E2'), { decay: 0.6 }), tt, 0.35);
hit(I.noiseSweep(2.2, 400, 1600, { q: 1.5, pink: true }), L('climb', 6).t, 0.18);
hit(I.noiseSweep(0.8, 3000, 600, { q: 3 }), ev.slip, 0.15);
// the final taps: everything else is silent; two heartbeats you can feel
for (const tt of ev.finalTaps) { hit(I.heartbeat(), tt, 0.9); hit(I.thud(55, 0.25), tt, 0.5); }
hit(I.noiseSweep(0.5, 800, 3000, { q: 2 }), ev.turn - 0.1, 0.12);
for (const tt of ev.steps) hit(I.woodTick(0.9), tt, 0.3);
hit(I.thud(70, 0.2), ev.gone, 0.5); hit(I.crash(9), ev.gone, 0.3);
hit(I.heartbeat(), ev.jump, 0.8); hit(I.boing(), ev.jump + 0.05, 0.25);
hit(I.paperFwip(0.8), ev.envelope, 0.4);
for (let k = 0; k < 44; k++) hit(I.woodTick(1.8 + rng() * 0.4), ev.note + 0.3 + k / 18, 0.08);
hit(I.pop(1600), ev.endCard - 0.5, 0.25); hit(I.ting(m('G5')), ev.endCard, 0.3); hit(I.crash(11), ev.endCard, 0.2);

// ---------- the voice, and the music under it ----------
const vo = Voice.speak(sc.vo, { out: path.join(__dirname, 'out'), engine: 'kokoro', length: DURATION });
if (vo.engine !== 'kokoro') throw new Error(`expected the kokoro voice, got ${vo.engine}`);
const music = [pad, bass, keys, drums, strings];
MIX.duck(music, vo.bus, { depth: 0.5 });
// a true silence around the final taps
for (const b of [pad, bass, keys, drums, strings, verb]) MIX.gate(b, SC.taps.t0 + 0.2, ev.finalTaps[1] + 1.2);

const room = reverb(verb, { room: 0.7, damp: 0.4 });
const stems = { pad, bass, keys, drums, strings, fx, voice: vo.bus, verb: room };
const GAIN = { pad: 2.4, bass: 0.8, keys: 1.2, drums: 0.8, strings: 2.2, fx: 1, voice: 1.9, verb: 0.8 };
const mix = MIX.mixdown(stems, GAIN, { stemDir: process.env.STEMS ? path.join(__dirname, 'out') : null });
MIX.highpass(mix, 30);
MIX.fadeOut(mix, DURATION - 1.5, DURATION);
const res = MIX.master(mix, 0.8, undefined, { lufs: process.env.LUFS ? +process.env.LUFS : -14 });
MIX.writeWav(path.join(__dirname, 'out', 'music.wav'), mix);
console.log(`out/music.wav  ${DURATION.toFixed(1)}s  ${res.lufs.toFixed(1)} LUFS  voice: ${vo.engine}`);
