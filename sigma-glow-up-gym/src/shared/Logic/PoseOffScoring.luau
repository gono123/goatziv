-- Pose-Off round scoring (BUILD_SPEC M5). Pure: no Roblox services.

local PoseOff = require(script.Parent.Parent.Config.PoseOff)

local Scoring = {}

-- meterPosition is 0..1 with 0.5 as the sweet spot. nil means no submission.
function Scoring.Timing(meterPosition)
	if meterPosition == nil then
		return 0
	end
	local accuracy = 1 - math.abs(meterPosition - 0.5) / 0.5
	return PoseOff.Score.TimingMax * math.clamp(accuracy, 0, 1)
end

function Scoring.PromptMatch(poseTags, promptTag)
	if poseTags then
		for _, tag in ipairs(poseTags) do
			if tag == promptTag then
				return PoseOff.Score.PromptMatch
			end
		end
	end
	return 0
end

function Scoring.Crowd(votesForContestant, totalVotes)
	if totalVotes <= 0 then
		return 0
	end
	return PoseOff.Score.CrowdMax * votesForContestant / totalVotes
end

-- Virtual votes when there is no real audience. Weighted by each contestant's
-- timing + prompt score. `random` returns 0..1. Returns a list parallel to baseScores.
function Scoring.NpcVotes(baseScores, voteCount, random)
	local total = 0
	for _, score in ipairs(baseScores) do
		total = total + score
	end

	local votes = {}
	for i = 1, #baseScores do
		votes[i] = 0
	end
	if #baseScores == 0 then
		return votes
	end

	for _ = 1, voteCount do
		local index = #baseScores
		if total <= 0 then
			index = math.min(#baseScores, math.floor(random() * #baseScores) + 1)
		else
			local roll = random() * total
			local running = 0
			for i, score in ipairs(baseScores) do
				running = running + score
				if roll < running then
					index = i
					break
				end
			end
		end
		votes[index] = votes[index] + 1
	end
	return votes
end

-- Whether real votes count, or the NPC crowd has to stand in.
function Scoring.UsesNpcCrowd(realVoterCount)
	return realVoterCount < PoseOff.MinRealVoters
end

-- entries = { { id = any, total = n, forfeited = bool }, ... }. Returns placements by id.
-- Forfeits always land last. Ties keep their input order, so results are stable.
function Scoring.Placements(entries)
	local order = {}
	for index, entry in ipairs(entries) do
		table.insert(order, { entry = entry, index = index })
	end
	table.sort(order, function(a, b)
		local aForfeit = a.entry.forfeited and 1 or 0
		local bForfeit = b.entry.forfeited and 1 or 0
		if aForfeit ~= bForfeit then
			return aForfeit < bForfeit
		end
		if a.entry.total ~= b.entry.total then
			return a.entry.total > b.entry.total
		end
		return a.index < b.index
	end)

	local placements = {}
	for place, item in ipairs(order) do
		placements[item.entry.id] = place
	end
	return placements
end

return Scoring
