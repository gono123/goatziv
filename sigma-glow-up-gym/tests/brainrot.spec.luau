local T = ...
local Config = T.load("src/shared/Config/Brainrots.luau")
local BrainrotSpin = T.load("src/shared/Logic/BrainrotSpin.luau")

local function total(odds)
	local sum = 0
	for _, entry in ipairs(odds) do
		sum = sum + entry.odds
	end
	return sum
end

T.test("odds add up to 100%", function()
	T.near(total(BrainrotSpin.Odds(0)), 1, 1e-9)
	T.near(total(BrainrotSpin.Odds(0.1)), 1, 1e-9)
	T.near(total(BrainrotSpin.Odds(5)), 1, 1e-9, "luck can never push odds past 100%")
end)

T.test("luck moves odds away from common", function()
	local plain = BrainrotSpin.Odds(0)
	local lucky = BrainrotSpin.Odds(0.1)
	T.near(lucky[1].odds, plain[1].odds - 0.1, 1e-9)
	for i = 2, #plain do
		T.truthy(lucky[i].odds > plain[i].odds, plain[i].rarity.id)
	end
end)

T.test("once a day", function()
	T.truthy(BrainrotSpin.CanSpin(0, 20000), "first spin")
	T.falsy(BrainrotSpin.CanSpin(20000, 20000), "same day")
	T.truthy(BrainrotSpin.CanSpin(20000, 20001), "next day")
end)

T.test("rolls land on the right rarity", function()
	T.eq(BrainrotSpin.RollRarity(0, 0).id, "Common")
	T.eq(BrainrotSpin.RollRarity(0.54, 0).id, "Common")
	T.eq(BrainrotSpin.RollRarity(0.56, 0).id, "Rare")
	T.eq(BrainrotSpin.RollRarity(0.9, 0).id, "Epic")
	T.eq(BrainrotSpin.RollRarity(0.97, 0).id, "Legendary")
	T.eq(BrainrotSpin.RollRarity(0.995, 0).id, "Mythic")
	T.eq(BrainrotSpin.RollRarity(0.99999999, 0).id, "Mythic")
end)

T.test("real odds match the odds shown to players", function()
	local random = T.rng(321)
	local counts = {}
	local spins = 100000
	for _ = 1, spins do
		local prize = BrainrotSpin.Pick(random(), random(), 0)
		counts[prize.rarity] = (counts[prize.rarity] or 0) + 1
	end
	for _, rarity in ipairs(Config.Rarities) do
		T.near(counts[rarity.id] / spins, rarity.odds, 0.01, rarity.id)
	end
end)

T.test("every rarity has a prize and every prize a valid rarity", function()
	for _, rarity in ipairs(Config.Rarities) do
		local found = false
		for _, brainrot in ipairs(Config.List) do
			found = found or brainrot.rarity == rarity.id
		end
		T.truthy(found, rarity.id .. " has no prizes")
	end
	for _, brainrot in ipairs(Config.List) do
		T.truthy(Config.RarityById[brainrot.rarity], brainrot.id)
	end
end)

T.test("a legendary doubles aura per rep", function()
	T.eq(Config.ById.PigeonPresso.auraMult, 2)
	T.eq(BrainrotSpin.Describe(Config.ById.PigeonPresso), "x2 Aura")
end)

T.test("every prize helps and has a description", function()
	for _, brainrot in ipairs(Config.List) do
		T.truthy(brainrot.auraMult > 1 or brainrot.luckyBonus, brainrot.id)
		T.truthy(#BrainrotSpin.Describe(brainrot) > 0, brainrot.id)
	end
end)

T.test("stronger prizes score higher", function()
	T.truthy(BrainrotSpin.Strength(Config.ById.CosmicToaster) > BrainrotSpin.Strength(Config.ById.PigeonPresso))
	T.truthy(BrainrotSpin.Strength(Config.ById.TurboPizza) > BrainrotSpin.Strength(Config.ById.PigeonPresso))
end)
