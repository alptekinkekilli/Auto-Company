---
name: Secret handling
slug: secret-handling
type: concept
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 7e5496c29eae3646af4874f74f0d70e22230b762a74acdfb7e38e93197b41aca
  - path: scripts/ops/rfq-send.py
    hash: 9f7b4a48afe6563f777bfe314209d32a3bc0343d178e25ecf0a442cac0ced2e5
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
  - path: tests/test_jcode_mcp_config.sh
    hash: 3a26837a4685e40b45e3e8593459a69680a7bc6cc7e839f4ceb986c570a27025
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
sources_digest: 7a00c437c8186472c28d7829786c73df41a521b48d34e46501d28da7d08363e2
links:
  - to: mcp-config-probe
    relation: implements
    description: 'Config keeps secrets in env, never argv.'
generator:
  version: 1
covers:
  - symbol: expand
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L96-L108'
  - symbol: sub
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L100-L105'
  - symbol: convert
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L111-L162'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L165-L276'
  - symbol: _load_key
    kind: function
    at: 'scripts/ops/rfq-send.py:L90-L111'
  - symbol: _app_dir
    kind: function
    at: 'scripts/ops/rfq-send.py:L114-L116'
  - symbol: _air
    kind: function
    at: 'scripts/ops/rfq-send.py:L120-L132'
  - symbol: _record
    kind: function
    at: 'scripts/ops/rfq-send.py:L135-L136'
  - symbol: _all_rows
    kind: function
    at: 'scripts/ops/rfq-send.py:L139-L150'
  - symbol: _sponsor_ok
    kind: function
    at: 'scripts/ops/rfq-send.py:L154-L155'
  - symbol: _opted_out
    kind: function
    at: 'scripts/ops/rfq-send.py:L158-L159'
  - symbol: _already_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L162-L163'
  - symbol: _email_of
    kind: function
    at: 'scripts/ops/rfq-send.py:L166-L168'
  - symbol: _caps_now
    kind: function
    at: 'scripts/ops/rfq-send.py:L171-L181'
  - symbol: render
    kind: function
    at: 'scripts/ops/rfq-send.py:L184-L191'
  - symbol: anonymity_scan
    kind: function
    at: 'scripts/ops/rfq-send.py:L194-L199'
  - symbol: decide
    kind: function
    at: 'scripts/ops/rfq-send.py:L202-L224'
  - symbol: _encode_subject
    kind: function
    at: 'scripts/ops/rfq-send.py:L228-L231'
  - symbol: send_fe
    kind: function
    at: 'scripts/ops/rfq-send.py:L234-L249'
  - symbol: _mark_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L252-L255'
  - symbol: main
    kind: function
    at: 'scripts/ops/rfq-send.py:L259-L301'
  - symbol: loop_env
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L39-L51'
  - symbol: main
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L54-L75'
---
<!-- context:generated:start -->
## Summary

Secrets are resolved from env, runtime.env, or macOS Keychain, and must never appear in process argv (where ps could expose them) — they live in MCP server env blocks. Keys are verified post-deploy by reading /proc/<pid>/environ, never printing values.

## Related

- implements [[mcp-config-probe]] — Config keeps secrets in env, never argv.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
