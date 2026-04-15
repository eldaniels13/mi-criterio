# SEGURIDAD DIGITAL: Transparencia sin riesgo

## Principio fundamental

**Transparencia radical NO significa ingenuidad digital.**

Hay una diferencia crítica:
- Compartir cómo piensas ✓
- Exponer credenciales que alguien puede usar contra ti ✗

GitHub + Git viven en **INTERNET PERMANENTE**. Una vez que un .git file está online, es prácticamente imposible borrarlo completamente (la gente lo archiva, lo copia, etc.).

---

## Lo que SÍ debe estar en el repo

✓ Perfil maestro (contexto de quién eres)
✓ Instrucciones de proyectos (cómo piensas)
✓ TODO/cambios documentados (decisiones)
✓ Email de contacto PÚBLICO
✓ LinkedIn PÚBLICO
✓ Ubicación general (país/ciudad, no dirección exacta)

---

## Lo que NUNCA debe estar en el repo

**CREDENCIALES:**
✗ API keys (Anthropic, GitHub, cualquier cosa)
✗ SSH private keys (~/.ssh/id_rsa)
✗ OAuth tokens
✗ Contraseñas (nunca, en ningún formato)
✗ Tokens de acceso personal (GitHub, etc.)

**INFORMACIÓN SENSIBLE:**
✗ Números de identificación (DNI, pasaporte)
✗ Números de cuenta bancaria / CLABE
✗ Detalles de tarjetas de crédito
✗ Direcciones exactas de hogar
✗ Números de teléfono personal (solo email)
✗ Información de personas que no dieron consentimiento

**DATOS FINANCIEROS PRIVADOS:**
✗ Tu saldo exacto en cuentas
✗ Inversiones específicas (solo puedes hablar en general)
✗ Historial de transacciones
✗ Documentos impositivos (CURP, RFC, etc.)

**INFORMACIÓN GEOPOLÍTICA SENSIBLE:**
✗ Planes de viaje específicos/fechas
✗ Familias en zonas peligrosas
✗ Cualquier cosa que pudiera ser "targeting" (dirección de alguien cercano, horarios rutina, etc.)

---

## Por qué estos cuidados en México específicamente

Estás en Guadalajara. Eso tiene implicaciones de seguridad:

1. **Crimen organizado:** Publicar rutinas, direcciones, o información que pueda ser "localized" es riesgo real
2. **Corrupción estatal:** Documentar crítica de Iberdrola (empresa ligada a gobierno) es OK. Pero no pongas datos que alguien malicioso pueda usar para encontrarte/hackearte
3. **Vigilancia privada:** Empleadores en México a veces hacen investigación intensiva — no des información que pueda ser usada en chantaje o presión

**Solución concreta:**
- Puedes criticar empresas, gobiernos, sistemas → eso es pensamiento político
- No publiques ubicación exacta, horarios, o datos que permitan "doxxing"
- Email + LinkedIn + GitHub suficientes para contacto

---

## El .gitignore: Explicación en profundidad

### ¿Qué es?

Archivo que le dice a Git: "Estos archivos/carpetas, no los sigas. Ignora cambios, no los commits, no los subas a GitHub."

### Plantas en el repositorio

```
mi-criterio/
├── .gitignore ← aquí van las reglas
├── archivo_public.txt ← Git lo sigue
├── .env ← Git lo ignora (nunca sube)
└── credenciales/ ← Git ignora carpeta entera
```

### Reglas de .gitignore (para ti, específicamente)

```
# ═══════════════════════════════════════════════════════════════
# SEGURIDAD: NUNCA SUBIR CREDENCIALES
# ═══════════════════════════════════════════════════════════════

# Archivos de credenciales
.env
.env.local
.env.*.local
*.key
*.pem
*_privado.txt
*_sensible.*
*_credentials.*
*_token.*
.credentials.json
credentials.json

# SSH keys (CRÍTICO)
~/.ssh/
id_rsa
id_rsa.pub
known_hosts

# ═══════════════════════════════════════════════════════════════
# SISTEMA: ignorar archivos de SO
# ═══════════════════════════════════════════════════════════════

.DS_Store
Thumbs.db
.AppleDouble
.LSOverride
desktop.ini

# ═══════════════════════════════════════════════════════════════
# IDE: ignorar configuración personal
# ═══════════════════════════════════════════════════════════════

.vscode/
.idea/
*.swp
*.swo
*~
.vim/
.project
.classpath

# ═══════════════════════════════════════════════════════════════
# CLAUDE CODE: IGNORAR ARCHIVOS LOCALES Y TEMPORALES
# ═══════════════════════════════════════════════════════════════

# Settings personales (NO versionar, cada máquina su settings.local.json)
.claude/settings.local.json

# Credenciales que Claude Code crea localmente
.claude/.credentials.json

# Historial de sesiones (personal, no compartir)
# Si decides tener .claude/projects/ aquí (no recomendado):
.claude/projects/

# ═══════════════════════════════════════════════════════════════
# DESARROLLO: ignorar dependencias, builds, logs
# ═══════════════════════════════════════════════════════════════

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node
node_modules/
npm-debug.log
yarn-error.log
package-lock.json (opcional — algunos lo versionan)

# C# / .NET
bin/
obj/
*.dll
*.exe
*.pdb
.vs/
.csproj.user

# Logs
*.log
*.log.*
logs/

# ═══════════════════════════════════════════════════════════════
# BACKUPS Y TEMPORALES
# ═══════════════════════════════════════════════════════════════

*.bak
*.backup
*.tmp
*.temp
*~
*.swp
*.swo

# ═══════════════════════════════════════════════════════════════
# DATOS PERSONALES: SÍ si tienes estos archivos
# ═══════════════════════════════════════════════════════════════

# Backups cifrados (si guardas backup_critico.vc aquí — lo harías con VeraCrypt)
*.vc
*.vault
*.encrypted

# Documentos financieros personales
*_finanzas_personal.*
*_inversiones_private.*
*_declaracion_impuestos.*

# CVs sin versionar (solo README sobre cómo actualizarlo)
CV_*_draft.docx
CV_*_personal.pdf

```

### Cómo aplicar en GitHub

**OPCIÓN 1: Crear desde cero (recomendado para ti)**

En GitHub.com → New Repo → gitignore template → selecciona "Python" (si usas Python)

O simplemente deja en blanco y copia el que generé arriba en tu máquina.

**OPCIÓN 2: Templates predefinidos de GitHub**

GitHub ofrece templates para:
- Python, Node, C#, etc.

**PERO:** Los templates generales no incluyen lo que TÚ necesitas (credenciales, Claude Code, datos sensibles específicos). Mejor hacer el tuyo.

**OPCIÓN 3: Mezclar**

Usa template Python + agrega tus reglas de seguridad adicionales.

---

## Verificar que .gitignore funciona

```bash
cd ~/mi-criterio

# Ver qué está siendo tracked
git status

# Ver qué está siendo ignorado
git check-ignore -v *

# Si ves ".env" o ".credentials.json" en el status, MALA NOTICIA:
# Esos archivos YA están en git (porque cometiste antes de .gitignore)

# Para LIMPIARLOS de histórico:
git rm --cached .env
git commit -m "security: remove .env from tracking"
git push
# Ahora .env nunca volverá a ser tracked
```

---

# CONTRIBUTING.md: Guía de colaboración

## Estructura clara que demuestra profesionalismo

```markdown
# Contributing to mi-criterio

Gracias por tu interés en colaborar. Este es un repositorio personal, 
pero aceptamos feedback estructurado de empleadores, mentores y colegas.

## Tipos de contribución que aceptamos

### 1. Issues: Feedback o señalar inconsistencias

Abre un issue si:
- Encuentras error técnico o lógico
- Quieres sugerir expansión de un proyecto (P1-P8)
- Tienes pregunta sobre el criterio desarrollado
- Quieres señalar un punto ciego que no reconozco

**Formato:**

```
Title: Feedback: [categoría]

**Categoría:** P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | perfil-maestro | metodología

**Descripción:**
[Tu feedback específico]

**Evidencia/Contexto:**
[Links, ejemplos, contexto]

**Mi respuesta esperada:**
[Qué esperas que haga con esto]
```

Ejemplo de BUENA issue:

```
Title: Feedback: P3 — Nuclear energy risk analysis

Categoría: P3

Tu análisis de nuclear incluye beneficios pero no profundiza en riesgos 
geopolíticos de proliferación de armas.

Evidencia: El tratado de no proliferación (NPT) tiene excepciones que 
México no exploras. Sugerencia: leer análisis de Arms Control Association.

Espero que: consideres agregar sección sobre proliferación en P3.
```

### 2. Pull Requests: Para correcciones y mejoras

Solo aceptamos PRs **pequeños y específicos**. No fusiones generales.

**Criterios para un PR aceptable:**

✓ Corrige error de tipografía o lógica clara
✓ Amplía un ejemplo existente (máx +50 líneas)
✓ Agrega fuente/referencia sin cambiar conclusión
✓ Actualiza una sección con cambios menores

✗ NO aceptamos PRs que:
✗ Cambien la filosofía general sin discusión previa
✗ Reescriban secciones enteras
✗ Agreguen nuevo criterio sin acuerdo
✗ Sean spam o autopromoción

**Flujo para PR:**

1. Fork el repo
2. Crea rama: `fix/[tipo]-[descripcion]` o `docs/[descripcion]`
   
   Ejemplos:
   - `fix/typo-p3-renewable`
   - `docs/expand-p4-etf-criteria`

3. Commit atómico (1 cambio específico):
   ```
   fix(p3): clarify nuclear risk assessment wording
   
   Added reference to Arms Control Association analysis.
   No conclusion change, just specificity.
   ```

4. Push a tu fork
5. PR con descripción clara

### 3. Feedback general (sin PR/issue formal)

Si tienes feedback que no es urgente:
- Email: danielgarciacastro64@gmail.com
- LinkedIn: mensaje directo
- Espacio: "Discussions" (si lo activo)

---

## Qué espero de ti como colaborador

1. **Específico, no vago**
   - MAL: "Este proyecto está incompleto"
   - BIEN: "P3 no menciona demanda de cobre para transición solar. Sugerencia: incluir análisis de ICMM."

2. **Honesto sobre sesgos**
   - Si tienes sesgo político, profesional o económico, decilo
   - Ejemplo: "Trabajo en Siemens Energy, así que mi feedback tiene sesgo"

3. **Respetuoso de decisiones**
   - Eldaniels tiene autonomía sobre criterio
   - El feedback es sugerencia, no orden
   - Si eldaniels rechaza tu PR, respeta la decisión

---

## Qué espero de eldaniels (yo) como mantenedor

1. Responder a todos los issues en 3-7 días
2. Ser claro si rechazo un PR (explicar por qué)
3. Considerar feedback genuino sin defensividad
4. Actualizar repo según cambios reales en mi criterio

---

## NO HACER en este repo

- Spam
- Solicitar dinero o favores
- Discusiones de política partidaria (sí podemos hablar geopolítica)
- Contenido sexual o violento
- Intentos de doxear, hackear o perjudicar al autor

Cualquier cosa así resultará en ban inmediato y reporte a GitHub.

---

## Flujo de decisión para colaboradores

¿Tu aporte es:

| ¿Qué es? | ¿Dónde va? |
|----------|-----------|
| Typo o error factual claro | PR pequeño directo |
| Sugiero expandir P1-P8 | Issue primero, luego PR |
| Quiero acceso de colaborador | Email pidiendo por qué + referencias |
| Quiero sugerir merge de criterio | Issue + conversación en comentarios |
| Es feedback general | Email o LinkedIn DM |

---

## Tabla de qué SÍ puede cambiar

| Elemento | ¿Puede cambiar? | ¿Por qué? |
|----------|-----------------|----------|
| Typos, gramática | SÍ | Error evidente |
| Fuentes/referencias | SÍ | Mejor documentación |
| Ejemplos | SÍ | Claridad |
| Definiciones | SÍ | Si Eldaniels acepta |
| Criterio core (P1-P8) | NO sin conversación | Es pensamiento vivo de Eldaniels |
| Filosofía general | NO sin conversación | Define identidad del repo |

---

## Cómo se vuelve alguien colaborador oficial

**Requiere:**
1. 3+ PRs pequeños aceptados
2. Demostración de entendimiento del proyecto
3. Propuesta clara de por qué necesitas acceso
4. Referencia de alguien que confíe en ti

**Acceso que se da:**
- Para merging de PRs propios
- Para comentar en issues
- Para sugerir cambios en perfil/criterio
- NO acceso a secretos, credenciales, o datos personales

---

## FAQ de colaboración

**P: ¿Puedo sugerir un nuevo P9?**
R: No. P1-P8 es estructura establecida. Pero puedes sugerir tema nuevo que quepa en alguno de los 8.

**P: ¿Puedo usar tu criterio para mi repo?**
R: SÍ. Licencia CC BY-NC-SA 4.0. Cita y no lo uses comercialmente.

**P: ¿Responden a todos los issues?**
R: Eldaniels se compromete a responder en 7 días. Si no, culpa a calendario de trabajo.

**P: ¿Puedo hacer PR para cambiar empresas objetivo?**
R: No, eso es decisión personal de Eldaniels. Puedes sugerir análisis de empresas en una issue.

---

## Código de conducta breve

**Sé honesto. Sé respetuoso. Sé específico.**

Eso es todo.
```

---

# RESUMEN: QUÉ INCLUIR EN EL REPO

Copia esto en dos archivos:

## ARCHIVO 1: mi-criterio/.gitignore

(El .gitignore que generé arriba — cópialo completo)

## ARCHIVO 2: mi-criterio/CONTRIBUTING.md

(El CONTRIBUTING que generé arriba)

---

# SIGUIENTE: Preguntas profundas sobre SECTOR OBJETIVO

Vamos a afinar esto juntos.

