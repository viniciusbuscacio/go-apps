# go-apps family — conventions for working sessions

This hub repo has no code. When working on any app of the family, these are
the standing conventions; each app repo's own docs override on specifics.

## Repos

- Apps: `go-calc`, `go-notepad` (more planned: file explorer, CLI).
- Libraries: `go-apiserver` (embedded REST control plane), `go-updates`
  (self-update mechanics), `go-installer` (macOS DMG builder + the Windows
  install mechanics: releases ship the same binary as a portable exe and a
  `-setup.exe` whose name opens it as the install/maintenance wizard).
- One repo per project, one local checkout per repo.
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
  codes. `GET /v1/ax` describes the app (descriptor + accessibility tree
  with testids and per-control risk: safe / navigation / external /
  sensitive / destructive). `/v1/ui/*` operates the real DOM via the UI
  bridge (app-local `uibridge.go` + `uibridge.ts`). Domain endpoints
  (`/v1/calc`, `/v1/stats`, `/v1/update`) register through
  `apiserver.HandleExtra` in each app.
- **Smoke test**: `tools/smoke` runs against the open app; every
  unconditional testid in `/v1/ax` must be reachable on screen.

## Updater (go-updates)

- Apps import `github.com/viniciusbuscacio/go-updates` (package `updater`)
  for the mechanics; each app keeps a thin local adapter (`update.go`), the
  Settings → Updates UI and the `GET /v1/update` endpoint. Reference
  implementation and UX decisions: go-notepad `docs/updater-design.md`.
- UX rules: auto-check once a day, opt-in (default OFF — no unasked network
  calls); Skip is per-tag; Later snoozes 7 days; Install downloads, verifies
  against `checksums.txt` (mandatory), swaps and restarts immediately.
- Release assets: `<app>-<tag>-<os>-<arch>.{zip,tar.gz}` ("macos" for
  darwin) + `checksums.txt` job after the platform builds.

## Working conventions

- Scope new features with a batch of ~20 questions in a `.md` file, each
  with an answer line to fill in. When an answer signals a concept wasn't
  clear, stop and explain it simply before deciding.
- The maintainer runs the visual tests himself (open the app, click,
  observe); agents verify through the REST control plane.
