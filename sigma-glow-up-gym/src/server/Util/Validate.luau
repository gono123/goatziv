-- Argument checks for remote handlers. A client can send anything, so check everything.

local Validate = {}

-- A finite number, optionally inside min..max.
function Validate.number(value, min, max)
	if type(value) ~= "number" or value ~= value or value == math.huge or value == -math.huge then
		return false
	end
	if min ~= nil and value < min then
		return false
	end
	if max ~= nil and value > max then
		return false
	end
	return true
end

function Validate.integer(value, min, max)
	return Validate.number(value, min, max) and math.floor(value) == value
end

-- A string no longer than maxLength (default 64).
function Validate.str(value, maxLength)
	return type(value) == "string" and #value <= (maxLength or 64)
end

function Validate.bool(value)
	return type(value) == "boolean"
end

-- A string that is a key of the given table. Rejects non-strings first, because
-- indexing a table with NaN or a client-made table is never what we want.
function Validate.key(value, tbl)
	return Validate.str(value) and rawget(tbl, value) ~= nil
end

-- A value equal to one of the items in a list.
function Validate.oneOf(value, list)
	for _, item in ipairs(list) do
		if item == value then
			return true
		end
	end
	return false
end

return Validate
