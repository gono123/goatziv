-- Colours, fonts and sizes used by every screen (MASTER_PROMPT Part 4).

local Theme = {
	Orange = Color3.fromHex("#FF8A1F"),
	Teal = Color3.fromHex("#1FC7B6"),
	Gold = Color3.fromHex("#FFD23F"),
	Panel = Color3.fromHex("#1B1B26"),
	PanelTransparency = 0.08,
	Text = Color3.fromHex("#FFFFFF"),
	Stroke = Color3.fromHex("#000000"),
	Success = Color3.fromHex("#3DD68C"),
	Danger = Color3.fromHex("#E5484D"),
	Dim = Color3.fromHex("#8A8A99"),

	HeaderFont = Enum.Font.FredokaOne,
	BodyFont = Enum.Font.GothamBold,

	PanelRadius = 14,
	ButtonRadius = 12,
	MinTapSize = 48,

	-- Height of Roblox's own top bar. Side UI starts below this so nothing overlaps it.
	TopBarHeight = 60,

	Rarity = {
		Common = Color3.fromHex("#9CA3AF"),
		Rare = Color3.fromHex("#3B82F6"),
		Epic = Color3.fromHex("#A855F7"),
		Legendary = Color3.fromHex("#FFD23F"),
	},
}

return Theme
