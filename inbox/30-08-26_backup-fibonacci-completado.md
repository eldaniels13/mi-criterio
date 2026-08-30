# Respaldo de fibonacci completado — 30 ago 2026

Cierra el handoff `28-08-26_handoff_plan-backups-restauracion-total.md`.
Los tres inventarios que exigía están hechos y el respaldo existe y está verificado.

---

## 1 · El riesgo mayor está retirado

El handoff decía: *"si el contenedor de abril no monta o el disco falló en
silencio, la única copia existente ya está perdida"*. No pasó.

Verificación completa contra el baseline SHA512 de abril:

| | |
|---|---:|
| archivos en baseline | 19 040 |
| coinciden | 19 027 (99.93 %) |
| cambiados | 9 |
| faltantes | 4 |
| **errores de lectura** | **0** |
| nuevos desde abril | 315 |

52.85 GB leídos en 565 s sin un solo error → el medio no se ha degradado.

Los 9 cambiados son `.mp3` en `Música`. Causa desconocida: sus mtime son de
2024, o sea que no se reescribieron. O bitrot, o se recopiaron en junio desde
otra fuente. El baseline de PowerShell guardó hashes pero no tamaños, así que
los dos casos no se pueden distinguir. No es concluyente ni alarmante.

---

## 2 · Los tres inventarios

**fibonacci ($HOME, 87 G)** — ~77 G regenerable, ~4.8 G irreemplazable.
Dos huecos que ningún documento previo listaba: `~/.local/bin` con 12 scripts
escritos a mano, y `~/.histfile`. Ninguno estaba respaldado.

**tenochtitlan (contenedor)** — Galerías 3 288 archivos / 17.13 GB,
Música 252 / 1.52 GB, más OneDrive ITESO y Programas.

**Cubot** — DCIM 583 archivos / 5.07 GB. La tarjeta SanDisk está puesta pero vacía.

Respuesta a la pregunta abierta del handoff: **fibonacci no tiene medios
personales**. Todo vive en tenochtitlan y en el teléfono.

---

## 3 · Lo que se construyó

Una herramienta que refresca el respaldo y comprueba lo escrito:

```
respaldar-fibonacci              simulación, no escribe nada
respaldar-fibonacci --ejecutar   copia real
respaldar-fibonacci --verificar  recalcula hashes contra el manifiesto
```

Vive fuera de este repo, junto a su configuración. **A propósito**: la lista
de qué se respalda es el mapa de dónde están los secretos, y este repo es
público. Misma lógica que `auditar_pre_push.sh`.

Decisiones de diseño que costaron una reescritura cada una:

- **Rechaza en firme un destino sin cifrar, sin bandera para saltárselo.**
  Las fuentes incluyen `.ssh` y `.gnupg`. Escribirlas en claro es peor que no
  respaldarlas.
- **Nunca borra en el destino** — sin `--delete`. Un espejo mal apuntado
  destruye la única copia.
- **La receta viaja con el respaldo.** Un disco recuperado explica cómo se
  hizo y cómo repetirlo.
- **Formatos nativos de rsync** (`--files-from`, `--exclude-from`) en vez del
  parser INI de ~40 líneas que había escrito primero.
- **`tar` para los archivos de sistema.** Guarda modo y dueño *dentro* del
  archivo, así que un destino NTFS que no sabe representarlos no los pierde.
  Un `sudo tar` eliminó de golpe el bucle de escritura, el de restauración y
  el footgun de `sudoers` con modo incorrecto.

---

## 4 · Resultado

```
$HOME        16 214 archivos ·  4.83 GB
sistema      sistema.tar.gz  ·  9 rutas con permisos intactos
paquetes     84 oficiales · 5 AUR
manifiesto   16 284 archivos
verificación 16 284 / 16 284 íntegro
```

**Cubot** — carrete de cámara completo (583 archivos / 5.1 GB), Download y
Documents completos. Faltan ~6 900 archivos diminutos (~170 MB) de
`Pictures` y `Movies`: miniaturas de WhatsApp, regenerables. Se decidió no
perseguirlos; MTP dejó de responder y lo que importa ya está.

---

## 5 · Correcciones a la documentación

`P8_Backup_Wiki/Timeline_Fases.md` estaba mal en tres hechos:

| decía | es |
|---|---|
| `xochimilco.vc` | `backup_critico.vc` |
| 200 GB exFAT | 150 GB NTFS |
| baseline en `K:\` | dentro del contenedor |

Corregido, y añadida FASE 1.5 con la migración a Linux.

---

## 6 · Queda abierto

- **Prueba real de restauración** en hardware distinto o VM. Un respaldo sin
  restaurar es una hipótesis.
- **VeraCrypt vs LUKS** para los discos futuros (FASE 2/3).
- **Herramienta genérica multi-dispositivo** — aplazada explícitamente.
- Los 9 mp3 cambiados: sin causa determinada.
