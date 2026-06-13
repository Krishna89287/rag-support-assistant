import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    enable_guardrails: bool = True

    @property
    def llm_ready(self) -> bool:
        return bool(self.groq_api_key)


settings = Settings()
