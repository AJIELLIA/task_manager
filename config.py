"""
config.py
Определяет настройки приложения с использованием Pydantic.
Настройки включают секретные ключи, конфигурацию базы данных и Redis.
Загружает переменные окружения из файла .env.
"""
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс для определения и хранения конфигурационных настроек приложения.
    """

    secret_key: str = os.getenv("SECRET_KEY", "your_secret_key")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    db_name: str = os.getenv("DB_NAME", "postgres")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "password")
    db_host: str = os.getenv("DB_HOST", "db")
    db_port: int = os.getenv("DB_PORT", 5432)

    @property
    def database_url(self) -> str:
        """
        Создает строку подключения к базе данных.
        Returns:
            str: Полная строка подключения к базе данных.
        """
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        """Конфигурация Pydantic для загрузки переменных окружения из файла."""
        env_file = ".env"


settings = Settings()
