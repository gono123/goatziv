local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)

local Colors = World.Colors
local Config = World.Arena

return function(parent)
	local model = Build.model(parent, "PoseOffArena")
	-- The arena lights must be visible from spawn, so never stream this model out.
	model.ModelStreamingMode = Enum.ModelStreamingMode.Persistent

	local c = Config.Center
	local size = Config.StageSize

	Build.part(
		model,
		"Stage",
		size,
		c + Vector3.new(0, size.Y / 2, 0),
		Colors.Black,
		Enum.Material.Glass,
		{ Reflectance = 0.3 }
	)

	local rigZ = c.Z + Config.PedestalZ
	for index, offset in ipairs(Config.PedestalX) do
		local top = size.Y + Config.PedestalHeight
		local pedestal = Build.disc(
			model,
			"Pedestal" .. index,
			Vector3.new(c.X + offset, size.Y + Config.PedestalHeight / 2, rigZ),
			5,
			Config.PedestalHeight,
			Colors.Gold,
			Enum.Material.Foil
		)
		pedestal:SetAttribute("StandY", top)

		-- A spotlight on the rig above each pedestal
		local lamp = Build.part(
			model,
			"Spotlight" .. index,
			Vector3.new(2, 1, 2),
			Vector3.new(c.X + offset, 24, rigZ),
			Colors.White,
			Enum.Material.Neon
		)
		local spot = Instance.new("SpotLight")
		spot.Name = "Light"
		spot.Face = Enum.NormalId.Bottom
		spot.Range = 40
		spot.Angle = 35
		spot.Brightness = 4
		spot.Parent = lamp
	end

	-- Rig and light towers
	for _, x in ipairs({ -size.X / 2, size.X / 2 }) do
		Build.part(
			model,
			"RigPost",
			Vector3.new(1.5, 25, 1.5),
			Vector3.new(c.X + x, 12.5, rigZ),
			Colors.Dark,
			Enum.Material.Metal
		)
		local tower = Build.part(
			model,
			"LightTower",
			Vector3.new(2, 40, 2),
			Vector3.new(c.X + x * 1.15, 20, c.Z - size.Z / 2),
			Colors.Orange,
			Enum.Material.Neon
		)
		Build.particles(tower, "Glow", Colors.Yellow, 3, 0.6, 1, 2)
	end
	Build.part(
		model,
		"RigBar",
		Vector3.new(size.X + 1.5, 1.5, 1.5),
		Vector3.new(c.X, 25, rigZ),
		Colors.Dark,
		Enum.Material.Metal
	)

	-- Giant neon sign behind the stage
	Build.sign(
		model,
		"PoseOffSign",
		"POSE-OFF",
		CFrame.new(c.X, 16, c.Z - size.Z / 2 - 1) * CFrame.Angles(0, math.rad(180), 0),
		36,
		10,
		Colors.Pink,
		Colors.White,
		Enum.Material.Neon
	)

	-- Scoreboard to the side of the stage
	local board = Build.part(
		model,
		"ScoreboardPanel",
		Vector3.new(18, 14, 1),
		CFrame.new(c.X - size.X / 2 - 8, 9, c.Z) * CFrame.Angles(0, math.rad(180), 0),
		Colors.Black,
		Enum.Material.SmoothPlastic
	)
	Build.surfaceText(board, Enum.NormalId.Front, "POSE-OFF\nJoin on the glowing pad!", Colors.Yellow, "Scoreboard")

	-- Queue pad
	local pad = Build.part(
		model,
		"QueuePad",
		Vector3.new(Config.QueuePadSize, 0.4, Config.QueuePadSize),
		Config.QueuePad + Vector3.new(0, 0.2, 0),
		Colors.Pink,
		Enum.Material.Neon,
		{ CanCollide = false }
	)
	Build.billboard(pad, "POSE-OFF: 0/4", UDim2.fromOffset(240, 70), Vector3.new(0, 7, 0), 120, "QueueLabel")

	-- Bleachers
	local bleachers = Build.model(model, "Bleachers")
	for tier = 1, Config.BleacherTiers do
		local height = tier * Config.BleacherStepHeight
		Build.part(
			bleachers,
			"Tier" .. tier,
			Vector3.new(Config.BleacherWidth, height, Config.BleacherDepth),
			Vector3.new(c.X, height / 2, Config.BleacherStartZ + (tier - 1) * Config.BleacherDepth),
			Colors.Dark,
			Enum.Material.Concrete
		)
	end
end
