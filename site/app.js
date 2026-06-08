const passDemo = {
  schema: "AXZ-LVT-RECEIPT-v1",
  receipt_id: "AXZ-LVT-DEMO-0001",
  artifact_name: "Axezent AI CTR Passing Demo",
  artifact_type: "software_receipt",
  truth_label: "FINITE_RECEIPT_VERIFIED",
  claim: "The submitted artifact passed the declared finite checks in this demo receipt.",
  scope: "Local deterministic receipt verification only. No global AI truthfulness claim.",
  evidence_hashes: [
    { name: "demo_payload", sha256: "d84e5319e23819616cbeb9f0cadbf4b0c2bb6fb77d0e560390bf7524bdac3387" }
  ],
  tests: [
    { name: "schema_present", status: "PASS" },
    { name: "hash_format", status: "PASS" },
    { name: "claim_boundary_present", status: "PASS" }
  ],
  cash_app: "$Axezent",
  contact: "axezentai@Gmail.com"
};

const failDemo = {
  ...passDemo,
  receipt_id: "AXZ-LVT-DEMO-0002",
  artifact_name: "Axezent AI CTR Failing Demo",
  claim: "This receipt intentionally contains a failed test to show rejection behavior.",
  evidence_hashes: [{ name: "bad_payload", sha256: "not-a-valid-sha256" }],
  tests: [
    { name: "schema_present", status: "PASS" },
    { name: "hash_format", status: "FAIL" }
  ]
};

const receiptInput = document.querySelector("#receiptInput");
const resultOutput = document.querySelector("#resultOutput");
const libraryEntries = document.querySelector("#libraryEntries");
const searchInput = document.querySelector("#searchInput");
let entries = [];

function canonicalize(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return "[" + value.map(canonicalize).join(",") + "]";
  return "{" + Object.keys(value).sort().map(k => JSON.stringify(k) + ":" + canonicalize(value[k])).join(",") + "}";
}

async function sha256Hex(text) {
  if (!crypto?.subtle) return "browser_crypto_unavailable";
  const bytes = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, "0")).join("");
}

async function verifyReceipt(receipt) {
  const errors = [];
  const warnings = [];
  const expectedSchema = "AXZ-LVT-RECEIPT-v1";
  const shaRe = /^[0-9a-f]{64}$/;

  if (receipt.schema !== expectedSchema) errors.push(`schema must be ${expectedSchema}`);
  ["receipt_id", "artifact_name", "claim", "truth_label", "scope"].forEach(key => {
    if (!receipt[key]) errors.push(`${key} is required`);
  });

  if (!Array.isArray(receipt.evidence_hashes) || receipt.evidence_hashes.length === 0) {
    errors.push("evidence_hashes must be a non-empty list");
  } else {
    receipt.evidence_hashes.forEach((item, index) => {
      if (!item || typeof item !== "object") {
        errors.push(`evidence_hashes[${index}] must be an object`);
      } else if (!shaRe.test(String(item.sha256 || ""))) {
        errors.push(`evidence_hashes[${index}].sha256 must be 64 lowercase hex characters`);
      }
    });
  }

  if (!Array.isArray(receipt.tests) || receipt.tests.length === 0) {
    errors.push("tests must be a non-empty list");
  } else {
    receipt.tests.forEach((test, index) => {
      if (!test || typeof test !== "object") {
        errors.push(`tests[${index}] must be an object`);
      } else {
        if (!test.name) errors.push(`tests[${index}].name is required`);
        if (!["PASS", "FAIL", "SKIP"].includes(test.status)) errors.push(`tests[${index}].status must be PASS, FAIL, or SKIP`);
        if (test.status === "FAIL") errors.push(`test failed: ${test.name}`);
      }
    });
  }

  if (String(receipt.claim || "").toLowerCase().includes("global") && !String(receipt.scope || "").toLowerCase().includes("no global")) {
    warnings.push("claim mentions global scope; keep public claim receipt-bounded");
  }

  const result = errors.length ? "REJECT" : "ACCEPT";
  return {
    engine: "Axezent AI Library of Verified Things",
    result,
    truth_label: receipt.truth_label || "MISSING_TRUTH_LABEL",
    errors,
    warnings,
    receipt_sha256: await sha256Hex(canonicalize(receipt)),
    truth_boundary: "finite deterministic receipt check only; no global proof, alignment, prize, investment, or guaranteed-support claim"
  };
}

function setReceipt(obj) {
  receiptInput.value = JSON.stringify(obj, null, 2);
  resultOutput.textContent = "Loaded. Click Verify receipt.";
}

document.querySelector("#loadPass").addEventListener("click", () => setReceipt(passDemo));
document.querySelector("#loadFail").addEventListener("click", () => setReceipt(failDemo));
document.querySelector("#clearReceipt").addEventListener("click", () => {
  receiptInput.value = "";
  resultOutput.textContent = "Ready. Load a demo or paste a receipt.";
});
document.querySelector("#verifyButton").addEventListener("click", async () => {
  try {
    const receipt = JSON.parse(receiptInput.value);
    const report = await verifyReceipt(receipt);
    resultOutput.textContent = JSON.stringify(report, null, 2);
    resultOutput.className = report.result === "ACCEPT" ? "result-accept" : "result-reject";
  } catch (err) {
    resultOutput.textContent = JSON.stringify({ result: "ERROR", errors: [String(err.message || err)] }, null, 2);
    resultOutput.className = "result-reject";
  }
});

document.querySelector("#copyCash").addEventListener("click", async () => {
  await navigator.clipboard?.writeText("$Axezent");
  document.querySelector("#copyCash").textContent = "Copied $Axezent";
});

function renderEntries(filter = "") {
  const q = filter.trim().toLowerCase();
  const visible = entries.filter(e => JSON.stringify(e).toLowerCase().includes(q));
  libraryEntries.innerHTML = visible.map(e => `
    <article class="card">
      <small>${e.truth_label}</small>
      <h3>${e.name}</h3>
      <p><strong>${e.category}</strong></p>
      <p>${e.description}</p>
      <p>Status: ${e.status}</p>
    </article>
  `).join("");
}

async function loadLibrary() {
  try {
    const res = await fetch("../data/library.json");
    const data = await res.json();
    entries = data.entries || [];
  } catch {
    entries = [
      { name: "Axezent AI CTR Receipt Checker", category: "AI compliance verification", status: "PUBLIC_STANDARD_SEED", truth_label: "FINITE_POLICY_RECEIPT_CHECK", description: "Checks finite AI-agent trace receipts against declared deterministic policy rules." },
      { name: "Axezent AI PRK-Fuzzer", category: "complexity reduction test data", status: "PUBLIC_STANDARD_SEED", truth_label: "FINITE_REDUCTION_RECEIPT_FUZZING", description: "Generates valid and controlled-invalid finite 3SAT-to-CLIQUE receipts." },
      { name: "Library of Verified Things Website", category: "public proof-artifact dashboard", status: "LAUNCH_READY_STATIC_SITE", truth_label: "BUSINESS_LAYER_SCAFFOLD", description: "Static website and local verifier." }
    ];
  }
  renderEntries();
}
searchInput.addEventListener("input", e => renderEntries(e.target.value));
setReceipt(passDemo);
loadLibrary();
