# go-apps.spec — the family specification

Version 1.2 — 2026-07-20.
This file is the single source of truth for the rules of the go-apps family.
Every repo's AGENTS.md (and CLAUDE.md, which imports it) directs here. When a
working session produces a new rule or learning, it lands in this file — or,
for UI/UX patterns with assets, in the go-design repo, which this spec
delegates to. History and the "why" of decisions live outside the repos (the
maintainer's notes); this file records only the current normative state.

## 1. The family

- Hub: `go-apps` (this repo, no code). Apps: `go-calc`, `go-notepad`,
  `go-passwords` (encrypted `.gpw` vault, GUI + `go-pw-cli`). More planned:
  file explorer, CLI.
- Libraries: `go-apiserver` (embedded REST control plane), `go-updates`
  (self-update mechanics), `go-installer` (macOS DMG + Windows two-exe
  install model: the release ships a portable exe and a `-setup.exe` that is
  the same binary, keyed by file name via `RunningAsSetup`).
- Design: `go-design` — the style guide (icon rules, tokens, tiles, UI
  patterns, vendored SVGs). READ IT BEFORE TOUCHING ANY APP UI. Apps consume
  it by copy, never by link; its `main` is the truth.
- One repo per project, one local checkout per repo, side by side in the
  same parent directory (sibling paths like `../go-design` resolve).
- Commits: conventional commits, English, straight to main. Releases via
  annotated semver tags (`vX.Y.Z`) — the tag push triggers the release CI.
- **Language: everything in the repos is English** — code, comments, tests,
  docs, UI strings, commit messages. The maintainer's working notes and
  decision journal are kept in Portuguese OUTSIDE GitHub; nothing in
  Portuguese lands in a repo.

## 2. Architecture (every app)

- Stack: Go + Wails v2 + Vue 3/TypeScript. Business logic in
  `internal/<domain>` — pure Go, testable, no Wails imports. `app.go` is a
  thin adapter. The frontend only renders; rules live in Go.
- Look: frameless window, custom title bar, dark/light themes, English UI,
  Fluent/Win11 style. App icon: Lucide glyph, white stroke on the family's
  graphite rounded tile (sources in go-design `tiles/`, rendered with
  `tools/mktile`).
- REST control plane (the `go-apiserver` library): X-API-Key + CIDR
  allowlist, structured errors `{"error":{code,message,status}}` with
  stable codes. OFF by default — an app opens no port the user didn't ask
  for. `GET /v1/ax` describes the app (descriptor + accessibility tree with
  testids and per-control risk: safe / navigation / external / sensitive /
  destructive). `/v1/ui/*` operates the real DOM via the UI bridge
  (app-local `uibridge.go` + `uibridge.ts`). Domain endpoints register
  through `apiserver.HandleExtra`.
- API port: ONE family-shared range, **8000–8999**. Each install draws its
  default port at random; Shuffle draws at random too. No per-app
  sub-ranges — collisions are near-impossible, and when one happens Start
  fails with a clear error the user resolves with Shuffle.
- Smoke test: `tools/smoke` runs against the open app with the server on;
  every unconditional testid in `/v1/ax` must be reachable on screen.

## 3. UI rules (full patterns and assets in go-design)

- NEVER a side drawer/panel for forms (permanent veto): create/edit is a
  full-window view of its own, with a back button.
- No emoji as icons — always a real Fluent (or family-chosen Lucide) SVG.
- Every Save has a Cancel next to it that discards the changes.
- Toasts are the family's notification surface (own implementation, no lib;
  top-right, theme-tinted). Form errors stay inline; no desktop
  notifications.
- Title-bar API indicator: green dot (`.api-dot`, `--success` token),
  rendered ONLY while the embedded REST server holds a port open; click
  opens the API settings; testid `api-indicator` in `/v1/ax`; backed by an
  `api:state` event emitted on every server state change.
- Content zoom: Ctrl/Cmd `+`/`−`/`0` and Ctrl+wheel. The title bar never
  scales — go-notepad zooms the editor text; form/list apps zoom the
  content area via a `.zoom-host` wrapper (50–200%, step 10%). Persisted
  (debounced) and restored on launch. **Exception: go-calc** — a fixed
  keypad grid that already scales with the window; zooming it would only
  overflow the layout (Windows Calculator has no zoom either).
- Every app has Settings sections Updates and About. go-notepad is the
  family's visual reference (labels outside cards, two-line rows, chevron
  cards for sub-views).

## 4. Updater (go-updates)

- Apps import the library for the mechanics; each app keeps a thin local
  adapter (`update.go`), the Settings → Updates UI and `GET /v1/update`.
  Reference implementation and UX decisions: go-notepad
  `docs/updater-design.md`.
- UX rules: auto-check once a day, opt-in (default OFF — no unasked network
  calls); Skip is per-tag; Later snoozes 7 days; Install downloads,
  verifies against `checksums.txt` (mandatory), swaps and restarts
  immediately.
- Release assets: `<app>-<tag>-<os>-<arch>.{zip,tar.gz}` ("macos" for
  darwin) + `checksums.txt` job after the platform builds. Windows also
  ships `<app>-<tag>-setup.exe` (go-installer).

## 5. Working conventions

- Scope new features with a batch of ~20 questions in a `.md` file, each
  with an answer line to fill in. When an answer signals a concept wasn't
  clear, stop and explain it simply before deciding.
- The maintainer runs the visual tests himself (open the app, click,
  observe); agents verify through the REST control plane.
- Gate before committing: `go vet`, `go test`, build (and the smoke suite
  when the change touches the UI or the AX tree).
- Every repo carries an `AGENTS.md` (app/lib specifics + the instruction to
  read this spec) and a one-line `CLAUDE.md` containing `@AGENTS.md`.
  Symlinks are not used (Windows checkouts break them).

## Changelog

- 1.2 (2026-07-20): explicit language rule — repos are 100% English; the
  Portuguese scope-questions doc moved out of the hub.
- 1.1 (2026-07-20): conformance audit fixes — records the go-calc content
  zoom exception (fixed keypad); go-passwords gains its `tools/smoke`
  (closing the §2 gap).
- 1.0 (2026-07-20): first consolidated spec — extracted from the hub's
  AGENTS.md; adds the shared 8000–8999 port range, title-bar API indicator,
  content zoom, toasts and the UI vetoes.
