from pydantic import BaseSettings

class VectorDBConfig(BaseSettings):
    vector_db_path: str = "./vector_db"

    class Config:
        env_file = ".env"
