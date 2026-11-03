-- Padded red bench, two uprights and a loaded barbell.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)

return function(model, origin)
	Build.part(
		model,
		"Pad",
		Vector3.new(2, 0.7, 5),
		origin * CFrame.new(0, 1.8, 0),
		Color3.fromRGB(205, 50, 50),
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

	for _, x in ipairs({ -2, 2 }) do
		Build.part(
			model,
			"Upright",
			Vector3.new(0.4, 4.5, 0.4),
			origin * CFrame.new(x, 2.25, -2),
			World.Colors.Steel,
			Enum.Material.Metal
		)
	end

	local a = (origin * CFrame.new(-3.6, 4.5, -2)).Position
	local b = (origin * CFrame.new(3.6, 4.5, -2)).Position
	Build.cylinder(model, "Bar", a, b, 0.25, World.Colors.Steel, Enum.Material.Metal)

	for _, offset in ipairs({ { a, -1 }, { b, 1 } }) do
		for i = 0, 1 do
			local inner = offset[1] + Vector3.new(offset[2] * i * 0.4, 0, 0)
			Build.cylinder(
				model,
				"Plate",
				inner,
				inner + Vector3.new(offset[2] * 0.35, 0, 0),
				1.8 - i * 0.5,
				World.Colors.Black,
				Enum.Material.Metal
			)
		end
	end
end
