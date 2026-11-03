local T = ...
local Economy = T.load("src/shared/Logic/Economy.luau")
local Offline = T.load("src/shared/Logic/Offline.luau")
local OfflineConfig = T.load("src/shared/Config/Offline.luau")
local Validate = T.load("src/server/Util/Validate.luau")
local RateLimiter = T.load("src/server/Util/RateLimiter.luau")

T.test("amounts must be positive finite numbers", function()
	T.truthy(Economy.IsValidAmount(5))
	T.falsy(Economy.IsValidAmount(0))
	T.falsy(Economy.IsValidAmount(-5))
	T.falsy(Economy.IsValidAmount(0 / 0))
	T.falsy(Economy.IsValidAmount(math.huge))
	T.falsy(Economy.IsValidAmount("5"))
end)

T.test("cost checks", function()
	T.truthy(Economy.CanAfford(100, 100))
	T.falsy(Economy.CanAfford(99, 100))
	T.falsy(Economy.CanAfford(100, -1), "negative costs would add currency")
end)

T.test("a receipt grants exactly once", function()
	local purchases = {}
	local grants = 0
	local function grant()
		grants = grants + 1
	end
	T.eq(Economy.ProcessReceipt(purchases, "abc", 100, grant), "Granted")
	T.eq(Economy.ProcessReceipt(purchases, "abc", 100, grant), "AlreadyGranted")
	T.eq(grants, 1)
end)

T.test("a failed grant is not recorded, so it can retry", function()
	local purchases = {}
	local failing = function()
		error("boom")
	end
	local refusing = function()
		return false
	end
	T.eq(Economy.ProcessReceipt(purchases, "abc", 100, failing), "Failed")
	T.eq(Economy.ProcessReceipt(purchases, "def", 100, refusing), "Failed")
	T.eq(#purchases, 0)
	T.eq(Economy.ProcessReceipt(purchases, "abc", 100, function() end), "Granted")
end)

T.test("only the newest receipts are kept", function()
	local purchases = {}
	for i = 1, 105 do
		Economy.RecordPurchase(purchases, "id" .. i, 100)
	end
	T.eq(#purchases, 100)
	T.falsy(Economy.HasPurchase(purchases, "id5"))
	T.truthy(Economy.HasPurchase(purchases, "id6"))
end)

T.test("offline pays nothing below the minimum", function()
	T.eq(Offline.Earned(1000000, 1000000 - OfflineConfig.MinSeconds + 1, 8, 100), 0)
	T.eq(Offline.Earned(1000000, 0, 8, 100), 0, "a brand new player has no absence")
end)

T.test("offline pays the configured share", function()
	local earned = Offline.Earned(1000000, 1000000 - 1000, 8, 100)
	T.near(earned, 1000 * OfflineConfig.Rate * 100, 1e-6)
end)

T.test("offline is capped", function()
	local now = 100000000
	T.eq(Offline.CountedSeconds(now, now - 1000000, 8), 8 * 3600)
	T.eq(Offline.CountedSeconds(now, now - 1000000, 24), 24 * 3600)
end)

T.test("offline perk adds to the rate", function()
	local plain = Offline.Earned(1000000, 1000000 - 1000, 8, 100)
	local perked = Offline.Earned(1000000, 1000000 - 1000, 8, 100, 0.05)
	T.near(perked - plain, 1000 * 0.05 * 100, 1e-6)
end)

T.test("validate rejects bad numbers", function()
	T.truthy(Validate.number(1))
	T.falsy(Validate.number("1"))
	T.falsy(Validate.number(0 / 0))
	T.falsy(Validate.number(math.huge))
	T.falsy(Validate.number(5, 0, 1))
	T.truthy(Validate.integer(3, 1, 8))
	T.falsy(Validate.integer(3.5, 1, 8))
end)

T.test("validate keys and strings", function()
	local tbl = { Dumbbells = 1 }
	T.truthy(Validate.key("Dumbbells", tbl))
	T.falsy(Validate.key("Nope", tbl))
	T.falsy(Validate.key(1, tbl))
	T.falsy(Validate.key({}, tbl))
	T.falsy(Validate.str(string.rep("x", 65)))
	T.truthy(Validate.oneOf(2, { 1, 2 }))
	T.falsy(Validate.oneOf(3, { 1, 2 }))
end)

T.test("rate limiter allows a burst, then refills over time", function()
	local player = {}
	T.truthy(RateLimiter.allow(player, "X", 2, 100))
	T.truthy(RateLimiter.allow(player, "X", 2, 100))
	T.falsy(RateLimiter.allow(player, "X", 2, 100))
	T.truthy(RateLimiter.allow(player, "X", 2, 100.5))
	T.truthy(RateLimiter.allow(player, "Y", 2, 100), "each remote has its own bucket")
end)
