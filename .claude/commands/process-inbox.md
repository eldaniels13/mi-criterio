Destila `inbox/` hacia los documentos canónicos de `proyectos/`, sin perder información y produciendo trabajo accionable.

**No es un comando de limpieza.** Vaciar el inbox no es el objetivo — el objetivo es que lo valioso llegue a un doc canónico verificado y que lo pendiente salga listo para empezar a trabajarlo.

---

## Paso 1 · Reconciliar disco contra índice (SIEMPRE primero)

`_index.md` no es la fuente de verdad — **el disco lo es**. Un archivo sin fila en el índice es invisible para el índice, no inexistente.

```bash
# La tabla de Capa 1, aislada. NO usar grep sobre todo _index.md:
# capturaría las tablas de Capa 2 y 3, y un archivo ya movido enmascararía
# a uno nuevo con el mismo nombre.
awk '/^## Capa 1/,/^## Capa 2/' _index.md \
  | grep -oE '^\| `[^`]+`' | tr -d '|` ' | sort > /tmp/idx1.txt

# HUÉRFANOS — en disco, sin fila en el índice → pendientes
comm -23 <(ls inbox/ | grep -v '^_' | sort) /tmp/idx1.txt

# FANTASMAS — con fila en el índice, sin archivo en disco → el índice miente
comm -13 <(ls inbox/ | grep -v '^_' | sort) /tmp/idx1.txt
```

Ambas listas se reportan. Los `_*` (plantillas, índices) nunca se procesan.

Además, releer los marcados `archivado`: `archivado` significa *"su valor ya vive en un doc canónico, verificado"*. Si nunca se comprobó dónde quedó su contenido, **no está archivado — está pendiente**.

## Paso 2 · Clasificar por tipo

| Prefijo | Tipo | Criterio de destilación |
|---|---|---|
| `*_handoff_*` | Cierre de sesión | Se destila hacia su doc canónico. Casi siempre `FUSIONAR`. |
| `*_captura_*` | Idea/link suelto | Se evalúa. Muchas veces `ARCHIVAR` o `DESCARTAR` sin culpa. |
| otro | Legado / externo | Leer y clasificar a mano. |

Plantillas en `inbox/_PLANTILLAS/`. Los archivos que empiezan con `_` nunca se procesan.

## Paso 3 · Analizar cada archivo

Leer el contenido — el nombre no basta. Antes de proponer destino, **buscar si el lente ya tiene doc canónico del tema**:

```bash
ls proyectos/P*/ recursos/ P8_Backup_Wiki/
```

## Paso 4 · Proponer una acción por archivo

| Acción | Cuándo |
|---|---|
| `FUSIONAR → canónico.md §N` | Existe doc canónico del tema. **Preferida por defecto.** |
| `UNIFICAR → canónico.md` | Varias fuentes del mismo tema → un solo doc |
| `MOVER → proyectos/P#/nombre.md` | No existe canónico; se crea. Nombre sin fecha. |
| `EXTRAER → ~/Codes/repo/` | Es código. Sale del repo, con `.gitignore` **antes** del `git init`. |
| `PARTIR` | Toca temas dispares con destinos distintos |
| `ARCHIVAR` | Su valor ya está verificado en un canónico |
| `DESCARTAR` | Sin valor recuperable |
| `MANTENER inbox` | Fragmento válido pero incompleto, o pertenece a una sesión futura ya asignada |
| `+ ACTUALIZAR perfil_maestro §N` | Cambia identidad, stack o criterio (se señala, no se edita) |

## Paso 5 · Reconciliar los canónicos que toca el lote

Sólo los docs canónicos de los lentes que el lote toca — no el repo entero.

Para cada uno, contrastar **crítica pero constructivamente** contra la realidad del disco:

- ¿Menciona archivos, rutas o comandos que ya no existen?
- ¿Hay archivos nuevos en ese lente ausentes del doc?
- ¿Alguna decisión quedó superada por hechos posteriores?
- ¿El estado declarado coincide con lo verificable hoy?

El drift encontrado se reporta y se corrige en el mismo lote. Auditoría del repo completo → comando aparte, no aquí.

## Paso 6 · Presentar para aprobación

| Archivo | Tipo | Acción | Destino | Razón |
|---|---|---|---|---|
| `DD-MM-YY_handoff_tema.md` | handoff | FUSIONAR | `proyectos/P3/tema.md` §4 | criterio energético consolidado |

Acompañar con: drift detectado en canónicos, y **pendientes accionables** extraídos del lote.

**Esperar aprobación. No mover nada antes.**

## Paso 7 · Ejecutar

1. Aplicar las acciones aprobadas
2. **Verificar cada fusión dato por dato antes de tocar el original** (ver Regla 2)
3. Actualizar `_index.md`: Capa 1 → Capa 2, estados, lentes secundarios
4. Volcar los pendientes accionables a `ToDo_global_eldaniels.md`
5. Señalar los fragmentos de `perfil_maestro` que correspondan — sin editarlo
6. Proponer commits, **sin ejecutarlos**

---

## Reglas

**1 · Destilar ≠ resumir.**
Sobreviven íntegros: cifras medidas, comandos exactos, rutas, versiones, hashes, IDs, errores textuales, evidencia empírica, y **decisiones descartadas con su razón** — evitar repetir un callejón sin salida vale tanto como documentar el acierto.
Se elimina sólo: cortesía conversacional, duplicación literal entre docs, y especulación ya refutada por hechos posteriores.
**Ante la duda, se conserva.**

**2 · Verificar antes de cerrar — mecanizado, no a ojo.**
Un archivo pasa a `archivado` sólo tras comprobar, dato por dato, que su residuo está en el destino. **A ojo esto se degrada en silencio bajo carga**, así que se mide:

```bash
.claude/scripts/verificar_residuo.sh FUENTE DESTINO
.claude/scripts/verificar_residuo.sh --lote DESTINO SRC1 SRC2 SRC3   # para UNIFICAR
```

El script clasifica cada dato duro ausente en tres categorías, y **sólo la primera exige acción**:

| | Significa | Qué hacer |
|---|---|---|
| 🔴 **PÉRDIDA** | No está en el destino ni en ningún otro doc, y sigue siendo cierto en disco | Fusionar antes de cerrar |
| 🔵 **REUBICADO** | Aparece en otro doc del repo | Verificar que sea el mismo dato, no sólo la misma cadena |
| ⚪ **OBSOLETO** | La ruta ya no existe en disco | Descartar a conciencia — conservarlo documentaría una mentira |

**Criterio de cierre: `perdida == 0`** (el script sale con código 1 si no). El desglose se incluye en el informe al usuario; las decisiones sobre 🔵 y ⚪ se justifican una por una, nunca en bloque.

Si el script marca 🔴, el archivo **no se toca** hasta fusionar lo que falta. Si no se verificó, sigue pendiente.

**3 · Nada se borra del repo.**
`DESCARTAR` es para lo que no tiene valor recuperable, y se justifica. Archivar nunca significa perder documentación.

**4 · Preferir append sobre archivo nuevo.**
El repo ya convergió en *un doc canónico por subproyecto, actualizado en sitio, sin fecha en el nombre*. Sembrar archivos nuevos fragmenta el criterio.

**5 · El código vive fuera.**
mi-criterio guarda criterio, no software. Scripts y apps → su propio repo en `~/Codes/`. Aquí queda el doc de arquitectura y decisión.

**6 · Destilar produce trabajo.**
Cada fusión emite sus pendientes al `ToDo_global`. Un inbox procesado que no generó ni un accionable probablemente se destiló mal.

**7 · Multi-lente sin duplicar.**
Un archivo puede tocar varios lentes: destino físico único, lentes secundarios declarados en `_index.md`.

**8 · Sensibilidad.**
Nunca mover al repo credenciales, cifras financieras reales ni nombres de institución financiera. Anonimizar (`Cuenta-1..N`, `[redactado]`) o dejar fuera.

**9 · No forzar completitud.**
Un fragmento válido puede quedarse en inbox. Si pertenece a una sesión futura ya asignada, se marca y se deja.

**10 · Preguntar ante la duda.**
No crear carpetas nuevas sin preguntar. Ante clasificación ambigua, preguntar antes de proponer.

**11 · Git a mano.**
Proponer commits; nunca ejecutarlos.

ARGUMENTS: enfoque o filtro para este lote (opcional)
