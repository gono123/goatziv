-- Loads, autosaves and saves player data with DataStoreService.
--
-- Prototype-grade: retries + autosave + BindToClose, but no cross-server session
-- locking. Swap the internals for ProfileStore before a public launch; the public
-- API (Get / OnLoaded / IsLoaded) can stay the same.

local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local STORE_NAME = "PlayerData_v1"
local AUTOSAVE_INTERVAL = 120

local TEMPLATE = {
	version = 1,
	aura = 0, -- current Glow Reset cycle
	lifetimeAura = 0,
	stage = 1, -- index into Stages.List (1 = Noob)
	glowResets = 0,
	glowShards = 0,
	dripTokens = 0,
	stats = {
		reps = 0,
		perfects = 0,
	},
	firstJoin = 0,
	lastJoin = 0,
}

local DataService = {}

local profiles = {} -- [Player] = data table
local loadedCallbacks = {}
local store = nil
local memoryOnly = false

local function deepCopy(value)
	if type(value) ~= "table" then
		return value
	end
	local copy = {}
	for k, v in pairs(value) do
		copy[k] = deepCopy(v)
	end
	return copy
end

-- Fill in any fields added to TEMPLATE since the player last saved.
local function reconcile(data, template)
	for key, value in pairs(template) do
		if data[key] == nil then
			data[key] = deepCopy(value)
		elseif type(value) == "table" and type(data[key]) == "table" then
			reconcile(data[key], value)
		end
	end
end

local function withRetries(fn, attempts)
	local lastError
	for attempt = 1, attempts do
		local ok, result = pcall(fn)
		if ok then
			return true, result
		end
		lastError = result
		if attempt < attempts then
			task.wait(math.min(2 ^ attempt, 8))
		end
	end
	return false, lastError
end

local function keyFor(player)
	return "player_" .. player.UserId
end

local function savePlayer(player, data, attempts)
	if memoryOnly or not store or not data then
		return
	end
	local ok, err = withRetries(function()
		store:UpdateAsync(keyFor(player), function()
			return data
		end)
	end, attempts or 3)
	if not ok then
		warn("[DataService] Save failed for " .. player.Name .. ": " .. tostring(err))
	end
end

local function loadPlayer(player)
	local saved = nil

	if not memoryOnly then
		local ok, result = withRetries(function()
			return store:GetAsync(keyFor(player))
		end, 4)

		if ok then
			saved = result
		elseif RunService:IsStudio() then
			warn(
				"[DataService] DataStore unavailable in Studio ("
					.. tostring(result)
					.. "). Using memory-only data. Enable Game Settings > Security > "
					.. "'Enable Studio Access to API Services' to test saving."
			)
			memoryOnly = true
		else
			-- Never let a player play on blank data: it would overwrite their save.
			player:Kick("We couldn't load your gains. Please rejoin!")
			return
		end
	end

	local data
	if type(saved) == "table" then
		data = saved
	else
		data = deepCopy(TEMPLATE)
		data.firstJoin = os.time()
	end
	reconcile(data, TEMPLATE)
	data.lastJoin = os.time()

	if not player.Parent then
		return -- left while loading
	end

	profiles[player] = data
	for _, callback in ipairs(loadedCallbacks) do
		task.spawn(callback, player, data)
	end
end

function DataService:Init()
	local ok, result = pcall(function()
		return DataStoreService:GetDataStore(STORE_NAME)
	end)
	if ok then
		store = result
	else
		warn("[DataService] Could not open DataStore: " .. tostring(result) .. ". Progress will NOT save.")
		memoryOnly = true
	end
end

function DataService:Start()
	Players.PlayerAdded:Connect(loadPlayer)
	for _, player in ipairs(Players:GetPlayers()) do
		task.spawn(loadPlayer, player)
	end

	Players.PlayerRemoving:Connect(function(player)
		local data = profiles[player]
		profiles[player] = nil
		if data then
			savePlayer(player, data, 3)
		end
	end)

	game:BindToClose(function()
		local pending = 0
		for player, data in pairs(profiles) do
			pending = pending + 1
			task.spawn(function()
				savePlayer(player, data, 2)
				pending = pending - 1
			end)
		end
		local deadline = os.clock() + 25
		while pending > 0 and os.clock() < deadline do
			task.wait(0.1)
		end
	end)

	task.spawn(function()
		while true do
			task.wait(AUTOSAVE_INTERVAL)
			for player, data in pairs(profiles) do
				task.spawn(savePlayer, player, data, 2)
			end
		end
	end)
end

-- Returns the live data table (mutate it directly), or nil if not loaded yet.
function DataService:Get(player)
	return profiles[player]
end

function DataService:IsLoaded(player)
	return profiles[player] ~= nil
end

-- callback(player, data) runs once per player when their data loads.
function DataService:OnLoaded(callback)
	table.insert(loadedCallbacks, callback)
	for player, data in pairs(profiles) do
		task.spawn(callback, player, data)
	end
end

return DataService
