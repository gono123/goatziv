local T = ...
local Formula = T.load("src/shared/Formula.luau")
local Stages = T.load("src/shared/Config/Stages.luau")
local Equipment = T.load("src/shared/Config/Equipment.luau")
local Training = T.load("src/shared/Config/Training.luau")

local PERFECT_RATE = 0.6
local GOOD_RATE = 0.3
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

-- Seconds until each stage for a player with the given Perfect rate. The marker
-- crosses gold every Period / 2 seconds, and a good player taps once per crossing.
local function simulate(seed, targetStage)
	local random = T.rng(seed)
	local repSeconds = Training.Period / 2
	local aura, stage, combo, seconds = 0, 1, 0, 0
	local reached = {}
	while stage < targetStage do
		local roll = random()
		local quality = "Miss"
		if roll < PERFECT_RATE then
			quality = "Perfect"
			combo = combo + 1
		else
			combo = 0
			if roll < PERFECT_RATE + GOOD_RATE then
				quality = "Good"
			end
		end
		aura = aura + Formula.AuraPerRep(bestBase(stage), Stages.List[stage].multiplier, quality, 0, combo, 1)
		seconds = seconds + repSeconds
		while Stages.List[stage + 1] and aura >= Stages.List[stage + 1].auraRequired do
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

T.test("pacing for a 60% Perfect player", function()
	for seed = 1, 10 do
		local reached = simulate(seed * 977, 4)
		T.truthy(reached[2] < 90, "Gym Rat took " .. reached[2] .. " s")
		T.truthy(reached[3] >= 180 and reached[3] <= 360, "Chad took " .. reached[3] .. " s")
		T.truthy(reached[4] >= 18 * 60 and reached[4] <= 30 * 60, "Sigma took " .. reached[4] .. " s")
	end
end)
