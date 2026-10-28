// THE SCRIPT, one spoken line per entry, grouped by scene. Prefix = speaker (no prefix = the narrator):
// F friend · K teacher · B Mr. Black · G Grandpa Sam · T Theo · N Nova. A line ending in "..." gets a
// longer held pause after it. timing.js turns this into timeline.js using the real voice durations.
(function () {
  const SCENES = [
    ['beach', ['You look up from the beach.', 'A plane crosses the sky.', 'You can read the name on its tail.', "And the pilot's face...", 'waving.']],
    ['moon', ['You glance at the Moon.', 'Craters. Mountains. Shadows.', 'No telescope.']],
    ['hill', ['A friend points at a hill two kilometers away.', "F:What's that?", 'You squint.', 'A man.', 'Eating a sandwich.', 'Ham...', 'and too much mustard.']],
    ['plate', ['Your name is Theo.', 'A British driving test asks you to read a number plate...', 'from twenty meters.', 'You?', 'Two kilometers.']],
    ['acuity', ['Normal eyes pick out details about one sixtieth of a degree wide.', 'Yours?', 'A hundred times finer.']],
    ['rule', ["But here's the rule.", 'Your eyes got a hundred times sharper.', 'Your legs did not.', 'You can spot trouble two kilometers away.', 'You still reach it...', 'at human speed.']],
    ['title', ['So what if your eyesight was a hundred times sharper?']],
    ['class', ['Plus: you never need glasses.', "From the back row, you can read the teacher's notes on her desk.", 'Do you?', 'Never.', 'Mostly.', 'Minus: you can read everything else too.', 'Every pore on her nose.', 'Every grey hair...', 'she thinks nobody can see.', 'K:Okay, class. Why is Theo staring at me?']],
    ['stadium', ['At the football match, you sit in the cheapest seat in the stadium.', 'You can still read the stitching on the ball.']],
    ['birds', ['In birdwatching club, everyone shares binoculars.', 'You count the feathers...', 'out loud.']],
    ['fovea', ['The catch?', 'Your sharpest vision only lives in one tiny spot.', "Hold your thumb out at arm's length.", 'That tiny patch?', "That's all your eyes see sharply at once.", 'So your eyes jump.', 'Three or four times a second.', 'Building the rest.', 'Except now, every jump brings in ten thousand times more detail.', 'And your brain...', 'has to sort all of it.', 'Headaches.', 'Every single day.']],
    ['harbor', ['But where it gets really crazy...', 'is the video.', 'A tourist films you at the harbor.', 'You read a tiny warning sign on a ship far out at sea.', 'The clip goes everywhere.']],
    ['message', ['By Friday, a message.', 'Mr. Black.', 'Polite.', 'Rich.', 'B:I have a job.', 'B:Sit in a café. Read a few phones. A few bank cards.', 'B:Nobody gets hurt.', "B:Doesn't that sound easy?"]],
    ['cost', ["And there's a cost.", "You can't switch it off.", 'Peeling paint.', 'Cracks in bridges.', 'Mold in the bread before anyone else can see it.', 'Your eyes never rest.', 'And the world stops looking beautiful.', 'It just looks...', 'detailed.', 'Sunsets turn into dust.', 'Faces turn into maps.']],
    ['grandpa', ["Then there's Grandpa Sam.", 'He used to be a lifeguard on this beach.', 'Now he has macular degeneration.', "It's a real disease.", 'It slowly wipes out the center of your vision, while the edges stay.', 'So you see the most.', 'And he sees the least.']],
    ['cliff', ['Every Sunday, you climb the cliff together.', 'He flies his big red kite.', "It's the one thing he still finds...", 'from the corner of his eye.', "G:I can't see the gulls anymore, Theo.", 'G:So you tell me.', 'And you do.', 'Every wing.', 'Every wave.', 'You make a promise too.', 'T:If I can see it...', "T:it's mine to fix."]],
    ['roof', ['Sunday comes.', "But you're not on the cliff.", "You're on a café roof, two kilometers down the coast.", "Mr. Black's job.", 'Below you, a woman at a cash machine.', 'Her card.', 'Her keys.', 'Her PIN.', "Mr. Black's voice in your ear.", 'B:Four numbers, kid.', "B:Then you're done."]],
    ['sea', ['Then...', 'you see it.', 'Far out past the beach.', 'A small boy.', 'On an orange board.', 'Drifting...', 'fast.', 'The water around him is darker.', 'Flatter.', 'A rip current.', 'Some rips move faster than an Olympic swimmer.', 'Has anyone on the sand noticed?', 'No.', 'The lifeguard is looking the wrong way.', 'Two kilometers.', "Even sprinting, you'd need six minutes.", 'Maybe more.', 'The board slips from his arms.']],
    ['choice', ['B:Theo?', 'B:The numbers. Now.', 'You can see the PIN.', 'You can see the boy.', "You can't have both.", 'The money...', 'or the boy.']],
    ['call', ['You drop the earpiece.', 'T:If I can see it...', "T:it's mine to fix.", 'You call the one person on that beach you trust.', 'T:Grandpa. Kite. Up. Now.', "He doesn't ask why."]],
    ['kite', ['The red kite climbs.', 'T:Left, Grandpa. More.', 'T:Stop. Hold it there.', "Grandpa can't see the boy.", 'But he can see his kite.', 'And now it hangs right above that tiny head.']],
    ['nova', ['You call the lifeguard station.', 'Her name is Nova.', 'T:Follow the red kite.', "T:He's right under it.", 'Nova grabs the rescue board.', "She doesn't fight the current.", 'She rides it out...', 'then cuts sideways.', "And that's the real lesson.", "If a rip ever pulls you out, don't fight it.", 'Swim parallel to the shore.', 'Then come back in.']],
    ['saved', ['Three minutes later, the boy is coughing on the sand.', 'Alive...', 'and furious about his board.', 'The whole beach is cheering for an old man with a kite.']],
    ['police', ['And Mr. Black?', 'You never gave him a single number.', 'You gave the police something better.', 'His car.', 'His plate.', 'His face.', 'All read...', 'from two kilometers away.', 'Cover your PIN, by the way.', "You never know who's watching."]],
    ['sunset', ["That evening, you're back on the cliff.", 'Grandpa grips your shoulder.', 'G:Tell me what you see.', "For the first time in weeks, the world isn't just detail.", "It's gold water.", 'A red kite.', 'And a family hugging a little boy.', 'Beautiful.']],
    ['real', ['Is any of this real?', 'Partly.', 'Macular degeneration is real, and it steals central vision first.', 'Rip currents are real too.', 'But eyes a hundred times sharper?', 'Physics says no.', 'Light spreads out as it passes through your pupil.', 'A normal pupil is a few millimeters wide.', "That's already near the limit.", 'A hundred times sharper?', "You'd need pupils a hundred times wider.", 'Roughly thirty centimeters.', 'Eyes...', 'the size of pizzas.', 'Which, to be fair, would make birdwatching awkward.']],
    ['sting', ['That night, you look up at the Moon.', 'And something on its surface...', 'moves.']],
    ['cta', ['So would you trade normal eyes for pizza-sized ones?', 'What do you think?', 'Tell us in the comments, and tell us which superpower we should do next.', 'Hit like, and subscribe for Part Two.']],
  ];
  // Kokoro voices (kokoro-onnx) and speaking rates per speaker (rate / 175 = speed)
  const VOICES = {
    narrator: { voice: 'am_michael', rate: 166 },
    friend: { voice: 'af_nicole', rate: 175 },
    teacher: { voice: 'bf_emma', rate: 170 },
    black: { voice: 'am_fenrir', rate: 160 },
    grandpa: { voice: 'bm_george', rate: 150 },
    theo: { voice: 'am_puck', rate: 175 },
    nova: { voice: 'af_bella', rate: 175 },
  };
  const WHO = { F: 'friend', K: 'teacher', B: 'black', G: 'grandpa', T: 'theo', N: 'nova' };
  const LINES = [];
  for (const [scene, ls] of SCENES) for (const raw of ls) {
    const m = /^([A-Z]):(.*)$/.exec(raw);
    LINES.push({ scene, who: m ? WHO[m[1]] : 'narrator', text: m ? m[2] : raw });
  }
  const out = { SCENES: SCENES.map(([id]) => id), LINES, VOICES };
  if (typeof module !== 'undefined') module.exports = out; else globalThis.LINES = out;
})();
