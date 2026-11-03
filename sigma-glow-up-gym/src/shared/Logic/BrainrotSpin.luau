-- Daily spin rules. Pure: no Roblox services.

local Config = require(script.Parent.Parent.Config.Brainrots)

local BrainrotSpin = {}

function BrainrotSpin.CanSpin(lastSpinDay, day)
	return day > lastSpinDay
end

-- Odds for each rarity. Luck moves odds from the first rarity to all the others,
-- in proportion to their odds. Always adds up to 1.
function BrainrotSpin.Odds(luck)
	local first = Config.Rarities[1]
	local moved = math.min(luck or 0, first.odds)
	local rest = 1 - first.odds

	local odds = {}
	for index, rarity in ipairs(Config.Rarities) do
		if index == 1 then
			odds[index] = { rarity = rarity, odds = first.odds - moved }
		else
			odds[index] = { rarity = rarity, odds = rarity.odds + moved * rarity.odds / rest }
		end
	end
	return odds
end

-- roll is 0..1.
function BrainrotSpin.RollRarity(roll, luck)
	local odds = BrainrotSpin.Odds(luck)
	local running = 0
	for _, entry in ipairs(odds) do
		running = running + entry.odds
		if roll < running then
			return entry.rarity
		end
	end
	return odds[#odds].rarity
end

-- Both rolls are 0..1. Every brainrot of the rolled rarity is equally likely.
function BrainrotSpin.Pick(rarityRoll, itemRoll, luck)
	local rarity = BrainrotSpin.RollRarity(rarityRoll, luck)
	local items = {}
	for _, brainrot in ipairs(Config.List) do
		if brainrot.rarity == rarity.id then
			table.insert(items, brainrot)
		end
	end
	return items[math.min(#items, math.floor(itemRoll * #items) + 1)]
end

-- Used to decide whether a new prize should be equipped automatically.
function BrainrotSpin.Strength(brainrot)
	return brainrot.auraMult + (brainrot.luckyBonus or 0)
end

-- Short text for the UI, such as "x2 Aura" or "x1.5 Aura, +5% lucky".
function BrainrotSpin.Describe(brainrot)
	local parts = {}
	if brainrot.auraMult > 1 then
		table.insert(parts, "x" .. brainrot.auraMult .. " Aura")
	end
	if brainrot.luckyBonus then
		table.insert(parts, "+" .. math.floor(brainrot.luckyBonus * 100 + 0.5) .. "% lucky")
	end
	return table.concat(parts, ", ")
end

return BrainrotSpin
