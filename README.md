# Axezent AI — Library of Verified Things

A ready-to-run company / product launch kit for a public-facing verification business.

**Positioning:**  
Axezent AI helps developers, researchers, and companies turn AI, software, math, and research claims into finite, replayable, receipt-backed artifacts.

**Core rule:**  
No claim without a receipt.

## Launch Status

Axezent AI — Library of Verified Things v0.1.0 is finished and live.

Completed:
- public GitHub repository created;
- all launch files uploaded;
- README, license, docs, examples, tests, and site files added;
- GitHub Actions workflow added;
- GitHub Pages deployed;
- first release published;
- live website verified;
- browser receipt verifier working;
- ACCEPT demo working;
- SHA-256 receipt output working;
- Library registry showing;
- pricing section showing;
- Cash App support showing;
- contact email showing;
- truth-boundary language included.

Final public status:

```text
AXEZENT_LIBRARY_OF_VERIFIED_THINGS__V0_1_PUBLIC_LAUNCH_COMPLETE
```

Truth label:

```text
PUBLIC_BUSINESS_LAYER__FINITE_RECEIPT_VERIFICATION__NO_GLOBAL_PROOF_CLAIM
```

## What is included

```text
site/                  Static public website
site/index.html        Landing page + local browser verifier
site/app.js            Browser receipt checker
site/styles.css        Responsive visual design
data/library.json      Seed registry for verified things
examples/              Passing and failing receipt examples
verify.py              No-dependency CLI verifier
api_server.py          No-dependency local API + website server
docs/                  Business, truth-boundary, onboarding, donation docs
.github/workflows/     GitHub Pages deployment workflow
```

## Run locally

```bash
python api_server.py
```

Open:

```text
http://127.0.0.1:8000
```

Verify the passing demo from the command line:

```bash
python verify.py examples/passing_receipt.json --pretty
```

Expected result:

```text
ACCEPT
```

Verify the failing demo:

```bash
python verify.py examples/failing_receipt.json --pretty
```

Expected result:

```text
REJECT
```

Test API endpoint:

```bash
curl -fsS -H "Content-Type: application/json" \
  --data-binary @examples/passing_receipt.json \
  http://127.0.0.1:8000/verify
```

## Public Truth Boundary

ACCEPT means the submitted receipt obeyed the deterministic checks implemented here. It does **not** prove:

- global AI truthfulness;
- full AI alignment;
- hidden model reasoning;
- all future outputs are safe;
- a full mathematical Millennium Prize result;
- guaranteed customer support;
- equity, tokens, investment rights, or ownership.

## Cash App

Optional donations support open-source development and maintenance:

```text
$Axezent
```

Donations are voluntary support. They do not create equity, tokens, investment rights, ownership rights, or guaranteed support obligations.

## Contact

```text
axezentai@Gmail.com
```
