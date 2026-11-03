-- Server entry point. Services are plain modules with Init(services) and Start().

local Services = script:WaitForChild("Services")

local ORDER = { "DataService", "EvolutionService", "TrainingService" }

local services = {}
for _, name in ipairs(ORDER) do
	services[name] = require(Services:WaitForChild(name))
end

for _, name in ipairs(ORDER) do
	services[name]:Init(services)
end

require(script:WaitForChild("Greybox")).Build()

for _, name in ipairs(ORDER) do
	services[name]:Start()
end

print("[SigmaGlowUpGym] Server started")
