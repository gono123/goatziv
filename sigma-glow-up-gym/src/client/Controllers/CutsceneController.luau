-- 3-second transformation cutscene (GDD section 13 beat sheet) + Glow Reset reveal.

local Lighting = game:GetService("Lighting")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local SoundService = game:GetService("SoundService")
local TweenService = game:GetService("TweenService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Stages = require(Shared.Config.Stages)
local Remotes = require(Shared.Remotes)

local player = Players.LocalPlayer
local camera = workspace.CurrentCamera

local CutsceneController = {}

local gui, title, subtitle, colorFx
local queue = {}
local playing = false

local function build()
	gui = Instance.new("ScreenGui")
	gui.Name = "Cutscene"
	gui.ResetOnSpawn = false
	gui.DisplayOrder = 10
	gui.Parent = player:WaitForChild("PlayerGui")

	title = Instance.new("TextLabel")
	title.AnchorPoint = Vector2.new(0.5, 0.5)
	title.Position = UDim2.fromScale(0.5, 0.4)
	title.Size = UDim2.fromScale(0, 0)
	title.BackgroundTransparency = 1
	title.Font = Enum.Font.FredokaOne
	title.TextScaled = true
	title.TextColor3 = Color3.new(1, 1, 1)
	title.TextTransparency = 1
	title.Parent = gui

	local s = Instance.new("UIStroke")
	s.Thickness = 4
	s.Parent = title

	subtitle = Instance.new("TextLabel")
	subtitle.AnchorPoint = Vector2.new(0.5, 0.5)
	subtitle.Position = UDim2.fromScale(0.5, 0.52)
	subtitle.Size = UDim2.fromScale(0.6, 0.06)
	subtitle.BackgroundTransparency = 1
	subtitle.Font = Enum.Font.FredokaOne
	subtitle.TextScaled = true
	subtitle.TextColor3 = Color3.new(1, 1, 1)
	subtitle.TextStrokeTransparency = 0
	subtitle.TextTransparency = 1
	subtitle.Parent = gui

	colorFx = Instance.new("ColorCorrectionEffect")
	colorFx.Name = "CutsceneColor"
	colorFx.Parent = Lighting
end

local function playSound()
	if Stages.StageUpSoundId ~= "" then
		local sound = Instance.new("Sound")
		sound.SoundId = Stages.StageUpSoundId
		sound.Volume = 0.8
		SoundService:PlayLocalSound(sound)
		task.delay(5, function()
			sound:Destroy()
		end)
	end
end

local function play(headline, subline, color)
	local fov = camera.FieldOfView

	-- 0.0s: desaturate + zoom in
	TweenService:Create(colorFx, TweenInfo.new(0.2), { Saturation = -1 }):Play()
	TweenService:Create(camera, TweenInfo.new(0.3, Enum.EasingStyle.Quad), { FieldOfView = fov - 15 }):Play()
	playSound()
	task.wait(0.5)

	-- 0.5s: (body scale already applied by the server) punch the FOV back
	TweenService:Create(camera, TweenInfo.new(0.25, Enum.EasingStyle.Back), { FieldOfView = fov + 5 }):Play()
	task.wait(1.0)

	-- 1.5s / 2.0s: name slam
	title.Text = headline
	title.TextColor3 = color
	title.TextTransparency = 0
	title.Size = UDim2.fromScale(0.1, 0.03)
	subtitle.Text = subline
	TweenService:Create(title, TweenInfo.new(0.35, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {
		Size = UDim2.fromScale(0.7, 0.16),
	}):Play()
	TweenService:Create(subtitle, TweenInfo.new(0.3), { TextTransparency = 0 }):Play()
	task.wait(1.0)

	-- 3.0s: restore
	TweenService:Create(colorFx, TweenInfo.new(0.4), { Saturation = 0 }):Play()
	TweenService:Create(camera, TweenInfo.new(0.4), { FieldOfView = fov }):Play()
	TweenService:Create(title, TweenInfo.new(0.5), { TextTransparency = 1 }):Play()
	TweenService:Create(subtitle, TweenInfo.new(0.5), { TextTransparency = 1 }):Play()
	task.wait(0.5)
end

local function enqueue(headline, subline, color)
	table.insert(queue, { headline, subline, color })
	if playing then
		return
	end
	playing = true
	while #queue > 0 do
		local item = table.remove(queue, 1)
		play(item[1], item[2], item[3])
	end
	playing = false
end

function CutsceneController.Init()
	build()

	Remotes.StageUp.OnClientEvent:Connect(function(stageIndex, stageName)
		local stage = Stages.Get(stageIndex)
		task.spawn(enqueue, string.upper(stageName), "GLOW UP UNLOCKED", stage.auraColor)
	end)

	Remotes.GlowResetDone.OnClientEvent:Connect(function(glowResets, shards)
		local bonus = math.floor(glowResets * 50)
		task.spawn(
			enqueue,
			"GLOW RESET",
			"+" .. bonus .. "% Aura forever  |  +" .. shards .. " Glow Shards",
			Color3.fromRGB(255, 255, 255)
		)
	end)
end

return CutsceneController
