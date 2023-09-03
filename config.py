import pathlib
from pydantic import BaseSettings


class Settings(BaseSettings):
    # default value if env variable does not exist
    MILVIUS_HOST: str
    MILVIUS_PORT: str = "19530"
    MILVIUS_USER: str = ""
    MILVIUS_PASSWORD: str = ""
    MILVIUS_SECURE: bool = False

    class Config:
        env_file = ".env"

    # model_config = SettingsConfigDict(env_file=".env")


# global instance
settings = Settings()


def get_milvius_connection():
    return {
        "host": settings.MILVIUS_HOST,
        "port": settings.MILVIUS_PORT,
        "user": settings.MILVIUS_USER,
        "password": settings.MILVIUS_PASSWORD,
        "secure": settings.MILVIUS_SECURE,
    }


ASSETS_PATH = pathlib.Path(__file__).parent / "frontend" / "out"
