# Script para iniciar el backend
Write-Host "🚀 Iniciando Backend (FastAPI)..." -ForegroundColor Cyan
Write-Host ""

Set-Location backend

# Activar entorno virtual
& .\venv\Scripts\Activate.ps1

# Iniciar servidor
Write-Host "✓ Backend ejecutándose en http://localhost:8000" -ForegroundColor Green
Write-Host "✓ Documentación API en http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

python -m src.main
