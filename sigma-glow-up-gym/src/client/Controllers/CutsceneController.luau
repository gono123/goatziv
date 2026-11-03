-- 3-second transformation cutscene (GDD section 13 beat sheet) + Glow Reset reveal.

local Lighting = game:GetService("Lighting")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Stages = require(Shared.Config.Stages)
local Remotes = require(Shared.Remotes)

local Components = require(script.Parent.Parent.UI.Components)
local SoundController = require(script.Parent.SoundController)
local EffectsController = require(script.Parent.EffectsController)

local CutsceneController = {}

local title, subtitle, colorFx
local queue = {}
local playing = false

local function build()
	local gui = Components.ScreenGui("Cutscene", 10)

	title = Components.Label("", 20)
	title.AnchorPoint = Vector2.new(0.5, 0.5)
	title.Position = UDim2.fromScale(0.5, 0.4)
	title.Size = UDim2.fromScale(0, 0)
	title.TextScaled = true
	title.Visible = false
	title.UIStroke.Thickness = 4
	title.Parent = gui

	subtitle = Components.Label("", 20)
	subtitle.AnchorPoint = Vector2.new(0.5, 0.5)
	subtitle.Position = UDim2.fromScale(0.5, 0.52)
	subtitle.Size = UDim2.fromScale(0.6, 0.06)
	subtitle.TextScaled = true
	subtitle.Visible = false
	subtitle.Parent = gui

	colorFx = Instance.new("ColorCorrectionEffect")
	colorFx.Name = "CutsceneColor"
	colorFx.Parent = Lighting
end

local function play(headline, subline, color, soundName)
	local camera = workspace.CurrentCamera
	local fov = camera.FieldOfView

	-- 0.0s: desaturate + zoom in
	TweenService:Create(colorFx, TweenInfo.new(0.2), { Saturation = -1 }):Play()
	TweenService:Create(camera, TweenInfo.new(0.3, Enum.EasingStyle.Quad), { FieldOfView = fov - 15 }):Play()
	SoundController.Play(soundName)
	task.wait(0.5)

	-- 0.5s: the server has started the body scale tween; punch the FOV back
	TweenService:Create(camera, TweenInfo.new(0.25, Enum.EasingStyle.Back), { FieldOfView = fov + 5 }):Play()
	task.wait(1.0)

	-- 1.5s: name slam
	title.Text = headline
	title.TextColor3 = color
	title.Size = UDim2.fromScale(0.1, 0.03)
	title.Visible = true
	subtitle.Text = subline
	subtitle.Visible = true
	TweenService:Create(title, TweenInfo.new(0.35, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {
		Size = UDim2.fromScale(0.7, 0.16),
	}):Play()
	EffectsController.Shake(0.3, 0.5)
	task.wait(1.5)

	-- 3.0s: restore
	TweenService:Create(colorFx, TweenInfo.new(0.4), { Saturation = 0 }):Play()
	TweenService:Create(camera, TweenInfo.new(0.4), { FieldOfView = fov }):Play()
	title.Visible = false
	subtitle.Visible = false
	task.wait(0.4)
end

local function enqueue(headline, subline, color, soundName)
	table.insert(queue, { headline, subline, color, soundName })
	if playing then
		return
	end
	playing = true
	while #queue > 0 do
		local item = table.remove(queue, 1)
		play(item[1], item[2], item[3], item[4])
	end
	playing = false
end

function CutsceneController.Init()
	build()

	Remotes.StageUp.OnClientEvent:Connect(function(stageIndex, stageName)
		local stage = Stages.Get(stageIndex)
		task.spawn(enqueue, string.upper(stageName), "GLOW UP UNLOCKED", stage.auraColor, "StageUp")
	end)

	Remotes.GlowResetDone.OnClientEvent:Connect(function(glowResets, shards)
		local bonus = math.floor(glowResets * 50)
		task.spawn(
			enqueue,
			"GLOW RESET",
			"+" .. bonus .. "% Aura forever  |  +" .. shards .. " Glow Shards",
			Color3.new(1, 1, 1),
			"GlowReset"
		)
	end)
end

return CutsceneController
