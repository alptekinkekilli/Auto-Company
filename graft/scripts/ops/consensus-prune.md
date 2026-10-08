# scripts/ops/consensus-prune.py · [[auto-loop-orchestration]] [[consensus-ledger-integrity-guards]] [[content-hash-provenance]]

Harness script that mechanically archives old 'What We Did This Cycle' entries from memories/consensus.md into a dated docs/operations archive to keep the file under the [PROMPT-SIZE] cap, fail-closed but never silent.

- _load_runtime_env · function · L64-L75 — Loads CONSENSUS_PRUNE_* overrides from logs/runtime.env so KEEP/MIN_BYTES/ENABLED can be tuned live without a redeploy, with the runtime.env value beating the process env.
- _env_int · function · L78-L83 — Reads an integer env/runtime value, falling back to the default when unset, non-numeric, or non-positive.
- _env_flag · function · L86-L87 — Reads a string env/runtime value with a default, returning the trimmed value.
- _app · function · L90-L91 — Resolves the app root path from an argument or defaults to the repo root two levels above this file.
- _sha16 · function · L94-L95 — Returns the first 16 hex chars of the SHA-256 digest of bytes, used for short content fingerprints.
- _load_state · function · L98-L102 — Loads the prune state JSON file, returning an empty dict on any read/parse failure so a corrupt state never blocks pruning.
- _save_state · function · L105-L112 — Atomically writes the prune state JSON via a temp file and os.replace, silently ignoring any failure.
- _section_sizes · function · L115-L120 — Computes the UTF-8 byte size of each '## ' top-level section in the consensus text, used for reporting section weights.
- Skip · class · L123-L124 — Exception type signalling that pruning must be skipped for this cycle (unknown shape, non-monotonic numbers, etc.).
- _split_section · function · L127-L141 — Finds the line-index range of the 'What We Did This Cycle' section body, raising Skip if the header is absent.
- _parse_entries · function · L144-L174 — Splits the section body into preamble, Cycle entries (with their numbers), and drops old archive notes, raising Skip on any unrecognised top-level bullet.
- _check_monotonic · function · L177-L184 — Verifies cycle numbers are unique and strictly monotonic (ascending or descending) in file order, else raises Skip.
- _archive_path · function · L187-L188 — Builds the monthly archive file path under docs/operations from the current UTC date.
- main · function · L191-L361 — Orchestrates the prune: validates the consensus file shape, selects the KEEP largest cycle numbers, archives removed entries byte-exact and idempotently, rewrites consensus atomically with an INCIDENT_RE-safe note, and records state for ledger-guard.
- finish_skip · function · L215-L233 — Records a skip in state, tracks the consecutive-skip streak, and prints an alarm line to Telegram once the streak reaches the threshold so fail-closed is never silent.
