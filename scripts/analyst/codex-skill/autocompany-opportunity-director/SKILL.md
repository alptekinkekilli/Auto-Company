---
name: autocompany-opportunity-director
description: Read a complete Auto Company opportunity scan, extract and normalize every candidate, independently screen and select the strongest opportunities with PROJECT_EVALUATION_FRAMEWORK.md, verify implementation-critical library and API claims through current Context7 documentation, rank and sequence finalists, design paid validation gates, and write a paste-ready memories/human-directive.md. Use when the user supplies all discovered ideas or a full consensus/scan and wants Codex to choose the candidates, challenge Auto Company's choices, improve a validation directive, or decide GO, CONDITIONAL GO, PIVOT, HOLD, or NO-GO. The user does not need to preselect candidates.
---

# Auto Company Opportunity Director

Produce a decision, not another brainstorm. Separate category evidence, company-specific WTP, technical feasibility, and business quality.

## Required inputs

Use the materials supplied by the user or present in the workspace:

- the complete candidate list, latest consensus, or opportunity scan;
- `PROJECT_EVALUATION_FRAMEWORK.md`;
- prior test results, payments, interviews, delivery logs, and directives;
- any proposed buyer, price, outcome, channel, and fulfillment method.

Search the workspace with `rg --files` and `rg`. Read the current framework completely. If it is absent, read [references/framework-fallback.md](references/framework-fallback.md).

Do not silently treat missing data as negative evidence. Mark it unknown and design the cheapest decisive test.

The user does not need to identify finalists. Treat candidate selection as part of the skill's job. If the user explicitly supplies a shortlist, evaluate it but still flag a stronger candidate found in the supplied scan.

## Context7 boundary

Use Context7 only for current, implementation-relevant documentation:

- whether a proposed platform/library/API supports the required operation;
- authentication, rate limits, webhooks, data formats, version behavior, or integration constraints;
- whether an incumbent platform has a documented native technical capability when its official docs are indexed.

Never use Context7 as evidence for:

- market size, buyer urgency, willingness to pay, pricing acceptance, or customer behavior;
- competitor adoption, market share, or distribution;
- legal conclusions or professional compliance advice;
- claims that require current market research rather than software documentation.

For those questions, use primary-source web research when authorized/needed and label evidence tiers honestly.

Do not send confidential code, customer data, internal project names, secrets, or unpublished strategy in Context7 queries. Rewrite queries generically.

## Query Context7

Use [scripts/context7_docs.sh](scripts/context7_docs.sh). It reads the API key from `CONTEXT7_API_KEY` or macOS Keychain service `autocompany-context7-key` without printing the token.

```bash
scripts/context7_docs.sh check
scripts/context7_docs.sh search "cloudflare workers" "D1 scheduled jobs and REST API support"
scripts/context7_docs.sh docs "/cloudflare/cloudflare-docs" "Document the exact API capability needed for a weekly data pipeline"
```

Resolve the library first unless an exact Context7 library ID is already known. Make narrow queries tied to a load-bearing technical assumption. Record:

- library ID and version if available;
- exact capability supported or unsupported;
- relevant constraint;
- retrieval date;
- whether the result changes the directive.

A Context7 miss means “not established through Context7,” not “the capability does not exist.”

## Evaluation workflow

### 1. Inventory the entire scan

Extract every distinct candidate before ranking. Include candidates marked rejected, closed, reframed, or queued so that prior conclusions can be audited without silently reopening duplicates.

For each candidate record:

- identifier and name;
- buyer and user;
- proposed price/model;
- delivered artifact/service;
- purchased outcome;
- current Auto Company decision;
- strongest evidence tier;
- known direct, free, platform, manual, and do-nothing substitutes;
- explicit legal, trust, margin, technical, and distribution risks.

Briefly explain every candidate in the output. Do not omit low-ranked candidates merely to make the finalists look stronger.

### 2. Normalize each candidate

State in one line:

> Buyer pays [price/model] for [delivered artifact/service] to obtain [measurable outcome].

Separate visible feature from purchased result. Reject vague candidate names that do not identify a buyer and outcome.

### 3. Build the evidence ledger

Classify every load-bearing claim:

1. Auto Company real payment/repeat use
2. Paid pilot or binding purchase
3. Target-customer problem interview
4. Completed critical usage
5. Waitlist/registration
6. Traffic/general category interest
7. Assumption

Competitor revenue or pricing is category evidence only. It is never Auto Company Tier 1 or 2 evidence.

Maintain four distinct ledgers:

- problem and buyer;
- WTP and price;
- distribution;
- fulfillment/technical feasibility.

### 4. Apply the five-alternative test

Inspect:

1. direct paid competitors;
2. free/open-source tools;
3. platform-native features;
4. manual/service alternatives;
5. doing nothing.

Ask whether the wedge is an actual product/business advantage or merely a feature an incumbent can add.

### 5. Run the independent selection screen

Do not rank a candidate highly merely because a landing page or manual pilot is cheap.

Score:

- frequency and urgency;
- measurable cost of inaction;
- repeat-purchase mechanism;
- gross-margin path;
- reusable production/data/IP;
- first-50-buyer reachability;
- incumbent/platform risk;
- trust, legal, security, and reliance risk.

Use a 0–5 score for each factor and show the reasoning, not just the total. Apply these default weights:

- problem frequency and measurable economic pain: 20%;
- Auto Company-specific WTP evidence: 20%;
- first-50-buyer reachability: 15%;
- repeat revenue/repurchase mechanism: 15%;
- reusable production, data, or IP and margin path: 15%;
- competitive/platform defensibility: 10%;
- legal, trust, security, and reliance safety: 5%.

Treat a fatal condition as a veto regardless of weighted score:

- dominant free/platform substitute closes the claimed wedge;
- no plausible consent-based first-50-buyer channel;
- fulfillment economics cannot reach the required margin without lowering quality or increasing liability;
- necessary expertise or authority is absent;
- offer depends on misleading legal, financial, security, or professional claims;
- candidate is only a generic product category with no concrete buyer/problem wedge.

Distinguish:

- **cheap to test**;
- **likely to produce payment**;
- **worth building if the test succeeds**.

After scoring, independently choose:

- one active finalist;
- at most one queued finalist;
- optional research-gated candidates;
- all remaining `HOLD` or `NO-GO` candidates.

Compare this selection with Auto Company's selection. Explain every disagreement through evidence, economics, or sequencing rather than taste.

### 6. Use Context7 for load-bearing implementation claims

Query only the libraries/APIs that materially affect feasibility or an incumbent-native-substitute claim. Do not query every technology mentioned.

If the candidate is still blocked by WTP or distribution and technical feasibility is ordinary, state that Context7 research is not decision-relevant yet and avoid unnecessary calls.

### 7. Rank and sequence

Choose at most:

- one active paid validation;
- one queued follow-up candidate;
- research-only/HOLD candidates;
- explicit NO-GO candidates.

Do not authorize parallel product builds. Do not replace a failed test with feature development or fresh ideation.

### 8. Design terminal experiments

For each `CONDITIONAL GO` or `PIVOT`, specify:

- hypothesis;
- one narrow segment;
- concrete prepaid offer and price;
- acquisition channel;
- qualified sample;
- duration;
- payment, delivery, repeat, margin, and outcome thresholds;
- pivot signals;
- terminal stop conditions.

Use the framework default—10 days, 50 qualified personalized contacts, 10 problem interviews, and 3 real payments—unless economics or buyer rarity justifies a documented change.

Interest, traffic, free pilots, compliments, checkout visits, email opens, and “maybe later” do not count as payment.

### 9. Write the directive

Use [references/directive-template.md](references/directive-template.md). The directive must:

- state `ACTIVE`, issue date, scope, and ordered priority;
- define what is and is not authorized;
- allow only one active validation at a time;
- contain numerical continue, pivot, and stop gates;
- prohibit product construction before the paid gate;
- require logged payments, delivery time, outcomes, repeat behavior, and acquisition source;
- end with the exact condition that marks the directive `DONE`.

Write the complete evaluation as a separate report when requested. Keep `human-directive.md` operational and compact.

## Decision discipline

- `GO`: real payment plus repeat behavior and reachable distribution support building/scaling.
- `CONDITIONAL GO`: run one bounded paid test; no broad build.
- `PIVOT`: preserve a proven problem/asset while changing a falsified buyer, offer, price, or channel.
- `HOLD`: name the external evidence/prerequisite and reevaluation condition.
- `NO-GO`: stop; state what new primary evidence would be required to reopen.

Never call a candidate `GO` because its code is ready, a regulation exists, a competitor charges money, or a manual test is inexpensive.

## Output order

1. Brief explanation of every candidate found in the scan.
2. Independent scoring and fatal-veto table.
3. Auto Company selection versus skill selection.
4. Executive decision and ordered portfolio.
5. Framework analysis of the active candidate.
6. Why queued/HOLD/NO-GO candidates are not active.
7. Context7 technical evidence and its decision impact.
8. Minimum validation experiment.
9. Continue/pivot/stop gates.
10. Paste-ready `memories/human-directive.md`.
11. Confidence and open questions.
