-- Daily quest pool (GDD section 10, BUILD_SPEC M7).

return {
	PerDay = 3,
	RerollsPerDay = 1,
	Pool = {
		{ id = "reps100", kind = "reps", target = 100, drip = 15, text = "Do 100 reps" },
		{ id = "reps300", kind = "reps", target = 300, drip = 30, text = "Do 300 reps" },
		{ id = "poseWin1", kind = "poseOffWins", target = 1, drip = 30, text = "Win 1 Pose-Off" },
		{ id = "poseWin2", kind = "poseOffWins", target = 2, drip = 50, text = "Win 2 Pose-Offs" },
		{ id = "posePlay2", kind = "poseOffsPlayed", target = 2, drip = 20, text = "Play 2 Pose-Offs" },
		{ id = "votes5", kind = "votes", target = 5, drip = 15, text = "Vote in 5 Pose-Off rounds" },
		{ id = "titanHits10", kind = "titanHits", target = 10, drip = 25, text = "Land 10 hits on the Titan" },
		{ id = "stageUp1", kind = "stageUps", target = 1, drip = 25, text = "Reach a new stage" },
	},
}
