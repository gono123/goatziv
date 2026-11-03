-- Deterministic daily quest picks (BUILD_SPEC M7). Pure: no Roblox services.
-- Uses its own generator so tests outside Roblox give the same picks as the game.

local QuestPicker = {}

local function makeRandom(seed)
	local state = seed % 4294967296
	return function(limit)
		state = (state * 1664525 + 1013904223) % 4294967296
		return math.floor(state / 4294967296 * limit) + 1
	end
end

-- Picks `count` quests from `pool` for this user and day, never repeating a kind.
-- `salt` changes the result (used for rerolls). `excludeKinds` is an optional set of kinds to skip.
function QuestPicker.Pick(pool, userId, day, count, salt, excludeKinds)
	local random = makeRandom(userId * 1000 + day + (salt or 0) * 7919)
	for _ = 1, 5 do
		random(1) -- the first outputs of a small generator barely depend on the seed
	end

	local candidates = {}
	for _, quest in ipairs(pool) do
		if not (excludeKinds and excludeKinds[quest.kind]) then
			table.insert(candidates, quest)
		end
	end

	local picks = {}
	local usedKinds = {}
	while #picks < count and #candidates > 0 do
		local quest = table.remove(candidates, random(#candidates))
		if not usedKinds[quest.kind] then
			usedKinds[quest.kind] = true
			table.insert(picks, quest)
		end
	end
	return picks
end

return QuestPicker
