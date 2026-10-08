---
name: directive writer section refs
slug: directive-writer-section-refs
type: concept
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

undefined_section_refs() in directive_writer.py detects references to absent sections, guarding against the bug that froze directive revision 11 (references to absent §6/§7). It is pure and deterministic (no file I/O or live directive state), comma-joining the list of undefined refs found in a body.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
