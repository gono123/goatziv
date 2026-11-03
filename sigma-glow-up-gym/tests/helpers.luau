-- Tiny test kit plus a loader that runs pure game modules outside Roblox.
--
-- T.load("src/shared/Formula.luau") runs the file with a fake `script` tree, where
-- `script.Parent.Config.Training` resolves straight to the loaded config table and
-- `require` simply returns its argument.

local fs = require("@lune/fs")
local luau = require("@lune/luau")

local T = {}

local passed = 0
local failed = 0
local cache = {}

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

-- The tree may only read the cache: Lune's file functions cannot run inside a metamethod,
-- so T.load loads every dependency it finds in the source before running the file.
local function makeNode(dir)
	return setmetatable({}, {
		__index = function(_, key)
			if key == "Parent" then
				return makeNode(string.match(dir, "^(.*)/[^/]+$") or ".")
			end
			local child = dir .. "/" .. key
			return cache[child .. ".luau"] or makeNode(child)
		end,
	})
end

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

function T.load(path)
	if cache[path] ~= nil then
		return cache[path]
	end

	local source = fs.readFile(path)
	local dir = string.match(path, "^(.*)/[^/]+$")
	for expression in string.gmatch(source, "require%(script%.([%w_%.]+)%)") do
		T.load(resolve(string.gsub(path, "%.luau$", ""), expression) .. ".luau")
	end

	local env = {
		script = { Parent = makeNode(dir) },
		require = function(value)
			return value
		end,
		Color3 = stubs.Color3,
		Vector3 = stubs.Vector3,
		game = stubs.game,
	}

	local result = luau.load(source, { debugName = path, environment = env })()
	cache[path] = result
	return result
end

-- Small seeded generator, so simulations give the same result every run.
function T.rng(seed)
	local state = seed
	return function()
		state = (state * 1664525 + 1013904223) % 4294967296
		return state / 4294967296
	end
end

return T
