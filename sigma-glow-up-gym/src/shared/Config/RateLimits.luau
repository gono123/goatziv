-- Calls per second allowed for each client -> server remote (see Util/Guard).

return {
	RequestRep = 5,
	RequestStopTraining = 2,
	RequestGlowReset = 1,
	RequestSync = 2,
	RequestSetSettings = 5,
	DebugCommand = 10,
}
