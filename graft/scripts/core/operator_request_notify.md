# scripts/core/operator_request_notify.py · [[atomic-write-read-back-verification]] [[operator-escalation-notification]] [[operator-request-lifecycle]]

Deterministic operator-escalation gate that dedups, notifies, and resolves OPREQ ledger requests, and regenerates the consensus.md Awaiting Operator projection.

- _looks_secret · function · L114-L123 — Decides whether a long opaque token is secret-shaped so only genuinely secret-looking tokens get redacted, not request IDs or doc slugs.
- now_iso · function · L134-L135 — Returns the current UTC time as an ISO-8601 string for audit stamps.
- norm_field · function · L138-L139 — Collapses whitespace in a field value to a single space for stable hashing and comparison.
- material_hash · function · L142-L151 — Computes a SHA-256 content fingerprint over the material request fields so dedup keys on actual content changes, not presence.
- parse_fields · function · L154-L166 — Parses a request block body into a key/value field dict, folding continuation lines into their field.
- parse_blocks · function · L169-L181 — Splits the ledger text into per-OPREQ blocks with their body spans for precise in-place rewrites.
- validate_required · function · L184-L186 — Checks that all required OPREQ fields are present and non-empty.
- set_field_in_block_body · function · L189-L198 — Rewrites or appends a single field line within a request block body.
- set_field_in_text · function · L201-L208 — Applies a field rewrite to the full ledger text at the given request's block span.
- scrub_secrets · function · L211-L216 — Redacts known secret patterns and secret-shaped long tokens from notification text before sending.
- compose_message · function · L241-L271 — Builds a scannable Telegram message with a type-specific headline, truncated required input, and the correct reply path.
- send_telegram · function · L274-L294 — Posts a message to the Telegram API and reports delivery only when the API confirms ok:true.
- attempt_notify · function · L297-L306 — Retries a Telegram send with backoff up to MAX_ATTEMPTS, returning success and attempt count.
- load_state · function · L309-L327 — Loads the dedup state JSON, backing up and resetting on corruption so a bad file never crashes the loop.
- write_state · function · L330-L337 — Atomically writes dedup state via temp-file replace and verifies the read-back matches.
- write_text_verified · function · L340-L342 — Writes a file and confirms the written bytes read back identically.
- audit · function · L345-L348 — Appends a timestamped line to the audit log.
- render_projection_body · function · L351-L366 — Renders the Awaiting Operator projection body from open items, or a none marker when empty.
- splice_projection · function · L369-L397 — Inserts or replaces the Awaiting Operator section in consensus.md, handling both existing and anchored insertion points.
- process_notifications · function · L400-L480 — Iterates OPEN requests, validates, fingerprints, dedups, and sends Telegram notifications for escalation-worthy types.
- _resolve_evidence_path · function · L489-L499 — Resolves a relative evidence path against the app root, confining it to the operator-evidence directory.
- verify_document_procurement · function · L502-L567 — Verifies a document-procurement resolution by checksum-matching an evidence file on disk, reading the evidence path from the directive first.
- verify_credential · function · L570-L611 — Verifies a credential resolution against a non-secret verification-log artifact.
- _directive_window_after · function · L635-L643 — Extracts the directive text window following an anchor label for a given request.
- verify_legal_or_financial_decision · function · L649-L671 — Verifies a legal/financial decision resolution from a structured decision the operator wrote in the directive.
- verify_authorization · function · L674-L700 — Verifies an authorization resolution from a structured operator decision in the directive.
- refusal_for · function · L716-L740 — Detects an operator REFUSE for a request from the directive and returns the refusal reason.
- verify_resolution · function · L743-L764 — Dispatches to the type-specific deterministic verifier to confirm a request is genuinely resolved before flipping OPEN to RESOLVED.
- _answer_sources · function · L767-L785 — Collects the directive and decisions text sources that may contain an operator answer.
- process_resolutions · function · L788-L846 — Scans OPEN requests against the directive and decisions text, verifying and flipping resolved ones to RESOLVED.
- _main_impl · function · L849-L941 — Orchestrates the full run: load ledger/state, process notifications and resolutions, write state and projection, always exiting 0.
- main · function · L944-L956 — Entry point that resolves the app dir and invokes the main implementation with default send/sleep functions.
