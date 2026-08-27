# scripts/ops/rfq_template.py · [[rfq-outreach-content]]

Module holding the non-sensitive RFQ email content (scope text, signature, subject, body) that rfq-send.py imports, so the copy can be iterated without touching protected send logic.

- subject · function · L43-L44 — Builds the email subject line asking for a price quote for the given category.
- body · function · L47-L64 — Composes the full RFQ email body: anonymous intro, the category-specific scope, requested quote details, and the Appricode signature.
