-- Every map size and position (MASTER_PROMPT Part 5). Y = 0 is the top of the baseplate.

local World = {}

World.Colors = {
	Baseplate = Color3.fromRGB(58, 63, 75),
	Orange = Color3.fromRGB(255, 138, 31),
	Teal = Color3.fromRGB(31, 199, 182),
	Gold = Color3.fromRGB(212, 175, 55),
	Yellow = Color3.fromRGB(255, 210, 63),
	Pink = Color3.fromRGB(255, 92, 168),
	Purple = Color3.fromRGB(150, 60, 255),
	Concrete = Color3.fromRGB(150, 152, 158),
	Rubber = Color3.fromRGB(43, 43, 51),
	Asphalt = Color3.fromRGB(48, 52, 58),
	Marble = Color3.fromRGB(237, 230, 214),
	Black = Color3.fromRGB(15, 15, 20),
	Steel = Color3.fromRGB(120, 124, 132),
	Dark = Color3.fromRGB(60, 62, 70),
	White = Color3.fromRGB(245, 245, 245),
}

World.Lighting = {
	ClockTime = 14,
	Brightness = 2.5,
	AtmosphereDensity = 0.25,
	AtmosphereHaze = 1,
	BloomIntensity = 0.4,
	BloomThreshold = 1.2,
	Saturation = 0.1,
	Contrast = 0.05,
}

World.Spawn = {
	Position = Vector3.new(0, 0.5, 0),
	Size = Vector3.new(12, 1, 12),
	PlazaSize = 50,
}

World.StarterGym = {
	Center = Vector3.new(0, 0, -70),
	Size = Vector3.new(90, 0, 60),
	WallHeight = 4,
	MirrorHeight = 16,
	DumbbellX = { -32, -20, -8 },
	BenchX = { 8, 20, 32 },
	StationZ = -62,
}

World.IronYard = {
	Center = Vector3.new(110, 0, -70),
	Size = Vector3.new(90, 0, 70),
	FenceHeight = 14,
	GateWidth = 20,
	SquatX = { 90, 110, 130 },
	SquatZ = -88,
	TireX = { 90, 110, 130 },
	TireZ = -58,
}

World.MogMansion = {
	Center = Vector3.new(110, 0, -180),
	Size = Vector3.new(80, 0, 60),
	WallHeight = 18,
	DoorWidth = 16,
	DoorHeight = 14,
	PressX = { 82, 98, 114 },
	PressZ = -192,
	-- VIP lounge fills the north-east corner
	LoungeMinX = 126,
	LoungeMinZ = -188,
	LoungeDoorWidth = 8,
}

World.CosmicDojo = {
	Center = Vector3.new(0, 80, -210),
	Size = Vector3.new(70, 0, 70),
	BenchX = { -20, 0, 20 },
	StationZ = -222,
	LaunchPad = Vector3.new(0, 0, -120),
	Landing = Vector3.new(0, 85, -195),
	ReturnPad = Vector3.new(0, 80, -183),
	ReturnLanding = Vector3.new(0, 5, -108),
	PadDiameter = 12,
	PadCooldown = 2,
	UnlockStage = 6,
	UnlockGlowResets = 3,
}

World.Arena = {
	Center = Vector3.new(-110, 0, -70),
	StageSize = Vector3.new(44, 3, 20),
	PedestalX = { -15, -5, 5, 15 }, -- relative to the centre
	PedestalZ = -2,
	PedestalHeight = 1,
	QueuePad = Vector3.new(-110, 0, -52),
	QueuePadSize = 12,
	BleacherWidth = 60,
	BleacherStartZ = -44,
	BleacherDepth = 4,
	BleacherStepHeight = 2,
	BleacherTiers = 3,
	SpectatorSpot = Vector3.new(-110, 3, -44),
	ExitSpot = Vector3.new(-110, 3, -48),
}

World.TitanPlaza = {
	Center = Vector3.new(0, 0, 90),
	Radius = 55,
	Landing = Vector3.new(0, 0, 105),
	PillarPosition = Vector3.new(0, 0, 40),
	PillarHeight = 45,
	PillarWidth = 8,
}

World.DripShop = {
	Center = Vector3.new(-60, 0, 40),
	Size = Vector3.new(24, 12, 18),
}

World.HallOfMog = {
	Center = Vector3.new(60, 0, 40),
	Size = Vector3.new(50, 20, 2),
	BoardX = { -16, 0, 16 },
}

World.StationStandOffset = 5.5 -- studs in front of a machine where the player stands
World.StationBaseSize = Vector3.new(7, 0.3, 7)

-- Zone gates, lowest stage first. A player locked out of one is locked out of all later ones.
World.Gates = {
	{ zone = "IronYard", unlockStage = 3 },
	{ zone = "MogMansion", unlockStage = 5 },
}

return World
