-- Shared UI building blocks. Each returns the instance it built. Where a part needs
-- updating later, a second return value is a small function that does it.

local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")

local Theme = require(script.Parent.Theme)
local SoundController = require(script.Parent.Parent.Controllers.SoundController)

local player = Players.LocalPlayer

local Components = {}

local function corner(parent, radius)
	local c = Instance.new("UICorner")
	c.CornerRadius = UDim.new(0, radius)
	c.Parent = parent
	return c
end

local function textStroke(parent, thickness)
	local s = Instance.new("UIStroke")
	s.Thickness = thickness or 2
	s.Color = Theme.Stroke
	s.ApplyStrokeMode = Enum.ApplyStrokeMode.Contextual
	s.Parent = parent
	return s
end

Components.Corner = corner
Components.TextStroke = textStroke

function Components.ScreenGui(name, displayOrder)
	local gui = Instance.new("ScreenGui")
	gui.Name = name
	gui.ResetOnSpawn = false
	gui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
	gui.ScreenInsets = Enum.ScreenInsets.DeviceSafeInsets
	gui.DisplayOrder = displayOrder or 0
	gui.Parent = player:WaitForChild("PlayerGui")
	return gui
end

-- A transparent label with the standard font and stroke.
function Components.Label(text, textSize, font)
	local label = Instance.new("TextLabel")
	label.BackgroundTransparency = 1
	label.Font = font or Theme.HeaderFont
	label.TextColor3 = Theme.Text
	label.TextSize = textSize or 20
	label.Text = text or ""
	textStroke(label, 2)
	return label
end

local function addPressFeedback(button)
	local scale = Instance.new("UIScale")
	scale.Parent = button
	local quick = TweenInfo.new(0.08, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
	button.InputBegan:Connect(function(input)
		local t = input.UserInputType
		if t == Enum.UserInputType.MouseButton1 or t == Enum.UserInputType.Touch then
			TweenService:Create(scale, quick, { Scale = 0.94 }):Play()
		end
	end)
	button.InputEnded:Connect(function(input)
		local t = input.UserInputType
		if t == Enum.UserInputType.MouseButton1 or t == Enum.UserInputType.Touch then
			TweenService:Create(scale, quick, { Scale = 1 }):Play()
		end
	end)
	button.Activated:Connect(function()
		SoundController.Play("Click")
	end)
end

-- size is a UDim2. Height is raised to the minimum tap size if needed.
function Components.Button(text, color, size)
	local button = Instance.new("TextButton")
	button.BackgroundColor3 = color or Theme.Orange
	button.Font = Theme.HeaderFont
	button.TextColor3 = Theme.Text
	button.TextSize = 20
	button.Text = text
	button.Size = size or UDim2.fromOffset(160, Theme.MinTapSize)
	corner(button, Theme.ButtonRadius)
	textStroke(button, 2)

	local limit = Instance.new("UISizeConstraint")
	limit.MinSize = Vector2.new(Theme.MinTapSize, Theme.MinTapSize)
	limit.Parent = button

	addPressFeedback(button)
	return button
end

-- 64 x 64 button with an emoji and a small label under it.
function Components.IconButton(emoji, labelText)
	local button = Instance.new("TextButton")
	button.Size = UDim2.fromOffset(64, 64)
	button.BackgroundColor3 = Theme.Panel
	button.BackgroundTransparency = Theme.PanelTransparency
	button.Text = ""
	corner(button, Theme.ButtonRadius)

	local icon = Components.Label(emoji, 28)
	icon.Name = "Icon"
	icon.Size = UDim2.new(1, 0, 0, 40)
	icon.Position = UDim2.fromOffset(0, 2)
	icon.Parent = button

	local label = Components.Label(labelText, 13)
	label.Name = "Caption"
	label.Size = UDim2.new(1, 0, 0, 18)
	label.Position = UDim2.fromOffset(0, 43)
	label.Parent = button

	addPressFeedback(button)
	return button
end

-- Returns the bar, and setProgress(0..1).
function Components.ProgressBar(size, color)
	local bar = Instance.new("Frame")
	bar.Size = size or UDim2.new(1, 0, 0, 22)
	bar.BackgroundColor3 = Theme.Panel
	corner(bar, 11)

	local outline = Instance.new("UIStroke")
	outline.Thickness = 2
	outline.Color = Theme.Stroke
	outline.Parent = bar

	local fill = Instance.new("Frame")
	fill.Name = "Fill"
	fill.Size = UDim2.fromScale(0, 1)
	fill.BackgroundColor3 = color or Theme.Teal
	corner(fill, 11)
	fill.Parent = bar

	local function setProgress(value)
		TweenService:Create(fill, TweenInfo.new(0.15, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
			Size = UDim2.fromScale(math.clamp(value, 0, 1), 1),
		}):Play()
	end
	return bar, setProgress
end

-- Pill for boosts and timers. Grows to fit its text. Returns the pill and setText(text).
function Components.Chip(text, color)
	local chip = Instance.new("Frame")
	chip.AutomaticSize = Enum.AutomaticSize.X
	chip.Size = UDim2.fromOffset(0, 30)
	chip.BackgroundColor3 = color or Theme.Teal
	corner(chip, 15)

	local padding = Instance.new("UIPadding")
	padding.PaddingLeft = UDim.new(0, 12)
	padding.PaddingRight = UDim.new(0, 12)
	padding.Parent = chip

	local label = Components.Label(text, 16)
	label.Name = "Text"
	label.AutomaticSize = Enum.AutomaticSize.X
	label.Size = UDim2.fromScale(0, 1)
	label.Parent = chip

	return chip, function(newText)
		label.Text = newText
	end
end

-- Red notification dot in the corner of parent. Returns the dot and setCount(n); 0 hides it.
function Components.Badge(parent)
	local badge = Instance.new("Frame")
	badge.Name = "Badge"
	badge.AnchorPoint = Vector2.new(1, 0)
	badge.Position = UDim2.new(1, 4, 0, -4)
	badge.Size = UDim2.fromOffset(22, 22)
	badge.BackgroundColor3 = Theme.Danger
	badge.Visible = false
	badge.ZIndex = 5
	corner(badge, 11)
	badge.Parent = parent

	local label = Components.Label("", 14)
	label.Size = UDim2.fromScale(1, 1)
	label.ZIndex = 5
	label.Parent = badge

	return badge, function(count)
		badge.Visible = count > 0
		label.Text = tostring(count)
	end
end

-- Row with `onSelect(index, name)`. Returns the row and selectTab(index).
function Components.Tabs(names, onSelect)
	local row = Instance.new("Frame")
	row.BackgroundTransparency = 1
	row.Size = UDim2.new(1, 0, 0, Theme.MinTapSize)

	local layout = Instance.new("UIListLayout")
	layout.FillDirection = Enum.FillDirection.Horizontal
	layout.SortOrder = Enum.SortOrder.LayoutOrder
	layout.Padding = UDim.new(0, 6)
	layout.Parent = row

	local buttons = {}
	local function selectTab(index)
		for i, button in ipairs(buttons) do
			button.BackgroundColor3 = (i == index) and Theme.Orange or Theme.Dim
		end
		if onSelect then
			onSelect(index, names[index])
		end
	end

	local width = 1 / #names
	for index, name in ipairs(names) do
		local button = Components.Button(name, Theme.Dim, UDim2.new(width, -6, 1, 0))
		button.LayoutOrder = index
		button.TextSize = 16
		button.Parent = row
		buttons[index] = button
		button.Activated:Connect(function()
			selectTab(index)
		end)
	end

	return row, selectTab
end

-- Row with a title, a smaller line under it and an empty "Action" slot on the right.
function Components.ListItem(titleText, subtitleText)
	local item = Instance.new("Frame")
	item.Size = UDim2.new(1, 0, 0, 64)
	item.BackgroundColor3 = Color3.new(1, 1, 1)
	item.BackgroundTransparency = 0.92
	corner(item, Theme.ButtonRadius)

	local title = Components.Label(titleText, 18)
	title.Name = "Title"
	title.Position = UDim2.fromOffset(12, 8)
	title.Size = UDim2.new(1, -150, 0, 24)
	title.TextXAlignment = Enum.TextXAlignment.Left
	title.Parent = item

	local subtitle = Components.Label(subtitleText, 13, Theme.BodyFont)
	subtitle.Name = "Subtitle"
	subtitle.Position = UDim2.fromOffset(12, 34)
	subtitle.Size = UDim2.new(1, -150, 0, 22)
	subtitle.TextXAlignment = Enum.TextXAlignment.Left
	subtitle.TextWrapped = true
	subtitle.Parent = item

	local action = Instance.new("Frame")
	action.Name = "Action"
	action.AnchorPoint = Vector2.new(1, 0.5)
	action.Position = UDim2.new(1, -8, 0.5, 0)
	action.Size = UDim2.fromOffset(130, Theme.MinTapSize)
	action.BackgroundTransparency = 1
	action.Parent = item

	return item
end

-- ---------------------------------------------------------------------------
-- Panels: centered modal windows. Only one is open at a time.
-- ---------------------------------------------------------------------------

local panelGui = nil
local openPanel = nil

local function getPanelGui()
	if not panelGui then
		panelGui = Components.ScreenGui("Panels", 20)
	end
	return panelGui
end

-- Returns { Content = scrolling list frame, Open(), Close(), Toggle(), IsOpen(), OnOpen = fn or nil }.
function Components.Panel(titleText)
	local panel = {}

	local backdrop = Instance.new("TextButton")
	backdrop.Name = titleText .. "Panel"
	backdrop.Size = UDim2.fromScale(1, 1)
	backdrop.BackgroundColor3 = Color3.new(0, 0, 0)
	backdrop.BackgroundTransparency = 0.5
	backdrop.Text = ""
	backdrop.AutoButtonColor = false
	backdrop.Visible = false
	backdrop.Parent = getPanelGui()

	local frame = Instance.new("Frame")
	frame.Name = "Window"
	frame.Active = true -- taps inside the window must not reach the backdrop
	frame.AnchorPoint = Vector2.new(0.5, 0.5)
	frame.Position = UDim2.fromScale(0.5, 0.5)
	frame.Size = UDim2.fromScale(0.9, 0.9)
	frame.BackgroundColor3 = Theme.Panel
	frame.BackgroundTransparency = Theme.PanelTransparency
	corner(frame, Theme.PanelRadius)
	frame.Parent = backdrop

	local limit = Instance.new("UISizeConstraint")
	limit.MaxSize = Vector2.new(560, 520)
	limit.Parent = frame

	local title = Components.Label(titleText, 26)
	title.Name = "Title"
	title.Position = UDim2.fromOffset(16, 6)
	title.Size = UDim2.new(1, -80, 0, 44)
	title.TextXAlignment = Enum.TextXAlignment.Left
	title.Parent = frame

	local close = Components.Button("X", Theme.Danger, UDim2.fromOffset(48, 48))
	close.Name = "Close"
	close.AnchorPoint = Vector2.new(1, 0)
	close.Position = UDim2.new(1, -6, 0, 4)
	close.Parent = frame

	local content = Instance.new("ScrollingFrame")
	content.Name = "Content"
	content.Position = UDim2.fromOffset(12, 56)
	content.Size = UDim2.new(1, -24, 1, -68)
	content.BackgroundTransparency = 1
	content.BorderSizePixel = 0
	content.ScrollBarThickness = 6
	content.CanvasSize = UDim2.fromOffset(0, 0)
	content.AutomaticCanvasSize = Enum.AutomaticSize.Y
	content.ScrollingDirection = Enum.ScrollingDirection.Y
	content.Parent = frame

	local layout = Instance.new("UIListLayout")
	layout.SortOrder = Enum.SortOrder.LayoutOrder
	layout.Padding = UDim.new(0, 8)
	layout.Parent = content

	panel.Content = content

	function panel.IsOpen()
		return backdrop.Visible
	end

	function panel.Close()
		backdrop.Visible = false
		if openPanel == panel then
			openPanel = nil
		end
	end

	function panel.Open()
		if openPanel and openPanel ~= panel then
			openPanel.Close()
		end
		openPanel = panel
		backdrop.Visible = true
		if panel.OnOpen then
			panel.OnOpen()
		end
	end

	function panel.Toggle()
		if panel.IsOpen() then
			panel.Close()
		else
			panel.Open()
		end
	end

	close.Activated:Connect(panel.Close)
	backdrop.Activated:Connect(panel.Close)

	return panel
end

-- ---------------------------------------------------------------------------
-- Toasts and floating text
-- ---------------------------------------------------------------------------

local feedbackGui = nil
local toastLabel = nil
local toastToken = 0

local function getFeedbackGui()
	if not feedbackGui then
		feedbackGui = Components.ScreenGui("Feedback", 30)
	end
	return feedbackGui
end

function Components.Toast(text)
	if not toastLabel then
		toastLabel = Components.Label("", 22)
		toastLabel.Name = "Toast"
		toastLabel.AnchorPoint = Vector2.new(0.5, 0)
		toastLabel.Position = UDim2.new(0.5, 0, 0, 150)
		toastLabel.Size = UDim2.new(0.9, 0, 0, 34)
		toastLabel.TextWrapped = true
		toastLabel.Parent = getFeedbackGui()
	end

	toastToken = toastToken + 1
	local token = toastToken
	toastLabel.Text = text
	toastLabel.Visible = true
	task.delay(2.5, function()
		if token == toastToken then
			toastLabel.Visible = false
		end
	end)
end

-- Floating text that rises and fades (rep results and so on).
function Components.Popup(text, color, scale)
	local label = Components.Label(text, math.floor(30 * (scale or 1)))
	label.AnchorPoint = Vector2.new(0.5, 0.5)
	label.Position = UDim2.fromScale(0.5 + (math.random() - 0.5) * 0.12, 0.62)
	label.Size = UDim2.fromOffset(300, 50)
	label.TextColor3 = color or Theme.Text
	label.Parent = getFeedbackGui()

	local stroke = label:FindFirstChildOfClass("UIStroke")
	local info = TweenInfo.new(0.9, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
	TweenService:Create(stroke, info, { Transparency = 1 }):Play()
	local tween = TweenService:Create(label, info, {
		Position = label.Position - UDim2.fromScale(0, 0.12),
		TextTransparency = 1,
	})
	tween:Play()
	tween.Completed:Connect(function()
		label:Destroy()
	end)
end

return Components
