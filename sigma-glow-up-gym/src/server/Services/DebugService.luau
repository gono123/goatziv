-- Debug and admin commands for testing. The server re-checks admin on every command.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Admins = require(Shared.Config.Admins)
local Stages = require(Shared.Config.Stages)
local FastMode = require(Shared.FastMode)
local Remotes = require(Shared.Remotes)
local Validate = require(script.Parent.Parent.Util.Validate)
local Guard = require(script.Parent.Parent.Util.Guard)

local MAX_GRANT = 1e12

local DebugService = {}

local services

local function isAdmin(player)
	if RunService:IsStudio() then
		return true
	end
	if game.CreatorType == Enum.CreatorType.User and player.UserId == game.CreatorId then
		return true
	end
	return table.find(Admins.UserIds, player.UserId) ~= nil
end

local function notify(player, message)
	Remotes.Notify:FireClient(player, message)
end

-- Calls a method on a service that may not be built yet.
local function callService(player, serviceName, method, ...)
	local service = services[serviceName]
	if service and service[method] then
		service[method](service, ...)
	else
		notify(player, serviceName .. " is not built yet")
	end
end

local commands = {}

function commands.AddAura(player, amount)
	if Validate.number(amount, 1, MAX_GRANT) then
		services.EconomyService:AddAura(player, amount, "debug")
	end
end

function commands.AddDrip(player, amount)
	if Validate.number(amount, 1, MAX_GRANT) then
		services.EconomyService:AddDrip(player, amount, "debug")
	end
end

function commands.AddShards(player, amount)
	if Validate.number(amount, 1, MAX_GRANT) then
		services.EconomyService:AddShards(player, amount, "debug")
	end
end

function commands.SetStage(player, index)
	if not Validate.integer(index, 1, #Stages.List) then
		return
	end
	local data = services.DataService:Get(player)
	data.aura = Stages.List[index].auraRequired
	data.cycleAura = data.aura
	if index < data.stage then
		data.stage = index
		services.EvolutionService:ApplyLook(player)
	else
		services.EvolutionService:CheckStage(player)
	end
	services.EvolutionService:Sync(player)
end

function commands.GlowResetNow(player)
	local data = services.DataService:Get(player)
	data.stage = math.max(data.stage, Stages.GlowResetStage)
	services.EvolutionService:GlowReset(player)
end

function commands.DayOffset(player)
	local offset = (player:GetAttribute("DebugDayOffset") or 0) + 1
	player:SetAttribute("DebugDayOffset", offset)
	notify(player, "Day offset is now +" .. offset)
	services.EvolutionService:Sync(player)
end

function commands.ResetData(player)
	services.TrainingService:Stop(player)
	services.DataService:Reset(player)
	services.EvolutionService:Sync(player)
	player:LoadCharacter()
	notify(player, "Your data was reset")
end

function commands.FastMode(player)
	FastMode.Set(not FastMode.IsOn())
	notify(player, "Fast mode " .. (FastMode.IsOn() and "ON" or "OFF"))
end

function commands.StartTitan(player)
	callService(player, "TitanService", "DebugStart")
end

function commands.TitanSkipPhase(player)
	callService(player, "TitanService", "DebugSkipPhase")
end

function commands.StartPoseOffBots(player)
	callService(player, "PoseOffService", "DebugStartWithBots", player)
end

function commands.AddQueueBot(player)
	callService(player, "PoseOffService", "DebugAddBot")
end

function commands.GrantAllPoses(player)
	callService(player, "PoseService", "GrantAll", player)
end

function commands.GrantAllCosmetics(player)
	callService(player, "CosmeticService", "GrantAll", player)
end

function commands.GrantAllBrainrots(player)
	services.BrainrotService:GrantAll(player)
end

function commands.FreeSpin(player)
	services.BrainrotService:ResetSpin(player)
end

function commands.SimulatePurchase(player, productName)
	if RunService:IsStudio() and Validate.str(productName) then
		callService(player, "ShopService", "DebugGrant", player, productName)
	end
end

function DebugService:Init(allServices)
	services = allServices
end

function DebugService:Start()
	local function onPlayer(player)
		player:SetAttribute("IsAdmin", isAdmin(player))
	end
	Players.PlayerAdded:Connect(onPlayer)
	for _, player in ipairs(Players:GetPlayers()) do
		onPlayer(player)
	end

	Guard.connect(services, "DebugCommand", function(player, command, argument)
		if not isAdmin(player) or not Validate.key(command, commands) then
			return
		end
		commands[command](player, argument)
	end)
end

return DebugService
