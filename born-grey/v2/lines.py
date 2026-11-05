"""Born Grey v2: the script, in the channel style (see ../STYLE_GUIDE.md).

Each entry is one sentence (or quote) read by the narrator. `[shot]` before a word means the picture
cuts to that shot on that word, so the picture always shows what is being said (cut every ~1.5 s).
Quotes are read by the same narrator voice, as in the reference videos.
"""

TITLE = "In This World, Everyone Is Born Grey 🩷"

SCRIPT = [
    "[aerial] In this world, everyone is born grey.",
    "[greyhair] Grey hair. [greyclothes] Grey clothes. [greyeyes] Grey eyes.",
    "[bank_ext] And if you want color, you have to buy it [bank_int] from the Color Bank.",
    "[test_a] Get an A on your test? [drop_yellow] You can afford one drop of yellow.",
    "[grandma_sock] Grandmas save up for ten years just to dye one sock.",
    "[mailman_walk] The mailman sold his car to buy red cheeks. [mailman_wave] Now he walks everywhere, but he looks very healthy.",
    "[prism_reveal] The richest man in town is Mr. Prism. [prism_shield] He's so colorful it hurts to look at him.",
    "[umbrella_up] He also built the Great Umbrella, [dome_aerial] a giant glass roof over the whole city, [sign_rain] because rain washes color away.",
    "[dry_street] So in our town, it never rains.",
    "[sign_rule] And there's one rule. [inspectors_march] You can never have color you didn't pay for.",
    "[inspector_mop] If the Grey Inspectors catch you, [scrub] they scrub you grey. [inspector_close] Forever.",
    "[hero_school] I'm the greyest kid in my school. [hero_lunch] Even my lunch is grey.",
    "[mom_paint] Every single morning, my mom paints me, head to toe.",
    "[mom_close] Just in case, she says. [hero_shrug] I thought every mom did that.",
    "[mom_rule] She has one rule for me. [mom_wag] If it ever rains, run home. [run_rule] Don't stop. [dont_look_up] Don't look up.",
    "[pip_intro] My best friend is Pip. [pip_shoelace] He saved up for three whole years to buy one blue shoelace. [pip_proud] He wears it every day.",
    "[recess] Then, one Tuesday at recess, [crack_sound] I heard it. Crack. [crack_dome] A tiny crack in the Great Umbrella.",
    "[rain_drop] And for the first time in a hundred years, [rain_me] it rained, right on me.",
    "[wash_face] The grey ran down my face. [wash_shirt] My shirt turned white. [wash_tie] My tie turned red.",
    "[wash_full] And my suit turned pink. [pink_reveal] Bright, loud, bubblegum pink.",
    "[kids_stare] The whole school went silent. [sandwich] Somebody dropped their sandwich.",
    "[sirens] Then the sirens started. [inspectors_run] Grey Inspectors, everywhere.",
    "[pip_push] Pip shoved me behind the bins. [pip_whisper] Run, he said. [pip_caught] And they grabbed him instead.",
    "[pip_scrub] They scrubbed him so hard, [shoelace_grey] his blue shoelace turned grey.",
    "[hero_run_home] So I ran. [run_feet] I didn't stop. [run_back] I didn't look up.",
    "[home_door] My mom locked the door and held my face.",
    "[mom_secret1] Everyone is born with color, she whispered. [mom_secret2] The day you're born, the Color Bank paints you grey. [bank_vats] Then they sell your own color back to you.",
    "[mom_secret3] The night you were born, the power went out. [blackout] They never got you.",
    "[knock] Then, a knock. [prism_door] Mr. Prism. [prism_point] Wash the boy.",
    "[escape_squeeze] I squeezed right past the inspectors [stairs] and ran all the way to the top of the Great Umbrella.",
    "[lever_wide] There was one giant lever. [lever_sign] It said, do not open. [lever_pull] So I opened it.",
    "[dome_split] The Great Umbrella split in half, [rain_city] and it rained on the whole city.",
    "[wash_town] The grey washed off everyone. [green_eyes] Green eyes. [red_hair] Red hair. [mom_yellow] My mom's yellow dress.",
    "[pip_color] And Pip? Bright orange, from head to toe. [pip_shoelace_blue] Except one shoelace. That stayed blue.",
    "[prism_rain] And Mr. Prism? [prism_wash] His colors were just paint. [prism_grey] Underneath, he was the only person in town who was actually born grey.",
    "[bank_umbrellas] Now the Color Bank sells umbrellas. [prism_desk] Mr. Prism works the front desk. [ending] Honestly? Grey kind of suits him.",
]

# extra picture time after a sentence (seconds), for beats that need it
HOLD = {"[pink_reveal]": 0.9, "[lever_pull]": 0.5, "[rain_city]": 0.8, "[ending]": 1.4, "[crack_dome]": 0.3}
