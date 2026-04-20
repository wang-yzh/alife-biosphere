from __future__ import annotations

import hashlib
import random


def derive_seed(base_seed: int, label: str) -> int:
    digest = hashlib.sha256(f"{base_seed}:{label}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def make_rng(base_seed: int, label: str = "root") -> random.Random:
    return random.Random(derive_seed(base_seed, label))
