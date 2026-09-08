# mi-criterio — índice

Mapa del repositorio. Tres capas: **captura → procesado → destilado**.
Para integrar nuevo contenido: `/process-inbox`

---

## Capa 1 · Captura `inbox/`

Zona de entrada sin clasificar. Voz, ideas, sesiones, fragmentos.
Procesamiento: semanal o con `/process-inbox`.

| Archivo | Tipo | Estado |
|---|---|---|
| `02-05-26_cv-siemens-energy-canva-edit.md` | sesión Canva | archivado |
| `04-05-26_voice-extraction-session-roles.md` | extracción voz | archivado |
| `05-04-26_arch-mft-corrupto.txt` | incidente técnico | archivado |
| `09-04-26_fibonacci-stack-base.txt` | sesión infra | archivado |
| `11-04-26_fibonacci-stack-completo.txt` | sesión infra | archivado |
| `14-04-26_fibonacci-arch-setup.html` | sesión infra | archivado |
| `15-04-26_ssh-agent-diagnosis.md` | diagnóstico SSH | archivado |
| `20-03-26_cvs-canva.md` | sesión CV | archivado |
| `20-03-26_perfil-git-diff.txt` | diff perfil | archivado |
| `20-04-26_ide-dual-cutwindow-2.txt` | sesión setup | archivado |
| `23-04-26_seguridad-settings.txt` | seguridad | archivado |
| `23-04-26_session-compact.md` | sesión compacta | archivado |
| `27-04-26_k2-systems-profile.md` | perfil empresa | archivado |
| `23-05-26_vpn-privacidad-y-seguridad-linux.md` | sesión seguridad | archivado (fusión → `proyectos/P2/arch_linux_security_audit_2026-05-23.md` §VPN) |
| `30-08-26_handoff-OpenClaw-Ollama.md` | handoff | archivado (fusión → `recursos/Herramientas_IA_Evaluadas.md` §OpenClaw + `HANDOFF_LLM_agentico_local.md` §10) |
| `31-08-26_handoff-gemini-code-deployment-landing-page-cliente.md` | handoff | archivado (fusión → `proyectos/P2/deployment_landing_pages.md` + `recursos/yazsarai_landing_page.md`) |
| `conversacion_caveman.pdf` | PDF local | pendiente (sesión P5 asignada · local-only, gitignored) |
| `conversacion_mexico_economia_caveman.pdf` | PDF local | pendiente (sesión P5 asignada · local-only, gitignored) |
| `08-09-26_handoff_respaldo-gaby-runbook.md` | handoff | pendiente (sesión P8×P2: rescate Carta Blanca ✅ + runbook backup + limpieza Gaby; sustituto FreeCell → Aisleriot ✅, stats a validar en dispositivo) |

---

## Capa 2 · Procesado `proyectos/`

Criterio consolidado por lente. Solo llega aquí lo que ya fue revisado.

### P1 — CNC / CAD / Manufactura `[latente]`
| Archivo | Propósito |
|---|---|
| `P1_cnc_manufactura.txt` | lente principal — pegar en conversaciones P1 |

### P2 — Programación y Desarrollo `[activo]`
| Archivo | Propósito |
|---|---|
| `P2_programacion_desarrollo.txt` | lente principal |
| `stack_ia_local_veredicto.md` | decisión: stack IA local CPU-only |
| `Plan: Stack IA local privado completo para CPU-only (3 workflows).txt` | plan infra IA local |
| `HANDOFF_LLM_agentico_local.md` | handoff maestro: LLM agéntico local, decisiones D1-D10, estado OpenCode |
| `COSMIC_setup_custom.md` | setup COSMIC/Arch: atajos, scripts, térmica/energía, shell/navegador/privacidad, CLIs IA globales (§12 deepcode) |
| `cutwindow2_contexto.md` | contexto IDE y rutas del proyecto nesting engine |
| `arquitectura_noticias_sin_sesgo.md` | diseño sistema RSS/GDELT/LLM local sin sesgo ni telemetría |
| `restmo_monitor_tuya.md` | monitor caudalímetro Restmo vía Tuya Cloud API |
| `deployment_landing_pages.md` | guía canónica: despliegue landing pages estáticas (Cloudflare Pages + CI/CD + cotización) |
| `browser_use_firefox_findings.md` | hallazgos: browser-use = CDP-only, incompatible con Firefox; alternativas mapeadas |
| `backup_cualquier_dispositivo_runbook.md` | runbook canónico: backup+auditoría de cualquier dispositivo (Windows .bat/.ps1 + Linux), destilado de P8_Backup_Wiki |

### P3 — Energía y Sostenibilidad `[activo]`
| Archivo | Propósito |
|---|---|
| `P3_energia_sostenibilidad.txt` | lente principal — eje vocacional |
| `geowind_links.md` | recursos geoeólicos |

### P4 — Finanzas Personales `[latente]`
| Archivo | Propósito |
|---|---|
| `P4_finanzas_inversiones.txt` | lente principal |

### P5 — Geopolítica y Economía `[latente]`
| Archivo | Propósito |
|---|---|
| `P5_geopolitica_economia.txt` | lente principal |

### P6 — Carrera y Futuro `[activo]`
| Archivo | Propósito |
|---|---|
| `P6_ayuda_futuro.txt` | lente principal |
| `SECTOR_OBJETIVO_REFINADO_EJECUTABLE.md` | mapa sector objetivo con acciones |
| `cv/CV_2026_eng.pdf` | CV inglés exportado |
| `cv/CV_2026_esp.pdf` | CV español exportado |
| `cv/PerfilCVs_Descripciones.md` | descripciones por rol |
| `cv/skills_master.md` | banco de habilidades |
| `cv/education_master.md` | banco educación |
| `cv/methodology.md` | metodología de extracción de voz |
| `cv/roles/` | carpeta roles extraídos |
| `cv/templates/` | plantillas |
| `cv/companies/` | carpeta empresas objetivo |
| `guia_voz_posgrado_sostenibilidad.md` | template sesión de voz para exploración de posgrado |
| `posgrado_opciones_sostenibilidad.md` | opciones de posgrado en sostenibilidad energética (may 2026) |
| `journey_p6cv_sistema.md` | retrospectiva narrativa de la construcción del sistema P6/cv |
| `cv/interview_cometer_pm_solar.md` | hechos duros: entrevista PM Cometer, sistemas energéticos discutidos |

### P7 — Filosofía y Humanidades `[activo]`
| Archivo | Propósito |
|---|---|
| `P7_filosofia_humanidades.txt` | lente principal |
| `Ritual conversacional de 7 pasos para inducir recursividad.txt` | framework filosófico |

### P8 — Ingeniería y Ciencia `[latente]`
| Archivo | Propósito |
|---|---|
| `P8_ingenieria_ciencia.txt` | lente principal |

---

## Capa 3 · Destilado (transversal)

Solo se actualiza cuando cambia identidad, criterio, o stack técnico.

| Archivo | Propósito |
|---|---|
| `perfil_maestro_eldaniels_v2.txt` | contexto completo — pegar al inicio de cualquier conversación |
| `proyectos_instrucciones_eldaniels_v2.txt` | cómo usar los lentes P1–P8 |
| `activacion_cruzada_eldaniels_final.txt` | sintaxis de activación cruzada entre lentes |
| `ToDo_global_eldaniels.md` | lista de tareas activas |

---

## Soporte

| Carpeta / Archivo | Propósito |
|---|---|
| `recursos/` | guías de referencia guardadas (Git, SSH, licencias, Claude Code) |
| `recursos/MEMORIA_SISTEMA_CLAUDE.md` | migración completa de toda la memoria de Claude Code (feedback, proyectos, 50 obs claude-mem, jun 2026) |
| `recursos/GUIA_INBOX_CROSS_AI.md` | formato canónico de captura inbox, vendor-neutral |
| `recursos/AUR_Atomic_Arch_2026_Informe.md` | informe forense: supply-chain attack AUR jun 2026 (1.937 paquetes) |
| `recursos/Herramientas_IA_Evaluadas.md` | resúmenes críticos: open-notebook, OmniRoute, diagram-design, project-nomad |
| `recursos/closing_session_transporte_seguro_gdl.md` | proyecto Transporte Seguro GDL: brief comercial + landing page construida |
| `recursos/yazsarai_landing_page.md` | tracker proyecto cliente YazSaraí: estado, blockers, triggers de retoma |
| `P8_Backup_Wiki/` | estrategia de backup y seguridad digital — `P8_Backup_Seguridad_Digital_Maestro.md` es el único doc de plan/estado (v2.0, absorbe Timeline_Fases + Archivos_Criticos_Inventory) |
| `P8_Backup_Wiki/mft_recovery_decision.md` | decisión técnica: instalación Linux limpia tras MFT corrupto |
| `P8_Backup_Wiki/freeze_i915_fsck_incidente.md` | incidente: freeze sistema + pérdida symlink `claude` por fsck tras corte abrupto |
| `CLAUDE.md` | instrucciones para Claude Code en este repo |
| `CONTRIBUTING.md` | convenciones del repo |
| `README.md` | descripción pública |
| `disclaimer_soberania_datos.txt` | aviso de soberanía de datos |

---

## Convenciones

- **Naming inbox:** `DD-MM-YY_tema-corto.md`
- **Naming proyectos:** sin fecha — es criterio permanente
- **Estado inbox:** `pendiente → procesado → descartado`
- **Estado lente:** `[activo | latente | archivado]`
- **Commit style:** `update P3: [qué cambió]` o `inbox: add DD-MM-YY_tema`
- **No forzar completitud** — el repo tolera fragmentos en inbox
