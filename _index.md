# mi-criterio — índice

Mapa del repositorio. Tres capas: **captura → procesado → destilado**.
Para integrar nuevo contenido: `/process-inbox`

---

## Capa 1 · Captura `inbox/`

Zona de entrada sin clasificar. Voz, ideas, sesiones, fragmentos.
Procesamiento: semanal o con `/process-inbox`.

| Archivo | Tipo | Estado |
|---|---|---|
| `02-05-26_cv_siemens_energy_canva_edit.md` | sesión Canva | archivado |
| `04_05_26_voice_extraction_session_roles.md` | extracción voz | archivado |
| `05-04-26_ArchMftCorrupto.txt` | incidente técnico | archivado |
| `09-04-26_FibonacciStackBase.txt` | sesión infra | archivado |
| `11-04-26_FibonacciStackCompleto.txt` | sesión infra | archivado |
| `14-04-26_FibonacciArchSetup.html` | sesión infra | archivado |
| `15-04-26_SshAgentDiagnosis.md` | diagnóstico SSH | archivado |
| `20-03-26_CVsCanva.md` | sesión CV | archivado |
| `20-03-26_PerfilGitDiff.txt` | diff perfil | archivado |
| `20-04-26_IDEdual_CutWindow_2.txt` | sesión setup | archivado |
| `23-04-26_Seguridad_Settings.txt` | seguridad | archivado |
| `23-04-26_session_compact.md` | sesión compacta | archivado |
| `27-04-26_K2SystemsProfile.md` | perfil empresa | archivado |

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
| `cutwindow2_contexto.md` | contexto IDE y rutas del proyecto nesting engine |

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
| `P8_Backup_Wiki/` | estrategia de backup y seguridad digital |
| `P8_Backup_Wiki/mft_recovery_decision.md` | decisión técnica: instalación Linux limpia tras MFT corrupto |
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
