#!/usr/bin/env python3
"""Axezent AI Library of Verified Things — finite receipt verifier.

Truth boundary:
ACCEPT means the submitted receipt obeyed the deterministic checks implemented
here. It does not prove global AI truthfulness, full AI alignment, a mathematical
Millennium Prize result, or correctness outside the receipt's declared scope.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EXPECTED_SCHEMA = "AXZ-LVT-RECEIPT-v1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class VerificationReport:
    result: str
    truth_label: str
    errors: list[str]
    warnings: list[str]
    receipt_sha256: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "engine": "Axezent AI Library of Verified Things",
            "result": self.result,
            "truth_label": self.truth_label,
            "errors": self.errors,
            "warnings": self.warnings,
            "receipt_sha256": self.receipt_sha256,
            "truth_boundary": (
                "finite deterministic receipt check only; no global proof, "
                "alignment, prize, investment, or guaranteed-support claim"
            ),
        }


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_json(obj: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(obj)).hexdigest()


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def verify_receipt(receipt: dict[str, Any]) -> VerificationReport:
    errors: list[str] = []
    warnings: list[str] = []
    receipt_hash = sha256_json(receipt)

    if receipt.get("schema") != EXPECTED_SCHEMA:
        errors.append(f"schema must be {EXPECTED_SCHEMA}")

    for required in ("receipt_id", "artifact_name", "claim", "truth_label", "scope"):
        if not receipt.get(required):
            errors.append(f"{required} is required")

    truth_label = str(receipt.get("truth_label", "MISSING_TRUTH_LABEL"))

    evidence_hashes = receipt.get("evidence_hashes")
    if not isinstance(evidence_hashes, list) or not evidence_hashes:
        errors.append("evidence_hashes must be a non-empty list")
    else:
        for i, item in enumerate(evidence_hashes):
            if not isinstance(item, dict):
                errors.append(f"evidence_hashes[{i}] must be an object")
                continue
            digest = item.get("sha256")
            if not isinstance(digest, str) or not SHA256_RE.match(digest):
                errors.append(f"evidence_hashes[{i}].sha256 must be 64 lowercase hex characters")

    tests = receipt.get("tests")
    if not isinstance(tests, list) or not tests:
        errors.append("tests must be a non-empty list")
    else:
        for i, test in enumerate(tests):
            if not isinstance(test, dict):
                errors.append(f"tests[{i}] must be an object")
                continue
            name = test.get("name")
            status = test.get("status")
            if not name:
                errors.append(f"tests[{i}].name is required")
            if status not in {"PASS", "FAIL", "SKIP"}:
                errors.append(f"tests[{i}].status must be PASS, FAIL, or SKIP")
            elif status == "FAIL":
                errors.append(f"test failed: {name}")

    scope = str(receipt.get("scope", "")).lower()
    if "global" in str(receipt.get("claim", "")).lower() and "no global" not in scope:
        warnings.append("claim mentions global scope; keep public claim receipt-bounded")

    result = "ACCEPT" if not errors else "REJECT"
    if any("required" in err or "non-empty" in err for err in errors):
        result = "INCOMPLETE" if len(errors) <= 2 else "REJECT"

    return VerificationReport(
        result=result,
        truth_label=truth_label,
        errors=errors,
        warnings=warnings,
        receipt_sha256=receipt_hash,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify an AXZ-LVT receipt.")
    parser.add_argument("receipt", help="Path to receipt JSON")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON report")
    args = parser.parse_args(argv)

    try:
        receipt = load_json(args.receipt)
        if not isinstance(receipt, dict):
            raise ValueError("receipt JSON must be an object")
        report = verify_receipt(receipt)
        print(json.dumps(report.to_dict(), indent=2 if args.pretty else None))
        return 0 if report.result == "ACCEPT" else 1
    except Exception as exc:
        print(json.dumps({
            "engine": "Axezent AI Library of Verified Things",
            "result": "ERROR",
            "errors": [str(exc)],
        }, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
