# scripts/ops/rfq_template.py

Module holding the RFQ email content (subject/body/SCOPE) so the text can be iterated freely without touching the protected send logic in rfq-send.py.

- _html_signature · function · L49-L56 — Loads the branded HTML signature from rfq_signature.html, extracting the <body> content, and falls back to a plain-text signature wrapped in <pre> if the file is missing.
- subject · function · L61-L62 — Builds the email subject line asking for a price quote for the given category.
- body · function · L65-L82 — Composes the full RFQ email body: anonymous intro, the category-specific scope, requested quote details, and the Appricode signature.
- body_html · function · L85-L108 — Builds the text/html email part with the same humanized message plus the branded HTML signature, HTML-escaping the scope text.
