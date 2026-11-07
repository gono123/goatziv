"""Episode 2: "In This World, Whoever Ties Your Tie Controls You 👔" -- same format as v2/lines.py.

`[shot]` before a word = the picture cuts there. Story shape from ../STYLE_GUIDE.md:
rule -> funny examples -> the one rule -> the hero -> the loss (Pip) -> the loophole -> rescue -> button.
Music: Six Forty Seven (creepy world part) -> Cry from [new_principal] (the story's turn).
"""

TITLE = "In This World, Whoever Ties Your Tie Controls You 👔"
TURN = "new_principal"

SCRIPT = [
    "[town] In this world, everyone wears a tie. [tie_close] And whoever ties your tie controls you.",
    "[remote] You see, a tie works like a remote control.",
    "[dad_boss] My dad's boss ties his tie every morning, [dad_yes] so my dad works until midnight and says yes sir in his sleep.",
    "[grandma_tie] Grandma tied her own tie fifty years ago. [grandma_no] Nobody has told her what to do since. Not even her doctor.",
    "[wedding] At weddings, couples tie each other's ties. [married] That's why married people always agree.",
    "[sign_rule] And there's one rule. [stranger] Never, ever let a stranger touch your tie.",
    "[hero_mirror] I'm the only kid in my school who ties his own. [hero_knot] Pink suit, striped tie, double knot.",
    "[mom_teach] My mom taught me when I was four. [mom_rule] Nobody touches your tie, she said. Not even me.",
    "[pip_intro] My best friend Pip can't tie a knot to save his life. [pip_mess] His tie looks like spaghetti.",
    "[new_principal] Then a new principal came to our school. [knotley_smile] Principal Knotley. He never stopped smiling.",
    "[picture_day] On the first day, he made an announcement. [knotley_offer] Free perfect knots for picture day.",
    "[line_up] Everyone lined up. [pip_line] Even Pip. [hero_no] Not me.",
    "[next_morning] The next morning, the whole school was quiet. [march] Kids walked in perfect lines. [no_laugh] Nobody laughed.",
    "[pip_empty] Pip didn't even say hi. His eyes were empty.",
    "[knotley_tug] Then Knotley tugged his own tie, [heads_turn] and every kid in the school turned their head at the same time.",
    "[hero_alone] Everyone except me.",
    "[knotley_notice] Knotley noticed. [knotley_close] Your knot looks crooked, son. Let me fix that.",
    "[run] I ran. [hide] I hid in the janitor's closet until the bell.",
    "[think] And that's when I figured it out. [threads] Knotley controls every kid, [his_tie] but who controls Knotley?",
    "[his_knot] Nobody. He ties his own tie. [hero_idea] Just like me.",
    "[assembly] At the afternoon assembly, five hundred kids sat perfectly still. [stage] Knotley stood on stage, holding his tie like a leash.",
    "[crawl] I crawled under every chair, [behind] right up behind him.",
    "[grab] I grabbed his tie, [untie] pulled it loose, [retie] and before he could turn around, I tied it again. [double] Double knot.",
    "[freeze] Knotley froze. [knotley_ask] Then he slowly looked at me. What would you like me to do?",
    "[order] Untie them, I said. Every single one.",
    "[untie_all] So the principal ran down every row, untying five hundred ties.",
    "[pip_wake] Pip blinked. [pip_why] Dude, why am I sitting so straight?",
    "[cafeteria] Now Knotley works in the cafeteria. [pancakes] He makes amazing pancakes.",
    "[ending] I tie his tie every morning. Honestly? He's way nicer now.",
]

HOLD = {"[double]": 0.4, "[untie_all]": 0.3, "[ending]": 1.4}
