# Arch Linux Security Audit — fibonacci
**Fecha:** 2026-05-23  
**Host:** fibonacci (Dell Latitude 5400, i7-8665U, ~32 GB RAM)  
**OS:** Arch Linux, kernel 7.0.9-arch2-1 (post-reboot)  
**DE:** COSMIC (Wayland)  
**Usuario:** eldaniels  
**Motivo:** Rumores en internet sobre vulnerabilidades en Linux; auditoría proactiva

---

## Estado inicial antes de la auditoría

| Componente | Estado |
|---|---|
| Kernel | 7.0.9-arch2-1 (después de reboot previo) |
| Firewall | Ninguno activo |
| DNS | Resolución vía el ISP sin cifrado |
| Docker group | eldaniels era miembro (= root equivalente) |
| rkhunter | No instalado |
| ClamAV | No instalado |
| sysctl hardening | Sin configurar |
| Firefox plugins | uBlock Origin + AdBlock + AdGuard AdBlocker (redundantes) |
| Ollama | Corriendo, bind a loopback (127.0.0.1:11434) — OK |
| Spotify | Escuchando en dos puertos no-loopback (zeroconf/mDNS) |
| Paquetes | Sistema completamente actualizado |

---

## Vulnerabilidades identificadas

### Crítica
- **Docker group**: eldaniels estaba en el grupo `docker` → acceso root sin contraseña vía `docker run --privileged`. Eliminado inmediatamente.

### Alta
- **Sin firewall**: ningún filtrado de paquetes entrantes activo.
- **DNS sin cifrar**: el ISP podía ver y manipular todas las consultas DNS. Sin DNSSEC, sin DoT.

### Media
- **Tres adblockers simultáneos**: AdBlock + AdGuard + uBlock Origin → conflictos y memoria desperdiciada.
- **Kernel sysctl sin endurecer**: parámetros por defecto, permisivos en redirecciones ICMP y martian packets.
- **Sin rkhunter**: sin baseline de binarios del sistema.
- **Sin ClamAV**: sin escaneo de archivos descargados.

### Baja / Informativa
- **Spotify zeroconf**: Broadcasting en red local. Aceptable en red doméstica, riesgo en redes públicas.
- **Firefox about:config**: WebRTC habilitado (riesgo de IP leak), fingerprinting sin resistencia, geolocalización activa.

---

## Correcciones aplicadas

### 1. Docker group — eliminado

```bash
sudo gpasswd -d eldaniels docker
# o:
sudo deluser eldaniels docker
```

**Por qué importa:** Docker monta namespaces con acceso root al host. Cualquier usuario en el grupo docker puede escalar privilegios trivialmente.

---

### 2. Firewall — nftables (Arch default)

#### Historia del proceso
Se intentó instalar **UFW** primero, pero falló con:
```
Warning: Extension icmp revision 0 not supported, missing kernel module?
```

**Causa raíz:** UFW usa `iptables-legacy`. Arch Linux moderno usa `iptables-nft`. Son incompatibles.

**Solución:** Se eliminó UFW y se adoptó **nftables** directamente, que es el framework nativo del kernel Linux.

```bash
sudo pacman -R ufw
sudo pacman -S nftables
sudo systemctl enable --now nftables
```

#### Contenido final de `/etc/nftables.conf`

```nft
#!/usr/bin/nft -f
destroy table inet filter
table inet filter {
  chain input {
    type filter hook input priority filter; policy drop;
    ct state invalid drop comment "early drop of invalid connections"
    ct state { established, related } accept comment "allow tracked connections"
    iif "lo" accept comment "allow from loopback"
    meta l4proto { icmp, ipv6-icmp } accept comment "allow icmp"
    meta pkttype host limit rate 5/second burst 5 packets counter reject with icmpx admin-prohibited
    counter
  }
  chain forward {
    type filter hook forward priority filter; policy drop;
  }
}
```

**Nota:** Se eliminó la regla `tcp dport ssh accept` porque no hay `sshd` corriendo en el sistema. La regla era innecesaria y abre superficie de ataque si sshd se instalara en el futuro sin configuración adicional.

**Nota sobre Docker:** Docker crea sus propias tablas nftables (`table ip filter`, `table ip nat`, `table ip6 filter`, `table ip6 nat`). Estas las gestiona el daemon de Docker automáticamente — no tocar.

#### Problema durante instalación: kernel/modules version mismatch

Durante la sesión previa (antes del reboot), nftables.service fallaba con:
```
nftables: Failed to start nftables
```

**Causa real:** El kernel corriendo era `7.0.5-arch1-1` pero los módulos instalados eran para `7.0.9-arch2-1`. No había directorio en `/lib/modules/7.0.5-arch1-1/`. Esto causó que todos los módulos de netfilter fallaran.

**Solución:** Reboot. El kernel cargó la versión `7.0.9-arch2-1` con sus módulos completos.

---

### 3. DNS hardening — Quad9 + DNS-over-TLS + DNSSEC

#### Historia del proceso

**Problema 1:** Intentar editar `/etc/systemd/resolved.conf` con nano pero sin guardar los cambios (dos veces).

**Solución:** Usar drop-in config en `/etc/systemd/resolved.conf.d/` (método preferido de systemd).

**Problema 2:** Heredoc con `sudo tee` fallaba — espacios al inicio del `EOF` lo hacían no reconocerse como terminador. También `}EOF` en la misma línea causó malformación.

**Solución:** Usar `printf` en lugar de heredoc:

```bash
sudo mkdir -p /etc/systemd/resolved.conf.d/
printf '[Resolve]\nDNS=9.9.9.9#dns.quad9.net\n149.112.112.112#dns.quad9.net\nFallbackDNS=1.1.1.1#cloudflare-dns.com\nDNSOverTLS=yes\nDNSSEC=yes\n' | sudo tee /etc/systemd/resolved.conf.d/dns-quad9.conf
```

#### Archivo `/etc/systemd/resolved.conf.d/dns-quad9.conf`

```ini
[Resolve]
DNS=9.9.9.9#dns.quad9.net
149.112.112.112#dns.quad9.net
FallbackDNS=1.1.1.1#cloudflare-dns.com
DNSOverTLS=yes
DNSSEC=yes
```

**Problema 3:** Después del reboot, `resolvectl status` mostraba como DNS activo: `****:****::2` — el servidor IPv6 de el ISP via DHCPv6.

**Causa:** Solo se había configurado `ipv4.ignore-auto-dns yes` en NetworkManager, pero no para IPv6.

**Solución:**
```bash
nmcli connection modify **** ipv6.ignore-auto-dns yes
nmcli connection up ****
```

#### Configuración NetworkManager aplicada

```bash
nmcli connection modify **** \
  ipv4.dns "9.9.9.9 149.112.112.112" \
  ipv4.ignore-auto-dns yes \
  ipv6.ignore-auto-dns yes
```

#### Verificación final

```bash
resolvectl status | grep -A5 "wlo1"
```
```
Link 4 (wlo1)
    Current Scopes: DNS LLMNR/IPv4 LLMNR/IPv6 mDNS/IPv4 mDNS/IPv6
         Protocols: +DefaultRoute +LLMNR +mDNS +DNSOverTLS DNSSEC=yes/supported
Current DNS Server: 9.9.9.9
       DNS Servers: 9.9.9.9 149.112.112.112
     Default Route: yes
```

**DNS totalmente limpio: Quad9 con cifrado DoT + DNSSEC activo.**

#### Por qué Quad9
- Filtra dominios maliciosos conocidos (blocklist de amenazas activa)
- Sin logs de usuario
- DNSSEC + DoT soportados
- Operado por fundación suiza sin ánimo de lucro

#### Arquitectura de la solución

```
Aplicación
    ↓
systemd-resolved (127.0.0.53)
    ↓ TLS cifrado
Quad9 (9.9.9.9) / Cloudflare fallback (1.1.1.1)
    ↓
Root servers
```

El router de el ISP ya no participa en la resolución DNS.

---

### 4. rkhunter — baseline + primer escaneo

```bash
sudo pacman -S rkhunter
sudo rkhunter --update
sudo rkhunter --propupd    # crea baseline de 114 binarios
sudo rkhunter --check --skip-keypress
```

#### Resultado del primer escaneo

```
Files checked: 114
Suspect files: 3
Rootkits checked: 486
Possible rootkits: 0
```

#### Análisis de los 3 "suspect files" (todos falsos positivos)

| Archivo | Warning | Causa real |
|---|---|---|
| `/usr/bin/egrep` | "replaced by a script" | GNU convirtió egrep a wrapper de `grep -E` intencionalmente |
| `/usr/bin/fgrep` | "replaced by a script" | Igual, wrapper de `grep -F` |
| `/usr/bin/ldd` | "replaced by a script" | ldd siempre ha sido un shell script en glibc |

#### Otros warnings del log (todos benignos)

| Warning | Causa |
|---|---|
| passwd/group: no copy exists | Primera ejecución, sin baseline previo para comparar |
| SSH PermitRootLogin not set | No hay sshd corriendo — advertencia irrelevante |
| SSH Protocol not set | Igual, sshd no instalado/corriendo |
| `/etc/.updated` hidden file | Archivo creado por pacman hooks de Arch |
| `.k5identity.5.gz`, `.k5login.5.gz` | Man pages de Kerberos que empiezan con punto — normal |

**Conclusión: 0 rootkits, 0 amenazas reales.**

---

### 5. sysctl kernel hardening

Archivo creado: `/etc/sysctl.d/99-security.conf`

```ini
kernel.kptr_restrict = 2
kernel.dmesg_restrict = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.all.log_martians = 1
net.ipv4.tcp_syncookies = 1
```

```bash
sudo sysctl --system   # aplica sin reboot
```

#### Qué hace cada parámetro

| Parámetro | Efecto |
|---|---|
| `kptr_restrict=2` | Oculta punteros del kernel a todos, incluso root sin CAP_SYSLOG |
| `dmesg_restrict=1` | Solo root puede leer dmesg (previene info leak a usuarios) |
| `accept_redirects=0` | Ignora ICMP redirects (vector de MITM en red local) |
| `rp_filter=1` | Modo estricto de reverse path filtering (anti-spoofing) |
| `log_martians=1` | Registra paquetes con direcciones imposibles |
| `tcp_syncookies=1` | Protección contra SYN flood DDoS |

---

### 6. ClamAV

```bash
sudo pacman -S clamav
sudo freshclam             # descarga 3.6M de firmas (daily + main + bytecode)
sudo systemctl enable --now clamav-freshclam clamav-daemon
```

#### Servicios activos

- `clamav-freshclam`: actualiza la base de datos de virus diariamente
- `clamav-daemon` (clamd): demonio para escaneo bajo demanda

**Uso:** Para escanear un directorio:
```bash
clamscan -r --bell -i ~/Downloads
```

---

### 7. Firefox hardening

#### Plugins
- Eliminados: **AdBlock**, **AdGuard AdBlocker** (redundantes con uBlock Origin, causan conflictos)
- Conservado: **uBlock Origin** (único adblock necesario)
- Activos: LocalCDN, Privacy Badger, Multi-Account Containers, Dark Reader, DeepL, Keepa, Keeper

#### about:config

| Propiedad | Valor | Efecto |
|---|---|---|
| `privacy.resistFingerprinting` | `true` | Uniformiza fingerprint del navegador |
| `geo.enabled` | `false` | Deshabilita geolocalización |
| `media.peerconnection.enabled` | `false` | Deshabilita WebRTC (previene IP leak en VPN) |

---

## Problemas encontrados durante la sesión

### Keyboard layout en COSMIC Wayland
Causa de 3+ intentos fallidos de contraseña sudo. El layout `us` causa que ciertos caracteres (como `@`, `-`, etc.) salgan en posición diferente.

**Fix:**
```bash
setxkbmap latam   # o setxkbmap es
```

Documentado en `~/cosmic-usb-fix.md`.

---

## Estado final de la auditoría

| Ítem | Estado |
|---|---|
| DNS (Quad9 + DoT + DNSSEC) | ✅ Activo y verificado |
| nftables firewall | ✅ Policy drop, solo conexiones establecidas/loopback |
| Docker group eliminado | ✅ |
| rkhunter baseline + escaneo | ✅ 0 rootkits |
| sysctl hardening | ✅ Aplicado y persistente |
| ClamAV + auto-update | ✅ Corriendo como daemon |
| Firefox (plugins + about:config) | ✅ |
| VPN | ✅ Decisión cerrada (ago-2026): NO usar — ver sección VPN |

---

## Pendiente

### VPN — decisión cerrada (ago-2026): NO usar

Análisis comparativo de mayo 2026 (fuente: `inbox/23-05-26_vpn-privacidad-y-seguridad-linux.md`, archivado):

| VPN | Fortaleza principal | Perfil ideal |
|---|---|---|
| **Surfshark** | Balance general (precio/Linux/privacidad) | Usuario práctico y móvil — **favorito del análisis** |
| **ExpressVPN** | Velocidad y estabilidad | Uso intensivo y premium (costo más elevado) |
| **ProtonVPN** | Privacidad y transparencia (Suiza, auditorías, Secure Core) | Privacidad profunda |

Conceptos que sobreviven del análisis (válidos si la decisión se reabriera): encriptación AES-256/ChaCha20, protocolos WireGuard/OpenVPN, política no-logs, jurisdicción favorable (Suiza, BVI, Islandia), kill switch. Surfshark destacó por conexiones ilimitadas, WireGuard + AES-256, Kill Switch, Camouflage Mode y cliente CLI Linux.

**Decisión (agosto 2026, no reabrir): NO usar VPN.** Verificación en vivo: `ip route` sin interfaces tunnel (tun/wg/ppp), `which mozillavpn` → not found, ningún proceso VPN activo. El caso de uso que motivó el análisis de mayo (redes públicas, movilidad) no se materializó en necesidad operativa real. Detalle completo en `proyectos/P2/COSMIC_setup_custom.md` §11.5.

---

## Comandos de referencia para mantenimiento

```bash
# Verificar DNS
resolvectl status | grep -A5 "wlo1"

# Ver reglas de firewall activas
sudo nft list ruleset

# Escaneo rkhunter
sudo rkhunter --check --skip-keypress

# Escaneo ClamAV (Downloads)
clamscan -r --bell -i ~/Downloads

# Ver log rkhunter
sudo grep "Warning" /var/log/rkhunter.log

# Recargar sysctl
sudo sysctl --system

# Estado servicios de seguridad
sudo systemctl status nftables clamav-daemon clamav-freshclam systemd-resolved
```

---

## Herramientas instaladas en esta sesión

| Herramienta | Paquete | Propósito |
|---|---|---|
| nftables | `nftables` | Firewall nativo del kernel |
| rkhunter | `rkhunter` | Detección de rootkits, backdoors y archivos sospechosos |
| ClamAV | `clamav` | Antivirus para archivos descargados |
| wget | `wget` (dep de rkhunter) | Descarga de actualizaciones |

---

*Sesión completada: 2026-05-23, ~12:50 CST*

---

# Sesión 2 — Hardening adicional: cifrado, privacidad de red y sandbox
**Fecha:** 2026-05-25  
**Host:** fibonacci (mismo equipo)  
**Continúa desde:** auditoría 2026-05-23

---

## Ítem 8: LUKS2 — verificación de cifrado en disco

El cifrado ya estaba activo desde la migración Win11→Arch Linux. Se verificó:

```bash
lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT
# Resultado: nvme0n1 tiene partición con FSTYPE=crypto_LUKS

sudo cryptsetup status luks-<uuid>
# Confirma: LUKS2, AES-256-XTS, device activo y mapeado
```

**Conclusión:** El NVMe completo está cifrado con LUKS2. Sin la passphrase, el disco es ilegible en cualquier otro equipo.

---

## Ítem 9: MAC address randomization — NetworkManager

### Objetivo
Ocultar la dirección MAC real del hardware al conectarse a redes WiFi. En redes desconocidas se usa MAC aleatoria; en redes de confianza se usa MAC estable (derivada de la red — fija entre sesiones pero nunca la real).

### Archivo global creado: `/etc/NetworkManager/conf.d/00-macrandomize.conf`

```ini
[device]
wifi.scan-rand-mac-address=yes

[connection]
wifi.cloned-mac-address=random
ethernet.cloned-mac-address=random
```

Esto establece `random` como política por defecto para cualquier red nueva o desconocida.

### Redes de confianza — configuradas en `stable`

| Conexión | Red | Tipo | MAC policy |
|---|---|---|---|
| **** | Red doméstica | WiFi | stable |
| **** | Hotspot del móvil | WiFi | stable |
| **** | Casa de los papás | WiFi | stable |
| **** | Red universitaria con portal cautivo | WiFi | stable |
| **** | Ethernet (casa) | Ethernet | stable |

`stable` = MAC derivada criptográficamente de la red (SSID + hardware). Es siempre la misma para esa red, nunca la MAC real, y el portal cautivo de ITESO la "recuerda" entre sesiones.

```bash
nmcli connection modify <nombre> wifi.cloned-mac-address stable
```

### Redes eliminadas (stale / públicas)
****, ****, ****, ****, ****, ****

### Verificación

```bash
ip link show wlo1
# MAC mostrada debe ser distinta de la MAC real del hardware
```

---

## Ítem 10: Firejail — sandbox selectivo para Firefox

### Decisión de arquitectura
Se eligió sandbox **selectivo** en lugar de sandboxear todas las apps (`firecfg`), para evitar conflictos con apps actuales y futuras.

Apps en sandbox: **Firefox** y **clamscan** únicamente.

### Mecanismo: symlinks en `/usr/local/bin/` (precede a `/usr/bin/` en PATH)

```bash
# Limpiar cualquier firecfg previo
sudo firecfg --clean

# Crear symlinks manualmente
sudo ln -sf /usr/bin/firejail /usr/local/bin/firefox
sudo ln -sf /usr/bin/firejail /usr/local/bin/clamscan

# Limpiar caché de comandos de zsh
hash -r

# Verificar
which firefox    # → /usr/local/bin/firefox
which clamscan   # → /usr/local/bin/clamscan
```

Cuando el shell ejecuta `firefox`, encuentra `/usr/local/bin/firefox` (→ firejail) antes que `/usr/bin/firefox`. Firejail lanza Firefox en un namespace aislado con perfil de seguridad propio.

### Nota sobre `firejail --list`
`--list` muestra procesos sandboxeados **activos en ese momento**. Lista vacía = ninguna app sandboxeada corriendo, **no** indica que Firejail esté roto.

---

## Ítem 11: hblock — bloqueo de trackers a nivel sistema

### Qué es
`hblock` genera un archivo `/etc/hosts` que redirige dominios de tracking, publicidad y malware conocidos a `0.0.0.0`. Opera a nivel sistema operativo, afecta **todas** las aplicaciones (no solo el navegador).

Complementa a uBlock Origin, que solo cubre Firefox.

### Instalación

```bash
sudo pacman -S hblock
sudo hblock
```

### Resultado

```
hblock v3.5.1
Installed: 2026-05-25 ~19:06 CST
Entries en /etc/hosts: 444,284 líneas
```

### Arquitectura de bloqueo multicapa

```
Aplicación
    ↓
/etc/hosts (hblock) — bloquea 444k dominios maliciosos/trackers para TODAS las apps
    ↓
systemd-resolved (127.0.0.53)
    ↓ TLS cifrado
Quad9 (9.9.9.9) — filtra dominios maliciosos adicionales vía threat intelligence
    ↓
Root servers
```

### Actualización periódica

```bash
sudo hblock   # re-genera y actualiza la lista
```

---

## Estado final acumulado (ambas sesiones)

| Ítem | Estado |
|---|---|
| DNS (Quad9 + DoT + DNSSEC) | ✅ Activo y verificado |
| nftables firewall (policy drop) | ✅ Activo y persistente |
| Docker group eliminado | ✅ |
| rkhunter baseline + escaneo | ✅ 0 rootkits |
| sysctl kernel hardening | ✅ Aplicado y persistente |
| ClamAV + auto-update daemon | ✅ Corriendo |
| Firefox (plugins + about:config) | ✅ |
| LUKS2 cifrado completo en NVMe | ✅ Verificado |
| MAC randomization (redes desconocidas) | ✅ Activo |
| MAC stable (redes de confianza) | ✅ 5 redes configuradas |
| Firejail — Firefox sandboxeado | ✅ Symlink activo |
| Firejail — clamscan sandboxeado | ✅ Symlink activo |
| hblock (444k dominios bloqueados) | ✅ Sistema completo |
| VPN | ✅ Decisión cerrada (ago-2026): NO usar — ver sección VPN |

---

## Comandos de referencia adicionales (sesión 2)

```bash
# Verificar MAC activa en WiFi
ip link show wlo1

# Ver política MAC de una conexión
nmcli connection show <nombre> | grep mac

# Ver apps sandboxeadas activas
firejail --list

# Actualizar lista hblock
sudo hblock

# Ver tamaño actual de /etc/hosts
wc -l /etc/hosts
```

---

*Sesión completada: 2026-05-25, ~19:20 CST*
