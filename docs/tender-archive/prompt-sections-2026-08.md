# PROMPT.md — Tender-çağı bölümleri (arşiv, 2026-08-24)

Wowcar 2.0 re-charter'ı sırasında PROMPT.md'den çıkarılan bölümlerin birebir
kopyası. Salt-okunur tarih; geri almak = ilgili bloğu PROMPT.md'ye taşımak.


<!-- ======== PROJECT SELECTION & EVALUATION + WTP HARD STOP + FEASIBILITY PACKETS (PROMPT.md, arşivlendi 2026-08-24) ======== -->

## PROJECT SELECTION & EVALUATION (MANDATORY — use the framework)

Both when CHOOSING which idea to pursue AND when validating the chosen one, apply
`PROJECT_EVALUATION_FRAMEWORK.md` (the standard decision framework). Read it.

- **SELECTION (Cycle 1 ranking):** Rank ideas by the framework's evidence-first
  principles. Reject or down-rank any idea justified mainly by a deadline, a
  trend, or the mere existence of a regulation — a regulation does NOT create
  product demand, and a looming date is not evidence. Prefer ideas whose
  willingness-to-pay can be tested the cheapest and fastest.
- **VALIDATION (Cycle 2 GO/NO-GO):** Produce the framework's report and choose
  GO / CONDITIONAL GO / PIVOT / NO-GO / HOLD from the STRONGEST available evidence
  tier. Before any feature build, run the cheapest possible willingness-to-pay
  test. Interest, traffic, signups, free usage, email opens, and "I'd be
  interested" never count as payment validation.

### OPPORTUNITY REGISTRY + SEARCH REGIME — both live in the framework file

Both gates now live in `PROJECT_EVALUATION_FRAMEWORK.md`:

- **Opportunity registry / scan dedup** — "Fırsat kaydı ve tarama dedup". Load
  `memories/candidate-registry.md` BEFORE you scan, brainstorm or propose anything; dedup by
  **axis = (buyer × delivery-shape × price-point)**, never by name; never revive an Archived
  axis; never silently delete an Archived entry; log what you excluded and why.
- **Search regime** — "SEARCH REGIME", the discovery policy: where the company is allowed to
  win, the generation arms, and the pricing-structure gate.

They were moved out of this prompt on 2026-07-29 because they govern discovery, which is
currently disabled — **they are NOT conditional on that toggle.** Whenever you scan, rank or
propose an opportunity, open the framework and follow them; that is mandatory, not optional,
and "I did not read it" is not a defence for a duplicate or an out-of-regime proposal. Neither
gate ever authorizes a build — the HARD STOP below still applies.

### HARD STOP — no build before willingness-to-pay evidence

This is a BLOCKING gate, not advice. Before you write product code, scaffold an MVP,
or "activate a launch" for the chosen idea:

1. There MUST be a recorded willingness-to-pay (WTP) signal — a real payment, a
   pre-order, a paid pilot commitment, or a priced fake-door with actual checkout
   ATTEMPTS. Interest, signups, traffic, email opens, "I'd use this", or the mere
   existence of a regulation/deadline do NOT count.
2. If that signal does NOT yet exist, the ONLY build permitted this cycle is the
   cheapest test that could produce it (e.g. a priced landing page with a real
   checkout button). Do NOT build the product itself.
3. A deadline, regulation, or trend may NEVER be cited as a reason to build, to skip
   this gate, or to choose a forbidden platform. "Protecting the launch date" is not
   a valid justification — a date you cannot validate WTP against is not demand.
4. Maintain a `## WTP Evidence` field in `memories/consensus.md`: the signal, its
   evidence tier, and the date. If it is empty/absent, you are in PRE-VALIDATION —
   do not claim the product is being "built" or "launched"; run the WTP test instead.

Building ahead of WTP evidence, or racing a deadline, is a PROCESS FAILURE to be
corrected the next cycle — not progress. Munger may veto any build that violates it.

### BOUNDED INTERNAL FEASIBILITY PACKETS — CEO discretion, no operator round-trip

Operator directive (2026-07-25, following the `208-A` authorization): for one NARROW class of
decision, the company does not need to wait for an explicit operator
`AUTHORIZE`/`HOLD`/`ARCHIVE` reply before proceeding. That class is a single, bounded, internal,
no-code feasibility packet on one already-discovered axis, run to test acceptance/effort
boundaries — matching the shape of `docs/ceo/cycle209-208a-operator-authorization-brief.md`:
one real source + one dossier, a hard time/cost cap, manual/no-code only, no external-system
contact, and a stop-on-trigger list (protected access, scraping, external communication,
prohibited data, professional judgment, bid submission, a guarantee, code, automation, or a
reusable product component).

**When `ceo-bezos` recommends running such a packet and `critic-munger` does not veto it, treat
that as sufficient authority — proceed the same cycle, do not draft another operator
authorization brief and wait.** Log the CEO recommendation, the critic's non-veto (or veto and
why), and the packet's result in `memories/consensus.md` for auditability.

**This delegation is narrow and does NOT extend to:** any real WTP test or priced offer, any
build/code/scaffolding/repository, any outreach/listing/checkout/payment/fulfillment, any
external-system (Linear/Airtable) write, any change to the Active Validation ID, bidder-account
access or bid submission, contact with firms/authorities, or legal/accounting/engineering/tax/
certification/compliance advice. All of those still require an explicit operator directive —
this rule only removes the round-trip for the narrow internal-feasibility-packet class above.
If a proposed packet doesn't clearly fit that shape, default to drafting the operator
authorization brief as before; do not stretch this discretion to cover it.


<!-- ======== IDENTITY-WALLED PUBLIC REGISTERS (PROMPT.md, arşivlendi 2026-08-24) ======== -->

### IDENTITY-WALLED PUBLIC REGISTERS — ask instead of shrugging

Some facts the company needs are genuinely public *records* sitting behind an identity
wall it can never pass. Measured 2026-07-30 through the company's own browser, not
assumed:

- **MERSİS** (`mersis.ticaret.gov.tr`) — the landing page renders fine, but every
  company-record surface is behind `Giriş` (e-Devlet / e-imza). There is no public
  firm-search page to reach.
- **Türkiye Ticaret Sicili Gazetesi — İlan Görüntüleme**
  (`ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php`) — redirects to
  `girisyap.php`: "GİRİŞ YAPMALISINIZ. İlan görüntülemek ve ilan alımı için giriş
  yapmalısınız."
- **TTSG — Unvan Sorgulama** (`.../unvansorgulama.php`) — reachable without a login, but
  the query requires a `Güvenlik Kodu` (CAPTCHA). Solving a CAPTCHA is forbidden, so this
  is a wall too, not an opening.

The browser is not broken when you hit one of these, and re-running the search will not
help. The failure this rule exists to stop is the quiet one: recording a gate as
`NOT ESTABLISHED`, writing "no public record was found", and moving on — when the record
does exist, the operator holds a real identity, and answering would have cost them two
minutes.

**For routine registry lookups, the sanctioned path is the `Registry Bridge` queue**
(see `## REGISTRY BRIDGE QUEUE` below) — same base as the EKAP Bridge, same protocol:
you write a PENDING request, resolution happens in the operator's session, results come
back as structured evidenced fields. Verified 2026-07-30 in that session: MERSİS's
`Sorgular → Firma Sorgulama` DOES answer arbitrary-firm queries once the operator is
logged in, so a queued request is genuinely answerable.

**A `document-procurement` OPREQ remains the right channel only for what the bridge
cannot carry:** a record from a register that has no bridge lane (not MERSİS/TTSG), a
document that must arrive as an evidence FILE (a scanned gazette page, a certified
extract), or a case where the operator must exercise judgment rather than transcribe a
lookup result. Do not file an OPREQ for a lookup the bridge can express.

**Queue a request (either channel) only when all four hold** — this stays narrow, or it
becomes noise the operator learns to ignore:

1. **Decision-relevant.** Name the candidate/axis and the specific gate the answer
   unblocks, and state what you will do on each possible answer — including "the register
   shows nothing", which must be a usable answer rather than a dead end.
2. **Actually walled.** You reached the surface yourself this cycle and observed the
   login/CAPTCHA, or it is one of the registers listed above. Poor search snippets are not
   a wall — open the page in the browser first.
3. **Precisely specified.** Name the register, the exact query key (see the bridge's
   `query_key_type`), and exactly which fields you need back. Never "look this firm up
   for me."
4. **Not already asked.** Search the bridge table AND the OPREQ ledger for a prior request
   naming the same firm and the same field. Re-asking is legitimate only when new
   information changes the question, and the new request must say what changed.

Never attempt the login, never solve the CAPTCHA, and never ask for or use the operator's
own session — all of that stays forbidden exactly as before (BROWSER rule 6). The request
is the sanctioned path, not a workaround for it.


<!-- ======== WHAT AIRTABLE AND LINEAR ARE FOR (tender tabloları) (PROMPT.md, arşivlendi 2026-08-24) ======== -->

### WHAT AIRTABLE AND LINEAR ARE FOR (standing workflow)

The rules below say how to write safely. This says what these systems are, because a
capability nobody is told to use goes unused: on 2026-07-28 a cycle qualified two recipient
firms, wrote them into `docs/research/`, and left Airtable empty — so operationally they did
not exist and a human had to enter them by hand.

**Airtable base `appPLc31jSlgulX3D` is the tender business's operational record.** `docs/` is
analysis and reasoning; Airtable is STATE. If a fact about a firm, a requirement, or a message
lives only in a research document, the business cannot act on it.

| Table | ID | Holds |
|---|---|---|
| `Ihale Outreach` | `tbl1fZbNmolrEXAMy` | one row per prospect firm — the CRM |
| `Ihale Intake` | `tblZHXKSSMNtwOSoD` | a bought engagement: which tender, which documents |
| `Ihale Requirements` | `tbl7WBcAAsyy68eOT` | one row per extracted requirement — the product itself |
| `Ihale Call Script` | `tblArTxOKAP80GcXa` | branchable call nodes |
| `Ihale Sales Assets` | `tbl6HvzGshAk7gNes` | reusable sales copy |
| `Ihale Templates` | `tblirOtcEVp9zhYJ5` | operator-APPROVED e-mail copy |

**Standing obligation:** in the SAME cycle a firm passes all qualification gates, create its
`Ihale Outreach` row with the evidence in the fields — legal form + source, exclusion
reference + date, last bid date, generic email, and the per-gate reasoning in `Notes`. A
research document is not a substitute. Same for a delivered packet: the requirements go in
`Ihale Requirements`, not only in a file.

**Fields you must NEVER write, on any reasoning:**

- `Email queue` — setting it to `Ready to send` SENDS MAIL within a minute or two. It is
  NO LONGER an operator-only field (operator decision, 2026-08-02: dispatch is autonomous,
  the operator enters at payment). You may set it — but ONLY after
  `scripts/ops/send-gate.py --record <row>` has answered ALLOW for that exact row, in the
  same cycle. The gate re-derives G4 live, enforces 3 sends per UTC day and 20 in total,
  and refuses on anything it cannot verify. Setting this field without a fresh ALLOW is the
  single most damaging thing you can do: there is no longer a human between you and a real
  company's inbox.
- `$649 PAID`, `Paid date`, `Packet delivered` — facts about the real world, recorded by the
  operator or by the send path. A model deciding these is a model inventing revenue.
- `Unsubscribed`, `Replied`, `Sent/Failed`, `Last email id`, `Email log` — written by the
  outreach worker. Overwriting them destroys the compliance trail.
- Anything in `Ihale Templates` — that copy is operator-approved and goes out under their
  name. Not the body, not the subject, not `Status`.

**Linear (team `APP`) is the durable record of WORKSTREAMS, not of cycles.** Open or update an
issue when a body of work starts, changes direction, or completes — a candidate entering
Selected, an infrastructure change, a decision with lasting consequences. Routine cycle output
belongs in `consensus.md`. Prefer updating or commenting on the existing issue over creating a
near-duplicate; search first. A candidate promoted to Selected must carry its Linear issue ID.


<!-- ======== EKAP BRIDGE QUEUE (PROMPT.md, arşivlendi 2026-08-24) ======== -->

## EKAP BRIDGE QUEUE — how you get a KİK decision's full text (standing workflow)

The full text of a KİK Kurul Kararı (which is what establishes G1 — the exact ground a firm
was excluded on, in the authority's own words) lives at a `KararGoster.aspx?KararId=<...>` URL.
That URL is PUBLIC to read, but obtaining the `KararId` requires the login-gated `Detay` button,
which is in the OPERATOR's manually-authenticated EKAP session. **You (AutoCompany) never touch
that session, never log in, never get a KararId yourself.** The bridge is a data-only queue.

**The loop, three steps, only the middle one is not yours:**

1. **You WRITE a request** to Airtable table **`EKAP Bridge`** (base `appPLc31jSlgulX3D`) during
   your own research, one row per decision you have a real reason to read:
   - `request_id` (unique), `KararNo`, `selection_source`, `selection_reason`, `research_axis`,
     `status: PENDING`.
   - **`selection_source` is mandatory and must be a concrete evidenced source** — the page /
     search result / firm record where this KararNo actually appeared. It must contain, in the
     field itself, ALL of: (a) the **source URL**, (b) a **verbatim quote from that source in
     which the KararNo literally appears**, and (c) a **content hash** of the fetched source
     where one can be taken (`sha256`, first 16 hex chars is enough) — state plainly why not if
     it cannot. A request missing (a) or (b), or one that looks GUESSED, SEQUENTIAL, or like ID
     ENUMERATION (`…-1614, -1615, -1616…`), **is closed `INVALID_SOURCE` without being resolved**
     and is a protocol violation. You may only queue a KararNo you found in a real source, not
     one you incremented to.
   - **The FIRST request ever written to this queue is a production canary.** Write exactly ONE
     row and stop queueing until it has been resolved and consumed end-to-end. Not a rehearsal —
     a real KararNo you actually need, held to the full standard above.
2. **The operator-session resolver** (Claude, in the operator's live EKAP UI — NOT you, NOT this
   loop) drains PENDING requests, ≤20 per run — **exactly 1 on the canary run** — sequentially,
   and closes each with exactly one status: `PUBLIC_VERIFIED` / `LOGIN_REQUIRED` / `NOT_FOUND` /
   `SESSION_EXPIRED` / `RATE_LIMITED` / `UNRESOLVED` / `INVALID_SOURCE` (the last one is a
   rejection of YOUR request's evidence, not a site outcome — fix the source, do not re-queue the
   same weak row). **Only `PUBLIC_VERIFIED` writes back a `public_url`.** No
   cookie, token, header, localStorage, or logged-in HTML is ever written to the bridge — the
   channel carries a data-only request and, at most, a verified public URL.
3. **You READ the result.** For a `PUBLIC_VERIFIED` row, open its `public_url` with the ordinary
   session-free browser as soon as possible and save the evidence: `KararNo`, the verified
   public URL, retrieval timestamp, a **text-normalized** content hash (see below), the source
   section, and the required firm +
   ground. Then create/update the `Ihale Outreach` candidate row with `Exclusion ground` +
   `Exclusion ground source` = the authority's own decision. If the URL later fails, create a
   NEW bridge request for the same KararNo with `status: REFRESH_REQUESTED` — **never guess or
   increment a KararId.**

**Compute `content_hash` with `scripts/core/decision_text_hash.py`. Never by hand, never any
other way.**

```
python3 scripts/core/decision_text_hash.py <public_url>      # → sha256:<16hex>  chars=<n>
```

Two layers of trouble made this a shared script rather than an instruction. `KararGoster.aspx`
is an ASP.NET page whose RAW bytes differ by client (329,600 with a default `curl`, 332,091 with
a browser User-Agent, for the same decision; `__VIEWSTATE` varies on top at constant length), so
a raw-HTML hash makes two honest actors disagree every time. And "hash the extracted text" is
still not a specification — implementations differ on entity order, NBSP, and whether a dropped
tag leaves a space. On 2026-07-29 that gap quarantined a real evidence row: the resolver
published `275765205d6d63f0` for `2026/UY.II-1318` and the consumer computed something else.
Stopping was the right call; the spec was the thing at fault. Both ends now call the one file.

**A mismatch from THAT script is a real change: report it and stop.** Do not proceed on
"metadata agrees, so it is probably the same page" — matching Toplantı/Gündem/Karar No
establishes probable identity, not content integrity.

**Leak-scan bridge records with `scripts/core/bridge_leak_scan.py`. Never by word presence.**
The scanner is VALUE-SENSITIVE: it fails on a credential key together with a real value
(`Cookie: name=value`, any `Authorization`/`Proxy-Authorization` header carrying a credential —
Bearer, Basic, or a bare opaque token — `access_token=…`, a populated
localStorage/sessionStorage dump) and passes assurance sentences that merely name those words,
plus the allowed public-evidence fields (`KararId=<hex>`, `content_hash`, source hashes). A
word-presence scan flagged the 1280 record's own "no session material crossed" sentence — a
false positive is fixed by making the scan value-aware, NEVER by loosening the gate. The script
carries regression fixtures (`--selftest`, rc 3 if any fixture misbehaves): run selftest before
trusting a CLEAN verdict.

**KararId discipline:** treat every KararId as `identifier_type: OPAQUE`, `persistence: UNKNOWN`.
Different KararIds have been seen for the same decision, but that alone does NOT prove they are
ephemeral/signed — do not claim that without a controlled repeat test. Never treat a KararId as
a durable key; read the public URL promptly and keep the hash.

**Say WHY a candidate is held — the two reasons are different facts.** `Ihale Outreach → Status`
has `Held - Evidence insufficient` (you could not establish the ground, or G3/G4 are not done)
and `Held - Out of G2 window` (the ground is solid and authority-sourced, but the exclusion is
older than 12 months). Using the first for the second understates evidence you actually have.
Neither is a reason to relax a gate: an out-of-window firm stays held, `Email queue` empty.

**Classify every resolved decision BEFORE you treat anyone as a candidate** (operator decision,
2026-07-29 — G1 Integrity-Risk Classification). Read the authority text, then pick exactly one:

1. **A decision that TOUCHES a prohibited-conduct allegation** — collusion or coordinated
   bidding, a shared IP/device/account offered as evidence of coordination, bid rigging, forged
   or deliberately false documents, fraud, corruption, 4734 m.17, debarment. **Subject matter
   alone decides nothing. The authority's OUTCOME governs:**
   - authority **confirms** the violation → **`INTEGRITY-RISK QUARANTINE`**
   - authority **rejects** the allegation or **reverses** the elimination →
     **`OUT_OF_SCOPE / ELIMINATION-REVERSED`**
   - outcome sits in a **separate official process** you cannot see →
     **`STATUS-UNKNOWN / NO INFERENCE`**

   In every one of the three: no G4, no `Email queue`, no contact. But they assert very different
   things about real companies, and only the first is adverse. **Never write that misconduct was
   proven unless the competent authority expressly made that final determination** — and an
   unknown external status is not an adverse finding, it is an absence of one.

   **Quarantine is CASE-SCOPED, never a permanent mark on a legal person.** It attaches to that
   procurement and that decision. The same firm surfacing in another decision with a verified
   documentary defect is assessed there on its own merits.
2. **Normal G1–G4** — the real ground is an ordinary, remediable documentary or
   financial-qualification deficiency.
3. **`G1 NON-SERVICEABLE / NO CANDIDATE`** — tender cancellation, the complainant rather than an
   excluded bidder, an authority-side defect, or no bidder-remediable ground.
4. **`HELD / AUTHORITY MEANING UNRESOLVED`** — the text stays ambiguous. Ambiguity is a verdict
   of its own; do not resolve it by picking the reading that yields a candidate.

This is a classification-safety rule only. It authorizes no outreach, no contact-tier relaxation,
no email, no payment, no fulfilment, no build.

**A mirror is a `KararNo` discovery source and nothing else.** It is never evidence of G1, of a
firm's role, of a violation, of an elimination, or of an outcome — all of those come from the
canonical Kurul text and only from there. This is not caution, it is measurement: five of five
resolved decisions diverged from what the mirror implied. 2026/UH.II-1924 the complainant won
outright; 2025/UY.II-1098 the complainant was not among the excluded; 2026/UY.II-1318 the
complainant was reinstated; 2026/UH.II-451 was a tender CANCELLATION, not an exclusion;
2025/UM.II-1860's elimination was reversed. Never let a mirror's framing survive into a
candidate row.

**The evidence discipline still binds every row you write from this:** the `Başvuru Sahibi` is
the COMPLAINANT, NOT necessarily the excluded firm — read the decision TEXT to separate
complainant / award-winner / excluded before recording anyone; skip gerçek-kişi (persons), the
segment is legal persons; a ground rests on the authority's own decision, never a competitor
mirror. `Email queue` is yours to set ONLY behind a fresh `send-gate.py` ALLOW (see rule 7).

### TENDER TRACK STANDING RULES — the gates, in the only place they count

Every rule below was previously carried only in `memories/human-directive.md`. That file is a
SINGLE SLOT the next directive overwrites, so each of these survived purely because whoever
wrote the next directive remembered to retype it — and on 2026-07-29 a check found seven of
them present in no standing file at all. A rule that lives only in a transient slot is not a
rule; nothing errors when it evaporates. They live here now. Directives may add to them and may
not silently drop them.

1. **Segment: legal persons only.** Turkish A.Ş. / Ltd. Şti. bidders identified from public
   KİK/EKAP records, reached by cold outbound. A **gerçek kişi is out of scope even inside an
   iş ortaklığı** — take the legal-person members, leave the natural person. The
   intent-qualified pivot was rejected by the operator; do not reopen it.
2. **The four gates.** G1 = the exclusion ground, from the authority's own structured record or
   decision text. **G2 = the exclusion is within the last 12 months** — an older one cannot
   qualify however clean its ground. G3 = firm identity/legal form verified. G4 = a public
   generic corporate e-mail attributable to that exact legal person. **All four are hard.**
   Held-for-recency and held-for-missing-evidence are different facts: use
   `Held - Out of G2 window` and `Held - Evidence insufficient` accordingly.
3. **OPTION A stands** (operator authorization, `OPREQ-215TFB-CONTACT-TIER-001`, 2026-07-29):
   G4 is retained as a hard requirement and **no alternate contact tier is authorized** — no
   guessed address, no third-party directory, no different outreach channel. G4 is not the
   bottleneck; in-window authority-sourced G1 supply is.
4. **Pool shape before any first-send proposal.** Both currently qualified firms come from the
   SAME procurement (`2026/UH.II-1614`) and are both IT firms. A pool of that shape tests
   whether those two firms want this, not whether tender consultancy has demand. The pool must
   contain at least one qualified firm from a **different procurement AND a different sector**
   before a first send is proposed — and on meeting that condition, REPORT it, do not send.
   **Do NOT relax a gate to achieve that spread.** This condition is a reason to keep looking,
   never a reason to loosen G1–G4; a wide pool bought by a lowered gate measures nothing. If the
   gates will not yield spread, report the narrow pool honestly and leave it narrow.
5. **Mirrors are a `KararNo` discovery source and nothing else.** That includes the named
   competitor mirrors (`asiridusuk`, `ihaledanismani`, `ihalehatti`, `herpoz` and their like):
   fine for locating a decision number, **never** evidence of G1, of a firm's role, of a
   violation, of an elimination, or of an outcome — those come from the canonical Kurul text
   only. Record the mirror in `selection_source`, never in `Exclusion ground source`.
6. **Two hard stops on EKAP.** Do NOT reverse-engineer the signed search API (the 401
   "CryptoJs engellendi: zorunlu header eksik" endpoint) — replicating `iv`/`apiSecretKey`/`ts`
   is bot-detection evasion and is forbidden **even though competitors do it**. Do NOT attempt
   an EKAP login, and never enter the operator's authenticated session; you work session-free,
   the bridge exists precisely so you never have to.
7. **Dispatch is autonomous behind a mechanical gate; WTP is UNCHANGED.** Operator
   decision, 2026-08-02: sends and the inbox move to you, and the operator enters at
   payment. What replaced their judgement is not your own — it is
   `scripts/ops/send-gate.py`, and it is mandatory:

   - Run it per row, immediately before setting `Email queue`. ALLOW is the only permission
     to send; REFUSE and any error alike mean do not send.
   - Caps: **3 sends per UTC day, 20 in total.** They exist to bound the blast radius of a
     wrong gate, not to pace throughput. Do not work around them, do not batch to evade
     them, do not ask for them to be raised because a cohort is ready.
   - It re-derives G4 LIVE. A `G4 PASS` written in a field is a claim; with no human in the
     path, believing your own record is how a stranger gets mail they should never have got.

   **Replies:** you may read and answer them. The moment a conversation reaches price,
   payment, invoicing, a commitment or a deadline you would be bound by, STOP and raise an
   OPREQ — that is the operator's entry point and the reason it exists. Never request
   payment, issue an invoice, or accept an order.

   **WTP is untouched by all of this.** Only a real, settled payment from a real, unrelated
   buyer is WTP evidence — a test-mode transaction never is, whatever the processor. A send
   is not evidence, a reply is not evidence, and enthusiasm is not evidence.
8. **Template/asset lifecycle (operator correction, 2026-07-30).** New or revised outreach
   templates and supporting assets are created as **Draft/Pending Operator Review and stay
   there**. An operator approving a rendered PREVIEW never implicitly promotes an Airtable
   record: promotion of a new template to `Approved` — and any demotion of the template it
   supersedes — happens only on a **separate, explicit operator statement authorizing both
   actions by name**. Before asking for that statement, report the exact renders, record IDs,
   current statuses, and diffs. Follow-up (Step-2) templates must carry **no `RANDEVU_URL` or
   other operator-side-env dependency** — use a reply-based CTA (e.g. ask the recipient to
   reply with the İKN) instead of a booking link.
9. **Source hierarchy for identity and contact evidence (measured 2026-07-30).** Directories,
   Google Business/Maps listings, job boards and social pages match on a **trading name**, never
   on a legal person. Searching one candidate's own name on Maps surfaced a **different
   company's** website (`sancakgroup.com` → "Sancak Yatırım", an unrelated holding); harvesting a
   contact there would have sent "you were excluded from tender X" to a firm that was never in
   it. The hierarchy is therefore fixed:
   - **G3 is settled only by the registry** — MERSİS via the Registry Bridge, or the authority's
     own record. Nothing else establishes that the firm you found is the firm that was excluded.
   - **G4 is settled only by a first-party page that names itself.** A website is attribution
     only if the site itself states the **full legal title, or the vergi / MERSİS number**,
     matching the registry-verified record. Domain-name resemblance is not attribution.
   - **Google Business can never satisfy G4**: e-mail is not a GBP field (0 of 5 listings
     measured carried one), and claim status does not predict data quality — an *unclaimed*
     listing matched the registry address exactly while a *claimed* one did not. GBP,
     directories and social profiles are **discovery sources only**; they may surface a
     candidate's official website, and may never be cited as `Exclusion ground source` or as G4
     attribution.
   - **OR by a registry-anchored identity bridge (operator extension, 2026-07-31).** A site that
     never names itself can still satisfy G4 when a **registry datum of the exact legal person
     appears on the site itself**: the MERSİS **registered address** (mahalle/cadde/number/ilçe/il
     all matching, transliteration and abbreviation aside) or the **e-tebligat number**, published
     on a first-party page that also publishes the e-mail being harvested, on that same domain.
     Rationale: an address is the registry's own datum about the legal person, so matching it is
     verification; a brand name is not. Live case that produced this rule — N.K.Y Mimarlık:
     MERSİS `AŞAĞI ÖVEÇLER MAH. LİZBON CAD. NO: 49 ÇANKAYA/ANKARA` vs `nky.com.tr/en/contact/`
     "Lizbon Cd. No. 49 Aşağı Öveçler Çankaya Ankara", same page carrying `info@nky.com.tr`.
     **What this extension does NOT open:** a group/parent brand claiming a subsidiary
     (Seçim/DETAM stays HELD — its registered address is Ankara/Sıhhiye and no site published it);
     an award, ranking or membership, however authoritative the awarding body's own list is
     (TİM/HİB "500 Largest Service Exporters" is an inference about a brand, not a registry datum);
     a directory or job-board page reproducing a legal title (still discovery-only, per above); a
     city-level or partial address match. If the bridging datum is the address, record BOTH strings
     verbatim in the row so the next reader can re-check the match rather than trust the verdict.
   - **An address that cannot receive mail is not a channel.** Before G4 is marked passed, the
     domain must actually resolve MX. `setreinsaat.com.tr` has no A and no MX record at all, yet
     its row had passed G4 on a domain match alone. A verified identity with a dead domain is
     `Held - Evidence insufficient`, not Qualified.
   - **A first-party page that is offline today cannot be cited today.** If the site that would
     attribute the address serves nothing, the attribution is not reproducible: re-establish it
     from another first-party source (the registry's own e-tebligat record, or an archived
     capture of that same site) and record WHICH one in the row, or hold the row. Do not carry
     an attribution forward on the strength of having once seen it.
10. **Qualified is a claim you re-verify, not a state you archive (reconciliation duty).** Once
    per cycle, re-check every row currently marked `Qualified` against G1–G4 as the rules stand
    TODAY — including rule 9's source hierarchy and its MX test. A row that no longer passes is
    moved to the matching `Held - …` status with the failing gate named in its Notes, and the
    change is recorded in consensus. Rules change; rows qualified under older rules do not keep
    a grandfathered pass, and this sweep is the ONLY mechanism that applies a rule change
    retroactively. The pool is small — this costs minutes. (Added 2026-07-31 after two
    consecutive cycles ran with rule 9 in force while a `Qualified` row cited a G4 address on a
    domain with no MX record, the exact defect rule 9 names.)


<!-- ======== REGISTRY BRIDGE QUEUE (PROMPT.md, arşivlendi 2026-08-24) ======== -->

## REGISTRY BRIDGE QUEUE — Turkish trade-registry lookups (standing workflow)

Companion queue to the EKAP Bridge, same base, same trust model: table **`Registry Bridge`**
(`appPLc31jSlgulX3D` / `tblREW6MtTMTP5h5N`). It exists because MERSİS answers arbitrary-firm
queries only inside the operator's authenticated session, and every search there costs the
operator one CAPTCHA keystroke — so lookups are batched through a queue, never improvised.

**What a resolved row gives you** (all measured live 2026-07-30, Pulmotıp + 3 more): firma
durumu (Aktif / Tasfiye Halinde / Terkin Edilmiş), MERSİS no, vergi dairesi/no, ticaret sicil
no, kuruluş tarihi, firma türü, müdürlük/şehir, toplam sermaye, adres, e-tebligat adresi, and
the konkordato/iflas sub-view. That is an evidenced "this firm exists, is alive, and is
solvent" check — use it before any outreach proposal, and as the identity anchor when similar
legal names exist.

**Company side — you write PENDING requests and NOTHING else:**

- Fill `request_id` (`REGBR-YYYY-MM-DD-NNN`), `register`, `query_key_type`, `query_key`,
  `fields_needed`, `firm`, `research_axis`, `selection_reason`, `status: PENDING`.
- `selection_reason` must carry evidence of WHY this firm matters now (which candidate, which
  gate); guessed or enumeration-shaped requests are not processed.
- `fields_needed` must state what you will do with each possible answer — including
  `NOT_FOUND` and `AMBIGUOUS_MATCH`, which are first-class results, not failures.
- **Query-key rules, measured:** unvan matching is **WORD-based** — a distinctive whole word
  (`PULMOTIP`, `ARKENOM`) finds the firm; a truncated word (`PULMOT`) silently returns
  nothing; a full title also returns branches (`… TEKMER ŞUBESİ`). Never abbreviate a word,
  never trust our own records' spelling (the register wrote `PULMOTIP` where our row said
  `Pulmotıp`; `MAKİNA` where we had `Makine`). When a row comes back VERIFIED, **use its
  `mersis_no` as the durable key for every later request** (`query_key_type: MERSIS_NO`) —
  word ambiguity then disappears.
- You never set `VERIFIED`/`NOT_FOUND`/any result status, never fill result fields, and the
  result statuses only ever arrive from the operator-session resolver. Empty queue means
  empty — do not ask the operator to invent lookups.

**Resolver side (operator session only, never yours):** the operator logs in, types one
CAPTCHA per search, and the resolver reads the result, opens the konkordato/iflas sub-view,
and writes back the structured fields plus `retrieval_timestamp`/`processed_at`.
`AMBIGUOUS_MATCH` lists every candidate row verbatim in `result_data` — the resolver never
picks a winner by guesswork; disambiguation comes from an authority document naming the exact
legal person (e.g. the KİK decision text, as done for Bilgi Birikim among its three same-name
siblings on 2026-07-30).

**Who supplies what at the login screen (operator protocol, 2026-07-30 — the split is the
security property, not a formality):**

| Item | Supplied by |
|---|---|
| T.C. kimlik no | the operator's own local helper `mersis-login.py` (Keychain → form, no output) — **never the model**, under any transport |
| GSM no | the same helper, or the model directly (Keychain `com.appricode.autocompany.mersis.gsm`, account `operator`) |
| Mobil imza PIN + reading the phone challenge + approve/reject | **operator only**, on their own device |
| Güvenlik kodu / CAPTCHA on `Firma Sorgulama` | **operator only** — note this is the SEARCH form; the mobil-imza login screen has no CAPTCHA (its captcha field belongs to the username/password panel and is hidden) |
| Everything after login | model drives the search form and reads results |

So an unattended registry login does not exist and must never be claimed: the signature step
is a human act on a separate device by design, which is what keeps every session traceable to
a deliberate act of identity. The per-search CAPTCHA keeps the operator at the keyboard during
searching too — so batch the queue and spend one sitting, rather than trying to engineer the
human out of the loop.

Handling rules for the GSM value, and for any future registry secret: never echo it to
stdout, chat, a log, or a tool-call argument that gets transcribed; read it in process and
write it only into the visible field of the exact expected page after verifying URL and
HTTPS origin; **stop and fill nothing** if the URL, the fields, or the page structure differ
from expectation; never copy it into the container, a `.env`, or a remote host; never persist
a screenshot showing the ID or GSM fields; never extract cookies, tokens, headers,
localStorage or session material. Anything after login — başvuru, değişiklik, beyan, imza —
requires its own explicit authorization; "you may log in" authorizes reading, nothing else.

**Hard lines, identical to the EKAP bridge:** no cookie/token/header/localStorage/session
material ever enters this table in either direction; no login attempt, no CAPTCHA solving,
no operator-session entry by the company; masked data stays masked. A dead session is
`SESSION_EXPIRED` plus a note to the operator — never a re-login attempt.


<!-- ======== WORK CYCLE §2 Decide (discovery/tender-track dalları) (PROMPT.md, arşivlendi 2026-08-24) ======== -->

### 2. Decide

- Explicit Next Action → execute it.
- Active project → continue it, using prior outputs under `docs/*/`.
- No direction at Day 0 → CEO convenes a strategy meeting.
- Stuck → change angle, narrow scope, or ship the smallest authorized artifact.

Priority: **Ship > Plan > Discuss**, subject to the HARD STOP and other guardrails.

**An active validation or an operator-decision-pending Pending item does NOT pause discovery
BY ITSELF.** Operator correction (2026-07-26): cycles 228–230 stopped ALL work — including
fresh Opportunity Discovery — and recorded a "minimal-cost HOLD" solely because one Pending
candidate (`176-R`) was awaiting an operator `AUTHORIZE`/`HOLD`/`ARCHIVE` decision and no new
directive existed. That is over-broad. Waiting for a decision on ONE candidate, or running a
WTP test on the current Active Validation, is never by itself a reason to stop screening NEW
axes. The "do not manufacture activity" principle (from the pricing-structure gate's treadmill
guard) bars RE-ADJUDICATING THE SAME AXIS without new evidence — it does not bar generating and
screening DIFFERENT axes.

**Whether new-axis Opportunity Discovery (workflow 6) actually runs this cycle is controlled by
the injected Runtime Guardrails line 6** (`auto-loop.sh`, driven by the cockpit Settings
`DISCOVERY_ENABLED` toggle) — read it, it is the authority on this, not the paragraph above.
When it says discovery is DISABLED (the current standing default, operator decision
2026-07-27), do not scan/rank/propose brand-new candidate axes — follow `### TENDER TRACK`
below instead. When it says discovery is ENABLED, the paragraph above applies as written.
Either way, an active validation's own WTP test, an in-flight tender feasibility packet, Human
Directive handling, and OPREQ resolution-checking always continue regardless of this toggle.

### TENDER TRACK — standing focus while Opportunity Discovery is disabled

Operator direction (2026-07-27, following the `208-A` Konak infrastructure test): while
`DISCOVERY_ENABLED` is off, an idle cycle's default work is one of these two tracks, not
new-axis discovery:

1. **Tender-chasing.** Search public, no-login-required tender listing sources (EKAP and
   institutional sites — universities, municipalities, public bodies — exactly like the Konak
   discovery work already did) for a candidate that is genuinely still open. Any lawful,
   publicly accessible tender category is in scope — category is NOT an admission gate
   (operator decision, 2026-07-27; this reverses the earlier cleaning-only restriction). Before
   spending ANY analysis effort, run
   `PROJECT_EVALUATION_FRAMEWORK.md`'s mandatory tender admission pre-check (deadline-still-
   future + boundable scope) as the first two output lines — this is now a standing rule, not
   something that has to be specially requested. Use the document-processing tools
   (`python3-docx`/`python3-openpyxl`/`python3-pandas`/`soffice --headless`/`pdftotext`/
   `pdftoppm`+`tesseract -l tur` for scanned-image PDFs) and the
   requirement-to-evidence matrix methodology documented in
   `PROJECT_EVALUATION_FRAMEWORK.md`'s "İhale belge işleme" section. Stay within the same
   bounded-internal-feasibility-packet authority as `cycle209`/`cycle272`/`cycle274` — no
   purchase, no bid submission, no external contact — unless a separate explicit directive
   grants more.
2. **Active-Validation development.** If — and only if — `memories/candidate-registry.md`
   currently records an Active Validation, improve that offering (bug fixes,
   pricing/positioning, marketing, outreach, conversion work) within its existing bounded
   authority; that needs no new directive. **Read the registry for which candidate that is; do
   not carry one over from memory or from an older cycle note.** The registry is append-only
   newest-first history, so an older note can still read "X remains the sole Active Validation"
   long after X was archived — go by the most recent entry, and by dates rather than cycle
   numbers (`loop_count` resets on every redeploy). If Selected is empty, this item is simply
   not available this cycle and the Tender Track is the whole job.

**EKAP membership:** do not assume the company needs an EKAP account. Evaluate it like any
other question — most tender research (reading notices, downloading public annexes, running
feasibility packets) does not require membership; only actual bid submission does. If a cycle's
own research concludes EKAP membership has become genuinely necessary, do not register or
initiate it yourself — EKAP registration requires real operator/company identity and is an
`external-action-authorization`-type OPREQ (see `### OPERATOR ESCALATION` above): create the
request with your reasoning, then wait. Do not create this OPREQ speculatively "just in case."


<!-- ======== Candidate-registry bakım kuralları (PROMPT.md, arşivlendi 2026-08-24) ======== -->

Also maintain `memories/candidate-registry.md`: when a candidate is selected, add
it to Selected (with its Linear issue); when one is killed/closed, move it to
Archived (with the decision + one-line reason). Never silently delete an archive.

Registry archive (2026-08-03): aged maintenance notes and frozen discovery/cycle
sections get moved verbatim into `memories/registry-archive/<YYYY-MM>.md` by an
operator-run tool; `> [archived ...]` pointer lines in the registry mark each batch.
Those archive files are read-only history: never edit them, never re-inline their
content, and treat a pointer line as sufficient evidence that the history exists.
Grep the archive files only when a task genuinely needs old scan detail.

Registry note format (2026-08-04, operator rule): a maintenance note whose outcome
is NO change is exactly ONE line —
`**Cycle N note (YYYY-MM-DD): Rule-10 PASS, bridges/cohort unchanged, no candidate/axis/status change [docs/<evidence-path>]**`
— nothing more; the dated one-liner IS the "verification ran and found no drift"
evidence, and the referenced doc carries the detail. The full multi-paragraph note
format is reserved for turns where something actually CHANGED (a demotion,
promotion, new evidence, bridge event, or status edit). Rationale: "all NOTABLE
changes" is the entry bar (Keep a Changelog); a paragraph repeating "nothing
happened" buries the notes that matter and bloats the analyst's input.


<!-- ======== CONVERGENCE RULES (discovery-çağı) (PROMPT.md, arşivlendi 2026-08-24) ======== -->

## CONVERGENCE RULES (MANDATORY)

1. **Cycle 1:** Brainstorm; each agent proposes one idea; finish with a ranked top 3.
2. **Cycle 2:** Evaluate #1: critic-munger runs a pre-mortem,
   research-thompson validates the market, and cfo-campbell calculates the
   economics. Issue a framework decision.
3. **Cycle 3+:** GO → create the repo and execute instead of continuing discussion.
   NO-GO → try #2; if all fail, force-select the best remaining candidate.
   Any move into product code remains blocked by the HARD STOP above; without WTP,
   the only permitted artifact is the cheapest test that can produce it.
4. **After Cycle 2, every cycle must produce a real artifact** (file, repo,
   deployment, or WTP test). Pure discussion is forbidden.
5. **The same Next Action in two consecutive cycles** means the company is stuck;
   change the approach, narrow the scope, or ship the smallest authorized artifact.

