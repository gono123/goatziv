-- Gym equipment (GDD section 4.3).
-- Any Part or Model tagged "Equipment" with an attribute EquipmentId matching a key below
-- becomes trainable. If no tagged equipment exists, the server builds a greybox gym.
--
-- animationId (optional): "rbxassetid://..." lift animation played while training.

return {
	Dumbbells = {
		displayName = "Dumbbells",
		base = 1,
		unlockStage = 1,
		order = 1,
		color = Color3.fromRGB(90, 90, 100),
		size = Vector3.new(4, 3, 4),
		animationId = nil,
	},
	Bench = {
		displayName = "Bench",
		base = 3,
		unlockStage = 2,
		order = 2,
		color = Color3.fromRGB(200, 60, 60),
		size = Vector3.new(6, 3, 3),
		animationId = nil,
	},
	SquatRack = {
		displayName = "Squat Rack",
		base = 10,
		unlockStage = 3,
		order = 3,
		color = Color3.fromRGB(60, 160, 200),
		size = Vector3.new(6, 8, 4),
		animationId = nil,
	},
	TireFlip = {
		displayName = "Tire Flip",
		base = 30,
		unlockStage = 4,
		order = 4,
		color = Color3.fromRGB(40, 40, 40),
		size = Vector3.new(7, 3, 7),
		animationId = nil,
	},
	MeteorPress = {
		displayName = "Meteor Press",
		base = 100,
		unlockStage = 5,
		order = 5,
		color = Color3.fromRGB(255, 140, 40),
		size = Vector3.new(6, 6, 6),
		animationId = nil,
	},
	BlackHoleBench = {
		displayName = "Black Hole Bench",
		base = 400,
		unlockStage = 6,
		unlockGlowResets = 3, -- OR unlocked after 3 Glow Resets
		order = 6,
		color = Color3.fromRGB(30, 10, 60),
		size = Vector3.new(7, 4, 4),
		animationId = nil,
	},
}
