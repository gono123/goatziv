# "In This World, Everyone Is Born Grey" -- script, split into shots.
# Each shot is (shot_id, [(speaker, text), ...], optional {"hold": seconds of picture after the last line}). Speakers map to voices in VOICES.
# voice.py turns this into out/vo/*.wav + out/timeline.json using the real voice durations.

TITLE = "In This World, Everyone Is Born Grey 🩷"

VOICES = {
    # Kokoro voices (kokoro-onnx). speed > 1 is faster.
    "N": {"voice": "am_puck", "speed": 1.12},     # narrator: the hero, first person
    "M": {"voice": "af_heart", "speed": 1.0},     # mom
    "P": {"voice": "bm_george", "speed": 0.95},   # Mr. Prism
    "K": {"voice": "am_michael", "speed": 1.1},   # classmate
}

SHOTS = [
    ("town_wide", [("N", "In this world, everyone is born grey.")]),
    ("grey_people", [("N", "Grey hair. Grey clothes. Grey eyes.")]),
    ("bank", [("N", "And if you want color, you have to buy it from the Color Bank.")]),
    ("yellow_drop", [("N", "Get an A on your test? You can afford one drop of yellow.")]),
    ("higgins", [("N", "Mr. Higgins sold his car to buy red cheeks."),
                 ("N", "Now he walks everywhere. But he looks very healthy.")]),
    ("prism", [("N", "The richest man in town is Mr. Prism."),
               ("N", "He owns the Color Bank, and he's so colorful it hurts to look at him.")]),
    ("umbrella", [("N", "He also built the Great Umbrella. A giant glass roof over the whole city."),
                  ("N", "Because rain ruins color. So in our town, it never rains.")]),
    ("inspectors", [("N", "And there's one rule. You can never have color you didn't pay for."),
                    ("N", "If the Grey Inspectors catch you, they wash you. Grey. Forever.")]),
    ("school_grey", [("N", "I'm the greyest kid in my school. Grey shoes. Grey hair."),
                     ("N", "Even my lunch is grey.")]),
    ("mom_paint", [("N", "And every single morning, my mom paints me. Head to toe."),
                   ("M", "Just in case."),
                   ("N", "I thought every mom did that.")]),
    ("mom_rule", [("N", "She only has one rule for me."),
                  ("M", "If it ever rains, you run home. You don't stop. You don't look up.")]),
    ("crack", [("N", "Then, one Tuesday at recess, I heard it. Crack."),
               ("N", "A tiny crack in the Great Umbrella.")]),
    ("rain_me", [("N", "And for the first time in a hundred years, it rained. Right on me.")], {"hold": 0.5}),
    ("wash", [("N", "The grey ran down my face. My shirt turned white. My tie turned red."),
              ("N", "And my suit turned pink. Bright, loud, bubblegum pink.")], {"hold": 1.4}),
    ("stare", [("N", "The whole school went silent."),
               ("K", "Dude. You're pink."),
               ("N", "Somebody dropped their sandwich.")]),
    ("sirens", [("N", "Then I heard the sirens. So I ran. I didn't stop. I didn't look up.")]),
    ("mom_secret", [("N", "My mom locked the door and held my face."),
                    ("M", "Everyone is born with color. The day you're born, the Color Bank paints you grey."),
                    ("M", "Then they sell your own color back to you."),
                    ("M", "The night you were born, the power went out. They never got you.")]),
    ("knock", [("N", "Then, a knock at the door."),
               ("P", "Wash the boy.")]),
    ("escape", [("N", "I squeezed right past the inspectors, and I ran."),
                ("N", "All the way to the top of the Great Umbrella.")]),
    ("lever", [("N", "There was one giant lever. It said, do not open."),
               ("N", "So I opened it.")], {"hold": 0.7}),
    ("dome_open", [("N", "The Great Umbrella split in half, and it rained on the whole city.")], {"hold": 1.6}),
    ("color_town", [("N", "The grey washed off everyone. Green eyes. Red hair. My mom's yellow dress."),
                    ("N", "Colors nobody had ever seen.")], {"hold": 0.8}),
    ("prism_grey", [("N", "And Mr. Prism? His colors were just paint."),
                    ("N", "Underneath, he was the only person in town who was actually born grey.")], {"hold": 0.4}),
    ("ending", [("N", "Now he's the greyest man in the city. Honestly? It kind of suits him.")]),
]
