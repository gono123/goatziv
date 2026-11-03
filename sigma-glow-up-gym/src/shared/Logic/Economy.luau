-- Currency checks and purchase idempotency (BUILD_SPEC M9, M10). Pure: no Roblox services.

local Economy = {}

-- True for positive, finite numbers: the only amounts a currency change may use.
function Economy.IsValidAmount(amount)
	return type(amount) == "number" and amount == amount and amount > 0 and amount < math.huge
end

function Economy.CanAfford(balance, cost)
	return Economy.IsValidAmount(cost) and balance >= cost
end

function Economy.HasPurchase(purchases, purchaseId)
	for _, id in ipairs(purchases) do
		if id == purchaseId then
			return true
		end
	end
	return false
end

-- Remembers a receipt id, keeping only the newest maxKept ids.
function Economy.RecordPurchase(purchases, purchaseId, maxKept)
	table.insert(purchases, purchaseId)
	while #purchases > maxKept do
		table.remove(purchases, 1)
	end
end

-- Runs grant() at most once per receipt id. Returns "AlreadyGranted", "Granted" or "Failed".
-- A grant that errors or returns false is not recorded, so Roblox retries it later.
function Economy.ProcessReceipt(purchases, purchaseId, maxKept, grant)
	if Economy.HasPurchase(purchases, purchaseId) then
		return "AlreadyGranted"
	end
	local ok, result = pcall(grant)
	if not ok or result == false then
		return "Failed"
	end
	Economy.RecordPurchase(purchases, purchaseId, maxKept)
	return "Granted"
end

return Economy
