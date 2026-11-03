-- An invisible zone gate. GateService decides who collides with it, and the client shows
-- a red force field and a lock sign only to players who are still locked out.

local Build = require(script.Parent.Build)

local Gate = {}

function Gate.Build(parent, zoneId, size, position)
	local part = Build.part(parent, "GateWall", size, position, Color3.fromRGB(229, 72, 77), Enum.Material.ForceField, {
		Transparency = 1,
		CanQuery = false,
	})
	part:SetAttribute("ZoneId", zoneId)
	part:AddTag("ZoneGate")

	local sign = Build.billboard(part, "", UDim2.fromOffset(240, 60), Vector3.new(0, 0, 0), 80, "LockSign")
	sign.Enabled = false
	return part
end

return Gate
