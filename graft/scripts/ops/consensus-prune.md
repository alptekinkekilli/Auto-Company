# scripts/ops/consensus-prune.py · [[consensus-and-registry-maintenance]] [[state-snapshot-consensus]]

Harness script that mechanically archives old 'What We Did This Cycle' entries from consensus.md into dated docs/ archives to keep the file under the [PROMPT-SIZE] brake threshold, fail-closed but never silent.

- _env_int · function · L61-L66 — Reads a positive integer from an env var, falling back to a default on missing/invalid/non-positive values.
- _app · function · L69-L70 — Resolves the app root path from an argument or defaults to the repo root two levels above this file.
- _sha16 · function · L73-L74 — Returns the first 16 hex chars of the SHA-256 digest of bytes, used for short content fingerprints.
- _load_state · function · L77-L81 — Loads the prune state JSON file, returning an empty dict on any read/parse failure so a corrupt state never blocks pruning.
- _save_state · function · L84-L91 — Atomically writes the prune state JSON via a temp file and os.replace, silently ignoring any failure.
- _section_sizes · function · L94-L99 — Computes the UTF-8 byte size of each '## ' top-level section in the consensus text, used for reporting section weights.
- Skip · class · L102-L103 — Exception type signalling that pruning must be skipped for this cycle (unknown shape, non-monotonic numbers, etc.).
- _split_section · function · L106-L120 — Finds the line-index range of the 'What We Did This Cycle' section body, raising Skip if the header is absent.
- _parse_entries · function · L123-L153 — Splits the section body into preamble, Cycle entries (with their numbers), and drops old archive notes, raising Skip on any unrecognised top-level bullet.
- _check_monotonic · function · L156-L163 — Verifies cycle numbers are unique and strictly monotonic (ascending or descending) in file order, else raises Skip.
- _archive_path · function · L166-L167 — Builds the monthly archive file path under docs/operations from the current UTC date.
- main · function · L170-L327 — Orchestrates the whole prune: reads consensus, parses/validates entries, keeps the KEEP largest cycle numbers, appends removed blocks idempotently to the archive, rewrites consensus atomically, and records state/metrics.
- finish_skip · function · L190-L208 — Records a skip in state, tracks the consecutive-skip streak, and prints an alarm line to Telegram once the streak reaches the threshold so fail-closed is never silent.
