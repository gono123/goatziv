-- Upgrades bought with Aura. Bought levels last until the next Glow Reset.
-- perLevel is the bonus each level adds: 0.2 means +20%.

local Upgrades = {}

Upgrades.List = {
	{
		id = "Power",
		name = "Stronger Reps",
		emoji = "💪",
		text = "+20% Aura per rep",
		baseCost = 25,
		costGrowth = 1.6,
		maxLevel = 20,
		perLevel = 0.2,
	},
	{
		id = "Lucky",
		name = "Lucky Reps",
		emoji = "🍀",
		text = "+3% chance of double Aura",
		baseCost = 150,
		costGrowth = 1.9,
		maxLevel = 10,
		perLevel = 0.03,
	},
	{
		id = "SpinLuck",
		name = "Brainrot Luck",
		emoji = "🧠",
		text = "+2% better daily spin odds",
		baseCost = 1000,
		costGrowth = 4,
		maxLevel = 5,
		perLevel = 0.02,
	},
}

Upgrades.ById = {}
for _, upgrade in ipairs(Upgrades.List) do
	Upgrades.ById[upgrade.id] = upgrade
end

return Upgrades
