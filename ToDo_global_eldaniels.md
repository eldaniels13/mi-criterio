━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TODO GLOBAL UNIFICADO — eldaniels · 2026-03-27
  Fuentes: perfil_maestro · session_diff 2026-03-20 ·
           cierre_sesion_fibonacci · memorias de sesiones P2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  CARRERA / TRACK ENERGÍA NACIONAL (May 2026 — voz ChatGPT)
  ─────────────────────────────────────────────────────────────────
  [ ] Activar alertas: CFE vacantes, SENER SPC, CENACE, LinkedIn "energía MX"
  [ ] Investigar Fundación Carolina (deadlines, requisitos UPM)
  [ ] Investigar Beca Iberdrola y Santander (energía/sostenibilidad)
  [ ] Curso corto BESS / smart grids (Coursera o equivalente)
  [ ] Mejorar inglés técnico energético (vocabulario redes, BESS, FERC)
  [ ] Mapear hiring managers Siemens Energy MX / Enel MX en LinkedIn
  [ ] Investigar UNAM IER (Temixco) — convocatoria, requisitos
  [ ] Networking ANES (Asociación Nacional de Energía Solar)


  RANDOM / por organizar
  ─────────────────────────────────────────────────────────────────
  [ ] hacer diagrama de red de conexion de PD (FWs, APs, ISP, etc)
  [~] expandir roles desempeñados — EncoreTools v1.0 ✅, 4 skeletons creados, pendiente voice extraction (TDI > MoldTech > PEP > Automotive)
  [ ] enriquecer experiencias y roles con recursos visuales
  [x] crear arquitectura de /proyectos/P6/cv


  SPOTIFY → SOBERANÍA DE DATOS MUSICALES  (P2 × P4 · multi-sesión)
  ─────────────────────────────────────────────────────────────────
  Contexto: Spotify es propietario y contradice el principio open source /
  copyleft. Se mantiene por una razón válida: TODOS los datos históricos de
  escucha viven ahí. Migrar no es instalar otra app, es un proyecto.
  Decisión (2026-08-06): no migrar a ciegas — primero extraer y poseer los datos.

  [ ] Solicitar descarga completa vía Spotify for Developers / Privacy
      (extended streaming history — tarda ~30 días en llegar)
  [ ] Registrar app en developer.spotify.com → client_id / secret (Web API)
  [ ] Extraer con API: top artists/tracks, audio features, playlists propias
  [ ] App Python de estadísticas — mejor que el Wrapped anual:
      · stack: pandas + matplotlib (o Streamlit, ya en el perfil)
      · métricas que Wrapped NO da: evolución multi-año, horarios de escucha,
        diversidad de géneros, tasa de descubrimiento vs. repetición
  [ ] Sólo entonces evaluar alternativa (Navidrome / Jellyfin / Funkwhale)
  [ ] Dar de baja Spotify cuando los datos estén fuera y la app funcione


  LINUX / ARCH — VM fibonacci
  ─────────────────────────────────────────────────────────────────
  [x]  Arch Linux instalado y arrancando en VirtualBox
  [x]  GRUB UEFI funcionando
  [x]  Red automática (systemd-networkd + systemd-resolved)
  [x]  IPv6 deshabilitado (ISP no soporta)
  [x]  Usuario eldaniels + sudo + wheel
  [x]  i3wm + autotiling fibonacci
  [x]  Firefox, git configurado, neovim base
  [x]  yay (AUR helper) instalado
  [x]  startx automático al login
  [ ]  LazyVim (falló por timeout de conexión — requiere mejor red)
  [x]  Terminar de configurar i3 (colores, fonts, gaps, i3status)
  [x]  Configurar Git → GitHub (eldaniels13) en la VM
  [ ]  Configuración de Neovim más allá de base


  LINUX / ARCH — HARDWARE REAL (Dell Latitude 5400)
  ─────────────────────────────────────────────────────────────────
  [x]  Guardar P8_Backup_Wiki
  [x]  Safe delete AppData\Roaming — carpetas identificadas
  [x]  Backup completo de Windows (FASE 0) ⚠ CRÍTICO
  [~]  Dual boot — particionar sin borrar Windows
  [x]  Instalar Arch en Dell Latitude 5400
  [x]  Instalar COSMIC (decisión tomada: el futuro es hoy — Wayland, auto tiling fibonacci)
  [ ]  LazyVim con buena conexión para desarrollo y trabajo
  [x]  sudo pacman -S veracrypt para xochimilco.vc
  [x]  Configurar multi-monitor (horizontal + vertical)
  [~]  IPv6 reactivar cuando cambies de ISP (borrar /etc/sysctl.d/99-disable-ipv6.conf)
  [x] Configurar ~/.zshrc completo (starship + plugins + nvm) ~/.config/starship.toml
  [x] Instalar Nerd Font (ttf-jetbrains-mono-nerd)
  [ ] Configurar starship.toml personalizado


  HERRAMIENTAS DE DESARROLLO
  ─────────────────────────────────────────────────────────────────
  [x]  git + GitHub (eldaniels13)
  [x]  neovim base
  [x]  VeraCrypt
  [x]  LazyVim
  [x]  lazygit
  [x]  .NET 8 SDK (dotnet 10.0.104)                       → hardware real
  [x]  Python + pip + venv (Python 3.14.4)                → hardware real
  [x]  Docker                                             → hardware real
  [x]  VS Code 1.114.0                                    → hardware real
  [x]  Node.js + npm (requerido para Claude Code)
  [x]  Claude Code CLI (npm install -g @anthropic-ai/claude-code)
  [x]  Ollama con deepseek-coder:6.7b y qwen2.5-coder:7b
  [x]  Krokiet (czkawka GUI) — ~/tools/krokiet, instalado Jun 29 2026 (bin directo GitHub, no AUR)
  [x]  Instalar https://github.com/thedotmack/claude-mem
  [x]  Instalar https://github.com/affaan-m/everything-claude-code
  [~]  project-nomad (Crosstalk-Solutions)
  [ ] Verificar compatibilidad Python 3.14 con pandas/matplotlib cuando se instale Jupyter
  
  
  EMAIL
  ─────────────────────────────────────────────────────────────────
  [x] Thunderbird instalado
  [ ] Crear cuenta Proton Mail
  [x] Configurar Thunderbird con todas las cuentas (Gmail personal, Gmail profesional, Outlook educativo)
  [ ] Migrar historial Gmail → Proton con Import Assistant.


  UTILIDADES DEL SISTEMA
  ─────────────────────────────────────────────────────────────────
  [x]  htop                                               pacman -S htop
  [x]  ripgrep (rg)                                       pacman -S ripgrep
  [x]  fzf                                                pacman -S fzf
  [x]  zsh + starship                                     → hardware real
  [x]  Thunar                                             pacman -S thunar
  [x]  Timeshift                                          yay -S timeshift


  CAD Y DISEÑO
  ─────────────────────────────────────────────────────────────────
  [x]  LibreCAD                                           pacman -S librecad
  [x]  FreeCAD                                            pacman -S freecad
  [x]  OpenSCAD                                           pacman -S openscad
  [x]  Inkscape 1.4.3                                     pacman -S inkscape


  EXCEL / HOJAS DE CÁLCULO
  ─────────────────────────────────────────────────────────────────
  [x]  LibreOffice                                        pacman -S libreoffice-fresh
  [x]  Gnumeric 1.12.60                                   pacman -S gnumeric


  ENERGÍA / PERFIL PROFESIONAL
  ─────────────────────────────────────────────────────────────────
  [ ]  Jupyter Lab                                        pip install jupyterlab
  [ ]  Python pandas                                      pip install pandas  ← pendiente
  [x]  matplotlib 3.10.8                                  pip install matplotlib
  [ ]  QGIS                                               pacman -S qgis


  REPO MI-CRITERIO
  ─────────────────────────────────────────────────────────────────
  [x]  Inicializar repo git mi-criterio/ y primer commit
  [x]  Crear repo privado en GitHub
  [x]  Añadir .gitignore (*.key, *_privado.txt, *_sensible.*, git-crypt)
  [x]  Subir arquitectura a repo mi-criterio/ en GitHub
  [x]  CLAUDE.md en root del repo (perfil_maestro integrado como CLAUDE.md)
  [x]  Crear archivos P1-P8 individuales en proyectos/
  [ ]  Crear cronograma_intereses.md como archivo permanente
  [~]  Criterio vivo de P3, P4, P2 — expandir en sesiones futuras
  [~]  Terminar de aprender a usar Git
  [ ]  Inicializar git en proyectos de Programas PerformanceDesigns
     (CutWindow_2, DeepNestSharp, NestingTesting, O2BToDxf...)
  [ ]  Subir proyectos PerformanceDesigns a GitHub (eldaniels13)
  [x] Crear ~/.claude/CLAUDE.md global (copia perfil_maestro v2)
  [x] Crear ~/.claude/settings.json global (permisos base)
  [x] Crear mi-criterio/.claude/CLAUDE.md (resumen P1-P8)
  [x] Crear mi-criterio/.claude/settings.json (permisos repo)
  [x] Crear mi-criterio/.claude/commands/p1-cad.md
  [x] Crear mi-criterio/.claude/commands/p2-code.md
  [x] Crear mi-criterio/.claude/commands/p3-energy.md
  [x] Crear mi-criterio/.claude/commands/p6-future.md
  [ ] Prueba: `claude /status` en mi-criterio y verificar CLAUDE.md's
  [x] Prueba: `/p1-cad` carga contexto P1 correctamente
  [ ] Registrar P1-P8 proyectos bajo git (git init en cada uno)
  [ ] Subir arquitectura completa a GitHub privado (mi-criterio)


  PROYECTOS ACTIVOS
  ─────────────────────────────────────────────────────────────────
  [~]  Terminar CutWindow_2 (nesting engine)
  [~]  Desarrollar Excel plantilla de finanzas personales
  [x]  Migrar de Win11Home a Linux Arch

DOCUMENTACIÓN PENDIENTE
──────────────────────────────────────────────────────────────
[~] Descripción detallada P4 (Finanzas) — estructura SOFIPOS/ETFs
[~] Descripción detallada P5 (Geopolítica) — marcos Prebisch, Bukele
[~] Descripción detallada P6 (Ayuda Futuro) — carrera, postgrad España

  GRAPHIFY — mi-criterio knowledge graph (iniciado Jun 14, 2026)
  ──────────────────────────────────────────────────────────────
  [!] PRIVACIDAD (2026-08-01): graphify-out/ SACADO del repo + gitignored.
      El grafo replica TODO el contenido del repo → arrastra PII (nombre legal
      completo, colegios, empleadores) y, antes del scrub, SSIDs de casa. graph.json
      y graph.html son un dossier de identidad geolocalizable.
  [ ] SESIÓN PROPIA: hacer graphify PUBLICABLE antes de volver a trackearlo.
      · Decidir qué es publicable vs privado (¿nombre legal? ¿colegios? ¿empleadores?)
      · Pipeline de scrub/anonimizado en la generación, no a mano post-hoc
      · Solo entonces quitar de .gitignore lo que sea seguro
  [ ] RESTMO-MONITOR REPO CLEANUP (para futura publicación en GitHub):
      · Crear .gitignore en ~/Codes/restmo-monitor/ ANTES de `git init`
      · Excluir: devices.json, tinytuya.json, *.key, .env, *.db (water_flow.db)
      · Proyecto luce listo para ser público (device ya sin pairing, claves rotadas)
  [ ] CRÍTICO: Resolver 113 nodos débilmente conectados
     · ¿Qué edges faltan para conectar Identidad, Puntos ciegos, Stack técnico al grafo?
     · ¿Hay nodos que sobren y deban eliminarse?
  [ ] CRÍTICO: Cohesión baja en comunidades grandes — ¿split o dejar?
     · "CV English & Career History" (cohesion 0.05) — muy suelta, ¿dividir?
     · "Repo Governance & Backup" (cohesion 0.09) — misma pregunta
  [ ] VERIFICAR: 2 edges INFERRED en "Plan Stack IA Local CPU-only"
     · ¿Son correctos los links a Stack IA Veredicto y P2 Programacion?
  [ ] VERIFICAR: el nodo de identidad (nombre legal) como único puente CV↔roles
     · ¿Las comunidades CV-documento y role-narratives deben enlazarse directamente?
  [ ] VERIFICAR: ¿Hay temas/proyectos enteros ausentes del grafo?
     · Nesting engine (C# AutoCAD plugin), trabajo específico sector energía, otros
  [ ] REVISAR: 5 conexiones sorprendentes — confirmar que son correctas
  [ ] EVALUAR: ¿Fusionar o renombrar alguna de las 22 comunidades?
  [ ] Leer sección "Knowledge Gaps" en graphify-out/GRAPH_REPORT.md
  → Grafo vive en: graphify-out/graph.html + GRAPH_REPORT.md + graph.json
  → Para actualizar: /graphify --update

  MEMORIA E INTEGRACIÓN IA
  ──────────────────────────────────────────────────────────────
  [x] Crear guía cross-AI para inbox integration (@inbox/chatgpt-memory.md)
     · Explica cómo ChatGPT, DeepSeek, Ollama pueden contribuir a mi-criterio
     · Template de formato para sesiones (DD-MM-YY_topic.md)
     · Integración con /process-inbox workflow
     · Ejemplos prácticos de P1-P6 conversaciones
  [ ] Docstring en perfil_maestro.txt para mencionar cross-AI capability
  [ ] Crear shortcut/alias para copiar guide cuando se abre nueva sesión ChatGPT
  [ ] Documentar las 356 convs ChatGPT + 121 DeepSeek como fuentes de esta arquitectura

  P6 VIDA PERSONAL / ADMIN / POSGRADO Y EMPLEO
  ─────────────────────────────────────────────────────────────────
  [ ]  Acomodar CVs en Canva
  [ ]  Migrar docs de OneDrive a Keeper
  [ ]  Actualizar perfil Indeed, LinkedIn, OCC y CompuTrabajo
  [x]  Generar contraseña VeraCrypt y almacenar en keeper
  [ ]  PENDIENTE BACKUP: Montar backup_critico.vc → correr Krokiet → eliminar PAP.zip (duplicado de PAP/) → desmontar
       · PAP/ (114MB, 53 archivos) = copia primaria. PAP.zip en raíz = redundante, borrar.
       · Comando mount: veracrypt backup_critico.vc /mnt/backup && ~/tools/krokiet
  [ ] Inventario de programas de posgrado en energía (México, Europa, Australia, etc.)
  [ ] Inventario de becas con fechas de cierre (CONAHCyT, Fulbright, DAAD, CONACYT-SENER)
  [~] CV actualizado con enfoque en energías renovables
     · Arquitectura /P6/cv creada ✓
     · roles/role_encoretools_cnc_programmer.md — completo v1.0 ✅
     · roles/role_tdi_biomedical.md — completo v1.0 ✅
     · roles/role_moldtech_thermoforming.md — skeleton v0.3 (voice session needed)
     · roles/role_pap_iteso_entreamigos.md — completo v1.0 ✅
     · roles/role_automotive_mechanic_2021.md — minimal v0.1 (short voice session)
     · roles/INDEX.md — tracker creado ✓
     · Todos los skeletons estandarizados al formato EncoreTools v1.0 ✓
     · Templates IT y Software tracks creados ✓
     · roles/role_performance_designs_mexico.md — completo ✓
     · skills_master.md, education_master.md — completos ✓
     · PerfilCVs_Descripciones.md — 4 perfiles bilingüe ✓
     · Contenido pendiente de integrar en Canva:
       — Programador C# · American Industries / Performance Designs
           Mayo 2025 a Marzo 2026
           Desarrollo de software en C# para corte laser de telas para paracaídas.
           Mantenimiento especializado de servidores de datos industriales.
       — Operador CNC / Técnico Mecánico · Moldtech S. de R.L.
           Mayo 2022 a Agosto 2022 / Agosto 2024 a Diciembre 2024
           Producción en serie plásticos por termoformado, manejo de CNC
           (cambio herramientas, fixtures, centros, set-up completo),
           metrología (Vernier, micrómetro, comparador óptico),
           proyectos de ensamble, soldadura, sujeciones.
  [ ] Statement of purpose — borrador inicial
  [ ] Actualizar LinkedIn e Indeed con perfil de ingeniería en energía.

  P6 BÚSQUEDA DE EMPLEO — EMPRESAS TARGET
  ─────────────────────────────────────────────────────────────────
  [x]  Crear directorio /P6/cv/companies/
  [x]  Continental — perfil + carta de presentación redactados (REF95136I, San Luis Potosí)
       · cover letter con lente solarpunk ✓
       · perfil profesional enhanced ✓
       · pendiente: subir a portal Continental y aplicar
  [~]  Siemens Energy — perfil general en redacción (sin vacante específica)
       · siemens_energy_profile.md en progreso
       · título confirmado: "Mechanical Engineer — Sustainable Energy Systems"
       · pendiente: completar secciones valores, skills, adjunto
       · pendiente: investigar portal jobs.siemens-energy.com
  [ ]  Ørsted — pendiente (objetivo explícito en SECTOR_OBJETIVO)
  [ ]  Iberdrola — pendiente
  [ ]  Empresas energía MX — pendiente (listado por definir)


  FINANZAS
  ─────────────────────────────────────────────────────────────────
  [ ]  Investigar y decidir estrategia ETFs
     · LuismiNegocios — candidatos a revisar:
         ITOT  (mercado total USA)
         S&P500 (500 más grandes USA)
         IYW / SOXX (semiconductores — alta volatilidad)
         EEM   (diversificación mercado global emergente)
         VIG   (altos dividendos)
         ETFs bonos / renta fija (pendiente identificar ticker)
         XBI   (tendencias: IA, energía renovable, etc.)
     · DeepSeek — ETFs renovables a analizar:
         INRG  (solar, eólica, hidrógeno, almacenamiento)
         RENG  (similar iShares, menor gasto)
         RNRG  (productores energía renovable)
         WREN  (menor sesgo USA, diversificación global)
         RNWZ  (parques eólicos, flujos estables contratos LP)
         RAYS  (específico solar)


  DECISIONES TOMADAS — NO REABRIR
  ─────────────────────────────────────────────────────────────────
  [x]  DE para hardware real: COSMIC (Wayland, tiling nativo, out-of-box)
  [x]  GPU futura: AMD (mejor soporte Linux)
  [x]  Boot: dual boot Windows + Arch (no triple)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  NOTAS DE FUSIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  · Los ítems de VM fibonacci ya completados se marcan [x] según
    el cierre_sesion_fibonacci.html
  · "Instalar Ollama", "claude-mem", "everything-claude-code" vienen
    del perfil_maestro pero no aparecían en session_diff — añadidos
  · "Terminar de configurar i3" viene del perfil_maestro
  · Picom deferido a hardware real (incompatible con VirtualBox GPU)
    — no se lista porque COSMIC reemplaza esa necesidad
  · LazyVim aparece en 3 fuentes — unificado en una sola entrada
  · "Configurar Git en VM" y "Neovim config" vienen de memorias
    de sesiones anteriores donde quedaron pendientes
