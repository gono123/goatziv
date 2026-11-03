-- Builds placeholder equipment so the game is playable on an empty Baseplate.
-- Skipped automatically once you place your own equipment tagged "Equipment".

local CollectionService = game:GetService("CollectionService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Equipment = require(Shared.Config.Equipment)
local Stages = require(Shared.Config.Stages)

local SPACING = 14
local ROW_Z = -30
local FLOOR_Y = 0 -- top of the default Baseplate

local Greybox = {}

local function makeLabel(part, def)
	local billboard = Instance.new("BillboardGui")
	billboard.Name = "Label"
	billboard.Size = UDim2.fromOffset(220, 60)
	billboard.StudsOffset = Vector3.new(0, def.size.Y / 2 + 2.5, 0)
	billboard.MaxDistance = 90
	billboard.Parent = part

	local label = Instance.new("TextLabel")
	label.Size = UDim2.fromScale(1, 1)
	label.BackgroundTransparency = 1
	label.Font = Enum.Font.FredokaOne
	label.TextScaled = true
	label.TextColor3 = Color3.new(1, 1, 1)
	label.TextStrokeTransparency = 0.3

	local unlock = Stages.Get(def.unlockStage).name
	label.Text = def.displayName .. "\n+" .. def.base .. " Aura/rep  |  " .. unlock
	label.Parent = billboard
end

function Greybox.Build()
	if #CollectionService:GetTagged("Equipment") > 0 then
		return
	end

	local folder = Instance.new("Folder")
	folder.Name = "GreyboxGym"

	local ids = {}
	for id in pairs(Equipment) do
		table.insert(ids, id)
	end
	table.sort(ids, function(a, b)
		return Equipment[a].order < Equipment[b].order
	end)

	for index, id in ipairs(ids) do
		local def = Equipment[id]
		local part = Instance.new("Part")
		part.Name = id
		part.Anchored = true
		part.Size = def.size
		part.Color = def.color
		part.Material = Enum.Material.SmoothPlastic
		part.TopSurface = Enum.SurfaceType.Smooth
		local x = (index - (#ids + 1) / 2) * SPACING
		part.Position = Vector3.new(x, FLOOR_Y + def.size.Y / 2, ROW_Z)
		part:SetAttribute("EquipmentId", id)
		makeLabel(part, def)
		part.Parent = folder
		CollectionService:AddTag(part, "Equipment")
	end

	folder.Parent = workspace
end

return Greybox
