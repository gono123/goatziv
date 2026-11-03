-- Spawns visuals locally: effects other players trigger (through the PlayEffect remote)
-- and effects for this player only. Nothing here affects gameplay.

local CollectionService = game:GetService("CollectionService")
local Lighting = game:GetService("Lighting")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local EffectsConfig = require(Shared.Config.Effects)
local Remotes = require(Shared.Remotes)

local Theme = require(script.Parent.Parent.UI.Theme)
local Components = require(script.Parent.Parent.UI.Components)

local player = Players.LocalPlayer

local EffectsController = {}

local HUD
local shakeUntil = 0
local shakeStrength = 0
local handlers = {}

-- Decorative effects are skipped on low graphics quality or when the player asks for it.
function EffectsController.IsLow()
	local data = HUD and HUD.GetData()
	if data and data.settings and data.settings.lowEffects then
		return true
	end
	local level = UserSettings():GetService("UserGameSettings").SavedQualityLevel.Value
	return level > 0 and level <= 3 -- 0 means automatic
end

local function characterOf(userId)
	local target = Players:GetPlayerByUserId(userId)
	return target and target.Character
end

local function burst(part, color, count, speed)
	local attachment = Instance.new("Attachment")
	attachment.Parent = part
	local emitter = Instance.new("ParticleEmitter")
	emitter.Enabled = false
	emitter.Color = ColorSequence.new(color)
	emitter.LightEmission = 1
	emitter.Lifetime = NumberRange.new(0.3, 0.7)
	emitter.Speed = NumberRange.new(speed or 6, (speed or 6) * 1.6)
	emitter.SpreadAngle = Vector2.new(180, 180)
	emitter.Size = NumberSequence.new({
		NumberSequenceKeypoint.new(0, 0.4),
		NumberSequenceKeypoint.new(1, 0),
	})
	emitter.Parent = attachment
	emitter:Emit(count)
	task.delay(1.2, function()
		attachment:Destroy()
	end)
end

function EffectsController.Shake(duration, strength)
	if EffectsController.IsLow() then
		strength = strength * 0.4
	end
	shakeUntil = os.clock() + duration
	shakeStrength = strength
end

-- ---------------------------------------------------------------------------
-- Effects for this player only
-- ---------------------------------------------------------------------------

function EffectsController.LuckyBurst()
	EffectsController.Shake(0.12, 0.12)
	if EffectsController.IsLow() then
		return
	end
	local character = player.Character
	if character then
		for _, name in ipairs({ "RightHand", "LeftHand" }) do
			local hand = character:FindFirstChild(name)
			if hand then
				burst(hand, Theme.Gold, 6)
			end
		end
	end
end

-- Full-screen confetti made of small frames (purchases, quests).
function EffectsController.Confetti()
	if EffectsController.IsLow() then
		return
	end
	local gui = Components.ScreenGui("Confetti", 40)
	local colors = { Theme.Orange, Theme.Teal, Theme.Gold, Theme.Success }
	for _ = 1, 30 do
		local piece = Instance.new("Frame")
		piece.Size = UDim2.fromOffset(math.random(6, 12), math.random(10, 18))
		piece.Position = UDim2.fromScale(math.random(), -0.05)
		piece.BackgroundColor3 = colors[math.random(#colors)]
		piece.BorderSizePixel = 0
		piece.Rotation = math.random(0, 360)
		piece.Parent = gui
		TweenService:Create(piece, TweenInfo.new(1 + math.random(), Enum.EasingStyle.Quad, Enum.EasingDirection.In), {
			Position = UDim2.fromScale(piece.Position.X.Scale + (math.random() - 0.5) * 0.2, 1.05),
			Rotation = piece.Rotation + math.random(-360, 360),
		}):Play()
	end
	task.delay(2.2, function()
		gui:Destroy()
	end)
end

-- ---------------------------------------------------------------------------
-- Effects sent by the server
-- ---------------------------------------------------------------------------

-- Expanding neon ring at a player's feet.
function handlers.Shockwave(params)
	local ring = Instance.new("Part")
	ring.Name = "Shockwave"
	ring.Shape = Enum.PartType.Cylinder
	ring.Anchored = true
	ring.CanCollide = false
	ring.CanQuery = false
	ring.CanTouch = false
	ring.Material = Enum.Material.Neon
	ring.Color = params.color or Theme.Gold
	ring.Size = Vector3.new(0.3, 2, 2)
	ring.CFrame = CFrame.new(params.position) * CFrame.Angles(0, 0, math.rad(90))
	ring.Transparency = 0.2
	ring.Parent = workspace

	local size = EffectsConfig.ShockwaveSize
	local tween = TweenService:Create(ring, TweenInfo.new(EffectsConfig.ShockwaveTime, Enum.EasingStyle.Quad), {
		Size = Vector3.new(0.3, size, size),
		Transparency = 1,
	})
	tween:Play()
	tween.Completed:Connect(function()
		ring:Destroy()
	end)
end

-- The signature moment: shades fall from the sky onto the face.
function handlers.SunglassesDrop(params)
	task.wait(EffectsConfig.SunglassesDropDelay)
	local character = characterOf(params.userId)
	local shades = character and character:FindFirstChild("SigmaShades")
	if not shades then
		return
	end

	local falling = shades:Clone()
	for _, child in ipairs(falling:GetChildren()) do
		child:Destroy()
	end
	falling.Anchored = true
	falling.CFrame = shades.CFrame + Vector3.new(0, EffectsConfig.SunglassesDropHeight, 0)
	falling.Parent = workspace
	shades.LocalTransparencyModifier = 1

	local tween = TweenService:Create(
		falling,
		TweenInfo.new(EffectsConfig.SunglassesDropTime, Enum.EasingStyle.Bounce, Enum.EasingDirection.Out),
		{ CFrame = shades.CFrame }
	)
	tween:Play()
	tween.Completed:Connect(function()
		falling:Destroy()
		if shades.Parent then
			shades.LocalTransparencyModifier = 0
		end
	end)
end

-- Rising white particles for everyone nearby, plus a white flash for the player who reset.
function handlers.GlowReset(params)
	local character = characterOf(params.userId)
	local root = character and character:FindFirstChild("HumanoidRootPart")
	if root and not EffectsController.IsLow() then
		burst(root, Color3.new(1, 1, 1), 40, 10)
	end

	if params.userId == player.UserId then
		local flash = Instance.new("ColorCorrectionEffect")
		flash.Brightness = 1
		flash.Parent = Lighting
		local tween = TweenService:Create(flash, TweenInfo.new(0.8), { Brightness = 0 })
		tween:Play()
		tween.Completed:Connect(function()
			flash:Destroy()
		end)
	end
end

-- Map particles are decoration, so they are the first thing to go on weak devices.
local function refreshDecorations()
	local enabled = not EffectsController.IsLow()
	for _, emitter in ipairs(CollectionService:GetTagged("DecorativeParticles")) do
		emitter.Enabled = enabled
	end
end

local function onCameraStep()
	if os.clock() < shakeUntil then
		local m = shakeStrength
		local camera = workspace.CurrentCamera
		camera.CFrame = camera.CFrame * CFrame.new((math.random() - 0.5) * m, (math.random() - 0.5) * m, 0)
	end
end

function EffectsController.Init(hud)
	HUD = hud

	Remotes.PlayEffect.OnClientEvent:Connect(function(name, params)
		local handler = handlers[name]
		if handler then
			handler(params or {})
		end
	end)

	RunService:BindToRenderStep("EffectsShake", Enum.RenderPriority.Camera.Value + 1, onCameraStep)

	HUD.OnData(refreshDecorations)
	CollectionService:GetInstanceAddedSignal("DecorativeParticles"):Connect(function(emitter)
		emitter.Enabled = not EffectsController.IsLow()
	end)
end

return EffectsController
