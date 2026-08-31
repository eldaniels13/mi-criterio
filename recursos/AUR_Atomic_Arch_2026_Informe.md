## Informe: Ataque a la cadena de suministro del AUR de Arch Linux — "Atomic Arch" (junio 2026), estado a 18 de julio de 2026

### TL;DR
- **El incidente ES REAL y está bien documentado**: Sonatype lo bautizó "Atomic Arch" el 11 de junio de 2026. No obstante, la descripción del usuario contiene imprecisiones técnicas: el paquete npm "atomic-lockfile" NO roba credenciales por sí mismo, sino que actúa como cargador de un binario ELF en Rust (el infostealer real); y la horquilla "400–1500" refleja la escalada de estimaciones a lo largo de los días (el recuento comunitario consolidado más autoritativo enumera finalmente **1.937 nombres de paquetes AUR afectados**, "casi 2.000", según la lista cscs referenciada por los avisos de CachyOS/Arch/Garuda).
- **A mediados de julio de 2026 NO existe ningún anuncio oficial de "todo resuelto" en archlinux.org/news**: el único post oficial sigue siendo el del 12 de junio, que aún describe la situación como activa, y los registros de cuentas nuevas del AUR siguen suspendidos. Los repositorios oficiales (`pacman -S` sobre core/extra/multilib) NUNCA se vieron afectados.
- **Sí existen herramientas reales de detección e IOCs publicados**; la herramienta "aur-malware-check" existe y es real. Recomendación clave: si instalaste o actualizaste cualquier paquete AUR entre el ~10 y el 16 de junio de 2026, audita el host y rota credenciales, porque el malware ya se habrá ejecutado en el momento de la compilación.

---

### Key Findings — Confirmado vs. no verificado

**CONFIRMADO (alta confianza, múltiples fuentes primarias):**
- Campaña real "Atomic Arch", nombrada por Sonatype, descubierta por el ingeniero Eyad Hasan el 11 de junio de 2026. Sonatype la rastrea como **Sonatype-2026-003775, CVSS 8.7**; la segunda ola la rastrea por separado como **Sonatype-2026-003808**. No hay CVE asignado.
- Vector: adopción/toma de control de paquetes AUR huérfanos + **falsificación de metadatos de commits git** para suplantar a mantenedores legítimos. Modificación del PKGBUILD/`.install` para ejecutar `npm install atomic-lockfile` (ola 1) o `bun install js-digest`/`lockfile-js` (ola 2).
- El PKGBUILD malicioso NO contiene el malware; solo añade la descarga de un paquete npm/bun cuyo hook `preinstall` ejecuta un binario ELF (`src/hooks/deps`). Esto es lo que le permitió evadir la detección basada en cambios en el código del paquete.
- Post oficial de Arch: **"Active AUR malicious packages incident", 12 de junio de 2026, por Campbell Jones**.
- Repos oficiales intactos; el incidente solo afecta al AUR.

**PARCIALMENTE CORRECTO / MATIZADO respecto a la descripción del usuario:**
- *"atomic-lockfile roba SSH keys, tokens, credenciales"* — impreciso. El paquete npm es únicamente el vehículo; el robo lo realiza el binario ELF en Rust. Como resume The Hacker News: *"Independent researcher Whanos reverse-engineered the deps payload and describes a Rust credential stealer aimed at developer workstations and build systems."*
- *"400–1500 paquetes"* — refleja la escalada del recuento: ~20 (estimación inicial de Sonatype) → 408 → 900 → 1.500+ → lista comunitaria consolidada de **1.937**.
- *"still active as of Jun 29"* — no confirmado por ninguna fuente de esa fecha exacta. La actividad aguda se calmó entre el 14 y el 19 de junio; a mediados de julio el incidente está **contenido pero no declarado oficialmente resuelto**.

---

### Details

**Cronología:**
- **11 jun 2026**: Sonatype descubre la campaña (ola 1, npm `atomic-lockfile`). ~20 paquetes iniciales, que rápidamente escalan a 408.
- **12 jun 2026**: post oficial de Arch. Segunda ola con Bun (`js-digest`/`lockfile-js`). El recuento sube a 900 y luego a 1.500+. La cadencia de publicación en npm demuestra un atacante iterando en horas, no días (según análisis de Corgea): `js-digest` creado 2026-06-12T10:21:34Z y retirado 2026-06-12T11:53:23Z (versión maliciosa 4.2.2); `lockfile-js` creado 2026-06-12T13:01:03Z y retirado 2026-06-12T16:29:49Z (versión maliciosa 1.4.2).
- **13–14 jun 2026**: tercera ola con código ofuscado (ht-browser-bin, paquetes Node.js, Plasma 6 applets, Firefox, LibreWolf, NeoVim). Detectada por el desarrollador a821 y por Nicolas Boichat usando un modelo de IA local Gemma. La ofuscación incluía dividir la cadena `bun` como `'b''u''n'` y escapes hexadecimales para evadir escáneres de firmas.
- **14–16 jun 2026**: ola de spam ruso/profanidades en más de 70 paquetes (inyección de mensajes ofensivos en bashrc/zshrc/fish). Considerada por parte de la comunidad como trolling de baja gravedad, no robo de credenciales.
- **15 jun 2026**: Arch deshabilita el registro de cuentas nuevas del AUR (anuncio de Leonidas Spyropoulos "artafinde" en aur-general). Previamente se probó Anubis (anti-bot) sin éxito.
- **Mediados jul 2026**: sin post oficial de resolución; registros aún suspendidos (última confirmación explícita de "aún deshabilitado": LWN, 19 jun); incidente contenido.

**Detalles técnicos del malware (CONFIRMADO por ioctl.fail, Sonatype, Corgea, Cloud Security Alliance):**
- Payload ola 1: binario `deps`, **ELF64 PIE, Rust async, stripped, 3.040.376 bytes, SHA-256 `6144d433f8a0316869877b5f834c801251bbb936e5f1577c5680878c7443c98b`**. El mismo hash aparece en `atomic-lockfile/package/src/hooks/deps`.
- Payload ola 2 (js-digest): binario ELF distinto, reportado por The CyberSec Guru con SHA-256 `7883bda1ff15425f2dbe622c45a3ae105ddfa6175009bbf0b0cad9bf5c79b316` (confianza media: fuente única secundaria).
- **Roba**: cookies/tokens de navegadores Chromium, apps Electron (Slack, Discord, Teams), tokens de GitHub/npm/HashiCorp Vault, material de OpenAI/ChatGPT, claves SSH, credenciales cloud.
- **C2**: servicio oculto Tor `olrh4mibs62l6kkuvvjyc5lrercqg5tz543r4lsw3o6mh5qb7g7sneid.onion`, callback `POST /api/agent` vía transporte loopback/SOCKS en 127.0.0.1; exfiltración de archivos a `temp.sh` (`POST /upload`). El endpoint C2 está codificado dentro del propio ELF, no en el wrapper JS.
- **Persistencia**: unidades systemd con `Restart=always` (en `/etc/systemd/system/` como root, o en `~/.config/systemd/user/` como usuario).
- **Rootkit eBPF OPCIONAL**: solo se activa con root + CAP_BPF. `scales.bpf.c`, hooks a `getdents64`, mapas fijados `hidden_pids`/`hidden_names`/`hidden_inodes`. Oculta procesos/archivos/sockets y bloquea el debugging. Varios análisis señalan que los primeros reportes "sobrevendieron" el rootkit: es opcional y no se usa para escalar privilegios.
- Referencia a `/usr/bin/monero-wallet-gui`: posible criptominero de segunda etapa (no analizado a fondo).
- **Publisher npm**: `herbsobering` (mismo para `atomic-lockfile` y `js-digest`). Según The CyberSec Guru, esa cuenta también tiene una imagen de contenedor en GitHub (`herbsobering430`) que el análisis sugiere que funciona como shell inverso o herramienta proxy. `atomic-lockfile@1.4.2` tenía solo 134 descargas semanales en Socket antes de retirarse — la exposición real es la ruta de compilación del AUR, no las instalaciones directas de npm.

**¿Existe "atomic-lockfile" en npm?** Sí existió (ya retirado). Importante: NO está en OSV.dev ni en la GitHub Advisory Database bajo ese nombre; está documentado solo en prosa en Socket.dev y Sonatype. Por tanto no hay un feed estructurado (GHSA/OSV) que consultar para estos nombres.

**Aclaración sobre "arojas" (suplantación):** La cuenta `arojas` es un **mantenedor legítimo de KDE que fue SUPLANTADO** mediante falsificación de commits git — no fue comprometida ni es maliciosa. Aclarado por David Runge (dvzrv) en aur-general el 12 de junio. Cuentas atacantes reales: `krisztinavarga`, `franziskaweber`, `tobiaswesterburg`, `ellenmyklebust` (ola 1); `custodiatovar`, `veramagalhaes` (ola 2).

**¿Relación con "Shai-Hulud" o AtomicStealer/AMOS? (pregunta sobre conflación):**
- El prefijo "Atomic" es **coincidencia** con AtomicStealer/AMOS (stealer de macOS) — NO hay relación técnica. Es una conflación por el nombre.
- **Shai-Hulud** es un gusano de npm DISTINTO (septiembre y noviembre de 2025, con variantes en 2026) que se autopropaga usando tokens npm robados para republicar paquetes del mantenedor víctima. Mecanismo diferente; NO es lo mismo que Atomic Arch.
- Sí existe **similitud reportada con la campaña "IronWorm"** (mismo binario Rust+eBPF, C2 Tor en `/api/agent`, tradecraft de temp.sh y naming `atomic-*`). Textualmente (Hackread): *"While these methods look a lot like an older campaign called IronWorm, Sonatype has not officially linked Atomic Arch to a specific hacker group yet."*

**Herramientas de detección/remediación reales (respuesta directa sobre "aur-malware-check"):**
- **`lenucksi/aur-malware-check`** (Python 3.14+, solo stdlib): `python -m aur_check`, `--full`, `--refresh`, `--check-pkgbuild`. Consolida listas comunitarias (~1.619+ paquetes). SÍ existe.
- **`nightdevil00/AUR-Malware`**: script `check-atomic-arch_new.sh` que descarga listas de 4 fuentes; fallback local con ~1.935 paquetes; comprueba systemd, eBPF, cachés npm/bun/pnpm/yarn y conexiones al C2.
- **`jasonherald/atomic-arch-check`**: 1.717 paquetes con niveles de confianza; decodificador estático de la ofuscación de la ola 3 (sin ejecución).
- **`musqz/archcanary`** (bifurcación ampliada) y **`Sohimaster/traur`** (scoring de confianza AUR con hook ALPM).
- Listas comunitarias: gist de Kidev, lista **cscs** (referenciada por los avisos de CachyOS/Arch/Garuda), doc HedgeDoc `md.archlinux.org/s/SxbqukK6IA`.

**Estado de controles nuevos del AUR (a mediados de julio 2026):**
- **Ningún control permanente del lado servidor confirmado como implementado.** Concreto: (a) registro de cuentas deshabilitado (medida temporal); (b) merge request en curso en aurweb (#904) para exponer información de "adopción reciente" vía RPC y que helpers como paru muestren advertencias; (c) característica ya lanzada en **yay v13** que muestra la fecha de última modificación del PKGBUILD.
- **2FA obligatorio para mantenedores, límites/retrasos en la adopción de huérfanos, revisión obligatoria de PKGBUILD**: solo en DISCUSIÓN en la lista de correo, no implementados. Arch descartó explícitamente exigir nombres reales o verificación de identidad. (Nota: fue Fedora, no Arch, quien decidió exigir 2FA a su grupo "provenpackager" el 23 de junio — no confundir.)

---

### Recommendations

**Etapa 1 — Verificación inmediata (todos los usuarios AUR):**
```bash
# ¿Qué paquetes AUR/foráneos tengo?
pacman -Qm

# Instalaciones/actualizaciones en la ventana del ataque (10–16 jun 2026)
grep -E '2026-06-1[0-6].*(installed|upgraded)' /var/log/pacman.log

# Buscar el patrón malicioso en cachés de helpers AUR
grep -RInE 'atomic-lockfile|js-digest|lockfile-js|ansi-colors|nextfile-js|npm install|bun install|src/hooks/deps' \
  ~/.cache/yay ~/.cache/paru ~/.cache/pikaur /tmp 2>/dev/null

# Residuo en cachés npm/bun (un hit indica que el paquete se resolvió)
grep -RInE 'atomic-lockfile|js-digest|lockfile-js' ~/.npm ~/.bun 2>/dev/null
```

**Etapa 2 — Búsqueda de compromiso/persistencia:**
```bash
# Servicios systemd sospechosos
grep -RIn 'Restart=always\|ExecStart=' /etc/systemd/system ~/.config/systemd/user 2>/dev/null

# Artefactos del rootkit eBPF (solo relevante si corrió como root)
ls -la /sys/fs/bpf/hidden_* 2>/dev/null

# Conexiones al C2/exfiltración
ss -tnp | grep -E 'temp.sh|olrh4mibs62l6kkuv'

# Binario del payload por tamaño+hash conocido
find / -type f -size 3040376c 2>/dev/null -exec sha256sum {} \; \
  | grep -i 6144d433f8a0316869877b5f834c801251bbb936e5f1577c5680878c7443c98b
```

**Etapa 3 — Usar una herramienta comunitaria:**
```bash
git clone https://github.com/lenucksi/aur-malware-check
cd aur-malware-check && python -m aur_check --full
```

**Etapa 4 — Si un paquete marcado se ejecutó (asume compromiso de credenciales):**
- Rota TODO: claves SSH, PATs de GitHub, tokens npm/Vault, credenciales cloud (AWS/GCP/Azure), sesiones de navegador, tokens de Slack/Discord/Teams, credenciales Docker/Podman.
- Si el payload corrió como root (rootkit eBPF posible): NO confíes en la limpieza. Reinstala desde medios confiables (ISO de Arch), monta el FS y elimina unidades systemd maliciosas y binarios bajo `/var/lib/`.
- `pacman -Rns <paquete>` NO limpia el host tras la ejecución; elimina archivos conocidos pero no prueba que el sistema esté limpio.

**Etapa 5 — Mitigación específica para tu caso (Arch + COSMIC + yay/paru en máquina de desarrollo):**
- Actualiza a **yay v13+** (muestra la fecha de última modificación del PKGBUILD).
- SIEMPRE revisa el diff del PKGBUILD y de los `.install` antes de construir; en paru usa `--review` / en yay no desactives el prompt de revisión de diffs. Desconfía especialmente de paquetes recién adoptados, con cambio de email del mantenedor, o que de repente añaden `npm`/`bun`/`node` como dependencia sin motivo funcional.
- Considera un hook `PreTransaction` de pacman que aborte la transacción si un paquete está en la lista de bloqueo comunitaria (el repo nightdevil00/AUR-Malware incluye un `install-hook.sh` para esto).
- Toma snapshots (Snapper/Timeshift) antes de actualizaciones AUR (no protege credenciales ya robadas, pero acelera la recuperación).
- **Umbral de re-evaluación**: relaja la vigilancia solo cuando Arch publique un post oficial de resolución en archlinux.org/news **o** reactive el registro de cuentas del AUR. Endurece de nuevo si aparece una nueva ola reportada en la lista aur-general.

---

### Precedentes y contexto (base rate del modelo de confianza del AUR)
- **Julio 2025 (precedente real citado por el usuario)**: incidente `librewolf-fix-bin`/`firefox-patch-bin`/`zen-browser-patched-bin` (usuario `danikpapas`) que instalaba **CHAOS RAT** vía un repo de GitHub; 3 paquetes, subidos el 16 jul y retirados el 18 jul 2025 (~46 h). Confirmado por BleepingComputer y los mantenedores del AUR.
- **2018**: adopción maliciosa del paquete `acroread` (visor PDF) — mismo vector de adopción de huérfanos, a menor escala.
- **Modelo de confianza del AUR**: los paquetes no están vetados ("use at your own risk"); los PKGBUILD son código ejecutable que corre en tu máquina durante la compilación. La adopción de huérfanos no tiene revisión, ni vouching, ni periodo de retardo — la debilidad estructural que Atomic Arch industrializó (había ~13.000 paquetes huérfanos y >107.000 paquetes en el AUR en el momento del ataque).

---

### Caveats
- Las cifras de "paquetes afectados" varían mucho según la fuente (20/408/900/1.500/1.937) por la naturaleza cambiante del recuento y la eliminación de commits. **No hay una lista oficial única y definitiva de Arch**; las listas más completas son comunitarias, y muchas incluyen paquetes huérfanos que quizá nadie tenía instalado.
- No hay atribución a un actor concreto. La sofisticación (Rust + eBPF + Tor) sugiere un adversario con recursos, pero es especulación.
- Varias fuentes son blogs de vendedores de seguridad (Sonatype, StepSecurity, Corgea, Rescana, The CyberSec Guru) con incentivo comercial; los hechos centrales están corroborados por fuentes primarias (post oficial de Arch, hilo aur-general, análisis técnico de ioctl.fail, cobertura de LWN/Phoronix/The Register/BleepingComputer).
- Los hashes SHA-256 (especialmente el de la ola 2) provienen de trackers comunitarios/blogs; verifícalos contra la fuente antes de usarlos como IOC de bloqueo en producción.
- No se pudo confirmar de forma definitiva ni la reactivación de registros ni una ola distinta en julio; la referencia "Update 15/07/2026" en un blog (Peq42) parece ser una re-cita mal fechada del evento de spam ruso de mediados de junio, no una ola nueva.