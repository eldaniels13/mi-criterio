# Journey Into mi-criterio — P6/cv: A Job Search System Built in a Week

**Date range:** April 12–19, 2026 (8 days)
**Observations analyzed:** 264 across 21 sessions
**Focus:** proyectos/P6/cv — the CV and job search infrastructure
**Generated:** April 19, 2026

---

## 1. Project Genesis

The mi-criterio repository didn't start as a CV system. It started on April 12, 2026 as a personal knowledge architecture — a place to consolidate 477 conversations from ChatGPT, DeepSeek, and Claude into eight thematic lenses (P1–P8). The first commit landed April 13 at 1:00 AM, after a late-night burst session that created all eight project context files in sequence.

P6 (Ayuda Futuro / Career & Personal Development) was always in the plan, but in those first 24 hours it was just one of eight files. The CV work emerged from a single observation documented on April 12 (#11): *"CV Raw Content Found — Work Experience Ready for Canva Formatting."* That recognition — the raw material already existed, it just wasn't structured — triggered everything that followed.

The real genesis was a constraint: there were existing Canva CVs (CV_2025_Programacion and CV_2025_Manufactura) and no systematic way to tailor them for specific companies. The job search was already active. The infrastructure wasn't. Building the infrastructure became the project.

---

## 2. Architectural Evolution

The P6/cv architecture went through three distinct phases across the eight days:

**Phase 0 — Pre-architecture (before Apr 15):** Canva files, raw experience text buried in todo lists, no systematic structure. The work experience content existed but was scattered across tools.

**Phase 1 — Initial scaffold (Apr 15–16):** Session S22 created the folder structure for P6/cv. A `cv_methodology.md` was written to establish the founding rule: *nothing in any CV can be invented — every claim traces back to a master role file.* This is the architectural keystone of the entire system. From it, the skills master, education master, role files, and CV templates were built in rapid succession (observations 200–210). In a single afternoon, the scaffolding went up: `roles/`, `templates/`, and the four bilingual profile summaries in `PerfilCVs_Descripciones.md`.

**Phase 2 — Company-level system (Apr 17–18):** The Continental application (REF95136I, San Luis Potosí) was the first real test of the system. Building it triggered a realization: company-specific profile documents needed their own home. The `companies/` directory was created (#232). A cover letter was written with a solarpunk lens. A professional bio was rewritten in conversational tone. The Siemens Energy profile template was created. The system was being used for the first time on real applications.

**Phase 3 — Consolidated pattern (Apr 19):** Architecture cleanup. The two-file-per-company approach (separate research and profile files) was designed, tried, and immediately rejected in the same session (#275). A `_research_template.md` was established as a reusable methodology. The Siemens files were merged without losing any voice session material. Bosch was scaffolded using the new single-file pattern. The directory tree in `methodology.md` was updated to match reality. The architecture stabilized.

In eight days: scattered Canva files → a fully structured, traceable, research-first job application pipeline.

---

## 3. Key Breakthroughs

**The methodology rule (#226, Apr 17):** The decision to require every CV claim to trace back to a master file was the founding architectural decision. It prevents credential inflation and creates interview defensibility — when a recruiter asks about any item, the answer exists because the source file exists. This rule was articulated explicitly on April 17 but implicitly enforced from the moment the role files were designed.

**Companies directory creation (#232, Apr 17):** A small structural move with a large conceptual shift. Before this, the CV system described a person. After this, it described a pipeline. Each target company gets its own document; the master files provide the traceable source material. The system became multi-target.

**Two-file rejection (#275, Apr 19):** The decision to consolidate research and profile into a single file happened within hours of creating the two-file pattern. The insight was direct: research exists to answer "Why this company?" — which lives in the profile as Q5. Keeping them in separate files means you always need both open. One file, co-located context, no duplication. The Bosch template was restructured immediately.

**Voice session capture (Apr 19 morning, Q1–Q4):** A 90-minute mobile voice session produced the most differentiated content in the entire system. The key quotes — verbatim voice responses — represent a quality of authentic expression that no AI-drafted prompt can replicate: *"I don't pick ideology. I pick evidence."* The decision to preserve both the edited prose and the raw voice material as separate subsections in the profile ensures the source material is never lost to the final version.

---

## 4. Work Patterns

The timeline reveals distinct work modes across the eight days:

**Late-night setup sprints (Apr 12–13):** Rapid file creation from roughly 11 PM to 1 AM. P1 through P8 context files built sequentially, git initialized, `.gitignore` written, first commit at 1:00 AM. Classic burst mode — high momentum, no interruptions.

**Debug/fix cycles (Apr 14):** Almost the entire day was consumed by the git push failure sequence (observations 45–61). Private email in commit history, GitHub email privacy protection blocking push, git history rewrite, email removed from file contents, sync verified. Seven distinct interventions. Not P6/cv work — but it cleared the path for everything that followed.

**Strategic design (Apr 15 morning):** The Canva audit and CV strategy session. Two existing CVs mapped, differentiation strategy defined, bilingual master CV approach confirmed. Thinking work, not building work.

**Infrastructure build (Apr 15–16 afternoon):** The methodology, master files, and templates created. No visible application output but all the scaffolding went up. The most important session in terms of long-term leverage.

**Application execution (Apr 17):** The system was used on real applications for the first time. Continental profile, cover letter with solarpunk framing, LinkedIn bio rewrite. The infrastructure proved itself.

**Consolidation (Apr 19):** Pattern cleanup before adding more companies. Merge decisions, file restructuring, architecture documentation updated.

---

## 5. Technical Debt

**Created and paid in minutes:** The two-file pattern for Bosch was designed at #268–271 and rejected at #275. Debt lifetime: approximately 15 minutes. This is the best possible outcome — a design decision made, its consequence immediately recognized, corrected before it could propagate to Ørsted or Iberdrola.

**Lingered briefly:** `cv_methodology.md` was initially placed in `P6/` instead of `P6/cv/` and moved at observation #205. Minor, but it shows the methodology document was needed before the folder structure it described was finalized.

**Typo in a key filename:** `PerfilCVs_Despriciones.md` (misspelled) appears in early observations and was corrected to `PerfilCVs_Descripciones.md` later. It persisted across at least two sessions before being fixed.

---

## 6. Challenges and Debugging Sagas

**Git email saga (Apr 14):** The longest debugging sequence in the project. Push rejected (#45) due to GitHub email privacy settings → root cause identified as private email in commit history (#47) → history rewritten with `git filter-branch` (#50) → file contents scanned for email exposure (#51–52) → email removed from README and CONTRIBUTING (#53–54) → session log redacted (#55) → remote sync verified (#61). Seven steps, one root cause. The system worked — but required the entire afternoon.

**Canva MCP permission gate (#144, Apr 15):** Mid-CV-edit, the Canva MCP server hit a permission wall that blocked execution. Edits were staged but could not be committed automatically. Required switching to manual confirmation flow, which broke the assumed automation. Resolved but established that Canva MCP is not fully reliable for unattended editing.

**Indeed MX zero results (#154–158, Apr 15):** The Indeed MCP tool consistently returned zero results for Guadalajara engineering roles. English queries failed. job_type filters failed. Only Spanish queries without filters returned results — and those weren't structured well enough for job alerts. The decision (#251): pause job alerts, adopt manual search. The infrastructure was built for automation that the platform couldn't support.

---

## 7. Memory and Continuity

The mi-criterio system is itself a memory architecture. The eight project lenses are designed to be pasted into future AI conversations for full context without re-explanation. This is a meta project: a knowledge system being built with AI assistance to improve future AI assistance.

The claude-mem hooks played a measurable role throughout. The PreToolUse hook consistently blocked redundant file reads — returning observation timelines instead of file content when files hadn't changed. On a project where the same files (methodology.md, skills_master.md, siemens_energy_profile.md) were referenced across multiple prompts in the same session, this was a real token saving mechanism.

The most direct continuity event: drafting the Bosch template (#268–269) using the Siemens profile structure as reference without re-reading the Siemens file. The hook-provided observation history contained enough structural information to draft from. Same for the `_research_template.md` (#270) — the Q5 research checklist from the voice session became the template backbone without a re-read.

The voice session itself is a continuity artifact. The 90-minute conversation happened in Claude mobile; the outputs were captured in `P6_siemens_energy_research.md`; those outputs were later merged into `siemens_energy_profile.md`. The original voice material is now co-located with the edited profile, preventing the source from being lost to the final version.

---

## 8. Token Economics & Memory ROI

| Metric | Value |
|---|---|
| Total discovery tokens (work produced) | 1,483,836 |
| Total read tokens (memory consumed) | 83,247 |
| Net tokens saved | 1,400,589 |
| Compression ratio | **17.8×** |
| Effective cost rate | **5.6% of original** |
| Observations | 264 |
| Sessions | 21 |
| Active days | 8 |

**Top 5 most expensive observations (highest-value memories):**

| ID | Title | Discovery Tokens |
|---|---|---|
| 146 | English CV Spanish Date Strings Corrected | 133,005 |
| 147 | English CV Profile Summary Rewritten with Energy Framing | 133,005 |
| 148 | TDI CNC Operator Date Still in Spanish After Edit Batch | 133,005 |
| 143 | CV_2026_eng Content Fully Mapped from Canva Design | 131,859 |
| 40 | Session Log 07 Contains Sensitive System Information | 23,431 |

Observations 143–148 all come from the April 15 Canva CV editing session — one intensive session that cost approximately 664K discovery tokens but produced the bilingual CV foundation that all subsequent applications (Continental, Siemens, Bosch, Ørsted) draw from without re-paying that cost.

**Passive recall savings estimate:**

| Factor | Value |
|---|---|
| Sessions with context injection | 20 (all after first) |
| Observations injected per session | ~50 |
| Avg discovery value per observation | 5,620 tokens |
| Relevance factor | 30% (conservative) |
| **Estimated savings** | **1,686,000 tokens** |

**Explicit recall events:** 2 recorded in the database. The real number is higher — the startup hook injects the compressed timeline on every session, acting as passive recall before the first prompt is written.

**Net ROI:** approximately 20× return on memory investment across 8 days.

**Monthly breakdown (all April 2026):**

| Month | Observations | Discovery Tokens | Sessions |
|---|---|---|---|
| 2026-04 | 264 | 1,483,836 | 21 |

---

## 9. Timeline Statistics

| Metric | Value |
|---|---|
| Date range | Apr 12–19, 2026 |
| Total observations | 264 |
| Total sessions | 21 |
| Discoveries (🔵) | 143 — 54% |
| Changes (✅) | 69 — 26% |
| Features (🟣) | 27 — 10% |
| Decisions (⚖️) | 14 — 5% |
| Bug fixes (🔴) | 11 — 4% |
| Most active day | April 15 (repo scaffold + Canva CV session) |
| Longest debug sequence | Apr 14 git email saga — 7 observations, ~2 hours |
| Richest single session | Apr 15 Canva CV session — 664K discovery tokens |

The discovery-heavy distribution (54%) is characteristic of a system-building phase. The same ratio on a mature system would indicate over-exploration. When P6/cv enters production use — active applications, portal uploads, interview responses — the ratio should shift toward changes and features.

---

## 10. Lessons and Meta-Observations

**The master file rule is load-bearing.** Every application document is only as good as its source files. The `role_mexico_performance_designs.md` file took effort to write correctly — but it now feeds Continental, Siemens, Bosch, and any future application without re-explaining the role. The investment in source files pays forward at every application.

**Research before application, not after.** The Siemens Q5 pause — stopping the voice session mid-answer to verify the company's actual values before claiming alignment — is the right discipline. A values-driven application written without verifying the company's values is at best performative, at worst dishonest. The research blocks in the template enforce this sequence structurally.

**File count is a real maintenance cost.** The two-file → one-file consolidation happened on the same day the two-file pattern was created. The friction was immediately obvious, not hypothetical. A new company target requires exactly one file. That file has two parts. This is the right level of structure.

**Voice material is irreplaceable.** The Q1–Q4 key quotes from the Siemens session are the most differentiated content in the system. No drafted paragraph produces *"I want to provide what my country has provided to me"* — that comes from 90 minutes of authentic conversation. The system now preserves raw voice material alongside edited versions as a structural requirement, not an afterthought.

**The system is ahead of the applications.** As of April 19, the infrastructure is robust and the methodology is stable. But only one application is complete (Continental — pending upload). Siemens is in progress. Bosch and Ørsted are empty templates. The characteristic risk for this profile — flagged explicitly in the CLAUDE.md: *"sesga hacia diseño de estrategia antes de ejecutar acciones concretas"* — is visible here. The next milestone is portal uploads, not more architectural refinement.

The system is ready. The applications are not yet sent.

---

*journey-into-mi-criterio-p6cv.md — April 19, 2026*
*Generated from 264 observations, 21 sessions, 1,483,836 discovery tokens*
*claude-mem compression: 17.8× — 5.6% of original work cost to recall*
