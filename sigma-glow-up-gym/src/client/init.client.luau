-- Client entry point.

-- Controllers read Shared and the Remotes straight away, so wait for the first replication.
if not game:IsLoaded() then
	game.Loaded:Wait()
end

local Controllers = script:WaitForChild("Controllers")

local SoundController = require(Controllers:WaitForChild("SoundController"))
local HUD = require(Controllers:WaitForChild("HUDController"))
local EffectsController = require(Controllers:WaitForChild("EffectsController"))
local TrainingController = require(Controllers:WaitForChild("TrainingController"))
local CutsceneController = require(Controllers:WaitForChild("CutsceneController"))
local SettingsController = require(Controllers:WaitForChild("SettingsController"))
local LocksController = require(Controllers:WaitForChild("LocksController"))
local DebugController = require(Controllers:WaitForChild("DebugController"))

SoundController.Init()
HUD.Init()
EffectsController.Init(HUD)
TrainingController.Init(HUD)
CutsceneController.Init()
SettingsController.Init(HUD)
LocksController.Init(HUD)
DebugController.Init(HUD)
