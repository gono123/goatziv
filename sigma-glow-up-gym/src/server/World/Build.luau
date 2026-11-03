-- Small helpers for building the map out of parts.

local Build = {}

-- `where` is a CFrame or a Vector3. `extra` is an optional table of more properties.
function Build.part(parent, name, size, where, color, material, extra)
	local part = Instance.new("Part")
	part.Name = name
	part.Anchored = true
	part.Size = size
	part.CFrame = typeof(where) == "CFrame" and where or CFrame.new(where)
	part.Color = color
	part.Material = material or Enum.Material.SmoothPlastic
	part.TopSurface = Enum.SurfaceType.Smooth
	part.BottomSurface = Enum.SurfaceType.Smooth
	if extra then
		for key, value in pairs(extra) do
			part[key] = value
		end
	end
	part.Parent = parent
	return part
end

-- A flat floor centred on `centre`, so its top sits 0.1 above it.
function Build.floor(parent, name, centre, sizeX, sizeZ, color, material)
	return Build.part(parent, name, Vector3.new(sizeX, 0.2, sizeZ), centre, color, material)
end

-- A cylinder running from point a to point b.
function Build.cylinder(parent, name, a, b, diameter, color, material, extra)
	local length = (b - a).Magnitude
	local where = CFrame.lookAt((a + b) / 2, b) * CFrame.Angles(0, math.rad(90), 0)
	local part = Build.part(parent, name, Vector3.new(length, diameter, diameter), where, color, material, extra)
	part.Shape = Enum.PartType.Cylinder
	return part
end

-- A flat disc lying on the ground, centred at `centre`.
function Build.disc(parent, name, centre, diameter, thickness, color, material, extra)
	local where = CFrame.new(centre) * CFrame.Angles(0, 0, math.rad(90))
	local part = Build.part(parent, name, Vector3.new(thickness, diameter, diameter), where, color, material, extra)
	part.Shape = Enum.PartType.Cylinder
	return part
end

function Build.ball(parent, name, centre, diameter, color, material, extra)
	local part = Build.part(parent, name, Vector3.new(diameter, diameter, diameter), centre, color, material, extra)
	part.Shape = Enum.PartType.Ball
	return part
end

-- Big text on one face of a part. The label is named "Text".
function Build.surfaceText(part, face, text, color, guiName)
	local gui = Instance.new("SurfaceGui")
	gui.Name = guiName or "SurfaceText"
	gui.Face = face
	gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
	gui.PixelsPerStud = 20
	gui.LightInfluence = 0

	local label = Instance.new("TextLabel")
	label.Name = "Text"
	label.Size = UDim2.fromScale(1, 1)
	label.BackgroundTransparency = 1
	label.Font = Enum.Font.FredokaOne
	label.TextScaled = true
	label.TextColor3 = color or Color3.new(1, 1, 1)
	label.TextStrokeTransparency = 0.2
	label.Text = text
	label.Parent = gui

	gui.Parent = part
	return gui
end

-- A plate with text on its front. `where` should face the viewer (front = look direction).
function Build.sign(parent, name, text, where, width, height, plateColor, textColor, material)
	local plate = Build.part(parent, name, Vector3.new(width, height, 0.5), where, plateColor, material)
	Build.surfaceText(plate, Enum.NormalId.Front, text, textColor)
	return plate
end

-- Text that always faces the camera, floating above a part. The label is named "Text".
function Build.billboard(part, text, size, offset, maxDistance, guiName)
	local gui = Instance.new("BillboardGui")
	gui.Name = guiName or "Label"
	gui.Size = size
	gui.StudsOffset = offset
	gui.MaxDistance = maxDistance or 90
	gui.LightInfluence = 0

	local label = Instance.new("TextLabel")
	label.Name = "Text"
	label.Size = UDim2.fromScale(1, 1)
	label.BackgroundTransparency = 1
	label.Font = Enum.Font.FredokaOne
	label.TextScaled = true
	label.TextColor3 = Color3.new(1, 1, 1)
	label.TextStrokeTransparency = 0.2
	label.Text = text
	label.Parent = gui

	gui.Parent = part
	return gui
end

function Build.model(parent, name)
	local model = Instance.new("Model")
	model.Name = name
	model.Parent = parent
	return model
end

-- Particles with sensible defaults. Decorative only, so rates stay modest.
function Build.particles(parent, name, color, rate, size, speed, lifetime)
	local emitter = Instance.new("ParticleEmitter")
	emitter.Name = name
	emitter.Color = ColorSequence.new(color)
	emitter.LightEmission = 1
	emitter.Rate = rate
	emitter.Lifetime = NumberRange.new(lifetime or 1, (lifetime or 1) * 1.5)
	emitter.Speed = NumberRange.new(speed or 1, (speed or 1) * 2)
	emitter.SpreadAngle = Vector2.new(180, 180)
	emitter.Size = NumberSequence.new({
		NumberSequenceKeypoint.new(0, size or 0.5),
		NumberSequenceKeypoint.new(1, 0),
	})
	emitter:AddTag("DecorativeParticles") -- switched off on low graphics by EffectsController
	emitter.Parent = parent
	return emitter
end

return Build
