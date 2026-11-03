-- A large tyre lying flat. A darker disc on top fakes the hole.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)

return function(model, origin)
	local base = origin.Position
	Build.disc(model, "Tire", base + Vector3.new(0, 1, 0), 7, 2, World.Colors.Black, Enum.Material.Rubber)
	Build.disc(
		model,
		"Hole",
		base + Vector3.new(0, 2.02, 0),
		3.5,
		0.05,
		Color3.fromRGB(5, 5, 8),
		Enum.Material.SmoothPlastic,
		{ CanCollide = false }
	)
end
