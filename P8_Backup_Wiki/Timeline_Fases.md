# Timeline_Fases

## FASE 0 — completada 2026-03-31
- [x] VeraCrypt instalado y validado en Windows 11
- [x] Inventario de archivos críticos completado (PowerShell)
- [x] Tamaños medidos por categoría
- [x] Backup selectivo en USB 32GB (7.7GB / 24GB disponibles)
- [x] Wiki P8 creada
- [x] Contraseña VeraCrypt generada y almacenada tepito

## FASE 1 — completada 2026-04-01 (trigger: llegada tenochtitlan + carcasa)
- [x] tenochtitlan recibido y verificado físicamente
- [x] tenochtitlan instalado en carcasa USB-C
- [x] Conectado y detectado (465 GB)
- [x] GPT creada, partición NTFS
- [x] VeraCrypt instalado en Windows
- [x] backup_critico.vc creado (150 GB, NTFS)
- [x] Archivos críticos copiados (OneDrive ITESO, Programas, Música, Galerías)
- [x] Integridad verificada (lectura post-copia)
- [x] Hash SHA512 baseline generado → dentro del contenedor
- [x] Procedimiento montaje Linux documentado → raíz de tenochtitlan
Fecha inicio real: __31/03/2026__

## FASE 1.5 — completada 2026-08-30 (migración a Linux)
- [x] Contenedor verificado tras 5 meses: 19,040 archivos, 0 errores de lectura
- [x] Respaldo automatizado de fibonacci creado (`respaldar-fibonacci`)
- [x] $HOME respaldado: 16,214 archivos / 4.83 GB, manifiesto SHA256 verificado
- [x] Archivos de sistema empaquetados (`sistema.tar.gz`, 9 rutas con permisos)
- [x] Guía de restauración escrita (`RESTAURAR.md`)
- [x] Receta autocontenida en el disco (`fibonacci/receta/`)
- [x] Cubot: carrete de cámara respaldado (583 archivos / 5.1 GB)
- [ ] Prueba real de restauración en hardware distinto o VM
Fecha inicio real: __30/08/2026__

## FASE 2 — pendiente (trigger: presupuesto + Linux migrado)
- [ ] Comprar HDD_A 2TB + enclosure
- [ ] Cifrar con LUKS full-disk
- [ ] rsync tenochtitlan → HDD_A
- [ ] Automatizar con cron (mensual)
Fecha inicio real: ___________

## FASE 3 — pendiente (trigger: completar FASE 2)
- [ ] Comprar HDD_B idéntico a HDD_A
- [ ] Clonar HDD_A → HDD_B con ddrescue
- [ ] Almacenar HDD_B geográficamente
- [ ] Configurar verificación anual
Fecha inicio real: ___________
