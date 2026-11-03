-- Finds and runs every tests/*.spec.luau. Run from the project root: lune run tests/run

local fs = require("@lune/fs")
local luau = require("@lune/luau")
local process = require("@lune/process")

local T = require("./helpers")

local specs = {}
for _, name in fs.readDir("tests") do
	if string.sub(name, -10) == ".spec.luau" then
		table.insert(specs, name)
	end
end
table.sort(specs)

for _, name in specs do
	print("-- " .. name)
	local path = "tests/" .. name
	local ok, err = pcall(function()
		luau.load(fs.readFile(path), { debugName = path })(T)
	end)
	if not ok then
		T.recordLoadFailure(path, err)
	end
end

local passed, failed = T.summary()
print(string.format("\n%d passed, %d failed", passed, failed))
process.exit(if failed > 0 then 1 else 0)
