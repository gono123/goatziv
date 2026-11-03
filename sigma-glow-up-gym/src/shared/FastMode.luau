-- Debug "fast mode": shortens cooldowns and timers while testing. Off unless an admin
-- turns it on through the debug panel. The workspace attribute replicates to clients.

local FAST_ATTRIBUTE = "DebugFastMode"
local COOLDOWN_DIVISOR = 10
local TIMER_DIVISOR = 5

local FastMode = {}

function FastMode.IsOn()
	return workspace:GetAttribute(FAST_ATTRIBUTE) == true
end

function FastMode.Set(on)
	workspace:SetAttribute(FAST_ATTRIBUTE, on)
end

function FastMode.Cooldown(seconds)
	if FastMode.IsOn() then
		return seconds / COOLDOWN_DIVISOR
	end
	return seconds
end

function FastMode.Timer(seconds)
	if FastMode.IsOn() then
		return seconds / TIMER_DIVISOR
	end
	return seconds
end

return FastMode
