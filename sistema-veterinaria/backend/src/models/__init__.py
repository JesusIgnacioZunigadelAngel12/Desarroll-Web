"""
Archivo __init__ para importar todos los modelos
"""
from .usuario import Usuario
from .cliente import Cliente
from .mascota import Mascota
from .producto import Producto
from .venta import Venta, DetalleVenta
from .cita import Cita
from .veterinario import Veterinario

__all__ = [
    "Usuario",
    "Cliente",
    "Mascota",
    "Producto",
    "Venta",
    "DetalleVenta",
    "Cita",
    "Veterinario"
]
