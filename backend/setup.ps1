# ClearScan — one-time local setup (PowerShell)
# Run from the backend/ directory

Write-Host "==> Creating virtual environment..." -ForegroundColor Cyan
python -m venv .venv

Write-Host "==> Activating venv..." -ForegroundColor Cyan
.\.venv\Scripts\Activate.ps1

Write-Host "==> Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Write-Host "==> Creating .env from template..." -ForegroundColor Cyan
    Copy-Item .env.example .env
    Write-Host "  ** Open backend/.env and fill in DATABASE_URL and ANTHROPIC_API_KEY **" -ForegroundColor Yellow
} else {
    Write-Host "==> .env already exists, skipping." -ForegroundColor Green
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "  1. Edit backend/.env with your DATABASE_URL and ANTHROPIC_API_KEY"
Write-Host "  2. flask db init   (first time only)"
Write-Host "  3. flask db migrate -m 'initial'"
Write-Host "  4. flask db upgrade"
Write-Host "  5. python app.py"
