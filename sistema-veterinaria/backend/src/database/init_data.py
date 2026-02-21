"""
Script para inicializar datos de ejemplo en la base de datos
"""
from sqlalchemy.orm import Session
from src.config.database import SessionLocal, init_db
from src.models.usuario import Usuario
from src.models.cliente import Cliente
from src.models.mascota import Mascota
from src.models.producto import Producto
from src.middleware.auth import get_password_hash


def crear_usuario_admin(db: Session):
    """Crea un usuario administrador por defecto"""
    admin = db.query(Usuario).filter(Usuario.username == "admin").first()
    
    if not admin:
        print("🔐 Hasheando contraseña...")
        password = "admin123"
        print(f"   Longitud de contraseña: {len(password)} bytes")
        hashed = get_password_hash(password)
        print(f"   Hash generado: {len(hashed)} bytes")
        
        admin = Usuario(
            username="admin",
            email="admin@veterinaria.com",
            hashed_password=hashed,
            nombre_completo="Administrador del Sistema",
            rol="admin"
        )
        db.add(admin)
        print("✅ Usuario administrador creado: admin / admin123")
    else:
        print("ℹ️  Usuario administrador ya existe")


def crear_datos_ejemplo(db: Session):
    """Crea datos de ejemplo para pruebas"""
    
    # Verificar si ya existen datos
    if db.query(Cliente).count() > 0:
        print("ℹ️  Ya existen datos en la base de datos")
        return
    
    # Crear clientes de ejemplo
    clientes = [
        Cliente(
            nombre="Juan",
            apellido="Pérez",
            telefono="555-0101",
            email="juan.perez@email.com",
            direccion="Calle Principal 123",
            documento="12345678"
        ),
        Cliente(
            nombre="María",
            apellido="González",
            telefono="555-0102",
            email="maria.gonzalez@email.com",
            direccion="Avenida Central 456",
            documento="87654321"
        ),
        Cliente(
            nombre="Carlos",
            apellido="Rodríguez",
            telefono="555-0103",
            email="carlos.rodriguez@email.com",
            direccion="Boulevard Norte 789"
        )
    ]
    
    for cliente in clientes:
        db.add(cliente)
    
    db.flush()  # Obtener IDs de clientes
    
    # Crear mascotas de ejemplo
    mascotas = [
        Mascota(
            nombre="Max",
            especie="Perro",
            raza="Labrador",
            edad=3,
            sexo="Macho",
            peso=25.5,
            cliente_id=clientes[0].id
        ),
        Mascota(
            nombre="Luna",
            especie="Gato",
            raza="Siamés",
            edad=2,
            sexo="Hembra",
            peso=4.2,
            cliente_id=clientes[0].id
        ),
        Mascota(
            nombre="Rocky",
            especie="Perro",
            raza="Pastor Alemán",
            edad=5,
            sexo="Macho",
            peso=32.0,
            cliente_id=clientes[1].id
        ),
        Mascota(
            nombre="Michi",
            especie="Gato",
            raza="Persa",
            edad=1,
            sexo="Hembra",
            peso=3.8,
            cliente_id=clientes[2].id
        )
    ]
    
    for mascota in mascotas:
        db.add(mascota)
    
    # Crear productos de ejemplo
    productos = [
        # Medicamentos
        Producto(
            codigo="MED-001",
            nombre="Antibiótico Veterinario",
            descripcion="Antibiótico de amplio espectro",
            categoria="Medicamento",
            precio=25.50,
            stock=50,
            stock_minimo=10
        ),
        Producto(
            codigo="MED-002",
            nombre="Antiparasitario",
            descripcion="Tratamiento contra parásitos internos",
            categoria="Medicamento",
            precio=18.00,
            stock=40,
            stock_minimo=10
        ),
        # Alimentos
        Producto(
            codigo="ALM-001",
            nombre="Alimento Premium Perros",
            descripcion="Alimento balanceado para perros adultos 10kg",
            categoria="Alimento",
            precio=45.00,
            stock=30,
            stock_minimo=5
        ),
        Producto(
            codigo="ALM-002",
            nombre="Alimento Premium Gatos",
            descripcion="Alimento balanceado para gatos adultos 5kg",
            categoria="Alimento",
            precio=35.00,
            stock=25,
            stock_minimo=5
        ),
        # Accesorios
        Producto(
            codigo="ACC-001",
            nombre="Collar ajustable",
            descripcion="Collar de nylon ajustable para perros",
            categoria="Accesorio",
            precio=12.00,
            stock=20,
            stock_minimo=5
        ),
        Producto(
            codigo="ACC-002",
            nombre="Plato de comida",
            descripcion="Plato de acero inoxidable",
            categoria="Accesorio",
            precio=8.50,
            stock=15,
            stock_minimo=5
        ),
        # Servicios
        Producto(
            codigo="SRV-001",
            nombre="Consulta Veterinaria",
            descripcion="Consulta general con veterinario",
            categoria="Servicio",
            precio=30.00,
            stock=999,
            stock_minimo=0
        ),
        Producto(
            codigo="SRV-002",
            nombre="Vacunación",
            descripcion="Aplicación de vacuna",
            categoria="Servicio",
            precio=20.00,
            stock=999,
            stock_minimo=0
        ),
        Producto(
            codigo="SRV-003",
            nombre="Baño y peluquería",
            descripcion="Servicio completo de baño y corte",
            categoria="Servicio",
            precio=25.00,
            stock=999,
            stock_minimo=0
        )
    ]
    
    for producto in productos:
        db.add(producto)
    
    db.commit()
    
    print(f"✅ Creados {len(clientes)} clientes de ejemplo")
    print(f"✅ Creadas {len(mascotas)} mascotas de ejemplo")
    print(f"✅ Creados {len(productos)} productos de ejemplo")


def main():
    """Función principal para inicializar la base de datos"""
    print("🚀 Iniciando configuración de la base de datos...")
    
    # Inicializar tablas
    init_db()
    print("✅ Tablas creadas correctamente")
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Crear usuario administrador
        crear_usuario_admin(db)
        
        # Crear datos de ejemplo
        crear_datos_ejemplo(db)
        
        print("\n✨ Base de datos inicializada correctamente")
        print("\n📝 Credenciales de acceso:")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        
    except Exception as e:
        print(f"❌ Error al inicializar datos: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
