# scripts/core/engine-usage-cost.py · [[ops-analysis-audit-tools]] [[scripts-core]]

CLI adapter that converts token usage (Claude API or jcode ndjson) into notional USD at Anthropic list prices so the APP-263 budget gates keep seeing real numbers, with a conservative unknown-model fallback that never reports zero.

- _n · function · L66-L69 — None-safe integer coercion so OpenAI-provider tokens events with null cache fields don't raise.
- cost_for · function · L72-L110 — Computes notional USD from token counts, honoring per-TTL cache-write breakdowns and pricing unknown models at the max known row times a conservative factor (or hard-failing under STRICT).
- main · function · L113-L191 — Parses input (usage JSON or summed ndjson tokens events), resolves the actual model from the done event or hint, and emits the cost line with exit codes for bad input and unknown models.
