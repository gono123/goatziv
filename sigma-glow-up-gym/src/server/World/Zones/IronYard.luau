local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)
local Station = require(script.Parent.Parent.Station)
local Gate = require(script.Parent.Parent.Gate)

local Colors = World.Colors
local Config = World.IronYard

local function fence(model, size, position)
	local h = Config.FenceHeight
	Build.part(
		model,
		"Fence",
		Vector3.new(size.X, h, size.Z),
		Vector3.new(position.X, h / 2, position.Z),
		Colors.Steel,
		Enum.Material.DiamondPlate,
		{ Transparency = 0.55 }
	)
end

local function floodlight(model, position, aim)
	Build.part(
		model,
		"Pole",
		Vector3.new(1, 24, 1),
		Vector3.new(position.X, 12, position.Z),
		Colors.Dark,
		Enum.Material.Metal
	)
	local lamp = Build.part(
		model,
		"Lamp",
		Vector3.new(4, 2, 1),
		CFrame.lookAt(Vector3.new(position.X, 24, position.Z), aim),
		Colors.White,
		Enum.Material.Neon
	)
	local light = Instance.new("SpotLight")
	light.Face = Enum.NormalId.Front
	light.Range = 60
	light.Angle = 80
	light.Brightness = 2
	light.Parent = lamp
end

return function(parent)
	local model = Build.model(parent, "IronYard")
	local c = Config.Center
	local halfX, halfZ = Config.Size.X / 2, Config.Size.Z / 2
	local minX, maxX = c.X - halfX, c.X + halfX
	local minZ, maxZ = c.Z - halfZ, c.Z + halfZ

	Build.floor(model, "Floor", c, Config.Size.X, Config.Size.Z, Colors.Asphalt, Enum.Material.Asphalt)

	fence(model, Vector3.new(Config.Size.X, 0, 1), Vector3.new(c.X, 0, minZ))
	fence(model, Vector3.new(Config.Size.X, 0, 1), Vector3.new(c.X, 0, maxZ))
	fence(model, Vector3.new(1, 0, Config.Size.Z), Vector3.new(maxX, 0, c.Z))

	-- West fence has the gate in the middle, facing the Starter Gym.
	local piece = (Config.Size.Z - Config.GateWidth) / 2
	for _, side in ipairs({ -1, 1 }) do
		fence(model, Vector3.new(1, 0, piece), Vector3.new(minX, 0, c.Z + side * (Config.GateWidth / 2 + piece / 2)))
	end
	Gate.Build(
		model,
		"IronYard",
		Vector3.new(1, Config.FenceHeight + 6, Config.GateWidth),
		Vector3.new(minX, (Config.FenceHeight + 6) / 2, c.Z)
	)

	for _, corner in ipairs({ { minX, minZ }, { maxX, minZ }, { minX, maxZ }, { maxX, maxZ } }) do
		floodlight(model, Vector3.new(corner[1], 0, corner[2]), c)
	end

	for _, x in ipairs(Config.SquatX) do
		Station.Build(model, "SquatRack", Vector3.new(x, 0.1, Config.SquatZ))
	end
	for _, x in ipairs(Config.TireX) do
		Station.Build(model, "TireFlip", Vector3.new(x, 0.1, Config.TireZ))
	end
end
