// THE SONG: a narrated film, so the music is a bed under the voice. Every sound comes from score.js:
// one clock (84 BPM), one chord table, mood runs per scene, a glassy ting on every lens pop, and hits on
// the scene cuts. The music ducks under the voice.   node song.js   (STEMS=1 writes stems)
const path = require('path');
const { SR, Bus, reverb } = require('./engine/audio/dsp');
const I = require('./engine/audio/instruments');
const MIX = require('./engine/audio/mix');
const Genre = require('./engine/audio/genres');
const Voice = require('./engine/audio/voice');
const sc = require('./score');
const { T, BEAT, BAR, DURATION, m, ev, clock, chordAt, runs, at, end } = sc;

const N = Math.ceil(DURATION * SR);
const bus = () => new Bus(N);
const buses = { drums: bus(), bass: bus(), pad: bus(), keys: bus() };
const lead = bus(), fx = bus(), verb = bus();

const pads = (from, to, { cutoff = 1400, gain = 0.07, oct = 12 } = {}) => {
  for (let b = from; b < to; b++) { const c = chordAt(T(b) + 0.01); for (const n of c.notes) { const { L, R } = I.padNote(n + oct, BAR * 1.05, { cutoff, attack: 0.6, release: 0.8 }); buses.pad.addStereo(L, R, T(b), gain); } }
};
const subRoots = (from, to, gain = 0.35) => { for (let b = from; b < to; b++) { const c = chordAt(T(b) + 0.01); buses.bass.addMono(I.bass(c.bass + 12, BAR * 0.95, { bright: 0.1, sub: 1 }), T(b), gain); } };
// an arpeggio through the chord on a music box (or guitar), sparse: every 8th, or every quarter
const ARP = [0, 1, 2, 1, 2, 1, 0, 1];
const arp = (from, to, { inst = 'box', gain = 0.12, every = 1, oct = 24, skipOdd = false } = {}) => {
  for (let b = from; b < to; b++) {
    if (skipOdd && b % 2) continue;
    const c = chordAt(T(b) + 0.01);
    for (let k = 0; k < 8; k += every) {
      const n = c.notes[ARP[k] % c.notes.length] + oct, t = T(b, k / 2);
      const x = inst === 'box' ? I.musicBox(n) : I.guitar(n - 12, BEAT * 1.4, { bright: 0.5, sustain: 0.996, seed: b * 8 + k });
      lead.addMono(x, t, gain, (k % 2 ? 0.25 : -0.25)); verb.addMono(x, t, gain * 0.8);
    }
  }
};

for (const r of runs) {
  const { mood, from, to } = r;
  if (mood === 'wonder') { pads(from, to, { cutoff: 1800, gain: 0.06 }); arp(from, to, { gain: 0.1 }); subRoots(from, to, 0.22); }
  if (mood === 'groove') { Genre.play('lofi', { clock, from, to, chordAt, buses, gain: 0.75 }); pads(from, to, { cutoff: 1100, gain: 0.035 }); }
  if (mood === 'shady') { pads(from, to, { cutoff: 800, gain: 0.07, oct: 0 }); subRoots(from, to, 0.35); for (let b = from; b < to; b++) for (let k = 0; k < 4; k++) fx.addMono(I.woodTick(k % 2 ? 1.0 : 1.3), T(b, k), 0.12, 0.3); }
  if (mood === 'sad') { pads(from, to, { cutoff: 1000, gain: 0.07 }); arp(from, to, { gain: 0.09, every: 2 }); }
  if (mood === 'tender') { pads(from, to, { cutoff: 1500, gain: 0.05 }); arp(from, to, { inst: 'guitar', gain: 0.5, every: 1, oct: 12 }); arp(from, to, { gain: 0.07, every: 4, skipOdd: true }); subRoots(from, to, 0.2); }
  if (mood === 'tension') {
    pads(from, to, { cutoff: 650, gain: 0.08, oct: 0 }); subRoots(from, to, 0.4);
    for (let b = from; b < to; b++) for (let k = 0; k < 4; k += 2) { buses.drums.addMono(I.heartbeat(), T(b, k), 0.5); }
    for (let b = from; b < to; b++) for (let k = 0; k < 8; k++) fx.addMono(I.woodTick(1.6), T(b, k / 2), 0.05, 0.4);
  }
  if (mood === 'rescue') {
    Genre.play('orchestral', { clock, from, to, chordAt, buses, gain: 0.85 });
    for (let b = from + 4; b < to; b++) { for (let k = 0; k < 4; k++) buses.drums.addMono(I.kick({ tail: 0.25, punch: 0.6 }), T(b, k), 0.35); buses.drums.addMono(I.snare({ tone: 0.4, snap: 0.5, decay: 0.12 }), T(b, 1), 0.18); buses.drums.addMono(I.snare({ tone: 0.4, snap: 0.5, decay: 0.12 }), T(b, 3), 0.18); }
    arp(from + 2, to, { gain: 0.06, every: 2 });
  }
  if (mood === 'warm') { Genre.play('orchestral', { clock, from, to, chordAt, buses, gain: 0.7, drums: false }); arp(from, to, { gain: 0.1 }); subRoots(from, to, 0.2); }
  if (mood === 'eerie') { pads(from, to, { cutoff: 700, gain: 0.08, oct: 0 }); for (let b = from; b < to; b++) { const x = I.bell(m('B5') + 0, 2.5, 3, 3.5); lead.addMono(x, T(b, 1), 0.06, 0.3); verb.addMono(x, T(b, 1), 0.12); } }
}

// the lens tings: a glass bell on each pop
for (const l of sc.lens) { const x = I.bell(2637, 0.7, 1.2, 2.76); fx.addMono(x, l.t, 0.16, 0.2); verb.addMono(x, l.t, 0.14); }
// hits on the cuts (in the breath between lines)
fx.addMono(I.thud(70, 0.25), ev.title, 0.7); fx.addMono(I.subBoom(1.4, 90, 34), ev.title, 0.4); fx.addMono(I.crash(3), ev.title, 0.18);
fx.addMono(I.subBoom(1.6, 80, 30), ev.choice, 0.55); fx.addMono(I.thud(55, 0.3), ev.choice, 0.6);
fx.addMono(I.pop(900), ev.kite, 0.5); fx.addMono(I.noiseSweep(1.2, 400, 6000, { q: 1.5 }), ev.kite + 0.05, 0.08);
fx.addMono(I.crash(7), ev.saved, 0.25); buses.drums.addMono(I.kick({ punch: 1.1 }), ev.saved, 0.7);
fx.addMono(I.thud(80, 0.2), ev.cta, 0.6); fx.addMono(I.pop(1400), ev.cta, 0.4);
// the earpiece drops: a little clatter
fx.addMono(I.woodTick(1.8), ev.drop + 0.7, 0.3); fx.addMono(I.woodTick(2.1), ev.drop + 0.85, 0.2);

// the held breath: the music stops for "The money... or the boy."
const gate0 = ev.split - 0.2, gate1 = end('choice', 'or the boy') + 0.5;
const music = [buses.drums, buses.bass, buses.pad, buses.keys, lead, verb];
for (const b of music) MIX.gate(b, gate0, gate1);

// the voiceover, and the music ducks under it
const vo = Voice.speak(sc.vo, { out: path.join(__dirname, 'out'), length: DURATION, engine: 'espeak-ng' });
MIX.duck([buses.drums, buses.bass, buses.pad, buses.keys, lead], vo.bus, { depth: 0.6 });

const room = reverb(verb, { room: 0.75, damp: 0.4 });
MIX.gate(room, gate0, gate1);
const stems = { ...buses, lead, fx, voice: vo.bus, verb: room };
const GAIN = { drums: 0.75, bass: 0.7, pad: 1, keys: 0.9, lead: 0.9, fx: 0.9, voice: 2.2, verb: 0.35 };
const mix = MIX.mixdown(stems, GAIN, { stemDir: process.env.STEMS ? path.join(__dirname, 'out') : null });
MIX.highpass(mix, 30);
MIX.fadeOut(mix, DURATION - 1.5, DURATION);
const res = MIX.master(mix, 0.8, undefined, { lufs: process.env.LUFS ? +process.env.LUFS : -14 });
MIX.writeWav(path.join(__dirname, 'out', 'music.wav'), mix);
console.log(`out/music.wav  ${DURATION.toFixed(1)}s  ${res.lufs.toFixed(1)} LUFS  voice: ${vo.engine}`);
