-- Timing-bar rep mini-game UI. The server decides the real result; this only draws
-- the marker (from the synced server clock) and sends tap timestamps.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Training = require(Shared.Config.Training)
local FastMode = require(Shared.FastMode)
local Formula = require(Shared.Formula)
local NumberFormat = require(Shared.NumberFormat)
local Remotes = require(Shared.Remotes)

local Theme = require(script.Parent.Parent.UI.Theme)
local Components = require(script.Parent.Parent.UI.Components)
local SoundController = require(script.Parent.SoundController)
local EffectsController = require(script.Parent.EffectsController)

local QUALITY_COLORS = {
	Perfect = Theme.Gold,
	Good = Theme.Success,
	Miss = Theme.Danger,
}
local QUALITY_SOUNDS = {
	Perfect = "RepPerfect",
	Good = "RepGood",
	Miss = "RepMiss",
}

local TrainingController = {}

local HUD
local gui, bar, barStroke, marker, goldZone, comboLabel, lockedLabel, titleLabel
local active = false
local cycleStart = 0
local lastTap = 0
local lockedIn = false

local function zone(name, halfWidth, color)
	local f = Instance.new("Frame")
	f.Name = name
	f.AnchorPoint = Vector2.new(0.5, 0.5)
	f.Position = UDim2.fromScale(0.5, 0.5)
	f.Size = UDim2.fromScale(halfWidth * 2, 1)
	f.BackgroundColor3 = color
	f.BorderSizePixel = 0
	f.Parent = bar
	return f
end

local function text(name, position, size, textSize)
	local label = Components.Label("", textSize)
	label.Name = name
	label.AnchorPoint = Vector2.new(0.5, 1)
	label.Position = position
	label.Size = size
	label.Parent = gui
	return label
end

local function build()
	gui = Components.ScreenGui("Training", 2)
	gui.Enabled = false

	bar = Instance.new("Frame")
	bar.Name = "Bar"
	bar.AnchorPoint = Vector2.new(0.5, 1)
	bar.Position = UDim2.new(0.5, 0, 1, -110)
	bar.Size = UDim2.new(0.55, 0, 0, 36)
	bar.BackgroundColor3 = Theme.Panel
	bar.ClipsDescendants = true
	Components.Corner(bar, 10)
	bar.Parent = gui

	barStroke = Instance.new("UIStroke")
	barStroke.Thickness = 2
	barStroke.Color = Theme.Stroke
	barStroke.Parent = bar

	local limit = Instance.new("UISizeConstraint")
	limit.MaxSize = Vector2.new(520, 36)
	limit.Parent = bar

	zone("Green", Training.GreenHalfWidth, Theme.Success)
	goldZone = zone("Gold", Training.GoldHalfWidth, Theme.Gold)

	marker = Instance.new("Frame")
	marker.Name = "Marker"
	marker.AnchorPoint = Vector2.new(0.5, 0.5)
	marker.Size = UDim2.new(0, 8, 1.4, 0)
	marker.BackgroundColor3 = Theme.Text
	marker.BorderSizePixel = 0
	marker.ZIndex = 3
	marker.Parent = bar

	titleLabel = text("Title", UDim2.new(0.5, 0, 1, -150), UDim2.fromOffset(400, 30), 22)
	comboLabel = text("Combo", UDim2.new(0.5, 0, 1, -180), UDim2.fromOffset(300, 28), 22)
	lockedLabel = text("LockedIn", UDim2.new(0.5, 0, 1, -210), UDim2.fromOffset(300, 32), 28)
	lockedLabel.TextColor3 = Theme.Gold
	lockedLabel.Text = "LOCKED IN"
	lockedLabel.Visible = false

	local stop = Components.Button("STOP", Theme.Danger, UDim2.fromOffset(120, Theme.MinTapSize))
	stop.Name = "Stop"
	stop.AnchorPoint = Vector2.new(0.5, 1)
	stop.Position = UDim2.new(0.5, 0, 1, -54)
	stop.Parent = gui
	stop.Activated:Connect(function()
		Remotes.RequestStopTraining:FireServer()
	end)
end

local function setLockedIn(value)
	lockedIn = value
	lockedLabel.Visible = value
	goldZone.Size = UDim2.fromScale(Formula.GoldHalfWidth(value) * 2, 1)
	barStroke.Color = value and Theme.Gold or Theme.Stroke
	barStroke.Thickness = value and 4 or 2
	EffectsController.SetLockedIn(value)
end

local function tap()
	if not active then
		return
	end
	local now = workspace:GetServerTimeNow()
	if now - lastTap < FastMode.Cooldown(Training.RepCooldown) then
		return
	end
	lastTap = now
	Remotes.RequestRep:FireServer(now)
end

local function onInput(input, gameProcessed)
	if not active then
		return
	end
	local t = input.UserInputType
	if t == Enum.UserInputType.MouseButton1 or t == Enum.UserInputType.Touch then
		if not gameProcessed then
			tap()
		end
	elseif input.KeyCode == Enum.KeyCode.Space or input.KeyCode == Enum.KeyCode.ButtonA then
		if UserInputService:GetFocusedTextBox() == nil then
			tap()
		end
	end
end

local function onRender()
	if active then
		local now = workspace:GetServerTimeNow()
		marker.Position = UDim2.fromScale(Formula.MarkerPosition(now - cycleStart), 0.5)
		local cooling = now - lastTap < FastMode.Cooldown(Training.RepCooldown)
		marker.BackgroundTransparency = cooling and 0.6 or 0
	end
end

function TrainingController.Init(hud)
	HUD = hud
	build()

	Remotes.TrainingStarted.OnClientEvent:Connect(function(_equipmentId, start, displayName)
		cycleStart = start
		active = true
		lastTap = 0
		setLockedIn(false)
		comboLabel.Text = ""
		titleLabel.Text = string.upper(displayName) .. " - TAP ON GOLD!"
		gui.Enabled = true
	end)

	Remotes.TrainingStopped.OnClientEvent:Connect(function()
		active = false
		gui.Enabled = false
		setLockedIn(false)
	end)

	Remotes.RepResult.OnClientEvent:Connect(function(quality, gained, combo, isLockedIn)
		-- The word is always shown, so feedback never relies on colour alone.
		local label = string.upper(quality) .. "!  +" .. NumberFormat.Abbreviate(gained)
		local scale = 1
		if quality == "Perfect" then
			scale = 1.25
			EffectsController.PerfectBurst()
		end
		HUD.Popup(label, QUALITY_COLORS[quality], scale)
		SoundController.Play(QUALITY_SOUNDS[quality])

		comboLabel.Text = combo >= 2 and ("x" .. combo .. " COMBO") or ""
		if isLockedIn ~= lockedIn then
			setLockedIn(isLockedIn)
		end
	end)

	UserInputService.InputBegan:Connect(onInput)
	RunService.RenderStepped:Connect(onRender)
end

return TrainingController
