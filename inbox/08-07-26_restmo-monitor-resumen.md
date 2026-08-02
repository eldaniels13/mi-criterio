# Monitor Restmo O-WM-2-BT vía Tuya Cloud API

## Objetivo

Visualizar en tiempo real las mediciones del medidor de flujo de agua **Restmo O-WM-2-BT** (Bluetooth, ecosistema Tuya/SmartLife) desde una laptop Windows, sin depender de la app móvil. Con visión a futuro de almacenamiento histórico, gráficos y exportación de datos. Preferencia por soluciones OS-neutrales cuando sea posible.

---

## Arquitectura final

```
Restmo O-WM-2-BT
      │ BLE (encriptado, propietario)
      ▼
Celular con SmartLife (A12 de Daniel)
      │ Internet
      ▼
Tuya Cloud (servidores de Tuya, Western America Data Center)
      │ HTTPS API
      ▼
Laptop Windows — Python + tinytuya
      │
      ▼
SQLite (water_flow.db) — histórico local
      │
      ▼
Dashboard futuro (Streamlit / gráficos)
```

---

## Decisiones técnicas clave

### Ruta descartada: BLE directo desde Windows

Se intentó conectar directamente por Bluetooth Low Energy desde Windows usando `bleak`, sin pasar por Tuya Cloud.

**Conclusión: descartado, con evidencia empírica.** El Restmo transmite su MAC de forma rotativa (privacidad BLE), nunca se anuncia con nombre reconocible, y aunque se logró conectar y mapear sus características GATT, **ningún valor cambiaba al soplar por el caudalímetro con el dispositivo conectado**. Causa raíz: Tuya encripta el protocolo de datos sobre BLE (AES-CBC + `local_key`, generada y almacenada solo en sus servidores). Los UUIDs estándar leíbles (`00002a00`, `00002b3a`, etc.) pertenecen al stack genérico de Bluetooth, no al sensor.

### Ruta elegida: Tuya Cloud API vía `tinytuya`

Se descartó `tuya-iot-sdk-python` (oficial) por estar orientado a integradores grandes, sin wizard de autodescubrimiento y con documentación pensada para "Industry Projects". `tinytuya` (comunidad, activo) resolvió el problema con su wizard automático de descubrimiento de `device_id` y `local_key`.

Se investigó también `python-tuya-ble` como alternativa para evitar dependencia continua del cloud (leer BLE localmente usando la `local_key` extraída una sola vez). **Descartado por ahora**: proyecto sin mantenimiento desde 2022, sin soporte documentado para medidores de agua (solo Fingerbots). Queda como posible Fase 3 futura — el `local_key` ya está respaldado en `devices.json` por si se retoma.

### Por qué NO se usó un emulador Android

Los dos problemas reales durante la vinculación (QR corrupto por la extensión Dark Reader del navegador, y mismatch de data center entre cuenta SmartLife y proyecto Tuya) vivían en la capa del navegador de la laptop y en la configuración del backend de Tuya — ninguno de los dos dependía del hardware/OS que ejecuta SmartLife. Un emulador habría heredado el mismo QR corrupto y el mismo mismatch de servidor, sumando solo complejidad de setup (Play Services no certificados, nueva sesión de login) sin aportar información diagnóstica nueva.

---

## Datos técnicos del dispositivo

| Campo | Valor |
|---|---|
| Modelo | Restmo O-WM-2-BT |
| Conectividad | Bluetooth (≤70m), app Smart Life (Tuya) |
| Rango de flujo | 0.3–11 GPM (1–41.9 L/min) |
| Tolerancia de medición | ±5% |
| Alimentación | 2x pilas AAA alcalinas |
| Device ID (Tuya) | `[device_id redactado]` |
| Categoría Tuya | `slj` |
| Data Center | Western America |

---

## Datapoints confirmados (vía `getdps`)

| Code Tuya | dp_id | Unidad | Significado |
|---|---|---|---|
| `flow_velocity` | 5 | 0.1 L/min | Flujo instantáneo |
| `water_once` | 2 | 0.1 L | Última consumición registrada |
| `water_use_data` | 1 | 0.1 L | Consumo acumulado (pendiente confirmar si es total histórico o periodo — se observó fijo en 0.0 durante las pruebas) |
| `voltage_current` | 4 | % | Nivel de batería (el nombre es engañoso, no es voltaje eléctrico) |

---

## Configuración del proyecto Tuya IoT

- Proyecto: `TME Caudalímetro`
- Development Method: Smart Home
- Data Center: Western America (corregido desde Eastern America tras detectar el mismatch — cuentas SmartLife creadas antes de nov. 2025 se quedaron en el data center original aunque México migró a Eastern America)
- Servicios activos: IoT Core, Smart Home Basic Service (ambos "In service", trial gratuito renovable)
- Vinculación de cuenta: SmartLife linkeada vía QR (Automatic Link) bajo `Link App Account → Tuya App Account Authorization`
- Credenciales (Client ID / Secret) y `local_key` del dispositivo respaldadas localmente en `tinytuya.json` / `devices.json` — **no versionar estos archivos en git**

---

## Estado del código

Script funcional actual: polling cada 5s vía Tuya Cloud API, persistencia en SQLite, display de una sola línea actualizándose en terminal (`\r` + padding).

Arquitectura del script pensada para extensión futura:
- `DP_MAP`: diccionario central que mapea código Tuya → nombre amigable, escala y unidad. Agregar un datapoint nuevo es una sola línea.
- Separación en capas puras: `fetch_reading` (cliente Tuya) → `persist` (SQLite) → `display_live` (terminal), cada una testeable/reemplazable de forma independiente.
- `CONFIG` centralizado arriba del archivo — único lugar a tocar para credenciales y parámetros.

Ideas de diseño pendientes de implementar, en orden de prioridad sugerido:
1. Notificaciones push vía Tuya Message Service (AMQP) en vez de polling — elimina latencia y consumo de cuota del trial
2. Variables de entorno (`.env` + `python-dotenv`) para credenciales, en vez de hardcodeadas en `CONFIG`
3. `argparse` para correr con flags (`--interval`, `--device-id`, `--no-persist`)
4. `logging` module en vez de `print` puro
5. Reintentos con backoff exponencial en `fetch_reading`
6. Separar en módulos (`config.py`, `tuya_client.py`, `storage.py`, `display.py`, `main.py`) cuando el proyecto crezca

---

## Checklist — lo que hemos logrado hasta ahora

- [x] Manual del Restmo revisado — specs, datapoints físicos, rangos de operación
- [x] Descarte definitivo de BLE directo (protocolo encriptado por Tuya, confirmado empíricamente con prueba de soplido en vivo)
- [x] Cuenta Tuya IoT Developer creada, proyecto `TME Caudalímetro` configurado
- [x] Cuenta SmartLife vinculada al proyecto (Automatic Link vía QR)
- [x] Restmo vinculado al proyecto → `Device ID: [device_id redactado]`
- [x] Wizard de tinytuya completado → `devices.json` con `local_key` respaldado
- [x] Datapoints reales identificados y documentados
- [x] Script v1 funcional: polling + guardado en SQLite
- [x] Confirmado en vivo: el flujo sube al abrir agua, batería y consumo se actualizan correctamente
- [x] Script v2: polling más frecuente (5s), display en una sola línea in-place, arquitectura expandible (`DP_MAP`, capas separadas)

## Pendientes

- [ ] Confirmar qué representa exactamente `water_use_data` (¿total histórico o periodo? — se quedó fijo en 0.0 durante todas las pruebas realizadas)
- [ ] Dashboard visual (Streamlit u otro) sobre los datos ya almacenados en SQLite
- [ ] Exportación a CSV
- [ ] Implementar mejoras de diseño listadas arriba (Message Service, `.env`, `argparse`, `logging`, reintentos, modularización)
- [ ] Decisión sobre Fase 3 (independencia de Tuya Cloud vía `local_key` + BLE local) — opcional, no urgente, prerequisito ya respaldado

---

## Notas para futuros desarrolladores (incluido Claude Code)

- El repo local de trabajo es `C:\restmo-monitor` en la laptop Windows del usuario — al migrar a Claude Code, replicar estructura o indicar nueva ruta.
- **No subir `tinytuya.json` ni `devices.json` a git** — contienen credenciales y `local_key`. Agregar a `.gitignore`.
- El proyecto Tuya usa el plan Trial Edition — tiene cuota limitada mensual; si se aumenta la frecuencia de polling por debajo de 5s, monitorear rate-limits.
- La categoría Tuya del dispositivo es `slj` — útil para futuras consultas a la API de Tuya sobre funciones soportadas por categoría.
- Referencia cruzada con el proyecto `mi-criterio`: este desarrollo es evidencia tipo `proyecto` (no `laboral` ni `declarativo`) — útil para `evidence_index.md` si se menciona en futuras aplicaciones de trabajo relacionadas con IoT, Python, o integración de APIs.
