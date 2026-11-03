-- Aura counter, stage name, progress bar, Glow Reset button, toasts and pop-up text.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Stages = require(Shared.Config.Stages)
local NumberFormat = require(Shared.NumberFormat)
local Remotes = require(Shared.Remotes)

local player = Players.LocalPlayer

local HUD = {}

local gui, stageLabel, auraLabel, progressFill, progressText, resetButton, toastLabel
local data = nil
local resetArmedUntil = 0

local function corner(parent, radius)
	local c = Instance.new("UICorner")
	c.CornerRadius = UDim.new(0, radius or 12)
	c.Parent = parent
end

local function stroke(parent, thickness)
	local s = Instance.new("UIStroke")
	s.Thickness = thickness or 2
	s.Color = Color3.new(0, 0, 0)
	s.ApplyStrokeMode = Enum.ApplyStrokeMode.Contextual
	s.Parent = parent
end

local function makeText(parent, name, size, position, textSize)
	local label = Instance.new("TextLabel")
	label.Name = name
	label.Size = size
	label.Position = position
	label.BackgroundTransparency = 1
	label.Font = Enum.Font.FredokaOne
	label.TextColor3 = Color3.new(1, 1, 1)
	label.TextSize = textSize
	label.Text = ""
	stroke(label, 2)
	label.Parent = parent
	return label
end

local function build()
	gui = Instance.new("ScreenGui")
	gui.Name = "HUD"
	gui.ResetOnSpawn = false
	gui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
	gui.Parent = player:WaitForChild("PlayerGui")

	local top = Instance.new("Frame")
	top.Name = "Top"
	top.AnchorPoint = Vector2.new(0.5, 0)
	top.Position = UDim2.new(0.5, 0, 0, 8)
	top.Size = UDim2.fromOffset(320, 96)
	top.BackgroundTransparency = 1
	top.Parent = gui

	stageLabel = makeText(top, "Stage", UDim2.new(1, 0, 0, 30), UDim2.new(0, 0, 0, 0), 28)
	auraLabel = makeText(top, "Aura", UDim2.new(1, 0, 0, 26), UDim2.new(0, 0, 0, 30), 24)
	auraLabel.TextColor3 = Color3.fromRGB(255, 220, 90)

	local bar = Instance.new("Frame")
	bar.Name = "Progress"
	bar.Position = UDim2.new(0, 0, 0, 62)
	bar.Size = UDim2.new(1, 0, 0, 22)
	bar.BackgroundColor3 = Color3.fromRGB(30, 30, 40)
	corner(bar, 11)
	stroke(bar, 2)
	bar.Parent = top

	progressFill = Instance.new("Frame")
	progressFill.Name = "Fill"
	progressFill.Size = UDim2.fromScale(0, 1)
	progressFill.BackgroundColor3 = Color3.fromRGB(120, 200, 255)
	corner(progressFill, 11)
	progressFill.Parent = bar

	progressText = makeText(bar, "Text", UDim2.fromScale(1, 1), UDim2.fromScale(0, 0), 14)
	progressText.ZIndex = 2

	resetButton = Instance.new("TextButton")
	resetButton.Name = "GlowReset"
	resetButton.AnchorPoint = Vector2.new(0, 1)
	resetButton.Position = UDim2.new(0, 16, 1, -16)
	resetButton.Size = UDim2.fromOffset(220, 56)
	resetButton.BackgroundColor3 = Color3.fromRGB(255, 200, 60)
	resetButton.Font = Enum.Font.FredokaOne
	resetButton.TextSize = 20
	resetButton.TextColor3 = Color3.fromRGB(40, 20, 0)
	resetButton.Text = "GLOW RESET"
	resetButton.Visible = false
	corner(resetButton, 14)
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

	toastLabel = makeText(gui, "Toast", UDim2.fromOffset(500, 40), UDim2.new(0.5, -250, 0, 116), 22)
	toastLabel.TextTransparency = 1
	toastLabel.TextStrokeTransparency = 1
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
		local progress = math.clamp((data.aura - stage.auraRequired) / span, 0, 1)
		progressFill.Size = UDim2.fromScale(progress, 1)
		progressText.Text = "Next: " .. nextStage.name .. " (" .. NumberFormat.Abbreviate(nextStage.auraRequired) .. ")"
	else
		progressFill.Size = UDim2.fromScale(1, 1)
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

function HUD.Toast(message)
	toastLabel.Text = message
	toastLabel.TextTransparency = 0
	toastLabel.TextStrokeTransparency = 0
	task.delay(2.5, function()
		if toastLabel.Text == message then
			TweenService:Create(toastLabel, TweenInfo.new(0.4), {
				TextTransparency = 1,
				TextStrokeTransparency = 1,
			}):Play()
		end
	end)
end

-- Floating text that rises and fades (rep results, etc).
function HUD.Popup(text, color, scale)
	local label = Instance.new("TextLabel")
	label.AnchorPoint = Vector2.new(0.5, 0.5)
	label.Position = UDim2.new(0.5 + (math.random() - 0.5) * 0.12, 0, 0.62, 0)
	label.Size = UDim2.fromOffset(300, 50)
	label.BackgroundTransparency = 1
	label.Font = Enum.Font.FredokaOne
	label.TextSize = math.floor(30 * (scale or 1))
	label.TextColor3 = color or Color3.new(1, 1, 1)
	label.Text = text
	stroke(label, 3)
	label.Parent = gui

	local tween = TweenService:Create(label, TweenInfo.new(0.9, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
		Position = label.Position - UDim2.fromScale(0, 0.12),
		TextTransparency = 1,
	})
	tween:Play()
	tween.Completed:Connect(function()
		label:Destroy()
	end)
end

function HUD.Init()
	build()

	Remotes.DataSync.OnClientEvent:Connect(function(snapshot)
		data = snapshot
		HUD.Refresh()
	end)

	Remotes.Notify.OnClientEvent:Connect(function(message)
		HUD.Toast(message)
	end)

	Remotes.RequestSync:FireServer()
end

return HUD
