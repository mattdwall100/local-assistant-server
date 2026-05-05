$repoRoot = Split-Path -Parent $PSScriptRoot
$clientRoot = Join-Path $repoRoot "clients/windows-mic-client"
$env:PYTHONPATH = Join-Path $clientRoot "src"

Push-Location $clientRoot
try {
    python -m windows_mic_client.main
}
finally {
    Pop-Location
}
