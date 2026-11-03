-- Rep mini-game + reset tuning (GDD sections 4.4, 4.5, 5).

return {
	-- Marker sweeps 0 -> 1 -> 0 once per Period seconds, so it crosses the
	-- center (gold zone) every Period / 2 seconds.
	Period = 2.0,

	-- Zones are measured as distance from the center of the bar (0..0.5).
	GoldHalfWidth = 0.06,
	GoldHalfWidthLockedIn = 0.09, -- gold zone widens in LOCKED IN mode
	GreenHalfWidth = 0.20,

	Quality = {
		Perfect = 2.0,
		Good = 1.0,
		Miss = 0.25,
	},

	-- Minimum time between reps. Stops tap-spamming from beating good timing.
	RepCooldown = 0.8,

	LockedInCombo = 20, -- consecutive Perfects needed
	LockedInMultiplier = 1.5,

	-- How far a client tap timestamp may be from server time before it's clamped.
	TapTolerancePast = 0.75,
	TapToleranceFuture = 0.15,

	-- Must be standing this close (studs) to the equipment to start training.
	TrainRange = 14,

	-- Glow Reset
	GlowResetBonus = 0.5, -- +50% Aura per reset, additive
	GlowShardsBase = 10,
	GlowShardsPerReset = 5,

	-- Anti-exploit logging
	FlagMinReps = 200,
	FlagPerfectRatio = 0.95,
}
