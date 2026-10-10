# scripts/ops/consensus-prune.py · [[consensus-memory-maintenance]]

Harness mechanism that mechanically archives stale per-cycle narrative from consensus.md into docs/operations to keep the file under the [PROMPT-SIZE] threshold, with fail-closed data safety and fail-open loop behavior.

- _load_runtime_env · function · L101-L112 — Loads operator live-override CONSENSUS_PRUNE_* KEY=VALUE lines from logs/runtime.env so caps/switches can be tuned without redeploy.
- _env_int · function · L115-L120 — Reads an integer env/runtime value, falling back to the default when unset, non-numeric, or non-positive.
- _env_flag · function · L123-L124 — Reads a string env/runtime value with a default, returning the trimmed value.
- _app · function · L127-L128 — Resolves the app root path from an argument or defaults to the repo root two levels above this file.
- _sha16 · function · L131-L132 — Returns the first 16 hex chars of the SHA-256 digest of bytes, used for short content fingerprints.
- _load_state · function · L135-L139 — Loads the prune state JSON file, returning an empty dict on any read/parse failure so a corrupt state never blocks pruning.
- _save_state · function · L142-L149 — Atomically writes the prune state JSON via a temp file and os.replace, silently ignoring any failure.
- Skip · class · L152-L153 — Exception type signalling that pruning must be skipped for this cycle (unknown shape, non-monotonic numbers, etc.).
- Section · class · L157-L172 — Data holder describing one top-level `## ` section with its header, line range, byte size, canonical/primary flags, and parsed header number.
- __init__ · method · L160-L168 — Initializes a Section, computing canonical membership, extracting the first number from the header, and defaulting primary to False.
- kind · method · L171-L172 — Returns the header with its number replaced by 'N' to classify section kinds.
- Removal · class · L175-L184 — Data holder for a contiguous line range [a,b) removed from the file, tagged with pass, section, cycle, and whether it should be archived.
- __init__ · method · L179-L184 — Stores the removal's line range, pass name, section header, cycle number, and archive flag.
- _split_sections · function · L187-L195 — Splits the file's lines into preamble plus Section objects at each top-level `## ` header, computing each section's byte size.
- _mark_primary · function · L198-L219 — Finds the byte-largest run of consecutive canonical, pairwise-distinct sections and marks them as the primary block to protect.
- flush · function · L204-L207 — Compares the current run's total bytes against the best run and keeps the larger one.
- _tail_pass · function · L223-L227 — Archives every non-primary section except the keep_tail largest-numbered ones, which stay in place.
- _entries_wwd · function · L230-L262 — Parses What We Did bullets (`- **Cycle N`) plus continuation lines into entries, drops old archive notes, and raises Skip on unrecognized top-level bullets.
- _entries_para · function · L265-L282 — Parses paragraph sections (NA/CP/CS) into entries where a paragraph starting with `**Cycle N` is a removable block including its trailing blank lines.
- _select · function · L285-L308 — Archives entries from the smallest cycle number until the section is under its byte cap (and entry keep bound), always leaving at least one entry, skipping on duplicate cycles or code fences.
- _line_offsets · function · L312-L316 — Computes the byte offset of each line's start in the file for later block extraction.
- _strip_and_blocks · function · L319-L334 — Removes the given line ranges from the data, returning stripped bytes plus (offset, bytes) blocks, and raises Skip on overlapping removals.
- _rebuild · function · L337-L346 — Inverse of _strip_and_blocks: re-inserts every removed block at its original byte offset to reconstruct the original file.
- main · function · L350-L647 — Orchestrates the whole prune run: reads consensus, applies tail/NA/CP/CS/WWD passes, rebuild-checks, archives with sha verification, and reports warnings or skip alarms.
- finish_skip · function · L379-L395 — Records a skip (or resets the streak) in state, prints a skip-streak alarm when over threshold, and never touches guard-facing keys.
- after_bytes · function · L461-L462 — Computes a section's byte size after its removals are applied.
- record_history · function · L478-L495 — Tracks per-section byte history across recent runs to detect bloat for warning emission.
- emit_warns · function · L497-L499 — Prints accumulated bloat and non-canonical-header warnings to stdout.
