#!/usr/bin/env bash
# Send a Telegram message to the operator (APP: real-time company<->operator channel).
# No-op if TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID are unset, so it is safe to call
# unconditionally from the loop. Never fails the caller.
# Usage: telegram-notify.sh "message text"    (or pipe the message on stdin)
set -uo pipefail

TOKEN="${TELEGRAM_BOT_TOKEN:-}"
CHAT="${TELEGRAM_CHAT_ID:-}"
[ -n "$TOKEN" ] && [ -n "$CHAT" ] || exit 0

MSG="${1:-$(cat 2>/dev/null || true)}"
[ -n "$MSG" ] || exit 0
# Telegram hard-caps message text at 4096 chars.
MSG=$(printf '%s' "$MSG" | head -c 3900)

curl -s --max-time 15 "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${CHAT}" \
  --data-urlencode "text=${MSG}" \
  --data-urlencode "disable_web_page_preview=true" >/dev/null 2>&1 || true
