# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="OBLIVION_",
        extra="ignore",
    )

    env: str = "development"
    api_keys: str = "change-me"
    rate_limit_per_minute: int = 60

    model_name: str = "mistralai/Mistral-Small-4-119B-2603"
    executor_base_url: str = "http://127.0.0.1:8000/v1"
    executor_api_key: str = "local"

    controller_base_url: str = ""
    controller_api_key: str = ""
    controller_model: str = ""

    verifier_base_url: str = ""
    verifier_api_key: str = ""
    verifier_model: str = ""

    request_timeout_seconds: float = 120.0
    max_steps: int = 6
    router_top_k: int = 6
    router_mode: str = "hybrid"
    embedding_dimensions: int = 384

    chunk_chars: int = 1400
    chunk_overlap: int = 180
    verify_threshold: float = 0.90
    counterfactual_enabled: bool = False
    counterfactual_tolerance: float = 0.08
    controller_cost_weight: float = 0.001
    active_token_cost_weight: float = 1.0
    trace_enabled: bool = True

    memory_enabled: bool = True
    memory_path: str = "data/oblivion_memory.db"
    storage_path: str = "data/oblivion_documents.db"

    max_query_chars: int = 20_000
    max_context_chars: int = 2_000_000

    @property
    def api_key_set(self) -> set[str]:
        return {key.strip() for key in self.api_keys.split(",") if key.strip()}

    @property
    def control_base_url(self) -> str:
        return self.controller_base_url or self.executor_base_url

    @property
    def control_api_key(self) -> str:
        return self.controller_api_key or self.executor_api_key

    @property
    def control_model(self) -> str:
        return self.controller_model or self.model_name

    @property
    def verify_base_url(self) -> str:
        return self.verifier_base_url or self.control_base_url

    @property
    def verify_api_key(self) -> str:
        return self.verifier_api_key or self.control_api_key

    @property
    def verify_model(self) -> str:
        return self.verifier_model or self.control_model


@lru_cache
def get_settings() -> Settings:
    return Settings()
