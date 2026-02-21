/**
 * Cliente API para comunicarse con el backend FastAPI
 */

const API_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

// Obtener token del localStorage
function getToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
}

// Headers con autenticación
function getHeaders(): HeadersInit {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  const token = getToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  return headers;
}

// Función helper para peticiones
async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;
  const config: RequestInit = {
    ...options,
    headers: {
      ...getHeaders(),
      ...options.headers,
    },
  };

  const response = await fetch(url, config);

  if (!response.ok) {
    if (response.status === 401) {
      // Token inválido o expirado
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    
    const error = await response.json().catch(() => ({ detail: 'Error desconocido' }));
    throw new Error(error.detail || `Error: ${response.status}`);
  }

  return response.json();
}

// === AUTENTICACIÓN ===

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  nombre_completo: string;
  rol?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export const authAPI = {
  login: (data: LoginData) =>
    fetchAPI<TokenResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  register: (data: RegisterData) =>
    fetchAPI('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getCurrentUser: () => fetchAPI('/api/auth/me'),
};

// === CLIENTES ===

export interface Cliente {
  id?: number;
  nombre: string;
  apellido: string;
  telefono: string;
  email?: string;
  direccion?: string;
  documento?: string;
  notas?: string;
}

export const clientesAPI = {
  getAll: (search?: string) => {
    const params = search ? `?search=${encodeURIComponent(search)}` : '';
    return fetchAPI<Cliente[]>(`/api/clientes${params}`);
  },

  getById: (id: number) => fetchAPI<Cliente>(`/api/clientes/${id}`),

  create: (data: Cliente) =>
    fetchAPI<Cliente>('/api/clientes', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, data: Partial<Cliente>) =>
    fetchAPI<Cliente>(`/api/clientes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  delete: (id: number) =>
    fetchAPI(`/api/clientes/${id}`, {
      method: 'DELETE',
    }),
};

// === MASCOTAS ===

export interface Mascota {
  id?: number;
  nombre: string;
  especie: string;
  raza?: string;
  edad?: number;
  sexo?: string;
  peso?: number;
  cliente_id: number;
  observaciones?: string;
}

export const mascotasAPI = {
  getAll: (cliente_id?: number) => {
    const params = cliente_id ? `?cliente_id=${cliente_id}` : '';
    return fetchAPI<Mascota[]>(`/api/mascotas${params}`);
  },

  getById: (id: number) => fetchAPI<Mascota>(`/api/mascotas/${id}`),

  create: (data: Mascota) =>
    fetchAPI<Mascota>('/api/mascotas', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, data: Partial<Mascota>) =>
    fetchAPI<Mascota>(`/api/mascotas/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  delete: (id: number) =>
    fetchAPI(`/api/mascotas/${id}`, {
      method: 'DELETE',
    }),
};

// === PRODUCTOS ===

export interface Producto {
  id?: number;
  codigo: string;
  nombre: string;
  descripcion?: string;
  categoria: string;
  precio: number;
  stock: number;
  stock_minimo?: number;
  activo?: boolean;
}

export const productosAPI = {
  getAll: (categoria?: string, search?: string) => {
    const params = new URLSearchParams();
    if (categoria) params.append('categoria', categoria);
    if (search) params.append('search', search);
    const queryString = params.toString();
    return fetchAPI<Producto[]>(`/api/productos${queryString ? '?' + queryString : ''}`);
  },

  getById: (id: number) => fetchAPI<Producto>(`/api/productos/${id}`),

  create: (data: Producto) =>
    fetchAPI<Producto>('/api/productos', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, data: Partial<Producto>) =>
    fetchAPI<Producto>(`/api/productos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  delete: (id: number) =>
    fetchAPI(`/api/productos/${id}`, {
      method: 'DELETE',
    }),
};

// === VENTAS ===

export interface DetalleVenta {
  producto_id: number;
  cantidad: number;
  precio_unitario: number;
}

export interface Venta {
  id?: number;
  codigo_venta?: string;
  cliente_id?: number;
  metodo_pago: string;
  descuento?: number;
  notas?: string;
  detalles: DetalleVenta[];
  total?: number;
}

export const ventasAPI = {
  getAll: () => fetchAPI<Venta[]>('/api/ventas'),

  getById: (id: number) => fetchAPI<Venta>(`/api/ventas/${id}`),

  create: (data: Venta) =>
    fetchAPI<Venta>('/api/ventas', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getEstadisticas: () => fetchAPI('/api/ventas/estadisticas'),
};
