#!/usr/bin/env python3
"""Verify that PR #1 contains the approved upstream Swarm model."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "swarm" / "js" / "scene.js"
EXPECTED_MODEL_SHA256 = (
    "6a5bbfe9dcbe2210fb803e3595978b9bd2a54695ae4d195a077bad560967e19b"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_model() -> None:
    if not MODEL.is_file():
        raise AssertionError(f"missing upstream Swarm model: {MODEL.relative_to(ROOT)}")
    actual = sha256(MODEL)
    if actual != EXPECTED_MODEL_SHA256:
        raise AssertionError(
            "Swarm model differs from approved upstream source: "
            f"expected {EXPECTED_MODEL_SHA256}, got {actual}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-only", action="store_true")
    parser.parse_args()

    try:
        verify_model()
    except AssertionError as error:
        print(f"FAIL: {error}")
        return 1

    print(f"PASS model {EXPECTED_MODEL_SHA256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
