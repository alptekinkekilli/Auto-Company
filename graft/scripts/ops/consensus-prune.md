# scripts/ops/consensus-prune.py · [[consensus-registry-maintenance]]

Harness mechanism that mechanically archives old 'What We Did This Cycle' entries from consensus.md into a dated docs/ archive to keep the file under the prompt-size cap, fail-closed but never silent.

- _load_runtime_env · function · L69-L80 — Loads CONSENSUS_PRUNE_* overrides from logs/runtime.env so KEEP/MIN_BYTES/ENABLED can be tuned live without a redeploy, with the runtime.env value beating the process env.
- _env_int · function · L83-L88 — Reads an integer env/runtime value, falling back to the default when unset, non-numeric, or non-positive.
- _env_flag · function · L91-L92 — Reads a string env/runtime value with a default, returning the trimmed value.
- _app · function · L95-L96 — Resolves the app root path from an argument or defaults to the repo root two levels above this file.
- _sha16 · function · L99-L100 — Returns the first 16 hex chars of the SHA-256 digest of bytes, used for short content fingerprints.
- _load_state · function · L103-L107 — Loads the prune state JSON file, returning an empty dict on any read/parse failure so a corrupt state never blocks pruning.
- _save_state · function · L110-L117 — Atomically writes the prune state JSON via a temp file and os.replace, silently ignoring any failure.
- _section_sizes · function · L120-L125 — Computes the UTF-8 byte size of each '## ' top-level section in the consensus text, used for reporting section weights.
- Skip · class · L128-L129 — Exception type signalling that pruning must be skipped for this cycle (unknown shape, non-monotonic numbers, etc.).
- _split_section · function · L132-L146 — Finds the line-index range of the 'What We Did This Cycle' section body, raising Skip if the header is absent.
- _parse_entries · function · L149-L186 — Splits the section body into preamble, cycle entries, and dropped archive notes, skipping on any unrecognized top-level bullet to fail closed on unknown shapes.
- _check_monotonic · function · L189-L196 — Verifies cycle numbers are unique and strictly monotonic (ascending or descending) in file order, else raises Skip.
- _archive_path · function · L199-L200 — Builds the monthly archive file path under docs/operations from the current UTC date.
- main · function · L203-L373 — Orchestrates the prune: validates the consensus file shape, selects the KEEP largest cycle numbers, archives removed entries byte-exact and idempotently, rewrites consensus atomically with an INCIDENT_RE-safe note, and records state for ledger-guard.
- finish_skip · function · L227-L245 — Records a skip in state, tracks the consecutive-skip streak, and prints an alarm line to Telegram once the streak reaches the threshold so fail-closed is never silent.
