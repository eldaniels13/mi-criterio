# LICENCIAS: Qué significa CC BY-NC-SA 4.0 y MIT

## Problema: ¿Por qué ponerle licencia a tu repo?

Sin licencia explícita, el código y contenido que creas tiene **copyright automático**. Eso significa que técnicamente nadie puede copiarlo, modificarlo, o reutilizarlo sin tu permiso explícito.

Pero TÚ quieres que la gente use tu pensamiento, lo critique, lo mejore, lo fork. Entonces pones una licencia que dice: "Está permitido ESTO, pero NO esto otro."

---

## CC BY-NC-SA 4.0 (para contenido/texto/ideas)

Tu perfil maestro, instrucciones, análisis son **contenido**, no código.

### ¿Qué significa cada parte?

**CC** = Creative Commons (organización que hace licencias justas)

**BY** = Atribución (crédito)
- Quien use tu trabajo DEBE mencionar que es tuyo
- Ejemplo: "Basado en arquitectura de eldaniels (github.com/eldaniels13/mi-criterio)"
- SIN esto violarían la licencia

**NC** = Non-Commercial (no comercial)
- La gente NO puede vender tu contenido
- Pueden estudiarlo, aprenderlo, modificarlo — SÍ
- Pueden venderlo como producto propio — NO
- **Razón:** es tu pensamiento, tus 477 conversaciones. Si alguien hace dinero de eso, deberías tener derecho.

**SA** = Share-Alike (compartir igual)
- Si alguien modifica tu trabajo, DEBE publicar los cambios bajo la MISMA licencia
- Evita que alguien tome tu idea, la "mejore", y luego la cierre bajo copyright propietario
- Es "viral" en el buen sentido — protege la libertad

**4.0** = Versión de la licencia (la más actual)

### Ejemplos prácticos

**SÍ puedo hacer:**
```
Como usuario, bajo CC BY-NC-SA 4.0:

✓ Copiar tu perfil maestro y adaptarlo para mí
  (siempre citando: "Basado en eldaniels")

✓ Crear una "versión mejorada" de tu P3 (energía)
  y publicarla en GitHub bajo CC BY-NC-SA 4.0

✓ Enseñar tus lentes cruzados en una clase gratis
  (mencionando que es idea de eldaniels)

✓ Traducir tu README a alemán y compartirlo
  (como CC BY-NC-SA 4.0, citando)
```

**NO puedo hacer:**
```
✗ Vender un ebook/curso con tu contenido
  (eso es comercial sin permiso)

✗ Publicar tu trabajo sin mencionar que viene de ti
  (eso viola el "BY")

✗ Tomar tu arquitectura P1-P8, mejorarlo, y publicar
  bajo MIT (código abierto) sin compartir crédito
  (eso viola "SA")

✗ Compilar tu repo en una "memoria colectiva de ingenieros"
  que vendo en Amazon (comercial + sin crédito = doble violación)
```

### Protección legal

Si alguien viola la licencia (ej: vende contenido tuyo):
- Técnicamente podrías demandar (aunque sería costoso)
- Más realista: GitHub te ayuda a reportar la violación
- CC BY-NC-SA es **socialmente vinculante** — la mayoría la respeta
- Es más sobre principios que sobre enforcement legal

---

## MIT (para código/scripts)

Cuando escribas código (nesting engine, scripts Python, etc.), usa MIT.

### ¿Qué significa?

MIT es extremadamente permisivo:

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...
```

**En español simple:**

- ✓ Copiar el código → SÍ
- ✓ Modificarlo → SÍ
- ✓ Venderlo → SÍ
- ✓ Incluirlo en otro proyecto → SÍ
- ✓ Hacer privado tu versión mejorada → SÍ
- Solo requisito: Incluir aviso de licencia + copyright (pequeño)

### Ejemplo MIT

Si tu nesting engine funciona en MIT:

```
Alguien puede:
✓ Tomar el código
✓ Mejorarlo
✓ Venderlo como plugin de AutoCAD
✓ No compartir los cambios de vuelta

Tu único requisito:
- En el archivo, debe decir: "Based on eldaniels' nesting engine (MIT)"
```

### ¿Por qué MIT para código y no CC?

CC BY-NC-SA es para contenido. MIT es para código porque:
- El código **necesita ser usado** en proyectos
- Ser muy restrictivo ahuyenta contribuciones
- MIT permite que mejoren el código libremente
- El código es software, no publicación intelectual

---

## Comparación visual: Los derechos que das

| Derecho | CC BY-NC-SA | MIT |
|---------|-------------|-----|
| Copiar | ✓ (con crédito) | ✓ |
| Modificar | ✓ (con crédito) | ✓ |
| Distribuir | ✓ (con crédito) | ✓ |
| Vender | ✗ | ✓ |
| Hacer privado | ✗ | ✓ |
| Cerrar bajo propietario | ✗ | ✓ |
| Requiere crédito | ✓ | ✓ (pequeño) |
| Si modificas, compartir igual | ✓ (SA) | ✗ |

---

## Para tu mi-criterio específicamente

```
mi-criterio/
├── perfil_maestro.txt           → CC BY-NC-SA 4.0
├── proyectos/P*.txt             → CC BY-NC-SA 4.0
├── activacion_cruzada.txt       → CC BY-NC-SA 4.0
├── TODO_unificado.txt           → CC BY-NC-SA 4.0
└── nesting_engine/              → MIT (cuando lo agregues)
    ├── engine.cs
    ├── LICENSE (MIT)
    └── README
```

### Cómo poner licencias en el repo

**Opción 1: Una sola licencia para todo (más simple)**

Archivo raíz: `LICENSE`

```
CONTENT LICENSE: CC BY-NC-SA 4.0
Applies to: *.txt, *.md, README, perfil_maestro, proyectos/, cronograma_intereses

CODE LICENSE: MIT
Applies to: *.cs, *.py, /nesting_engine, /scripts

Full text of CC BY-NC-SA 4.0:
https://creativecommons.org/licenses/by-nc-sa/4.0/

Full text of MIT:
https://opensource.org/licenses/MIT
```

**Opción 2: Licencias separadas (si algunos archivos son diferentes)**

```
mi-criterio/
├── LICENSE (CC BY-NC-SA 4.0 para contenido)
├── nesting_engine/
│   └── LICENSE (MIT para código)
```

**Opción 3: Indicador en cada archivo (lo más profesional)**

En README.md al final:

```markdown
## Licencia

**Contenido** (perfil maestro, P1-P8, TODO, criterio):
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**Código** (nesting engine, scripts, herramientas cuando existan):
[MIT](https://opensource.org/licenses/MIT)

---

### CC BY-NC-SA 4.0 Resumen

- Puedes usar, adaptar, y compartir
- Debes dar crédito
- NO puedes vender o monetizar
- Si adaptas, compartis bajo la misma licencia

### MIT Resumen

- Libre para usar, modificar, vender
- Solo requisito: mantener aviso de licencia
```

---

## Tu situación específica (sin licencia ahora)

**Hoy:** No tienes licencia formal

**Problema:** Alguien podría tomar tu perfil maestro y venderlo como ebook sin permiso

**Solución:** Agregando CC BY-NC-SA 4.0 le dices al mundo: "Está bien usarlo, pero siguiendo estas reglas"

**Cuándo hacerlo:** Cuando subas el repo a GitHub, agrega el `LICENSE` file.

---

## Preguntas para ti

1. **¿Te parece bien que alguien fork tu repo y lo mejore?**
   - SÍ → CC BY-NC-SA 4.0 es buena
   - NO → Podrías usar "All Rights Reserved" (cerrado)

2. **¿Escribirás código (nesting engine, scripts)?**
   - SÍ → MIT para código
   - NO → Solo CC BY-NC-SA 4.0 para contenido

3. **¿Quieres que tu trabajo sea usado en contextos académicos/no-lucrativos?**
   - SÍ → CC BY-NC-SA 4.0 es perfecta
   - NO → More restrictive license needed

4. **¿Te importa si alguien "mejora" tu perfil y vende cursos?**
   - NO (está bien el CC BY-NC-SA 4.0)
   - SÍ (cambiar a "All Rights Reserved")

---

## Respuesta honesta sobre CC BY-NC-SA

**Es licencia política.** Dice: "Mi pensamiento tiene valor. Puedes aprenderlo. Pero si lo monetizas, debo estar en la conversación."

Es perfecta para alguien como eldaniels que:
- Construye pensamiento público
- Quiere que sea útil
- NO quiere que otros lucren a costa suya sin permiso
- Cree en compartir conocimiento pero NO explotación

---

## Copiar esto en tu repo

Archivo: `mi-criterio/LICENSE`

```
CONTENT LICENSE
───────────────────────────────────────────────────────────

This work is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.

To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/

Applies to:
- perfil_maestro_eldaniels.txt
- proyectos/ (P1-P8 instruction files)
- cronograma_intereses.md
- All markdown and text documentation

Summary:
- Share and adapt for personal/educational use
- Must credit eldaniels
- Cannot be sold or commercialized
- If adapted, must share under same license


CODE LICENSE
───────────────────────────────────────────────────────────

When code is added to this repository (nesting engine, scripts, tools),
it will be licensed under MIT.

To view MIT license, visit https://opensource.org/licenses/MIT

Applies to:
- *.cs (C# code)
- *.py (Python scripts)
- nesting_engine/ directory
- Any executable/compilable code

Summary:
- Use, modify, sell freely
- Must include MIT license notice


RATIONALE
───────────────────────────────────────────────────────────

Content (architecture, thinking, frameworks) uses CC BY-NC-SA 4.0 because:
- It represents personal intellectual work
- It should be useful, but not exploited for profit without permission
- It reflects commitment to knowledge-sharing in sustainable development

Code uses MIT because:
- Code should be freely used in other projects
- It encourages contribution and improvement
- MIT is industry standard for open source
```

Done. Ahora vamos a lo importante: SECTOR OBJETIVO y empresas.
