# Script para iniciar el frontend
Write-Host "🚀 Iniciando Frontend (Astro)..." -ForegroundColor Cyan
Write-Host ""

Set-Location frontend

Write-Host "✓ Frontend ejecutándose en http://localhost:4321" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

npm run dev
