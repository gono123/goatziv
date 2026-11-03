# Runs every check: format, lint, unit tests, Rojo build. Stops at the first failure.
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

function Invoke-Step($title, $exe, [string[]]$arguments) {
	Write-Host "== $title =="
	& $exe @arguments
	if ($LASTEXITCODE -ne 0) {
		Write-Host "FAILED: $title"
		exit $LASTEXITCODE
	}
}

Invoke-Step "stylua" "stylua" @("--check", "src", "tests")
Invoke-Step "selene" "selene" @("src")
Invoke-Step "lune tests" "lune" @("run", "tests/run")
Invoke-Step "rojo build" "rojo" @("build", "-o", "build.rbxl")
Write-Host "All checks passed."
