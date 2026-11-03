-- Per-player, per-remote token bucket. Every remote handler goes through this.

local Players = game:GetService("Players")

local RateLimiter = {}

local buckets = {} -- [player] = { [name] = { tokens, last } }

-- True if this player may fire `name` now, at up to `perSecond` calls per second on
-- average. Allows a burst of one second's worth. `now` is only passed by tests.
function RateLimiter.allow(player, name, perSecond, now)
	now = now or os.clock()

	local playerBuckets = buckets[player]
	if not playerBuckets then
		playerBuckets = {}
		buckets[player] = playerBuckets
	end

	local capacity = math.max(perSecond, 1)
	local bucket = playerBuckets[name]
	if not bucket then
		bucket = { tokens = capacity, last = now }
		playerBuckets[name] = bucket
	end

	bucket.tokens = math.min(capacity, bucket.tokens + (now - bucket.last) * perSecond)
	bucket.last = now

	if bucket.tokens < 1 then
		return false
	end
	bucket.tokens = bucket.tokens - 1
	return true
end

function RateLimiter.forget(player)
	buckets[player] = nil
end

Players.PlayerRemoving:Connect(RateLimiter.forget)

return RateLimiter
