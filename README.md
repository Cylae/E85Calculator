# E85Calculator · Aygo Blend

[![CI](https://github.com/Cylae/E85Calculator/actions/workflows/ci.yml/badge.svg)](https://github.com/Cylae/E85Calculator/actions/workflows/ci.yml)

An E85/SP98 composition calculator, a sourced technical report for a 2014 Toyota Aygo, and **native Android and iOS prototypes**. All documentation, app interfaces, validation messages and release notes are in English. The fuel specifications covered by the report apply to France.

**No maximum blend guaranteeing the absence of an engine warning light is established for an unconverted Aygo.** This project simulates composition under assumptions; it does not determine engine tolerance or replace conversion validation or diagnosis.

Toyota specifies a nominal 35 L tank. The “two bars out of six” scenario uses an illustrative 11.67 L remaining volume. Gauge bars are not a measurement in litres.

| Deliverable | Location |
| --- | --- |
| English report with calculations, limitations and primary sources | [Markdown](reports/Report_Toyota_Aygo_E85_SP98.md) and [PDF](reports/Report_Toyota_Aygo_E85_SP98.pdf) |
| Standalone offline calculator | [web/index.html](web/index.html) |
| Native Android: Kotlin + Jetpack Compose | [android/](android/) |
| Native iOS: Swift + SwiftUI | [ios/AygoBlend.xcodeproj](ios/AygoBlend.xcodeproj) |
| Reference calculation engine and tests | [verification/](verification/) |
| Document generation and structural checks | [tooling/](tooling/) |
| Build, test and release pipeline | [.github/workflows/ci.yml](.github/workflows/ci.yml) |

## Model

```text
ef = (R × er + X × ep + Y × es) / C
C = R + X + Y
X = [C × t - R × er - (C-R) × es] / (ep - es)
```

Volumes are in litres; fractions range from 0 to 1. `X` is the volume of fuel sold as E85, not pure ethanol. The solver uses upper composition bounds to maximise `X` under a selected ceiling. If even adding only SP98 cannot guarantee that ceiling, it returns an infeasible result and no E85 quantity. `X` is rounded down to 0.01 L.

Defaults: simulated final volume 35 L, estimated remaining volume 11.67 L, unknown remaining ethanol 0–85%, SP98 0–5%, pump E85 54–85%, selected ceiling 10%. The 54% lower bound distinguishes pure ethanol from the regulatory sum of ethanol and higher alcohols, which may contribute up to 6%. Actual batch composition requires measurement or documentation.

A simulated 10% ceiling does not establish compliance with every standardised SP95-E10 requirement. The apps neither predict warning lights nor control the ECU or clear faults.

## Use the offline calculator

Open `web/index.html` in a browser. Its engine, interface and styles are embedded; calculation requires no installation or remote requests. Saving assumptions is explicit and local. Source links open only when requested. Displayed numbers use English decimal points; input also accepts a decimal comma.

## Android

Requirements: Android Studio compatible with AGP 8.13, JDK 17, Android SDK 36 and Gradle 8.13. Open `android/` as a Gradle project. Dependencies: AGP 8.13.2, Kotlin 2.2.20 and Compose BOM 2025.09.00. Minimum Android version: API 26 / Android 8.0.

A binary Gradle wrapper is not included. CI installs the specified Gradle version. With Gradle 8.13 available:

```bash
gradle -p android testDebugUnitTest assembleDebug
```

The debug APK is created at `android/app/build/outputs/apk/debug/app-debug.apk`. The app requests no network permission. It saves fields locally only when the user chooses to save them.

## iOS

Open `ios/AygoBlend.xcodeproj` in Xcode and select an iPhone or iPad simulator. The project includes a shared `AygoBlend` scheme and an XCTest target. Minimum iOS version: 16. No external dependencies.

```bash
python3 tooling/test_ios.py
```

The script chooses an available iPhone simulator and runs `xcodebuild test` with simulator code signing disabled. A physical iPhone requires an Apple signing team and a device build. The simulator archive is not an installable iPhone IPA. Assumptions are stored locally through `AppStorage` as they are edited.

## Generate and verify

```bash
node verification/test_blend.cjs
python3 -m pip install -r requirements.txt
python3 tooling/create_projects.py
python3 tooling/build_report.py
python3 tooling/build_html.py
python3 tooling/verify_artifacts.py
```

The same 18 numerical cases are used by JavaScript and generated as Kotlin/XCTest fixtures. JavaScript also checks nine parsing cases and 10,000 deterministic simulations, including volume conservation, interval bounds and an independently searched maximum. Each native suite contains 20 tests.

Browser checks use Playwright:

```bash
npm install
npx playwright install chromium
node verification/test_web.cjs
```

The browser suite verifies reset after saving, stale results, comma input, invalid volumes, impossible ceilings, offline operation and mobile overflow. CI runs these checks, builds the Android debug APK and tests iOS on a simulator. Failed checks block release publication. Browser screenshots and test summaries are retained as CI artifacts.

The report's PDF layout is visually reviewed after generation. For the exact published commit's build status, use the CI badge and the linked workflow run rather than assuming success from the existence of workflow files.

## Release

Tags matching `v*` run verification. After all three verification jobs pass, the release job publishes a **prerelease** containing the PDF, Markdown, offline HTML, source archive, Android debug APK and iOS simulator app archive. Notes come from `RELEASE_NOTES.md`.

The workflow can also be started from Actions with `release_version` set to a version such as `v0.1.0`. It creates the tag and prerelease on the verified commit after all jobs pass. Leaving the field empty runs verification only.

For the initial publication through an integration that can push commits but cannot create tags, an exact commit message of `Release v0.1.0` on `main` also requests that first prerelease. The same checks still apply.

## Publish a new copy

`tooling/publish_github.py` uses the authenticated GitHub CLI identity to create a new private repository by default, configure its description and topics, push `main`, then push `v0.1.0`. It avoids modifying an existing repository of the same name. Use `--public` only for an explicitly public copy.

```bash
python3 tooling/publish_github.py
```

This command requires Git, authenticated GitHub CLI, a clean reviewed commit on `main`, and no existing remote. It is for a new copy; the current project is [Cylae/E85Calculator](https://github.com/Cylae/E85Calculator).

## Sources and maintenance

Primary sources, dates and relevant pages are listed in the report. Regulatory bounds were checked on 4 October 2026 and do not update automatically. Changes must document updated assumptions and amend affected test cases. See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow.

MIT licence. No affiliation with Toyota.
