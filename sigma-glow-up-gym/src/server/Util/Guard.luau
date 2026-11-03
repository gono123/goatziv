-- Connects a client -> server remote with the checks every handler needs first:
-- data loaded, then the rate limit. Handlers validate their own arguments next.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local RateLimits = require(Shared.Config.RateLimits)
local Remotes = require(Shared.Remotes)
local RateLimiter = require(script.Parent.RateLimiter)

local Guard = {}

function Guard.connect(services, name, handler)
	local perSecond = RateLimits[name]
	assert(perSecond, "Add " .. name .. " to Config/RateLimits")

	Remotes[name].OnServerEvent:Connect(function(player, ...)
		if not services.DataService:IsLoaded(player) then
			return
		end
		if not RateLimiter.allow(player, name, perSecond) then
			return
		end
		handler(player, ...)
	end)
end

return Guard
