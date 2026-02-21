# Script para iniciar backend y frontend simultáneamente
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Sistema de Gestión Veterinaria" -ForegroundColor Cyan
Write-Host "  Iniciando servicios..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Iniciar backend en segundo plano
Write-Host "1. Iniciando Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-File", "start-backend.ps1"
Write-Host "   ✓ Backend iniciado en nueva ventana" -ForegroundColor Green

# Esperar 3 segundos
Start-Sleep -Seconds 3

# Iniciar frontend
Write-Host "2. Iniciando Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-File", "start-frontend.ps1"
Write-Host "   ✓ Frontend iniciado en nueva ventana" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✓ SISTEMA INICIADO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📚 URLs del sistema:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:4321" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "📝 Credenciales:" -ForegroundColor Cyan
Write-Host "   Usuario: admin" -ForegroundColor White
Write-Host "   Contraseña: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Para cerrar los servidores, cierra las ventanas de PowerShell" -ForegroundColor Yellow
Write-Host ""

# Esperar a que el usuario presione una tecla
Read-Host "Presiona Enter para cerrar esta ventana"
