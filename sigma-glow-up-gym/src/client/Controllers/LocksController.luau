-- Local lock visuals: equipment labels and markers, and zone gates. Only looks: the
-- server enforces every lock on its own.

local CollectionService = game:GetService("CollectionService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Equipment = require(Shared.Config.Equipment)
local Stages = require(Shared.Config.Stages)
local World = require(Shared.Config.World)

local Theme = require(script.Parent.Parent.UI.Theme)

local TOAST_COOLDOWN = 3

local player = Players.LocalPlayer

local LocksController = {}

local HUD
local gateStages = {}
local lastToast = 0

local function unlockedEquipment(def, data)
	if data.stage >= def.unlockStage then
		return true
	end
	return def.unlockGlowResets ~= nil and data.glowResets >= def.unlockGlowResets
end

local function refreshEquipment(instance, data)
	local def = Equipment[instance:GetAttribute("EquipmentId")]
	if not def then
		return
	end
	local unlocked = unlockedEquipment(def, data)

	local label = instance:FindFirstChild("Label", true)
	local text = label and label:FindFirstChild("Text")
	if text then
		text.Text = def.displayName .. "\n+" .. def.base .. " Aura/rep"
		if not unlocked then
			text.Text = text.Text .. "\n🔒 " .. string.upper(Stages.Get(def.unlockStage).name)
		end
		text.TextColor3 = unlocked and Theme.Text or Theme.Dim
	end

	local marker = instance:FindFirstChild("StationMarker", true)
	if marker then
		marker.Color = unlocked and Theme.Orange or Theme.Danger
	end
end

local function isGateLocked(gate, data)
	local stage = gateStages[gate:GetAttribute("ZoneId")]
	return stage ~= nil and data.bestStage < stage
end

local function refreshGate(gate, data)
	local locked = isGateLocked(gate, data)
	gate.Transparency = locked and 0.4 or 1

	local sign = gate:FindFirstChild("LockSign")
	if sign then
		sign.Enabled = locked
		local stage = gateStages[gate:GetAttribute("ZoneId")]
		local text = sign:FindFirstChild("Text") -- with streaming, children can arrive a moment later
		if stage and text then
			text.Text = "🔒 Unlocks at " .. string.upper(Stages.Get(stage).name)
		end
	end
end

local function refreshAll(data)
	for _, instance in ipairs(CollectionService:GetTagged("Equipment")) do
		refreshEquipment(instance, data)
	end
	for _, gate in ipairs(CollectionService:GetTagged("ZoneGate")) do
		refreshGate(gate, data)
	end
end

local function hookGate(gate)
	local data = HUD.GetData()
	if data then
		refreshGate(gate, data)
	end

	gate.Touched:Connect(function(hit)
		local character = player.Character
		local latest = HUD.GetData()
		if not character or not latest or not hit:IsDescendantOf(character) or not isGateLocked(gate, latest) then
			return
		end
		if os.clock() - lastToast > TOAST_COOLDOWN then
			lastToast = os.clock()
			local stage = gateStages[gate:GetAttribute("ZoneId")]
			HUD.Toast("Unlocks at " .. string.upper(Stages.Get(stage).name) .. "!")
		end
	end)
end

function LocksController.Init(hud)
	HUD = hud
	for _, gate in ipairs(World.Gates) do
		gateStages[gate.zone] = gate.unlockStage
	end

	-- With streaming on, parts arrive as the player gets close.
	for _, gate in ipairs(CollectionService:GetTagged("ZoneGate")) do
		hookGate(gate)
	end
	CollectionService:GetInstanceAddedSignal("ZoneGate"):Connect(hookGate)
	CollectionService:GetInstanceAddedSignal("Equipment"):Connect(function(instance)
		local data = HUD.GetData()
		if data then
			refreshEquipment(instance, data)
		end
	end)

	HUD.OnData(refreshAll)
end

return LocksController
