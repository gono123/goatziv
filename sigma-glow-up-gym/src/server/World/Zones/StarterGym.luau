local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)
local Station = require(script.Parent.Parent.Station)

local Colors = World.Colors
local Config = World.StarterGym

local function wall(model, size, position)
	Build.part(model, "HalfWall", size, position, Colors.Teal, Enum.Material.SmoothPlastic)
end

return function(parent)
	local model = Build.model(parent, "StarterGym")
	local c = Config.Center
	local halfX, halfZ = Config.Size.X / 2, Config.Size.Z / 2
	local h = Config.WallHeight
	local opening = 20

	Build.floor(model, "Floor", c, Config.Size.X, Config.Size.Z, Colors.Rubber, Enum.Material.Slate)

	-- South wall with a wide entrance, east and west walls with doorways.
	local southPiece = (Config.Size.X - 30) / 2
	for _, side in ipairs({ -1, 1 }) do
		wall(model, Vector3.new(southPiece, h, 1), Vector3.new(c.X + side * (15 + southPiece / 2), h / 2, c.Z + halfZ))
		local sidePiece = (Config.Size.Z - opening) / 2
		for _, end_ in ipairs({ -1, 1 }) do
			wall(
				model,
				Vector3.new(1, h, sidePiece),
				Vector3.new(c.X + side * halfX, h / 2, c.Z + end_ * (opening / 2 + sidePiece / 2))
			)
		end
	end

	-- Mirror back wall
	local mirrorZ = c.Z - halfZ
	Build.part(
		model,
		"BackWall",
		Vector3.new(Config.Size.X, Config.MirrorHeight, 1),
		Vector3.new(c.X, Config.MirrorHeight / 2, mirrorZ - 0.5),
		Colors.Dark,
		Enum.Material.Concrete
	)
	Build.part(
		model,
		"Mirror",
		Vector3.new(Config.Size.X - 4, Config.MirrorHeight - 8, 0.2),
		Vector3.new(c.X, (Config.MirrorHeight - 8) / 2 + 1, mirrorZ + 0.1),
		Colors.White,
		Enum.Material.Glass,
		{ Reflectance = 0.4, Transparency = 0.1 }
	)

	-- Motivational signs above the mirror
	local signY = Config.MirrorHeight - 3
	local signs = { { -28, "+1 AURA EVERY REP" }, { 0, "NO DAYS OFF" }, { 28, "GLOW UP OR GO HOME" } }
	for _, entry in ipairs(signs) do
		Build.sign(
			model,
			"Sign",
			entry[2],
			CFrame.new(c.X + entry[1], signY, mirrorZ + 0.3) * CFrame.Angles(0, math.rad(180), 0),
			24,
			4.5,
			Colors.Orange
		)
	end

	for _, x in ipairs(Config.DumbbellX) do
		Station.Build(model, "Dumbbells", Vector3.new(x, 0.1, Config.StationZ))
	end
	for _, x in ipairs(Config.BenchX) do
		Station.Build(model, "Bench", Vector3.new(x, 0.1, Config.StationZ))
	end
end
