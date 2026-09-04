# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from .audit import CostModel
from .config import Settings, get_settings
from .control import LLMControlPlane
from .engine import OblivionTextLM
from .executor import LLMExecutor
from .llm_client import OpenAICompatibleClient
from .memory import ConversationMemory
from .router import HybridObligationRouter, LexicalObligationRouter


def build_engine(settings: Settings | None = None) -> OblivionTextLM:
    current = settings or get_settings()

    executor_client = OpenAICompatibleClient(
        current.executor_base_url,
        current.executor_api_key,
        current.model_name,
        current.request_timeout_seconds,
    )
    control_client = OpenAICompatibleClient(
        current.control_base_url,
        current.control_api_key,
        current.control_model,
        current.request_timeout_seconds,
    )
    verifier_client = OpenAICompatibleClient(
        current.verify_base_url,
        current.verify_api_key,
        current.verify_model,
        current.request_timeout_seconds,
    )

    router = (
        HybridObligationRouter(current.router_top_k, current.embedding_dimensions)
        if current.router_mode.lower() == "hybrid"
        else LexicalObligationRouter(current.router_top_k)
    )
    memory = ConversationMemory(current.memory_path) if current.memory_enabled else None

    return OblivionTextLM(
        executor=LLMExecutor(executor_client),
        control=LLMControlPlane(
            control_client,
            current.verify_threshold,
            verifier_client=verifier_client,
        ),
        router=router,
        cost_model=CostModel(
            current.controller_cost_weight,
            current.active_token_cost_weight,
        ),
        max_steps=current.max_steps,
        counterfactual_enabled=current.counterfactual_enabled,
        counterfactual_tolerance=current.counterfactual_tolerance,
        trace_enabled=current.trace_enabled,
        memory=memory,
    )
