# Plan de Estudio Secuencial de Python 2025

**Documento operativo** para un proyecto de **ChatGPT-5** como programa completo de aprendizaje de Python

---

## 0) Propósito y alcance

Este documento define un **itinerario guiado por ChatGPT-5** para llevar a un estudiante desde **fundamentos** hasta **nivel profesional**, con dos especializaciones opcionales: **Web/Backend & DevOps** o **Escritorio + Base de Datos**. El plan integra varias fuentes de video analizadas previamente (playlist “desde cero”, colección de 5 videos orientados a web/DevOps y serie de 4 videos con fundamentos/POO/GUI/MySQL), sin depender de ninguna en exclusiva.

---

## 1) Resultado esperado (perfil de egreso)

Al finalizar, el estudiante será capaz de:

1. **Programar en Python con soltura**, aplicando buenas prácticas (PEP8, tipado básico, manejo de excepciones, documentación).
2. **Estructurar proyectos** en paquetes, escribir **tests** con `pytest` y usar **entornos virtuales**.
3. Emplear **decoradores**, **generadores** y **concurrencia** (async/hilos/procesos) cuando corresponda.
4. Elegir y completar **una especialización**:
   - **Web/Backend & DevOps:** FastAPI, auth (OAuth2/JWT), DB relacional/NoSQL, Docker, CI/CD.
   - **Escritorio + BD:** Tkinter/CustomTkinter o PyQt5, CRUD con DB, empaquetado de app.
5. (Opcional) **Datos/IA**: NumPy/Pandas/Polars, visualización, scikit-learn, bases de ML.

---

## 2) Modo de uso con ChatGPT-5

### 2.1 Prompt inicial (copiar/pegar)

> Actúa como **mentor de Python**. Sigue el _Plan de Estudio Secuencial de Python 2025_. Para cada sesión, dame:
>
> 1. breve repaso teórico, 2) 3 ejercicios graduados con _auto-chequeo_ (tests), 3) un mini-proyecto, 4) retroalimentación sobre mi solución (pídeme el código), 5) un _quiz_ de 5 preguntas. Mantén registro de progreso por bloque.

### 2.2 Bucle diario sugerido (45–90 min)

1. 10–15’ teoría guiada + lectura corta.
2. 20–40’ ejercicios (con pruebas).
3. 15–30’ mini-proyecto / refactor.
4. 5–10’ quiz + _retrospectiva_: ¿qué aprendí?, ¿qué me costó?

### 2.3 Criterios de avance

No avanzar de bloque hasta: **dominar** la lista de competencias del bloque, entregar **deliverables** mínimos (ver §6) y aprobar **quiz** (≥80%) + **tests**.

---

## 3) Rutas de contenido (selección flexible)

Consulta el índice de videos y playlists en **resources/videos.md**.  
En el calendario semanal se señalan “Videos base” por semana con referencias a ese índice.

---

## 4) Plan secuencial por bloques

### Bloque 0 — Preparación (1 semana)

**Objetivos:** Instalar Python 3.10+ (ideal 3.12), VS Code, Git; usar `venv`/`pip`. Conocer PEP8 y atajos.  
**Salida:** repo `python-boot` con `hello.py`, `requirements.txt` y guía de entorno.  
**Instrucción a ChatGPT-5:**

> Revísame instalación, crea checklist de entorno, proponme 3 ejercicios de warming-up y verifica mi `requirements.txt`. Pídeme capturas de `python --version` y `pip list`.

### Bloque 1 — Fundamentos (4–6 semanas)

**Temas:** sintaxis, variables, tipos, `str` y métodos, listas/tuplas/sets/dicts, operadores, `if/elif/else`, bucles, `break/continue/else`, funciones (`*args/**kwargs`), módulos básicos, `match/case`, f-strings.  
**Recursos base:** Serie 4 (Video 1/4) **o** Playlist **o** Curso largo (secc. #1–#45 aprox.).  
**Mini-proyectos:** calculadora CLI, agenda (JSON), juego de adivinanzas/quiz.  
**Criterio de salida:** 8–12 katas resueltas sin consultar; diferencias de estructuras claras; scripts limpios.  
**Instrucción a ChatGPT-5:**

> Dame 10 katas (con _tests_), 2 mini-proyectos con rúbrica y evalúa mis soluciones con refactor PEP8.

### Bloque 2 — Intermedio (6–8 semanas)

**Temas:** POO (clases, `__init__`, herencia, encapsulamiento, polimorfismo, abstracción), archivos (TXT/CSV/JSON), excepciones, `datetime`, comprehensions, lambdas, HOF, **regex (`re`)**, **paquetes/namespaces**, **venv/pip**, documentación, depuración.  
**Recursos:** Serie 4 (Video 2/4) + refuerzos (colección web para regex/comprehensions/paquetes).  
**Mini-proyectos:** CLI “tareas” (JSON/CSV), conversor de zonas horarias, parser de logs (regex).  
**Criterio de salida:** POO funcional; empaquetar módulos; manejo robusto de errores; docstrings.  
**Instrucción a ChatGPT-5:**

> Pídeme un proyecto CLI con CRUD y logs. Exige `--help`, `--version`, manejo de errores y `README`. Genera _tests_ `pytest`.

### Bloque 3 — Avanzado (8–10 semanas)

**Temas:** **decoradores** (con parámetros, `*args/**kwargs`), **generadores/iteradores**, introspección, `dataclasses`, **typing** moderno, **concurrencia** (`asyncio`, `threading`, `multiprocessing`), **profiling** (`cProfile`), caching (`functools.lru_cache`), patrones.  
**Recursos:** Serie 4 (Video 2/4) para decoradores/generadores; práctica adicional de `asyncio` y `multiprocessing`.  
**Mini-proyectos:**

- Librería “**toolbox**” con `@timed`, `@retry`, `@memoize`.
- Generador `read_chunks(path, n)` (tests).
- Crawler `asyncio` (descargas concurrentes, _retries_).  
  **Criterio de salida:** escribes decoradores completos; comparas async vs hilos/procesos; haces profiling/caching.  
  **Instrucción a ChatGPT-5:**
  > Propón 3 ejercicios de decoradores (incluye con parámetros), 2 de generadores y un reto `asyncio` (timeout, retry, semáforos). Evalúa complejidad y profiling.

### (Opcional) Bloque 4 — Datos / IA (10–16 semanas)

**Temas:** NumPy 2, Pandas 2/3, **Polars**, Matplotlib/Plotly, scikit-learn, PyTorch 2; si escala: Dask/PySpark.  
**Proyecto:** EDA + 2 modelos con validación y tablero Plotly.  
**Criterio de salida:** pipeline reproducible (notebooks + scripts + reporte).  
**Instrucción a ChatGPT-5:**

> Define un dataset público y diseña EDA→features→modelo. Exige `requirements.txt`, `Makefile` simple y reporte.

### Bloque 5 — Profesionalización (elige una rama; 12–16 semanas)

#### Rama A — Web/Backend & DevOps

**Temas:** FastAPI, routers, validación, **OAuth2/JWT**, CORS, ORMs (SQLAlchemy + Alembic), **Docker**, **CI/CD (GitHub Actions)**, logging/metrics, **async** end-to-end, Postgres/Mongo, realtime.  
**Proyecto integrador:** API REST con auth, DB y tests (pytest + httpx), Docker Compose (app + DB), pipeline CI/CD (lint+tests+deploy).  
**Criterio de salida:** _commit_ a `main` dispara pipeline y deja el despliegue operativo.  
**Instrucción a ChatGPT-5:**

> Genera OpenAPI, esquema SQLAlchemy y migraciones. Exige tests de integración, `docker-compose.yml` y workflow de Actions. Pide observabilidad (logs y tiempos).

#### Rama B — Escritorio + Base de Datos

**Temas:** Tkinter/**CustomTkinter** o PyQt5, arquitectura GUI (MVC/MVP), hilos o `concurrent.futures`, SQLite/MySQL, empaquetado (PyInstaller/Briefcase), seguridad de credenciales.  
**Proyecto integrador:** **Gestor de inventario** GUI (CRUD + filtros + exportación), DB (SQLite/MySQL), barra de progreso y tareas en hilo, empaquetado `.exe/.app`.  
**Criterio de salida:** binario instalable, DB migrable, UI fluida.  
**Instrucción a ChatGPT-5:**

> Exige arquitectura por módulos, _thread-safe_ para tareas largas (cola o `after()`), pruebas de lógica, empaquetado con PyInstaller y manual de usuario.

---

## 5) Plantilla semanal (instanciable por ChatGPT-5)

**Semana X — [Bloque, Tema]**

- **Objetivo**: …
- **Video(s) base**: …
- **Lectura/Apunte**: …
- **Ejercicios**: 3 katas con tests (ChatGPT-5 genera).
- **Mini-proyecto**: … (criterios de aceptación).
- **Quiz (5 preguntas)**: …
- **Retro**: 3 mejoras + foco siguiente semana.

---

## 6) Entregables y rúbricas

| Bloque | Deliverables                                            | Rúbrica (resumen)                                                                    |
| ------ | ------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| B0     | Repo con `hello.py`, `requirements.txt`, `venv`         | Entorno reproducible (✔), README claro (✔)                                           |
| B1     | 2 mini-proyectos CLI + 10 katas                         | Correctitud (40), estilo PEP8 (30), diseño simple (30)                               |
| B2     | Proyecto CLI empaquetado + errores + docstrings + tests | Correctitud (35), robustez (30), modularidad (20), docs (15)                         |
| B3     | Librería “toolbox” + crawler `asyncio` + profiling      | Correctitud (30), performance (25), API clara (25), pruebas (20)                     |
| B5A    | API FastAPI + DB + Docker + CI/CD                       | Tests (30), despliegue reproducible (30), seguridad básica (20), observabilidad (20) |
| B5B    | App GUI + DB + empaquetado                              | UX fluida (25), robustez (25), empaquetado (25), pruebas+docs (25)                   |

---

## 7) Buenas prácticas

- **Black** y **Ruff** desde Semana 1.
- **Docstrings** (Google/Numpy) y `typing` básico.
- **Git**: ramas por feature y PR con checklist.
- **.env** para configuración; sin credenciales en repo.
- **pytest**: cobertura mínima 70% (B3+) y 80% (B5).

---

## 8) Personalización por objetivo

**Generalista:** Serie 4 (V1/4, V2/4) + tramos de curso largo (decoradores).  
**Web/Backend:** Tras B3, rota a Colección 5 (FastAPI, Docker, CI/CD, DB).  
**Escritorio + BD:** Tras B2, inicia GUI (Tkinter o PyQt5) y DB.  
**Datos/IA:** Inserta B4 tras B2/B3.

---

## 9) Checklist de progreso (para README del repo)

- [ ] B0 completo
- [ ] B1: 10 katas + 2 mini-proyectos
- [ ] B2: CLI empaquetado + tests + docstrings
- [ ] B3: decoradores/generadores + crawler async + profiling
- [ ] B5A **o** B5B: proyecto integrador
- [ ] (Opcional) B4: EDA + modelos + dashboard

---

## 10) Cierre y siguientes pasos

- Portafolio con 3 piezas: 1) Capstone, 2) Librería “toolbox”, 3) Demo de la otra rama.
- Solicitar **code review** final y un **plan de mejora a 90 días** (temas a profundizar, deudas técnicas, nuevas features).

# touch
