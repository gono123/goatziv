-- Debug panel for testing. Only appears for admins (the server re-checks every command).
-- Open with the wrench button or F8.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local UserInputService = game:GetService("UserInputService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Remotes = require(Shared.Remotes)

local Theme = require(script.Parent.Parent.UI.Theme)
local Components = require(script.Parent.Parent.UI.Components)

local player = Players.LocalPlayer

local DebugController = {}

local BUTTONS = {
	{ "+1K Aura", "AddAura", 1e3 },
	{ "+1M Aura", "AddAura", 1e6 },
	{ "+1B Aura", "AddAura", 1e9 },
	{ "Stage 1", "SetStage", 1 },
	{ "Stage 2", "SetStage", 2 },
	{ "Stage 3", "SetStage", 3 },
	{ "Stage 4", "SetStage", 4 },
	{ "Stage 5", "SetStage", 5 },
	{ "Stage 6", "SetStage", 6 },
	{ "+1,000 Drip", "AddDrip", 1000 },
	{ "+100 Shards", "AddShards", 100 },
	{ "Glow Reset now", "GlowResetNow" },
	{ "Start Titan", "StartTitan" },
	{ "Titan skip phase", "TitanSkipPhase" },
	{ "Pose-Off with bots", "StartPoseOffBots" },
	{ "Add bot to queue", "AddQueueBot" },
	{ "Day offset +1", "DayOffset" },
	{ "Fast mode on/off", "FastMode" },
	{ "Grant all poses", "GrantAllPoses" },
	{ "Grant all cosmetics", "GrantAllCosmetics" },
	{ "Reset my data", "ResetData", nil, true },
}

local built = false
local panel

local function addButtons(list, order)
	local grid = Instance.new("Frame")
	grid.BackgroundTransparency = 1
	grid.AutomaticSize = Enum.AutomaticSize.Y
	grid.Size = UDim2.fromScale(1, 0)
	grid.LayoutOrder = order
	grid.Parent = panel.Content

	local layout = Instance.new("UIGridLayout")
	layout.CellSize = UDim2.new(0.5, -4, 0, Theme.MinTapSize)
	layout.CellPadding = UDim2.fromOffset(6, 6)
	layout.SortOrder = Enum.SortOrder.LayoutOrder
	layout.Parent = grid

	for index, entry in ipairs(list) do
		local color = entry[4] and Theme.Danger or Theme.Teal
		local button = Components.Button(entry[1], color, UDim2.fromScale(1, 1))
		button.LayoutOrder = index
		button.TextSize = 15
		button.Parent = grid
		button.Activated:Connect(function()
			Remotes.DebugCommand:FireServer(entry[2], entry[3])
		end)
	end
end

local function build(HUD)
	if built then
		return
	end
	built = true

	panel = Components.Panel("Debug")
	addButtons(BUTTONS, 1)

	HUD.AddSideButton("Debug", "🛠️", "Debug", 200, panel.Toggle)

	UserInputService.InputBegan:Connect(function(input, gameProcessed)
		if not gameProcessed and input.KeyCode == Enum.KeyCode.F8 then
			panel.Toggle()
		end
	end)
end

-- Lets later systems add buttons, such as one per product. Each entry: { label, command, argument }.
function DebugController.AddButtons(list, order)
	if panel then
		addButtons(list, order)
	end
end

function DebugController.Init(HUD)
	local function check()
		if player:GetAttribute("IsAdmin") then
			build(HUD)
		end
	end
	player:GetAttributeChangedSignal("IsAdmin"):Connect(check)
	check()
end

return DebugController
