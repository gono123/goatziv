-- Daily brainrot spin panel: odds, spin reel, collection and equipping.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Brainrots = require(Shared.Config.Brainrots)
local BrainrotSpin = require(Shared.Logic.BrainrotSpin)
local Upgrades = require(Shared.Logic.Upgrades)
local Remotes = require(Shared.Remotes)

local Theme = require(script.Parent.Parent.UI.Theme)
local Components = require(script.Parent.Parent.UI.Components)
local SoundController = require(script.Parent.SoundController)
local EffectsController = require(script.Parent.EffectsController)

local REEL_SECONDS = 2
local REEL_STEP = 0.08
local SECONDS_PER_DAY = 86400
-- Prizes this rare get confetti.
local CELEBRATE = { Epic = true, Legendary = true, Mythic = true }

local BrainrotController = {}

local panel, reelLabel, spinButton, oddsLabel, setBadge, chip, setChipText
local latest = nil
local spinning = false
local rowsKey = nil
local rows = {}

local function timeUntilNextSpin()
	local left = SECONDS_PER_DAY - os.time() % SECONDS_PER_DAY
	return string.format("%02d:%02d:%02d", math.floor(left / 3600), math.floor(left / 60) % 60, left % 60)
end

local function refreshSpinButton()
	if spinning or not latest then
		return
	end
	if latest.brainrots.canSpin then
		spinButton.Text = "SPIN!"
		spinButton.BackgroundColor3 = Theme.Orange
	else
		spinButton.Text = "Next spin in " .. timeUntilNextSpin()
		spinButton.BackgroundColor3 = Theme.Dim
	end
end

local function refreshOdds(data)
	local parts = {}
	for _, entry in ipairs(BrainrotSpin.Odds(Upgrades.SpinLuck(data.upgrades))) do
		table.insert(parts, entry.rarity.id .. " " .. string.format("%.1f", entry.odds * 100) .. "%")
	end
	oddsLabel.Text = "Odds: " .. table.concat(parts, " · ")
end

local function refreshChip(data)
	local brainrot = Brainrots.ById[data.brainrots.equipped]
	chip.Visible = brainrot ~= nil
	if brainrot then
		setChipText(brainrot.emoji .. " " .. brainrot.name .. " " .. BrainrotSpin.Describe(brainrot))
		chip.BackgroundColor3 = Brainrots.RarityById[brainrot.rarity].color
	end
end

-- The list only changes on a spin or equip, while data arrives on every rep.
local function refreshCollection(data)
	local state = data.brainrots
	local keyParts = { tostring(state.equipped) }
	for _, brainrot in ipairs(Brainrots.List) do
		table.insert(keyParts, tostring(state.owned[brainrot.id] or 0))
	end
	local key = table.concat(keyParts, ",")
	if key == rowsKey then
		return
	end
	rowsKey = key

	for _, row in ipairs(rows) do
		row:Destroy()
	end
	rows = {}

	for index, brainrot in ipairs(Brainrots.List) do
		local count = state.owned[brainrot.id]
		local rarity = Brainrots.RarityById[brainrot.rarity]
		local title = "❓ ???"
		local subtitle = brainrot.rarity .. " - not found yet"
		if count then
			title = brainrot.emoji .. " " .. brainrot.name .. (count > 1 and (" x" .. count) or "")
			subtitle = brainrot.rarity .. " - " .. BrainrotSpin.Describe(brainrot)
		end

		local item = Components.ListItem(title, subtitle)
		item.LayoutOrder = 10 + index
		item.Title.TextColor3 = count and rarity.color or Theme.Dim
		item.Parent = panel.Content
		table.insert(rows, item)

		if count then
			local isEquipped = state.equipped == brainrot.id
			local button = Components.Button(
				isEquipped and "EQUIPPED" or "EQUIP",
				isEquipped and Theme.Success or Theme.Teal,
				UDim2.fromScale(1, 1)
			)
			button.TextSize = 16
			button.Parent = item.Action
			button.Activated:Connect(function()
				Remotes.RequestEquipBrainrot:FireServer(brainrot.id)
			end)
		end
	end
end

local function playReel(prize, isNew, dripBonus)
	spinning = true
	spinButton.Text = "SPINNING..."
	spinButton.BackgroundColor3 = Theme.Dim
	SoundController.Play("Spin")

	local finish = os.clock() + REEL_SECONDS
	while os.clock() < finish do
		local shown = Brainrots.List[math.random(#Brainrots.List)]
		reelLabel.Text = shown.emoji .. " " .. shown.name
		reelLabel.TextColor3 = Theme.Text
		task.wait(REEL_STEP)
	end

	local rarity = Brainrots.RarityById[prize.rarity]
	reelLabel.Text = prize.emoji .. " " .. prize.name .. " (" .. prize.rarity .. ")"
	reelLabel.TextColor3 = rarity.color
	if CELEBRATE[prize.rarity] then
		EffectsController.Confetti()
		SoundController.Play("Purchase")
	end

	local detail = BrainrotSpin.Describe(prize)
	if isNew then
		Components.Toast("NEW! " .. prize.name .. ": " .. detail)
	else
		Components.Toast("Duplicate " .. prize.name .. ": +" .. dripBonus .. " Drip")
	end

	spinning = false
	refreshSpinButton()
end

local function build(HUD)
	panel = Components.Panel("Daily Spin")
	local button
	button, setBadge = HUD.AddSideButton("Spin", "🎰", "Spin", 20, function()
		panel.Toggle()
	end)
	button.LayoutOrder = 20

	chip, setChipText = Components.Chip("", Theme.Teal)
	chip.Name = "BrainrotChip"
	chip.Visible = false
	chip.Parent = HUD.GetChipRow()

	reelLabel = Components.Label("Spin for a brainrot!", 24)
	reelLabel.Size = UDim2.new(1, 0, 0, 44)
	reelLabel.LayoutOrder = 1
	reelLabel.Parent = panel.Content

	spinButton = Components.Button("", Theme.Orange, UDim2.new(1, -8, 0, 54))
	spinButton.LayoutOrder = 2
	spinButton.Parent = panel.Content
	spinButton.Activated:Connect(function()
		if not spinning and latest and latest.brainrots.canSpin then
			Remotes.RequestSpin:FireServer()
		end
	end)

	oddsLabel = Components.Label("", 13, Theme.BodyFont)
	oddsLabel.Size = UDim2.new(1, -8, 0, 36)
	oddsLabel.TextWrapped = true
	oddsLabel.LayoutOrder = 3
	oddsLabel.Parent = panel.Content
end

function BrainrotController.Init(HUD)
	build(HUD)

	HUD.OnData(function(data)
		latest = data
		setBadge(data.brainrots.canSpin and 1 or 0)
		refreshSpinButton()
		refreshOdds(data)
		refreshChip(data)
		refreshCollection(data)
	end)

	Remotes.SpinResult.OnClientEvent:Connect(function(prizeId, isNew, dripBonus)
		local prize = Brainrots.ById[prizeId]
		if prize then
			panel.Open()
			playReel(prize, isNew, dripBonus)
		end
	end)

	-- Keeps the countdown on the button moving while the panel is open.
	task.spawn(function()
		while true do
			task.wait(1)
			if panel.IsOpen() then
				refreshSpinButton()
			end
		end
	end)
end

return BrainrotController
