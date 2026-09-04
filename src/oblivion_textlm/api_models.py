# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str = "oblivion-textlm-v2"
    messages: list[ChatMessage]
    temperature: float = 0.0
    max_tokens: int = 900
    mode: str = "oblivion"
    session_id: str | None = None
    metadata: dict = Field(default_factory=dict)


class DirectQueryRequest(BaseModel):
    query: str
    context: str
    mode: str = "oblivion"
    session_id: str | None = None
