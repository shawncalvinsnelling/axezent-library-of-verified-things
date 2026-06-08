import json
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify", ROOT / "verify.py")
verify = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(verify)

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def test_passing_accepts():
    report = verify.verify_receipt(load("examples/passing_receipt.json"))
    assert report.result == "ACCEPT"
    assert report.errors == []

def test_failing_rejects():
    report = verify.verify_receipt(load("examples/failing_receipt.json"))
    assert report.result == "REJECT"
    assert report.errors
