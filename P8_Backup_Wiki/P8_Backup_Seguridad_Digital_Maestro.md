# Plan Maestro: Backup Digital Seguro y Soberanía de Datos

**Estado**: FASE 0 (Preparación sin Hardware)  
**Versión**: 1.0  
**Última actualización**: 2026-03-30  
**Objetivo**: 2TB máxima soberanía, cifrado LUKS, redundancia geográfica  

---

## 📋 Índice Rápido

- [FASE 0: Preparación (AHORA)](#fase-0-preparación-ahora)
- [FASE 1: Kingston + VeraCrypt](#fase-1-kingston--veracrypt)
- [FASE 2: HDD_A LUKS](#fase-2-hdd_a-luks)
- [FASE 3: HDD_B Redundancia](#fase-3-hdd_b-redundancia)
- [Timeline General](#timeline-general)
- [Gaps Identificados y Soluciones](#gaps-identificados-y-soluciones)

---

## FASE 0: Preparación (AHORA)

**Objetivo**: Preparar todo lo que podemos hacer mientras llega Kingston NV3 + carcasa USB-C.  
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

**¿Por qué ahora?**: Necesitas saber EXACTAMENTE qué entra en `backup_critico.vc` antes de crear el contenedor.

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

**¿Por qué?**: No puedes crear `backup_critico.vc` de 480GB si solo tienes 200GB de datos.

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

**¿Por qué ahora?**: La contraseña es tu única defensa si Kingston se roba.

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
  └─ BACKUP de base de datos KeePass en Kingston (cuando llegue)

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
      └─ Kingston NV3 500GB: specs, llegada estimada
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
      └─ Checklist de qué entra en backup_critico.vc

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

## FASE 1: Kingston + VeraCrypt

**Objetivo**: Backup crítico en Kingston con VeraCrypt, acceso desde Windows y Linux.  
**Duración**: 2-3 semanas (espera + creación + validación)  
**Trigger**: Recepción Kingston NV3 + carcasa USB-C  
**Prerequisito**: FASE 0 completada

### 1.1 Recepción y Setup Físico

```
□ Kingston NV3 500GB llega
  └─ Desempaque
  └─ Inspecciona: sin daño físico

□ Carcasa USB-C llega
  └─ Desempaque
  └─ Verifica incluya: cable USB-C, adaptador poder, manual

□ Instalar Kingston en carcasa
  └─ Apaga laptop
  └─ Abre carcasa (típicamente: destornillador Phillips pequeño)
  └─ Inserta Kingston en slot M.2 (ángulo 30°, presiona suavemente)
  └─ Asegura con tornillo
  └─ Cierra carcasa
  └─ Enciende laptop

□ Conectar Kingston vía USB-C
  └─ Usa puerto USB-C principal (si tienes Thunderbolt 3/4 mejor)
  └─ Windows debe detectar automáticamente como "Disco externo"
  └─ Verifica en Administrador de discos (diskmgmt.msc)
  └─ Nota la letra asignada (ej: D:\)
```

### 1.2 Crear Contenedor VeraCrypt en Kingston

```
□ Conecta Kingston (si no está conectada)

□ Abre VeraCrypt (Windows)
  └─ Click: Create Volume

□ Selecciona: Encrypted File Container
  └─ Click: Next

□ Ubicación del contenedor:
  └─ Browse → D:\backup_critico.vc (donde D:\ es Kingston)
  └─ Nombre: backup_critico
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
  └─ Ve a D:\ → debe estar vacía (Kingston, no el contenedor)
  └─ Busca archivo backup_critico.vc (~400GB)
  └─ Si lo ves → ✓ Contenedor creado correctamente
```

### 1.3 Montar y Poblar Contenedor

```
□ Montar contenedor en VeraCrypt
  └─ Abre VeraCrypt
  └─ Click: Select File
  └─ Navega a D:\backup_critico.vc
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
  └─ backup_critico.vc sigue en D:\ (cifrado)
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

  └─ Guarda este CSV en lugar seguro (también en Kingston, carpeta separada)
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
  veracrypt --text --mount /media/usb/backup_critico.vc /mnt/backup_mounted --password=TU_CONTRASEÑA
  
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
□ Recibir Kingston NV3 + carcasa USB-C
□ Instalar Kingston en carcasa (físico)
□ Conectar Kingston vía USB-C a laptop
□ Descargar VeraCrypt (Windows)
□ Instalar VeraCrypt (Windows)
□ Crear contenedor backup_critico.vc (200GB)
□ Montar contenedor en VeraCrypt
□ Copiar archivos críticos (Categorías A-E)
□ Verificar integridad (lectura post-copia)
□ Generar hash baseline (SHA512)
□ Documentar procedimiento montaje Linux
□ Desmountar y guardar Kingston en lugar seguro
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

### 2.4 Sincronizar Kingston → HDD_A (rsync)

```
□ Montar Kingston en Linux
  veracrypt --text --mount /media/usb/backup_critico.vc /mnt/backup_kingston --password=TU_CONTRASEÑA

□ Sincronizar Kingston hacia HDD_A
  rsync -avz --checksum /mnt/backup_kingston/ /mnt/hdd_a/backup/ --delete
  
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
  find /mnt/backup_kingston -type f | wc -l
  find /mnt/hdd_a/backup -type f | wc -l
  
  (Ambos deben ser idénticos)

□ Desmountar Kingston
  veracrypt --text --dismount /mnt/backup_kingston
```

### 2.5 Automatizar rsync con cron (Futuro)

```
□ Editar crontab
  crontab -e
  
  Añadir línea (ejecutar rsync cada mes, primer domingo a las 02:00):
  0 2 * * 0 rsync -av --checksum /media/usb/backup_kingston/ /mnt/hdd_a/backup/ --delete >> /var/log/rsync_hdd_a.log 2>&1

□ Alternativa: Script bash + cron
  Crear archivo: ~/bin/sync_kingston_to_hdd_a.sh
  
  ```bash
  #!/bin/bash
  KINGSTON_MOUNT="/mnt/backup_kingston"
  HDD_A="/mnt/hdd_a/backup"
  LOGFILE="/var/log/rsync_hdd_a.log"
  
  # Montar Kingston
  veracrypt --text --mount /media/usb/backup_critico.vc $KINGSTON_MOUNT --password=TU_CONTRASEÑA
  
  # Sincronizar
  rsync -avz --checksum $KINGSTON_MOUNT/ $HDD_A/ --delete >> $LOGFILE 2>&1
  
  # Desmountar
  veracrypt --text --dismount $KINGSTON_MOUNT
  
  echo "Backup sync completado: $(date)" >> $LOGFILE
  ```
  
  Hacer ejecutable:
  chmod +x ~/bin/sync_kingston_to_hdd_a.sh
  
  Añadir a crontab:
  0 2 * * 0 ~/bin/sync_kingston_to_hdd_a.sh
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
□ Sincronizar Kingston → HDD_A (rsync)
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
  └─ Guarda hash/logs en Kingston o local
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

## Timeline General

```
FASE 0 (Ahora - Semana 1-2)
├─ Instalar VeraCrypt Windows
├─ Medir tamaños archivos críticos
├─ Preparar wiki documentación
├─ Generar y almacenar contraseñas
└─ Tiempo: 7-10 días, $0

FASE 1 (Semana 2-4, tras recepción Kingston)
├─ Instalar Kingston en carcasa
├─ Crear contenedor VeraCrypt (480GB)
├─ Copiar archivos críticos
├─ Verificar integridad
├─ Documentar procedimiento Linux
└─ Tiempo: 2-3 semanas, ~$150 (hardware ya comprado)

FASE 2 (6-12 meses después, presupuesto HDD_A)
├─ Comprar HDD_A + enclosure
├─ Instalar LUKS full-disk
├─ rsync Kingston → HDD_A
├─ Automatizar con cron
└─ Tiempo: 1-2 semanas, ~$90-100

FASE 3 (12-18 meses después, presupuesto HDD_B)
├─ Comprar HDD_B + enclosure
├─ Clonar HDD_A → HDD_B
├─ Almacenar geográficamente
├─ Verificaciones anuales
└─ Tiempo: 2-3 semanas, ~$90-100

TOTAL INVERSIÓN: ~$330-350 USD (distribuido en tiempo)
MÁXIMA PROTECCIÓN: Redundancia geográfica, cifrado full-disk, backups verificados
```

---

## Gaps Identificados y Soluciones

| Gap | Descripción | Solución |
|---|---|---|
| **Contraseña VeraCrypt** | Dónde guardarla de forma segura | Fase 0.4: Papel físico + KeePass dual backup |
| **Sincronización automática** | Kingston → HDD_A sin intervención manual | Fase 2.5: Script bash + cron (mensual) |
| **Verificación periódica** | Confirmar que no hay bit rot en HDD_B | Fase 3.6: Alarma anual, log de auditoría |
| **Recuperación de desastre** | Qué hacer si Kingston se pierde/daña | Respuesta: HDD_A es origen, HDD_B copia; recrear Kingston desde HDD_A |
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

**Última actualización**: 2026-03-30  
**Versión**: 1.0  
**Mantenedor**: Tú (P8 Project)
