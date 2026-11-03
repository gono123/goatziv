-- Upgrades panel: spend Aura on levels that last until the next Glow Reset.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local UpgradesConfig = require(Shared.Config.Upgrades)
local Upgrades = require(Shared.Logic.Upgrades)
local NumberFormat = require(Shared.NumberFormat)
local Remotes = require(Shared.Remotes)

local Theme = require(script.Parent.Parent.UI.Theme)
local Components = require(script.Parent.Parent.UI.Components)

local UpgradesController = {}

function UpgradesController.Init(HUD)
	local panel = Components.Panel("Upgrades")
	local _, setBadge = HUD.AddSideButton("Upgrades", "⬆️", "Upgrades", 10, panel.Toggle)

	local rows = {}
	for index, upgrade in ipairs(UpgradesConfig.List) do
		local item = Components.ListItem(upgrade.emoji .. " " .. upgrade.name, upgrade.text)
		item.LayoutOrder = index
		item.Parent = panel.Content

		local buy = Components.Button("", Theme.Orange, UDim2.fromScale(1, 1))
		buy.TextSize = 16
		buy.Parent = item.Action
		buy.Activated:Connect(function()
			Remotes.RequestBuyUpgrade:FireServer(upgrade.id)
		end)

		rows[upgrade.id] = { item = item, buy = buy }
	end

	HUD.OnData(function(data)
		local affordable = 0
		for _, upgrade in ipairs(UpgradesConfig.List) do
			local row = rows[upgrade.id]
			local level = data.upgrades[upgrade.id] or 0
			local cost = Upgrades.Cost(upgrade, level)
			row.item.Title.Text = upgrade.emoji .. " " .. upgrade.name .. "  Lv " .. level .. "/" .. upgrade.maxLevel
			if cost then
				local canBuy = data.aura >= cost
				row.buy.Text = NumberFormat.Abbreviate(cost) .. " Aura"
				row.buy.BackgroundColor3 = canBuy and Theme.Orange or Theme.Dim
				if canBuy then
					affordable = affordable + 1
				end
			else
				row.buy.Text = "MAX"
				row.buy.BackgroundColor3 = Theme.Success
			end
		end
		setBadge(affordable)
	end)
end

return UpgradesController
