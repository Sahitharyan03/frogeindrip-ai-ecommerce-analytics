# Data Privacy, Security & Governance Protocol
**Project:** Frogeindrip Analytics Platform  
**Compliance Standards:** Client Confidentiality, PII Redaction, Zero Hardcoded Secrets, OWASP LLM Guardrails  

---

## 1. Client Identity & Account Redaction

1. **Brand Identity:** The verified business and client brand is **Frogeindrip**.
2. **Account Profile Redaction:** In the primary Square Analytics screenshots, the account profile name "Real Knitz" appears in the top-left navigation drawer. In accordance with client privacy requirements:
   - "Real Knitz" is strictly treated as an internal Square profile identifier, not a separate employer or corporate entity.
   - All public documentation, UI cards, and screenshots must redact or replace this label with `[REDACTED ACCOUNT ID]`.
   - Never confuse or rename Frogeindrip to Real Knitz.

---

## 2. PII (Personally Identifiable Information) Firewall

1. **No Sensitive Customer Records in Git:**
   - Raw client customer CSVs (containing personal email addresses, phone numbers, or physical street addresses) are excluded via `.gitignore`.
2. **Synthetic Demonstration Isolation:**
   - All granular transactional datasets published in `data/synthetic/` are generated via deterministic simulation (`seed=42`) using anonymized synthetic names and fake domains (`example.com`).
   - No real customer PII exists anywhere in the repository codebase.

---

## 3. Environment & Credential Management

1. **Zero Committed API Keys:**
   - `OPENAI_API_KEY` and other sensitive environmental tokens are never committed to version control.
   - Credentials must be configured via local `.env` files (ignored in `.gitignore`) or runtime environment variables.
2. **API-Key-Free Default Mode:**
   - The application does not require an OpenAI API key to run. If no key is detected, the AI Copilot seamlessly defaults to an offline deterministic engine with full data grounding and zero degradation of analytical correctness.

---

## 4. AI Copilot Safety Guardrails

1. **No Arbitrary SQL Execution:**
   - The LLM is never permitted to execute dynamic, arbitrary SQL strings against the database.
   - User queries are mapped strictly to predefined, read-only parameterized analytics tools in `frogeindrip.ai.tools`.
2. **Injection Defense:**
   - Inputs containing SQL DDL/DML keywords (`DROP`, `DELETE`, `UPDATE`, `ALTER`, `GRANT`) are intercepted and rejected by the input firewall.
3. **Database as Untrusted Content:**
   - Content retrieved from the database is treated strictly as data, never as prompt instructions.
