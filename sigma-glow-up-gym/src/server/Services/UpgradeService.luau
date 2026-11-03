-- Upgrades bought with Aura.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local UpgradesConfig = require(Shared.Config.Upgrades)
local Upgrades = require(Shared.Logic.Upgrades)
local Remotes = require(Shared.Remotes)
local Validate = require(script.Parent.Parent.Util.Validate)
local Guard = require(script.Parent.Parent.Util.Guard)

local UpgradeService = {}

local services

function UpgradeService:Init(allServices)
	services = allServices
end

function UpgradeService:Start()
	Guard.connect(services, "RequestBuyUpgrade", function(player, upgradeId)
		if not Validate.key(upgradeId, UpgradesConfig.ById) then
			return
		end
		local data = services.DataService:Get(player)
		local upgrade = UpgradesConfig.ById[upgradeId]
		local level = data.upgrades[upgradeId] or 0
		local cost = Upgrades.Cost(upgrade, level)
		if not cost then
			return
		end
		if not services.EconomyService:SpendAura(player, cost, "upgrade") then
			Remotes.Notify:FireClient(player, "Not enough Aura yet!")
			return
		end
		data.upgrades[upgradeId] = level + 1
		services.EvolutionService:Sync(player)
	end)
end

return UpgradeService
