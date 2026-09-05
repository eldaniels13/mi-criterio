# Deployment de landing pages estáticas — guía canónica

> **Propósito:** flujo estándar, profesional y sin costos recurrentes para desplegar una landing page estática (HTML/CSS/JS/imágenes) con dominio propio. Nace de la sesión 31-08-26 (Gemini) para el proyecto cliente YazSaraí; se generaliza como criterio P2.
> **Lens:** P2 (programación/infraestructura web)
> **Tracker del proyecto cliente:** `recursos/yazsarai_landing_page.md` (estado, blockers, next steps)

---

## 1 · Arquitectura adoptada

```
Git local → GitHub (repositorio PRIVADO) → Cloudflare Pages (CI/CD)
  → DNS (CNAME/A en el registrador del cliente) → SSL automático (Edge)
  → Formulario: Web3Forms / Formspree (serverless, sin backend propio)
```

- **Cloudflare Pages + GitHub privado:** infraestructura global (CDN), certificado SSL gratuito, CI/CD nativo, protección DDoS, cero costos de servidor.
- **Web3Forms / Formspree:** un formulario HTML estático requiere un endpoint receptor — el formulario no envía correos por sí solo. Estos servicios lo resuelven sin costo y sin código.

## 2 · Decisión técnica — qué se descartó y por qué

| Opción | Veredicto | Razón |
|---|---|---|
| Cloudflare Pages + GitHub Privado | ✅ adoptado | CDN global, SSL automático, CI/CD nativo, gratis |
| Hosting tradicional cPanel / FTP | ❌ descartado | Lento, mantenimiento manual, cobros mensuales recurrentes |
| Repositorio Público en GitHub | ❌ descartado | Expone el código del cliente a terceros |
| Servidor/backend propio para formularios | ❌ descartado | Complejidad innecesaria; Web3Forms/Formspree lo resuelven |

**Suposición que resultó falsa:** *"los formularios HTML envían correos por sí solos"* — requieren endpoint receptor (`action` de Web3Forms/Formspree).

## 3 · Riesgo mayor identificado

**Rutas absolutas rotas dentro del HTML entregado por el cliente** (ej. `src="C:/Users/..."`), que rompen imágenes y estilos en producción. Mitigación: probar visualmente en el subdominio temporal `.pages.dev` **antes** de mapear el dominio final.

## 4 · Regla de oro

1. Repositorio GitHub siempre **Privado** — protege la propiedad del cliente.
2. Archivo raíz estrictamente `index.html`; rutas a imágenes/CSS **relativas** (`./img/`).
3. Si hay formulario: agregar el atributo `action` (Web3Forms/Formspree) antes de entregar.
4. **No cobrar por "horas de subida"** — cobrar por infraestructura segura, HTTPS y cero costo mensual de hosting.

## 5 · Estrategia de cotización — los 5 pilares de valor

1. Aprovisionamiento e infraestructura en CDN Global de alta velocidad (Cloudflare Pages).
2. Encriptación de datos y Certificado de Seguridad SSL/HTTPS.
3. Enrutamiento y Mapeo de Registros DNS con Dominio Personalizado.
4. Integración y canalización de Formulario de Contacto a correo electrónico.
5. Control de Calidad (QA), optimización de carga y pruebas de responsividad móvil.

## 6 · Flujo de ejecución estándar

1. Recibir `.zip` del cliente + accesos al registrador de dominio + correo receptor del formulario.
2. Auditar estructura interna: `index.html` en raíz, rutas relativas.
3. Crear repositorio privado en GitHub e importar la carpeta descomprimida.
4. Conectar Cloudflare Pages con GitHub → desplegar versión de prueba (`.pages.dev`).
5. Configurar registros CNAME/A en el registrador → validar certificado SSL (HTTPS).
6. Decisión de método DNS: **CNAME** (si el cliente cambia registros puntuales) vs **Nameservers** (si otorga acceso total al panel del dominio) — resolver según el acceso que dé el cliente.

## 7 · Bloqueadores típicos

- Recepción de los archivos fuente del cliente.
- Acceso al registrador de dominio (GoDaddy, Hostinger, Namecheap, etc.).
