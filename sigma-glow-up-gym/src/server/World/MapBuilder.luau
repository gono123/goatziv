-- Builds the whole map on server start, unless workspace.Map already exists. That way a
-- hand-built map can replace this later: see "Using your own map" in MY_TODO.md.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Lighting = game:GetService("Lighting")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local World = require(Shared.Config.World)

local Build = require(script.Parent.Build)

local Zones = script.Parent.Zones
local ZONE_BUILDERS = {
	require(Zones.SpawnPlaza),
	require(Zones.StarterGym),
	require(Zones.IronYard),
	require(Zones.MogMansion),
	require(Zones.CosmicDojo),
	require(Zones.PoseOffArena),
	require(Zones.TitanPlaza),
	require(Zones.DripShop),
	require(Zones.HallOfMog),
}

local MapBuilder = {}

local function setupBaseplate()
	local baseplate = workspace:FindFirstChild("Baseplate")
	if not baseplate then
		baseplate = Instance.new("Part")
		baseplate.Name = "Baseplate"
		baseplate.Anchored = true
		baseplate.Size = Vector3.new(512, 16, 512)
		baseplate.Position = Vector3.new(0, -8, 0)
		baseplate.Parent = workspace
	end
	baseplate.Color = World.Colors.Baseplate
	baseplate.Material = Enum.Material.Concrete
	for _, child in ipairs(baseplate:GetChildren()) do
		if child:IsA("Texture") then
			child:Destroy()
		end
	end
end

local function setupSpawn()
	local spawn = workspace:FindFirstChildOfClass("SpawnLocation")
	if not spawn then
		spawn = Instance.new("SpawnLocation")
		spawn.Parent = workspace
	end
	spawn.Anchored = true
	spawn.Size = World.Spawn.Size
	spawn.CFrame = CFrame.new(World.Spawn.Position) -- faces -Z, towards the Starter Gym
	spawn.Color = World.Colors.Orange
	spawn.Material = Enum.Material.SmoothPlastic
	spawn.Neutral = true
	spawn.Duration = 0 -- no spawn force field
	for _, child in ipairs(spawn:GetChildren()) do
		if child:IsA("Decal") then
			child:Destroy()
		end
	end
end

local function ensureEffect(className)
	local effect = Lighting:FindFirstChildOfClass(className)
	if not effect then
		effect = Instance.new(className)
		effect.Parent = Lighting
	end
	return effect
end

local function setupLighting()
	local config = World.Lighting
	Lighting.ClockTime = config.ClockTime
	Lighting.Brightness = config.Brightness

	-- Scripts can't always set Technology, so default.project.json sets it too.
	pcall(function()
		Lighting.Technology = Enum.Technology.ShadowMap
	end)

	local atmosphere = ensureEffect("Atmosphere")
	atmosphere.Density = config.AtmosphereDensity
	atmosphere.Haze = config.AtmosphereHaze

	local bloom = ensureEffect("BloomEffect")
	bloom.Intensity = config.BloomIntensity
	bloom.Threshold = config.BloomThreshold

	local color = ensureEffect("ColorCorrectionEffect")
	color.Saturation = config.Saturation
	color.Contrast = config.Contrast
end

function MapBuilder.Build()
	-- Scripts can't always set StreamingEnabled, so default.project.json sets it too.
	pcall(function()
		workspace.StreamingEnabled = true
	end)

	if workspace:FindFirstChild("Map") then
		return
	end

	setupBaseplate()
	setupSpawn()
	setupLighting()

	local map = Build.model(workspace, "Map")
	for _, buildZone in ipairs(ZONE_BUILDERS) do
		buildZone(map)
	end
end

return MapBuilder
