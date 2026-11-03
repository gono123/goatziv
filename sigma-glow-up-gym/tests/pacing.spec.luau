local T = ...
local Formula = T.load("src/shared/Formula.luau")
local Stages = T.load("src/shared/Config/Stages.luau")
local Equipment = T.load("src/shared/Config/Equipment.luau")
local UpgradesConfig = T.load("src/shared/Config/Upgrades.luau")
local Upgrades = T.load("src/shared/Logic/Upgrades.luau")

local CLICKS_PER_SECOND = 3 -- a normal player clicking steadily
local WALK_SECONDS = 3 -- time to move to a newly unlocked machine

local function bestBase(stageIndex)
	local best = 0
	for _, def in pairs(Equipment) do
		if stageIndex >= def.unlockStage then
			best = math.max(best, def.base)
		end
	end
	return best
end

local function buyEverythingAffordable(balance, levels)
	local bought = true
	while bought do
		bought = false
		for _, upgrade in ipairs(UpgradesConfig.List) do
			local cost = Upgrades.Cost(upgrade, levels[upgrade.id] or 0)
			if cost and balance >= cost then
				balance = balance - cost
				levels[upgrade.id] = (levels[upgrade.id] or 0) + 1
				bought = true
			end
		end
	end
	return balance
end

-- Seconds until each stage. The player spends Aura on upgrades as soon as they can.
-- Spending never slows stage progress, because stages use Aura earned, not Aura held.
local function simulate(seed, targetStage, brainrotMult)
	local random = T.rng(seed)
	local repSeconds = 1 / CLICKS_PER_SECOND
	local balance, earned, stage, seconds = 0, 0, 1, 0
	local levels = {}
	local reached = {}
	while stage < targetStage do
		local gained = Formula.AuraPerRep(
			bestBase(stage),
			Stages.List[stage].multiplier,
			0,
			Upgrades.PowerMultiplier(levels),
			brainrotMult,
			1
		)
		if random() < Upgrades.LuckyChance(levels) then
			gained = gained * 2
		end
		balance = balance + gained
		earned = earned + gained
		seconds = seconds + repSeconds
		balance = buyEverythingAffordable(balance, levels)
		while Stages.List[stage + 1] and earned >= Stages.List[stage + 1].auraRequired do
			stage = stage + 1
			reached[stage] = seconds
			seconds = seconds + WALK_SECONDS
		end
	end
	return reached
end

T.test("stage thresholds rise in order", function()
	for i = 2, #Stages.List do
		T.truthy(Stages.List[i].auraRequired > Stages.List[i - 1].auraRequired, "stage " .. i)
		T.truthy(Stages.List[i].multiplier > Stages.List[i - 1].multiplier, "multiplier " .. i)
	end
end)

T.test("every stage has a machine it can train on", function()
	for i = 1, #Stages.List do
		T.truthy(bestBase(i) > 0, "no machine available at stage " .. i)
	end
end)

T.test("pacing with upgrades and no brainrot", function()
	local reached = simulate(977, 4, 1)
	print(string.format("     Gym Rat %.0fs, Chad %.1fm, Sigma %.1fm", reached[2], reached[3] / 60, reached[4] / 60))
	T.truthy(reached[2] < 90, "Gym Rat took " .. reached[2] .. " s")
	T.truthy(reached[3] >= 180 and reached[3] <= 360, "Chad took " .. reached[3] .. " s")
	T.truthy(reached[4] >= 18 * 60 and reached[4] <= 30 * 60, "Sigma took " .. reached[4] .. " s")
end)

T.test("a x2 brainrot helps but never skips the early game", function()
	local plain = simulate(977, 4, 1)
	local helped = simulate(977, 4, 2)
	print(
		string.format("     with x2: Gym Rat %.0fs, Chad %.1fm, Sigma %.1fm", helped[2], helped[3] / 60, helped[4] / 60)
	)
	T.truthy(helped[4] < plain[4], "x2 should be faster")
	T.truthy(helped[4] >= 8 * 60, "Sigma with x2 took only " .. helped[4] .. " s")
end)
