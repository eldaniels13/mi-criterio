Lee el contenido de `inbox/` y propón un plan de integración para cada archivo sin clasificar.

## Tu tarea

1. **Listar** todos los archivos con estado `pendiente` en `_index.md` (capa 1 · inbox)
2. **Analizar** cada archivo: leer su nombre, fecha, y contenido si es necesario para clasificar
3. **Proponer** para cada uno exactamente una de estas acciones:
   - `MOVER → proyectos/P#/` — criterio consolidado, nombre sugerido sin fecha
   - `MOVER → proyectos/P#/` + `ACTUALIZAR perfil_maestro §N` — si cambia identidad, stack o criterio
   - `ARCHIVAR` — información pasada sin valor futuro, queda en inbox como referencia
   - `DESCARTAR` — sin valor recuperable
   - `MANTENER inbox` — fragmento válido pero incompleto, no procesar aún

4. **Presentar** la propuesta como tabla para aprobación:

| Archivo | Acción | Destino | Razón |
|---|---|---|---|
| `DD-MM-YY_nombre.md` | MOVER | `proyectos/P3/tema.md` | criterio energético consolidado |

5. **Esperar aprobación** — no mover nada hasta que el usuario confirme

6. Una vez aprobado:
   - Mover los archivos a sus destinos
   - Actualizar `_index.md` (mover filas de Capa 1 a Capa 2, cambiar estado)
   - Si algún archivo requiere actualizar `perfil_maestro`, señalarlo con el fragmento concreto a añadir/modificar (no editar directamente — el usuario decide)
   - Proponer commit: `inbox: process DD-MM-YY batch` o más específico si aplica

## Reglas

- No forzar completitud — si un archivo es un fragmento válido, puede quedarse en inbox
- Un archivo puede tocar múltiples lentes — elige el lente principal para el destino físico y señala los secundarios
- Si el nombre del archivo tiene espacios o caracteres raros, proponer nombre limpio al mover
- No crear carpetas nuevas sin preguntar
- Si hay duda sobre la clasificación, pregunta antes de proponer
