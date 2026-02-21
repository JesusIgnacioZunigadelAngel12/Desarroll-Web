"""
Archivo __init__ para routes
"""
from .auth_routes import router as auth_router
from .cliente_routes import router as cliente_router
from .mascota_routes import router as mascota_router
from .producto_routes import router as producto_router
from .venta_routes import router as venta_router
from .cita_routes import router as cita_router
from .veterinario_routes import router as veterinario_router

__all__ = [
    "auth_router",
    "cliente_router",
    "mascota_router",
    "producto_router",
    "venta_router",
    "cita_router",
    "veterinario_router"
]
