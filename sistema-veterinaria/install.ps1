# Script de instalación completa para Sistema Veterinaria
# PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Sistema de Gestión Veterinaria" -ForegroundColor Cyan
Write-Host "  Instalación Completa" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ $pythonVersion encontrado" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Python no encontrado. Por favor instala Python 3.8+" -ForegroundColor Red
    exit 1
}

# Verificar Node.js
Write-Host "2. Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "   ✓ Node.js $nodeVersion encontrado" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Node.js no encontrado. Por favor instala Node.js 16+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INSTALANDO BACKEND" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ir al directorio backend
Set-Location backend

# Crear entorno virtual
Write-Host "3. Creando entorno virtual de Python..." -ForegroundColor Yellow
python -m venv venv
Write-Host "   ✓ Entorno virtual creado" -ForegroundColor Green

# Activar entorno virtual
Write-Host "4. Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "   ✓ Entorno virtual activado" -ForegroundColor Green

# Instalar dependencias
Write-Host "5. Instalando dependencias de Python..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "   ✓ Dependencias instaladas" -ForegroundColor Green

# Verificar archivo .env
if (-not (Test-Path ".env")) {
    Write-Host "6. Creando archivo .env..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "   ✓ Archivo .env creado" -ForegroundColor Green
} else {
    Write-Host "6. Archivo .env ya existe" -ForegroundColor Green
}

# Inicializar base de datos
Write-Host "7. Inicializando base de datos..." -ForegroundColor Yellow
python -m src.database.init_data
Write-Host "   ✓ Base de datos inicializada con datos de ejemplo" -ForegroundColor Green

# Volver al directorio raíz
Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INSTALANDO FRONTEND" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ir al directorio frontend
Set-Location frontend

# Instalar dependencias
Write-Host "8. Instalando dependencias de Node.js..." -ForegroundColor Yellow
npm install --silent
Write-Host "   ✓ Dependencias instaladas" -ForegroundColor Green

# Verificar archivo .env
if (-not (Test-Path ".env")) {
    Write-Host "9. Creando archivo .env..." -ForegroundColor Yellow
    "PUBLIC_API_URL=http://localhost:8000" | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "   ✓ Archivo .env creado" -ForegroundColor Green
} else {
    Write-Host "9. Archivo .env ya existe" -ForegroundColor Green
}

# Volver al directorio raíz
Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✓ INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Credenciales por defecto:" -ForegroundColor Cyan
Write-Host "   Usuario: admin" -ForegroundColor White
Write-Host "   Contraseña: admin123" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Para iniciar el sistema:" -ForegroundColor Cyan
Write-Host "   1. Backend:  .\start-backend.ps1" -ForegroundColor White
Write-Host "   2. Frontend: .\start-frontend.ps1" -ForegroundColor White
Write-Host "   3. O ambos:  .\start-all.ps1" -ForegroundColor White
Write-Host ""
Write-Host "📚 URLs del sistema:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:4321" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
