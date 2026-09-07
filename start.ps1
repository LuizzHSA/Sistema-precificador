$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $root "backend"
$frontend = Join-Path $root "frontend"
$python = Join-Path $backend ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "Ambiente Python não encontrado. Execute: cd backend; python -m venv .venv; .\.venv\Scripts\python.exe -m pip install -r requirements.txt"
    exit 1
}

$env:SECRET_KEY = "local-secret-key-change-me"
$env:JWT_SECRET_KEY = "local-jwt-secret-key-change-me"
$env:AUTH_EMAIL = "admin@pricetracker.com"
$env:AUTH_PASSWORD_HASH = & $python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('admin123'))"
$env:AUTH_NAME = "Administrador"

& $python (Join-Path $backend "init_db.py")
& $python (Join-Path $backend "seed.py")
Start-Process -FilePath $python -ArgumentList "main.py" -WorkingDirectory $backend
Start-Process -FilePath $python -ArgumentList "-m", "http.server", "8080" -WorkingDirectory $frontend
Start-Process "http://localhost:8080"

Write-Host "Projeto iniciado em http://localhost:8080"
Write-Host "Login: admin@pricetracker.com / admin123"