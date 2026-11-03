-- Runs the real MapBuilder against Lune's Roblox engine stand-in. This catches wrong
-- property names and bad values in the world code, and checks the part budget.

local T = ...

local World = T.loadRoblox("src/shared/Config/World.luau")
local Equipment = T.loadRoblox("src/shared/Config/Equipment.luau")
local MapBuilder = T.loadRoblox("src/server/World/MapBuilder.luau")

MapBuilder.Build()

local workspace = T.robloxGame:GetService("Workspace")
local map = workspace:FindFirstChild("Map")

local function descendantsTagged(tag)
	local found = {}
	for _, instance in ipairs(map:GetDescendants()) do
		if instance:HasTag(tag) then
			table.insert(found, instance)
		end
	end
	return found
end

T.test("map builds", function()
	T.truthy(map, "workspace.Map should exist")
	T.truthy(workspace:FindFirstChild("Baseplate"))
	T.truthy(workspace:FindFirstChildOfClass("SpawnLocation"))
end)

T.test("part budget", function()
	local parts = 0
	for _, instance in ipairs(map:GetDescendants()) do
		if instance:IsA("BasePart") then
			parts = parts + 1
		end
	end
	print("     map parts: " .. parts)
	T.truthy(parts <= 3500, parts .. " parts is over budget")
end)

T.test("every zone exists", function()
	for _, name in ipairs({
		"SpawnPlaza",
		"StarterGym",
		"IronYard",
		"MogMansion",
		"CosmicDojo",
		"PoseOffArena",
		"TitanPlaza",
		"DripShop",
		"HallOfMog",
	}) do
		T.truthy(map:FindFirstChild(name), name)
	end
end)

T.test("each machine has three stations with base, marker and label", function()
	local counts = {}
	for _, model in ipairs(descendantsTagged("Equipment")) do
		local id = model:GetAttribute("EquipmentId")
		T.truthy(Equipment[id], "unknown equipment " .. tostring(id))
		counts[id] = (counts[id] or 0) + 1
		T.truthy(model.PrimaryPart and model.PrimaryPart.Name == "Base", id .. " needs a Base")
		T.truthy(model:FindFirstChild("StationMarker"), id .. " needs a StationMarker")
		T.truthy(model:FindFirstChild("Label", true), id .. " needs a Label")
	end
	for id in pairs(Equipment) do
		T.eq(counts[id], 3, id)
	end
end)

T.test("every station's standing spot is inside the training range", function()
	local Training = T.loadRoblox("src/shared/Config/Training.luau")
	T.truthy(World.StationStandOffset < Training.TrainRange)
end)

T.test("every gate has a zone listed in World.Gates", function()
	local known = {}
	for _, gate in ipairs(World.Gates) do
		known[gate.zone] = true
	end
	local gates = descendantsTagged("ZoneGate")
	T.eq(#gates, #World.Gates)
	for _, gate in ipairs(gates) do
		T.truthy(known[gate:GetAttribute("ZoneId")])
	end
end)

T.test("gates are listed lowest stage first", function()
	for i = 2, #World.Gates do
		T.truthy(World.Gates[i].unlockStage > World.Gates[i - 1].unlockStage)
	end
end)

T.test("arena has what the Pose-Off needs", function()
	local arena = map:FindFirstChild("PoseOffArena")
	for i = 1, 4 do
		T.truthy(arena:FindFirstChild("Pedestal" .. i), "Pedestal" .. i)
		T.truthy(arena:FindFirstChild("Spotlight" .. i), "Spotlight" .. i)
	end
	T.truthy(arena:FindFirstChild("QueuePad"))
	T.truthy(arena:FindFirstChild("ScoreboardPanel"))
end)
