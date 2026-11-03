-- Low rack with two dumbbells.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)

local function dumbbell(model, centre)
	local left = centre + Vector3.new(-0.9, 0, 0)
	local right = centre + Vector3.new(0.9, 0, 0)
	Build.cylinder(model, "Handle", left, right, 0.3, World.Colors.Steel, Enum.Material.Metal)
	Build.cylinder(model, "Plate", left, left + Vector3.new(-0.5, 0, 0), 1, World.Colors.Black, Enum.Material.Metal)
	Build.cylinder(model, "Plate", right, right + Vector3.new(0.5, 0, 0), 1, World.Colors.Black, Enum.Material.Metal)
end

return function(model, origin)
	local shelf = origin * CFrame.new(0, 1.5, 0)
	Build.part(model, "Shelf", Vector3.new(6, 0.4, 2.4), shelf, World.Colors.Steel, Enum.Material.Metal)
	for _, x in ipairs({ -2.6, 2.6 }) do
		Build.part(
			model,
			"Leg",
			Vector3.new(0.4, 1.5, 2),
			origin * CFrame.new(x, 0.75, 0),
			World.Colors.Dark,
			Enum.Material.Metal
		)
	end
	dumbbell(model, (origin * CFrame.new(-1.4, 2.3, 0)).Position)
	dumbbell(model, (origin * CFrame.new(1.4, 2.3, 0)).Position)
end
