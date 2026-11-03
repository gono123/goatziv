local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)

local Colors = World.Colors
local Config = World.DripShop

local function mannequin(model, position, color)
	Build.part(
		model,
		"Legs",
		Vector3.new(1.6, 3, 0.9),
		position + Vector3.new(0, 1.5, 0),
		Colors.Dark,
		Enum.Material.SmoothPlastic
	)
	Build.part(model, "Torso", Vector3.new(2.4, 2.4, 1), position + Vector3.new(0, 4.2, 0), color, Enum.Material.Fabric)
	Build.ball(model, "Head", position + Vector3.new(0, 6.1, 0), 1.3, Colors.White)
end

return function(parent)
	local model = Build.model(parent, "DripShop")
	local c = Config.Center
	local s = Config.Size
	local minX, maxX = c.X - s.X / 2, c.X + s.X / 2
	local minZ, maxZ = c.Z - s.Z / 2, c.Z + s.Z / 2

	Build.floor(model, "Floor", c, s.X, s.Z, Colors.White, Enum.Material.SmoothPlastic)

	-- Back and side walls. The front faces east, towards the plaza, and stays open.
	Build.part(
		model,
		"Wall",
		Vector3.new(1, s.Y, s.Z),
		Vector3.new(minX, s.Y / 2, c.Z),
		Colors.Pink,
		Enum.Material.SmoothPlastic
	)
	for _, z in ipairs({ minZ, maxZ }) do
		Build.part(
			model,
			"Wall",
			Vector3.new(s.X, s.Y, 1),
			Vector3.new(c.X, s.Y / 2, z),
			Colors.Pink,
			Enum.Material.SmoothPlastic
		)
	end
	Build.part(
		model,
		"Roof",
		Vector3.new(s.X + 3, 1, s.Z + 2),
		Vector3.new(c.X + 0.5, s.Y + 0.5, c.Z),
		Colors.Teal,
		Enum.Material.SmoothPlastic
	)
	Build.sign(
		model,
		"ShopSign",
		"DRIP SHOP",
		CFrame.new(maxX + 1, s.Y - 1.5, c.Z) * CFrame.Angles(0, math.rad(-90), 0),
		16,
		3,
		Colors.Teal
	)

	local counter = Build.part(
		model,
		"Counter",
		Vector3.new(3, 3, 10),
		Vector3.new(c.X - 3, 1.5, c.Z),
		Colors.Teal,
		Enum.Material.SmoothPlastic
	)
	counter:AddTag("DripShopCounter")

	mannequin(model, Vector3.new(c.X + 4, 0.1, minZ + 3), Colors.Orange)
	mannequin(model, Vector3.new(c.X + 4, 0.1, maxZ - 3), Colors.Purple)
end
