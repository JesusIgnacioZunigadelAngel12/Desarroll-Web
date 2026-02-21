"""
Configuración de la aplicación
Maneja todas las variables de entorno y configuraciones globales
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Clase de configuración que carga variables desde .env
    """
    # Configuración del servidor
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    PROJECT_NAME: str = "Sistema Veterinaria API"
    VERSION: str = "1.0.0"
    
    # Base de datos
    DATABASE_URL: str = "sqlite:///./veterinaria.db"
    
    # Seguridad JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:4321"
    
    @property
    def origins_list(self) -> List[str]:
        """Convierte la cadena de orígenes permitidos en una lista"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()
