const els = {
  pulseDot: document.getElementById("pulseDot"),
  pulseText: document.getElementById("pulseText"),
  lastUpdate: document.getElementById("lastUpdate"),
  latency: document.getElementById("latency"),

  guardianState: document.getElementById("guardianState"),
  guardianMeta: document.getElementById("guardianMeta"),
  daemonState: document.getElementById("daemonState"),
  daemonMeta: document.getElementById("daemonMeta"),
  loopState: document.getElementById("loopState"),
  loopMeta: document.getElementById("loopMeta"),
  autostartState: document.getElementById("autostartState"),
  autostartMeta: document.getElementById("autostartMeta"),

  cardGuardian: document.getElementById("cardGuardian"),
  cardDaemon: document.getElementById("cardDaemon"),
  cardLoop: document.getElementById("cardLoop"),
  cardAutostart: document.getElementById("cardAutostart"),

  stateList: document.getElementById("stateList"),
  consensusText: document.getElementById("consensusText"),
  ideasText: document.getElementById("ideasText"),
  ideasBadge: document.getElementById("ideasBadge"),
  analystText: document.getElementById("analystText"),
  analystBadge: document.getElementById("analystBadge"),
  analystCopy: document.getElementById("analystCopy"),
  analystCopyAll: document.getElementById("analystCopyAll"),
  analystRunNow: document.getElementById("analystRunNow"),
  analystRunStatus: document.getElementById("analystRunStatus"),
  logText: document.getElementById("logText"),
  rawText: document.getElementById("rawText"),

  creditBadge: document.getElementById("creditBadge"),
  costWindow: document.getElementById("costWindow"),
  costWindowLabel: document.getElementById("costWindowLabel"),
  costTotal: document.getElementById("costTotal"),
  costLast: document.getElementById("costLast"),
  costCycles: document.getElementById("costCycles"),
  costLimits: document.getElementById("costLimits"),
  costFallbacks: document.getElementById("costFallbacks"),
  costOffloads: document.getElementById("costOffloads"),
  costBudget: document.getElementById("costBudget"),
  costEngine: document.getElementById("costEngine"),
  codexWindow: document.getElementById("codexWindow"),
  ccusageBlock: document.getElementById("ccusageBlock"),
  ccusageRange: document.getElementById("ccusageRange"),
  ccTotal: document.getElementById("ccTotal"),
  ccTotalLabel: document.getElementById("ccTotalLabel"),
  ccClaude: document.getElementById("ccClaude"),
  ccCodex: document.getElementById("ccCodex"),
  ccModels: document.getElementById("ccModels"),

  directiveInput: document.getElementById("directiveInput"),
  directiveBadge: document.getElementById("directiveBadge"),
  directiveStatus: document.getElementById("directiveStatus"),
  directiveCurrent: document.getElementById("directiveCurrent"),
  directiveUpdated: document.getElementById("directiveUpdated"),
  btnDirective: document.getElementById("btnDirective"),
  settingsForm: document.getElementById("settingsForm"),
  settingsBadge: document.getElementById("settingsBadge"),
  settingsStatus: document.getElementById("settingsStatus"),
  btnSaveSettings: document.getElementById("btnSaveSettings"),
  btnRedeploy: document.getElementById("btnRedeploy"),
  btnWake: document.getElementById("btnWake"),

  btnRefresh: document.getElementById("btnRefresh"),
  btnStart: document.getElementById("btnStart"),
  btnStop: document.getElementById("btnStop"),
  btnTail: document.getElementById("btnTail"),
  btnRaw: document.getElementById("btnRaw"),
  autoToggle: document.getElementById("autoToggle"),
  refreshInterval: document.getElementById("refreshInterval"),
};

let timer = null;
let rawVisible = false;

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderInlineMarkdown(text) {
  let html = escapeHtml(text);
  html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  return html;
}

function renderMarkdown(md) {
  const lines = String(md || "").replace(/\r\n?/g, "\n").split("\n");
  const out = [];
  let inList = false;
  let inCode = false;
  let inParagraph = false;

  const closeParagraph = () => {
    if (inParagraph) {
      out.push("</p>");
      inParagraph = false;
    }
  };
  const closeList = () => {
    if (inList) {
      out.push("</ul>");
      inList = false;
    }
  };

  for (const line of lines) {
    if (line.startsWith("```")) {
      closeParagraph();
      closeList();
      if (!inCode) {
        out.push("<pre><code>");
        inCode = true;
      } else {
        out.push("</code></pre>");
        inCode = false;
      }
      continue;
    }

    if (inCode) {
      out.push(`${escapeHtml(line)}\n`);
      continue;
    }

    if (!line.trim()) {
      closeParagraph();
      closeList();
      continue;
    }

    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      closeParagraph();
      closeList();
      const level = h[1].length;
      out.push(`<h${level}>${renderInlineMarkdown(h[2].trim())}</h${level}>`);
      continue;
    }

    const li = line.match(/^\s*[-*]\s+(.*)$/);
    if (li) {
      closeParagraph();
      if (!inList) {
        out.push("<ul>");
        inList = true;
      }
      out.push(`<li>${renderInlineMarkdown(li[1].trim())}</li>`);
      continue;
    }

    closeList();
    if (!inParagraph) {
      out.push("<p>");
      inParagraph = true;
    } else {
      out.push("<br />");
    }
    out.push(renderInlineMarkdown(line.trim()));
  }

  closeParagraph();
  closeList();
  if (inCode) {
    out.push("</code></pre>");
  }

  return out.join("");
}

function classForState(kind, state) {
  if (kind === "daemon") {
    if (state === "active") return "good";
    if (state === "inactive" || state === "not_installed" || state === "unsupported") return "warn";
    return "bad";
  }
  if (kind === "loop") {
    if (state === "running") return "good";
    if (state === "stopped") return "warn";
    return "bad";
  }
  if (kind === "guardian") {
    if (state === "running") return "good";
    if (state === "stopped" || state === "unsupported") return "warn";
    return "bad";
  }
  if (kind === "autostart") {
    if (state === "configured") return "good";
    if (state === "not_configured" || state === "unsupported") return "warn";
    return "bad";
  }
  return "warn";
}

function applyCardState(card, kind, state) {
  card.classList.remove("good", "warn", "bad");
  card.classList.add(classForState(kind, state));
}

function formatTime(isoText) {
  try {
    return new Date(isoText).toLocaleString();
  } catch {
    return isoText;
  }
}

function renderStateList(parsed, stateFile, router) {
  router = router || {};
  const routed = (router.routedEngine || "").toUpperCase();
  const routedModel = router.routedModel
    ? router.routedModel + (router.routedEffort ? ` · effort ${router.routedEffort}` : "")
    : "-";
  const ladder = (arr) => (Array.isArray(arr) && arr.length ? arr.join(" → ") : "-");
  const budgetInterval = `$${router.windowBudget || "-"} cap · ${router.interval || "-"}s`;

  const rows = [
    ["Active engine (routed)", routed || "-"],
    ["Active model", routedModel],
    ["Router decision", router.routerReason || "-"],
    ["Tier selection", router.tierMode || "-"],
    ["Claude ladder (cheap→capable)", ladder(router.claudeLadder)],
    ["Codex effort ladder", ladder(router.codexLadder)],
    ["Base engine / model", `${parsed.loop.engine || "-"} / ${parsed.loop.model || "-"}`],
    ["Budget / interval", budgetInterval],
    ["Loop Count", parsed.loop.loopCount || stateFile.LOOP_COUNT || "-"],
    ["Error Count", parsed.loop.errorCount || stateFile.ERROR_COUNT || "-"],
    ["Last Run", parsed.loop.lastRun || stateFile.LAST_RUN || "-"],
    ["Daemon ActiveState", parsed.daemon.activeState || "-"],
  ];

  els.stateList.innerHTML = rows
    .map(([k, v]) => `<div><dt>${k}</dt><dd>${String(v)}</dd></div>`)
    .join("");
}

async function fetchStatus() {
  const started = performance.now();
  const res = await fetch("/api/status", { cache: "no-store" });
  const data = await res.json();
  const elapsed = Math.round(performance.now() - started);

  const parsed = data.parsed || {};
  const guardian = parsed.guardian || {};
  const daemon = parsed.daemon || {};
  const loop = parsed.loop || {};
  const autostart = parsed.autostart || {};

  els.guardianState.textContent = (guardian.state || "unknown").toUpperCase();
  els.guardianMeta.textContent = guardian.pid ? `PID ${guardian.pid}` : "PID --";
  applyCardState(els.cardGuardian, "guardian", guardian.state);

  els.daemonState.textContent = (daemon.state || "unknown").toUpperCase();
  els.daemonMeta.textContent = daemon.mainPid ? `MainPID ${daemon.mainPid}` : "MainPID --";
  applyCardState(els.cardDaemon, "daemon", daemon.state);

  els.loopState.textContent = (loop.state || "unknown").toUpperCase();
  const loopCycle = loop.loopCount ? `Cycle ${loop.loopCount}` : "Cycle --";
  const loopPid = loop.pid ? `PID ${loop.pid}` : "PID --";
  els.loopMeta.textContent = `${loopCycle} | ${loopPid}`;
  applyCardState(els.cardLoop, "loop", loop.state);

  els.autostartState.textContent = (autostart.state || "unknown").toUpperCase();
  els.autostartMeta.textContent = autostart.raw || "Autostart";
  applyCardState(els.cardAutostart, "autostart", autostart.state);

  renderStateList(parsed, data.stateFile || {}, data.router || {});
  setWakeAvailability(data.stateFile || {});

  const consensusRaw = (data.consensusHead || parsed.consensusPreview || "(no consensus)").trim();
  els.consensusText.innerHTML = renderMarkdown(consensusRaw);
  els.logText.textContent = (data.logTail || parsed.recentLog || "(no logs yet)").trim();
  els.rawText.textContent = data.raw || "";

  const healthy = data.ok && loop.state === "running" && daemon.state === "active";
  els.pulseText.textContent = healthy ? "Live Link: STABLE" : "Live Link: ATTENTION";
  els.pulseDot.style.background = healthy ? "var(--good)" : "var(--warn)";

  renderDirective(data.directive || {});
  renderCost(data.cost || {});
  applyHostControls(data.hostKind);

  els.lastUpdate.textContent = `Last update: ${formatTime(data.timestamp)}`;
  els.latency.textContent = `Roundtrip: ${elapsed}ms`;
}

function renderCost(cost) {
  const usd = (n) => `$${(Number(n) || 0).toFixed(2)}`;
  els.costWindow.textContent = usd(cost.windowUsd);
  els.costWindowLabel.textContent = cost.windowBudget
    ? `5h window / $${cost.windowBudget} cap`
    : "5h window";
  els.costTotal.textContent = usd(cost.totalUsd);
  els.costLast.textContent = usd(cost.lastUsd);
  els.costCycles.textContent = cost.cycles ?? 0;
  els.costLimits.textContent = cost.limitHits ?? 0;
  els.costFallbacks.textContent = cost.fallbackHits ?? 0;
  els.costOffloads.textContent = cost.budgetOffloads ?? 0;
  els.costBudget.textContent = cost.budgetPauses ?? 0;
  els.costEngine.textContent = (cost.engine || "—").toUpperCase();
  els.codexWindow.textContent = cost.codexWindow ?? 0;

  renderCcusage(cost.ccusage || {});

  const reason = (cost.creditReason || "").trim();
  if (reason === "out_of_credits") {
    // Pay-as-you-go OVERFLOW credits are off — expected under the cost cap. The
    // company runs on the Max subscription window, so this is informational, not
    // a failure. Health is whether cycles keep completing (see Loop/Cost above).
    els.creditBadge.textContent = "SUBSCRIPTION ONLY";
    els.creditBadge.className = "badge badge-none";
    els.creditBadge.title =
      "No pay-as-you-go extra credits (overflow off — intended). Cycles run on the Max plan window.";
  } else if (reason) {
    els.creditBadge.textContent = reason.toUpperCase();
    els.creditBadge.className = "badge badge-pending";
    els.creditBadge.title = "";
  } else {
    els.creditBadge.textContent = "OK";
    els.creditBadge.className = "badge badge-done";
    els.creditBadge.title = "";
  }
}

function renderCcusage(cc) {
  if (!els.ccusageBlock) return;
  const usd = (n) => `$${(Number(n) || 0).toFixed(2)}`;
  if (!cc.available) {
    // Fail open: hide the block when ccusage isn't installed / still computing.
    els.ccusageBlock.hidden = true;
    return;
  }
  els.ccusageBlock.hidden = false;
  els.ccTotal.textContent = usd(cc.totalCost);
  els.ccTotalLabel.textContent = cc.days ? `Total (${cc.days}d)` : "Total";
  els.ccClaude.textContent = usd(cc.claudeCost);
  els.ccCodex.textContent = usd(cc.codexCost);
  els.ccusageRange.textContent = cc.today && cc.today.date
    ? `${cc.today.date} · ${usd(cc.today.cost)}`
    : "";
  const models = Array.isArray(cc.models) ? cc.models : [];
  els.ccModels.textContent = models.length
    ? models.map((m) => `${m.name} ${usd(m.cost)}`).join(" · ")
    : "—";
}

let hostControlsApplied = false;
function applyHostControls(hostKind) {
  if (hostControlsApplied || hostKind !== "linux") return;
  // In the container the loop is a child of the entrypoint, managed by Coolify —
  // Start/Stop map to a no-op here. Disable them and point at Settings → Redeploy.
  for (const b of [els.btnStart, els.btnStop]) {
    b.disabled = true;
    b.title = "Managed by Coolify in the container. Use Settings → Save & Redeploy.";
    b.classList.add("btn-disabled");
  }
  hostControlsApplied = true;
}

function renderDirective(directive) {
  const status = (directive.status || "NONE").toUpperCase();
  els.directiveBadge.textContent = status;
  els.directiveBadge.className = `badge badge-${status.toLowerCase()}`;

  if (directive.present && directive.directive) {
    els.directiveCurrent.textContent = directive.directive;
    els.directiveUpdated.textContent = directive.updated
      ? `updated ${formatTime(directive.updated)}`
      : "";
  } else {
    els.directiveCurrent.textContent = "(none)";
    els.directiveUpdated.textContent = "";
  }
}

async function submitDirective() {
  const text = els.directiveInput.value.trim();
  if (!text) {
    els.directiveStatus.textContent = "Type a directive first.";
    return;
  }
  const label = els.btnDirective.textContent;
  els.btnDirective.disabled = true;
  els.btnDirective.textContent = "Sending...";
  els.directiveStatus.textContent = "";
  try {
    const res = await fetch("/api/directive", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ directive: text }),
    });
    const data = await res.json();
    if (!res.ok || !data.ok) {
      throw new Error(data.error || "Failed to send directive");
    }
    els.directiveInput.value = "";
    els.directiveStatus.textContent = "Directive sent — the next cycle will pick it up.";
    renderDirective(data.directive || {});
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    els.directiveStatus.textContent = msg;
  } finally {
    els.btnDirective.disabled = false;
    els.btnDirective.textContent = label;
  }
}

function renderSettings(settings) {
  const spec = settings.spec || [];
  const values = settings.values || {};
  els.settingsForm.innerHTML = "";
  for (const s of spec) {
    const row = document.createElement("label");
    row.className = "settings-row";
    const cur = values[s.key] ?? "";
    const labelHtml = `<span class="settings-label">${s.label}<code>${s.key}</code></span>`;
    if (s.type === "bool") {
      row.innerHTML = `${labelHtml}<input type="checkbox" data-key="${s.key}" ${
        cur === "1" ? "checked" : ""
      } />`;
    } else {
      row.innerHTML = `${labelHtml}<input type="${
        s.type === "number" ? "text" : "text"
      }" data-key="${s.key}" value="${String(cur).replace(/"/g, "&quot;")}" placeholder="(default)" />`;
    }
    els.settingsForm.appendChild(row);
  }
}

function gatherSettings() {
  const out = {};
  els.settingsForm.querySelectorAll("[data-key]").forEach((el) => {
    const key = el.getAttribute("data-key");
    out[key] = el.type === "checkbox" ? (el.checked ? "1" : "0") : el.value.trim();
  });
  return out;
}

let ideasLoaded = false;
async function loadIdeas() {
  try {
    const res = await fetch("/api/ideas", { cache: "no-store" });
    const data = await res.json();
    ideasLoaded = true;
    if (data && data.present) {
      els.ideasText.innerHTML = renderMarkdown(data.markdown || "");
      els.ideasBadge.textContent = "LOADED";
      els.ideasBadge.classList.remove("badge-none");
    } else {
      els.ideasText.textContent = "(no opportunity-scan.md yet)";
    }
  } catch (err) {
    ideasLoaded = false;
    els.ideasText.textContent = "Failed to load ideas — will retry when you close and reopen this panel.";
  }
}

let analystLoaded = false;
let analystRaw = "";
async function loadAnalysis() {
  try {
    const res = await fetch("/api/analysis", { cache: "no-store" });
    const data = await res.json();
    // Only latch the loaded flag on SUCCESS: it used to be set at the call
    // site before the fetch resolved, so one transient failure (e.g. the panel
    // expanded during a container swap) stuck as "Failed to load analysis."
    // until a full page reload, even though the backend was healthy.
    analystLoaded = true;
    if (data && data.present) {
      analystRaw = data.markdown || "";
      els.analystText.innerHTML = renderMarkdown(analystRaw);
      els.analystBadge.textContent = "LOADED";
      els.analystBadge.classList.remove("badge-none");
    } else {
      els.analystText.textContent = "(no analysis yet — the Codex analyst cron has not run)";
    }
    renderAnalystTrigger(data && data.trigger);
  } catch (err) {
    analystLoaded = false;
    els.analystText.textContent = "Failed to load analysis — will retry when you close and reopen this panel.";
  }
}

// On-demand run lifecycle, from the host watcher's volume markers. The button is a
// courtesy — the server refuses doubles, the host flock is the real guard.
function renderAnalystTrigger(trigger) {
  if (!els.analystRunStatus) return;
  if (!trigger) { els.analystRunStatus.textContent = ""; return; }
  if (trigger.running) {
    els.analystRunStatus.textContent = `Analyst run IN FLIGHT (${trigger.running_info || "no info"})`;
    els.analystRunNow.disabled = true;
  } else if (trigger.pending) {
    els.analystRunStatus.textContent = "Run request QUEUED — the host watcher fires within 5 minutes.";
    els.analystRunNow.disabled = true;
  } else {
    els.analystRunStatus.textContent = trigger.last ? `Last on-demand run: ${trigger.last}` : "";
    els.analystRunNow.disabled = false;
  }
}

async function runAnalystNow() {
  if (!window.confirm("Queue an Opportunity Analyst run now? Starts within 5 minutes, takes ~15 minutes, costs ~$23.")) return;
  const label = els.analystRunNow.textContent;
  els.analystRunNow.disabled = true;
  els.analystRunNow.textContent = "Queuing...";
  try {
    const res = await fetch("/api/analyst/run", { method: "POST" });
    const data = await res.json();
    els.analystRunStatus.textContent = data.ok
      ? data.message
      : `Refused: ${data.error || "unknown reason"}`;
  } catch (err) {
    els.analystRunStatus.textContent = err instanceof Error ? err.message : String(err);
  } finally {
    els.analystRunNow.textContent = label;
    loadAnalysis().catch(() => {});
  }
}

// Extract just the paste-ready directive from the analyst report: the last fenced
// ```md / ```markdown block that looks like a directive; strip a leading
// "# Human Directive" line (the Director panel re-wraps it). Falls back to the
// "Paste-ready" section, then the whole report.
function extractDirective(md) {
  if (!md) return "";
  const fences = [...md.matchAll(/```(?:md|markdown)?\s*\n([\s\S]*?)```/g)];
  for (let i = fences.length - 1; i >= 0; i--) {
    const b = fences[i][1];
    if (/human directive|##\s*decision|##\s*authorization|##\s*directive|status:/i.test(b)) {
      return b.replace(/^\s*#\s*Human Directive\s*\n/i, "").trim();
    }
  }
  const m = md.match(/##\s*10\.[\s\S]*/);
  if (m) return m[0].trim();
  return md.trim();
}

async function copyToBtn(btn, text) {
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
    const prev = btn.textContent;
    btn.textContent = "Copied";
    setTimeout(() => { btn.textContent = prev; }, 1500);
  } catch (e) {}
}

if (els.analystCopy) {
  els.analystCopy.addEventListener("click", () => copyToBtn(els.analystCopy, extractDirective(analystRaw)));
}
if (els.analystCopyAll) {
  els.analystCopyAll.addEventListener("click", () => copyToBtn(els.analystCopyAll, analystRaw));
}
if (els.analystRunNow) {
  els.analystRunNow.addEventListener("click", runAnalystNow);
}

// Director panel: copy-to-clipboard directive templates (served from
// dashboard/directive-templates/*.md). Copy → paste into the box above → Send.
async function loadDirectiveTemplates() {
  const holder = document.getElementById("directiveTemplates");
  if (!holder) return;
  try {
    const res = await fetch("/api/directive-templates");
    const data = await res.json();
    const tpls = (data && data.templates) || [];
    holder.innerHTML = "";
    if (!tpls.length) {
      holder.innerHTML = '<span class="muted mono">(no templates)</span>';
      return;
    }
    tpls.forEach((t) => {
      const b = document.createElement("button");
      b.className = "tpl-btn";
      b.textContent = t.label;
      if (t.hint) b.title = t.hint;
      b.addEventListener("click", () => copyToBtn(b, t.text));
      holder.appendChild(b);
    });
  } catch (e) {
    holder.innerHTML = '<span class="muted mono">(templates unavailable)</span>';
  }
}
loadDirectiveTemplates();

async function loadSettings() {
  try {
    const res = await fetch("/api/settings");
    const data = await res.json();
    renderSettings(data);
  } catch (err) {
    els.settingsForm.innerHTML = `<p class="muted">Failed to load settings.</p>`;
  }
}

async function saveSettings(withRedeploy) {
  els.btnSaveSettings.disabled = true;
  els.btnRedeploy.disabled = true;
  els.settingsStatus.textContent = "Saving...";
  try {
    const res = await fetch("/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ values: gatherSettings() }),
    });
    const data = await res.json();
    if (!res.ok || !data.ok) throw new Error(data.error || "Save failed");
    renderSettings(data.settings || {});
    els.settingsStatus.textContent = "Saved. Applies after redeploy/restart.";
    if (withRedeploy) {
      els.settingsStatus.textContent = "Saved. Triggering redeploy...";
      const rd = await fetch("/api/redeploy", { method: "POST" });
      const rdData = await rd.json();
      els.settingsStatus.textContent =
        rd.ok && rdData.ok
          ? "Redeploy triggered — new config applies once it lands."
          : `Saved, but redeploy: ${rdData.error || "failed"}`;
    }
  } catch (err) {
    els.settingsStatus.textContent = err instanceof Error ? err.message : String(err);
  } finally {
    els.btnSaveSettings.disabled = false;
    els.btnRedeploy.disabled = false;
  }
}

// "Run cycle now" ends the sleep between cycles. It is enabled ONLY while the loop
// is idle: during a running cycle there is nothing to wake, and the only sleep alive
// then is the cycle-timeout watchdog, which must not be touched. The server enforces
// this too — the button state is a courtesy, not the guard.
function setWakeAvailability(stateFile) {
  const status = String((stateFile && stateFile.STATUS) || "").toLowerCase();
  const sleeping = status === "idle";
  els.btnWake.disabled = !sleeping;
  els.btnWake.title = sleeping
    ? "Loop is sleeping — start the next cycle now."
    : `Loop is ${status || "in an unknown state"} — nothing to wake.`;
}

async function wakeLoop() {
  const label = els.btnWake.textContent;
  els.btnWake.disabled = true;
  els.btnWake.textContent = "Waking...";
  try {
    const res = await fetch("/api/wake", { method: "POST" });
    const data = await res.json();
    els.settingsStatus.textContent =
      res.ok && data.ok
        ? "Cycle starting now — the wait was ended, LOOP_INTERVAL is unchanged."
        : `Wake refused: ${data.error || "unknown reason"}`;
  } catch (err) {
    els.settingsStatus.textContent = err instanceof Error ? err.message : String(err);
  } finally {
    els.btnWake.textContent = label;
    fetchStatus().catch(() => {});
  }
}

async function runAction(action) {
  const btn = action === "start" ? els.btnStart : els.btnStop;
  const label = btn.textContent;
  btn.disabled = true;
  btn.textContent = `${label}...`;
  try {
    const res = await fetch(`/api/action/${action}`, { method: "POST" });
    const data = await res.json();
    if (!res.ok || !data.ok) {
      throw new Error(data.output || `Action ${action} failed`);
    }
    await fetchStatus();
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    alert(msg);
  } finally {
    btn.disabled = false;
    btn.textContent = label;
  }
}

function resetAutoTimer() {
  if (timer) {
    clearInterval(timer);
    timer = null;
  }
  if (els.autoToggle.checked) {
    timer = setInterval(() => {
      fetchStatus().catch(() => {});
    }, Number(els.refreshInterval.value));
  }
}

els.btnRefresh.addEventListener("click", () => fetchStatus().catch(() => {}));
els.btnStart.addEventListener("click", () => runAction("start"));
els.btnStop.addEventListener("click", () => runAction("stop"));
els.btnWake.addEventListener("click", () => wakeLoop());
els.btnTail.addEventListener("click", () => fetchStatus().catch(() => {}));
els.btnRaw.addEventListener("click", () => {
  rawVisible = !rawVisible;
  els.rawText.classList.toggle("hidden", !rawVisible);
});
els.btnDirective.addEventListener("click", () => submitDirective());
els.btnSaveSettings.addEventListener("click", () => saveSettings(false));
els.btnRedeploy.addEventListener("click", () => saveSettings(true));

// Collapsible panels (Settings, Current directive) — default collapsed via markup.
document.querySelectorAll(".collapse-toggle").forEach((btn) => {
  btn.addEventListener("click", () => {
    const target = document.getElementById(btn.getAttribute("data-target"));
    if (!target) return;
    const collapsed = target.classList.toggle("collapsed");
    btn.setAttribute("aria-expanded", String(!collapsed));
    if (btn.getAttribute("data-target") === "ideasBody" && !collapsed && !ideasLoaded) {
      loadIdeas().catch(() => {});
    }
    if (btn.getAttribute("data-target") === "analystBody" && !collapsed && !analystLoaded) {
      loadAnalysis().catch(() => {});
    }
  });
});
// --- Requests to you (operator requests) -------------------------------------------
// Answers go to memories/operator-decisions.md, NOT to the directive slot, so replying
// here can never overwrite a directive the loop is mid-way through executing.
const AUTH_LABELS = ["System", "Action", "Target", "Limit"];
const opreqEls = {
  list: document.getElementById("opreqList"),
  badge: document.getElementById("opreqBadge"),
};

function renderOperatorRequests(payload) {
  const open = (payload && payload.open) || [];
  opreqEls.badge.textContent = String(open.length);
  opreqEls.badge.className = `badge badge-${open.length ? "pending" : "none"}`;

  if (!open.length) {
    opreqEls.list.innerHTML = '<p class="muted mono">Nothing waiting on you.</p>';
    return;
  }

  opreqEls.list.innerHTML = open
    .map((req) => {
      const fields = req.authorizable
        ? AUTH_LABELS.map(
            (label) => `
          <label class="opreq-field">
            <span class="opreq-field-label">${label}</span>
            <textarea rows="2" data-field="${label}">${escapeHtml(
              (req.proposed && req.proposed[label]) || ""
            )}</textarea>
          </label>`
          ).join("")
        : `<p class="muted">This request type is not answered with an authorization block.
             Refuse it here, or answer it in a directive.</p>`;
      const authBtn = req.authorizable
        ? `<button class="btn btn-start" data-act="authorize">Authorize</button>`
        : "";
      return `
      <article class="opreq-card" data-id="${escapeHtml(req.id)}">
        <div class="opreq-head">
          <span class="mono opreq-id">${escapeHtml(req.id)}</span>
          <span class="muted mono">${escapeHtml(req.type)} · blocks ${escapeHtml(
        req.blockedScope || "—"
      )}</span>
        </div>
        <p class="opreq-question">${escapeHtml(req.requiredInput)}</p>
        <details class="opreq-form" ${req.authorizable ? "" : "open"}>
          <summary>Proposed authorization — read and edit before approving</summary>
          ${fields}
        </details>
        <label class="opreq-field">
          <span class="opreq-field-label">Reason (refusal only)</span>
          <textarea rows="1" data-reason="1" placeholder="why you are declining"></textarea>
        </label>
        <div class="director-actions">
          ${authBtn}
          <button class="btn btn-stop" data-act="refuse">Refuse</button>
          <span class="muted mono" data-status="1"></span>
        </div>
      </article>`;
    })
    .join("");

  opreqEls.list.querySelectorAll("button[data-act]").forEach((btn) => {
    btn.addEventListener("click", () => submitDecision(btn));
  });
}

async function submitDecision(btn) {
  const card = btn.closest(".opreq-card");
  const statusEl = card.querySelector("[data-status]");
  const decision = btn.getAttribute("data-act");
  const fields = {};
  AUTH_LABELS.forEach((label) => {
    const box = card.querySelector(`[data-field="${label}"]`);
    fields[label] = box ? box.value : "";
  });
  const reasonBox = card.querySelector("[data-reason]");

  card.querySelectorAll("button").forEach((b) => (b.disabled = true));
  statusEl.textContent = "Recording…";
  try {
    const res = await fetch("/api/operator-decision", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: card.getAttribute("data-id"),
        decision,
        fields,
        reason: reasonBox ? reasonBox.value : "",
      }),
    });
    const data = await res.json();
    if (!res.ok || !data.ok) throw new Error(data.error || "Failed to record decision");
    // Deliberately NOT a full re-render. The request legitimately stays OPEN until the
    // company's own verifier moves it, so redrawing the list would replace this card
    // with an identical one and silently erase the confirmation — the operator would
    // reasonably click again and append a duplicate decision.
    card.classList.add("opreq-answered");
    statusEl.textContent =
      decision === "authorize"
        ? "Authorized — recorded. The company applies it on its next cycle."
        : "Refused — recorded. The company will take no action on this.";
  } catch (err) {
    statusEl.textContent = err instanceof Error ? err.message : String(err);
    card.querySelectorAll("button").forEach((b) => (b.disabled = false));
  }
}

async function loadOperatorRequests() {
  try {
    const res = await fetch("/api/operator-requests");
    renderOperatorRequests(await res.json());
  } catch {
    opreqEls.list.innerHTML = '<p class="muted mono">(requests unavailable)</p>';
  }
}

els.autoToggle.addEventListener("change", resetAutoTimer);
els.refreshInterval.addEventListener("change", resetAutoTimer);
loadOperatorRequests().catch(() => {});

fetchStatus().catch((err) => {
  const msg = err instanceof Error ? err.message : String(err);
  els.rawText.textContent = msg;
});
loadSettings().catch(() => {});
resetAutoTimer();
