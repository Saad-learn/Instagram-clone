from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    SQLALCHEMY_DATABASE_URL: str
    hostname: str
    port: int
    password: str
    name: str
    username: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    cloud_name: str
    api_key: str
    api_secret: str

    class Config:
        env_file = ".env"

settings = Settings()
