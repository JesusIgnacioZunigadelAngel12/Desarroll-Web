# Sistema de Gestión Veterinaria - Backend

API REST para gestión integral de una veterinaria, desarrollada con FastAPI y SQLite.

## 🚀 Características

- **Autenticación JWT**: Sistema seguro de login y registro
- **Gestión de Clientes**: CRUD completo de clientes
- **Gestión de Mascotas**: Control de mascotas vinculadas a clientes
- **Inventario de Productos**: Gestión de productos con control de stock
- **Punto de Venta (POS)**: Sistema de ventas con actualización automática de inventario
- **Estadísticas**: Panel de estadísticas de ventas

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. **Clonar o navegar al directorio del proyecto**

```bash
cd backend
```

2. **Crear entorno virtual (recomendado)**

```bash
python -m venv venv
```

3. **Activar entorno virtual**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

5. **Configurar variables de entorno**

Copiar `.env.example` a `.env` y configurar:

```bash
copy .env.example .env
```

Editar `.env` y cambiar `SECRET_KEY` por una clave segura.

6. **Inicializar base de datos**

```bash
python -m src.database.init_data
```

Esto creará:
- Las tablas de la base de datos
- Un usuario administrador (admin/admin123)
- Datos de ejemplo para pruebas

## ▶️ Ejecutar el servidor

```bash
python -m src.main
```

O usando uvicorn directamente:

```bash
uvicorn src.main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

## 📚 Documentación de la API

FastAPI genera documentación automática:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Autenticación

1. **Registrar un usuario** (POST `/api/auth/register`)
2. **Iniciar sesión** (POST `/api/auth/login`)
3. **Usar el token** en las peticiones siguientes:

```
Authorization: Bearer <tu_token>
```

## 📁 Estructura del Proyecto

```
backend/
├── src/
│   ├── config/          # Configuración y base de datos
│   ├── models/          # Modelos SQLAlchemy
│   ├── schemas/         # Schemas Pydantic
│   ├── controllers/     # Lógica de negocio
│   ├── routes/          # Endpoints de la API
│   ├── middleware/      # Autenticación y middleware
│   ├── database/        # Scripts de inicialización
│   └── main.py          # Aplicación principal
├── requirements.txt     # Dependencias
├── .env.example        # Ejemplo de variables de entorno
└── README.md           # Este archivo
```

## 🗄️ Base de Datos

El proyecto usa SQLite por defecto. El archivo `veterinaria.db` se crea automáticamente.

### Tablas principales:

- **usuarios**: Usuarios del sistema
- **clientes**: Clientes de la veterinaria
- **mascotas**: Mascotas de los clientes
- **productos**: Inventario de productos y servicios
- **ventas**: Registro de ventas
- **detalles_venta**: Detalles de cada venta

## 🛠️ Endpoints Principales

### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual

### Clientes
- `GET /api/clientes` - Listar clientes
- `POST /api/clientes` - Crear cliente
- `GET /api/clientes/{id}` - Obtener cliente
- `PUT /api/clientes/{id}` - Actualizar cliente
- `DELETE /api/clientes/{id}` - Eliminar cliente

### Mascotas
- `GET /api/mascotas` - Listar mascotas
- `POST /api/mascotas` - Crear mascota
- `GET /api/mascotas/{id}` - Obtener mascota
- `PUT /api/mascotas/{id}` - Actualizar mascota
- `DELETE /api/mascotas/{id}` - Eliminar mascota

### Productos
- `GET /api/productos` - Listar productos
- `POST /api/productos` - Crear producto
- `GET /api/productos/{id}` - Obtener producto
- `PUT /api/productos/{id}` - Actualizar producto
- `GET /api/productos/low-stock` - Productos con stock bajo

### Ventas
- `POST /api/ventas` - Crear venta
- `GET /api/ventas` - Listar ventas
- `GET /api/ventas/{id}` - Obtener venta
- `GET /api/ventas/estadisticas` - Estadísticas de ventas
- `PATCH /api/ventas/{id}/cancelar` - Cancelar venta

## 🔒 Seguridad

- Contraseñas hasheadas con bcrypt
- Autenticación con JWT
- Validación de datos con Pydantic
- Protección de rutas con middleware

## 📝 Usuario por defecto

```
Usuario: admin
Contraseña: admin123
```

**⚠️ IMPORTANTE**: Cambiar estas credenciales en producción.

## 🧪 Testing

```bash
pytest
```

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
