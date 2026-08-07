# inbox/06-08-26_zsh-dropdown-fzf-tab-setup.md

**Fecha:** 2026-08-06 · **Lens:** P2-P8 (desarrollo + soberanía)
**Tags:** zsh, shell, autocomplete, fzf-tab, tealdeer, terminal, discovery-learning
**Archivos generados:** zsh-dropdown-autocomplete-setup.md — spec técnica completa con diagnóstico y config

## Contexto

Configuración de autocompletado avanzado en zsh con dropdown navegable (fzf-tab) + preview de man pages / tldr. Objetivo dual: velocidad de tipeo + aprendizaje de comandos Linux por descubrimiento. Mantiene intacto zsh-autosuggestions (sugerencia inline gris).

## Puntos clave

- **Stack:** fzf-tab (dropdown) + fzf (motor) + tealdeer (tldr, preview rápido) + man (fallback)
- **Trigger:** Tab (estándar zsh, no automático) → dropdown con historial primero, sistema después
- **Preview:** tldr si existe, fallback a man; navegación 100% teclado (Ctrl+J/K para arriba/abajo, Ctrl+H/L para cambiar grupo)
- **Instalación:** fzf-tab requiere diagnóstico previo (paso 4 del spec) para conocer plugin manager (manual git / zinit / antidote / oh-my-zsh)
- **Orden crítico:** compinit → zsh-autosuggestions → fzf-tab (en ese orden en .zshrc)
- **No tocar:** zsh-autosuggestions existente; fzf-tab es layer encima, no reemplazo

## Decisiones tomadas

- [x] Rechazar zsh-autocomplete (dropdown automático sin Tab, conflictos conocidos con autosuggestions)
- [x] Rechazar keybindings mouse, usar Tab + Ctrl modifiers (100% teclado, aprendizaje motor)
- [x] Incluir grouping de historial vs sistema (visualiza diferencia, aprende scope)
- [x] Usar tldr + fallback man (tldr es orientado ejemplos, man es referencia completa)

## Pendientes

- [ ] Ejecutar diagnóstico paso 4 (confirmar plugin manager)
- [ ] Instalar fzf + tealdeer con pacman
- [ ] Instalar fzf-tab según el plugin manager detectado
- [ ] Agregar zstyle config en .zshrc (orden de sourcing es crítico)
- [ ] Ejecutar testing checklist (paso 9) y confirmar cada punto
- [ ] Documentar bindings finales (Tab, Ctrl+J/K, Ctrl+H/L, Enter, Esc) en .zshrc como comentario para referencia futura

## Insight cross-lens

**P2 + P8:** Terminal optimizada para descubrimiento acelera aprendizaje de Linux (P2), mientras que 100% teclado sin mouse preserva soberanía de control (P8 — flujo manual, auditable). Evita "click negro" en UI de terminal.

---

# inbox/06-08-26_chrome-vs-privacidad-decision.md

**Fecha:** 2026-08-06 · **Lens:** P2-P8 (soberanía, filosofía)
**Tags:** navegador, privacidad, chrome, firefox, ungoogled-chromium, copyleft, trade-off
**Archivos generados:** ninguno (decisión, no spec)

## Contexto

Necesidad de fallback a Chrome porque ciertos sitios (unsubscribe links de SendGrid, CleverTap) no cargan en Firefox privado. Tensión: máxima privacidad/soberanía vs. compatibilidad web práctica.

Dos URLs específicas fallan:
- `u54482689.ct.sendgrid.net/ls/click?...` (SendGrid tracking link)
- `eu1-unsubscribe.clevertap-pages.com/email/unsubscribe/...` (CleverTap detection)

Ambas detectan fingerprinting defensivo: JavaScript + telemetría habilitada = "navegador normal", JavaScript ausente + `privacy.resistFingerprinting = true` = "bot/usuario privacidad-first".

## Puntos clave

- **Raíz del problema:** No es incompatibilidad técnica, es **detección antibot**. Esos servicios bloquean navegadores con privacidad máxima porque los confunden con scrapers.
- **google-chrome desde AUR:** Descarga binario precompilado de Google → telemetría integrada → contradice filosofía declarada (copyleft + soberanía)
- **Alternativas con privacidad:**
  - Firefox dual-mode (perfil "compatibility" sin `privacy.resistFingerprinting`) → 0 fricción, mismo open source
  - Ungoogled-Chromium (AUR compilado localmente) → Chromium sin Google, pero 1-2h compilación en i7-8665U
  - Chromium-bin (pacman official) → Chromium puro, binario Arch (no auditado por ti, pero no Google)
  - Brave (oficial) → Privacidad integrada, pero telemetría Brave, no open source puro

## Decisiones tomadas

- [x] NO instalar google-chrome (viola filosofía)
- [x] Opción primaria: Firefox dual-mode (perfil "compatibility") → máxima compatibilidad con filosofía
- [x] Opción fallback: Chromium-bin si Firefox dual-mode falla → no Google, setup rápido
- [x] Evitar Ungoogled-Chromium por ahora (1-2h compilación innecesaria si dual-mode funciona)

## Pendientes

- [ ] Crear perfil Firefox "compatibility" (sin privacy.resistFingerprinting)
- [ ] Probar los dos links en perfil-compat
- [ ] Si funcionan: uso Firefox dual-mode únicamente (philosophia preservada)
- [ ] Si fallan: evaluar Chromium-bin vs. otro approach
- [ ] Documentar alias en .zshrc: `alias firefox-compat='firefox -P compatibility --new-instance'`

## Insight cross-lens

**P8 + P2:** Trade-off real entre soberanía (no usar Chrome) vs. practicidad (acceso a sitios). Solución: Firefox dual-mode preserva ambas — copyleft + funcionalidad, sin instalación nueva. Aprendizaje: **no todo problema técnico necesita herramienta nueva; a veces es re-configuración**.

---

# inbox/06-08-26_firefox-clevertap-unsubscribe-troubleshooting.md

**Fecha:** 2026-08-06 · **Lens:** P2 (debugging)
**Tags:** firefox, firejail, ublock-origin, clevertap, session-cookies, sandbox
**Archivos generados:** ninguno (diagnóstico live)

## Contexto

Link de unsubscribe CleverTap (`eu1-unsubscribe.clevertap-pages.com`) devuelve error "We could not retrieve your email address" en Firefox con perfil "compatibility". Advertencias:
1. "Disable ad-blockers if enabled" (uBlock Origin activo)
2. "Enable Javascript on your browser" (JS aparentemente deshabilitado)
3. "Check your internet connection" (falso; es detección de contexto de sesión)

La captura de pantalla muestra Firefox ejecutado con **`firejail`** (`firejail /usr/bin/firefox -P compatibility --new-instance`), que:
- Intercepta cookies de sesión (necesarias para el flujo de unsubscribe)
- Modifica user-agent implícitamente
- Confunde con AppArmor/SELinux ("Cannot confine the application using AppArmor")
- Ralentiza en hardware ULV (i7-8665U)

## Puntos clave

- **Culpable principal:** Firejail está sandboxing Firefox → rompe session state
- **uBlock Origin secundario:** Puede estar bloqueando scripts de tracking necesarios para el flujo (no es "publicidad", es infraestructura de sesión)
- **Solución quirúrgica:** Ejecutar Firefox sin firejail para links de unsubscribe
- **Pregunta crítica:** ¿Por qué firejail está configurado para Firefox? (sandbox útil solo si ejecutas binarios untrusted; Firefox es confiable)

## Decisiones tomadas

- [x] Diagnosticar que firejail es el bloqueante (no Firefox mismo)
- [x] Crear alias sin firejail: `firefox-compat='firefox -P compatibility --new-instance'`
- [x] Crear alias con firejail si deseas sandbox: `firefox-private='firejail firefox -P default --new-instance'`

## Pendientes

- [ ] Verificar si firejail está hardcodeado en .zshrc / .bashrc / .config
- [ ] Ejecutar Firefox sin firejail: `/usr/bin/firefox -P compatibility --new-instance &`
- [ ] Probar link CleverTap de nuevo
- [ ] Si funciona: problema confirmado (firejail)
- [ ] Si falla: deshabilitar uBlock Origin temporalmente y reintentar
- [ ] Documentar decisión final: firejail + Firefox = incompatible para unsubscribe flows

## Insight cross-lens

**P2 + P8:** Sandbox (firejail) es medida de defensa, pero puede ser **excesiva** en hardware limitado y rompe flujos de navegación normal. Aprendizaje: **seguridad en capas** — AppArmor/SELinux ya sandbokean COSMIC; firejail adicional es redundancia que daña usabilidad. Evaluar threat model real vs. herramientas defensivas genéricas.

---

## Notas para siguiente inbox

- Resolver confirmación: ¿firejail era necesario? ¿Firefox sin firejail funciona con unsubscribe?
- Decisión final sobre navegador fallback (Firefox dual-mode vs. Chromium-bin)
- Documentar flujo final de unsubscribe en wiki P8 (caso de uso: batch unsubscribe links)
