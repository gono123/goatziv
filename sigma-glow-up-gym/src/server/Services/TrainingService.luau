-- Training sessions and server-side rep checks (GDD section 5 + 15.3).
--
-- Flow: player triggers an equipment ProximityPrompt -> server starts a session -> each
-- client click sends one RequestRep -> server enforces the cooldown and adds the Aura.

local CollectionService = game:GetService("CollectionService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Equipment = require(Shared.Config.Equipment)
local Stages = require(Shared.Config.Stages)
local Training = require(Shared.Config.Training)
local FastMode = require(Shared.FastMode)
local Formula = require(Shared.Formula)
local Upgrades = require(Shared.Logic.Upgrades)
local Remotes = require(Shared.Remotes)
local Guard = require(script.Parent.Parent.Util.Guard)

local EQUIPMENT_TAG = "Equipment"

local TrainingService = {}

local services
local sessions = {} -- [Player] = session
local hooked = {} -- [Instance] = true
local occupied = {} -- [equipment Instance] = Player

local function getPosition(instance)
	if instance:IsA("BasePart") then
		return instance.Position
	end
	return instance:GetPivot().Position
end

local function isUnlocked(def, data)
	if data.stage >= def.unlockStage then
		return true
	end
	if def.unlockGlowResets and data.glowResets >= def.unlockGlowResets then
		return true
	end
	return false
end

-- ---------------------------------------------------------------------------
-- Sessions
-- ---------------------------------------------------------------------------

function TrainingService:Stop(player, silent)
	local session = sessions[player]
	if not session then
		return
	end
	sessions[player] = nil
	if occupied[session.instance] == player then
		occupied[session.instance] = nil
	end

	if session.track then
		session.track:Stop()
	end

	local humanoid = session.humanoid
	if humanoid and humanoid.Parent then
		humanoid.WalkSpeed = session.prevWalkSpeed
		humanoid.JumpPower = session.prevJumpPower
		humanoid.JumpHeight = session.prevJumpHeight
	end

	if not silent and player.Parent then
		Remotes.TrainingStopped:FireClient(player)
	end
end

function TrainingService:IsTraining(player)
	return sessions[player] ~= nil
end

function TrainingService:Begin(player, equipmentInstance)
	local equipmentId = equipmentInstance:GetAttribute("EquipmentId")
	local def = Equipment[equipmentId]
	if not def then
		warn("[TrainingService] Unknown EquipmentId on " .. equipmentInstance:GetFullName())
		return
	end

	local data = services.DataService:Get(player)
	if not data then
		return
	end

	-- Pressing the prompt of the machine you're on stops training.
	local current = sessions[player]
	if current and current.instance == equipmentInstance then
		self:Stop(player)
		return
	end

	if not isUnlocked(def, data) then
		Remotes.Notify:FireClient(player, def.displayName .. " unlocks at " .. Stages.Get(def.unlockStage).name .. "!")
		return
	end

	local character = player.Character
	local humanoid = character and character:FindFirstChildOfClass("Humanoid")
	local root = character and character:FindFirstChild("HumanoidRootPart")
	if not humanoid or not root or humanoid.Health <= 0 then
		return
	end

	local target = getPosition(equipmentInstance)
	if (root.Position - target).Magnitude > Training.TrainRange then
		return
	end

	if occupied[equipmentInstance] then
		Remotes.Notify:FireClient(player, "Station taken — try the next one")
		return
	end

	self:Stop(player, true)

	local session = {
		instance = equipmentInstance,
		equipmentId = equipmentId,
		humanoid = humanoid,
		lastRep = 0,
		prevWalkSpeed = humanoid.WalkSpeed,
		prevJumpPower = humanoid.JumpPower,
		prevJumpHeight = humanoid.JumpHeight,
		track = nil,
	}
	sessions[player] = session
	occupied[equipmentInstance] = player

	humanoid.WalkSpeed = 0
	humanoid.JumpPower = 0
	humanoid.JumpHeight = 0

	local standAt = root.Position
	local marker = equipmentInstance:FindFirstChild("StationMarker", true)
	if marker then
		local height = marker.Position.Y + marker.Size.Y / 2 + humanoid.HipHeight + root.Size.Y / 2
		standAt = Vector3.new(marker.Position.X, height, marker.Position.Z)
	end
	root.CFrame = CFrame.lookAt(standAt, Vector3.new(target.X, standAt.Y, target.Z))

	if def.animationId then
		local animator = humanoid:FindFirstChildOfClass("Animator")
		if animator then
			local animation = Instance.new("Animation")
			animation.AnimationId = def.animationId
			local ok, track = pcall(function()
				return animator:LoadAnimation(animation)
			end)
			if ok and track then
				track.Looped = true
				track:Play()
				session.track = track
			end
		end
	end

	Remotes.TrainingStarted:FireClient(player, equipmentId, def.displayName)
end

-- ---------------------------------------------------------------------------
-- Reps
-- ---------------------------------------------------------------------------

local function onRequestRep(player)
	local session = sessions[player]
	if not session then
		return
	end

	local now = os.clock()
	local minimumGap = FastMode.Cooldown(Training.RepCooldown) * Training.RepCooldownSlack
	if now - session.lastRep < minimumGap then
		return
	end
	session.lastRep = now

	local data = services.DataService:Get(player)
	local def = Equipment[session.equipmentId]
	if not data or not def then
		return
	end

	data.stats.reps = data.stats.reps + 1

	local gained = Formula.AuraPerRep(
		def.base,
		Stages.Get(data.stage).multiplier,
		data.glowResets,
		Upgrades.PowerMultiplier(data.upgrades),
		services.BrainrotService:GetAuraMultiplier(player),
		1
	)

	local luckyChance = Upgrades.LuckyChance(data.upgrades) + services.BrainrotService:GetLuckyBonus(player)
	local lucky = math.random() < luckyChance
	if lucky then
		gained = gained * 2
	end

	services.EconomyService:AddAura(player, gained, "training")

	Remotes.RepResult:FireClient(player, gained, lucky)
end

-- ---------------------------------------------------------------------------
-- Equipment hookup
-- ---------------------------------------------------------------------------

local function hookEquipment(instance)
	if hooked[instance] then
		return
	end
	hooked[instance] = true

	local def = Equipment[instance:GetAttribute("EquipmentId")]

	local prompt = instance:FindFirstChildWhichIsA("ProximityPrompt", true)
	if not prompt then
		local host = instance
		if instance:IsA("Model") then
			host = instance.PrimaryPart or instance:FindFirstChildWhichIsA("BasePart", true)
		end
		if not host then
			warn("[TrainingService] Equipment has no BasePart for a prompt: " .. instance:GetFullName())
			return
		end
		prompt = Instance.new("ProximityPrompt")
		prompt.ActionText = "Train"
		prompt.ObjectText = def and def.displayName or "Equipment"
		prompt.HoldDuration = 0
		prompt.MaxActivationDistance = 10
		prompt.RequiresLineOfSight = false
		prompt.Parent = host
	end

	prompt.Triggered:Connect(function(player)
		TrainingService:Begin(player, instance)
	end)
end

-- ---------------------------------------------------------------------------
-- Lifecycle
-- ---------------------------------------------------------------------------

function TrainingService:Init(allServices)
	services = allServices
end

function TrainingService:Start()
	for _, instance in ipairs(CollectionService:GetTagged(EQUIPMENT_TAG)) do
		hookEquipment(instance)
	end
	CollectionService:GetInstanceAddedSignal(EQUIPMENT_TAG):Connect(hookEquipment)

	Guard.connect(services, "RequestRep", onRequestRep)
	Guard.connect(services, "RequestStopTraining", function(player)
		self:Stop(player)
	end)

	local function watchCharacter(player, character)
		local humanoid = character:WaitForChild("Humanoid", 10)
		if humanoid then
			humanoid.Died:Connect(function()
				self:Stop(player)
			end)
		end
	end

	local function onPlayer(player)
		player.CharacterAdded:Connect(function(character)
			watchCharacter(player, character)
		end)
		player.CharacterRemoving:Connect(function()
			self:Stop(player, true)
		end)
		if player.Character then
			task.spawn(watchCharacter, player, player.Character)
		end
	end

	Players.PlayerAdded:Connect(onPlayer)
	for _, player in ipairs(Players:GetPlayers()) do
		onPlayer(player)
	end

	Players.PlayerRemoving:Connect(function(player)
		self:Stop(player, true)
	end)
end

return TrainingService
