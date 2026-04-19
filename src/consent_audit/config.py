"""Runtime configuration loaded from environment variables."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # LLM / VLM
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    anthropic_vlm_model: str = Field(default="claude-opus-4-7", alias="ANTHROPIC_VLM_MODEL")
    anthropic_llm_fast_model: str = Field(
        default="claude-haiku-4-5-20251001", alias="ANTHROPIC_LLM_FAST_MODEL"
    )
    anthropic_llm_deep_model: str = Field(
        default="claude-opus-4-7", alias="ANTHROPIC_LLM_DEEP_MODEL"
    )
    openai_vlm_model: str = Field(default="gpt-4o", alias="OPENAI_VLM_MODEL")

    # Storage
    database_url: str = Field(default="", alias="DATABASE_URL")
    s3_endpoint_url: str = Field(default="", alias="S3_ENDPOINT_URL")
    s3_bucket: str = Field(default="", alias="S3_BUCKET")
    s3_access_key_id: str = Field(default="", alias="S3_ACCESS_KEY_ID")
    s3_secret_access_key: str = Field(default="", alias="S3_SECRET_ACCESS_KEY")

    # Runtime
    ssrp_budget_cap: float = Field(default=50.0, alias="SSRP_BUDGET_CAP")
    agent_site_timeout: int = Field(default=180, alias="AGENT_SITE_TIMEOUT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")


settings = Settings()
