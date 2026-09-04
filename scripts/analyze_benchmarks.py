# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from collections import defaultdict


def bootstrap_ci(values: list[float], samples: int = 2000, seed: int = 7):
    if not values:
        return (0.0, 0.0)
    rng = random.Random(seed)
    means = []
    for _ in range(samples):
        draw = [rng.choice(values) for _ in values]
        means.append(statistics.mean(draw))
    means.sort()
    lo = means[int(0.025 * (len(means) - 1))]
    hi = means[int(0.975 * (len(means) - 1))]
    return lo, hi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonl")
    args = parser.parse_args()

    groups = defaultdict(list)
    with open(args.jsonl, encoding="utf-8") as source:
        for line in source:
            if line.strip():
                row = json.loads(line)
                groups[row["mode"]].append(row)

    for mode, rows in groups.items():
        f1 = [100.0 * float(row["f1"]) for row in rows]
        latency = [float(row["latency_ms"]) for row in rows]
        lo, hi = bootstrap_ci(f1)
        print(
            json.dumps(
                {
                    "mode": mode,
                    "n": len(rows),
                    "exact_match_pct": 100
                    * statistics.mean(bool(row["exact_match"]) for row in rows),
                    "f1_pct": statistics.mean(f1),
                    "f1_95ci": [lo, hi],
                    "latency_mean_ms": statistics.mean(latency),
                    "latency_median_ms": statistics.median(latency),
                    "latency_stdev_ms": statistics.pstdev(latency) if len(latency) > 1 else 0.0,
                    "latency_sem_ms": (
                        statistics.pstdev(latency) / math.sqrt(len(latency))
                        if len(latency) > 1
                        else 0.0
                    ),
                }
            )
        )


if __name__ == "__main__":
    main()
