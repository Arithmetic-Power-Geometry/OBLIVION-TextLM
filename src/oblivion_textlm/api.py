# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import time
import uuid
from dataclasses import asdict

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from . import __version__
from .api_models import ChatRequest, DirectQueryRequest
from .baseline import BaselineTextLM
from .chunking import chunk_text
from .config import get_settings
from .factory import build_engine
from .rag import RAGTextLM
from .safety import SafetyGuard
from .security import authenticate

REQ = Counter("oblivion_requests_total", "OBLIVION requests", ["endpoint", "status"])
LAT = Histogram("oblivion_request_seconds", "OBLIVION request latency", ["endpoint"])

app = FastAPI(
    title="OBLIVION TextLM",
    version=__version__,
    docs_url="/docs",
    redoc_url=None,
)


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    REQ.labels(request.url.path, "500").inc()
    return JSONResponse(status_code=500, content={"error": {"message": "Internal server error"}})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "oblivion-textlm", "version": __version__}


@app.get("/metrics")
async def metrics(_: str = Depends(authenticate)):
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


async def _infer(query: str, context: str, mode: str, session_id: str | None = None):
    settings = get_settings()
    guard = SafetyGuard(settings.max_query_chars, settings.max_context_chars)
    safety = guard.check(query, context)
    if not safety.allowed:
        raise HTTPException(status_code=413, detail=safety.reason)

    engine = build_engine(settings)
    chunks = chunk_text(context, settings.chunk_chars, settings.chunk_overlap)
    if not chunks:
        chunks = chunk_text(query, settings.chunk_chars, settings.chunk_overlap)

    normalized = mode.lower()
    if normalized == "baseline":
        return await BaselineTextLM(engine.executor).infer(query, chunks)
    if normalized == "rag":
        return await RAGTextLM(engine.executor, engine.router).infer(query, chunks)
    if normalized != "oblivion":
        raise HTTPException(status_code=400, detail="mode must be baseline, rag, or oblivion")
    return await engine.infer(query, chunks, session_id=session_id)


def _payload(result):
    return {
        "answer": result.answer,
        "mode": result.mode,
        "live_obligations": [asdict(item) for item in result.obligations],
        "audit": asdict(result.audit),
        "trace": [asdict(item) for item in result.trace],
        "citations": [asdict(item) for item in result.citations],
        "timings": [asdict(item) for item in result.timings],
    }


@app.post("/v1/oblivion/query")
async def direct(req: DirectQueryRequest, _: str = Depends(authenticate)):
    started = time.perf_counter()
    result = await _infer(req.query, req.context, req.mode, req.session_id)
    LAT.labels("direct").observe(time.perf_counter() - started)
    REQ.labels("direct", "200").inc()
    return _payload(result)


@app.post("/v1/chat/completions")
async def chat(req: ChatRequest, _: str = Depends(authenticate)):
    started = time.perf_counter()
    user_messages = [message.content for message in req.messages if message.role == "user"]
    query = user_messages[-1] if user_messages else ""
    context = "\n".join(
        f"{message.role.upper()}: {message.content}" for message in req.messages
    )
    result = await _infer(query, context, req.mode, req.session_id)
    elapsed = time.perf_counter() - started
    LAT.labels("chat").observe(elapsed)
    REQ.labels("chat", "200").inc()
    completion_id = f"chatcmpl-oblivion-{uuid.uuid4().hex[:16]}"
    return {
        "id": completion_id,
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": result.answer},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": result.audit.input_tokens,
            "completion_tokens": result.audit.output_tokens,
            "total_tokens": result.audit.input_tokens + result.audit.output_tokens,
        },
        "oblivion": _payload(result),
    }
