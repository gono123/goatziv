-- Aura totals, stage-ups, avatar transformation (scaling, shades, aura) and Glow Reset.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Stages = require(Shared.Config.Stages)
local Formula = require(Shared.Formula)
local NumberFormat = require(Shared.NumberFormat)
local Remotes = require(Shared.Remotes)

local SCALE_VALUES = {
	width = "BodyWidthScale",
	height = "BodyHeightScale",
	depth = "BodyDepthScale",
	head = "HeadScale",
}

local EvolutionService = {}

local services

-- ---------------------------------------------------------------------------
-- Look (body scale, sunglasses, aura particles)
-- ---------------------------------------------------------------------------

local function applyScale(humanoid, stage)
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
			numberValue.Value = base * stage.scale[key]
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

function EvolutionService:ApplyLook(player)
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
	applyScale(humanoid, stage)
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

	Remotes.DataSync:FireClient(player, {
		aura = data.aura,
		lifetimeAura = data.lifetimeAura,
		stage = data.stage,
		glowResets = data.glowResets,
		glowShards = data.glowShards,
		dripTokens = data.dripTokens,
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

	local newStage = data.stage
	while Stages.List[newStage + 1] and data.aura >= Stages.List[newStage + 1].auraRequired do
		newStage = newStage + 1
	end

	if newStage ~= data.stage then
		data.stage = newStage
		self:ApplyLook(player)
		Remotes.StageUp:FireClient(player, newStage, Stages.Get(newStage).name)
	end
end

function EvolutionService:AddAura(player, amount)
	local data = services.DataService:Get(player)
	if not data or amount <= 0 then
		return
	end
	data.aura = data.aura + amount
	data.lifetimeAura = data.lifetimeAura + amount
	self:CheckStage(player)
	self:Sync(player)
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
	local shards = Formula.GlowShardsForReset(data.glowResets)
	data.glowShards = data.glowShards + shards
	data.aura = 0
	data.stage = 1

	self:ApplyLook(player)
	self:Sync(player)
	Remotes.GlowResetDone:FireClient(player, data.glowResets, shards)
end

-- ---------------------------------------------------------------------------
-- Lifecycle
-- ---------------------------------------------------------------------------

function EvolutionService:Init(allServices)
	services = allServices
end

function EvolutionService:Start()
	services.DataService:OnLoaded(function(player)
		self:Sync(player)

		-- Scale values are set by the avatar loader, so wait for the appearance.
		player.CharacterAppearanceLoaded:Connect(function()
			self:ApplyLook(player)
		end)
		if player.Character and player:HasAppearanceLoaded() then
			self:ApplyLook(player)
		end
	end)

	Remotes.RequestGlowReset.OnServerEvent:Connect(function(player)
		self:GlowReset(player)
	end)

	Remotes.RequestSync.OnServerEvent:Connect(function(player)
		self:Sync(player)
	end)
end

return EvolutionService
