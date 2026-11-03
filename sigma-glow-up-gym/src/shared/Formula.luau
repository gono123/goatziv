-- Pure game math shared by server (authoritative) and client (visuals).

local Training = require(script.Parent.Config.Training)

local Formula = {}

-- Position (0..1) of a meter that sweeps 0 -> 1 -> 0 once per `period` seconds.
function Formula.MarkerPosition(elapsed, period)
	local phase = (elapsed % period) / period
	if phase < 0.5 then
		return phase * 2
	end
	return (1 - phase) * 2
end

function Formula.ResetMultiplier(glowResets)
	return 1 + Training.GlowResetBonus * glowResets
end

-- AuraPerRep = EquipmentBase x Stage x Resets x Upgrades x Brainrot x Boosts. Extras are optional.
function Formula.AuraPerRep(
	equipmentBase,
	stageMultiplier,
	glowResets,
	upgradeMultiplier,
	brainrotMultiplier,
	boostMultiplier
)
	return equipmentBase
		* stageMultiplier
		* Formula.ResetMultiplier(glowResets)
		* (upgradeMultiplier or 1)
		* (brainrotMultiplier or 1)
		* (boostMultiplier or 1)
end

-- Rough Aura per second from training: best machine x stage x resets, at 1 rep per second.
function Formula.EstimatedRatePerSecond(bestEquipmentBase, stageMultiplier, glowResets)
	return bestEquipmentBase * stageMultiplier * Formula.ResetMultiplier(glowResets)
end

-- Shards granted for the Nth reset (1-based).
function Formula.GlowShardsForReset(resetNumber)
	return Training.GlowShardsBase + Training.GlowShardsPerReset * resetNumber
end

return Formula
