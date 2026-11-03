-- Upgrade costs and effects. Pure: no Roblox services.

local Config = require(script.Parent.Parent.Config.Upgrades)

local Upgrades = {}

-- Aura cost of the next level, or nil at max level.
function Upgrades.Cost(upgrade, level)
	if level >= upgrade.maxLevel then
		return nil
	end
	return math.floor(upgrade.baseCost * upgrade.costGrowth ^ level)
end

local function bonus(levels, id)
	return (levels[id] or 0) * Config.ById[id].perLevel
end

function Upgrades.PowerMultiplier(levels)
	return 1 + bonus(levels, "Power")
end

function Upgrades.LuckyChance(levels)
	return bonus(levels, "Lucky")
end

function Upgrades.SpinLuck(levels)
	return bonus(levels, "SpinLuck")
end

return Upgrades
