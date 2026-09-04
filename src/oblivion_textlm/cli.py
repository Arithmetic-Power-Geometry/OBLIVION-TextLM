# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import argparse
import asyncio
import json
from dataclasses import asdict

from .audit import CostModel
from .baseline import BaselineTextLM
from .chunking import chunk_text
from .control import DeterministicDemoControl
from .engine import OblivionTextLM
from .executor import DeterministicDemoExecutor
from .rag import RAGTextLM
from .router import HybridObligationRouter


async def _demo(mode: str):
    query = "What colour is Rahul's bicycle?"
    context = "Rahul borrowed Maya's bicycle. Maya's bicycle was painted red."
    chunks = chunk_text(context)
    executor = DeterministicDemoExecutor()
    router = HybridObligationRouter(3)
    if mode == "baseline":
        result = await BaselineTextLM(executor).infer(query, chunks)
    elif mode == "rag":
        result = await RAGTextLM(executor, router).infer(query, chunks)
    else:
        engine = OblivionTextLM(
            executor,
            DeterministicDemoControl(),
            router,
            CostModel(controller_weight=0.0),
            max_steps=2,
        )
        result = await engine.infer(query, chunks)
    print(json.dumps(asdict(result), indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(prog="oblivion-textlm")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo")
    demo.add_argument("--mode", choices=["baseline", "rag", "oblivion"], default="oblivion")
    args = parser.parse_args()
    if args.command == "demo":
        asyncio.run(_demo(args.mode))


if __name__ == "__main__":
    main()
