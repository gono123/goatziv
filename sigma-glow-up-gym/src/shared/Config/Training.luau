-- Rep and Glow Reset tuning. Training is plain clicking: every click is one rep.

return {
	-- Minimum seconds between reps. This caps clicks at 5 per second, so spamming and
	-- simple auto-clickers gain little over a player who clicks quickly.
	RepCooldown = 0.2,
	-- The server allows reps slightly closer together, because network delay bunches clicks up.
	RepCooldownSlack = 0.6,

	-- Must be standing this close (studs) to the equipment to start training.
	TrainRange = 14,

	-- Glow Reset
	GlowResetBonus = 0.5, -- +50% Aura per reset, additive
	GlowShardsBase = 10,
	GlowShardsPerReset = 5,
}
