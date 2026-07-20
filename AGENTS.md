# go-apps family — conventions for working sessions

This hub repo has no code. When working on any app of the family, these are
the standing conventions; each app repo's own docs override on specifics.

**Where rules live (the golden rule):** engineering/architecture conventions
live HERE; UI/UX patterns and visual rules live in **go-design** (read it
before touching any app UI). When a session produces a new learning, record
it in the right one of those two places — that is how the next app inherits
it. Every repo carries an `AGENTS.md` (this convention) plus a one-line
`CLAUDE.md` containing `@AGENTS.md`, so any agent picks the rules up
automatically.

## Repos

- Apps: `go-calc`, `go-notepad`, `go-passwords` (password manager: encrypted
  `.gpw` vault, GUI + `go-pw-cli` CLI). More planned: file explorer, CLI.
- Libraries: `go-apiserver` (embedded REST control plane), `go-updates`
  (self-update mechanics), `go-installer` (macOS DMG builder + the Windows
  install mechanics: releases ship the same binary as a portable exe and a
  `-setup.exe` whose name opens it as the install/maintenance wizard).
- Design: `go-design` — the style guide (icon rules, tokens, tiles, UI
  patterns, vendored SVGs). READ IT BEFORE TOUCHING ANY APP UI; new apps
  copy assets from there (copy, don't link; `main` is the truth).
  Icon rule: Fluent System Icons first; Lucide where Fluent has no equivalent
  or the family already chose it (identity tiles are Lucide, by decision).
- One repo per project, one local checkout per repo (side by side in the
  same parent directory — sibling paths like `../go-design` resolve).
- Commits: conventional commits, English, straight to main. Releases via
  annotated semver tags (`vX.Y.Z`) — the tag push triggers the release CI.

## Architecture (every app)

- **Stack**: Go + Wails v2 + Vue 3/TypeScript. Business logic in
  `internal/<domain>` — pure Go, testable, no Wails imports. `app.go` is a
  thin adapter. The frontend only renders; rules live in Go.
- **Look**: frameless window, custom title bar, dark/light themes, English
  UI, Fluent/Win11 style. App icons: Lucide glyph, white stroke on the
  family's dark rounded tile (`build/appicon-source.svg`; regenerate
  `appicon.png` and a multi-size `icon.ico` from it — render each size from
  the vector).
- **REST control plane** (the `go-apiserver` library): X-API-Key + CIDR
  allowlist, structured errors `{"error":{code,message,status}}` with stable
  codes. OFF by default — an app opens no port the user didn't ask for.
  `GET /v1/ax` describes the app (descriptor + accessibility tree
  with testids and per-control risk: safe / navigation / external /
  sensitive / destructive). `/v1/ui/*` operates the real DOM via the UI
  bridge (app-local `uibridge.go` + `uibridge.ts`). Domain endpoints
  (`/v1/calc`, `/v1/stats`, `/v1/update`, go-passwords' `/v1/secrets`…)
  register through `apiserver.HandleExtra` in each app.
- **Port ranges**: go-calc 8700–8799, go-notepad 8800–8899,
  go-passwords 8900–8999. Next app takes the next hundred.
- **Smoke test**: `tools/smoke` runs against the open app; every
  unconditional testid in `/v1/ax` must be reachable on screen.

## UI rules (full patterns in go-design; the hard vetoes)

- **NEVER a side drawer/panel for forms** (permanent veto): create/edit is a
  full-window view of its own, with a back button.
- **No emoji as icons** — always a real Fluent (or family-chosen Lucide) SVG.
- **Every Save has a Cancel next to it** that discards the changes.
- **Toasts** are the family's notification surface (own implementation, no
  lib; top-right, theme-tinted). Form errors stay inline; no desktop
  notifications.
- **Title-bar API indicator**: green dot (`.api-dot`, `--success` token),
  rendered ONLY while the embedded REST server holds a port open; click
  opens the API settings; testid `api-indicator` in `/v1/ax`. Backed by an
  `api:state` event emitted on every server state change.
- **Content zoom**: Ctrl/Cmd `+`/`−`/`0` and Ctrl+wheel. Title bar never
  scales — notepad zooms the editor text; form/list apps zoom the content
  area via a `.zoom-host` wrapper (50–200%, step 10%). Persisted (debounced)
  and restored on launch.
- Every app has Settings sections **Updates** and **About**, and the
  go-notepad Settings layout is the visual reference (labels outside cards,
  two-line rows, chevron cards for sub-views).

## Updater (go-updates)

- Apps import `github.com/viniciusbuscacio/go-updates` (package `updater`)
  for the mechanics; each app keeps a thin local adapter (`update.go`), the
  Settings → Updates UI and the `GET /v1/update` endpoint. Reference
  implementation and UX decisions: go-notepad `docs/updater-design.md`.
- UX rules: auto-check once a day, opt-in (default OFF — no unasked network
  calls); Skip is per-tag; Later snoozes 7 days; Install downloads, verifies
  against `checksums.txt` (mandatory), swaps and restarts immediately.
- Release assets: `<app>-<tag>-<os>-<arch>.{zip,tar.gz}` ("macos" for
  darwin) + `checksums.txt` job after the platform builds. Windows also
  ships `<app>-<tag>-setup.exe` (go-installer).

## Working conventions

- Scope new features with a batch of ~20 questions in a `.md` file, each
  with an answer line to fill in. When an answer signals a concept wasn't
  clear, stop and explain it simply before deciding.
- The maintainer runs the visual tests himself (open the app, click,
  observe); agents verify through the REST control plane.
- Gate before committing: `go vet`, `go test`, build (and the smoke suite
  when the change touches the UI or the AX tree).
