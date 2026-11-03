-- Tiny test kit plus a loader that runs pure game modules outside Roblox.
--
-- T.load("src/shared/Formula.luau") runs the file with a fake `script` tree, where
-- `script.Parent.Config.Training` resolves straight to the loaded config table and
-- `require` simply returns its argument.

local fs = require("@lune/fs")
local luau = require("@lune/luau")
local roblox = require("@lune/roblox")

local T = {}

local passed = 0
local failed = 0

function T.test(name, fn)
	local ok, err = pcall(fn)
	if ok then
		passed = passed + 1
	else
		failed = failed + 1
		print("  FAIL " .. name .. "\n       " .. tostring(err))
	end
end

function T.recordLoadFailure(path, err)
	failed = failed + 1
	print("  FAIL could not run " .. path .. "\n       " .. tostring(err))
end

function T.summary()
	return passed, failed
end

function T.eq(actual, expected, message)
	if actual ~= expected then
		error((message or "values differ") .. ": got " .. tostring(actual) .. ", wanted " .. tostring(expected), 2)
	end
end

function T.near(actual, expected, tolerance, message)
	if math.abs(actual - expected) > tolerance then
		error((message or "values not close") .. ": got " .. tostring(actual) .. ", wanted " .. tostring(expected), 2)
	end
end

function T.truthy(value, message)
	if not value then
		error(message or "expected a truthy value", 2)
	end
end

function T.falsy(value, message)
	if value then
		error(message or "expected a falsy value", 2)
	end
end

local stubs = {
	Color3 = {
		fromRGB = function(r, g, b)
			return { R = r / 255, G = g / 255, B = b / 255 }
		end,
	},
	Vector3 = {
		new = function(x, y, z)
			return { X = x, Y = y, Z = z }
		end,
	},
	game = {
		GetService = function(_, name)
			return {
				Name = name,
				PlayerRemoving = {
					Connect = function() end,
				},
			}
		end,
	},
}

local function resolve(dir, expression)
	for part in string.gmatch(expression, "[^%.]+") do
		if part == "Parent" then
			dir = string.match(dir, "^(.*)/[^/]+$") or "."
		else
			dir = dir .. "/" .. part
		end
	end
	return dir
end

-- Each loader keeps its own cache, because modules see different globals.
-- `makeGlobals(makeNode)` returns the globals a module runs with.
local function createLoader(makeGlobals)
	local cache = {}
	local load

	-- The tree may only read the cache: Lune's file functions cannot run inside a metamethod,
	-- so load() first loads every dependency it finds in the source.
	local function makeNode(dir)
		return setmetatable({}, {
			__index = function(_, key)
				if key == "Parent" then
					return makeNode(string.match(dir, "^(.*)/[^/]+$") or ".")
				end
				local child = dir .. "/" .. key
				local cached = cache[child .. ".luau"]
				if cached ~= nil then
					return cached
				end
				return makeNode(child)
			end,
		})
	end

	local globals = makeGlobals(makeNode)

	local function loadDependencies(path, source)
		local own = string.gsub(path, "%.luau$", "")

		for expression in string.gmatch(source, "require%(script%.([%w_%.]+)%)") do
			load(resolve(own, expression) .. ".luau")
		end
		for expression in string.gmatch(source, "require%(Shared%.([%w_%.]+)%)") do
			load("src/shared/" .. string.gsub(expression, "%.", "/") .. ".luau")
		end
		for expression in string.gmatch(source, 'WaitForChild%("Shared"%)%.([%w_%.]+)%)') do
			load("src/shared/" .. string.gsub(expression, "%.", "/") .. ".luau")
		end

		-- Aliases such as: local Zones = script.Parent.Zones
		for alias, expression in string.gmatch(source, "local ([%w_]+) = script%.([%w_%.]+)[\r\n]") do
			local aliasDir = resolve(own, expression)
			for child in string.gmatch(source, "require%(" .. alias .. "%.([%w_]+)%)") do
				load(aliasDir .. "/" .. child .. ".luau")
			end
		end
	end

	load = function(path)
		if cache[path] ~= nil then
			return cache[path]
		end

		local source = fs.readFile(path)
		loadDependencies(path, source)

		local env = {
			script = { Parent = makeNode(string.match(path, "^(.*)/[^/]+$")) },
			require = function(value)
				return value
			end,
		}
		for key, value in pairs(globals) do
			env[key] = value
		end

		local result = luau.load(source, { debugName = path, environment = env })()
		cache[path] = result
		return result
	end

	return load
end

-- Pure modules: only the small stubs above.
T.load = createLoader(function()
	return stubs
end)

-- World code: real Roblox datatypes and instances from Lune, so a wrong property name fails.
T.robloxGame = roblox.Instance.new("DataModel")
T.loadRoblox = createLoader(function(makeNode)
	local realGame = T.robloxGame
	return {
		Instance = roblox.Instance,
		Vector2 = roblox.Vector2,
		Vector3 = roblox.Vector3,
		CFrame = roblox.CFrame,
		Color3 = roblox.Color3,
		UDim = roblox.UDim,
		UDim2 = roblox.UDim2,
		Enum = roblox.Enum,
		NumberRange = roblox.NumberRange,
		NumberSequence = roblox.NumberSequence,
		NumberSequenceKeypoint = roblox.NumberSequenceKeypoint,
		ColorSequence = roblox.ColorSequence,
		workspace = realGame:GetService("Workspace"),
		game = {
			GetService = function(_, name)
				if name == "ReplicatedStorage" then
					return {
						WaitForChild = function(_, child)
							return makeNode("src/" .. string.lower(child))
						end,
					}
				end
				return realGame:GetService(name)
			end,
		},
	}
end)

-- Small seeded generator, so simulations give the same result every run.
function T.rng(seed)
	local state = seed
	return function()
		state = (state * 1664525 + 1013904223) % 4294967296
		return state / 4294967296
	end
end

return T
