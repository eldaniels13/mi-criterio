# AGENTS.md

Guidance for OpenCode sessions in `mi-criterio`. Pairs with `CLAUDE.md` (Claude Code). If this
file and other docs disagree, trust this file + git log + the disk over prose.

## What this repo is

A personal knowledge architecture, not a software project. No code, build, test, lint, or CI.
Work here = editing structured docs and git hygiene. Docs are authored in Spanish; preserve
existing style and language. "El historial de Git es el historial de pensamiento" — eldaniels
owns and controls the repo; suggest commits for meaningful updates, don't bulk-commit.

## Layout (3 layers)

1. `inbox/` — unclassified capture. Names: `DD-MM-YY_{handoff|captura}_tema-kebab.md`
   (templates in `inbox/_PLANTILLAS/`; files starting `_` are never processed).
2. `proyectos/P1–P8/` — canonical, per-lens criterion. One canonical doc per subproject,
   updated in place, **no dates in filenames**. `proyectos/P#/P#_*.txt` lenses are context
   to paste into conversations, not code.
3. Distilled, top-level: `perfil_maestro_eldaniels_v2.txt` (always-current master context),
   `proyectos_instrucciones_eldaniels_v2.txt`, `activacion_cruzada_eldaniels_final.txt`,
   `ToDo_global_eldaniels.md` (states: `[x]` done, `[~]` in progress, `[ ]` pending).

`_index.md` is a navigable map of the above, but **the disk is the source of truth**, not the
index. Update it whenever files move/are added.

## Core workflows

- **Ingesting a handoff/captura** → follow `.claude/commands/process-inbox.md` step by step.
  Invariants: reconcile disk vs `_index.md` first (orphans/ghosts via the `awk`+`comm`
  snippets there); prefer `FUSIONAR` (append) into the existing canonical doc over new files;
  ask before creating new folders or on ambiguous classification; propose commits, never run
  them; nothing in the repo is ever deleted (`DESCARTAR` must be justified).
- **Lossless distillation is machine-checked, not eyeballed**:
  `.claude/scripts/verificar_residuo.sh FUENTE DESTINO` (or `--lote DESTINO SRC...`).
  A file is only marked `archivado` when 🔴 `perdida == 0` (script exits 1 otherwise).
  Data-hard tokens (commands, paths, versions, hashes, measures) survive verbatim.
- **Writing a handoff** → `.claude/commands/handoff.md` + `inbox/_PLANTILLAS/handoff.md`.
  Verify every file path before writing it (past handoffs cited files that never existed or
  lived elsewhere). "Diseñado" ≠ "medido": never report something working that wasn't run.
  State honestly: half-done = 🟡, not ✅.

## Git conventions

- Work on `feature/N-*` branches; feature branches get merged into local `main`. `origin/main`
  (public, `git@github.com:eldaniels13/mi-criterio.git`) is pushed deliberately and currently
  lags local `main` by dozens of commits — do not assume local == remote.
- Commit style follows git log (not the older `update P3:` prose): lowercase conventional
  commits with a `P#`/resources scope, e.g. `docs(P2): ...`, `feat(P6): ...`,
  `inbox(add): DD-MM-YY_tema`, `refactor(P8): ...`, `chore: ...`.
- Pre-push gate: `.claude/scripts/auditar_pre_push.sh` (diffs vs `origin/main`; `--tree` scans
  everything). Exits: 0 clean, 1 decide, 2 hard credential block. It never prints matched
  content — only location + category; open the line yourself to decide.

## Privacy / sensitivity (this is a PUBLIC repo)

- Never commit or push credentials or real financial data. `.gitignore` already blocks the
  known set: `proyectos/P4/*.xlsx` (real finances), Tuya `local_key`/`devices.json`,
  `*_privado.txt`, `*_sensible.*`, `*.key`, `.webui_secret_key`, CV drafts. Anonymize as
  `[redactado]` / `Cuenta-1..N` / `~`.
- Do not push these gitignored local dirs either: `graphify-out/` (mirrors all repo content
  incl. personal data), `.agents/`, `.claude/skills/`, `skills-lock.json`,
  `.claude/settings.local.json`.

## Gotchas

- `CLAUDE.md`, `.claude/CLAUDE.md`, and `README.md` still reference `sesiones/` and
  `cronograma_intereses.md` — neither exists on disk (`sesiones/` was renamed to `inbox/`;
  the timeline doc was never created). `_index.md` reflects current reality.
- `perfil_maestro_eldaniels_v2.txt` updates are deliberate: during inbox processing, signal
  (don't edit) the sections it would touch.
- Core criterion in `proyectos/P#/*.txt` and the repo philosophy are eldaniels' living
  thought — don't rewrite/restructure them; appending new documented, verified experience is
  the normal operation (see `CONTRIBUTING.md` for what can change freely).
