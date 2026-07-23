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

function renderStateList(parsed, stateFile) {
  const rows = [
    ["Engine", parsed.loop.engine || "-"],
    ["Model", parsed.loop.model || "-"],
    ["Loop Count", parsed.loop.loopCount || stateFile.LOOP_COUNT || "-"],
    ["Error Count", parsed.loop.errorCount || stateFile.ERROR_COUNT || "-"],
    ["Last Run", parsed.loop.lastRun || stateFile.LAST_RUN || "-"],
    ["Loop Daemon Summary", parsed.loop.daemonSummary || "-"],
    ["Daemon ActiveState", parsed.daemon.activeState || "-"],
    ["Daemon SubState", parsed.daemon.subState || "-"],
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

  renderStateList(parsed, data.stateFile || {});

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
    if (data && data.present) {
      els.ideasText.innerHTML = renderMarkdown(data.markdown || "");
      els.ideasBadge.textContent = "LOADED";
      els.ideasBadge.classList.remove("badge-none");
    } else {
      els.ideasText.textContent = "(no opportunity-scan.md yet)";
    }
  } catch (err) {
    els.ideasText.textContent = "Failed to load ideas.";
  }
}

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
      ideasLoaded = true;
      loadIdeas().catch(() => {});
    }
  });
});
els.autoToggle.addEventListener("change", resetAutoTimer);
els.refreshInterval.addEventListener("change", resetAutoTimer);

fetchStatus().catch((err) => {
  const msg = err instanceof Error ? err.message : String(err);
  els.rawText.textContent = msg;
});
loadSettings().catch(() => {});
resetAutoTimer();
