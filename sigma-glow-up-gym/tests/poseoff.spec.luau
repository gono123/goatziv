local T = ...
local Scoring = T.load("src/shared/Logic/PoseOffScoring.luau")
local PoseOff = T.load("src/shared/Config/PoseOff.luau")

T.test("timing score peaks at the centre", function()
	T.eq(Scoring.Timing(0.5), PoseOff.Score.TimingMax)
	T.eq(Scoring.Timing(0), 0)
	T.eq(Scoring.Timing(1), 0)
	T.eq(Scoring.Timing(0.25), PoseOff.Score.TimingMax / 2)
	T.eq(Scoring.Timing(nil), 0, "no submission scores nothing")
end)

T.test("prompt match needs the tag", function()
	T.eq(Scoring.PromptMatch({ "flex", "aura" }, "aura"), PoseOff.Score.PromptMatch)
	T.eq(Scoring.PromptMatch({ "flex" }, "aura"), 0)
	T.eq(Scoring.PromptMatch(nil, "aura"), 0)
end)

T.test("crowd score is a vote share", function()
	T.eq(Scoring.Crowd(5, 10), PoseOff.Score.CrowdMax / 2)
	T.eq(Scoring.Crowd(0, 0), 0)
end)

T.test("npc crowd casts every vote and favours the higher score", function()
	local random = T.rng(42)
	local totals = { 0, 0 }
	for _ = 1, 200 do
		local votes = Scoring.NpcVotes({ 50, 10 }, PoseOff.NpcCrowdVotes, random)
		T.eq(votes[1] + votes[2], PoseOff.NpcCrowdVotes)
		totals[1] = totals[1] + votes[1]
		totals[2] = totals[2] + votes[2]
	end
	T.truthy(totals[1] > totals[2] * 2, "higher score should win most votes")
end)

T.test("npc crowd still votes when everyone scored zero", function()
	local votes = Scoring.NpcVotes({ 0, 0, 0 }, 9, T.rng(7))
	T.eq(votes[1] + votes[2] + votes[3], 9)
end)

T.test("npc crowd is used only without a real audience", function()
	T.truthy(Scoring.UsesNpcCrowd(0))
	T.truthy(Scoring.UsesNpcCrowd(1))
	T.falsy(Scoring.UsesNpcCrowd(2))
end)

T.test("placements sort by score and forfeits land last", function()
	local placements = Scoring.Placements({
		{ id = "quitter", total = 500, forfeited = true },
		{ id = "second", total = 100 },
		{ id = "first", total = 200 },
	})
	T.eq(placements.first, 1)
	T.eq(placements.second, 2)
	T.eq(placements.quitter, 3)
end)

T.test("ties keep a stable order", function()
	local placements = Scoring.Placements({ { id = "a", total = 10 }, { id = "b", total = 10 } })
	T.eq(placements.a, 1)
	T.eq(placements.b, 2)
end)
