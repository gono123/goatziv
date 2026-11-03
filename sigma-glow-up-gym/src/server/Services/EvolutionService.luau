-- Stage-ups, avatar transformation (scaling, shades, aura), client sync and Glow Reset.
-- Aura itself is added by EconomyService.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local EffectsConfig = require(Shared.Config.Effects)
local Stages = require(Shared.Config.Stages)
local Formula = require(Shared.Formula)
local NumberFormat = require(Shared.NumberFormat)
local Remotes = require(Shared.Remotes)
local Validate = require(script.Parent.Parent.Util.Validate)
local Guard = require(script.Parent.Parent.Util.Guard)

local SCALE_VALUES = {
	width = "BodyWidthScale",
	height = "BodyHeightScale",
	depth = "BodyDepthScale",
	head = "HeadScale",
}

local EvolutionService = {}

local services
local syncVersions = {} -- [Player] = number

-- ---------------------------------------------------------------------------
-- Look (body scale, sunglasses, aura particles)
-- ---------------------------------------------------------------------------

local function applyScale(humanoid, stage, tweenTime)
	-- R15 only. Scale relative to the player's own avatar proportions,
	-- remembered the first time we touch each value.
	-- NOTE: verify in Studio how far these go past avatar-editor limits on your
	-- avatar types; if they clamp, use per-stage "muscle suit" accessories instead.
	for key, valueName in pairs(SCALE_VALUES) do
		local numberValue = humanoid:FindFirstChild(valueName)
		if numberValue and numberValue:IsA("NumberValue") then
			local baseAttr = "Base" .. valueName
			local base = humanoid:GetAttribute(baseAttr)
			if base == nil then
				base = numberValue.Value
				humanoid:SetAttribute(baseAttr, base)
			end
			local target = base * stage.scale[key]
			if tweenTime then
				TweenService:Create(numberValue, TweenInfo.new(tweenTime, Enum.EasingStyle.Back), {
					Value = target,
				}):Play()
			else
				numberValue.Value = target
			end
		end
	end
end

local function applySunglasses(character, stage)
	local existing = character:FindFirstChild("SigmaShades")
	if not stage.sunglasses then
		if existing then
			existing:Destroy()
		end
		return
	end
	if existing then
		return
	end

	local head = character:FindFirstChild("Head")
	if not head or not head:IsA("BasePart") then
		return
	end

	-- Placeholder shades. Replace with a real Accessory mesh later.
	local shades = Instance.new("Part")
	shades.Name = "SigmaShades"
	shades.Size = Vector3.new(1.1, 0.28, 0.12)
	shades.Color = Color3.fromRGB(10, 10, 10)
	shades.Material = Enum.Material.Glass
	shades.Reflectance = 0.4
	shades.CanCollide = false
	shades.CanQuery = false
	shades.CanTouch = false
	shades.Massless = true
	shades.CFrame = head.CFrame * CFrame.new(0, 0.15, -head.Size.Z / 2 - 0.05)

	local weld = Instance.new("WeldConstraint")
	weld.Part0 = head
	weld.Part1 = shades
	weld.Parent = shades

	shades.Parent = character
end

local function applyAura(character, stage)
	local root = character:FindFirstChild("HumanoidRootPart")
	if not root then
		return
	end

	local emitter = root:FindFirstChild("StageAura")
	if not emitter then
		emitter = Instance.new("ParticleEmitter")
		emitter.Name = "StageAura"
		emitter.LightEmission = 1
		emitter.Lifetime = NumberRange.new(0.8, 1.4)
		emitter.Speed = NumberRange.new(1, 3)
		emitter.SpreadAngle = Vector2.new(180, 180)
		emitter.Size = NumberSequence.new({
			NumberSequenceKeypoint.new(0, 0.6),
			NumberSequenceKeypoint.new(1, 0),
		})
		emitter.Transparency = NumberSequence.new({
			NumberSequenceKeypoint.new(0, 0.2),
			NumberSequenceKeypoint.new(1, 1),
		})
		emitter.Parent = root
	end

	emitter.Color = ColorSequence.new(stage.auraColor)
	emitter.Rate = stage.auraRate
	emitter.Enabled = stage.auraRate > 0
end

-- tweenTime is optional: stage-ups and resets animate, respawns apply at once.
function EvolutionService:ApplyLook(player, tweenTime)
	local data = services.DataService:Get(player)
	local character = player.Character
	if not data or not character then
		return
	end
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	if not humanoid then
		return
	end

	local stage = Stages.Get(data.stage)
	applyScale(humanoid, stage, tweenTime)
	applySunglasses(character, stage)
	applyAura(character, stage)
end

-- ---------------------------------------------------------------------------
-- Leaderstats + client sync
-- ---------------------------------------------------------------------------

local function ensureLeaderstats(player)
	local folder = player:FindFirstChild("leaderstats")
	if not folder then
		folder = Instance.new("Folder")
		folder.Name = "leaderstats"

		local aura = Instance.new("StringValue")
		aura.Name = "Aura"
		aura.Parent = folder

		local stage = Instance.new("StringValue")
		stage.Name = "Stage"
		stage.Parent = folder

		folder.Parent = player
	end
	return folder
end

function EvolutionService:Sync(player)
	local data = services.DataService:Get(player)
	if not data then
		return
	end

	local stats = ensureLeaderstats(player)
	stats.Aura.Value = NumberFormat.Abbreviate(data.aura)
	stats.Stage.Value = Stages.Get(data.stage).name

	syncVersions[player] = (syncVersions[player] or 0) + 1

	Remotes.DataSync:FireClient(player, {
		version = syncVersions[player],
		aura = data.aura,
		lifetimeAura = data.lifetimeAura,
		stage = data.stage,
		bestStage = data.bestStage,
		glowResets = data.glowResets,
		glowShards = data.glowShards,
		dripTokens = data.dripTokens,
		settings = data.settings,
	})
end

-- ---------------------------------------------------------------------------
-- Progression
-- ---------------------------------------------------------------------------

function EvolutionService:CheckStage(player)
	local data = services.DataService:Get(player)
	if not data then
		return
	end

	local oldStage = data.stage
	local newStage = oldStage
	while Stages.List[newStage + 1] and data.aura >= Stages.List[newStage + 1].auraRequired do
		newStage = newStage + 1
	end

	if newStage == oldStage then
		return
	end

	data.stage = newStage
	data.bestStage = math.max(data.bestStage, newStage)
	services.GateService:Refresh(player)
	self:ApplyLook(player, EffectsConfig.StageUpScaleTime)
	Remotes.StageUp:FireClient(player, newStage, Stages.Get(newStage).name)

	local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
	if root then
		local stage = Stages.Get(newStage)
		local feet = root.Position - Vector3.new(0, root.Size.Y / 2 + 2, 0)
		services.EffectsService:PlayNear(root.Position, EffectsConfig.NearbyRadius, "Shockwave", {
			position = feet,
			color = stage.auraColor,
		})
		if stage.sunglasses and not Stages.Get(oldStage).sunglasses then
			services.EffectsService:PlayNear(root.Position, EffectsConfig.NearbyRadius, "SunglassesDrop", {
				userId = player.UserId,
			})
		end
	end
end

-- Kept so callers can add Aura through either service; the work happens in EconomyService.
function EvolutionService:AddAura(player, amount, source)
	return services.EconomyService:AddAura(player, amount, source)
end

function EvolutionService:GlowReset(player)
	local data = services.DataService:Get(player)
	if not data then
		return
	end
	if data.stage < Stages.GlowResetStage then
		Remotes.Notify:FireClient(player, "Reach " .. Stages.Get(Stages.GlowResetStage).name .. " to Glow Reset!")
		return
	end

	services.TrainingService:Stop(player)

	data.glowResets = data.glowResets + 1
	data.aura = 0
	data.stage = 1
	local shards = Formula.GlowShardsForReset(data.glowResets)
	services.EconomyService:AddShards(player, shards, "glowReset")

	self:ApplyLook(player, EffectsConfig.GlowResetScaleTime)
	Remotes.GlowResetDone:FireClient(player, data.glowResets, shards)

	local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
	if root then
		services.EffectsService:PlayNear(root.Position, EffectsConfig.NearbyRadius, "GlowReset", {
			userId = player.UserId,
		})
	end
end

-- ---------------------------------------------------------------------------
-- Lifecycle
-- ---------------------------------------------------------------------------

function EvolutionService:Init(allServices)
	services = allServices
end

function EvolutionService:Start()
	services.DataService:OnLoaded(function(player, data)
		data.bestStage = math.max(data.bestStage, data.stage) -- saves from before bestStage existed
		self:Sync(player)

		-- Scale values are set by the avatar loader, so wait for the appearance.
		player.CharacterAppearanceLoaded:Connect(function()
			self:ApplyLook(player)
		end)
		if player.Character and player:HasAppearanceLoaded() then
			self:ApplyLook(player)
		end
	end)

	Players.PlayerRemoving:Connect(function(player)
		syncVersions[player] = nil
	end)

	Guard.connect(services, "RequestGlowReset", function(player)
		self:GlowReset(player)
	end)

	Guard.connect(services, "RequestSync", function(player)
		self:Sync(player)
	end)

	Guard.connect(services, "RequestSetSettings", function(player, music, sfx, lowEffects)
		if not Validate.number(music, 0, 1) or not Validate.number(sfx, 0, 1) or not Validate.bool(lowEffects) then
			return
		end
		local data = services.DataService:Get(player)
		data.settings.music = music
		data.settings.sfx = sfx
		data.settings.lowEffects = lowEffects
		self:Sync(player)
	end)
end

return EvolutionService
