local ReplicatedStorage = game:GetService("ReplicatedStorage")
local World = require(ReplicatedStorage:WaitForChild("Shared").Config.World)
local Build = require(script.Parent.Parent.Build)

local Colors = World.Colors
local Config = World.TitanPlaza

local STRIPES = 36
local CRACKS = 14

return function(parent)
	local model = Build.model(parent, "TitanPlaza")
	-- The clock must be visible from spawn, so never stream this model out.
	model.ModelStreamingMode = Enum.ModelStreamingMode.Persistent

	local c = Config.Center
	local r = Config.Radius

	Build.disc(model, "Ground", c, r * 2, 0.2, Colors.Concrete, Enum.Material.Concrete)

	-- Warning stripes around the edge
	for i = 1, STRIPES do
		local angle = (i / STRIPES) * math.pi * 2
		local where = CFrame.new(c + Vector3.new(math.cos(angle) * (r - 2), 0.12, math.sin(angle) * (r - 2)))
			* CFrame.Angles(0, -angle, 0)
		local color = (i % 2 == 0) and Colors.Yellow or Colors.Black
		Build.part(
			model,
			"Stripe",
			Vector3.new(4, 0.06, 8),
			where,
			color,
			Enum.Material.SmoothPlastic,
			{ CanCollide = false }
		)
	end

	-- Cracks, placed by a fixed pattern so every server looks the same
	for i = 1, CRACKS do
		local angle = i * 2.4
		local distance = 8 + (i * 13) % (r - 16)
		local where = CFrame.new(c + Vector3.new(math.cos(angle) * distance, 0.11, math.sin(angle) * distance))
			* CFrame.Angles(0, angle * 1.7, 0)
		Build.part(
			model,
			"Crack",
			Vector3.new(10 + i % 7, 0.04, 0.6),
			where,
			Colors.Dark,
			Enum.Material.Slate,
			{ CanCollide = false }
		)
	end

	-- Clock pillar with the countdown on all four sides
	local position = Config.PillarPosition
	local w = Config.PillarWidth
	local h = Config.PillarHeight
	Build.part(
		model,
		"ClockPillar",
		Vector3.new(w, h, w),
		position + Vector3.new(0, h / 2, 0),
		Colors.Dark,
		Enum.Material.Concrete
	)
	local clock = Build.part(
		model,
		"ClockFaces",
		Vector3.new(w + 0.4, w * 0.8, w + 0.4),
		position + Vector3.new(0, h - w * 0.6, 0),
		Colors.Black,
		Enum.Material.SmoothPlastic
	)
	for _, face in ipairs({ Enum.NormalId.Front, Enum.NormalId.Back, Enum.NormalId.Left, Enum.NormalId.Right }) do
		local gui = Build.surfaceText(clock, face, "TITAN\n--:--", Colors.Yellow, "Clock" .. face.Name)
		gui:AddTag("TitanClock")
	end
	Build.part(
		model,
		"Beacon",
		Vector3.new(w + 1, 1, w + 1),
		position + Vector3.new(0, h + 0.5, 0),
		Colors.Orange,
		Enum.Material.Neon
	)
end
