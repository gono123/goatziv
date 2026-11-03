-- Owns every currency change, so analytics and client sync happen in exactly one place.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Economy = require(Shared.Logic.Economy)

local EconomyService = {}

local services

function EconomyService:Init(allServices)
	services = allServices
end

function EconomyService:Start() end

function EconomyService:AddAura(player, amount, _source)
	local data = services.DataService:Get(player)
	if not data or not Economy.IsValidAmount(amount) then
		return false
	end
	data.aura = data.aura + amount
	data.cycleAura = data.cycleAura + amount
	data.lifetimeAura = data.lifetimeAura + amount
	services.EvolutionService:CheckStage(player)
	services.EvolutionService:Sync(player)
	return true
end

local function add(player, field, amount)
	local data = services.DataService:Get(player)
	if not data or not Economy.IsValidAmount(amount) then
		return false
	end
	data[field] = data[field] + amount
	services.EvolutionService:Sync(player)
	return true
end

local function spend(player, field, amount)
	local data = services.DataService:Get(player)
	if not data or not Economy.CanAfford(data[field], amount) then
		return false
	end
	data[field] = data[field] - amount
	services.EvolutionService:Sync(player)
	return true
end

-- Spending never lowers stage progress: stages use cycleAura.
function EconomyService:SpendAura(player, amount, _sink)
	return spend(player, "aura", amount)
end

function EconomyService:AddDrip(player, amount, _source)
	return add(player, "dripTokens", amount)
end

function EconomyService:SpendDrip(player, amount, _sink)
	return spend(player, "dripTokens", amount)
end

function EconomyService:AddShards(player, amount, _source)
	return add(player, "glowShards", amount)
end

function EconomyService:SpendShards(player, amount, _sink)
	return spend(player, "glowShards", amount)
end

return EconomyService
