# scripts/core/engine-usage-cost.py · [[engine-output-extraction]]

CLI adapter that converts token usage (from Claude API JSON or jcode ndjson streams) into notional USD at Anthropic list prices, with a conservative unknown-model fallback so budget gates never silently read zero.

- _n · function · L75-L78 — None-safe integer coercion so OpenAI-provider tokens events with null cache fields don't raise.
- cost_for · function · L81-L123 — Computes notional USD cost from a token-usage dict, pricing known models from the PRICES table and unknown models at the max row times a conservative factor (or hard-failing under STRICT=1), including cache read/write multipliers.
- main · function · L126-L204 — Parses input (usage JSON or summed ndjson tokens events), resolves the actual model from the done event or hint, and emits the cost line with exit codes for bad input and unknown models.
