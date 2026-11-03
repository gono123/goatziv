-- Two tall uprights, a crossbar and a barbell with big plates.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)

return function(model, origin)
	for _, x in ipairs({ -3, 3 }) do
		for _, z in ipairs({ -1.5, 1.5 }) do
			Build.part(
				model,
				"Upright",
				Vector3.new(0.5, 9, 0.5),
				origin * CFrame.new(x, 4.5, z),
				World.Colors.Teal,
				Enum.Material.Metal
			)
		end
		Build.part(
			model,
			"TopBar",
			Vector3.new(0.5, 0.5, 3.5),
			origin * CFrame.new(x, 9, 0),
			World.Colors.Teal,
			Enum.Material.Metal
		)
	end
	Build.part(
		model,
		"Crossbar",
		Vector3.new(6.5, 0.5, 0.5),
		origin * CFrame.new(0, 9, -1.5),
		World.Colors.Teal,
		Enum.Material.Metal
	)

	local a = (origin * CFrame.new(-4.5, 5.5, 0)).Position
	local b = (origin * CFrame.new(4.5, 5.5, 0)).Position
	Build.cylinder(model, "Bar", a, b, 0.3, World.Colors.Steel, Enum.Material.Metal)
	Build.cylinder(model, "Plate", a, a + Vector3.new(-0.5, 0, 0), 3, World.Colors.Black, Enum.Material.Metal)
	Build.cylinder(model, "Plate", b, b + Vector3.new(0.5, 0, 0), 3, World.Colors.Black, Enum.Material.Metal)
end
