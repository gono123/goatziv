-- Stage name, Aura, progress bar, side buttons, Glow Reset button. Other controllers
-- add their buttons and chips through this module.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Stages = require(Shared.Config.Stages)
local NumberFormat = require(Shared.NumberFormat)
local Remotes = require(Shared.Remotes)

local Theme = require(script.Parent.Parent.UI.Theme)
local Components = require(script.Parent.Parent.UI.Components)

local HUD = {}

local gui, stageLabel, auraLabel, setProgress, progressFill, progressText, resetButton
local sideColumn, chipRow, topRight
local data = nil
local resetArmedUntil = 0
local listeners = {}
local sideButtons = {}

local function build()
	gui = Components.ScreenGui("HUD", 1)

	-- Top centre: stage, Aura, progress
	local top = Instance.new("Frame")
	top.Name = "Top"
	top.AnchorPoint = Vector2.new(0.5, 0)
	top.Position = UDim2.new(0.5, 0, 0, 6)
	top.Size = UDim2.new(0.5, 0, 0, 84)
	top.BackgroundTransparency = 1
	top.Parent = gui

	local limit = Instance.new("UISizeConstraint")
	limit.MaxSize = Vector2.new(300, 84)
	limit.Parent = top

	stageLabel = Components.Label("", 24)
	stageLabel.Name = "Stage"
	stageLabel.Size = UDim2.new(1, 0, 0, 28)
	stageLabel.Parent = top

	auraLabel = Components.Label("", 20)
	auraLabel.Name = "Aura"
	auraLabel.Position = UDim2.fromOffset(0, 28)
	auraLabel.Size = UDim2.new(1, 0, 0, 24)
	auraLabel.TextColor3 = Theme.Gold
	auraLabel.Parent = top

	local bar
	bar, setProgress = Components.ProgressBar(UDim2.new(1, 0, 0, 24))
	bar.Name = "Progress"
	bar.Position = UDim2.fromOffset(0, 56)
	bar.Parent = top
	progressFill = bar.Fill

	progressText = Components.Label("", 13)
	progressText.Name = "Text"
	progressText.Size = UDim2.fromScale(1, 1)
	progressText.ZIndex = 2
	progressText.Parent = bar

	-- Left column. Wraps into more columns on short screens, and stops above the thumbstick.
	sideColumn = Instance.new("Frame")
	sideColumn.Name = "SideColumn"
	sideColumn.Position = UDim2.fromOffset(8, Theme.TopBarHeight)
	sideColumn.Size = UDim2.new(0, 220, 1, -(Theme.TopBarHeight + 170))
	sideColumn.BackgroundTransparency = 1
	sideColumn.Parent = gui

	local layout = Instance.new("UIListLayout")
	layout.FillDirection = Enum.FillDirection.Vertical
	layout.Wraps = true
	layout.SortOrder = Enum.SortOrder.LayoutOrder
	layout.Padding = UDim.new(0, 4)
	layout.Parent = sideColumn

	-- Boost chips, right of the side column
	chipRow = Instance.new("Frame")
	chipRow.Name = "Chips"
	chipRow.Position = UDim2.fromOffset(84, Theme.TopBarHeight + 34)
	chipRow.Size = UDim2.new(0.5, -84, 0, 30)
	chipRow.BackgroundTransparency = 1
	chipRow.Parent = gui

	local chipLayout = Instance.new("UIListLayout")
	chipLayout.FillDirection = Enum.FillDirection.Horizontal
	chipLayout.SortOrder = Enum.SortOrder.LayoutOrder
	chipLayout.Padding = UDim.new(0, 6)
	chipLayout.Parent = chipRow

	-- Top right: Titan timer
	topRight = Instance.new("Frame")
	topRight.Name = "TopRight"
	topRight.AnchorPoint = Vector2.new(1, 0)
	topRight.Position = UDim2.new(1, -8, 0, Theme.TopBarHeight)
	topRight.Size = UDim2.fromOffset(170, 40)
	topRight.BackgroundTransparency = 1
	topRight.Parent = gui

	-- Under the top centre stack, clear of the thumbstick and jump button.
	resetButton = Components.Button("GLOW RESET (+50% forever)", Theme.Gold, UDim2.fromOffset(250, Theme.MinTapSize))
	resetButton.Name = "GlowReset"
	resetButton.AnchorPoint = Vector2.new(0.5, 0)
	resetButton.Position = UDim2.new(0.5, 0, 0, 96)
	resetButton.TextSize = 17
	resetButton.Visible = false
	resetButton.Parent = gui

	resetButton.Activated:Connect(function()
		if os.clock() < resetArmedUntil then
			resetArmedUntil = 0
			Remotes.RequestGlowReset:FireServer()
		else
			resetArmedUntil = os.clock() + 3
			resetButton.Text = "TAP AGAIN TO CONFIRM"
			task.delay(3, function()
				if os.clock() >= resetArmedUntil then
					HUD.Refresh()
				end
			end)
		end
	end)
end

function HUD.Refresh()
	if not data then
		return
	end

	local stage = Stages.Get(data.stage)
	local nextStage = Stages.List[data.stage + 1]

	stageLabel.Text = string.upper(stage.name)
	auraLabel.Text = "AURA " .. NumberFormat.Abbreviate(data.aura)
	progressFill.BackgroundColor3 = stage.auraColor

	if nextStage then
		local span = nextStage.auraRequired - stage.auraRequired
		setProgress((data.cycleAura - stage.auraRequired) / span)
		progressText.Text = "Next: " .. nextStage.name .. " (" .. NumberFormat.Abbreviate(nextStage.auraRequired) .. ")"
	else
		setProgress(1)
		progressText.Text = "MAX STAGE"
	end

	resetButton.Visible = data.stage >= Stages.GlowResetStage
	if os.clock() >= resetArmedUntil then
		resetButton.Text = "GLOW RESET (+50% forever)"
	end
end

function HUD.GetData()
	return data
end

-- callback(data) runs on every data update, and right away if data already arrived.
function HUD.OnData(callback)
	table.insert(listeners, callback)
	if data then
		task.spawn(callback, data)
	end
end

-- Adds a button to the left column. Lower order sits higher. Returns the button and setBadge(n).
function HUD.AddSideButton(id, emoji, caption, order, onActivated)
	local button = Components.IconButton(emoji, caption)
	button.Name = id
	button.LayoutOrder = order
	button.Parent = sideColumn
	button.Activated:Connect(onActivated)

	local _, setBadge = Components.Badge(button)
	sideButtons[id] = button
	return button, setBadge
end

function HUD.GetSideButton(id)
	return sideButtons[id]
end

function HUD.GetChipRow()
	return chipRow
end

function HUD.GetTopRight()
	return topRight
end

function HUD.Toast(message)
	Components.Toast(message)
end

function HUD.Popup(text, color, scale)
	Components.Popup(text, color, scale)
end

function HUD.Init()
	build()

	Remotes.DataSync.OnClientEvent:Connect(function(snapshot)
		data = snapshot
		HUD.Refresh()
		for _, callback in ipairs(listeners) do
			task.spawn(callback, data)
		end
	end)

	Remotes.Notify.OnClientEvent:Connect(function(message)
		HUD.Toast(message)
	end)

	Remotes.RequestSync:FireServer()
end

return HUD
