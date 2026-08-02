# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

`mi-criterio` is a personal knowledge architecture repo. It stores context documents that eldaniels pastes into AI conversations to provide full background without re-explaining history. It is not a software project — there are no builds, tests, or deployments.

## Structure

```
mi-criterio/
├── CLAUDE.md                                    ← this file
├── README.md
├── CONTRIBUTING.md
├── LICENSE.md
├── .gitignore
├── perfil_maestro_eldaniels_v2.txt              ← master profile, always updating
├── proyectos_instrucciones_eldaniels_v2.txt     ← how to use the P1-P8 lenses
├── activacion_cruzada_eldaniels_final.txt       ← cross-lens activation syntax
├── disclaimer_soberania_datos.txt
├── ToDo_global_eldaniels.md                    ← master task list
├── cronograma_intereses.md                      ← [PENDIENTE] timeline of interest evolution
├── proyectos/                                   ← one subdirectory per project lens
│   ├── P1/P1_cnc_manufactura.txt
│   ├── P2/P2_programacion_desarrollo.txt
│   ├── P3/P3_energia_sostenibilidad.txt
│   ├── P4/P4_finanzas_inversiones.txt
│   ├── P5/P5_geopolitica_economia.txt
│   ├── P6/P6_ayuda_futuro.txt
│   ├── P6/SECTOR_OBJETIVO_REFINADO_EJECUTABLE.md
│   ├── P7/P7_filosofia_humanidades.txt
│   └── P8/P8_ingenieria_ciencia.txt
├── P8_Backup_Wiki/                              ← backup & security documentation
│   ├── P8_Backup_Seguridad_Digital_Maestro.md
│   ├── Archivos_Criticos_Inventory.md
│   └── Timeline_Fases.md
├── recursos/                                    ← reference guides and saved resources
│   ├── LICENCIAS_EXPLICADAS.md
│   ├── SEGURIDAD_GITIGNORE_CONTRIBUTING.md
│   ├── SSH_Y_CLAUDE_PROJECTS_EXPLICADO.md
│   ├── git_daily_workflow_reference.html
│   └── claude-code-install.html
└── sesiones/                                    ← session logs and diffs
    ├── 12-03-26_CutWindow_2_contexto.md
    ├── 20-03-26_PerfilGitDiff.txt
    ├── 20-03-26_CVsCanva.md
    ├── 05-04-26_ArchMftCorrupto.txt
    ├── 07-04-26_MftRecoveryDecision.txt
    ├── 09-04-26_FibonacciStackBase.txt
    ├── 11-04-26_FibonacciStackCompleto.txt
    ├── 14-04-26_FibonacciArchSetup.html
    ├── 15-04-26_SshAgentDiagnosis.md
    ├── 20-04-26_IDEdual_CutWindow_2.txt
    ├── 23-04-26_Seguridad_Settings.txt
    ├── 23-04-26_cierre_sesion.txt
    ├── 23-04-26_session_compact.md
    └── 27-04-26_K2SystemsProfile.md
```

## Git Conventions

- `main` branch holds `perfil_maestro_eldaniels_v2.txt` — the source of truth for full context
- Each `proyectos/P*/` file corresponds to a thematic lens that can be used independently
- Commit when a meaningful update is made to any document (career change, new tool adopted, new project started)
- Suggested commit style: `update P3: add geothermal research notes` or `perfil: new job at X`

## Document Roles

| File | Use |
|---|---|
| `perfil_maestro_eldaniels_v2.txt` | Paste at start of any new AI conversation for full context |
| `proyectos_instrucciones_eldaniels_v2.txt` | How to use the P1-P8 lenses together |
| `proyectos/P*/` | Paste individually when working in a specific domain |
| `cronograma_intereses.md` | [PENDIENTE] Timeline of skill/interest evolution over time |
| `activacion_cruzada_eldaniels_final.txt` | Syntax for cross-lens problem analysis |
| `ToDo_global_eldaniels.md` | Master task list — what is live, in progress, pending |
| `P8_Backup_Wiki/` | Backup strategy and critical files inventory |
| `recursos/` | Saved reference guides (Git, SSH, licenses, Claude Code) |
| `sesiones/` | Session logs — timestamped record of decisions and diffs |

## Key Interconnections to Maintain

When updating one document, check if related lenses need updating too:

- Finanzas ↔ Geopolítica ↔ Energía (often co-evolve)
- Programación ↔ Finanzas (Excel project is shared)
- CNC ↔ Ingeniería (applied physics, materials)
- Energía ↔ Filosofía (Solarpunk framing)
- Ayuda Futuro ↔ all (career decisions require multiple lenses)
