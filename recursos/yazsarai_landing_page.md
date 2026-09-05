# YazSaraí — landing page (tracker de proyecto cliente)

> **Guía canónica:** `proyectos/P2/deployment_landing_pages.md` — el criterio técnico vive ahí. Este archivo es solo el estado del proyecto.
> **Sesión origen:** 31-08-26 (Gemini) · **Estado:** ✅ arquitectura diseñada — 🔴 bloqueado por inputs del cliente

---

## Estado real

| Componente | Estado |
|---|---|
| Arquitectura Git/Cloudflare Pages | ✅ diseñada (GitHub privado → Cloudflare Pages CI/CD) |
| Integración DNS / SSL | ✅ definida (CNAME/A + SSL automático en Edge) |
| Formulario | ✅ Web3Forms/Formspree seleccionado (serverless) |
| Estrategia de cotización | ✅ 5 pilares de valor definidos |
| Archivos fuente (`.zip` del cliente) | 🔴 pendientes de recibir |
| Acceso al registrador de dominio | 🔴 pendiente (GoDaddy/Hostinger/Namecheap) |

## Siguientes pasos

1. [ ] Enviar plantilla de comunicación al cliente: solicitar `.zip`, accesos al dominio y correo para el formulario.
2. [ ] Crear repositorio privado en GitHub e importar la carpeta descomprimida.
3. [ ] Conectar Cloudflare Pages con GitHub y desplegar versión de prueba (`.pages.dev`).
4. [ ] Configurar registros CNAME/A en el registrador y validar SSL (HTTPS).
5. [ ] Decidir método DNS: CNAME vs Nameservers (según el acceso que otorgue el cliente).

## Reglas de la sesión

- Repo GitHub siempre **Privado** (propiedad del cliente).
- `index.html` estricto en raíz; rutas relativas (`./img/`); validar en `.pages.dev` antes del dominio final (riesgo: rutas absolutas `C:/Users/...` en el HTML entregado).
- Cotizar por infraestructura/seguridad, no por horas de subida.

## Trigger de retoma

> Cuando eldaniels diga **"retomar"**, **"hagamos pendientes"**, **"qué urge?"**, **"qué hacemos hoy?"**, **"qué procede?"**, **"what should we tackle next"** o frases equivalentes → sugerir esta sesión como pendiente.

## Escalado

Si el proyecto crece (mantenimiento continuo, más páginas, CMS) → crear repositorio propio en `~/Codes/` y mover el código ahí. Este tracker sigue en el repo como registro del criterio.
