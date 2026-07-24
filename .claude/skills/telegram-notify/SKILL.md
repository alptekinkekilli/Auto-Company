---
name: telegram-notify
description: "Reach the human operator in real time on Telegram. Use when the company hits a decision point, a blocker, a payment/WTP signal, or anything the operator should see now — between the automatic per-cycle summaries."
---

# Telegram notify — reach the operator now

The company already sends the operator a short Telegram summary at the end of **every** cycle (wired into `scripts/core/auto-loop.sh`). Use this skill only for an **extra, ad-hoc** message when something happens the operator should see immediately.

## How

Run the notifier with your message as the argument:

```bash
bash scripts/core/telegram-notify.sh "🟢 WTP SIGNAL: a $549 staging-QA payment settled (Meridian Studio). Deal in Airtable Staging-QA Outreach. Awaiting your go to deliver."
```

It sends to the operator's Telegram and is a **no-op** if `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` are not set (so it never errors).

## When to use (not every cycle — the auto-summary already covers routine)

- A real **paid / WTP signal** (payment settled, pre-order, checkout attempt).
- A **blocker** that stops progress and needs the operator (missing access, a directive conflict, a broken external dependency).
- The **Codex analyst** produced a materially different selection the operator should review.
- A **guardrail** situation you refused to cross and want the operator to resolve.
- The operator explicitly asked to be pinged on X.

## Rules

- One message = one clear point. Lead with a tag: 🟢 signal · 🛑 blocker · 🧠 analyst · ⚠️ guardrail · ℹ️ info.
- Keep it short and actionable (what happened + what you need). Telegram caps at ~4096 chars; the script truncates.
- Never send secrets, tokens, credentials, or raw customer data.
- This channel is **outbound only** (company → operator); it does not accept instructions back. Operator steering still comes through `memories/human-directive.md` ([[apply-company-directive]]).
