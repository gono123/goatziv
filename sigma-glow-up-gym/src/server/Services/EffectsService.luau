-- Sends visuals other players should see. Clients spawn the actual effects locally.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Remotes = require(Shared.Remotes)

local EffectsService = {}

function EffectsService:Init() end

function EffectsService:Start() end

function EffectsService:PlayAll(name, params)
	Remotes.PlayEffect:FireAllClients(name, params)
end

function EffectsService:PlayFor(player, name, params)
	Remotes.PlayEffect:FireClient(player, name, params)
end

function EffectsService:PlayNear(position, radius, name, params)
	for _, player in ipairs(Players:GetPlayers()) do
		local character = player.Character
		local root = character and character:FindFirstChild("HumanoidRootPart")
		if root and (root.Position - position).Magnitude <= radius then
			Remotes.PlayEffect:FireClient(player, name, params)
		end
	end
end

return EffectsService
