# Timeline_Fases

## FASE 0 — completada 2026-03-31
- [x] VeraCrypt instalado y validado en Windows 11
- [x] Inventario de archivos críticos completado (PowerShell)
- [x] Tamaños medidos por categoría
- [x] Backup selectivo en USB 32GB (7.7GB / 24GB disponibles)
- [x] Wiki P8 creada
- [x] Contraseña VeraCrypt generada y almacenada KeeperSecurity

## FASE 1 — pendiente (trigger: llegada Kingston NV3 + carcasa)
- [x] Kingston NV3 recibido y verificado físicamente
- [x] Kingston instalado en carcasa USB-C
- [x] Conectado y detectado (Disco 3, 465 GB, En línea)
- [x] GPT creada, partición NTFS K:\
- [x] VeraCrypt instalado en Windows
- [x] backup_critico.vc creado (200 GB, exFAT)
- [x] Archivos críticos copiados (OneDrive ITESO, Programas, Música, Fotos, MATLAB)
- [x] Integridad verificada (lectura post-copia)
- [x] Hash SHA512 baseline generado → K:\hash_baseline_2026-04-01.csv
- [x] Procedimiento montaje Linux documentado → K:\VeraCrypt_Linux_Montaje.txt
- [ ] Desmontar Z:\ en VeraCrypt antes de desconectar Kingston
Fecha inicio real: __31/03/2026__

## FASE 2 — pendiente (trigger: presupuesto + Linux migrado)
- [ ] Comprar HDD_A 2TB + enclosure
- [ ] Cifrar con LUKS full-disk
- [ ] rsync Kingston → HDD_A
- [ ] Automatizar con cron (mensual)
Fecha inicio real: ___________

## FASE 3 — pendiente (trigger: completar FASE 2)
- [ ] Comprar HDD_B idéntico a HDD_A
- [ ] Clonar HDD_A → HDD_B con ddrescue
- [ ] Almacenar HDD_B geográficamente
- [ ] Configurar verificación anual
Fecha inicio real: ___________
