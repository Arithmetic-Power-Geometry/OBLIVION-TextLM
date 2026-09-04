# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from .types import Certificate, Verdict


def conservative_verdict(
    certificate: Certificate,
    *,
    threshold: float = 0.90,
) -> Verdict:
    if certificate.claim.lower() != "completed":
        return Verdict.UNCERTAIN
    if certificate.confidence < threshold:
        return Verdict.UNCERTAIN
    if not certificate.evidence_ids:
        return Verdict.UNCERTAIN
    return Verdict.VERIFIED
