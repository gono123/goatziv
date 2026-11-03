-- Single source of truth for RemoteEvents. The server creates them; clients wait for them.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local EVENT_NAMES = {
	-- server -> client
	"TrainingStarted", -- (equipmentId, displayName)
	"TrainingStopped", -- ()
	"RepResult", -- (auraGained, wasLucky)
	"StageUp", -- (stageIndex, stageName)
	"GlowResetDone", -- (glowResets, shardsGained)
	"DataSync", -- (snapshot table)
	"Notify", -- (message)
	"PlayEffect", -- (effectName, params table)
	"SpinResult", -- (brainrotId, isNew, duplicateDrip)

	-- client -> server
	"RequestRep", -- ()
	"RequestStopTraining", -- ()
	"RequestGlowReset", -- ()
	"RequestSync", -- ()
	"RequestSetSettings", -- (musicVolume, sfxVolume, lowEffects)
	"DebugCommand", -- (commandName, argument) admins only, re-checked on the server
	"RequestBuyUpgrade", -- (upgradeId)
	"RequestSpin", -- ()
	"RequestEquipBrainrot", -- (brainrotId)
}

local Remotes = {}

if RunService:IsServer() then
	local folder = ReplicatedStorage:FindFirstChild("Remotes")
	if not folder then
		folder = Instance.new("Folder")
		folder.Name = "Remotes"
		folder.Parent = ReplicatedStorage
	end
	for _, name in ipairs(EVENT_NAMES) do
		local remote = folder:FindFirstChild(name)
		if not remote then
			remote = Instance.new("RemoteEvent")
			remote.Name = name
			remote.Parent = folder
		end
		Remotes[name] = remote
	end
else
	local folder = ReplicatedStorage:WaitForChild("Remotes")
	for _, name in ipairs(EVENT_NAMES) do
		Remotes[name] = folder:WaitForChild(name)
	end
end

return Remotes
