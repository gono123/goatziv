local T = ...
local Config = T.load("src/shared/Config/Upgrades.luau")
local Upgrades = T.load("src/shared/Logic/Upgrades.luau")

local power = Config.ById.Power

T.test("cost rises with level", function()
	T.eq(Upgrades.Cost(power, 0), power.baseCost)
	T.truthy(Upgrades.Cost(power, 5) > Upgrades.Cost(power, 4))
end)

T.test("max level has no next cost", function()
	T.eq(Upgrades.Cost(power, power.maxLevel), nil)
	T.truthy(Upgrades.Cost(power, power.maxLevel - 1) ~= nil)
end)

T.test("effects follow levels", function()
	T.eq(Upgrades.PowerMultiplier({}), 1)
	T.near(Upgrades.PowerMultiplier({ Power = 5 }), 2, 1e-9)
	T.near(Upgrades.LuckyChance({ Lucky = 2 }), 0.06, 1e-9)
	T.near(Upgrades.SpinLuck({ SpinLuck = 5 }), 0.1, 1e-9)
end)

T.test("lucky chance stays below certain at max level", function()
	T.truthy(Upgrades.LuckyChance({ Lucky = Config.ById.Lucky.maxLevel }) < 1)
end)

T.test("every upgrade can be bought", function()
	for _, upgrade in ipairs(Config.List) do
		T.truthy(upgrade.baseCost > 0 and upgrade.costGrowth > 1 and upgrade.maxLevel >= 1, upgrade.id)
	end
end)
