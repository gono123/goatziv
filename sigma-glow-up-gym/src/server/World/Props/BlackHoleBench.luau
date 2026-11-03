-- A bench under a black sphere with a purple neon ring and swirling particles.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)

return function(model, origin)
	Build.part(
		model,
		"Pad",
		Vector3.new(2, 0.7, 5),
		origin * CFrame.new(0, 1.8, 0),
		World.Colors.Purple,
		Enum.Material.Fabric
	)
	Build.part(
		model,
		"Support",
		Vector3.new(1.4, 1.5, 3),
		origin * CFrame.new(0, 0.75, 0),
		World.Colors.Dark,
		Enum.Material.Metal
	)

	local centre = (origin * CFrame.new(0, 7, -1)).Position
	local hole = Build.ball(model, "BlackHole", centre, 4, World.Colors.Black, Enum.Material.SmoothPlastic)
	Build.disc(model, "Ring", centre, 6.4, 0.2, World.Colors.Purple, Enum.Material.Neon, { CanCollide = false })

	local emitter = Build.particles(hole, "Swirl", World.Colors.Purple, 8, 0.4, 1, 1.5)
	emitter.RotSpeed = NumberRange.new(90, 180)
end
