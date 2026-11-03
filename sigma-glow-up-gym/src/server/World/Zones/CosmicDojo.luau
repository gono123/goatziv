local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)
local Station = require(script.Parent.Parent.Station)

local Colors = World.Colors
local Config = World.CosmicDojo

local function pad(parent, name, position, text)
	local part = Build.disc(
		parent,
		name,
		position + Vector3.new(0, 0.2, 0),
		Config.PadDiameter,
		0.4,
		Colors.Purple,
		Enum.Material.Neon
	)
	Build.billboard(part, text, UDim2.fromOffset(240, 60), Vector3.new(0, 6, 0), 90)
	return part
end

return function(parent)
	local model = Build.model(parent, "CosmicDojo")
	local c = Config.Center
	local halfX, halfZ = Config.Size.X / 2, Config.Size.Z / 2

	local floor = Build.part(
		model,
		"Floor",
		Vector3.new(Config.Size.X, 1, Config.Size.Z),
		c - Vector3.new(0, 0.5, 0),
		Colors.Black,
		Enum.Material.Glass,
		{ Reflectance = 0.25 }
	)
	Build.particles(floor, "Stars", Colors.White, 10, 0.3, 0.5, 4)

	-- Neon purple edges: low rails so nobody walks off by accident.
	for _, side in ipairs({ -1, 1 }) do
		Build.part(
			model,
			"Edge",
			Vector3.new(Config.Size.X, 1.5, 1),
			c + Vector3.new(0, 0.75, side * halfZ),
			Colors.Purple,
			Enum.Material.Neon
		)
		Build.part(
			model,
			"Edge",
			Vector3.new(1, 1.5, Config.Size.Z),
			c + Vector3.new(side * halfX, 0.75, 0),
			Colors.Purple,
			Enum.Material.Neon
		)
	end

	for _, x in ipairs(Config.BenchX) do
		Station.Build(model, "BlackHoleBench", Vector3.new(x, c.Y + 0.1, Config.StationZ))
	end

	pad(parent, "LaunchPad", Config.LaunchPad, "STEP HERE: FLY TO COSMIC DOJO")

	-- A tall glowing column, so the way up can be seen from across the map.
	Build.cylinder(
		parent,
		"LaunchBeam",
		Config.LaunchPad,
		Config.LaunchPad + Vector3.new(0, Config.LaunchBeamHeight, 0),
		Config.PadDiameter - 2,
		Colors.Purple,
		Enum.Material.Neon,
		{ Transparency = 0.7, CanCollide = false, CanQuery = false, CanTouch = false }
	)

	pad(model, "ReturnPad", Config.ReturnPad, "BACK DOWN")
end
