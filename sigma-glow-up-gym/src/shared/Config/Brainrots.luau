-- Daily spin prizes. All characters are original to this game (see CLAUDE.md guardrails).
-- The spin is free and these are never sold. Odds are always shown to the player.
--
-- auraMult multiplies Aura per rep. luckyBonus adds to the chance of double Aura.

local Brainrots = {}

-- odds add up to 1. The first entry is the one Brainrot Luck takes odds away from.
Brainrots.Rarities = {
	{ id = "Common", odds = 0.55, color = Color3.fromRGB(156, 163, 175), duplicateDrip = 5 },
	{ id = "Rare", odds = 0.28, color = Color3.fromRGB(59, 130, 246), duplicateDrip = 10 },
	{ id = "Epic", odds = 0.12, color = Color3.fromRGB(168, 85, 247), duplicateDrip = 25 },
	{ id = "Legendary", odds = 0.04, color = Color3.fromRGB(255, 210, 63), duplicateDrip = 50 },
	{ id = "Mythic", odds = 0.01, color = Color3.fromRGB(255, 92, 168), duplicateDrip = 100 },
}

Brainrots.List = {
	{ id = "SockGoblin", name = "Sock Goblin", emoji = "🧦", rarity = "Common", auraMult = 1.1 },
	{ id = "SoggyWaffle", name = "Soggy Waffle", emoji = "🧇", rarity = "Common", auraMult = 1.15 },
	{ id = "CouchCarl", name = "Couch Carl", emoji = "🛋️", rarity = "Common", auraMult = 1, luckyBonus = 0.05 },
	{ id = "BananaBouncer", name = "Banana Bouncer", emoji = "🍌", rarity = "Rare", auraMult = 1.25 },
	{ id = "BucketKnight", name = "Bucket Knight", emoji = "🪣", rarity = "Rare", auraMult = 1.3 },
	{ id = "DuckDeadlift", name = "Duck Deadlift", emoji = "🦆", rarity = "Epic", auraMult = 1.5 },
	{ id = "SirSandwich", name = "Sir Sandwich", emoji = "🥪", rarity = "Epic", auraMult = 1.5, luckyBonus = 0.05 },
	{ id = "PigeonPresso", name = "Pigeon Presso", emoji = "🐦", rarity = "Legendary", auraMult = 2 },
	{ id = "TurboPizza", name = "Turbo Pizza", emoji = "🍕", rarity = "Legendary", auraMult = 2, luckyBonus = 0.05 },
	{ id = "CosmicToaster", name = "Cosmic Toaster", emoji = "🌌", rarity = "Mythic", auraMult = 3 },
}

Brainrots.ById = {}
for _, brainrot in ipairs(Brainrots.List) do
	Brainrots.ById[brainrot.id] = brainrot
end

Brainrots.RarityById = {}
for _, rarity in ipairs(Brainrots.Rarities) do
	Brainrots.RarityById[rarity.id] = rarity
end

return Brainrots
