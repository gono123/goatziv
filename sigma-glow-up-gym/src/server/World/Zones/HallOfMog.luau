local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)

local Colors = World.Colors
local Config = World.HallOfMog

local BOARDS = {
	{ name = "BoardAura", title = "WEEKLY AURA" },
	{ name = "BoardRating", title = "SEASON RATING" },
	{ name = "BoardTitan", title = "TITAN HITS" },
}

return function(parent)
	local model = Build.model(parent, "HallOfMog")
	local c = Config.Center
	local s = Config.Size
	local midY = s.Y / 2

	Build.part(
		model,
		"Wall",
		Vector3.new(s.X, s.Y, s.Z),
		Vector3.new(c.X, midY, c.Z),
		Colors.Black,
		Enum.Material.Concrete
	)

	-- Gold frame
	for _, y in ipairs({ 0.5, s.Y - 0.5 }) do
		Build.part(
			model,
			"Frame",
			Vector3.new(s.X + 2, 1, s.Z + 1),
			Vector3.new(c.X, y, c.Z),
			Colors.Gold,
			Enum.Material.Foil
		)
	end
	for _, x in ipairs({ -s.X / 2, s.X / 2 }) do
		Build.part(
			model,
			"Frame",
			Vector3.new(1, s.Y, s.Z + 1),
			Vector3.new(c.X + x, midY, c.Z),
			Colors.Gold,
			Enum.Material.Foil
		)
	end

	-- Faces north, towards the spawn plaza.
	Build.sign(
		model,
		"HallSign",
		"HALL OF MOG",
		CFrame.new(c.X, s.Y + 2.5, c.Z),
		30,
		4,
		Colors.Gold,
		Colors.Black,
		Enum.Material.Foil
	)
	for index, board in ipairs(BOARDS) do
		local part = Build.part(
			model,
			board.name,
			Vector3.new(14, 15, 0.4),
			Vector3.new(c.X + Config.BoardX[index], midY, c.Z - s.Z / 2 - 0.2),
			Colors.Dark,
			Enum.Material.SmoothPlastic
		)
		Build.surfaceText(part, Enum.NormalId.Front, board.title .. "\nComing soon", Colors.Yellow, "Board")
	end
end
