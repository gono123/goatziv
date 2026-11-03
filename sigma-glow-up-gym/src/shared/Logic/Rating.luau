-- Multiplayer Elo and rating tiers (BUILD_SPEC M5). Pure: no Roblox services.

local PoseOff = require(script.Parent.Parent.Config.PoseOff)

local Rating = {}

function Rating.Expected(rating, opponentRating)
	return 1 / (1 + 10 ^ ((opponentRating - rating) / 400))
end

-- entries = { { rating = n, placement = n }, ... } with placement 1 = winner.
-- Returns a list of rating changes in the same order.
function Rating.Deltas(entries)
	local deltas = {}
	local count = #entries
	for i, me in ipairs(entries) do
		local delta = 0
		for j, other in ipairs(entries) do
			if i ~= j then
				local actual = 0.5
				if me.placement < other.placement then
					actual = 1
				elseif me.placement > other.placement then
					actual = 0
				end
				delta = delta + PoseOff.Rating.K * (actual - Rating.Expected(me.rating, other.rating)) / (count - 1)
			end
		end
		deltas[i] = delta
	end
	return deltas
end

function Rating.Tier(rating)
	local tiers = PoseOff.Rating.Tiers
	local result = tiers[1]
	for _, tier in ipairs(tiers) do
		if rating >= tier.min then
			result = tier
		end
	end
	return result
end

return Rating
