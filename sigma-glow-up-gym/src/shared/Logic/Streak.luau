-- Daily streak day math (BUILD_SPEC M7). Pure: no Roblox services.

local Config = require(script.Parent.Parent.Config.Streak)

local Streak = {}

local SECONDS_PER_DAY = 86400

function Streak.Day(now, dayOffset)
	return math.floor(now / SECONDS_PER_DAY) + (dayOffset or 0)
end

-- Monday-based week index. Day 0 (1 Jan 1970) was a Thursday.
function Streak.Week(day)
	return math.floor((day + 3) / 7)
end

function Streak.IsClaimable(streak, day)
	return day > streak.lastClaimDay
end

-- Advances the streak table for a claim on `day`. Returns false if already claimed,
-- otherwise true and whether a freeze was used.
function Streak.Claim(streak, day)
	if not Streak.IsClaimable(streak, day) then
		return false, false
	end

	local week = Streak.Week(day)
	if week ~= streak.freezeWeek then
		streak.freezeWeek = week
		streak.freezesLeft = Config.FreezesPerWeek
	end

	local usedFreeze = false
	if day == streak.lastClaimDay + 1 then
		streak.count = streak.count + 1
	elseif day == streak.lastClaimDay + 2 and streak.freezesLeft > 0 then
		streak.freezesLeft = streak.freezesLeft - 1
		streak.count = streak.count + 1
		usedFreeze = true
	else
		streak.count = 1
	end
	streak.lastClaimDay = day
	return true, usedFreeze
end

-- Reward for a streak count: { drip = n, cosmetic = id or nil }.
function Streak.Reward(count)
	local dayInCycle = (count - 1) % 7 + 1
	if dayInCycle < 7 then
		return { drip = Config.DripByDay[dayInCycle] }
	end
	if count == 7 then
		return { drip = Config.Day7FirstDrip, cosmetic = Config.Day7Cosmetic }
	end
	return { drip = Config.Day7RepeatDrip }
end

return Streak
