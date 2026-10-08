# tests/test_consensus_prune.py · [[operational-guard-tripwires]]

End-to-end test suite for the consensus-prune script, covering archiving, no-op thresholds, skip guards, kill switch, dry-run, dedupe, and ledger-guard integration.

- check · function · L17-L20 — Records a pass/fail result for a named test assertion and accumulates failures for the final summary.
- newapp · function · L23-L26 — Creates a fresh temporary app directory with the expected memories/logs/docs/operations subdirectories for a test run.
- consensus · function · L29-L30 — Returns the path to the consensus.md file inside a given app directory.
- entry · function · L33-L38 — Builds a single consensus cycle entry bullet padded with filler to a target byte size (default 1800) to simulate realistic large entries.
- doc · function · L41-L51 — Assembles a full consensus markdown document from cycle entries plus optional extra bullet and note, with the standard section headers.
- run · function · L54-L62 — Helper that invokes the consensus-prune script as a subprocess with the given cycle, app dir, env overrides, and optional dry-run flag, returning exit code and stdout.
- guard · function · L65-L68 — Invokes the ledger-guard.py script as a subprocess against an app dir for a given cycle and returns its stdout.
