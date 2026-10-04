# E85Calculator 0.1.0 - Prerelease

Initial native mobile prototypes and a fuel-composition calculator documenting the 2014 Toyota Aygo E85/SP98 scenario. All project documentation, interfaces and messages are in English.

- English Markdown and 16-page PDF report with primary sources, detailed calculations, uncertainty bounds and warning-light limitations.
- Native Android app in Kotlin / Jetpack Compose and native iOS app in Swift / SwiftUI, with build projects and engine tests.
- Standalone offline HTML calculator with explicit local storage, reset and result sharing.
- 18 shared reference cases, nine decimal-parsing cases, 10,000 deterministic simulations and 20 engine tests per native platform.
- Browser checks and Android/iOS verification required before release assets are published.
- Pinned GitHub Actions, dependency updates, contribution instructions and a bug-report template.

This version calculates composition under assumptions. No maximum blend guaranteeing no engine warning light is validated for the Aygo. Absence of a warning light alone does not establish fuel compatibility.

The Android asset is a **debug APK**. The iOS archive contains a **simulator application**, not a signed IPA for a physical iPhone. Release assets are created only after the corresponding CI jobs pass.
