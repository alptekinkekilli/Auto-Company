---
name: cost audit tool surface
slug: cost-audit-tool-surface
type: concept
sources:
  - path: tests/test_cost_audit_tool_surface.py
    hash: 801b92c715ca95cef9c34ab863f87fa443c8abcc65ba03237a934f5aed78121a
sources_digest: 65c78c93d0cfb2571cd60fa948df8ff16076750450177467d92e46909a85f8f9
links:
  - to: cost-model-hint
    relation: uses
    description: Both price token streams from the engine
generator:
  version: 1
covers:
  - symbol: ok
    kind: function
    at: 'tests/test_cost_audit_tool_surface.py:L24-L25'
  - symbol: 'no'
    kind: function
    at: 'tests/test_cost_audit_tool_surface.py:L28-L31'
---
<!-- context:generated:start -->
## Summary

The §5 tool-surface logic in cost-audit.py subtracts tools hidden by the JCODE_TOOLS_DENY deny-list from the advertised column rather than counting the raw MCP schema-cache (which previously caused OPREQ-1 false positives). The auto-loop.sh default yields exactly 15 browseros and 2 context7 denied tools while keeping mcp__browseros__tabs available; an environment override of JCODE_TOOLS_DENY takes precedence. The hidden/in-prefix calculation must be robust to cache format (namespaced variants).

## Related

- uses [[cost-model-hint]] — Both price token streams from the engine
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
