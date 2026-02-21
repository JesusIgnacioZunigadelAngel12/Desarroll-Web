# Sistema de Gestión Veterinaria

Sistema web completo para la gestión integral de una veterinaria, desarrollado con **FastAPI** (backend) y **Astro** (frontend).

## 🎯 Características Principales

### Backend (FastAPI + SQLite)
- ✅ **Autenticación JWT**: Sistema seguro de login y registro
- ✅ **Gestión de Clientes**: CRUD completo con búsqueda
- ✅ **Gestión de Mascotas**: Registro completo vinculado a clientes
- ✅ **Inventario de Productos**: Control de stock con alertas
- ✅ **Punto de Venta (POS)**: Sistema de ventas con actualización automática de inventario
- ✅ **Estadísticas**: Dashboard con métricas en tiempo real
- ✅ **API REST**: Documentación automática con Swagger

### Frontend (Astro + Tailwind CSS)
- ✅ **Diseño Moderno**: Interfaz limpia y profesional estilo médico
- ✅ **Responsivo**: Adaptado a todos los dispositivos
- ✅ **Dashboard Interactivo**: Visualización de datos clave
- ✅ **Gestión de Ventas**: Sistema POS intuitivo y rápido
- ✅ **Búsqueda en Tiempo Real**: Filtros dinámicos
- ✅ **Modales y Formularios**: Experiencia de usuario optimizada

## 🗄️ Base de Datos

El sistema utiliza SQLite con el siguiente esquema:

- **usuarios**: Autenticación y control de acceso
- **clientes**: Información de clientes
- **mascotas**: Mascotas vinculadas a clientes
- **productos**: Inventario de productos y servicios
- **ventas**: Registro de ventas
- **detalles_venta**: Items de cada venta

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- Node.js 16 o superior
- npm o yarn

### 1. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
copy .env.example .env

# Inicializar base de datos con datos de ejemplo
python -m src.database.init_data

# Ejecutar servidor
python -m src.main
```

El backend estará disponible en: `http://localhost:8000`

### 2. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Crear archivo de configuración
echo PUBLIC_API_URL=http://localhost:8000 > .env

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: `http://localhost:4321`

## 🔐 Credenciales por Defecto

```
Usuario: admin
Contraseña: admin123
```

**⚠️ IMPORTANTE**: Cambiar estas credenciales en producción.

## 📱 Uso del Sistema

### 1. Inicio de Sesión
Accede a `http://localhost:4321/login` y usa las credenciales por defecto.

### 2. Dashboard
Visualiza estadísticas generales, productos con stock bajo y acciones rápidas.

### 3. Gestión de Clientes
- Crear, editar y eliminar clientes
- Buscar clientes por nombre, email o teléfono
- Ver mascotas asociadas a cada cliente

### 4. Gestión de Productos
- Administrar inventario
- Categorizar productos (Medicamento, Alimento, Accesorio, Servicio)
- Alertas de stock bajo
- Control de precios y stock

### 5. Punto de Venta (POS)
- Seleccionar productos mediante búsqueda o catálogo
- Agregar al carrito con control de cantidades
- Seleccionar cliente (opcional)
- Aplicar descuentos
- Elegir método de pago
- Finalizar venta con actualización automática de inventario

### 6. Historial de Ventas
- Ver todas las ventas realizadas
- Filtrar por fecha y cliente
- Ver detalles de cada venta
- Estadísticas de ventas

## 📂 Estructura del Proyecto

```
sistema-veterinaria/
├── backend/                  # API FastAPI
│   ├── src/
│   │   ├── config/          # Configuración y DB
│   │   ├── models/          # Modelos SQLAlchemy
│   │   ├── schemas/         # Schemas Pydantic
│   │   ├── controllers/     # Lógica de negocio
│   │   ├── routes/          # Endpoints API
│   │   ├── middleware/      # Autenticación JWT
│   │   ├── database/        # Scripts DB
│   │   └── main.py          # Aplicación principal
│   ├── requirements.txt     # Dependencias Python
│   └── README.md
│
└── frontend/                 # Aplicación Astro
    ├── src/
    │   ├── layouts/         # Layouts reutilizables
    │   ├── pages/           # Páginas de la app
    │   ├── components/      # Componentes UI
    │   ├── services/        # Cliente API
    │   └── styles/          # Estilos globales
    ├── package.json
    └── README.md
```

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **Pydantic**: Validación de datos
- **JWT**: Autenticación segura
- **SQLite**: Base de datos ligera
- **Uvicorn**: Servidor ASGI

### Frontend
- **Astro**: Framework web moderno
- **Tailwind CSS**: Estilos utility-first
- **TypeScript**: Tipado estático
- **Fetch API**: Comunicación con backend

## 📖 API Documentation

La documentación interactiva de la API está disponible en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔒 Seguridad

- Contraseñas hasheadas con bcrypt
- Autenticación mediante JWT
- Validación de datos en backend
- Protección de rutas sensibles
- Control de acceso por roles
- CORS configurado

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

## 📦 Build para Producción

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m src.main
```

### Frontend
```bash
cd frontend
npm run build
npm run preview
```

## 🚀 Deployment

### Backend (Render, Railway, Heroku)
1. Configurar variables de entorno
2. Cambiar SECRET_KEY
3. Configurar base de datos PostgreSQL (opcional)
4. Deploy desde repositorio Git

### Frontend (Vercel, Netlify, Cloudflare Pages)
1. Conectar repositorio
2. Configurar variable PUBLIC_API_URL
3. Build command: `npm run build`
4. Output directory: `dist`

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📝 Notas Adicionales

### Migrar a PostgreSQL (Producción)

Si necesitas migrar a PostgreSQL:

1. Actualizar `DATABASE_URL` en `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/veterinaria
```

2. Instalar driver de PostgreSQL:
```bash
pip install psycopg2-binary
```

3. Ejecutar inicialización:
```bash
python -m src.database.init_data
```

### Personalización

El sistema puede personalizarse fácilmente:

- **Colores**: Modificar `tailwind.config.js`
- **Logo**: Reemplazar emoji en layouts
- **Categorías**: Agregar en modelos y schemas
- **Campos**: Extender modelos según necesidades
- **Reportes**: Agregar endpoints de estadísticas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

Desarrollado como proyecto de demostración de Full Stack con FastAPI y Astro.

---

**💡 Tip**: Para mejores prácticas en producción, considera:
- Usar PostgreSQL en lugar de SQLite
- Implementar rate limiting
- Añadir logs estructurados
- Configurar backups automáticos
- Implementar tests automatizados
- Usar CI/CD para deployments

¿Necesitas ayuda? Revisa la documentación de la API en `/docs` o los ejemplos en el código.
