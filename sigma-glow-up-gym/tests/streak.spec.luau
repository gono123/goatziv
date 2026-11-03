local T = ...
local Streak = T.load("src/shared/Logic/Streak.luau")

local function fresh(lastClaimDay, count, freezesLeft, freezeWeek)
	return { count = count, lastClaimDay = lastClaimDay, freezesLeft = freezesLeft, freezeWeek = freezeWeek }
end

local DAY = 20000
local WEEK = Streak.Week(DAY)

T.test("next day continues the streak", function()
	local s = fresh(DAY - 1, 3, 1, WEEK)
	T.truthy(Streak.Claim(s, DAY))
	T.eq(s.count, 4)
	T.eq(s.freezesLeft, 1)
end)

T.test("same day cannot claim twice", function()
	local s = fresh(DAY, 3, 1, WEEK)
	T.falsy(Streak.IsClaimable(s, DAY))
	T.falsy((Streak.Claim(s, DAY)))
	T.eq(s.count, 3)
end)

T.test("one missed day uses the freeze", function()
	local s = fresh(DAY - 2, 3, 1, WEEK)
	local ok, usedFreeze = Streak.Claim(s, DAY)
	T.truthy(ok)
	T.truthy(usedFreeze)
	T.eq(s.count, 4)
	T.eq(s.freezesLeft, 0)
end)

T.test("one missed day without a freeze resets", function()
	local s = fresh(DAY - 2, 3, 0, WEEK)
	Streak.Claim(s, DAY)
	T.eq(s.count, 1)
end)

T.test("two missed days reset even with a freeze", function()
	local s = fresh(DAY - 3, 5, 1, WEEK)
	Streak.Claim(s, DAY)
	T.eq(s.count, 1)
	T.eq(s.freezesLeft, 1)
end)

T.test("freeze refills in a new week", function()
	local s = fresh(DAY - 2, 3, 0, WEEK - 1)
	local _, usedFreeze = Streak.Claim(s, DAY)
	T.truthy(usedFreeze, "new week gives a fresh freeze")
	T.eq(s.count, 4)
	T.eq(s.freezeWeek, WEEK)
end)

T.test("weeks start on Monday", function()
	-- 1970-01-04 was a Sunday (day 3), 1970-01-05 a Monday (day 4).
	T.eq(Streak.Week(3) + 1, Streak.Week(4))
	T.eq(Streak.Week(4), Streak.Week(10))
end)

T.test("first ever claim starts at 1", function()
	local s = fresh(0, 0, 1, 0)
	Streak.Claim(s, DAY)
	T.eq(s.count, 1)
end)

T.test("rewards follow the seven day cycle", function()
	T.eq(Streak.Reward(1).drip, 10)
	T.eq(Streak.Reward(6).drip, 40)
	T.eq(Streak.Reward(7).drip, 60)
	T.eq(Streak.Reward(7).cosmetic, "shake_chain")
	T.eq(Streak.Reward(8).drip, 10)
	T.eq(Streak.Reward(14).drip, 100)
	T.eq(Streak.Reward(14).cosmetic, nil)
end)
