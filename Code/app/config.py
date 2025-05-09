from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    DATABASE_URL: str
    PROXMOX_USER: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int
    CONCURRENT_LIMIT: int

    LDAP_BASE_REALM: str
    LDAP_PRIVILEGED_REALM: str

    PROXMOX_PASSWORD: str
    PROXMOX_HOST: str
    LDAP_SERVER: str
    LDAP_BASE_DN: str
    LDAP_PRIVILEGED_DN: str

    DEBUG: bool = False  # Default value

    class Config:
         env_file = str(Path(__file__).parent / ".env")

settings = Settings()