local T = ...
local QuestPicker = T.load("src/shared/Logic/QuestPicker.luau")
local Quests = T.load("src/shared/Config/Quests.luau")

local function ids(list)
	local out = {}
	for _, quest in ipairs(list) do
		table.insert(out, quest.id)
	end
	return table.concat(out, ",")
end

T.test("same user and day give the same quests", function()
	T.eq(ids(QuestPicker.Pick(Quests.Pool, 123, 20000, 3)), ids(QuestPicker.Pick(Quests.Pool, 123, 20000, 3)))
end)

T.test("picks vary across days", function()
	local seen = {}
	local distinct = 0
	for day = 20000, 20020 do
		local key = ids(QuestPicker.Pick(Quests.Pool, 123, day, 3))
		if not seen[key] then
			seen[key] = true
			distinct = distinct + 1
		end
	end
	T.truthy(distinct >= 5, "only " .. distinct .. " distinct sets in 21 days")
end)

T.test("no duplicate kinds", function()
	for day = 20000, 20200 do
		local kinds = {}
		local picks = QuestPicker.Pick(Quests.Pool, 987654, day, Quests.PerDay)
		T.eq(#picks, Quests.PerDay)
		for _, quest in ipairs(picks) do
			T.falsy(kinds[quest.kind], "duplicate kind " .. quest.kind)
			kinds[quest.kind] = true
		end
	end
end)

T.test("excluded kinds never appear", function()
	for day = 20000, 20050 do
		for _, quest in ipairs(QuestPicker.Pick(Quests.Pool, 5, day, 3, 0, { stageUps = true })) do
			T.truthy(quest.kind ~= "stageUps")
		end
	end
end)

T.test("salt changes the picks", function()
	local changed = false
	for day = 20000, 20020 do
		if ids(QuestPicker.Pick(Quests.Pool, 5, day, 3, 0)) ~= ids(QuestPicker.Pick(Quests.Pool, 5, day, 3, 1)) then
			changed = true
		end
	end
	T.truthy(changed)
end)

T.test("asking for more than the kinds available returns what exists", function()
	local pool = { { id = "a", kind = "x" }, { id = "b", kind = "x" } }
	T.eq(#QuestPicker.Pick(pool, 1, 1, 3), 1)
end)
