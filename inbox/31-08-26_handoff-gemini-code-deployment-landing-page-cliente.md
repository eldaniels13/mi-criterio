31-08-26 — Deployment de Landing Page Estática y Estructuración de Cotización

**Fecha de corte:** 2026-08-31 · **Herramienta:** Gemini
**Lente(s):** P1 principal × P2, P3 secundarios
**Estado global:** ✅ completado

---

## 1 · Objetivo y motivación

**Objetivo:** Diseñar la arquitectura de despliegue profesional, limpia y sin costos recurrentes para una landing page estática (HTML/CSS/JS/imágenes) con dominio propio, y definir una estrategia de cotización ejecutable para el cliente.

**Motivación — por qué, no sólo qué:** Faltan conocimientos específicos de infraestructura web e integración de dominios. Se requiere un flujo libre de errores que evite costos innecesarios para el cliente, garantice HTTPS/DDoS por defecto y justifique el cobro por valor técnico y estabilidad en lugar de horas de programación.

| Driver | Detalle |
| --- | --- |
| Autonomía de Deployment | Capacidad de desplegar sitios estáticos mediante CI/CD sin gestionar servidores ni backend |
| Valor Percibido y Justificación | Formular una cotización sólida basada en seguridad, CDN global y cero mantenimiento |
| Privacidad del Cliente | Proteger el código fuente manteniendo repositorios privados en GitHub sin exponerlos públicamente |

---

## 2 · Estado real verificado al cerrar

| Componente | Estado | Verificado cómo |
| --- | --- | --- |
| Arquitectura Git/Cloudflare | ✅ | Diseñada la canalización local $\rightarrow$ GitHub (Repo Privado) $\rightarrow$ Cloudflare Pages (CI/CD) |
| Integración DNS / SSL | ✅ | Definida la delegación vía registros CNAME/A y certificado SSL automático en Edge |
| Integración de Formulario | ✅ | Seleccionada integración serverless mediante Web3Forms / Formspree directo en HTML |
| Estrategia de Cotización | ✅ | Desglosados los 5 pilares de valor técnico para justificar la propuesta comercial |

**Lo que NO quedó resuelto:**

* Recibir los archivos `.zip` finales del cliente para auditar la estructura interna de rutas y el archivo `index.html`.
* Acceso al registrador de dominio (GoDaddy, Hostinger, Namecheap, etc.) para ejecutar los cambios de DNS.

---

## 3 · Archivos tocados — con ruta verificada

| Ruta | Acción | Qué cambió y por qué |
| --- | --- | --- |
| `docs/handoffs/31-08-26_handoff_deployment-landing.md` | creado | Documento canónico de traspaso de sesión y guía de ejecución |

**Cambios fuera del repo:**

* Ninguno en esta sesión (pendiente creación de repositorio privado en GitHub y proyecto en Cloudflare Pages).

---

## 4 · Evaluado y descartado

| Opción / intento | Veredicto | Razón |
| --- | --- | --- |
| Cloudflare Pages + GitHub Privado | ✅ adoptado | Infraestructura global, gratis, SSL automático, CI/CD nativo y protección contra ataques |
| Hosting Tradicional cPanel / FTP | ❌ descartado | Lento, requiere mantenimiento manual, cobros mensuales recurrentes e infraestructura frágil |
| Repositorio Público en GitHub | ❌ descartado | Expone el código del cliente a terceros de forma innecesaria |
| Servidor / Backend propio para Formularios | ❌ descartado | Complejidad innecesaria; servicios tipo Web3Forms resuelven la recepción de correo sin costo ni código |

**Suposiciones que resultaron falsas:**

* *Pensar que los formularios HTML envían correos por sí solos:* Un formulario estático requiere un endpoint receptor (Web3Forms/Formspree) para procesar el envío sin backend propio.

---

## 5 · Decisiones tomadas

* [x] Usar Cloudflare Pages vinculado a GitHub Privado — *porque* ofrece máxima velocidad global (CDN), certificado SSL gratuito y cero costos de servidor para el cliente.
* [x] Utilizar Web3Forms o Formspree — *porque* evita la programación de un backend para procesar datos de contacto.
* [x] Cotizar por valor de infraestructura y configuración — *porque* el valor del trabajo reside en la estabilidad, seguridad y puesta en marcha técnica, no en el tiempo de subida de archivos.
* [ ] Selección del método de DNS (CNAME vs Nameservers) — falta definir si el cliente otorga acceso total al panel del dominio o prefiere cambiar registros puntuales.

**Punto ciego `[!]**`: Asumir que las rutas internas del HTML entregado por el cliente están bien escritas (relativas) antes de probar el despliegue.

---

## 6 · Siguientes pasos

1. [ ] Enviar la plantilla de comunicación al cliente solicitando el archivo `.zip`, accesos al dominio y correo para formulario.
2. [ ] Crear repositorio privado en GitHub e importar la carpeta descomprimida.
3. [ ] Conectar Cloudflare Pages con GitHub y desplegar la versión de prueba (`.pages.dev`).
4. [ ] Configurar registros CNAME/A en el registrador de dominios y validar certificado SSL (HTTPS).

**Bloqueadores:** Recepción de los archivos fuente y accesos al registrador de dominio por parte del cliente.

**Riesgo mayor:** Rutas absolutas rotas dentro del código HTML/CSS entregado (ej. `src="C:/Users/..."`), lo que rompería imágenes y estilos al subir a producción. Probar visualmente en el subdominio temporal de Cloudflare antes de mapear el dominio final.

---

## 7 · Regla de oro para quien retome esto

1. Mantén siempre el repositorio de GitHub en modo **Privado** para proteger la propiedad del cliente.
2. Valida que el archivo raíz se llame estrictamente `index.html` y que las rutas a imágenes/CSS sean relativas (`./img/`).
3. Si la página lleva formulario, agrega el atributo `action` de Web3Forms antes de entregar.
4. No cobres por "horas de subida"; cobra por la infraestructura segura, HTTPS y cero costo mensual de hosting.

---

## 8 · Datos duros a preservar

```markdown
# Flujo de Integración
Git Repo (Privado) -> Cloudflare Pages -> DNS CNAME -> SSL Auto -> Web3Forms

# Estructura de la propuesta comercial (Desglose de conceptos)
1. Aprovisionamiento e infraestructura en CDN Global de alta velocidad (Cloudflare Pages).
2. Encriptación de datos y Certificado de Seguridad SSL/HTTPS.
3. Enrutamiento y Mapeo de Registros DNS con Dominio Personalizado.
4. Integración y canalización de Formulario de Contacto a correo electrónico.
5. Control de Calidad (QA), optimización de carga y pruebas de responsividad móvil.

```

---

## 9 · Destino sugerido

**Doc canónico:** `proyectos/P1/deployment_landing_pages.md` — fusionar como guía estándar de deployments estáticos.

**Actualiza `perfil_maestro`:** sí — agregar Cloudflare Pages y GitHub CI/CD a la pila de herramientas dominadas.

**Código a extraer:** No aplica en esta sesión.