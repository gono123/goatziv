// THE SCRIPT, one spoken line per entry, grouped by scene. Prefix = speaker (no prefix = the narrator):
// S Sam · M Mia · L Leo · B Mr. Black · K the zoo keeper. A line ending in "..." gets a longer held pause
// after it. timing.js turns this into timeline.js using the real voice durations.
(function () {
  const SCENES = [
    ['spider', ['A spider drops onto your hand.', "You don't scream.", 'You just...', 'let it walk.', 'Scared?', 'Not even a little.']],
    ['haunted', ['The lights die in the haunted house.', 'A monster leaps from the dark.', 'Everyone shrieks.', 'You tap him on the shoulder.', "S:Excuse me. Where's the exit?"]],
    ['coaster', ['Your roller coaster creeps to the top of the first drop.', 'The whole car is screaming.', 'You?', 'You yawn.', 'And your popcorn...', 'is still in the bag.']],
    ['brain', ['Your name is Sam.', 'Deep in your brain sit two tiny clusters shaped like almonds.', "Together they're called the amygdala.", 'See a snake, and they fire before you even know what you saw.', 'Your heart races.', 'Adrenaline floods your blood.', 'Your muscles tense to run.', "That's most people.", 'You?', 'Nothing.']],
    ['sm', ["This isn't pure fantasy.", 'Scientists studied a real woman known only as S.M.', 'A rare disease damaged both her amygdalae.', 'She handled snakes.', 'In a haunted house, she poked a monster...', 'and the actor jumped.']],
    ['rule', ["But here's your rule.", 'Your fear is gone.', 'Your danger is not.', 'Fear was never the enemy.', 'It was the alarm.', 'And yours...', 'is unplugged.']],
    ['title', ['So what if you had zero fear?', "And what's life actually like without it?"]],
    ['speech', ['Monday.', 'A speech in front of the whole school.', 'Five hundred faces.', 'Your voice never shakes.', 'Mia corners you after.', 'M:How are you not nervous?', 'Plus: exams feel like crosswords.', 'No sweaty hands.', 'No blank mind.']],
    ['space', ['Minus: personal space.', "Most people stand roughly an arm's length from a stranger.", 'You?', 'About half that.', 'People keep stepping back.', 'Leo tugs your sleeve.', "L:Mate. You're doing it again."]],
    ['zoo', ['At the zoo, you walk straight to the reptile house.', 'The keeper lets you hold the python.', 'Then begs you to stop.', 'K:Please. Put. The python. Down.']],
    ['skate', ['The catch?', 'Your body still breaks.', 'You try the biggest ramp at the skate park.', 'First go.', 'No wobble in your head...', 'but plenty in your knees.', 'Crack.', 'A broken wrist.', 'A bone needs around six weeks to knit back together.', 'Fearless or not.']],
    ['bridge', ['But where it gets really crazy...', 'is the glass bridge.', 'Hundreds of meters above a valley.', 'Adults crawl across on their hands.', 'You stroll across eating an apple.', 'Someone films it.', 'By morning...', 'two million views.']],
    ['message', ['Then a message arrives.', 'Mr. Black.', 'He runs the biggest stunt channel online.', 'B:We pay. Big.', 'B:Why waste a gift like yours?']],
    ['cost', ["And there's a cost.", 'A roller coaster is fun for a reason.', 'Your body screams danger.', "Your brain knows you're safe.", 'That clash is the rush.', 'You only get half.', 'No thrill.', 'No spark.', 'Just...', 'a ride.']],
    ['faces', ['And the worst part?', "The amygdala doesn't only make fear.", 'It helps you spot fear in other faces.', 'Without it, a frightened face looks...', 'blank.', 'Mia trembles before her final exam.', 'You tell her she looks totally fine.', "She doesn't speak to you for a week.", 'How do you comfort someone...', "when you can't see them hurting?", 'So you make yourself a rule.', "S:I can't feel it. So I have to think it."]],
    ['leo', ["Then there's Leo.", 'Your best friend since you were six.', 'Leo is scared of everything.', 'Dogs.', 'Thunder.', 'The dark.', 'Above all, heights.', "He won't stand on a chair to change a light bulb.", 'Years ago, he made you a deal.', "L:Two taps on my chest means I'm scared.", "L:Don't laugh.", 'You promised.', 'Two taps...', 'and you stop.']],
    ['tell', ['When you tell him about Mr. Black, he goes quiet.', "You can't read his face, of course.", 'But he taps.', 'Twice.', "L:Sam. Please don't."]],
    ['crane', ['You go anyway.', 'An old crane at the docks.', 'A steel beam, forty meters up.', 'Thirty centimeters wide.', 'Cameras everywhere.', 'Mr. Black clips a safety line to your belt.', 'The stream goes live.', 'Then you feel a tug.', "He's unclipped it.", 'B:More real this way, kid.', "You're already halfway out."]],
    ['ladder', ['Then the ladder rattles.', 'Leo?', 'He followed you.', "He's climbing.", 'L:Sam? Come back!', 'Ten meters.', 'Twenty.', 'Thirty.', 'Then he stops.', 'Frozen.', 'The wind up here is far stronger than on the ground.', 'A fall from forty meters takes under three seconds.', "And Leo's fingers...", 'are slipping.']],
    ['choice', ['You look at his face.', "You can't read it.", "To you, it's just...", 'a face.', 'Mr. Black hisses through your earpiece.', 'B:What are you waiting for? A million people are watching.', 'Ahead, the end of the beam.', 'The views.', 'The money.', 'Behind you, your best friend.', 'The views...', 'or Leo.', 'Then Leo lifts one shaking hand.', 'And taps his chest.', 'Twice.']],
    ['rescue', ['You turn around.', "You don't rush.", "You can't feel it...", 'so you think it.', 'Step. Breathe. Step.', 'You crouch beside the ladder.', 'S:Leo. Look at me. Can you hear me?', 'S:Three points of contact.', 'S:Two hands and a foot. Or two feet and a hand.', 'S:Always three.', "It's the oldest rule in climbing.", 'You talk him down.', 'One rung at a time.', 'Your calm becomes his calm.', 'The only steady thing in the sky...', 'is your voice.']],
    ['truth', ['At the bottom, he collapses in the dust.', 'Then you pick up the camera Mr. Black dropped.', 'Still live.', 'You point it at the loose safety line.', 'S:He unclipped this. On purpose.', "You don't shout.", "You don't shove him.", 'You just tell the truth.', 'By evening, his channel is gone.']],
    ['lesson', ['And remember:', 'no video is worth a hospital bed.', 'If someone asks you to drop your safety gear for views...', "they're not the one who'd fall."]],
    ['brave', ['The comments fill with one name.', 'Leo.', 'Leo, who climbed thirty meters while terrified.', "Because that's brave.", 'Not feeling nothing...', 'feeling everything, and climbing anyway.']],
    ['end', ['Later he asks how you stayed so calm.', 'You shrug.', "S:I can't feel it. So I have to think it.", 'He grins.', "L:Then I'll feel it for both of us.", "You still can't see the fear on his face.", 'But you can see that grin.', "And when he hugs you, your heart does something it hasn't done in years.", 'It jumps.']],
    ['sting', ['That night, an envelope slides under your door.', 'No stamp.', 'No name.', 'One line.', "We know what you can't feel. We need you."]],
    ['cta', ['So what would you do with zero fear?', "Tell us the first scary thing you'd try in the comments.", 'And if you got chills when Leo tapped twice...', 'hit like, and subscribe for Part Two.']],
  ];
  // Kokoro voices (kokoro-onnx) and speaking rates per speaker (rate / 175 = speed)
  const VOICES = {
    narrator: { voice: 'am_michael', rate: 166 },
    sam: { voice: 'am_puck', rate: 172 },
    mia: { voice: 'af_bella', rate: 175 },
    leo: { voice: 'bm_fable', rate: 172 },
    black: { voice: 'am_fenrir', rate: 160 },
    keeper: { voice: 'bf_emma', rate: 160 },
  };
  const WHO = { S: 'sam', M: 'mia', L: 'leo', B: 'black', K: 'keeper' };
  const LINES = [];
  for (const [scene, ls] of SCENES) for (const raw of ls) {
    const m = /^([A-Z]):(.*)$/.exec(raw);
    LINES.push({ scene, who: m ? WHO[m[1]] : 'narrator', text: m ? m[2] : raw });
  }
  const out = { SCENES: SCENES.map(([id]) => id), LINES, VOICES };
  if (typeof module !== 'undefined') module.exports = out; else globalThis.LINES = out;
})();
