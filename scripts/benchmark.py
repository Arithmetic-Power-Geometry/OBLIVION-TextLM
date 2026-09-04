# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
"""Compare baseline, RAG, and OBLIVION over the same HTTP endpoint."""

import argparse
import json
import os
import statistics
import time

import requests

MODES = ("baseline", "rag", "oblivion")


def norm(value):
    return " ".join(str(value or "").lower().split())


def token_f1(prediction: str, gold: str) -> float:
    p = norm(prediction).split()
    g = norm(gold).split()
    if not p and not g:
        return 1.0
    if not p or not g:
        return 0.0
    common = {}
    for token in p:
        common[token] = min(p.count(token), g.count(token))
    overlap = sum(common.values())
    precision = overlap / len(p)
    recall = overlap / len(g)
    return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--url", default=os.getenv("OBLIVION_URL", "http://127.0.0.1:8080"))
    parser.add_argument("--key", default=os.getenv("OBLIVION_API_KEY", "change-me"))
    parser.add_argument("--modes", default=",".join(MODES))
    parser.add_argument("--repeats", type=int, default=1)
    args = parser.parse_args()

    modes = [mode.strip() for mode in args.modes.split(",") if mode.strip()]
    rows = []
    with open(args.input, encoding="utf-8") as source:
        examples = [json.loads(line) for line in source if line.strip()]

    for example in examples:
        for mode in modes:
            for repeat in range(max(1, args.repeats)):
                started = time.perf_counter()
                response = requests.post(
                    args.url.rstrip("/") + "/v1/oblivion/query",
                    headers={"Authorization": f"Bearer {args.key}"},
                    json={
                        "query": example["query"],
                        "context": example["context"],
                        "mode": mode,
                    },
                    timeout=300,
                )
                response.raise_for_status()
                data = response.json()
                gold = example.get("gold_answer", "")
                row = {
                    "id": example.get("id"),
                    "repeat": repeat,
                    "mode": mode,
                    "answer": data.get("answer"),
                    "gold_answer": gold,
                    "exact_match": norm(data.get("answer")) == norm(gold),
                    "f1": token_f1(data.get("answer", ""), gold),
                    "latency_ms": round((time.perf_counter() - started) * 1000, 3),
                    "audit": data.get("audit", {}),
                    "timings": data.get("timings", []),
                    "citations": data.get("citations", []),
                }
                rows.append(row)

    with open(args.output, "w", encoding="utf-8") as target:
        for row in rows:
            target.write(json.dumps(row) + "\n")

    for mode in modes:
        selected = [row for row in rows if row["mode"] == mode]
        if selected:
            print(
                mode,
                "EM=",
                round(100 * statistics.mean(row["exact_match"] for row in selected), 2),
                "F1=",
                round(100 * statistics.mean(row["f1"] for row in selected), 2),
                "latency_ms=",
                round(statistics.mean(row["latency_ms"] for row in selected), 2),
            )


if __name__ == "__main__":
    main()
