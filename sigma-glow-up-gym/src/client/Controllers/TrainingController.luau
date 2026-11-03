-- Training UI. Every click or tap sends one rep request. The server decides what it earns.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local UserInputService = game:GetService("UserInputService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Training = require(Shared.Config.Training)
local FastMode = require(Shared.FastMode)
local NumberFormat = require(Shared.NumberFormat)
local Remotes = require(Shared.Remotes)

local Theme = require(script.Parent.Parent.UI.Theme)
local Components = require(script.Parent.Parent.UI.Components)
local SoundController = require(script.Parent.SoundController)
local EffectsController = require(script.Parent.EffectsController)

local TrainingController = {}

local HUD
local gui, titleLabel, repsLabel
local active = false
local lastTap = 0
local sessionReps = 0

local function build()
	gui = Components.ScreenGui("Training", 2)
	gui.Enabled = false

	titleLabel = Components.Label("", 26)
	titleLabel.Name = "Title"
	titleLabel.AnchorPoint = Vector2.new(0.5, 1)
	titleLabel.Position = UDim2.new(0.5, 0, 1, -140)
	titleLabel.Size = UDim2.fromOffset(420, 34)
	titleLabel.Parent = gui

	repsLabel = Components.Label("", 20)
	repsLabel.Name = "Reps"
	repsLabel.AnchorPoint = Vector2.new(0.5, 1)
	repsLabel.Position = UDim2.new(0.5, 0, 1, -110)
	repsLabel.Size = UDim2.fromOffset(300, 28)
	repsLabel.TextColor3 = Theme.Gold
	repsLabel.Parent = gui

	local stop = Components.Button("STOP", Theme.Danger, UDim2.fromOffset(120, Theme.MinTapSize))
	stop.Name = "Stop"
	stop.AnchorPoint = Vector2.new(0.5, 1)
	stop.Position = UDim2.new(0.5, 0, 1, -54)
	stop.Parent = gui
	stop.Activated:Connect(function()
		Remotes.RequestStopTraining:FireServer()
	end)
end

local function tap()
	local now = os.clock()
	if now - lastTap < FastMode.Cooldown(Training.RepCooldown) then
		return
	end
	lastTap = now
	Remotes.RequestRep:FireServer()
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

function TrainingController.Init(hud)
	HUD = hud
	build()

	Remotes.TrainingStarted.OnClientEvent:Connect(function(_equipmentId, displayName)
		active = true
		lastTap = 0
		sessionReps = 0
		titleLabel.Text = string.upper(displayName) .. " - CLICK TO LIFT!"
		repsLabel.Text = ""
		gui.Enabled = true
	end)

	Remotes.TrainingStopped.OnClientEvent:Connect(function()
		active = false
		gui.Enabled = false
	end)

	Remotes.RepResult.OnClientEvent:Connect(function(gained, lucky)
		sessionReps = sessionReps + 1
		repsLabel.Text = sessionReps .. " REPS"

		local amount = "+" .. NumberFormat.Abbreviate(gained)
		if lucky then
			HUD.Popup("LUCKY!  " .. amount, Theme.Gold, 1.25)
			SoundController.Play("RepLucky")
			EffectsController.LuckyBurst()
		else
			HUD.Popup(amount, Theme.Text, 1)
			SoundController.Play("RepClick")
		end
	end)

	UserInputService.InputBegan:Connect(onInput)
end

return TrainingController
