$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root "backend\.venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "Ambiente Python não encontrado. Execute primeiro o setup do README."
    exit 1
}

Set-Location (Join-Path $root "backend")
& $python -m pytest -q