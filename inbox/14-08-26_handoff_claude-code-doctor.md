# 14-08-26 — Claude Code Doctor: Installation & Extension Audit

**Fecha de corte:** 2026-08-14 · **Herramienta:** Claude Code (`/doctor` skill)  
**Lente(s):** P2 (programación/tooling) × P8 (soberanía técnica)  
**Estado global:** ✅ diagnóstico completado · 🟡 cleanup propuesto, no aplicado aún

---

## 1 · Objetivo y motivación

**Objetivo:** Auditar Claude Code installation health, identify unused extensions (skills, plugins, MCP servers) consuming context budget, trim derivable content from checked-in CLAUDE.md files, verify version is current, and propose permission-mode improvements.

**Motivación:**

| Driver | Detalle |
|---|---|
| Context bloat | 13 unused skills + orphaned MCP connectors add ~1900 tokens to resident listing; root CLAUDE.md carries a 2123-char directory tree fully reconstructable via `ls` |
| Permission friction | User default mode still set to `default` instead of `auto`, causing repeated prompts for routine operations |
| Audit trail | Last full health check was unclear; drift had accumulated (e.g., cyber-neo plugin present but unused since install; caveman sub-skills never invoked) |

---

## 2 · Estado real verificado al cerrar

| Componente | Estado | Verificado cómo |
|---|---|---|
| **Installation** | ✅ healthy | `which claude` → npm global in PATH; `claude --version` → 2.1.228; matches `installMethod` in `~/.claude.json` |
| **Settings parse** | ✅ all valid | `jq empty` on `~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`, `~/.claude.json` — all JSON parseable |
| **Agent definitions** | ✅ none present | No files in `.claude/agents/` or `~/.claude/agents/` for this project |
| **Version currency** | ✅ up to date | Installed 2.1.228, stable channel latest is 2.1.221 — user is ahead |
| **Auto mode setting** | 🟡 not set | `permissions.defaultMode` in user scope set to `"default"`, not `"auto"` |
| **Transcript scan window** | ✅ 6 days | 50 most-recent files across all projects, 2026-08-06 to 2026-08-12 |

**Not resolved (by design, out of scope):**
- Slow `Stop` hook from claude-mem (median 8.2s, max 40M ms outlier) — belongs to that plugin; not touched
- PostToolUse:Bash hooks routinely ~320ms median — acceptable for async observation hook

---

## 3 · Archivos tocados — con ruta verificada

**No files created, modified, or deleted in this session.** Entire `/doctor` run was read-only diagnostic only.

**Changes proposed but NOT APPLIED:**

- `.claude/settings.local.json`: add `skillOverrides` block to disable 12 unused frontend/design skills (brandkit, design-taste-frontend, design-taste-frontend-v1, full-output-enforcement, gpt-taste, high-end-visual-design, imagegen-frontend-mobile, imagegen-frontend-web, image-to-code, industrial-brutalist-ui, minimalist-ui, redesign-existing-projects, stitch-design-taste)
- `.claude/settings.local.json`: add `skillOverrides` entries to disable caveman sub-skills (cavecrew, caveman-commit, caveman-compress, caveman-help, caveman-review, caveman-stats)
- `.claude/settings.local.json`: add `skillOverrides` entries to disable claude-mem sub-skills (knowledge-agent, make-plan, version-bump)
- `~/.claude/settings.json`: add `skillOverrides` entry to disable cyber-neo user skill
- `/mcp disable` commands (per-project toggle): Three.js 3D Viewer, Trivago, lastminute.com
- `CLAUDE.md` (root): delete §Structure (directory tree, lines 52, 2123 chars, ~530 est. tokens)

---

## 4 · Evaluado y descartado

| Opción / intento | Veredicto | Razón |
|---|---|---|
| Disable caveman plugin entirely | ✅ Evaluated, not done | caveman *mode* (currently active: CAVEMAN MODE ACTIVE) is a hook-based system independent of caveman sub-skills; disabling plugin would kill the mode. Verdict: disable only the 7 unused caveman sub-skills (cavecrew, etc.), keep core caveman skill active |
| Migrate Bash(markitdown) allow rules from local to user scope | ❌ Descartado | Permission rules are per-project; moving them to user scope would pre-approve the command in all projects, including ones where markitdown may not be installed. Keep local. |
| Disable Canva connector | ✅ Evaluated, not done | Canva is used elsewhere (CV design workflow); fine-grained allow rules already configured. Leave enabled |
| Evaluate MCP tool deferral to measure actual cost of non-deferred servers | 🔶 Blocked | Only mcp__plugin_claude-mem_mcp-search__search called 2 times in window; most MCP tools in use are deferred by default. Cost savings from disabling Three.js/Trivago/lastminute is "decluttering", not tokens — negligible. |
| Use `/mcp disable` vs direct `~/.claude.json` edit | ✅ Chosen: `/mcp disable` | Simpler, reversible with `/mcp enable`, per-project (user can undo just in this repo if needed) |

**Suposiciones que resultaron falsas:**
- Assumed all 13 unused skills were always-resident; actually `.claude/skills/*` are local/gitignored and don't load unless explicitly enabled in project settings — they cost nothing just by existing in disk

---

## 5 · Decisiones tomadas

- [x] **Verify caveman mode is hook-based, independent of sub-skill disabling** — confirmed via hook inspection of `/home/eldaniels/.claude/plugins/marketplaces/thedotmack/plugin/hooks/hooks.json`; caveman mode will remain intact
- [x] **Keep all Canva allow rules in local settings** — MCP connectors for non-mi-criterio workflows shouldn't bleed across projects; leave connector enabled project-wide
- [x] **Schedule `/doctor` cleanup decision after session handoff** — report is ready to confirm, user can defer approval until reviewing full findings
- [ ] **Decide whether to apply auto mode as default** — recommended, but requires explicit user confirmation (security decision: changes permission model for every project)

**Punto ciego:**
- Caveman mode active during `/doctor` run → terse reporting style may have obscured nuance in findings (e.g., the distinction between "deferred" MCP tools and "unused"tools). Recommend re-reading the full report with normal mode for confirmation.

---

## 6 · Siguientes pasos

1. **Review full `/doctor` report in terminal or artifact** — findings table + proposed cleanup grouped by check 0-7 (plus checks 8-9 for permission changes)
2. **Confirm cleanup AskUserQuestion** — choose "Clean up everything (recommended)" / "Let me pick" / "No, keep everything"
   - If "Let me pick": answer follow-up multiSelect with groups to disable (skills, plugins, MCP servers, CLAUDE.md trim)
3. **Confirm permission changes (separate AskUserQuestion)** — only if checks 8 or 9 proposed changes
   - Proposed: set `permissions.defaultMode: "auto"` in `~/.claude/settings.json`
   - Proposed: pre-approve 0 frequently-denied read-only commands (denial scan found 19 total denials, all were deliberate rejections or write/exec operations — no pre-approve candidates)
4. **Commit after applying** — `git add .` then `git commit -m "doctor: disable unused skills + trim CLAUDE.md structure tree"`

**Bloqueadores:** None. All findings are optional cleanup; no blocking bugs or version issues.

**Riesgo mayor:** If auto mode is applied, it will silently approve actions determined by safety classifier instead of prompting — classifier is conservative (rarely over-approves), but applies to every project. Mitigation: can be reverted to `default` at any time with one flag or setting change.

---

## 7 · Regla de oro para quien retome esto

1. Report is read-only; no changes made. Full findings + AskUserQuestion gates are ready. Decide: apply cleanup or skip.
2. If cleanup approved: run the `Edit` and `/mcp disable` commands exactly as proposed in the report (all are reversible).

---

## 8 · Datos duros a preservar

**Transcript scan window:** 50 files, 2026-08-06 22:24 to 2026-08-12 09:16 CST (6 days, ~147 total files in `~/.claude/projects/*/*.jsonl`)

**Unused extensions identified:**

```
PROJECT SKILLS (.claude/skills/ gitignored):
  12 frontend/design skills: brandkit, design-taste-frontend, design-taste-frontend-v1, 
    full-output-enforcement, gpt-taste, high-end-visual-design, imagegen-frontend-mobile, 
    imagegen-frontend-web, image-to-code, industrial-brutalist-ui, minimalist-ui, 
    redesign-existing-projects, stitch-design-taste
    → Usage: design-taste-frontend used once (2026-06-03, 51 days ago); rest never used
    → Est. resident tokens: ~1194 combined
    → Verdict: remove (not applicable to personal knowledge repo)

USER SKILLS (~/.claude/skills/):
  cyber-neo [Security audit skill, 310 char desc]
    → Usage: 0 total, never in window
    → Est. resident tokens: ~120
    → Verdict: remove

PLUGIN SKILLS — caveman@caveman:
  cavecrew, caveman-commit, caveman-compress, caveman-help, caveman-review, 
  caveman-stats, caveman [core] (7 sub-skills)
    → Usage: caveman used 1 time (2026-06-21); caveman-review/compress/stats/help/commit/cavecrew all 0
    → Est. resident tokens: ~570 combined
    → Verdict: remove caveman sub-skills (not the core skill or hook)

PLUGIN SKILLS — claude-mem@thedotmack:
  knowledge-agent [233 char desc], make-plan [184], version-bump [235] (not in sub-skills list but referenced)
    → Usage: 0 total for those three; do, smart-explore, mem-search, timeline-report all used (keep)
    → Est. resident tokens: ~163 combined (3 unused)
    → Verdict: remove those 3

MCP SERVERS (claude.ai connectors, deferred, no usage counter):
  Three.js 3D Viewer, Trivago, lastminute.com
    → Invocation: 0 in window
    → Cost: deferred (names only in context)
    → Verdict: remove (declutter, reversible via `/mcp enable`)

CLAUDE.md trim (root, always-loaded):
  § Structure [directory tree] — 52 lines, 2123 chars, ~530 est. tokens
    → Fully reconstructable via ls/find; not derivable content, just repo layout
    → Verdict: cut, replace with one-line pointer
```

**Denial records (Check 9):** 19 total denials in window across 5 transcript files
- `user-rejected` (user said no): 14 entries — AskUserQuestion (3), ExitPlanMode (1), Bash/Write/MCP calls (9)
- `permission-rule` (deny rule blocked): 2 entries — sudo/dmidecode attempts (expected blocks)
- No candidates for allow-rule pre-approval (all denials were either user-intentional or write/privileged operations)

**Hook performance (Check 5):**
- Stop:Stop — 47 runs, median 8.2s, max 40654266ms (outlier: worker stall)
- SessionStart:startup — 12 runs, median 743ms, max 2.0s
- SessionStart:compact — 12 runs, median 487ms, max 1.9s
- All PostToolUse hooks (Bash/Read/Write/Edit/ToolSearch/AskUserQuestion) — 100-450ms typical, under 5s max

---

## 9 · Destino sugerido

**Doc canónico:** None — this is a procedural/cleanup handoff, not a feature or research document. Findings feed directly into `AskUserQuestion` gates (pending user confirmation to apply).

**Actualiza `perfil_maestro`:** No changes to identity, stack, or core criteria. Tooling hygiene only.

**Código a extraer:** N/A

**Insight cross-lens:** Caveman mode (P2 tooling) interacts with settings cascade (P2 config) and plugin architecture (P2 infrastructure) — the decision to preserve caveman mode while disabling caveman sub-skills required understanding all three layers. Not a bug, but a design decision worth recording: mode ≠ skills.

---

**Sugerido commit (sin ejecutar):** `inbox: handoff 14-08-26 claude-code-doctor`
