# 25-05-26 — Cross-AI Memory Integration Guide for mi-criterio Inbox

**Purpose:** Enable ChatGPT, DeepSeek, Claude, Ollama, or any LLM to contribute structured conversation data to the mi-criterio personal knowledge management system.

---

## Quick Start: How to Save a Conversation to mi-criterio

When you finish a productive conversation with any AI, capture the key insights by creating a file in `@inbox/` using this format:

### File Naming Convention
```
DD-MM-YY_topic_short_description.md
```

**Examples:**
- `25-05-26_nesting_engine_architecture.md`
- `24-05-26_siemens_energy_cv_strategy.md`
- `23-05-26_postgrad_upm_research.md`

---

## File Structure (Simple Template)

```markdown
# DD-MM-YY — [Topic Title]

## Context
[Where did this conversation happen? What AI model? What was the goal?]

**AI:** ChatGPT / DeepSeek / Claude / Ollama / other  
**Duration:** ~30 min (optional)  
**Goal:** What were you trying to accomplish?

---

## Key Insights / Decisions

- **Insight 1:** [What you learned or decided]
- **Insight 2:** [Specific finding, direction, or next step]
- **Insight 3:** [Any blockers, clarifications, or pivots]

---

## Artifacts & Output

### Artifact 1: [Name]
```
[Code, text, outline, or structured data produced in the conversation]
```

### Artifact 2: [Name]
```
[Any second artifact — template, checklist, config, etc.]
```

---

## Integration Hint (for Claude Code triage)

**Lens(es):** P1, P2, P3, P6, etc. — which project(s) does this belong to?  
**Status:** Complete / Skeleton / In-Progress  
**Action:** Move to P#/ and integrate into _index.md / Archive / Keep in inbox for refinement

---

## Next Steps

- [ ] Action 1
- [ ] Action 2
- [ ] Reference external resource (link, commit, etc.)
```

---

## Why This Format?

1. **Portable** — Works with any AI, any chat interface
2. **Scannable** — Quick to read; clear structure
3. **Self-contained** — No Claude-specific metadata needed
4. **Triage-ready** — Includes hints for moving from inbox → proyectos/
5. **Human-friendly** — Can be written during or after a session

---

## Integration Workflow (What Happens Next)

Once you save a file to `@inbox/`:

1. **You run:** `/process-inbox` in Claude Code
2. **Claude reads** all pending inbox files and proposes actions:
   - `MOVER → P#/` (move to specific project folder)
   - `MOVER + ACTUALIZAR perfil_maestro` (move + update core profile if identity changes)
   - `ARCHIVAR` (move to archive)
   - `DESCARTAR` (delete)
   - `MANTENER inbox` (keep in inbox for later processing)
3. **You approve** the proposed actions
4. **Files migrate** from Capa 1 (inbox) → Capa 2 (proyectos/) with status tracked in `_index.md`

---

## Practical Examples

### Example 1: Job Search Strategy Session (ChatGPT)

```markdown
# 25-05-26 — Siemens Energy Energy CV + Cover Letter Strategy

## Context
**AI:** ChatGPT 4o  
**Goal:** Refine CV bullet points for a Mechanical Engineer role at Siemens Energy Querétaro (C#/.NET focus)

---

## Key Insights

- Siemens Energy prioritizes cross-functional team impact — emphasize *collaboration* in CNC/software sections
- "SW Developer" title is stronger than "Programador C#" for their ATS
- Cover letter should **not** repeat CV; instead, show *why you care about renewable energy*
- Energy background (not in current CV) is hidden asset — add to skills or statement of purpose

---

## Artifacts

### Refined CV Bullets (Spanish)
- Desarrollo de software en C# para sistemas de corte láser en paracaídas (American Industries, Performance Designs)
  - Integración con servidores industriales y control en tiempo real
  - [ADD: cross-functional collaboration example if available]

### Cover Letter Opening (Draft)
> Mi formación en ingeniería mecánica y experiencia en sistemas de automatización me motiva a contribuir a la transición energética desde dentro de Siemens Energy...

---

## Integration Hint

**Lens(es):** P6 (job search), P2 (C# software development)  
**Status:** Skeleton  
**Action:** Move to `P6/cv/applications/siemens_energy/` and link in `companies/siemens_energy_profile.md`
```

### Example 2: CNC/Nesting Engine Insight (DeepSeek)

```markdown
# 24-05-26 — CutWindow_2 DXF Import Edge Cases & Robustness

## Context
**AI:** DeepSeek Coder (Local Ollama)  
**Goal:** Identify edge cases in DXF polygon import logic before open-source release

---

## Key Insights

- **Self-intersecting paths** are common in CAD exports from cheap laser software → need validation layer
- **Degenerate polygons** (zero-area, collinear points) crash the nesting engine → add pre-filter
- **Coordinate precision** mismatch (7 decimal places vs integer) causes false overlaps → normalize to 6 decimals

---

## Proposed Fix

1. Add `DxfValidator.IsValidPolygon()` check pre-import
2. Log skipped invalid paths with reason (helps user debug their CAD files)
3. Update README with "Supported DXF Export Formats" section

---

## Integration Hint

**Lens:** P2 (CutWindow development)  
**Status:** Complete (ready to implement)  
**Action:** Move to `P2/cutwindow2_contexto.md` and link under "Known Issues"
```

---

## Tips for Better Inbox Integration

**✓ DO:**
- Capture decisions, not just information
- Include external links (research articles, company URLs, etc.)
- Note blockers explicitly ("waiting for X to clarify Y")
- Use the same topic name consistently across multiple sessions

**✗ DON'T:**
- Save every conversation — only those with lasting value
- Dump raw chat logs — summarize key points instead
- Include sensitive personal data (passwords, API keys, etc.)
- Use vague filenames like `25-05-26_notes.md`

---

## Naming Tips by Project

| Lens | Example Filenames |
|------|-------------------|
| **P1** CNC | `DD-MM-YY_cnc_grbl_configuration.md` |
| **P2** Code | `DD-MM-YY_cutwindow_async_refactor.md` |
| **P3** Energy | `DD-MM-YY_solar_thermal_hybrid_research.md` |
| **P4** Finance | `DD-MM-YY_etf_dividend_yield_comparison.md` |
| **P6** Career | `DD-MM-YY_upm_madrid_application_strategy.md` |

---

## Questions?

This guide is self-contained and vendor-neutral. If you have a conversation with *any* AI — Claude, ChatGPT, DeepSeek, Llama, Mistral, whatever — you can use this format to deposit the output into mi-criterio and let the `/process-inbox` workflow handle the rest.

**The goal:** One unified inbox, many AI assistants, zero vendor lock-in.

---

*Version 1.0 — May 25, 2026*  
*Last updated: 2026-05-25*
