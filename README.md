# go-apps

A **mini-framework** for small cross-platform desktop apps in Go — one
architecture, one look, one set of shared libraries — and the family of apps
built from it. Each project lives in its own repository and is fully
self-contained — this repo is the map.

## The apps

| Project | What it is |
|---|---|
| [go-calc](https://github.com/viniciusbuscacio/go-calc) | A Windows 11-style calculator with exact arithmetic (math/big rationals). The original template of the family. |
| [go-notepad](https://github.com/viniciusbuscacio/go-notepad) | A tabbed plain-text editor with session restore, bundled fonts and word-wrap. |

## The libraries

| Project | What it is |
|---|---|
| [go-apiserver](https://github.com/viniciusbuscacio/go-apiserver) | The embedded REST control plane: API-key auth, CIDR allowlist, the `/v1/ax` descriptor and the UI-bridge endpoints that make every app agent-operable. |
| [go-updates](https://github.com/viniciusbuscacio/go-updates) | Self-update: checks GitHub Releases, verifies `checksums.txt`, swaps the running binary and restarts. Used by every app. |
| [go-installer](https://github.com/viniciusbuscacio/go-installer) | The native install experience: the styled drag-to-Applications DMG on macOS and the embedded "next-next-finish" wizard on Windows — the downloaded exe IS the installer. |

## What makes the family a family

- **Go + Wails v2 + Vue/TypeScript**, one binary per OS (Windows, macOS,
  Linux), frameless window with its own title bar, dark/light themes.
- **Logic lives in Go** (`internal/*`, pure and testable); the frontend only
  draws. `app.go` is a thin adapter between the two.
- **Agent-operable by design**: every app embeds a REST server (API key +
  IP allowlist). `GET /v1/ax` returns the app descriptor and an accessibility
  tree — every control with its testid, action, keyboard shortcut and risk
  level — and `/v1/ui/*` presses the real buttons and reads the real screen.
  An AI agent can drive, test and update the app without touching a mouse.
  Each repo's `docs/agent-api.md` is the guide.
- **One release contract**: semver tags build all three OSes in CI and publish
  assets named `<app>-<tag>-<os>-<arch>` plus a `checksums.txt` — which is
  what the in-app updater consumes.

Each repo's README and `docs/` tell its full story; start with go-calc for
the architecture and go-notepad for the updater.

## FAQ

**Why?**
Because I always wanted to have the same app experience on Windows, Linux and
macOS. I'm building it one small app at a time.

**Why Go + Wails?**
One codebase, one small native binary per OS, no Electron-sized runtime — and
the whole app logic stays in plain, testable Go.

**Why one repository per app?**
Each app doubles as a self-contained template: you can read one repo top to
bottom and understand everything, then reuse the pattern for the next app.
What proves itself in one app graduates into a shared library (like
go-updates).

**Why "mini-framework"?**
Today it is a shared pattern (the architecture, the agent-operable REST
contract, the release pipeline) plus shared libraries, growing one piece at a
time. As more pieces graduate from the apps into libraries, the framework
part gets less "mini".
