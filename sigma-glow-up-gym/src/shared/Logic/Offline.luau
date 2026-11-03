-- Offline Aura (BUILD_SPEC M7). Pure: no Roblox services.

local Config = require(script.Parent.Parent.Config.Offline)

local Offline = {}

-- Seconds that count towards the payout: 0 below the minimum, capped at capHours.
function Offline.CountedSeconds(now, lastSeen, capHours)
	if lastSeen <= 0 then
		return 0
	end
	local elapsed = now - lastSeen
	if elapsed < Config.MinSeconds then
		return 0
	end
	return math.min(elapsed, capHours * 3600)
end

-- bonusRate is the extra share from perks, such as 0.05 for +5%.
function Offline.Earned(now, lastSeen, capHours, ratePerSecond, bonusRate)
	return Offline.CountedSeconds(now, lastSeen, capHours) * (Config.Rate + (bonusRate or 0)) * ratePerSecond
end

return Offline
