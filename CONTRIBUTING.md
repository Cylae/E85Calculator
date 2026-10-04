# Contributing to E85Calculator

Use an issue to describe a calculation, interface or documentation defect. Include volumes, composition bounds, the selected ceiling, the observed result and the expected result. Keep gauge-bar scenarios explicitly labelled as estimates. All new code messages, interfaces, documentation and release notes must be in English.

## Change the calculation

The reference model is `verification/blend.js`. Reflect model changes in the Kotlin and Swift engines. Add an independently checked case to `verification/test_vectors.json`, then update its definition in `tooling/create_projects.py`, which regenerates the aligned native fixtures and the vector file.

The model must conserve volume, apply upper bounds for the ceiling, round E85 down and reject infeasible targets. Calculated composition does not validate engine compatibility.

## Change an interface or the report

Edit `tooling/web_template.html`, then run `python3 tooling/build_html.py`. The standalone HTML embeds the exact reference engine.

English report content is in `tooling/report_pages.py`; layout and calculations are in `tooling/build_report.py`. After generation, inspect the rendered PDF for page breaks, margins, figures and links. Use dated primary sources for technical facts and distinguish specifications, assumptions and measurements.

## Verify a change

```bash
node verification/test_blend.cjs
python3 tooling/verify_artifacts.py
npm install
npx playwright install chromium
node verification/test_web.cjs
gradle -p android testDebugUnitTest assembleDebug
python3 tooling/test_ios.py
```

The last two commands require the Android environment described in the README and a Mac with Xcode and an iOS simulator, respectively. CI runs them on suitable platforms. Explain the change and the checks actually performed in a pull request.

## Publish a version

Update `CHANGELOG.md`, `RELEASE_NOTES.md` and app version numbers. Create a `vX.Y.Z` tag or start the workflow with `release_version`. The release job waits for all three verification jobs. Current app artifacts are an Android debug APK and an iOS simulator application; they are not signed production distributions.
