# go-apps

A family of small cross-platform desktop apps written in Go, sharing one
architecture, one look and one set of libraries. Each project lives in its own
repository and is fully self-contained — this repo is the map.

## The apps

| Project | What it is |
|---|---|
| [go-calc](https://github.com/viniciusbuscacio/go-calc) | A Windows 11-style calculator with exact arithmetic (math/big rationals). The original template of the family. |
| [go-notepad](https://github.com/viniciusbuscacio/go-notepad) | A tabbed plain-text editor with session restore, bundled fonts and word-wrap. |

## The libraries

| Project | What it is |
|---|---|
| [go-updates](https://github.com/viniciusbuscacio/go-updates) | Self-update: checks GitHub Releases, verifies `checksums.txt`, swaps the running binary and restarts. Used by every app. |
| go-install *(planned)* | The "next-next-finish" install wizard, embedded in each app's own binary. |

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
