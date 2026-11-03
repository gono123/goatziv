-- Zone gates and the Cosmic Dojo launch pad.
--
-- Gates use collision groups. A part can only be in one group, and later gates need
-- higher stages, so a player's group is the FIRST gate they are locked out of, and that
-- group collides with that gate and every later one. Unlocked players collide with none.

local PhysicsService = game:GetService("PhysicsService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local World = require(Shared.Config.World)
local Stages = require(Shared.Config.Stages)
local Remotes = require(Shared.Remotes)

local GateService = {}

local services
local lastPad = {} -- [Player] = os.clock() of the last launch

local function gateGroup(zone)
	return "Gate_" .. zone
end

local function lockedGroup(zone)
	return "Locked_" .. zone
end

local function registerGroups()
	for _, gate in ipairs(World.Gates) do
		for _, name in ipairs({ gateGroup(gate.zone), lockedGroup(gate.zone) }) do
			if not PhysicsService:IsCollisionGroupRegistered(name) then
				PhysicsService:RegisterCollisionGroup(name)
			end
		end
	end
	for gateIndex, gate in ipairs(World.Gates) do
		PhysicsService:CollisionGroupSetCollidable(gateGroup(gate.zone), "Default", false)
		for lockedIndex, locked in ipairs(World.Gates) do
			PhysicsService:CollisionGroupSetCollidable(
				gateGroup(gate.zone),
				lockedGroup(locked.zone),
				lockedIndex <= gateIndex
			)
			PhysicsService:CollisionGroupSetCollidable(gateGroup(gate.zone), gateGroup(locked.zone), false)
		end
	end
end

local function groupFor(data)
	for _, gate in ipairs(World.Gates) do
		if data.bestStage < gate.unlockStage then
			return lockedGroup(gate.zone)
		end
	end
	return "Default"
end

local function setCharacterGroup(character, group)
	for _, part in ipairs(character:GetDescendants()) do
		if part:IsA("BasePart") then
			part.CollisionGroup = group
		end
	end
end

function GateService:Refresh(player)
	local data = services.DataService:Get(player)
	local character = player.Character
	if data and character then
		setCharacterGroup(character, groupFor(data))
	end
end

local function watchCharacter(player, character)
	GateService:Refresh(player)
	-- Accessories and shades arrive after spawn.
	character.DescendantAdded:Connect(function(part)
		local data = services.DataService:Get(player)
		if data and part:IsA("BasePart") then
			part.CollisionGroup = groupFor(data)
		end
	end)
end

local function playerFromHit(hit)
	local model = hit:FindFirstAncestorOfClass("Model")
	return model and Players:GetPlayerFromCharacter(model)
end

local function padReady(player)
	local now = os.clock()
	if lastPad[player] and now - lastPad[player] < World.CosmicDojo.PadCooldown then
		return false
	end
	lastPad[player] = now
	return true
end

local function launch(player, destination)
	local character = player.Character
	if not character then
		return
	end
	pcall(function()
		player:RequestStreamAroundAsync(destination)
	end)
	if player.Character == character then
		services.EffectsService:PlayNear(character:GetPivot().Position, 80, "Shockwave", {
			position = character:GetPivot().Position - Vector3.new(0, 3, 0),
			color = World.Colors.Purple,
		})
		character:PivotTo(CFrame.new(destination))
	end
end

local function connectPads(map)
	local Config = World.CosmicDojo

	local launchPad = map:FindFirstChild("LaunchPad", true)
	if launchPad then
		launchPad.Touched:Connect(function(hit)
			local player = playerFromHit(hit)
			local data = player and services.DataService:Get(player)
			if not data or not padReady(player) then
				return
			end
			if data.bestStage >= Config.UnlockStage or data.glowResets >= Config.UnlockGlowResets then
				launch(player, Config.Landing)
			else
				local stageName = Stages.Get(Config.UnlockStage).name
				local message = "Unlocks at " .. stageName .. " or " .. Config.UnlockGlowResets .. " Glow Resets"
				Remotes.Notify:FireClient(player, message)
			end
		end)
	end

	local returnPad = map:FindFirstChild("ReturnPad", true)
	if returnPad then
		returnPad.Touched:Connect(function(hit)
			local player = playerFromHit(hit)
			if player and padReady(player) then
				launch(player, Config.ReturnLanding)
			end
		end)
	end
end

function GateService:Init(allServices)
	services = allServices
end

function GateService:Start()
	registerGroups()

	for _, part in ipairs(workspace:GetDescendants()) do
		if part:IsA("BasePart") and part:HasTag("ZoneGate") then
			part.CollisionGroup = gateGroup(part:GetAttribute("ZoneId"))
		end
	end

	local map = workspace:FindFirstChild("Map")
	if map then
		connectPads(map)
	end

	local function onPlayer(player)
		player.CharacterAdded:Connect(function(character)
			watchCharacter(player, character)
		end)
		if player.Character then
			watchCharacter(player, player.Character)
		end
	end
	Players.PlayerAdded:Connect(onPlayer)
	for _, player in ipairs(Players:GetPlayers()) do
		onPlayer(player)
	end
	Players.PlayerRemoving:Connect(function(player)
		lastPad[player] = nil
	end)

	services.DataService:OnLoaded(function(player)
		self:Refresh(player)
	end)
end

return GateService
