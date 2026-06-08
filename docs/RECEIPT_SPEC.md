# AXZ-LVT Receipt Spec v1

Required fields:

```text
schema
receipt_id
artifact_name
claim
truth_label
scope
evidence_hashes
tests
```

Expected schema:

```text
AXZ-LVT-RECEIPT-v1
```

Evidence hash format:

```text
64 lowercase hexadecimal SHA-256 characters
```

Test status values:

```text
PASS
FAIL
SKIP
```

Result meanings:

```text
ACCEPT      receipt satisfies implemented checks
REJECT      receipt violates implemented checks
INCOMPLETE  receipt lacks minimal evidence
```
