// Measures every narration line: synthesizes it once (cached in out/.vo-cache) and writes timing.js,
// the length of each line in seconds, so score.js can lay the film out around the real voice.
//   node make-timing.js
const fs = require('fs');
const path = require('path');
process.env.PYTHONPATH = [path.join(__dirname, 'tts'), process.env.PYTHONPATH].filter(Boolean).join(path.delimiter);
const Voice = require('./engine/audio/voice');
const { SCENES, VOICE } = require('./lines');

const flat = SCENES.flatMap((s) => s.lines.map(([text]) => ({ at: 0, text, voice: VOICE })));
const vo = Voice.speak(flat, { out: path.join(__dirname, 'out'), engine: 'kokoro', save: false });
if (vo.engine !== 'kokoro') throw new Error(`expected the kokoro voice, got ${vo.engine}`);
const dur = vo.lines.map((l) => +(l.end - l.t).toFixed(3));
fs.writeFileSync(path.join(__dirname, 'timing.js'),
  '// written by make-timing.js: the spoken length of every line in lines.js, in order\n' +
  `(function () { const D = ${JSON.stringify(dur)}; if (typeof module !== 'undefined') module.exports = D; else globalThis.VO_DUR = D; })();\n`);
console.log(`timing.js  ${dur.length} lines  ${dur.reduce((a, b) => a + b, 0).toFixed(1)}s of speech`);
