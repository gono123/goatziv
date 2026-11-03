-- Steel frame holding a glowing orange meteor.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)

return function(model, origin)
	for _, x in ipairs({ -3, 3 }) do
		Build.part(
			model,
			"Frame",
			Vector3.new(0.6, 9, 0.6),
			origin * CFrame.new(x, 4.5, 0),
			World.Colors.Steel,
			Enum.Material.Metal
		)
	end
	Build.part(
		model,
		"TopFrame",
		Vector3.new(6.6, 0.6, 0.6),
		origin * CFrame.new(0, 9, 0),
		World.Colors.Steel,
		Enum.Material.Metal
	)

	local meteor = Build.ball(
		model,
		"Meteor",
		(origin * CFrame.new(0, 5, 0)).Position,
		4.4,
		World.Colors.Orange,
		Enum.Material.Neon
	)

	local light = Instance.new("PointLight")
	light.Color = World.Colors.Orange
	light.Range = 18
	light.Brightness = 2
	light.Parent = meteor

	Build.particles(meteor, "Sparks", World.Colors.Orange, 6, 0.5, 1.5, 1.2)
end
