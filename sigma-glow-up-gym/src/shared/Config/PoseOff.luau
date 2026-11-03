-- Pose-Off tuning (GDD section 7, BUILD_SPEC M5).

return {
	MinPlayers = 2,
	MaxPlayers = 4,
	QueueCountdown = 10,
	BotFillAfter = 30,
	Rounds = 3,
	WalkoutPerContestant = 2,
	PromptTime = 2,
	PoseTime = 5,
	ShowcaseTimePer = 2,
	VoteTime = 5,
	FinaleTime = 4,
	ResultsTime = 5,
	MeterPeriod = 1.2, -- power meter sweeps faster than the training bar
	Score = { TimingMax = 40, PromptMatch = 20, CrowdMax = 40 },
	NpcCrowdVotes = 10, -- used when fewer than MinRealVoters real spectators vote
	MinRealVoters = 2,
	Rewards = {
		Drip = { 30, 15, 5, 5 }, -- by placement
		AuraSurgeSeconds = { 180, 60, 0, 0 }, -- seconds of the player's estimated Aura rate
		VoterDripPerCorrectRound = 2,
		HypeBroDrip = 3, -- spectators who voted in every round
		FirstPoseOffDrip = 50, -- one-time bonus (FTUE)
	},
	SameOpponentLimitPerHour = 3, -- after this, rewards vs that opponent drop to 0
	AfkRoundsToForfeit = 2,
	AfkQueueCooldown = 60,
	Bot = {
		PromptMatchChance = 0.5,
		TimingMin = 12,
		TimingMax = 34,
		FirstMatchTimingMin = 8, -- a new player's first match is tuned to be winnable
		FirstMatchTimingMax = 20,
	},
	SpectatorRange = 90,
	OrbitSpeed = 1.5, -- radians per second

	Rating = {
		Start = 1000,
		K = 32,
		-- Ascending. A rating belongs to the last tier whose min it reaches.
		Tiers = {
			{ name = "Bronze Bro", min = 0, color = Color3.fromRGB(205, 127, 50) },
			{ name = "Silver Sigma", min = 1100, color = Color3.fromRGB(192, 200, 210) },
			{ name = "Gold Goat", min = 1250, color = Color3.fromRGB(255, 210, 63) },
			{ name = "Diamond Mogger", min = 1400, color = Color3.fromRGB(110, 225, 255) },
			{ name = "Cosmic Legend", min = 1600, color = Color3.fromRGB(255, 120, 230) },
		},
	},
}
