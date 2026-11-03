-- 1234 -> "1.23K", 5600000 -> "5.6M"

local SUFFIXES = { "", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc" }

local NumberFormat = {}

function NumberFormat.Abbreviate(n)
	n = tonumber(n) or 0
	if n < 0 then
		return "-" .. NumberFormat.Abbreviate(-n)
	end
	if n < 1000 then
		return tostring(math.floor(n))
	end

	local index = 1
	while n >= 1000 and index < #SUFFIXES do
		n = n / 1000
		index = index + 1
	end

	local text
	if n >= 100 then
		text = tostring(math.floor(n))
	elseif n >= 10 then
		text = string.format("%.1f", math.floor(n * 10) / 10)
	else
		text = string.format("%.2f", math.floor(n * 100) / 100)
	end

	-- Trim trailing zeros after a decimal point: "5.60" -> "5.6", "5.00" -> "5"
	if string.find(text, ".", 1, true) then
		text = (string.gsub(text, "0+$", ""))
		text = (string.gsub(text, "%.$", ""))
	end

	return text .. SUFFIXES[index]
end

return NumberFormat
