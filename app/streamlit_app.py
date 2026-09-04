# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import asdict
from io import BytesIO
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from oblivion_textlm import __version__
from oblivion_textlm.audit import CostModel
from oblivion_textlm.baseline import BaselineTextLM
from oblivion_textlm.chunking import chunk_text
from oblivion_textlm.control import DeterministicDemoControl
from oblivion_textlm.engine import OblivionTextLM
from oblivion_textlm.executor import DeterministicDemoExecutor
from oblivion_textlm.rag import RAGTextLM
from oblivion_textlm.router import HybridObligationRouter

st.set_page_config(page_title="OBLIVION TextLM", page_icon="◐", layout="wide")

st.markdown(
    """
    <style>
    .stApp {background: radial-gradient(circle at 15% 0%, #172033 0, #090c12 40%);}
    .block-container {max-width: 1500px;}
    .obl {letter-spacing:.16em;font-size:2.15rem;font-weight:800;}
    .sub {color:#9ba8bd;margin-top:-.5rem;}
    .chip {display:inline-block;border:1px solid rgba(255,255,255,.12);
    border-radius:999px;padding:.22rem .55rem;margin:.15rem .2rem .15rem 0;font-size:.78rem;}
    div[data-testid="stMetric"] {border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:.6rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


def extract_text(uploaded) -> str:
    if uploaded is None:
        return ""
    name = uploaded.name.lower()
    data = uploaded.getvalue()
    if name.endswith((".txt", ".md", ".csv", ".json", ".log")):
        return data.decode("utf-8", errors="replace")
    if name.endswith(".pdf"):
        from pypdf import PdfReader

        reader = PdfReader(BytesIO(data))
        return "\n\n".join((page.extract_text() or "") for page in reader.pages)
    if name.endswith(".docx"):
        from docx import Document

        doc = Document(BytesIO(data))
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    raise ValueError("Unsupported file type")


def demo_components():
    executor = DeterministicDemoExecutor()
    router = HybridObligationRouter(6)
    oblivion = OblivionTextLM(
        executor,
        DeterministicDemoControl(),
        router,
        CostModel(controller_weight=0.0),
        max_steps=2,
    )
    return executor, router, oblivion


st.markdown('<div class="obl">OBLIVION TextLM</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub">Query-relative TextLM · baseline / RAG / OBLIVION comparison console</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<span class="chip">HYBRID RETRIEVAL</span>'
    '<span class="chip">SEMANTIC OBLIGATIONS</span>'
    '<span class="chip">VERIFIED RETIREMENT</span>'
    '<span class="chip">TRACE + AUDIT</span>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Runtime")
    mode = st.selectbox("Mode", ["OBLIVION", "RAG", "BASELINE"])
    st.warning(
        "This public no-key console uses the deterministic smoke-test executor. "
        "For real model comparison, connect the repository to a separately licensed "
        "OpenAI-compatible pretrained LLM endpoint such as Mistral Small 4."
    )
    show_trace = st.toggle("Show OBLIVION trace", True)
    show_raw = st.toggle("Show raw result", False)
    st.caption(f"v{__version__}")
    st.caption("© 2026 Mohammad Amir Khusru Akhtar. All rights reserved.")

left, right = st.columns([1.2, 0.8], gap="large")
with left:
    uploaded = st.file_uploader(
        "Optional document",
        type=["txt", "md", "csv", "json", "log", "pdf", "docx"],
    )
    context_box = st.text_area("Context", height=230)
    question = st.text_area("Question", height=90)
    run = st.button("Run", type="primary", use_container_width=True)

    if run:
        context = "\n\n".join(
            item for item in [context_box.strip(), extract_text(uploaded).strip()] if item
        )
        if not context or not question.strip():
            st.error("Provide context/document and a question.")
        else:
            chunks = chunk_text(context)
            executor, router, oblivion = demo_components()
            if mode == "BASELINE":
                result = asyncio.run(BaselineTextLM(executor).infer(question, chunks))
            elif mode == "RAG":
                result = asyncio.run(RAGTextLM(executor, router).infer(question, chunks))
            else:
                result = asyncio.run(oblivion.infer(question, chunks))
            st.session_state["result"] = asdict(result)

    result = st.session_state.get("result")
    if result:
        st.markdown("### Answer")
        st.write(result["answer"])
        if result.get("citations"):
            st.markdown("#### Sources")
            for citation in result["citations"][:8]:
                page = f" · page {citation['page']}" if citation.get("page") else ""
                st.caption(
                    f"[{citation['chunk_id']}] {citation['source']}{page}: "
                    f"{citation['quote']}"
                )

with right:
    result = st.session_state.get("result")
    st.markdown("### Run state")
    if result:
        audit = result.get("audit", {})
        c1, c2, c3 = st.columns(3)
        c1.metric("Mode", result.get("mode", ""))
        c2.metric("Input tokens", audit.get("input_tokens", 0))
        c3.metric("Total ms", f"{audit.get('total_ms', 0):.1f}")
        if show_trace and result.get("trace"):
            st.markdown("#### Birth · verify · discharge")
            for step in result["trace"]:
                with st.expander(f"Step {step['step'] + 1}"):
                    st.json(step)
        if result.get("timings"):
            st.markdown("#### Stage timing")
            st.dataframe(result["timings"], use_container_width=True, hide_index=True)
        if show_raw:
            st.code(json.dumps(result, indent=2), language="json")
    else:
        st.info("Run a query to inspect answer, citations, timing, and OBLIVION state.")
