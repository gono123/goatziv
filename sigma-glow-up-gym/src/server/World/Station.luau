-- Builds one training station: base, floor marker, label and the machine itself.
-- `where` is the machine's position on the floor, and the player stands on its +Z side.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Equipment = require(Shared.Config.Equipment)
local World = require(Shared.Config.World)

local Build = require(script.Parent.Build)

local Props = script.Parent.Props
local BUILDERS = {
	Dumbbells = require(Props.Dumbbells),
	Bench = require(Props.Bench),
	SquatRack = require(Props.SquatRack),
	TireFlip = require(Props.TireFlip),
	MeteorPress = require(Props.MeteorPress),
	BlackHoleBench = require(Props.BlackHoleBench),
}

local Station = {}

function Station.Build(parent, equipmentId, where)
	local def = Equipment[equipmentId]
	local model = Build.model(parent, equipmentId)
	local origin = CFrame.new(where)

	local base = Build.part(
		model,
		"Base",
		World.StationBaseSize,
		origin * CFrame.new(0, World.StationBaseSize.Y / 2, 0),
		World.Colors.Dark,
		Enum.Material.Metal
	)
	model.PrimaryPart = base

	BUILDERS[equipmentId](model, origin * CFrame.new(0, World.StationBaseSize.Y, 0))

	-- Thin neon square showing where the player stands. Coloured by the client when locked.
	Build.part(
		model,
		"StationMarker",
		Vector3.new(4, 0.06, 4),
		origin * CFrame.new(0, 0.13, World.StationStandOffset),
		World.Colors.Orange,
		Enum.Material.Neon,
		{ CanCollide = false, CanQuery = false }
	)

	local labelText = def.displayName .. "\n+" .. def.base .. " Aura/rep"
	Build.billboard(base, labelText, UDim2.fromOffset(180, 60), Vector3.new(0, def.size.Y + 3, 0), 70)

	model:SetAttribute("EquipmentId", equipmentId)
	model:AddTag("Equipment")
	return model
end

return Station
