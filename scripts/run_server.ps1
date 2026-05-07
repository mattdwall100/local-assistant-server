$repoRoot = Split-Path -Parent $PSScriptRoot
echo $PSScriptRoot
$env:PYTHONPATH = Join-Path $repoRoot "src"

Push-Location $repoRoot
try {
    python -m assistant_server.main
}
finally {
    Pop-Location
}
