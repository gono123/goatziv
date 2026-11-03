-- Plays named sounds from Config/Sounds. Names with an empty id are skipped silently.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local SoundService = game:GetService("SoundService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Sounds = require(Shared.Config.Sounds)

local SoundController = {}

local cache = {}
local musicVolume = 0.5
local sfxVolume = 0.8
local currentMusic = nil
local activeLoops = {}

local function getSound(name)
	local id = Sounds[name]
	if not id or id == "" then
		return nil
	end
	local sound = cache[name]
	if not sound then
		sound = Instance.new("Sound")
		sound.Name = name
		sound.SoundId = id
		sound.Parent = SoundService
		cache[name] = sound
	end
	return sound
end

function SoundController.Play(name)
	local sound = getSound(name)
	if sound then
		sound.Volume = sfxVolume
		sound.TimePosition = 0
		sound:Play()
	end
end

-- Looping effect, such as the LOCKED IN beat.
function SoundController.StartLoop(name)
	local sound = getSound(name)
	if sound and not activeLoops[name] then
		activeLoops[name] = sound
		sound.Looped = true
		sound.Volume = sfxVolume
		sound:Play()
	end
end

function SoundController.StopLoop(name)
	local sound = activeLoops[name]
	if sound then
		activeLoops[name] = nil
		sound:Stop()
	end
end

function SoundController.PlayMusic(name)
	local sound = getSound(name)
	if currentMusic and currentMusic ~= sound then
		currentMusic:Stop()
	end
	currentMusic = sound
	if sound and not sound.IsPlaying then
		sound.Looped = true
		sound.Volume = musicVolume
		sound:Play()
	end
end

function SoundController.SetVolumes(music, sfx)
	musicVolume = music
	sfxVolume = sfx
	if currentMusic then
		currentMusic.Volume = music
	end
	for _, sound in pairs(activeLoops) do
		sound.Volume = sfx
	end
end

function SoundController.Init()
	SoundController.PlayMusic("Music_Gym")
end

return SoundController
