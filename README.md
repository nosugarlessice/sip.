# sip.

days in cups. A quiet drink diary: snap the cup in your hand, sip to rate it, and watch your month fill up with little stickers.

- **Website:** https://nosugarlessice.github.io/sip./ (from `docs/`)
- **The app (iPhone and any browser):** https://nosugarlessice.github.io/sip./app/ — add it to your home screen
- **Android:** https://github.com/nosugarlessice/sip./releases/latest/download/sip-android.apk

## What's where

| Path | What it is |
|---|---|
| `docs/index.html` | The website. Add `?adjust` to its address for the spacing panel. |
| `docs/app/` | The app, as an installable web app (manifest, offline service worker, icons) |
| `docs/app/ml/` | The on-phone cutout model (U2-Net-p) and its runtime. Photos never leave the phone. |
| `android/` | Wraps `docs/app` into an Android app with Capacitor |
| `.github/workflows/android.yml` | Builds the `.apk` and attaches it to a release when a `v*` tag is pushed |
| `sip-source.html` | The app's single source file (what `docs/app/index.html` is built from) |

## Releasing the Android app

Push a tag like `v0.1.0`, or run **Actions → Build Android app** with a version. The `.apk` lands on the release with the same name every time, so the website's download link always gets the newest one.
