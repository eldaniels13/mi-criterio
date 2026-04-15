# SSH KEYS: Qué son y por qué nunca van en Git

## ¿Qué es una SSH key?

Una **SSH key** es un par de "cerraduras digitales" para autenticarte en servidores/GitHub SIN usar contraseña.

Ejemplo físico:
- Tu **private key** (id_rsa) = llave física única que solo TÚ tienes
- Tu **public key** (id_rsa.pub) = cerradura que pones en GitHub

GitHub dice: "Si me demuestras que tienes la llave privada, te dejo entrar."

### El que NUNCA SUBE a GitHub

**Private key (id_rsa):**
```bash
# Ubicación típica
~/.ssh/id_rsa

# Contenido (NUNCA publiques esto)
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0Z8L9gX1+K7Q...
[líneas y líneas de datos cifrados]
-----END RSA PRIVATE KEY-----
```

Si alguien obtiene tu id_rsa, pueden:
- Hacer git push como si fueras tú
- Acceder a tus servidores
- Hacer cambios destructivos en tus repos
- Borrar todo
- Es como si tuvieran tu tarjeta de crédito

### El que SÍ puedes compartir

**Public key (id_rsa.pub):**
```bash
# Ubicación
~/.ssh/id_rsa.pub

# Contenido (es seguro compartir)
ssh-rsa AAAAB3NzaC1yc2EAAAADAQAB...
```

Es como tu número de celular — no es secreto.

---

## Por qué terminaste con SSH

Dijiste: "no cuento con una licencia. solo recuerdo haber configurado una SSH para mi extrabajo, pero no disponibles ahora."

Traducción: Tenías SSH configurada para autenticarte en GitHub, pero no tienes acceso a esas keys ahora (probablemente porque:
- Borró Windows
- La máquina dónde estaban está inaccesible
- Las perdió en la transición a Arch

---

## ¿Necesitas SSH keys ahora?

**NO inmediatamente.** Tienes dos opciones:

### OPCIÓN A: Usar HTTPS + Personal Access Token (más simple para ti ahora)

```bash
# En lugar de SSH, usas:
git clone https://github.com/eldaniels13/mi-criterio.git

# GitHub te pide autenticación
# Copias un "token" (contraseña temporal) en lugar de tu contraseña real
```

**Ventaja:** No necesitas generar SSH keys. Más simple.

**Desventaja:** El token expira, necesitas manejarlo con cuidado.

### OPCIÓN B: Generar nuevas SSH keys en Arch (mejor a largo plazo)

Si quieres hacer esto correctamente:

```bash
# 1. Generar nuevas keys
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa

# Te pide passphrase (contraseña adicional)
# Usa algo como: [tu contraseña fuerte de máquina]

# 2. Copiar public key
cat ~/.ssh/id_rsa.pub

# 3. Pegar en GitHub → Settings → SSH and GPG keys → New SSH key
# [Paste aquí el contenido de id_rsa.pub]

# 4. Probar
ssh -T git@github.com
# Debe decir: "Hi eldaniels13! You've successfully authenticated..."

# 5. Ahora usar SSH en tus repos
git remote set-url origin git@github.com:eldaniels13/mi-criterio.git
```

---

## IMPORTANTE: SSH keys NO van en .gitignore

Espera... sí van. Pero de forma diferente.

### Estructura segura

```
~/.ssh/              ← carpeta HOME, NO en el repo
├── id_rsa           ← PRIVATE (nunca en .gitignore porque NO está en repo)
├── id_rsa.pub       ← PUBLIC (también no en .gitignore)
├── known_hosts      ← logs de conexiones pasadas
└── config           ← configuración SSH

mi-criterio/         ← TU REPO
├── .gitignore       ← archivo de seguridad
├── .env             ← IGNORADO (no existe en repo)
└── [otros archivos]
```

**El punto:** SSH keys viven FUERA de tu repositorio (en ~/.ssh/), así que Git nunca los toca.

En .gitignore es precaución por si acaso:
```
# Si alguien accidentalmente metiera keys en el repo
~/.ssh/
id_rsa
id_rsa.pub
known_hosts
```

---

## Lo que VAS a poner en .gitignore para Claude Code

```
# CLAUDE CODE: evitar que suban cosas locales
.claude/settings.local.json    ← configuración personal
.claude/.credentials.json      ← si Claude Code crea credenciales locales
.claude/projects/              ← ← AQUÍ viene la explicación
```

---

# ~/.claude/projects/ — ¿Qué es y por qué ignorarlo?

## ¿Qué es?

Cuando usas Claude Code, automáticamente crea una carpeta:

```
~/.claude/projects/
├── session-2026-03-15.jsonl
├── session-2026-03-16.jsonl
└── session-2026-03-17.jsonl
```

Estos archivos JSONL contienen:
- Historial de tu sesión con Claude
- Lo que preguntaste
- Lo que hizo Claude Code
- Timestamps
- Rutas de archivos

**Básicamente:** Es tu historial de conversaciones con Claude, guardado localmente.

## ¿Por qué NO ponerlo en .gitignore?

Buena pregunta. Hay dos escenarios:

### ESCENARIO 1: Lo NORMAL (recomendado)

**~/.claude/projects/ está en tu HOME**, no en el repo.

```bash
# Structure real:
/home/eldaniels/.claude/projects/   ← aquí guardado, FUERA del repo
/home/eldaniels/mi-criterio/        ← tu repo
```

En este caso:
- Git NUNCA ve ~/.claude/projects/
- No necesitas .gitignore rule
- Los archivos nunca suben a GitHub

### ESCENARIO 2: Lo MALO (si alguien fuera de lugar lo metiera)

Si por error copiaras tu ~/.claude/ **dentro** del repo:

```bash
# MALO — no hagas esto:
mi-criterio/
└── .claude/
    ├── CLAUDE.md
    ├── settings.json
    ├── settings.local.json
    ├── .credentials.json
    └── projects/              ← aquí hay tus conversaciones privadas
        ├── session-2026-03-15.jsonl
        └── session-2026-03-16.jsonl
```

En este caso:
- Subirías tus conversaciones privadas a GitHub
- Violarías privacidad
- Podrías exponer info sensible
- **Aquí es dónde entra .gitignore**

```
# En .gitignore para protegerse de errores:
.claude/projects/
```

---

## Resumen: La regla de oro

```
Dentro del repositorio (mi-criterio/):
├── .claude/
│   ├── CLAUDE.md          ✓ Versiona (es instrucciones)
│   ├── settings.json      ✓ Versiona (es config compartida)
│   ├── settings.local.json ✗ IGNORA (config personal)
│   ├── .credentials.json   ✗ IGNORA (credenciales)
│   ├── projects/          ✗ IGNORA (conversaciones privadas)
│   └── commands/          ✓ Versiona (son skills compartidos)

Fuera del repositorio (en HOME):
└── ~/.claude/projects/    ← Esto NUNCA entra al repo

```

---

## Tu .gitignore: Cómo se ve

```bash
# Protección contra error humano
.claude/settings.local.json
.claude/.credentials.json
.claude/projects/           # Si alguien lo metiera aquí por error
```

**¿Es probable que metas proyectos/? No. Pero es precaución.**

---

## Referencia rápida: Dónde vive qué

| Archivo | Ubicación | ¿En Git? | ¿Por qué? |
|---------|-----------|----------|----------|
| id_rsa (SSH private) | ~/.ssh/id_rsa | ✗ | Es credencial, no en ningún repo |
| CLAUDE.md | .claude/CLAUDE.md | ✓ | Instrucciones compartidas |
| settings.json | .claude/settings.json | ✓ | Config compartida de permisos |
| settings.local.json | .claude/settings.local.json | ✗ | Config personal, en .gitignore |
| projects/ | ~/.claude/projects/ | ✗ | Historial privado, vive en HOME |
| .credentials.json | .claude/.credentials.json | ✗ | Credenciales locales, en .gitignore |

---

## Comando para verificar que todo está seguro

```bash
cd ~/mi-criterio

# Ver qué está siendo tracked
git status

# Resultados esperados:
# - NO deben aparecer .env, *.key, .credentials, etc.
# - SÍ deben aparecer CLAUDE.md, settings.json, README, etc.

# Ver exactamente qué ignora
git check-ignore -v *

# Resultados esperados:
# .claude/settings.local.json
# .env (si existe)
# etc.
```

---

## Bottom line

**SSH keys:** No van nunca en repos. Viven en ~/.ssh/ fuera del repo.

**~/.claude/projects/:** Tampoco va. Vive en ~/.claude/ fuera del repo. Pero agregas una línea en .gitignore como precaución.

**Tus credenciales:** Cada archivo sensible tiene una línea en .gitignore para asegurar que Git nunca los toca.

Si todo está configurado bien:
```bash
# Esto debería estar vacío (ningún archivo sensible)
git ls-files --others --ignored --exclude-standard | head -20
```

If there's output, eso significa hay sensibles siendo ignorados — perfecto.

