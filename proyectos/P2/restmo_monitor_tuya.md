# Monitor Restmo O-WM-2-BT vía Tuya Cloud API

**Fecha:** 2026-07-08 · **Lens:** P2 (programación) · **Host de ejecución:** laptop Windows (TME), no fibonacci
**Estado:** ✅ script v2 funcional — polling + persistencia + display en vivo

## Objetivo

Visualizar en tiempo real las mediciones del medidor de flujo de agua **Restmo O-WM-2-BT** (Bluetooth, ecosistema Tuya/SmartLife) sin depender de la app móvil, con vista a almacenamiento histórico, gráficos y exportación. Preferencia por soluciones OS-neutrales.

## Arquitectura final

```
Restmo O-WM-2-BT (BLE, encriptado, propietario)
  → Celular con SmartLife (A12)
  → Tuya Cloud (Western America Data Center)
  → Laptop Windows — Python + tinytuya
  → SQLite (water_flow.db) — histórico local
  → Dashboard futuro (Streamlit)
```

## Decisiones técnicas y rutas descartadas

**BLE directo desde Windows (`bleak`) — descartado, evidencia empírica.** Se logró conectar y mapear características GATT, pero ningún valor cambiaba al soplar el caudalímetro con el dispositivo conectado. Causa: Tuya encripta el protocolo sobre BLE (AES-CBC + `local_key`, generada y almacenada solo en sus servidores). Los UUIDs GATT estándar (`00002a00`, `00002b3a`) son del stack genérico de Bluetooth, no del sensor.

**`tuya-iot-sdk-python` (oficial) descartado** por estar orientado a integradores grandes, sin wizard de autodescubrimiento. **`tinytuya`** (comunidad, activo) resolvió con wizard automático de `device_id`/`local_key`.

**`python-tuya-ble` evaluado, descartado por ahora** — sin mantenimiento desde 2022, sin soporte documentado para medidores de agua (solo Fingerbots). Queda como posible Fase 3 (independencia de Tuya Cloud); `local_key` ya respaldado en `devices.json` por si se retoma.

**Emulador Android descartado** — los dos problemas reales durante vinculación (QR corrupto por Dark Reader del navegador, mismatch de data center SmartLife↔Tuya) vivían en capa navegador/backend Tuya, no en hardware/OS de SmartLife. Un emulador habría heredado el mismo QR corrupto y mismatch sin aportar diagnóstico nuevo.

## Datos técnicos del dispositivo

| Campo | Valor |
|---|---|
| Modelo | Restmo O-WM-2-BT |
| Conectividad | Bluetooth (≤70m), app Smart Life (Tuya) |
| Rango de flujo | 0.3–11 GPM (1–41.9 L/min) |
| Tolerancia | ±5% |
| Alimentación | 2x AAA alcalinas |
| Categoría Tuya | `slj` |
| Data Center | Western America (corregido desde Eastern America — cuentas SmartLife creadas antes de nov. 2025 se quedaron en el data center original aunque México migró a Eastern America) |

## Datapoints confirmados (`getdps`)

| Code Tuya | dp_id | Unidad | Significado |
|---|---|---|---|
| `flow_velocity` | 5 | 0.1 L/min | Flujo instantáneo |
| `water_once` | 2 | 0.1 L | Última consumición registrada |
| `water_use_data` | 1 | 0.1 L | Consumo acumulado — pendiente confirmar si es total histórico o periodo, se observó fijo en 0.0 durante pruebas |
| `voltage_current` | 4 | % | Nivel de batería (nombre engañoso, no es voltaje eléctrico) |

## Configuración del proyecto Tuya IoT

Proyecto `TME Caudalímetro` · Development Method: Smart Home · Data Center: Western America · Servicios: IoT Core + Smart Home Basic Service (trial gratuito renovable) · vinculación SmartLife vía QR (`Link App Account → Tuya App Account Authorization`). Credenciales y `local_key` respaldados localmente en `tinytuya.json`/`devices.json` — **no versionar en git** (ya en `.gitignore` del repo: `proyectos/P2/restmo-monitor/{tinytuya,devices,tuya-raw}.json`, `water_flow.db`).

## Estado del código

Script funcional: polling cada 5s vía Tuya Cloud API, persistencia SQLite, display de una sola línea in-place en terminal. Arquitectura pensada para extensión: `DP_MAP` (código Tuya → nombre/escala/unidad, agregar datapoint = una línea), capas puras (`fetch_reading` → `persist` → `display_live`, testeables independiente), `CONFIG` centralizado.

**Mejoras de diseño pendientes de implementar (orden sugerido):**
1. Notificaciones push vía Tuya Message Service (AMQP) en vez de polling — elimina latencia y consumo de cuota trial
2. Variables de entorno (`.env` + `python-dotenv`) en vez de hardcodeadas en `CONFIG`
3. `argparse` (`--interval`, `--device-id`, `--no-persist`)
4. `logging` en vez de `print`
5. Reintentos con backoff exponencial en `fetch_reading`
6. Modularizar (`config.py`, `tuya_client.py`, `storage.py`, `display.py`, `main.py`) cuando crezca

## Checklist logrado

- [x] Manual revisado — specs, datapoints, rangos
- [x] BLE directo descartado con prueba empírica de soplido en vivo
- [x] Cuenta Tuya IoT Developer + proyecto `TME Caudalímetro` configurado
- [x] SmartLife vinculada (Automatic Link vía QR)
- [x] Restmo vinculado, `devices.json` con `local_key` respaldado
- [x] Datapoints reales identificados y documentados
- [x] Script v1 (polling + SQLite) y v2 (5s, display in-place, arquitectura expandible)
- [x] Confirmado en vivo: flujo/batería/consumo se actualizan correctamente al abrir agua

## Pendientes

- [ ] Confirmar qué representa `water_use_data` exactamente (total histórico vs periodo)
- [ ] Dashboard visual (Streamlit) sobre datos ya en SQLite
- [ ] Exportación a CSV
- [ ] Implementar mejoras de diseño listadas arriba
- [ ] Decisión Fase 3 (independencia de Tuya Cloud vía `local_key` + BLE local) — opcional, prerequisito ya respaldado

## Notas operativas

- Repo local de trabajo: `C:\restmo-monitor` en laptop Windows TME — ver `project_restmo_monitor_dual_machine` (código vive en `mi-criterio`, sólo corre/testea en la laptop Windows).
- Plan Tuya Trial Edition tiene cuota mensual limitada; monitorear rate-limits si se baja de 5s de polling.
- Evidencia tipo `proyecto` (no laboral/declarativo) — candidato para `evidence_index.md` si se menciona en aplicaciones de trabajo relacionadas con IoT/Python/integración de APIs.
