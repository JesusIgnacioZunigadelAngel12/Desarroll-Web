# 🚀 Inicio Rápido - Sistema de Veterinaria

## ✅ Sistema Instalado y Funcionando

El sistema ya está completamente instalado y configurado. Los servidores están ejecutándose:

- **Frontend (Astro)**: http://localhost:4321
- **Backend (FastAPI)**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 🔐 Credenciales de Acceso

```
Usuario: admin
Contraseña: admin123
```

## 📋 Datos de Ejemplo

El sistema ya tiene datos de prueba cargados:

- ✅ 3 clientes de ejemplo
- ✅ 4 mascotas asociadas
- ✅ 9 productos en 4 categorías
- ✅ Usuario administrador

## 🎯 Acceso al Sistema

1. Abre el navegador en: http://localhost:4321
2. Inicia sesión con las credenciales de administrador
3. Explora las siguientes secciones:

### Dashboard 📊
- Vista general con estadísticas
- Clientes, mascotas y productos registrados
- Alertas de stock bajo
- Accesos rápidos

### Clientes 👥
- Lista de clientes
- Búsqueda por nombre, apellido o documento
- Crear, editar y eliminar clientes
- Ver mascotas asociadas

### Mascotas 🐾
- Gestión de mascotas
- Asociar mascotas a clientes
- Filtrar por especie
- Información detallada (raza, edad, peso, etc.)

### Productos 📦
- Inventario completo
- Filtrar por categoría
- Alertas de reposición automáticas
- Control de stock

### Punto de Venta 🛒
- Sistema POS completo
- Seleccionar cliente
- Agregar productos al carrito
- Aplicar descuentos
- Múltiples métodos de pago
- Actualización automática de inventario

### Historial de Ventas 📋
- Ver todas las ventas realizadas
- Detalles de cada venta
- Filtros y búsqueda

## 🛑 Detener los Servidores

Para detener los servidores, presiona `Ctrl + C` en cada terminal.

## 🔄 Reiniciar el Sistema

### Opción 1: Scripts Individuales

**Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m src.main
```

**Frontend:**
```powershell
cd frontend
npm run dev
```

### Opción 2: Script Combinado (Recomendado)

```powershell
.\start-all.ps1
```

Este script inicia ambos servidores automáticamente.

## 📚 Documentación API

Visita http://localhost:8000/docs para:

- Ver todos los endpoints disponibles
- Probar las APIs interactivamente
- Ver esquemas de datos
- Obtener ejemplos de request/response

## 🔧 Configuración Adicional

### Variables de Entorno

**Backend** (`backend/.env`):
```env
SECRET_KEY=tu_clave_secreta_super_segura_aqui
DATABASE_URL=sqlite:///./veterinaria.db
DEBUG=True
```

**Frontend** (`frontend/.env`):
```env
PUBLIC_API_URL=http://localhost:8000
```

## 📁 Base de Datos

La base de datos SQLite se encuentra en:
```
backend/veterinaria.db
```

### Reinicializar Base de Datos

Si necesitas reiniciar la base de datos con datos frescos:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m src.database.init_data
```

**⚠️ ADVERTENCIA**: Esto eliminará todos los datos existentes.

## 🎨 Características Principales

✅ **Autenticación JWT**: Sistema de login seguro  
✅ **CRUD Completo**: Clientes, mascotas y productos  
✅ **Sistema POS**: Ventas con control de inventario  
✅ **Diseño Responsivo**: Funciona en desktop y móvil  
✅ **Validaciones**: Formularios con validación en tiempo real  
✅ **Stock Automático**: Alertas y actualización automática  
✅ **Búsqueda y Filtros**: En todas las secciones  

## 🐛 Solución de Problemas

### El backend no inicia
```powershell
# Verificar que el venv está activado
cd backend
.\venv\Scripts\Activate.ps1

# Verificar dependencias
pip list

# Reinstalar si es necesario
pip install -r requirements.txt
```

### El frontend no inicia
```powershell
# Verificar node_modules
cd frontend
npm install

# Limpiar cache si es necesario
Remove-Item -Path node_modules -Recurse -Force
npm install
```

### Error de CORS
Asegúrate de que el backend permite el origen del frontend en `backend/src/config/settings.py`:
```python
CORS_ORIGINS = "http://localhost:4321,http://127.0.0.1:4321"
```

## 📞 Próximos Pasos

1. **Explorar la API**: Visita http://localhost:8000/docs
2. **Crear una venta**: Usa el módulo POS para registrar una venta
3. **Personalizar**: Modifica estilos en `frontend/src/pages/*.astro`
4. **Agregar funcionalidades**: Extiende los controladores en `backend/src/controllers/`

## 🎉 ¡Todo Listo!

El sistema está completamente funcional y listo para usar. Disfruta explorando todas las características.
