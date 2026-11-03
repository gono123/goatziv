local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)

local Colors = World.Colors
local Config = World.Spawn

local function chevron(model, z)
	for _, side in ipairs({ -1, 1 }) do
		local where = CFrame.new(side * 1.7, 0.15, z) * CFrame.Angles(0, side * math.rad(45), 0)
		Build.part(
			model,
			"Arrow",
			Vector3.new(5, 0.06, 1),
			where,
			Colors.Orange,
			Enum.Material.Neon,
			{ CanCollide = false }
		)
	end
end

return function(parent)
	local model = Build.model(parent, "SpawnPlaza")
	local half = Config.PlazaSize / 2

	Build.floor(
		model,
		"Floor",
		Vector3.new(0, 0, 0),
		Config.PlazaSize,
		Config.PlazaSize,
		Colors.Concrete,
		Enum.Material.Concrete
	)

	-- Orange trim
	for _, side in ipairs({ -1, 1 }) do
		Build.part(
			model,
			"Trim",
			Vector3.new(Config.PlazaSize, 0.3, 1),
			Vector3.new(0, 0.05, side * half),
			Colors.Orange,
			Enum.Material.SmoothPlastic
		)
		Build.part(
			model,
			"Trim",
			Vector3.new(1, 0.3, Config.PlazaSize),
			Vector3.new(side * half, 0.05, 0),
			Colors.Orange,
			Enum.Material.SmoothPlastic
		)
	end

	-- Neon ring around the spawn point
	local ring = Config.Size.X + 2
	for _, side in ipairs({ -1, 1 }) do
		Build.part(
			model,
			"SpawnRing",
			Vector3.new(ring + 1, 0.1, 1),
			Vector3.new(0, 0.14, side * ring / 2),
			Colors.Orange,
			Enum.Material.Neon,
			{ CanCollide = false }
		)
		Build.part(
			model,
			"SpawnRing",
			Vector3.new(1, 0.1, ring + 1),
			Vector3.new(side * ring / 2, 0.14, 0),
			Colors.Orange,
			Enum.Material.Neon,
			{ CanCollide = false }
		)
	end

	-- Welcome arch
	for _, x in ipairs({ -15, 15 }) do
		Build.part(model, "Post", Vector3.new(1.5, 20, 1.5), Vector3.new(x, 10, -22), Colors.Dark, Enum.Material.Metal)
	end
	Build.sign(
		model,
		"WelcomeSign",
		"SIGMA GLOW-UP GYM",
		CFrame.new(0, 17, -22) * CFrame.Angles(0, math.rad(180), 0),
		30,
		6,
		Colors.Orange
	)

	-- Arrows and a path towards the Starter Gym
	for _, z in ipairs({ -12, -18, -28, -34 }) do
		chevron(model, z)
	end
	Build.floor(model, "Path", Vector3.new(0, 0, -32), 10, 16, Colors.Concrete, Enum.Material.Concrete)
end
