-- Pure game math shared by server (authoritative) and client (visuals).

local Training = require(script.Parent.Config.Training)

local Formula = {}

-- Marker position on the bar (0..1) for a given time since the cycle started.
-- `period` is optional and defaults to the training bar.
function Formula.MarkerPosition(elapsed, period)
	period = period or Training.Period
	local phase = (elapsed % period) / period
	if phase < 0.5 then
		return phase * 2
	end
	return (1 - phase) * 2
end

function Formula.GoldHalfWidth(lockedIn)
	if lockedIn then
		return Training.GoldHalfWidthLockedIn
	end
	return Training.GoldHalfWidth
end

function Formula.Quality(position, lockedIn)
	local distance = math.abs(position - 0.5)
	if distance <= Formula.GoldHalfWidth(lockedIn) then
		return "Perfect"
	elseif distance <= Training.GreenHalfWidth then
		return "Good"
	end
	return "Miss"
end

function Formula.IsLockedIn(combo)
	return combo >= Training.LockedInCombo
end

function Formula.ResetMultiplier(glowResets)
	return 1 + Training.GlowResetBonus * glowResets
end

-- AuraPerRep = EquipmentBase x StageMultiplier x Quality x ResetMultiplier x Combo x Boosts
function Formula.AuraPerRep(equipmentBase, stageMultiplier, quality, glowResets, combo, boostMultiplier)
	local qualityMultiplier = Training.Quality[quality] or 0
	local comboMultiplier = 1
	if Formula.IsLockedIn(combo) then
		comboMultiplier = Training.LockedInMultiplier
	end
	return equipmentBase
		* stageMultiplier
		* qualityMultiplier
		* Formula.ResetMultiplier(glowResets)
		* comboMultiplier
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
