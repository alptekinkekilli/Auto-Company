---
name: directive writer & section refs
slug: directive-writer-section-refs
type: file
sources:
  - path: tests/test_directive_section_refs.sh
    hash: 413742241d956ae77feb01e20780757ee86fa63f3699e3926a2ddeea81a53a71
sources_digest: 8b661c6cefe4ff5f3a7f27bbb81f63b12029092bb13b454946fa8130a43147a8
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

scripts/core/directive_writer.py's undefined_section_refs() guards against references to absent sections (the bug that froze directive revision 11). It is tested purely via stdin heredocs with no file I/O or live directive state, checking comma-joined output for clean bodies, no-section bodies, the exact revision-11 failure shape, mixed defined/undefined refs, and defined-but-unreferenced headers.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
