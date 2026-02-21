"""
Archivo __init__ para schemas
"""
from .usuario_schema import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    Token,
    TokenData,
    LoginRequest
)
from .cliente_schema import (
    ClienteBase,
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteWithMascotas
)
from .mascota_schema import (
    MascotaBase,
    MascotaCreate,
    MascotaUpdate,
    MascotaResponse
)
from .producto_schema import (
    ProductoBase,
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse
)
from .venta_schema import (
    VentaBase,
    VentaCreate,
    VentaResponse,
    DetalleVentaBase,
    DetalleVentaCreate,
    DetalleVentaResponse,
    VentaStats
)

__all__ = [
    # Usuario
    "UsuarioBase", "UsuarioCreate", "UsuarioUpdate", "UsuarioResponse",
    "Token", "TokenData", "LoginRequest",
    # Cliente
    "ClienteBase", "ClienteCreate", "ClienteUpdate", "ClienteResponse", "ClienteWithMascotas",
    # Mascota
    "MascotaBase", "MascotaCreate", "MascotaUpdate", "MascotaResponse",
    # Producto
    "ProductoBase", "ProductoCreate", "ProductoUpdate", "ProductoResponse",
    # Venta
    "VentaBase", "VentaCreate", "VentaResponse",
    "DetalleVentaBase", "DetalleVentaCreate", "DetalleVentaResponse",
    "VentaStats"
]
