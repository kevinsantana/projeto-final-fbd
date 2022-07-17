from typing import Any, Dict, Optional

from pydantic import BaseModel, BaseSettings, PostgresDsn, validator


class DatabaseModel(BaseModel):
    DATABASE_USER: str = "auxilio_emergencial"
    DATABASE_PASS: str = "auxilio_emergencial"
    DATABASE_HOST: str = "172.22.0.2"
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str = "auxilio_emergencial"
    DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    @validator("DATABASE_URL", pre=True)
    def make_db_url(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        return PostgresDsn.build(
            scheme="postgresql",
            user=values["DATABASE_USER"],
            password=values["DATABASE_PASS"],
            host=values["DATABASE_HOST"],
            port=values["DATABASE_PORT"],
            path=f"/{values['DATABASE_NAME']}",
        )


class Envs(BaseSettings):
    DB_URI: str = DatabaseModel().DATABASE_URL

    class Config:
        case_sensitive = True


envs = Envs()
