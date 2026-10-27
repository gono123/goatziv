// THE WORDS: the narration of scripts/what-if-you-had-zero-fear.md, split into scenes and lines.
// Each line is [text, who?, pauseAfter?]. `who` is whose line it is (the narrator reads every line;
// the speaker's mouth moves and the caption takes their colour). score.js lays the lines out in time
// from their measured lengths (timing.js, written by `node make-timing.js`).
(function () {
  const N = 'narrator';
  const SCENES = [
    { id: 'spider', lines: [['A spider drops onto your hand.'], ["You don't scream."], ['You just... let it walk.', N, 0.6], ['Scared? Not even a little.']] },
    { id: 'haunted', lines: [['The lights die in the haunted house.'], ['A monster leaps from the dark.'], ['Everyone shrieks.'], ['You tap him on the shoulder.'], ["Excuse me. Where's the exit?", 'sam']] },
    { id: 'coaster', lines: [['Your roller coaster creeps to the top of the first drop.'], ['The whole car is screaming.'], ['You? You yawn.', N, 0.5], ['And your popcorn... is still in the bag.']] },
    { id: 'brain', lines: [['Your name is Sam.', N, 0.6], ['Deep in your brain sit two tiny clusters shaped like almonds.'], ["Together they're called the amygdala."], ['See a snake, and they fire before you even know what you saw.'], ['Your heart races.'], ['Adrenaline floods your blood.'], ['Your muscles tense to run.'], ["That's most people."], ['You? Nothing.', N, 0.6]] },
    { id: 'sm', lines: [["This isn't pure fantasy."], ['Scientists studied a real woman known only as S.M.'], ['A rare disease damaged both her amygdalae.'], ['She handled snakes.'], ['In a haunted house, she poked a monster... and the actor jumped.']] },
    { id: 'rule', lines: [["But here's your rule."], ['Your fear is gone.'], ['Your danger is not.', N, 0.6], ['Fear was never the enemy.'], ['It was the alarm.'], ['And yours... is unplugged.']] },
    { id: 'title', lines: [['So what if you had zero fear?', N, 0.4], ["And what's life actually like without it?"]] },
    { id: 'speech', lines: [['Monday. A speech in front of the whole school.'], ['Five hundred faces.'], ['Your voice never shakes.'], ['Mia corners you after.'], ['How are you not nervous?', 'mia']] },
    { id: 'exams', lines: [['Plus: exams feel like crosswords.'], ['No sweaty hands. No blank mind.']] },
    { id: 'space', lines: [['Minus: personal space.'], ["Most people stand roughly an arm's length from a stranger."], ['You? About half that.'], ['People keep stepping back.'], ['Leo tugs your sleeve.'], ["Mate. You're doing it again.", 'leo']] },
    { id: 'zoo', lines: [['At the zoo, you walk straight to the reptile house.'], ['The keeper lets you hold the python.'], ['Then begs you to stop.'], ['Please. Put. The python. Down.', 'keeper']] },
    { id: 'skate', lines: [['The catch? Your body still breaks.', N, 0.5], ['You try the biggest ramp at the skate park.'], ['First go.'], ['No wobble in your head... but plenty in your knees.', N, 0.3], ['Crack.', N, 0.5], ['A broken wrist.'], ['A bone needs around six weeks to knit back together.'], ['Fearless or not.']] },
    { id: 'bridge', lines: [['But where it gets really crazy... is the glass bridge.'], ['Hundreds of meters above a valley.'], ['Adults crawl across on their hands.'], ['You stroll across eating an apple.'], ['Someone films it.'], ['By morning... two million views.']] },
    { id: 'black', lines: [['Then a message arrives.'], ['Mr. Black.'], ['He runs the biggest stunt channel online.'], ['We pay. Big. Why waste a gift like yours?', 'black']] },
    { id: 'cost', lines: [["And there's a cost."], ['A roller coaster is fun for a reason.'], ['Your body screams danger.'], ["Your brain knows you're safe."], ['That clash is the rush.'], ['You only get half.'], ['No thrill. No spark. Just... a ride.', N, 0.6]] },
    { id: 'faces', lines: [['And the worst part?', N, 0.4], ["The amygdala doesn't only make fear."], ['It helps you spot fear in other faces.'], ['Without it, a frightened face looks... blank.'], ['Mia trembles before her final exam.'], ['You tell her she looks totally fine.'], ["She doesn't speak to you for a week."], ["How do you comfort someone... when you can't see them hurting?", N, 0.6]] },
    { id: 'rule2', lines: [['So you make yourself a rule.'], ["I can't feel it. So I have to think it.", 'sam', 0.6]] },
    { id: 'leo', lines: [["Then there's Leo."], ['Your best friend since you were six.'], ['Leo is scared of everything.'], ['Dogs. Thunder. The dark.'], ['Above all, heights.'], ["He won't stand on a chair to change a light bulb."]] },
    { id: 'deal', lines: [['Years ago, he made you a deal.'], ["Two taps on my chest means I'm scared.", 'leo'], ["Don't laugh. You promised.", 'leo'], ['Two taps... and you stop.', N, 1.1]] },
    { id: 'tell', lines: [['When you tell him about Mr. Black, he goes quiet.'], ["You can't read his face, of course."], ['But he taps. Twice.', N, 1.1], ["Sam. Please don't.", 'leo', 0.5], ['You go anyway.', N, 0.6]] },
    { id: 'crane', lines: [['An old crane at the docks.'], ['A steel beam, forty meters up.'], ['Thirty centimeters wide.'], ['Cameras everywhere.'], ['Mr. Black clips a safety line to your belt.'], ['The stream goes live.', N, 0.5], ['Then you feel a tug.', N, 0.4], ["He's unclipped it."], ['More real this way, kid.', 'black'], ["You're already halfway out."]] },
    { id: 'climb', lines: [['Then the ladder rattles.'], ['Leo? He followed you.'], ["He's climbing."], ['Sam? Come back!', 'leo'], ['Ten meters. Twenty. Thirty.'], ['Then he stops. Frozen.', N, 0.5], ['The wind up here is far stronger than on the ground.'], ['A fall from forty meters takes under three seconds.'], ["And Leo's fingers... are slipping.", N, 0.6]] },
    { id: 'choice', lines: [['You look at his face.'], ["You can't read it."], ["To you, it's just... a face."], ['What are you waiting for? A million people are watching.', 'black'], ['Ahead, the end of the beam. The views. The money.'], ['Behind you, your best friend.'], ['The views... or Leo.', N, 1.0]] },
    { id: 'taps', lines: [['Then Leo lifts one shaking hand.'], ['And taps his chest.', N, 0.2], ['Twice.', N, 1.2]] },
    { id: 'turn', lines: [['You turn around.'], ["You don't rush."], ["You can't feel it... so you think it."], ['Step. Breathe. Step.'], ['You crouch beside the ladder.'], ['Leo. Look at me. Can you hear me?', 'sam'], ['Three points of contact.'], ['Two hands and a foot. Or two feet and a hand.'], ['Always three.'], ["It's the oldest rule in climbing."]] },
    { id: 'down', lines: [['You talk him down.'], ['One rung at a time.'], ['Your calm becomes his calm.'], ['The only steady thing in the sky... is your voice.', N, 0.6]] },
    { id: 'truth', lines: [['At the bottom, he collapses in the dust.'], ['Then you pick up the camera Mr. Black dropped.'], ['Still live.'], ['You point it at the loose safety line.'], ['He unclipped this. On purpose.', 'sam'], ["You don't shout. You don't shove him."], ['You just tell the truth.'], ['By evening, his channel is gone.']] },
    { id: 'psa', lines: [['And remember: no video is worth a hospital bed.'], ["If someone asks you to drop your safety gear for views... they're not the one who'd fall.", N, 0.6]] },
    { id: 'comments', lines: [['The comments fill with one name.'], ['Leo.', N, 0.4], ['Leo, who climbed thirty meters while terrified.'], ["Because that's brave."], ['Not feeling nothing... feeling everything, and climbing anyway.', N, 0.6]] },
    { id: 'hug', lines: [['Later he asks how you stayed so calm.'], ['You shrug.'], ["I can't feel it. So I have to think it.", 'sam'], ['He grins.'], ["Then I'll feel it for both of us.", 'leo'], ["You still can't see the fear on his face."], ['But you can see that grin.'], ["And when he hugs you, your heart does something it hasn't done in years."], ['It jumps.', N, 0.8]] },
    { id: 'envelope', lines: [['That night, an envelope slides under your door.'], ['No stamp. No name.'], ['One line.', N, 0.5], ['We know what you can\'t feel. We need you.', 'note', 0.8]] },
    { id: 'outro', lines: [['So what would you do with zero fear?'], ["Tell us the first scary thing you'd try in the comments."], ['And if you got chills when Leo tapped twice... hit like, and subscribe for Part Two.']] },
  ];
  const VOICE = 'am_onyx*0.8+am_michael*0.2@0.93'; // a deep, warm storyteller (Kokoro, via tts/kokoro.py)
  const out = { SCENES, VOICE };
  if (typeof module !== 'undefined') module.exports = out; else globalThis.LINES = out;
})();
