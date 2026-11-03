local T = ...
local Rating = T.load("src/shared/Logic/Rating.luau")

local function sum(list)
	local total = 0
	for _, value in ipairs(list) do
		total = total + value
	end
	return total
end

T.test("elo sums to about zero", function()
	local deltas = Rating.Deltas({
		{ rating = 1000, placement = 1 },
		{ rating = 1200, placement = 2 },
		{ rating = 900, placement = 3 },
		{ rating = 1500, placement = 4 },
	})
	T.near(sum(deltas), 0, 1e-6)
end)

T.test("even match moves half of K", function()
	local deltas = Rating.Deltas({ { rating = 1000, placement = 1 }, { rating = 1000, placement = 2 } })
	T.near(deltas[1], 16, 1e-9)
	T.near(deltas[2], -16, 1e-9)
end)

T.test("beating a stronger player pays more", function()
	local upset = Rating.Deltas({ { rating = 1000, placement = 1 }, { rating = 1400, placement = 2 } })
	local expected = Rating.Deltas({ { rating = 1400, placement = 1 }, { rating = 1000, placement = 2 } })
	T.truthy(upset[1] > expected[1])
end)

T.test("tiers map to the right names", function()
	T.eq(Rating.Tier(1000).name, "Bronze Bro")
	T.eq(Rating.Tier(1099).name, "Bronze Bro")
	T.eq(Rating.Tier(1100).name, "Silver Sigma")
	T.eq(Rating.Tier(1249).name, "Silver Sigma")
	T.eq(Rating.Tier(1250).name, "Gold Goat")
	T.eq(Rating.Tier(1400).name, "Diamond Mogger")
	T.eq(Rating.Tier(1600).name, "Cosmic Legend")
	T.eq(Rating.Tier(-50).name, "Bronze Bro", "very low ratings stay in the first tier")
end)
