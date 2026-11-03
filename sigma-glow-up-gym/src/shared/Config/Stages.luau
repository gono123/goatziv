-- Evolution stages. Index 1 = Noob. All tuning lives here (see GDD section 4.2).
-- scale values multiply the player's own avatar proportions (R15 only).

local Stages = {}

Stages.List = {
	{
		name = "Noob",
		auraRequired = 0,
		multiplier = 1,
		scale = { width = 1.00, height = 1.00, depth = 1.00, head = 1.00 },
		auraColor = Color3.fromRGB(235, 235, 235),
		auraRate = 0, -- no aura particles yet
		sunglasses = false,
	},
	{
		name = "Gym Rat",
		auraRequired = 75,
		multiplier = 1.5,
		scale = { width = 1.10, height = 1.02, depth = 1.05, head = 1.00 },
		auraColor = Color3.fromRGB(120, 200, 255),
		auraRate = 4,
		sunglasses = false,
	},
	{
		name = "Chad",
		auraRequired = 1200,
		multiplier = 2.5,
		scale = { width = 1.25, height = 1.08, depth = 1.15, head = 1.00 },
		auraColor = Color3.fromRGB(80, 140, 255),
		auraRate = 8,
		sunglasses = false,
	},
	{
		name = "Sigma",
		auraRequired = 45000,
		multiplier = 4,
		scale = { width = 1.40, height = 1.12, depth = 1.25, head = 1.02 },
		auraColor = Color3.fromRGB(170, 90, 255),
		auraRate = 14,
		sunglasses = true,
	},
	{
		name = "Gigasigma",
		auraRequired = 500000,
		multiplier = 6,
		scale = { width = 1.55, height = 1.18, depth = 1.35, head = 1.04 },
		auraColor = Color3.fromRGB(255, 200, 60),
		auraRate = 20,
		sunglasses = true,
	},
	{
		name = "Cosmic Mogger",
		auraRequired = 10000000,
		multiplier = 10,
		scale = { width = 1.75, height = 1.25, depth = 1.45, head = 1.06 },
		auraColor = Color3.fromRGB(255, 120, 230),
		auraRate = 30,
		sunglasses = true,
	},
}

-- Stage index at which Glow Reset becomes available (5 = Gigasigma).
Stages.GlowResetStage = 5

-- Optional: put a licensed Roblox audio asset id here, e.g. "rbxassetid://123".
Stages.StageUpSoundId = ""

function Stages.Get(index)
	return Stages.List[math.clamp(index, 1, #Stages.List)]
end

return Stages
