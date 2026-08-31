# Plan Maestro: Backup Digital Seguro y Soberanía de Datos

**Estado**: FASE 1.5 completada (migración a Linux) — FASE 2/3 pendientes de presupuesto
**Versión**: 2.0
**Última actualización**: 2026-08-30
**Objetivo**: 2TB máxima soberanía, cifrado LUKS, redundancia geográfica

> **Archivo unificado (2026-08-30):** este documento absorbe `Timeline_Fases.md` y
> `Archivos_Criticos_Inventory.md`, retirados como archivos sueltos — todo el estado de fases
> y el inventario de archivos críticos vive aquí. `mft_recovery_decision.md` se mantiene aparte
> (registro de incidente, no procedimiento; referenciado desde `proyectos/P2/COSMIC_setup_custom.md` §9.1).

---

## 📋 Índice Rápido

- [Estado Real (actualizado 2026-08-30)](#estado-real-actualizado-2026-08-30)
- [FASE 0: Preparación (AHORA)](#fase-0-preparación-ahora)
- [FASE 1: tenochtitlan + VeraCrypt](#fase-1-tenochtitlan--veracrypt)
- [FASE 2: HDD_A LUKS](#fase-2-hdd_a-luks)
- [FASE 3: HDD_B Redundancia](#fase-3-hdd_b-redundancia)
- [Timeline por Fases (checklist real)](#timeline-por-fases-checklist-real)
- [Inventario de Archivos Críticos](#inventario-de-archivos-críticos)
- [Gaps Identificados y Soluciones](#gaps-identificados-y-soluciones)

---

## Estado Real (actualizado 2026-08-30)

> El plan original (FASE 0-3 abajo) se escribió en 2026-03 para Windows + VeraCrypt. La migración
> a Arch Linux ya ocurrió; algunos supuestos del plan original (VeraCrypt como cifrado principal,
> disco raíz sin cifrar) **ya no aplican** al equipo `fibonacci` (disco raíz es LUKS+LVM nativo).
> Leer esta sección antes que las FASE 0-3 originales, que se conservan como registro histórico.

**Corrección de tres hechos que Timeline_Fases.md tenía mal** (detectado 2026-08-30):

| Decía | Es |
|---|---|
| `xochimilco.vc` | `backup_critico.vc` |
| 200 GB exFAT | 150 GB NTFS |
| baseline en `K:\` | dentro del contenedor |

### El riesgo mayor identificado en 28-08-26 quedó retirado en 30-08-26

El handoff del 28-08 advertía: *"si el contenedor de abril no monta o el disco falló en silencio,
la única copia existente ya está perdida"*. Verificación contra el baseline SHA512 de abril:

| | |
|---|---:|
| archivos en baseline | 19 040 |
| coinciden | 19 027 (99.93%) |
| cambiados | 9 (`.mp3` en Música, mtime de 2024 — bitrot o recopiados en junio, no concluyente) |
| faltantes | 4 |
| **errores de lectura** | **0** |
| nuevos desde abril | 315 |

52.85 GB leídos en 565 s sin un solo error — el medio (`tenochtitlan`) no se ha degradado.

### Los tres inventarios que el handoff del 28-08 exigía (resueltos 30-08)

- **fibonacci ($HOME, 87 G)** — ~77 G regenerable (`.local` 50G modelos Ollama, `.cache` 23G,
  gestores de paquetes ~5.8G), **~4.8 G irreemplazable**. Dos huecos que ningún documento previo
  listaba: `~/.local/bin` (12 scripts escritos a mano) y `~/.histfile` — ninguno respaldado hasta esta sesión.
- **tenochtitlan (contenedor)** — Galerías 3,288 archivos / 17.13 GB, Música 252 / 1.52 GB, más OneDrive ITESO y Programas.
- **Cubot** — DCIM 583 archivos / 5.07 GB. Tarjeta SanDisk puesta pero vacía.

**Conclusión: fibonacci no tiene medios personales.** Todo vive en tenochtitlan y en el teléfono — resuelve la pregunta abierta del 28-08 (*"Cubot, tenochtitlan, fibonacci... no estoy completamente seguro"*).

### Herramienta construida: `respaldar-fibonacci`

Vive **fuera de este repo**, junto a su configuración — la lista de qué se respalda es el mapa de
dónde están los secretos, y este repo es público (misma lógica que `.claude/scripts/auditar_pre_push.sh`).

```
respaldar-fibonacci              simulación, no escribe nada
respaldar-fibonacci --ejecutar   copia real
respaldar-fibonacci --verificar  recalcula hashes contra el manifiesto
```

**Decisiones de diseño (cada una costó una reescritura):**
- Rechaza en firme un destino sin cifrar, sin bandera para saltárselo — las fuentes incluyen `.ssh`/`.gnupg`; escribirlas en claro es peor que no respaldarlas.
- Nunca borra en el destino (sin `--delete`) — un espejo mal apuntado destruye la única copia.
- La receta viaja con el respaldo — un disco recuperado explica cómo se hizo y cómo repetirlo (`fibonacci/receta/`, `RESTAURAR.md`).
- Formatos nativos de rsync (`--files-from`, `--exclude-from`) en vez de un parser INI propio de ~40 líneas descartado.
- `tar` para archivos de sistema — guarda modo/dueño *dentro* del archivo, así un destino NTFS que no los representa no los pierde. Un `sudo tar` eliminó de golpe el bucle de escritura, el de restauración, y el footgun de permisos incorrectos en `sudoers`.

**Resultado verificado:**
```
$HOME        16,214 archivos ·  4.83 GB
sistema      sistema.tar.gz  ·  9 rutas con permisos intactos
paquetes     84 oficiales · 5 AUR
manifiesto   16,284 archivos
verificación 16,284 / 16,284 íntegro
Cubot        583 archivos / 5.1 GB (carrete completo) + Download + Documents completos
             faltan ~6,900 archivos diminutos (~170 MB) de Pictures/Movies — miniaturas WhatsApp,
             regenerables; MTP dejó de responder, no se persiguieron
```

**Limpieza de duplicados relacionada (30-08-26, log de sesión):** eliminados Mars Manuals (18),
Cubot IMG (554), Zenaj MP3 (1) — liberó ~4.73 GiB en tenochtitlan.

### Queda abierto

- **Prueba real de restauración** en hardware distinto o VM — un respaldo sin restaurar es una hipótesis, no un hecho. Es el siguiente paso de mayor riesgo pendiente.
- **VeraCrypt vs LUKS** para los discos futuros (FASE 2/3) — VeraCrypt se eligió en 2026-03 por compatibilidad con Windows 11; la migración a Arch ya ocurrió y el disco raíz es LUKS nativo. Decisión pendiente, no reabrir sin resolver.
- **Herramienta genérica multi-dispositivo** — aplazada explícitamente, `respaldar-fibonacci` es específica a esta máquina.
- Los 9 `.mp3` cambiados en el baseline: sin causa determinada (bitrot vs recopiado, no distinguible con los datos disponibles).
- `~/.ssh` y credenciales: excluidos a propósito desde marzo con nota "manejo aparte" que nunca se ejecutó — son justo lo que restaura el *acceso* a todo lo demás; el objetivo declarado ("restaurar como si nada hubiera pasado") no se cumple sin resolver esto.

---

## FASE 0: Preparación (AHORA)

**Objetivo**: Preparar todo lo que podemos hacer mientras llega tenochtitlan + carcasa USB-C.  
**Duración estimada**: 7-10 días  
**Recursos requeridos**: Laptop actual (Windows 11), conexión internet, papel/notas  
**Costo**: $0

### 0.1 Instalación y Validación VeraCrypt (Windows 11)

**¿Por qué ahora?**: Necesitas aprender la herramienta antes de tener hardware crítico.

```
□ Descargar VeraCrypt 1.25+ desde https://www.veracrypt.fr/
  └─ Versión: Windows (64-bit si tu Windows es 64-bit)
  └─ Guardar en C:\Users\[tu_usuario]\Downloads\VeraCrypt_Setup.exe

□ Instalar VeraCrypt
  └─ Ejecutar .exe
  └─ Acepta licencia
  └─ Selecciona: "Install for current user only" (más seguro)
  └─ Opción: "Enable keyfile support" (adelantado, por ahora no necesario)
  └─ Completar instalación

□ Verificar instalación
  └─ Abre VeraCrypt desde menú Inicio
  └─ Debe aparecer GUI con botones: Mount / Dismount / Create Volume
  └─ Cierra VeraCrypt (solo queremos verificar que corre)

□ Documentar ruta instalación
  └─ Típicamente: C:\Program Files\VeraCrypt\VeraCrypt.exe
  └─ Guarda en tu wiki personal (carpeta Documentos)
```

**Prueba de Compatibilidad (Opcional pero Recomendado)**:
```
□ Crear contenedor VeraCrypt pequeño (prueba, 1GB) en C:\Temp\
  └─ Propósito: Validar que funciona crear, montar, desmontar
  └─ Pasos:
     1. VeraCrypt → Create Volume → Encrypted File Container
     2. Ubicación: C:\Temp\test_1gb.vc
     3. Tamaño: 1GB
     4. Algoritmo: AES-256 (default)
     5. Filesystem: NTFS
     6. Contraseña: algo_random_12345 (temporal, para prueba)
     7. Esperar creación (~1 minuto)

□ Montar contenedor de prueba
  └─ VeraCrypt → Select File → C:\Temp\test_1gb.vc
  └─ Click Mount
  └─ Pide contraseña → escribe algo_random_12345
  └─ Aparece unidad montada (ej: E:\ o F:\)

□ Escribir archivo de prueba
  └─ Abre E:\ (o la unidad montada)
  └─ Crea archivo de texto: "Esto es una prueba de VeraCrypt"
  └─ Guarda como prueba.txt
  └─ Cierra

□ Desmontar
  └─ VeraCrypt → Select File → C:\Temp\test_1gb.vc
  └─ Click Dismount
  └─ Unidad E:\ desaparece del explorador

□ Verificar integridad
  └─ Monta de nuevo (mismo proceso)
  └─ Abre E:\ → prueba.txt debe estar ahí con contenido intacto
  └─ Si está → ✓ VeraCrypt funciona correctamente

□ Limpiar
  └─ Desmonta test_1gb.vc
  └─ Elimina archivo C:\Temp\test_1gb.vc (ya no lo necesitas)
```

---

### 0.2 Documentación de Estructura de Datos Críticos

**¿Por qué ahora?**: Necesitas saber EXACTAMENTE qué entra en `xochimilco.vc` antes de crear el contenedor.

**Nota**: La selección granular de archivos está en otra conversación (P2). Aquí definimos **estructura y categorías**.

```
□ Crear documento: C:\Users\[tu_usuario]\Documents\P8_Archivos_Criticos.txt

□ Completar con CATEGORÍAS (no archivos aún):

   CATEGORÍA A: IRREEMPLAZABLES (fotos, videos personales)
   └─ Ubicación típica: C:\Users\[tu_usuario]\Pictures\
   └─ Subdirs: [año]-[mes]-evento / viajes / familia
   └─ Estimado: ?? GB (MEDIR en Fase 0.5)

   CATEGORÍA B: CONFIGURACIONES Y CREDENCIALES (SSH, GPG, configs)
   └─ Ubicación típica: C:\Users\[tu_usuario]\.ssh\ 
                        C:\Users\[tu_usuario]\AppData\Roaming\[apps]\
   └─ CRÍTICO: NUNCA en la nube, NUNCA compartido
   └─ Estimado: ?? MB (típicamente <1GB)

   CATEGORÍA C: DOCUMENTOS DE IDENTIDAD (CVs, recibos, contratos)
   └─ Ubicación típica: C:\Users\[tu_usuario]\Documents\[proyectos]\
   └─ Estimado: ?? GB (MEDIR en Fase 0.5)

   CATEGORÍA D: PROYECTOS ACTIVOS (code, CAD, diseño)
   └─ Ubicación típica: C:\Users\[tu_usuario]\projects\
   └─ Estimado: ?? GB (MEDIR en Fase 0.5)

   CATEGORÍA E: REFERENCIAS (libros, manuales, papers)
   └─ Ubicación típica: C:\Users\[tu_usuario]\Downloads\ (históricos)
   └─ Estimado: ?? GB (MEDIR en Fase 0.5)

   TOTAL ESTIMADO: ?? GB (debe ser <300GB para caber en M.2)
```

---

### 0.3 Medición Real de Tamaños (Fase 0.5)

**¿Por qué?**: No puedes crear `xochimilco.vc` de 480GB si solo tienes 200GB de datos.

```
□ Abrir PowerShell como Admin
  └─ Botón derecho Start → Windows PowerShell (Admin)

□ Ejecutar comando para medir por carpeta:
  
  # Medir Documentos
  Get-ChildItem -Path "C:\Users\[tu_usuario]\Documents" -Recurse | 
    Measure-Object -Property Length -Sum | 
    Select-Object @{Name="Size_GB"; Expression={[math]::Round($_.Sum/1GB, 2)}}

  # Medir Pictures
  Get-ChildItem -Path "C:\Users\[tu_usuario]\Pictures" -Recurse | 
    Measure-Object -Property Length -Sum | 
    Select-Object @{Name="Size_GB"; Expression={[math]::Round($_.Sum/1GB, 2)}}

  # Medir .ssh y configs
  Get-ChildItem -Path "C:\Users\[tu_usuario]\.ssh" -Recurse | 
    Measure-Object -Property Length -Sum | 
    Select-Object @{Name="Size_MB"; Expression={[math]::Round($_.Sum/1MB, 2)}}

□ Tabular resultados en P8_Archivos_Criticos.txt
  └─ Documenta EXACTAMENTE cuánto tiene cada categoría
```

---

### 0.4 Plan de Contraseña VeraCrypt (SEGURIDAD CRÍTICA)

**¿Por qué ahora?**: La contraseña es tu única defensa si tenochtitlan se roba.

```
□ Generar contraseña fuerte
  
  Requisitos mínimos:
  ├─ Longitud: 16+ caracteres
  ├─ Caracteres: MAYÚS + minús + números + símbolos
  ├─ NO palabras diccionario
  ├─ NO información personal (fechas de nacimiento, nombres)
  
  Generador recomendado (local, sin internet):
  ├─ Python: python -c "import secrets; print(secrets.token_urlsafe(16))"
  ├─ Online seguro: https://www.lastpass.com/password-generator (desconectar internet después)
  ├─ Manual (si nada funciona): mezcla 16 caracteres random en papel

  Ejemplo BUENO: K#7mP2xR$vL9!jQ4nWz1@bT8cF3dE6
  Ejemplo MALO:  contraseña123 / 12345678 / myname2024

□ Almacenar contraseña de forma SEGURA
  
  Opción A: Papel físico (MÁS SEGURO)
  └─ Escribe contraseña en papel
  └─ Guarda en lugar seguro (caja fuerte, lugar oculto)
  └─ NO en tu escritorio, NO en notas digitales sin cifrar

  Opción B: KeePass local (BUENO)
  └─ Descargar KeePass (https://keepass.info/)
  └─ Crear base de datos KeePass con contraseña FUERTE para KeePass misma
  └─ Generar contraseña VeraCrypt dentro de KeePass
  └─ Guardar base de datos en C:\Users\[tu_usuario]\AppData\Local\KeePass\
  └─ BACKUP de base de datos KeePass en tenochtitlan (cuando llegue)

  Opción C: Manager integrado Windows (NO RECOMENDADO)
  └─ Windows Credential Manager no está diseñado para secretos de larga vida
  └─ Evitar si es posible

□ DOCUMENTAR plan de acceso en caso de emergencia
  └─ Ejemplo: "Si pierdo acceso a KeePass, contraseña está en caja fuerte del escritorio"
  └─ Guardar este plan en lugar seguro TAMBIÉN
```

---

### 0.5 Estructura Wiki Personal (Documentación)

**¿Por qué?**: Necesitas tracking visual de todo el proceso.

```
□ Crear carpeta: C:\Users\[tu_usuario]\Documents\P8_Backup_Wiki\

□ Crear archivos:

   1. README.md
      └─ Descripción proyecto, objetivo final, timeline
      └─ Link a cada sección de la wiki

   2. Hardware_Specs.md
      └─ tenochtitlan 500GB: specs, llegada estimada
      └─ Carcasa USB-C: compatibilidad verificada
      └─ Modelos HDD futuros (cuando llegue Fase 2)

   3. Software_Setup.md
      └─ VeraCrypt: versión, ruta instalación, parámetros
      └─ VeraCrypt CLI flags para Linux (cuando llegue)
      └─ rsync: sintaxis exacta para backups
      └─ LUKS: parámetros para Fase 2

   4. Archivos_Criticos_Inventory.md
      └─ Categorías + tamaños medidos
      └─ Rutas exactas en Windows
      └─ Checklist de qué entra en xochimilco.vc

   5. Seguridad_Credenciales.md
      └─ Dónde está guardada contraseña VeraCrypt
      └─ Plan de acceso en emergencia
      └─ Backup de credenciales (si aplica)

   6. Timeline_Fases.md
      └─ Copia de este documento
      └─ Anota fechas reales cuando complete cada paso

□ Vincular estos archivos desde P8_Backup_Wiki\README.md
  └─ Así todo está centralizado y visible
```

---

### 0.6 Preparativos Técnicos Menores

```
□ Verificar espacio libre en C:\
  └─ Necesitas al menos 10GB libre para operaciones (temporal)
  └─ Si tienes <10GB: limpiar caché, desinstalar software innecesario

□ Descargar e instalar 7-Zip (para comprimir datos si es necesario)
  └─ https://www.7-zip.org/
  └─ Alternativa: Usar tar en PowerShell (más avanzado)

□ Instalar rsync en Windows (para futuro)
  └─ Opción: WSL2 (Windows Subsystem for Linux)
     ├─ Habilita WSL2 en Windows
     ├─ Instala distribución Linux (Ubuntu/Arch en WSL)
     ├─ rsync está disponible en Linux subsystem
     └─ Más adelante, cuando migres completamente a Linux
  
  └─ Opción: Robocopy nativo (Windows)
     └─ Comando: robocopy [origen] [destino] /E /V
     └─ Funciona, menos potente que rsync, pero no requiere instalación

□ Nota: NO instales estas herramientas aún si no las necesitas hoy
  └─ Mantén Windows limpio hasta migración
```

---

## FASE 1: tenochtitlan + VeraCrypt

**Objetivo**: Backup crítico en tenochtitlan con VeraCrypt, acceso desde Windows y Linux.  
**Duración**: 2-3 semanas (espera + creación + validación)  
**Trigger**: Recepción tenochtitlan + carcasa USB-C  
**Prerequisito**: FASE 0 completada

### 1.1 Recepción y Setup Físico

```
□ tenochtitlan 500GB llega
  └─ Desempaque
  └─ Inspecciona: sin daño físico

□ Carcasa USB-C llega
  └─ Desempaque
  └─ Verifica incluya: cable USB-C, adaptador poder, manual

□ Instalar tenochtitlan en carcasa
  └─ Apaga laptop
  └─ Abre carcasa (típicamente: destornillador Phillips pequeño)
  └─ Inserta tenochtitlan en slot M.2 (ángulo 30°, presiona suavemente)
  └─ Asegura con tornillo
  └─ Cierra carcasa
  └─ Enciende laptop

□ Conectar tenochtitlan vía USB-C
  └─ Usa puerto USB-C principal (si tienes Thunderbolt 3/4 mejor)
  └─ Windows debe detectar automáticamente como "Disco externo"
  └─ Verifica en Administrador de discos (diskmgmt.msc)
  └─ Nota la letra asignada (ej: D:\)
```

### 1.2 Crear Contenedor VeraCrypt en tenochtitlan

```
□ Conecta tenochtitlan (si no está conectada)

□ Abre VeraCrypt (Windows)
  └─ Click: Create Volume

□ Selecciona: Encrypted File Container
  └─ Click: Next

□ Ubicación del contenedor:
  └─ Browse → D:\xochimilco.vc (donde D:\ es tenochtitlan)
  └─ Nombre: xochimilco
  └─ Extensión: .vc (automática)

□ Tamaño del contenedor:
  └─ Si total datos <300GB → crea contenedor de 400GB
  └─ Si total datos ~200GB → crea contenedor de 300GB
  └─ (Basado en medidas de Fase 0.5)
  └─ Esto deja margen para crecimiento + overhead

□ Algoritmo de cifrado:
  └─ Default: AES-512 (excelente, no cambies)

□ Filesystem:
  └─ Default: NTFS (compatible Windows + Linux)

□ Contraseña:
  └─ Introduce contraseña guardada en Fase 0.4
  └─ Verifica dos veces (sin errores)

□ Crear volumen
  └─ Click: Format
  └─ Espera proceso (5-10 minutos para 400GB)
  └─ Barra de progreso
  └─ Cuando termine: "Volume created successfully"

□ Verificar creación
  └─ Cierra VeraCrypt
  └─ Abre Administrador de archivos
  └─ Ve a D:\ → debe estar vacía (tenochtitlan, no el contenedor)
  └─ Busca archivo xochimilco.vc (~400GB)
  └─ Si lo ves → ✓ Contenedor creado correctamente
```

### 1.3 Montar y Poblar Contenedor

```
□ Montar contenedor en VeraCrypt
  └─ Abre VeraCrypt
  └─ Click: Select File
  └─ Navega a D:\xochimilco.vc
  └─ Click: Mount
  └─ Pide contraseña → introduce la guardada
  └─ Asigna letra (ej: E:\)
  └─ Click: OK
  └─ Espera 10-20 segundos (montaje)

□ Verificar montaje
  └─ Abre Administrador de archivos
  └─ Debe aparecer nueva unidad E:\ (o la que asignó VeraCrypt)
  └─ Si ves "VERACRYPT VOLUME" en la unidad → ✓ Montada correctamente

□ Copiar archivos críticos
  └─ Basado en P2 (otra conversación, aquí usamos estructura de Fase 0.2)
  └─ Copiar CATEGORÍA A (fotos) → E:\Fotos\
  └─ Copiar CATEGORÍA B (credenciales) → E:\Credenciales\
  └─ Copiar CATEGORÍA C (documentos) → E:\Documentos\
  └─ Copiar CATEGORÍA D (proyectos) → E:\Proyectos\
  └─ Copiar CATEGORÍA E (referencias) → E:\Referencias\

□ Método de copia:
  └─ Opción A: Arrastra y suelta en Administrador de archivos (GUI, lento)
  └─ Opción B: Robocopy desde PowerShell (CLI, rápido)
  
     # Ejemplo con Robocopy:
     robocopy C:\Users\[tu_usuario]\Pictures E:\Fotos /E /V
     robocopy C:\Users\[tu_usuario]\.ssh E:\Credenciales /E /V
     robocopy C:\Users\[tu_usuario]\Documents E:\Documentos /E /V

□ Verificar copias
  └─ Abre E:\ en Administrador de archivos
  └─ Confirma que directorios aparecen (Fotos/, Documentos/, etc.)
  └─ Abre un archivo de prueba → debe abrir normalmente (sin corrupción)

□ Calcular espacio usado
  └─ Click derecho E:\ → Propiedades
  └─ Nota: "Espacio usado" vs. "Tamaño total"
  └─ Documenta en P8_Archivos_Criticos.md (actualizar)

□ Desmountar contenedor
  └─ VeraCrypt → Select E:\ (VERACRYPT VOLUME)
  └─ Click: Dismount
  └─ E:\ desaparece del explorador
  └─ xochimilco.vc sigue en D:\ (cifrado)
```

### 1.4 Verificación de Integridad (Windows)

```
□ Montar contenedor de nuevo
  └─ Proceso idéntico a 1.3
  └─ Asigna misma letra o diferente (ej: F:\)

□ Verificar contenido intacto
  └─ Abre F:\ (o la nueva letra)
  └─ Navega a Fotos/ → abre una foto (visualiza que se ve correctamente)
  └─ Navega a Documentos/ → abre un PDF o .txt
  └─ Si todo abre sin error → integridad OK

□ Opción avanzada: Hash SHA256
  └─ PowerShell Admin:
     Get-ChildItem -Path "F:\Fotos" -Recurse | 
       Get-FileHash -Algorithm SHA256 | 
       Export-Csv -Path "C:\hash_fotos_baseline.csv" -NoTypeInformation

  └─ Guarda este CSV en lugar seguro (también en tenochtitlan, carpeta separada)
  └─ Usarás para verificaciones futuras (Fase 2)

□ Desmountar
  └─ VeraCrypt → Dismount
  └─ F:\ desaparece
```

### 1.5 Preparación para Migración a Linux

```
□ Descargar VeraCrypt para Linux (adelantado)
  └─ https://www.veracrypt.fr/ → Linux version
  └─ Guardar en carpeta Descargas (para cuando instales Linux)
  └─ O preparar instalación via pacman/apt en Arch

□ Documentar procedimiento montaje VeraCrypt en Linux
  └─ Crear archivo: P8_Backup_Wiki/VeraCrypt_Linux_Setup.md
  
  Ejemplo contenido:
  ```bash
  # Instalación en Arch Linux COSMIC
  sudo pacman -S veracrypt
  
  # Montaje:
  veracrypt --text --mount /media/usb/xochimilco.vc /mnt/backup_mounted --password=TU_CONTRASEÑA
  
  # Acceso:
  ls -lah /mnt/backup_mounted/
  
  # Desmontaje:
  veracrypt --text --dismount /mnt/backup_mounted
  ```

□ Validación CLI en Windows (opcional, adelantado)
  └─ VeraCrypt incluye CLI además de GUI
  └─ Comando: "veracrypt" en PowerShell
  └─ Permite automatización futura (scripts)
```

### 1.6 Checklist Fase 1

```
□ Recibir tenochtitlan + carcasa USB-C
□ Instalar tenochtitlan en carcasa (físico)
□ Conectar tenochtitlan vía USB-C a laptop
□ Descargar VeraCrypt (Windows)
□ Instalar VeraCrypt (Windows)
□ Crear contenedor xochimilco.vc (200GB)
□ Montar contenedor en VeraCrypt
□ Copiar archivos críticos (Categorías A-E)
□ Verificar integridad (lectura post-copia)
□ Generar hash baseline (SHA512)
□ Documentar procedimiento montaje Linux
□ Desmountar y guardar tenochtitlan en lugar seguro
□ ACTUALIZAR P8_Backup_Wiki con datos reales
```

---

## FASE 2: HDD_A LUKS

**Objetivo**: Almacenamiento primario 2TB cifrado con LUKS full-disk.  
**Duración**: 1-2 semanas (compra, setup, migración)  
**Trigger**: Presupuesto disponible + completar Fase 1  
**Prerequisito**: Migración a Linux Arch COSMIC completada

### 2.1 Selección y Compra HDD_A

```
□ Especificaciones (ver documento P8_Componentes.md):
  ├─ Capacidad: 2TB
  ├─ Forma: 3.5" SATA
  ├─ RPM: 5400-7200
  ├─ Cache: ≥64MB
  ├─ MTBF: ≥60,000 horas

□ Modelos recomendados (BBB):
  ├─ WD Red Pro 2TB (~$60-70 USD)
  ├─ Seagate IronWolf 2TB (~$60-70 USD)
  └─ (Ambos son confiables y costo-efectivos)

□ Comprar HDD_A
  └─ Recibir + inspeccionar (sin daño)

□ Comprar enclosure USB 3.1 UASP
  └─ Especificaciones (ver documento):
     ├─ USB 3.1 Type-A o USB-C
     ├─ 3.5" SATA
     ├─ UASP protocol
     └─ Conectores 12V+5V
  
  └─ Modelo recomendado: Sabrent EC-US31 (~$20-30 USD)
```

### 2.2 Instalación HDD_A en Enclosure

```
□ Apagar laptop
□ Abrir enclosure (tornillero Phillips)
□ Instalar HDD_A:
  └─ Enchufa conectores SATA (datos + poder)
  └─ Asegura con tornillos
  └─ Cierra enclosure
□ Enciende laptop
□ Conecta enclosure vía USB → Linux detecta automáticamente
  └─ Verifica: lsblk | grep sdb (o similar)
```

### 2.3 Configurar LUKS Full-Disk en HDD_A

```
□ Identificar disco
  sudo lsblk -o NAME,SIZE,TYPE
  
  Resultado típico:
  sdb           2T disk  ← Este es tu HDD_A
  ├─sdb1        2T part

□ Desmountar si está montado
  sudo umount /dev/sdb1

□ Cifrar con LUKS
  sudo cryptsetup luksFormat --cipher aes-xts-plain64 --key-size 256 /dev/sdb1
  
  VeraCrypt solicitará contraseña:
  └─ Escribe contraseña fuerte (≠ a VeraCrypt si es posible)
  └─ Confirma dos veces

□ Abrir volumen LUKS
  sudo cryptsetup luksOpen /dev/sdb1 hdd_a_decrypted
  
  (Esto crea archivo de dispositivo virtual en /dev/mapper/hdd_a_decrypted)

□ Formatear con filesystem
  sudo mkfs.ext4 /dev/mapper/hdd_a_decrypted -L "HDD_A_LUKS"
  
  (Elige ext4 por compatibilidad y recuperación de datos)

□ Montar
  sudo mount /dev/mapper/hdd_a_decrypted /mnt/hdd_a
  
  Verifica:
  ls -la /mnt/hdd_a
  
  Debe estar vacío y montado.

□ Verificar permiso de escritura
  touch /mnt/hdd_a/test.txt
  rm /mnt/hdd_a/test.txt
  
  Si funciona → permisos OK
```

### 2.4 Sincronizar tenochtitlan → HDD_A (rsync)

```
□ Montar tenochtitlan en Linux
  veracrypt --text --mount /media/usb/xochimilco.vc /mnt/backup_tenochtitlan --password=TU_CONTRASEÑA

□ Sincronizar tenochtitlan hacia HDD_A
  rsync -avz --checksum /mnt/backup_tenochtitlan/ /mnt/hdd_a/backup/ --delete
  
  Explicación flags:
  ├─ -a: archive (permisos, timestamps)
  ├─ -v: verbose (ve el progreso)
  ├─ -z: comprime en tránsito
  ├─ --checksum: verifica integridad post-copia
  └─ --delete: sincronización bidireccional

□ Esperar finalización
  └─ Depende tamaño datos (200GB = 30-60 minutos)
  └─ Console mostrará "X files transferred"

□ Verificar integridad
  Opción A: SHA256 (si creaste baseline en Fase 1.4)
  sha256sum -c /mnt/hdd_a/backup/hash_fotos_baseline.csv
  
  Opción B: Contar archivos
  find /mnt/backup_tenochtitlan -type f | wc -l
  find /mnt/hdd_a/backup -type f | wc -l
  
  (Ambos deben ser idénticos)

□ Desmountar tenochtitlan
  veracrypt --text --dismount /mnt/backup_tenochtitlan
```

### 2.5 Automatizar rsync con cron (Futuro)

```
□ Editar crontab
  crontab -e
  
  Añadir línea (ejecutar rsync cada mes, primer domingo a las 02:00):
  0 2 * * 0 rsync -av --checksum /media/usb/backup_tenochtitlan/ /mnt/hdd_a/backup/ --delete >> /var/log/rsync_hdd_a.log 2>&1

□ Alternativa: Script bash + cron
  Crear archivo: ~/bin/sync_tenochtitlan_to_hdd_a.sh
  
  ```bash
  #!/bin/bash
  TENOCHTITLAN_MOUNT="/mnt/backup_tenochtitlan"
  HDD_A="/mnt/hdd_a/backup"
  LOGFILE="/var/log/rsync_hdd_a.log"
  
  # Montar tenochtitlan
  veracrypt --text --mount /media/usb/xochimilco.vc $TENOCHTITLAN_MOUNT --password=TU_CONTRASEÑA
  
  # Sincronizar
  rsync -avz --checksum $TENOCHTITLAN_MOUNT/ $HDD_A/ --delete >> $LOGFILE 2>&1
  
  # Desmountar
  veracrypt --text --dismount $TENOCHTITLAN_MOUNT
  
  echo "Backup sync completado: $(date)" >> $LOGFILE
  ```
  
  Hacer ejecutable:
  chmod +x ~/bin/sync_tenochtitlan_to_hdd_a.sh
  
  Añadir a crontab:
  0 2 * * 0 ~/bin/sync_tenochtitlan_to_hdd_a.sh
```

### 2.6 Checklist Fase 2

```
□ Comprar HDD_A 2TB (WD Red Pro o Seagate IronWolf)
□ Comprar enclosure USB 3.1 UASP
□ Instalar HDD_A en enclosure
□ Conectar a laptop + verificar detección
□ Cifrar con LUKS full-disk
□ Formatear con ext4
□ Montar en /mnt/hdd_a
□ Sincronizar tenochtitlan → HDD_A (rsync)
□ Verificar integridad (SHA256 o count files)
□ Automatizar rsync con cron
□ Documentar procedimiento en P8_Backup_Wiki/LUKS_Setup.md
□ Guardar contraseña LUKS en lugar seguro
```

---

## FASE 3: HDD_B Redundancia Geográfica

**Objetivo**: Copia idéntica HDD_A, almacenada fuera ubicación principal.  
**Duración**: 2-3 semanas (compra + clonación)  
**Trigger**: Completar Fase 2 + disponibilidad almacenamiento geográfico  
**Prerequisito**: HDD_A funcional y sincronizado

### 3.1 Selección y Compra HDD_B

```
□ Comprar HDD_B idéntico a HDD_A
  └─ Especificaciones: 2TB, 3.5" SATA, MTBF ≥60k
  └─ Modelo: WD Red Pro 2TB (mismo que HDD_A)
  └─ Razón: Garantiza compatibilidad y consistencia

□ Comprar segundo enclosure USB 3.1 UASP
  └─ Especificaciones idénticas al de HDD_A
  └─ Modelo: Sabrent EC-US31
```

### 3.2 Instalación HDD_B en Enclosure

```
□ Procedimiento idéntico a 2.2
  └─ Apagar, abrir enclosure, instalar HDD_B, cerrar, enciender
  └─ Conectar vía USB
  └─ Verificar con lsblk
```

### 3.3 Clonación Full-Disk HDD_A → HDD_B (ddrescue)

```
□ Identificar discos
  sudo lsblk -o NAME,SIZE,TYPE
  
  Resultado:
  sdb           2T ← HDD_A (origen, LUKS)
  sdc           2T ← HDD_B (destino, vacío)

□ Clonar con ddrescue (preserva LUKS)
  sudo ddrescue --force /dev/sdb /dev/sdc --verbose
  
  Flags:
  ├─ --force: no pide confirmación (cuidado: destructivo)
  ├─ --verbose: muestra progreso
  └─ Resultado: clonación bit-a-bit (incluyendo tabla particiones + LUKS)

□ Esperar finalización
  └─ 2TB = 2-4 horas depende velocidad USB
  └─ Consola mostrará "Copying data..."
  └─ Al terminar: "Finished successfully"

□ Desmontar ambos discos
  sudo umount /dev/mapper/hdd_a_decrypted (si estaba montado)
  sudo umount /dev/sdb /dev/sdc
```

### 3.4 Verificación Integridad Post-Clonación

```
□ Opción A: MD5 simple
  sudo md5sum /dev/sdb > /tmp/hdd_a.md5
  sudo md5sum /dev/sdc > /tmp/hdd_b.md5
  diff /tmp/hdd_a.md5 /tmp/hdd_b.md5
  
  Si no hay output → hashes idénticos → ✓ Clonación perfecta

□ Opción B: Montar HDD_B y verificar contenido
  sudo cryptsetup luksOpen /dev/sdc hdd_b_decrypted
  sudo mount /dev/mapper/hdd_b_decrypted /mnt/hdd_b_test
  
  # Contar archivos
  find /mnt/hdd_b_test -type f | wc -l
  find /mnt/hdd_a -type f | wc -l
  
  # Deben ser idénticos
  
  sudo umount /mnt/hdd_b_test
  sudo cryptsetup luksClose hdd_b_decrypted

□ Crear archivo de verificación
  └─ Guarda hash/logs en tenochtitlan o local
  └─ Documenta fecha clonación, tamaño, resultado
```

### 3.5 Almacenamiento Geográfico HDD_B

```
□ Seleccionar ubicación segura
  
  Opciones:
  ├─ Casa de padres/hermano de confianza (LOCAL)
  ├─ Casillero de seguridad bancario (CARO pero seguro)
  ├─ Casa de amigo cercano (VERIFICADO)
  └─ Office coworking con CCTV (CARO pero confiable)

□ Empacar HDD_B
  └─ Coloca en caja antiestática
  └─ Abre-cierra con papel burbuja (protege vibraciones)
  └─ Etiqueta: "BACKUP CRÍTICO — NO MOVER" (evita accidentes)

□ Transportar
  └─ Manejo cuidadoso (HDD es mecánico, sensible a caídas)
  └─ NO en morral de motos (vibración excesiva)
  └─ Vehículo personal, caja fija

□ Almacenar
  └─ Lugar fresco, seco (evita humedad/calor extremo)
  └─ Estante o caja: NO en piso (riesgo inundación)
  └─ LUKS cifrado: si se pierde, datos no accesibles sin contraseña

□ Documentar ubicación
  └─ Guarda información en lugar seguro:
     ├─ Dirección exacta
     ├─ Contacto persona que lo guarda
     ├─ Fecha entrega
     └─ Fecha última verificación
```

### 3.6 Verificación Periódica HDD_B (Anual)

```
□ Cada 12 meses, acceder a HDD_B
  └─ Recuperar del almacenamiento geográfico
  └─ Conectar vía USB a laptop
  └─ Montar LUKS (desbloquea con contraseña)
  └─ Lectura spot-check (abre algunos archivos)
  └─ Calcular hash si tienes tiempo

□ Si todo está bien
  └─ Desmountar, reempacar
  └─ Devolver a almacenamiento geográfico
  └─ Documentar fecha verificación

□ Si hay problema (corrupción, no arranca)
  └─ NO DESESPERES: tienes HDD_A como origen
  └─ Clona de nuevo HDD_A → HDD_B_nueva
  └─ Desecha HDD_B vieja si es irrecuperable

□ Documentar en log
  └─ Crear archivo: P8_Backup_Wiki/HDD_B_Verification_Log.md
  └─ Anota cada verificación con fecha, resultado, acciones
```

### 3.7 Checklist Fase 3

```
□ Comprar HDD_B 2TB (idéntico a HDD_A)
□ Comprar segundo enclosure USB 3.1
□ Instalar HDD_B en enclosure
□ Conectar a laptop + verificar detección
□ Clonar HDD_A → HDD_B con ddrescue
□ Verificar integridad post-clonación (MD5 o contenido)
□ Empacar HDD_B en caja antiestática
□ Transportar a ubicación geográfica segura
□ Documentar ubicación (dirección, contacto, fechas)
□ Configurar alarma anual para verificación HDD_B
□ Crear log de verificaciones periódicas
```

---

## Timeline por Fases (checklist real)

### FASE 0 — completada 2026-03-31
- [x] VeraCrypt instalado y validado en Windows 11
- [x] Inventario de archivos críticos completado (PowerShell)
- [x] Tamaños medidos por categoría
- [x] Backup selectivo en USB 32GB (7.7GB / 24GB disponibles)
- [x] Wiki P8 creada
- [x] Contraseña VeraCrypt generada y almacenada

### FASE 1 — completada 2026-04-01 (trigger: llegada tenochtitlan + carcasa)
- [x] tenochtitlan recibido y verificado físicamente
- [x] tenochtitlan instalado en carcasa USB-C
- [x] Conectado y detectado (465 GB)
- [x] GPT creada, partición NTFS
- [x] VeraCrypt instalado en Windows
- [x] `backup_critico.vc` creado (150 GB, NTFS)
- [x] Archivos críticos copiados (OneDrive ITESO, Programas, Música, Galerías)
- [x] Integridad verificada (lectura post-copia)
- [x] Hash SHA512 baseline generado → dentro del contenedor
- [x] Procedimiento montaje Linux documentado → raíz de tenochtitlan
- Fecha inicio real: 31/03/2026

### FASE 1.5 — completada 2026-08-30 (migración a Linux)
- [x] Contenedor verificado tras 5 meses: 19,040 archivos, 0 errores de lectura
- [x] Respaldo automatizado de fibonacci creado (`respaldar-fibonacci`)
- [x] $HOME respaldado: 16,214 archivos / 4.83 GB, manifiesto SHA256 verificado
- [x] Archivos de sistema empaquetados (`sistema.tar.gz`, 9 rutas con permisos)
- [x] Guía de restauración escrita (`RESTAURAR.md`)
- [x] Receta autocontenida en el disco (`fibonacci/receta/`)
- [x] Cubot: carrete de cámara respaldado (583 archivos / 5.1 GB)
- [ ] Prueba real de restauración en hardware distinto o VM
- Fecha inicio real: 30/08/2026

### FASE 2 — pendiente (trigger: presupuesto + Linux migrado — Linux ya migrado, falta presupuesto)
- [ ] Comprar HDD_A 2TB + enclosure
- [ ] Cifrar con LUKS full-disk
- [ ] rsync tenochtitlan → HDD_A
- [ ] Automatizar con cron (mensual)
- Fecha inicio real: pendiente

### FASE 3 — pendiente (trigger: completar FASE 2)
- [ ] Comprar HDD_B idéntico a HDD_A
- [ ] Clonar HDD_A → HDD_B con ddrescue
- [ ] Almacenar HDD_B geográficamente
- [ ] Configurar verificación anual
- Fecha inicio real: pendiente

```
TOTAL INVERSIÓN ORIGINAL ESTIMADA: ~$330-350 USD (distribuido en tiempo)
MÁXIMA PROTECCIÓN: Redundancia geográfica, cifrado full-disk, backups verificados
```

---

## Inventario de Archivos Críticos

**Backup USB inicial**: 32GB · `F:\backup_danyb_2026` · 7.7GB usados · 2026-03-31

| Carpeta en USB | Origen | Contenido |
|---|---|---|
| `Programas PerformanceDesigns\` | `C:\Users\danyb\` | CutWindow_2, DeepNestSharp, NestingTesting, O2BToDxf y más — código fuente completo |
| `Música\*` (Hard Groove, Mi Musica, MIXO, PsyTrance) | `C:\Users\danyb\Music\` | MP3s personales y DJ |
| `MATLAB\` | `C:\Users\danyb\Documents\MATLAB\` | Ejemplo3_BombaCentrifuga, ICE codes, Vibraciones |
| `jueguitos\` | varios | Civilization VI, Los Sims 4, GTA V, Minecraft — saves seleccionados |
| `VSCode_user_config\` + `VSCode_extensions.txt` | `AppData\Roaming\Code\User\` | settings.json, keybindings, snippets, 14 extensiones |
| `AppData_Roaming\Cura_perfiles\` | `AppData\Roaming\cura\` | Perfiles Creality Ender-3 v2 Neo |
| `AppData_Roaming\CIMCO_AS\` | `AppData\Roaming\CIMCO AS\` | Macros .MAC (haas, heidenhain, iso), configs máquina |
| `.gitconfig` (raíz USB) | — | Config global git (user: eldaniels13, editor: nvim) |

**Categorías cubiertas:** A (irreemplazables personales) ✅ música · B (credenciales/configs) ✅ git/VSCode/Cura/CIMCO · C (documentos) ✅ universidad+MATLAB · D (proyectos activos) ✅ código fuente completo · E (referencias/juegos) ✅ saves seleccionados.

**Decisiones conscientes de exclusión:** instaladores SOLIDWORKS (8.9GB, reinstalable desde cuenta uni) · AutoCAD (licencia educativa caducada) · FL Studio (sin proyectos propios) · rekordbox (uso básico) · caché AppData (Mozilla, Discord, Minecraft — regenerable).

### Configs de sistema Arch Linux (fuera del repo — backup obligatorio)

**Regla dura:** viven en `~/.config/` y `/etc/` — NUNCA dentro de `mi-criterio/`. El repo solo los **documenta** (`recursos/ARCH_LINUX_SETUP_REFERENCE.md`); los archivos vivos van al backup externo.

| Archivo vivo (ruta real) | Qué hace | Cómo recrear |
|---|---|---|
| `~/.config/wireplumber/wireplumber.conf.d/51-bose-no-suspend.conf` | Evita que WirePlumber suspenda por inactividad el sink Bose USB (audio mudo tras pausa) | `restore.sh` del bundle externo |
| `/etc/udev/rules.d/99-bose-usb-no-autosuspend.rules` | Desactiva USB autosuspend del Bose (05a7:1020), persistente a reboot/replug | idem |

**Verificación post-restauración:** `pactl list short sinks | grep -i bose` → `IDLE` (no `SUSPENDED`) tras reproducir y pausar; Bose `power/control` = `on`.

### Reproducibilidad post-reinstall — bundle `arch-setup-backup/`

**Decisión (2026-06-20):** el mecanismo de restauración es un **bundle en el backup externo**
(Kingston/USB), NO en ningún repo. El repo solo describe; el backup contiene y restaura.

```
arch-setup-backup/
├── restore.sh              # recrea configs + reinstala paquetes (idempotente)
├── README.md               # qué hace y cómo correrlo tras reinstall
├── configs/
│   ├── wireplumber/51-bose-no-suspend.conf
│   └── udev/99-bose-usb-no-autosuspend.rules
├── pkglist-official.txt    # pacman -Qqe
└── pkglist-aur.txt         # pacman -Qqm
```

**Estado del bundle (verificado 2026-08-28):** congelado desde 2026-06-20 — 2 configs, 2 pkglists,
`restore.sh`, `README.md`, ~2 meses desactualizado. **Faltan los archivos nuevos del comando
`refresh`** (2026-08-28): `~/.zshrc` (función `refresh`), `~/.local/bin/refresh-system`,
`/usr/local/bin/refresh-system-privileged{,-hard}`, `/etc/sudoers.d/refresh-system` — documentados
en `proyectos/P2/COSMIC_setup_custom.md` §9.4, pendientes de incorporar al bundle.

**No incluido en el bundle (manejo aparte, backup cifrado):** `~/.ssh/` claves privadas — nunca en
repo ni en bundle plano · credenciales/tokens.

**Patrón de fallo identificado (28-08):** un procedimiento manual documentado se desactualiza; uno
automatizado no. `refresh-system` dejó de ser manual y por eso se mantiene vivo — el bundle de
backup sigue siendo manual y por eso lleva 2 meses congelado. **La automatización no es
optimización: es la única forma de que el backup exista cuando haga falta.**

---

## Gaps Identificados y Soluciones

| Gap | Descripción | Solución |
|---|---|---|
| **Contraseña VeraCrypt** | Dónde guardarla de forma segura | Fase 0.4: Papel físico + KeePass dual backup |
| **Sincronización automática** | tenochtitlan → HDD_A sin intervención manual | Fase 2.5: Script bash + cron (mensual) |
| **Verificación periódica** | Confirmar que no hay bit rot en HDD_B | Fase 3.6: Alarma anual, log de auditoría |
| **Recuperación de desastre** | Qué hacer si tenochtitlan se pierde/daña | Respuesta: HDD_A es origen, HDD_B copia; recrear tenochtitlan desde HDD_A |
| **Escalabilidad futura** | ¿Qué si necesitas más de 2TB? | Expandir LUKS: agregar nuevo HDD (LUKS soporta múltiples discos) |
| **Auditoría y trazabilidad** | Tracking de cambios y accesos | Mantener logs en P8_Backup_Wiki/ (fechas, hashes, operaciones) |
| **Obsolescencia tecnológica** | ¿Y si LUKS se vuelve inseguro en 20 años? | Verificaciones periódicas + migrar si es necesario (LUKS es resiliente a cambios SO) |
| **Acceso en emergencia** | ¿Si necesito datos urgentemente y no recuerdo contraseña? | Documento de emergencia con instrucciones + contactos de backup (papeles, familia) |

---

## Notas Finales

- **Cada fase es independiente pero secuencial**: No puedes saltar Fase 0.
- **Tiempo ≠ Complejidad**: Fase 0 toma una semana pero es simple.
- **Costo distribuido**: No es $350 de golpe, es ~$150 inicial + $90-100 en 6-12 meses.
- **Soberanía real**: Los datos están en TUS máquinas, cifrados con contraseña QUE SOLO TÚ SABES.
- **BBB confirmado**: Máxima funcionalidad (protección contra 5 amenazas), mínimo costo (sin NAS), máxima soberanía (offline, local, sin terceros).

---

**Última actualización**: 2026-08-30
**Versión**: 2.0
**Mantenedor**: Tú (P8 Project)
