"""
Aplicación principal FastAPI - Sistema de Veterinaria
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config.settings import settings
from src.config.database import init_db
from src.routes import (
    auth_router,
    cliente_router,
    mascota_router,
    producto_router,
    venta_router,
    cita_router,
    veterinario_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación
    Se ejecuta al iniciar y cerrar el servidor
    """
    # Inicializar base de datos
    print("[INFO] Inicializando base de datos...")
    init_db()
    print("[INFO] Base de datos inicializada correctamente")
    
    yield
    
    print("[INFO] Cerrando aplicacion...")


# Crear instancia de FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API REST para sistema de gestión veterinaria con FastAPI y SQLite",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registrar rutas
app.include_router(auth_router)
app.include_router(cliente_router)
app.include_router(mascota_router)
app.include_router(producto_router)
app.include_router(venta_router)
app.include_router(cita_router)
app.include_router(veterinario_router)


@app.get("/")
def root():
    """
    Endpoint raíz - Información de la API
    """
    return {
        "mensaje": "Bienvenido al Sistema de Gestión Veterinaria",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """
    Endpoint para verificar el estado de la API
    """
    return {
        "status": "healthy",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
