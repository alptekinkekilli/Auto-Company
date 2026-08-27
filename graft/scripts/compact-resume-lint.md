# scripts/compact-resume-lint.py · [[compact-ritual]] [[compact-ritual-scripts]]

A lint script that mechanically enforces the 'foreign-reader test' half of the compact ritual by rejecting stale measurement numbers in the resume and requiring all template sections.

- main · function · L39-L71 — Reads the resume file, collects violations (empty file, leftover placeholders, missing sections, forbidden numbers) and exits 1 with a red report if any are found, else 0 green.
