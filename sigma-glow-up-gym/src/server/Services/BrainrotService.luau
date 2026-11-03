-- Daily brainrot spin: one free spin per UTC day. Prizes give permanent Aura help
-- while equipped. Never affects Pose-Off scoring.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Brainrots = require(Shared.Config.Brainrots)
local BrainrotSpin = require(Shared.Logic.BrainrotSpin)
local Streak = require(Shared.Logic.Streak)
local Upgrades = require(Shared.Logic.Upgrades)
local Remotes = require(Shared.Remotes)
local Validate = require(script.Parent.Parent.Util.Validate)
local Guard = require(script.Parent.Parent.Util.Guard)

local BrainrotService = {}

local services

local function today(player)
	return Streak.Day(os.time(), player:GetAttribute("DebugDayOffset"))
end

local function equippedOf(data)
	return Brainrots.ById[data.brainrots.equipped]
end

function BrainrotService:GetAuraMultiplier(player)
	local data = services.DataService:Get(player)
	local brainrot = data and equippedOf(data)
	return brainrot and brainrot.auraMult or 1
end

function BrainrotService:GetLuckyBonus(player)
	local data = services.DataService:Get(player)
	local brainrot = data and equippedOf(data)
	return brainrot and brainrot.luckyBonus or 0
end

-- The part of DataSync the spin panel needs.
function BrainrotService:Snapshot(player, data)
	return {
		owned = data.brainrots.owned,
		equipped = data.brainrots.equipped,
		canSpin = BrainrotSpin.CanSpin(data.brainrots.lastSpinDay, today(player)),
	}
end

function BrainrotService:GrantAll(player)
	local data = services.DataService:Get(player)
	for _, brainrot in ipairs(Brainrots.List) do
		data.brainrots.owned[brainrot.id] = data.brainrots.owned[brainrot.id] or 1
	end
	services.EvolutionService:Sync(player)
end

function BrainrotService:ResetSpin(player)
	local data = services.DataService:Get(player)
	data.brainrots.lastSpinDay = 0
	services.EvolutionService:Sync(player)
end

local function spin(player)
	local data = services.DataService:Get(player)
	local state = data.brainrots
	local day = today(player)
	if not BrainrotSpin.CanSpin(state.lastSpinDay, day) then
		return
	end
	-- Mark the day first, so nothing below can ever pay out twice.
	state.lastSpinDay = day

	local prize = BrainrotSpin.Pick(math.random(), math.random(), Upgrades.SpinLuck(data.upgrades))
	local isNew = state.owned[prize.id] == nil
	state.owned[prize.id] = (state.owned[prize.id] or 0) + 1

	local dripBonus = 0
	if not isNew then
		dripBonus = Brainrots.RarityById[prize.rarity].duplicateDrip
		services.EconomyService:AddDrip(player, dripBonus, "spinDuplicate")
	end

	local current = equippedOf(data)
	if not current or BrainrotSpin.Strength(prize) > BrainrotSpin.Strength(current) then
		state.equipped = prize.id
	end

	services.EvolutionService:Sync(player)
	Remotes.SpinResult:FireClient(player, prize.id, isNew, dripBonus)
end

function BrainrotService:Init(allServices)
	services = allServices
end

function BrainrotService:Start()
	Guard.connect(services, "RequestSpin", spin)

	Guard.connect(services, "RequestEquipBrainrot", function(player, brainrotId)
		if not Validate.key(brainrotId, Brainrots.ById) then
			return
		end
		local data = services.DataService:Get(player)
		if data.brainrots.owned[brainrotId] then
			data.brainrots.equipped = brainrotId
			services.EvolutionService:Sync(player)
		end
	end)
end

return BrainrotService
