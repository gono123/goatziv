-- Settings panel: music and SFX volume, low-effects mode. Saved on the server.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Remotes = require(Shared.Remotes)

local Theme = require(script.Parent.Parent.UI.Theme)
local Components = require(script.Parent.Parent.UI.Components)
local SoundController = require(script.Parent.SoundController)

local STEP = 0.1
local SEND_DELAY = 0.4 -- group quick taps into one save

local SettingsController = {}

local settings = { music = 0.5, sfx = 0.8, lowEffects = false }
local refreshers = {}
local sendToken = 0

local function refresh()
	for _, fn in ipairs(refreshers) do
		fn()
	end
	SoundController.SetVolumes(settings.music, settings.sfx)
end

local function send()
	sendToken = sendToken + 1
	local token = sendToken
	task.delay(SEND_DELAY, function()
		if token == sendToken then
			Remotes.RequestSetSettings:FireServer(settings.music, settings.sfx, settings.lowEffects)
		end
	end)
end

local function addVolumeRow(panel, order, title, field)
	local item = Components.ListItem(title, "")
	item.LayoutOrder = order
	item.Parent = panel.Content

	local minus = Components.Button("-", Theme.Dim, UDim2.fromOffset(48, 48))
	minus.Parent = item.Action
	local plus = Components.Button("+", Theme.Orange, UDim2.fromOffset(48, 48))
	plus.AnchorPoint = Vector2.new(1, 0)
	plus.Position = UDim2.fromScale(1, 0)
	plus.Parent = item.Action

	local function change(delta)
		local value = math.clamp(settings[field] + delta, 0, 1)
		settings[field] = math.floor(value * 10 + 0.5) / 10
		refresh()
		send()
	end
	minus.Activated:Connect(function()
		change(-STEP)
	end)
	plus.Activated:Connect(function()
		change(STEP)
	end)

	table.insert(refreshers, function()
		item.Subtitle.Text = math.floor(settings[field] * 100 + 0.5) .. "%"
	end)
end

local function addLowEffectsRow(panel, order)
	local item = Components.ListItem("Low effects", "Fewer particles. Runs faster on older phones.")
	item.LayoutOrder = order
	item.Parent = panel.Content

	local toggle = Components.Button("OFF", Theme.Dim, UDim2.fromScale(1, 1))
	toggle.Parent = item.Action
	toggle.Activated:Connect(function()
		settings.lowEffects = not settings.lowEffects
		refresh()
		send()
	end)

	table.insert(refreshers, function()
		toggle.Text = settings.lowEffects and "ON" or "OFF"
		toggle.BackgroundColor3 = settings.lowEffects and Theme.Success or Theme.Dim
	end)
end

function SettingsController.Init(HUD)
	local panel = Components.Panel("Settings")
	addVolumeRow(panel, 1, "Music", "music")
	addVolumeRow(panel, 2, "Sound effects", "sfx")
	addLowEffectsRow(panel, 3)

	HUD.AddSideButton("Settings", "⚙️", "Settings", 100, panel.Toggle)

	HUD.OnData(function(data)
		-- Don't overwrite a change that is still waiting to be sent.
		if data.settings and not panel.IsOpen() then
			settings.music = data.settings.music
			settings.sfx = data.settings.sfx
			settings.lowEffects = data.settings.lowEffects
			refresh()
		end
	end)
	refresh()
end

return SettingsController
