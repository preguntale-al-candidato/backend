import pathlib
from pydantic import BaseSettings


class Settings(BaseSettings):
    # default value if env variable does not exist
    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: str = "19530"
    MILVUS_USER: str = ""
    MILVUS_PASSWORD: str = ""
    MILVUS_SECURE: bool = False

    class Config:
        env_file = ".env"


# global instance
settings = Settings()


def get_milvus_connection():
    return {
        "host": settings.MILVUS_HOST,
        "port": settings.MILVUS_PORT,
        "user": settings.MILVUS_USER,
        "password": settings.MILVUS_PASSWORD,
        "secure": settings.MILVUS_SECURE,
    }


ASSETS_PATH = pathlib.Path(__file__).parent / "frontend" / "out"
