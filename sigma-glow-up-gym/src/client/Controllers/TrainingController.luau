-- Timing-bar rep mini-game UI. The server decides the real result; this only draws
-- the marker (from the synced server clock) and sends tap timestamps.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Training = require(Shared.Config.Training)
local Formula = require(Shared.Formula)
local NumberFormat = require(Shared.NumberFormat)
local Remotes = require(Shared.Remotes)

local player = Players.LocalPlayer
local camera = workspace.CurrentCamera

local QUALITY_COLORS = {
	Perfect = Color3.fromRGB(255, 215, 0),
	Good = Color3.fromRGB(120, 255, 120),
	Miss = Color3.fromRGB(255, 110, 110),
}

local TrainingController = {}

local HUD
local gui, bar, marker, goldZone, comboLabel, lockedLabel, titleLabel
local active = false
local cycleStart = 0
local lastTap = 0
local lockedIn = false
local shakeUntil = 0

local function corner(parent, radius)
	local c = Instance.new("UICorner")
	c.CornerRadius = UDim.new(0, radius)
	c.Parent = parent
end

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
	local label = Instance.new("TextLabel")
	label.Name = name
	label.AnchorPoint = Vector2.new(0.5, 1)
	label.Position = position
	label.Size = size
	label.BackgroundTransparency = 1
	label.Font = Enum.Font.FredokaOne
	label.TextSize = textSize
	label.TextColor3 = Color3.new(1, 1, 1)
	label.TextStrokeTransparency = 0
	label.Text = ""
	label.Parent = gui
	return label
end

local function build()
	gui = Instance.new("ScreenGui")
	gui.Name = "Training"
	gui.ResetOnSpawn = false
	gui.Enabled = false
	gui.Parent = player:WaitForChild("PlayerGui")

	bar = Instance.new("Frame")
	bar.Name = "Bar"
	bar.AnchorPoint = Vector2.new(0.5, 1)
	bar.Position = UDim2.new(0.5, 0, 1, -110)
	bar.Size = UDim2.new(0.6, 0, 0, 36)
	bar.BackgroundColor3 = Color3.fromRGB(40, 40, 55)
	bar.ClipsDescendants = true
	corner(bar, 10)
	bar.Parent = gui

	local limit = Instance.new("UISizeConstraint")
	limit.MaxSize = Vector2.new(520, 36)
	limit.Parent = bar

	zone("Green", Training.GreenHalfWidth, Color3.fromRGB(70, 180, 90))
	goldZone = zone("Gold", Training.GoldHalfWidth, Color3.fromRGB(255, 205, 40))

	marker = Instance.new("Frame")
	marker.Name = "Marker"
	marker.AnchorPoint = Vector2.new(0.5, 0.5)
	marker.Size = UDim2.new(0, 8, 1.4, 0)
	marker.BackgroundColor3 = Color3.new(1, 1, 1)
	marker.BorderSizePixel = 0
	marker.ZIndex = 3
	marker.Parent = bar

	titleLabel = text("Title", UDim2.new(0.5, 0, 1, -150), UDim2.fromOffset(400, 30), 24)
	comboLabel = text("Combo", UDim2.new(0.5, 0, 1, -180), UDim2.fromOffset(300, 28), 22)
	lockedLabel = text("LockedIn", UDim2.new(0.5, 0, 1, -210), UDim2.fromOffset(300, 32), 28)
	lockedLabel.TextColor3 = QUALITY_COLORS.Perfect
	lockedLabel.Text = "LOCKED IN"
	lockedLabel.Visible = false

	local stop = Instance.new("TextButton")
	stop.Name = "Stop"
	stop.AnchorPoint = Vector2.new(0.5, 1)
	stop.Position = UDim2.new(0.5, 0, 1, -58)
	stop.Size = UDim2.fromOffset(120, 40)
	stop.BackgroundColor3 = Color3.fromRGB(200, 60, 60)
	stop.Font = Enum.Font.FredokaOne
	stop.TextSize = 20
	stop.TextColor3 = Color3.new(1, 1, 1)
	stop.Text = "STOP"
	corner(stop, 10)
	stop.Parent = gui
	stop.Activated:Connect(function()
		Remotes.RequestStopTraining:FireServer()
	end)
end

local function setLockedIn(value)
	lockedIn = value
	lockedLabel.Visible = value
	goldZone.Size = UDim2.fromScale(Formula.GoldHalfWidth(value) * 2, 1)
end

local function tap()
	if not active then
		return
	end
	local now = workspace:GetServerTimeNow()
	if now - lastTap < Training.RepCooldown then
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
		local elapsed = workspace:GetServerTimeNow() - cycleStart
		marker.Position = UDim2.fromScale(Formula.MarkerPosition(elapsed), 0.5)
		local cooling = workspace:GetServerTimeNow() - lastTap < Training.RepCooldown
		marker.BackgroundTransparency = cooling and 0.6 or 0
	end
end

local function onCameraShake()
	if os.clock() < shakeUntil then
		local m = 0.12
		camera.CFrame = camera.CFrame
			* CFrame.new((math.random() - 0.5) * m, (math.random() - 0.5) * m, 0)
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
		local label = string.upper(quality) .. "!  +" .. NumberFormat.Abbreviate(gained)
		local scale = 1
		if quality == "Perfect" then
			scale = 1.25
			shakeUntil = os.clock() + 0.12
		end
		HUD.Popup(label, QUALITY_COLORS[quality], scale)

		if combo >= 2 then
			comboLabel.Text = "x" .. combo .. " COMBO"
		else
			comboLabel.Text = ""
		end
		if isLockedIn ~= lockedIn then
			setLockedIn(isLockedIn)
		end
	end)

	UserInputService.InputBegan:Connect(onInput)
	RunService.RenderStepped:Connect(onRender)
	RunService:BindToRenderStep("TrainingShake", Enum.RenderPriority.Camera.Value + 1, onCameraShake)
end

return TrainingController
