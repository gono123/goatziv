-- Client entry point.

local Controllers = script:WaitForChild("Controllers")

local HUD = require(Controllers:WaitForChild("HUDController"))
local TrainingController = require(Controllers:WaitForChild("TrainingController"))
local CutsceneController = require(Controllers:WaitForChild("CutsceneController"))

HUD.Init()
TrainingController.Init(HUD)
CutsceneController.Init()
