# CutWindow_2 — contexto de sesión dedicada

**Última sesión de código activo**: 12 de marzo 2026 en Visual Studio Pro / Win11 Pro
**Propósito**: Nesting engine para corte láser/telas con plugin AutoCAD
**Estado**: migración Windows → Linux post MFT corruption + reinstalación stack

---

## Ubicación del código

- **Primaria**: `~/Codes/CutWindow_2` en fibonacci (Arch Linux)
- **Backup**: Kingston NV3 externo → `backup_critico.vc` (VeraCrypt) → carpeta `Programas/`

---

## Entorno de desarrollo elegido

**IDE principal**: JetBrains Rider (licencia no-comercial gratuita)

Razones:
- Mejor tooling C# disponible en Linux (refactors avanzados, profiler, NuGet UI, test runner visual)
- Debugger con hot reload WPF/WinForms (cuando proyecto lo permite)
- Superior a VSCodium + OmniSharp comunitario para proyecto productivo

Trade-offs de soberanía aceptados:
- Binario cerrado (igual que VS Code oficial — honestamente cerrado vs hipócritamente cerrado)
- Revalidación de licencia cada 30 días (envía email, fingerprint, versión — no código)
- Formato `.idea/` específico del vendor, no transferible a otros IDEs
- Dependencia de cuenta JetBrains

Configuración crítica al primer arranque:
- Settings → Appearance & Behavior → System Settings → Data Sharing → **desactivar todo**
- AI Assistant: **desactivar** (usar Ollama local o Claude Code según necesidad consciente)
- Telemetría: desactivar en mismo panel

**IDE secundario**: VSCodium (para Python, scripts, Markdown, portfolio)
- Extensiones instaladas: ms-python, errorlens, gitlens, csharp, ms-toolsai.jupyter, ruff
- (verificar con `codium --list-extensions --show-versions`)

---

## Stack de IA disponible para este proyecto

**Ollama local** (fibonacci, corre como servicio de usuario):
- `qwen2.5-coder:7b` — chat técnico (~5GB RAM)
- `qwen2.5-coder:1.5b` — autocomplete FIM, pulled ✓ (~1GB RAM, 200-500ms latencia)
- `deepseek-coder:6.7b` — chat con razonamiento (~4GB RAM)
- `nomic-embed-text` — embeddings para indexado @codebase, pulled ✓ (~300MB RAM)

**Claude Code** (cuando calidad > privacidad del snippet):
- CLI ya instalado en fibonacci
- Pendiente: extensión en VSCodium (vía `claude` en terminal integrado o Open VSX)
- Regla: decisión consciente por tarea. NO enviar código AutoCAD propietario con serial.
  SÍ enviar algoritmos geométricos genéricos, refactors arquitecturales, debugging complejo.

**Continue.dev** (pendiente de instalar y configurar):
- Extensión en VSCodium (Open VSX)
- Config en `~/.continue/config.yaml` (schema v1, no el config.json legacy)
- Roles sugeridos:
  - autocomplete → qwen2.5-coder:1.5b
  - chat → qwen2.5-coder:7b
  - edit → deepseek-coder:6.7b
  - embed → nomic-embed-text

---

## Inspección pre-apertura (correr primero)

```bash
cd ~/Codes/CutWindow_2

# Estructura de proyectos
find . -name "*.csproj" -o -name "*.sln" | head -20

# TargetFramework de cada proyecto
grep -r "TargetFramework" --include="*.csproj" .

# Referencias externas
grep -r "PackageReference\|Reference Include" --include="*.csproj" .

# Tamaño y última modificación
du -sh . && ls -la
```

Pegar salida antes de abrir en Rider.

---

## Desafíos esperados Windows → Linux

| Tipo de proyecto                     | Compila en Linux        |
|--------------------------------------|-------------------------|
| `net8.0` / `netstandard2.0` class lib| ✅ Sí                   |
| `net8.0` + xUnit/NUnit tests         | ✅ Sí                   |
| `net48` (.NET Framework)             | ❌ No                   |
| `net8.0-windows` + WPF/WinForms      | ❌ No (Windows Desktop) |
| AutoCAD plugin (ObjectARX/Managed)   | ❌ No (SDK Windows-only)|

Rider en Linux marca los proyectos incompatibles con ícono tachado. No cargan pero no rompen el resto.

---

## Refactor arquitectural propuesto

Separar lógica de dominio de lógica de plataforma — aprovechar el reset forzado de la migración:

```
CutWindow_2.Core            ← net8.0, compila en Linux
  ├─ Geometry/              ← polígonos, rotación, bounding box, colisiones
  ├─ Algorithms/            ← nesting engine (el corazón productivo)
  └─ Models/                ← DTOs puros, sin dependencias externas

CutWindow_2.AutoCAD         ← net48, solo en Windows
  └─ adapter AutoCAD ↔ Models (convierte entidades ObjectARX a DTOs)

CutWindow_2.CLI (NUEVO)     ← net8.0, corre en Linux
  └─ consola para probar Core sin AutoCAD (input: DXF/SVG, output: layout)

CutWindow_2.Tests           ← net8.0, corre en Linux
  └─ xUnit sobre Core (cobertura algorítmica)
```

Beneficios:
- 80% del trabajo (algoritmos) se desarrolla en fibonacci sin fricción
- 20% (integración AutoCAD) se prueba cuando Windows vuelva a ser accesible
- Día que quieras otro frontend (QCAD, webapp, LibreCAD scripting) — Core ya desacoplado
- Tests corren en CI/CD futuro sin licencias AutoCAD

---

## Decisiones de diseño persistentes

- **Prioridad**: corrección geométrica > velocidad > mantenibilidad
- Proyecto productivo, NO académico — evitar over-engineering pero sí testing exhaustivo
- Punto ciego activo: diseñar sistemas antes de validar factibilidad → **validar cada algoritmo con casos reales antes de escalarlo**
- Excel avanzado (subproyecto paralelo) NO relacionado con esta solución

---

## Otros proyectos PerformanceDesigns relacionados

- `DeepNestSharp` — referencia de nesting algorithm (open source, C#)
- `NestingTesting` — playground para probar variantes algorítmicas
- `O2BToDxfConverter` — utility para convertir formatos
- Pendiente global: push a GitHub (eldaniels13) — repos privados

---

## Secuencia sugerida para sesión CutWindow_2 dedicada

1. Verificar Rider instalado y telemetría desactivada
2. Correr comandos de inspección (arriba)
3. Abrir `CutWindow_2.sln` en Rider
4. Dejar indexar (2-5 min primera vez)
5. Intentar Build Solution — leer errores por proyecto
6. Identificar qué del Core realmente es puro (sin deps AutoCAD) y qué está contaminado
7. Diseñar plan de separación concreto proyecto por proyecto
8. Ejecutar primer paso del refactor (usualmente: crear nueva Core limpia, mover tipos uno por uno)
9. Configurar Continue.dev en VSCodium con `~/.continue/config.yaml`
10. Decidir qué partes envolver con tests inmediatamente (algoritmos geométricos primero)

---

## Notas de estado al cierre de sesión 2026-04-20

- Rider descargándose con `yay -Syu rider` (warnings PGP normales)
- Extensiones VSCodium ya instaladas (listado pendiente de verificar)
- Ollama models nuevos: pulled ✓ (qwen2.5-coder:1.5b, nomic-embed-text)
- Continue.dev: pendiente instalar + configurar `config.yaml`
- Claude Code extension VSCodium: pendiente instalar