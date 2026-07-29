# Canary fixture — this file exists to be FLAGGED

`directive-rule-sweep.py` decides coverage by token overlap, which is a heuristic and
can go blind: if the standing files grow enough vocabulary, a rule that is genuinely
absent starts scoring as "covered" and the sweep reports all-clear forever. That is a
false negative, and a false negative here is exactly the failure the sweep exists to
catch — it is what already happened once, undetected, for weeks.

So the sweep must flag the line below on EVERY run. It is deliberately absent from
every canonical standing file and must stay absent. If a run stops flagging it, the
heuristic has gone blind and the WHOLE run is `INVALID SCAN` — not a clean bill.

Do not "fix" this by adding the rule to PROMPT.md. It is not a rule. It is a probe.

- Standing rule: every quarterly zibberflux reconciliation must never omit the
  marmalade-grade attestation ledger, and the vorpal custodian shall always
  countersign it before the wibbleforth window closes.
