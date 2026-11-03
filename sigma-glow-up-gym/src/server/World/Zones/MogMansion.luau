local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)
local Station = require(script.Parent.Parent.Station)
local Gate = require(script.Parent.Parent.Gate)

local Colors = World.Colors
local Config = World.MogMansion

local function wall(model, size, position)
	Build.part(model, "Wall", size, position, Colors.Marble, Enum.Material.Marble)
end

local function chandelier(model, position, height)
	Build.part(
		model,
		"Chain",
		Vector3.new(0.2, 4, 0.2),
		Vector3.new(position.X, height - 2, position.Z),
		Colors.Gold,
		Enum.Material.Foil
	)
	local bulb = Build.ball(
		model,
		"Chandelier",
		Vector3.new(position.X, height - 5, position.Z),
		3,
		Colors.Yellow,
		Enum.Material.Neon
	)
	local light = Instance.new("PointLight")
	light.Color = Colors.Yellow
	light.Range = 40
	light.Brightness = 2
	light.Parent = bulb
end

return function(parent)
	local model = Build.model(parent, "MogMansion")
	local c = Config.Center
	local h = Config.WallHeight
	local halfX, halfZ = Config.Size.X / 2, Config.Size.Z / 2
	local minX, maxX = c.X - halfX, c.X + halfX
	local minZ, maxZ = c.Z - halfZ, c.Z + halfZ

	Build.floor(model, "Floor", c, Config.Size.X, Config.Size.Z, Colors.Marble, Enum.Material.Marble)

	-- Outer walls and roof
	wall(model, Vector3.new(Config.Size.X, h, 1), Vector3.new(c.X, h / 2, minZ))
	wall(model, Vector3.new(1, h, Config.Size.Z), Vector3.new(minX, h / 2, c.Z))
	wall(model, Vector3.new(1, h, Config.Size.Z), Vector3.new(maxX, h / 2, c.Z))
	Build.part(
		model,
		"Roof",
		Vector3.new(Config.Size.X + 2, 1, Config.Size.Z + 2),
		Vector3.new(c.X, h + 0.5, c.Z),
		Colors.Gold,
		Enum.Material.Foil
	)

	-- South wall with the gated doorway
	local piece = (Config.Size.X - Config.DoorWidth) / 2
	for _, side in ipairs({ -1, 1 }) do
		wall(model, Vector3.new(piece, h, 1), Vector3.new(c.X + side * (Config.DoorWidth / 2 + piece / 2), h / 2, maxZ))
	end
	local lintel = h - Config.DoorHeight
	wall(model, Vector3.new(Config.DoorWidth, lintel, 1), Vector3.new(c.X, Config.DoorHeight + lintel / 2, maxZ))
	Gate.Build(
		model,
		"MogMansion",
		Vector3.new(Config.DoorWidth, Config.DoorHeight, 1),
		Vector3.new(c.X, Config.DoorHeight / 2, maxZ)
	)

	-- Gold trim along the top of the front
	Build.part(
		model,
		"Trim",
		Vector3.new(Config.Size.X, 1, 1.4),
		Vector3.new(c.X, h - 0.5, maxZ),
		Colors.Gold,
		Enum.Material.Foil
	)
	Build.sign(
		model,
		"MansionSign",
		"MOG MANSION",
		CFrame.new(c.X, Config.DoorHeight + 2, maxZ + 0.8) * CFrame.Angles(0, math.rad(180), 0),
		28,
		4,
		Colors.Gold,
		Colors.Black,
		Enum.Material.Foil
	)

	chandelier(model, Vector3.new(c.X - 20, 0, c.Z - 5), h)
	chandelier(model, Vector3.new(c.X + 5, 0, c.Z + 5), h)

	-- VIP lounge in the north-east corner, door opened by the VIP pass.
	local loungeMinX, loungeMinZ = Config.LoungeMinX, Config.LoungeMinZ
	local depth = loungeMinZ - minZ
	local doorWidth = Config.LoungeDoorWidth
	local doorZ = minZ + depth / 2
	wall(model, Vector3.new(maxX - loungeMinX, h, 1), Vector3.new((loungeMinX + maxX) / 2, h / 2, loungeMinZ))
	local sidePiece = (depth - doorWidth) / 2
	for _, side in ipairs({ -1, 1 }) do
		wall(
			model,
			Vector3.new(1, h, sidePiece),
			Vector3.new(loungeMinX, h / 2, doorZ + side * (doorWidth / 2 + sidePiece / 2))
		)
	end
	wall(model, Vector3.new(1, h - 10, doorWidth), Vector3.new(loungeMinX, 10 + (h - 10) / 2, doorZ))
	Build.part(
		model,
		"VIPDoor",
		Vector3.new(1, 10, doorWidth),
		Vector3.new(loungeMinX, 5, doorZ),
		Colors.Gold,
		Enum.Material.Foil,
		{ Transparency = 0.3 }
	)
	Build.sign(
		model,
		"VIPSign",
		"VIP LOUNGE",
		CFrame.new(loungeMinX - 0.8, 12.5, doorZ) * CFrame.Angles(0, math.rad(90), 0),
		10,
		2.5,
		Colors.Gold,
		Colors.Black,
		Enum.Material.Foil
	)
	Build.part(
		model,
		"VIPCouch",
		Vector3.new(12, 2, 4),
		Vector3.new((loungeMinX + maxX) / 2, 1, minZ + 4),
		Color3.fromRGB(120, 30, 60),
		Enum.Material.Fabric
	)

	for _, x in ipairs(Config.PressX) do
		Station.Build(model, "MeteorPress", Vector3.new(x, 0.1, Config.PressZ))
	end
end
