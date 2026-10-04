# Toyota Aygo 2014
## Understanding the E85 / SP98 blend

Technical report prepared for Alexandre

**35-litre nominal tank. Two bars remaining. No proven blend that guarantees no engine warning light.**

These calculations describe fuel composition under explicit assumptions. They do not establish the ethanol tolerance of your engine.

Source-grounded documentation, an offline calculator, a native Android prototype and a native iOS prototype.

Documentary checks: 4 October 2026
Project version: 0.1.0

Scope: the French fuel market and a European-specification Toyota Aygo. All project documentation and application interfaces are in English.

<!-- pagebreak -->

# 01. Your current fill-up: a practical answer

Your vehicle is described as a 2014 petrol Toyota Aygo, rated at 69 metric horsepower, with two visible fuel-gauge bars out of six. This report assumes a standard vehicle without an approved E85 conversion. An installed conversion and its approval would change the assessment.

> With unknown remaining-fuel composition and no vehicle-specific E85 validation, the conservative choice for this fill-up is **0 litres of additional E85**, followed by **SP98 E5 until the pump's first automatic shut-off**. The 23.3 litres below are a scenario estimate, not a quantity to force into the tank.

Toyota specifies a nominal 35 L tank for the Aygo introduced in 2014. [S1]

If, only to illustrate the gauge-based reasoning, each bar represented the same volume:

```
Remaining volume R = 35 × 2 / 6 = 35 / 3 L
R = 11.666666... L
Additional volume A = 35 × 4 / 6 = 70 / 3 L
A = 23.333333... L
```

Nominal capacity and bar count do not provide a calibration in litres. Neither "one bar = 5.833 L" nor a correspondence between 35 L and your pump's shut-off has been established for this car. Gauge thresholds, vehicle inclination and filling conditions are not measured here.

**Adding SP98 dilutes ethanol when the remaining fuel contains more ethanol. It guarantees neither the absence of an engine warning light nor the disappearance of an existing fault.**

The actual quantity added is the quantity displayed by the pump. An exact composition calculation also requires the remaining volume and its composition.

<!-- pagebreak -->

# 02. Verified facts and unknowns

| Item | Evidence or status | Consequence |
| --- | --- | --- |
| 2014 Aygo, 69 metric hp | User description | Exact VIN identification not supplied |
| 1.0 VVT-i engine, 998 cm³ | Toyota 2014 specification [S1] | Consistent documentary reference |
| 35 L tank | Toyota nominal capacity [S1] | Does not measure remaining litres |
| SP95-E10 compatibility | European 2014 Aygo covered by the French list [S2] | Applies to compliant standardised fuel |
| E85 conversion | Not specified | Standard-vehicle assumption |
| Remaining fuel | E85 and SP98 mentioned; proportions unknown | No exact ethanol fraction can be assigned |
| Pump-fuel ethanol | Not measured | Use bounds or a batch composition certificate |
| ECU correction limits | Not measured | No personalised warning-light threshold established |

The official French list dated June 2026 covers Toyota vehicles marketed for Europe from January 1998, with exceptions for particular Avensis models. A European 2014 Aygo is therefore covered. This establishes compatibility with **compliant SP95-E10**, not any arbitrary mixture that happens to have the same ethanol fraction. [S2]

The original expressions "Super Ethanol E95" and "E98" are interpreted here as **Superethanol E85** and **SP98 E5 petrol**, consistently with the requested E85/SP98 comparison.

SP95 and SP98 refer to research octane ratings. E5, E10 and E85 describe alcohol composition; 98 does not mean 98% petrol. SP98 E5 permits up to 5% ethanol without guaranteeing an exact 5% content. [S3]

<!-- pagebreak -->

# 03. E85 varies by batch and season

Annex II of the consolidated French fuel order distinguishes the following periods. The regulated quantity is the combined volume percentage of **ethanol plus saturated higher alcohols**. [S4]

| Period | Dates | Minimum combined content | Maximum |
| --- | --- | --- | --- |
| Winter | 1 November to 15 March | 60% | 85% |
| Transition seasons | 16 March to 30 April; 1 to 31 October | 60% | 85% |
| Summer | 1 May to 30 September | 70% | 85% |

**4 October 2026 is in a transition season. It is incorrect to assume that your station's E85 necessarily contains 65%, 75% or 85% ethanol.** [S4]

The ministry commonly describes E85 as containing 60–85% ethanol. [S3] When distinguishing pure ethanol, the annex's wording matters: higher alcohols may reach 6% by volume. A theoretical lower ethanol bound is therefore 60 - 6 = 54% in winter and transition seasons, or 70 - 6 = 64% in summer. These are bounds derived from specifications, not measurements of your batch. [S4]

The calculator defaults to **54–85% pure ethanol in the E85 pump fuel**. The 85% upper bound determines the maximum addition under a selected ceiling. Examples labelled E60 or E85 explicitly assume those pure-ethanol fractions.

The order restricts E85 use to Flex-fuel vehicles and SP95-E10-compatible vehicles fitted with an approved conversion. [S4] Calculating a percentage does not validate a conversion or demonstrate compliance with every EN 228 petrol requirement. Volatility, oxygenates, distillation characteristics and material compatibility cannot be represented by one fraction.

<!-- pagebreak -->

# 04. Why the warning light is not a reliable threshold

A 2009 DOE / NREL / ORNL study examined 16 vehicles with blends up to E20. It did not report warning-light illumination attributable to ethanol content during that limited phase. However, seven vehicles became relatively leaner at high load, unlike the other nine; application of learned corrections depended on engine-management strategy. See PDF pages 37 and 41–43, sections 3.1.3 and 3.1.5. [S5]

**Inference: the absence of a warning light is insufficient evidence of correct fuelling under every operating condition.** This study predates your 2014 Aygo and does not validate E20, E30 or E50 for it.

Short-term fuel trim, STFT, and long-term fuel trim, LTFT, describe ECU fuelling adjustments. A positive correction may be consistent with additional fuel demand, but can have other causes. A single idle reading does not characterise the complete operating range.

The ECU calibration, diagnostic readings, thermal conditions, cold-start and high-load strategies, and injector margins are unknown for this car. **No universal LTFT or ethanol threshold is adopted here as a guarantee against a warning light.**

SP98 is not an antidote to E85. It dilutes ethanol because it contains much less of it; a higher octane rating does not itself create additional injector-flow capacity.

The technically defensible goal is to validate compatibility and fuelling. Searching only for the warning-light boundary can overlook a problem elsewhere in the operating range.

<!-- pagebreak -->

# 05. The volume balance

Ethanol fractions range from 0 to 1: 30% is written as 0.30. Volumes are expressed in litres.

| Variable | Definition |
| --- | --- |
| R | Remaining fuel volume |
| er | Ethanol fraction of the remaining fuel |
| X | Added volume of fuel sold as E85 |
| ep | Actual ethanol fraction of that E85 |
| Y | Added SP98 volume |
| es | Actual ethanol fraction of the SP98 |
| C | Final volume used in the model: R + X + Y |
| t | Target final fraction in a simulation |

```
Ethanol volume = R × er + X × ep + Y × es
Final fraction ef = (R × er + X × ep + Y × es) / C
With A = C - R and Y = A - X:
X = [C × t - R × er - A × es] / (ep - es)
Y = A - X
```

This equation solves a **composition**, not an engine-tolerance question. It assumes additive, comparable volumes, homogeneous mixing and known fractions. Temperature effects and slight real-world non-additivity are omitted: the figures are algebraically exact under assumptions, not a laboratory analysis.

If X is negative, adding only SP98 still exceeds the target: **the target is impossible by adding fuel to this final volume**. If X exceeds A, even filling the available space entirely with E85 cannot reach the target. If ep = es, both additions affect composition equally and this division is undefined.

For an actual completed fill-up, use the litres displayed at both pumps rather than assuming C is necessarily 35 L.

<!-- pagebreak -->

# 06. Worked example: two bars out of six

**Calculation example, not a fuel-use recommendation: target E30.** Assumptions: C = 35 L; R = 35/3 L; remaining fuel exactly 5% ethanol; E85 exactly 85%; SP98 exactly 5%.

```
A = 35 - 35/3 = 70/3 L
X = [35 × 0.30 - (35/3) × 0.05 - (70/3) × 0.05]
    / (0.85 - 0.05)
X = 8.75 / 0.80 = 10.9375 L of E85
Y = 70/3 - 10.9375 = 12.395833... L of SP98
```

Independent check through ethanol conservation:

```
Remaining ethanol = (35/3) × 0.05 = 0.583333... L
Ethanol from E85 = 10.9375 × 0.85 = 9.296875 L
Ethanol from SP98 = 12.395833... × 0.05
                 = 0.619791666... L
Total = 10.5 L of ethanol; 10.5 / 35 = 0.30
```

| Simulation rounding | E85 | SP98 remainder | Final content |
| --- | --- | --- | --- |
| Algebraic values | 10.9375 L | 12.395833... L | 30.0000% |
| E85 rounded down to 0.01 L | 10.93 L | 12.403333... L | 29.9829% |

E85 represents approximately **46.87% of the added fuel**, whereas the final mixture contains 30% ethanol. These percentages describe different quantities.

The apps round X down to 0.01 L, then calculate Y as the exact remainder in the model. Displaying Y to two decimal places only rounds its presentation. An actual addition must be reassessed using the actual final volume.

<!-- pagebreak -->

# 07. Comparing hypothetical targets

Every row assumes C = 35 L, R = 35/3 L, remaining fuel and SP98 exactly 5%, and E85 exactly 85%. Displayed volumes are rounded to two decimals. **No row is a validated threshold for your Aygo.**

| Target | Added E85 | Added SP98 | E85 / addition | Interpretation |
| --- | --- | --- | --- | --- |
| E10 | 2.19 L | 21.15 L | 9.37 % | Simulation only |
| E20 | 6.56 L | 16.77 L | 28.13 % | Simulation only |
| E30 | 10.94 L | 12.40 L | 46.88 % | Simulation only |
| E40 | 15.31 L | 8.02 L | 65.62 % | Simulation only |
| E50 | 19.69 L | 3.65 L | 84.38 % | Simulation only |
| E60 | Exceeds available volume | - | - | Maximum : E58.33 |

E10 is a numerical reference corresponding to the ethanol limit of the compatible standardised fuel. A homemade 10% blend is not automatically equivalent to compliant SP95-E10. Higher targets are explanatory simulations without vehicle qualification.

Pump composition also changes the solution. For the same mathematical E30 target, volumes, remaining fuel and SP98:

| Assumed pump ethanol | Added E85 | Added SP98 | E85 / addition |
| --- | --- | --- | --- |
| 60 % | 15.91 L | 7.42 L | 68.18 % |
| 70 % | 13.46 L | 9.87 L | 57.69 % |
| 75 % | 12.50 L | 10.83 L | 53.57 % |
| 85 % | 10.94 L | 12.40 L | 46.88 % |

If the 10.9375 L of E85 actually contains 60% ethanol, keeping the SP98 amount from the 85% example produces **22.19%**, rather than 30%. Apparently precise litre quantities cannot correct unknown pump composition.

Adding "a small splash" of SP98 to a large amount of E85 does not create a low-ethanol blend. Excluding remaining fuel, 90% E85 at 85% plus 10% SP98 at 5% gives 0.90 × 0.85 + 0.10 × 0.05 = **77% ethanol**.

<!-- pagebreak -->

# 08. Remaining fuel can make a target impossible

This table assumes C = 35 L, R = 35/3 L, added E85 at 85% and added SP98 at 5%. Each row assumes a different remaining-fuel composition.

| Assumed remainder | After adding only SP98 | E85 to target E30 | SP98 to target E30 |
| --- | --- | --- | --- |
| E5 | 5.00 % | 10.94 L | 12.40 L |
| E10 | 6.67 % | 10.21 L | 13.12 L |
| E20 | 10.00 % | 8.75 L | 14.58 L |
| E30 | 13.33 % | 7.29 L | 16.04 L |
| E50 | 20.00 % | 4.38 L | 18.96 L |
| E70 | 26.67 % | 1.46 L | 21.88 L |
| E85 | 31.67 % | Impossible | Impossible |

> If the remaining fuel actually contains 85% ethanol, adding only 23.333333... L of SP98 at 5% still leaves **31.666666...% ethanol**. E30 and E10 are impossible to reach simply by adding fuel up to 35 L.

```
ef = [(35/3) × 0.85 + (70/3) × 0.05] / 35
ef = 0.316666666...
```

If the two remaining bars contain an unknown E85/SP98 blend, its ethanol fraction may be much higher than the E5 assumption used earlier. This is why an exact "number of E85 litres to add now" cannot be justified from the gauge bars alone.

Repeated dilution can be modelled under assumptions. If a homogeneous tank is consumed down to volume fraction q, then topped up with fuel of fraction es:

```
e(n+1) = q × e(n) + (1-q) × es
After n identical cycles: e(n) = es + q^n × [e(0)-es]
```

Purely mathematical example: q = 1/3, e(0) = 0.85 and es = 0.05 produce 31.67%, 13.89%, then 7.96% after successive additions. This sequence does not instruct you to keep driving with irregular engine operation and does not model warning-light behaviour.

<!-- pagebreak -->

# 09. Calculate with explicit uncertainty

For a modelled known volume R and bounded compositions, every volume contribution is non-negative. Blend bounds therefore follow from combining the minimum and maximum fractions separately.

```
ef_min = [R × er_min + X × ep_min + Y × es_min] / C
ef_max = [R × er_max + X × ep_max + Y × es_max] / C
```

To **mathematically maximise X under ceiling t**, use the upper bounds:

```
X_max = [C × t - R × er_max - (C-R) × es_max]
        / (ep_max - es_max)
```

A negative result means the ceiling cannot be guaranteed across all entered compositions. The calculator returns "ceiling cannot be guaranteed" and no E85 volume. It does not turn an infeasible result into a blending instruction.

With two bars out of six, remaining ethanol unknown between 0 and 85%, and SP98 between 0 and 5%, adding only SP98 gives a theoretical range of **0–31.67%**. This prevents a guaranteed E10 ceiling in that scenario.

The solver caps X at the available volume and rounds it down. This optimisation respects **the entered ceiling under the model's assumptions**; it does not prove that the ceiling suits the engine.

Remaining-volume uncertainty differs from composition uncertainty. If R has bounds, R × (er - es) is linear: check both endpoints of R with an X physically possible at each. The prototypes accept one R and flag an estimate without inventing a litre interval from gauge bars.

If only E85 and SP98 have been used with unknown proportions, 0–85% is a conservative envelope for the remaining ethanol fraction. It is not suitable for a tank containing another substance.

<!-- pagebreak -->

# 10. Injection demand and fuel energy

Argonne reference properties illustrate volumetric fuel demand: petrol density 0.741 kg/L and stoichiometric air/fuel ratio 14.7; ethanol density 0.790 kg/L and ratio 9.0. The listed lower heating values are 42.7 and 26.8 MJ/kg. These describe reference fuels, not your SP98 batch or the Aygo calibration. See slide 3, PDF page 3. [S6]

For volume fraction e and the same air mass flow, using a binary petrol/ethanol model:

```
Air required per litre B(e) = (1-e) × 0.741 × 14.7
                           + e × 0.790 × 9.0
Fuel volume relative to E5 = B(0.05) / B(e)
Energy per litre H(e) = (1-e) × 0.741 × 42.7
                     + e × 0.790 × 26.8
```

| Blend | B(e), kg air/L | Extra flow vs E5 | H(e), MJ/L |
| --- | --- | --- | --- |
| E5 | 10.704 | 0.00 % | 31.12 |
| E10 | 10.514 | 1.80 % | 30.59 |
| E20 | 10.136 | 5.60 % | 29.55 |
| E30 | 9.758 | 9.69 % | 28.50 |
| E50 | 9.001 | 18.91 % | 26.41 |
| E85 | 7.677 | 39.42 % | 22.74 |

Density must enter the calculation. Weighting mass-based air/fuel ratios directly by volume percentages would be a different approximation.

This stoichiometric flow is neither a prediction of LTFT nor a road-consumption forecast. Starting, vaporisation, commanded richness, other oxygenates such as ETBE, and actual engine efficiency remain outside the model.

<!-- pagebreak -->

# 10a. Modelled flow and energy per litre

These charts use only the assumptions and equations on the previous page. The bars show model outputs, not measurements on your Aygo.

<!-- figure: injection.png -->

At higher ethanol fractions, the model requires more fuel volume to maintain the same stoichiometric balance with the same airflow. For E85 it gives approximately **39.4% extra flow** relative to E5. Your injector margin and ECU command strategy are unknown.

<!-- figure: energy.png -->

The model gives 31.12 MJ/L at E5 and 22.74 MJ/L at E85. With identical efficiency and energy demand, H(E5) / H(E85) implies 36.8% more fuel volume. This simplified assumption is not a road-consumption forecast.

<!-- pagebreak -->

# 11. Evidence needed for engine validation

Going beyond a composition simulation requires documenting the exact vehicle, any conversion, the condition of its fuel system and fuelling under the relevant operating conditions. This report does not replace that assessment.

| Information to record | Purpose |
| --- | --- |
| VIN, engine, ECU reference and calibration | Avoid extrapolating from another Aygo |
| E85 conversion and approval, if fitted | Check the intended operating scope |
| Fuel types, litres and mileage at every fill-up | Reconstruct the remainder in a homogeneous model |
| Stored and pending OBD codes and associated data | Identify a fault before attributing it to fuel |
| STFT, LTFT, open/closed loop, temperature and load | Put observed corrections in context |
| Cold starting, misfires, lambda and fuel supply | Examine conditions not covered by idle readings |

Retaining codes and associated data before resetting prevents loss of diagnostic evidence. Irregular operation, loss of power or a flashing warning light warrants stopping the trial and having the vehicle examined. Provoking a fault is unnecessary to calculate composition.

For blend tracking, record mileage and the litres of each fuel at every fill-up. Under the homogeneous-tank assumption, composition stays unchanged during consumption while volume decreases. Keep this assumption separate from an actual measurement.

To compare costs without inventing your station's prices:

```
Addition cost = X × E85_price + Y × SP98_price
Average price of added litres = cost / (X+Y)
Cost per 100 km = measured consumption × consumed-fuel price
```

The average addition price does not immediately describe the cost of fuel already in the tank. Actual savings depend on measured consumption and, where applicable, conversion cost.

<!-- pagebreak -->

# 12. The supplied calculators

| Deliverable | Technology | Use |
| --- | --- | --- |
| Android | Kotlin and Jetpack Compose | Android Studio project, native interface |
| iOS | Swift and SwiftUI | Xcode project, native interface |
| Offline demonstration | HTML/CSS/JavaScript with no remote dependencies | Open web/index.html in a browser |

The mobile apps use native interfaces and their own calculation engines. The HTML page is a third standalone calculator. Neither mobile project substitutes a WebView for its native interface.

Features include final and remaining volume, composition bounds for remaining fuel and E85, a selected numerical ceiling, final interval, infeasible-case rejection, downward E85 rounding, local storage and result sharing. The "2 bars out of 6" scenario is explicitly an estimate.

The interfaces bound SP98 between 0 and 5%. For an exact 5% simulation, the engine accepts a single-point interval. Initial settings use an unknown remaining composition and a 10% ceiling, exposing uncertainty instead of arbitrarily proposing an E85-rich blend.

**The entered ceiling is not a known property of the Aygo.** The prototypes offer no learned engine threshold, warning-light prediction or OBD connection. Source links and the documentary date remain visible.

Open android in Android Studio with JDK 17, Android SDK 36 and Gradle 8.13. Open ios/AygoBlend.xcodeproj in Xcode for an iOS 16 or later simulator. README.md describes build commands and prerequisites.

Distribution: the release pipeline requires successful Android and iOS checks. The Android asset is a debug APK; the iOS asset is a simulator app archive, not a signed iPhone IPA. Check the repository's CI result for the specific commit before treating a build as validated.

<!-- pagebreak -->

# 13. Verification and maintenance

The JavaScript engine is verified through 18 reference cases, nine decimal-parsing cases and 10,000 deterministic simulations. Checks cover volume conservation, all eight composition-interval corners, ceiling compliance and X optimality through an independent numerical search. Invalid inputs and infeasible targets are covered.

Kotlin and Swift projects each contain 20 tests: the same 18 reference cases, decimal parsing and rejection of non-finite numbers. GitHub workflows build Android, test iOS on a simulator, check documents and publish a release only after verification succeeds. A workflow file alone is not evidence of a successful run.

PDF and Markdown are generated from shared English content by tooling/build_report.py and tooling/report_pages.py. Scientific content, units and assumptions must remain synchronised with all three engines.

Regulatory bounds do not update automatically in this prototype. Changes require checking the consolidated order, documenting updated values and publishing a new version. A future remote source should retain provenance, retrieval date and offline behaviour. No public API is assumed to know the composition of your fuel batch.

**Still undetermined: the maximum blend that avoids a warning light for your car.** A litre balance cannot establish it. The supplied documentation distinguishes calculable compositions from engine behaviour requiring vehicle-specific validation.

The balance can be exact under its assumptions even when input data are uncertain. Additional decimal places do not turn a fuel-gauge estimate into a measurement.

<!-- pagebreak -->

# 14. Sources checked on 4 October 2026

**[S1] Toyota, Aygo introduction, 4 March 2014.** Specification: 1.0 VVT-i, 998 cm³, nominal 35 L tank.

[Toyota 2014 specification](https://media.toyota.co.uk/new-aygo-toyota-steps-fun-factor-new-city-car/)

**[S2] French ministry responsible for ecology, June 2026 SP95-E10 list.** PDF page 5, TOYOTA: European vehicles from January 1998, with Avensis exceptions.

[Official SP95-E10 compatibility list](https://www.ecologie.gouv.fr/sites/default/files/documents/Liste_v%C3%A9hicules_SP95-E10_Juin2026.pdf)

**[S3] French ministry responsible for ecology, authorised fuels.** French definitions of SP95/SP98 E5, SP95-E10 and E85.

[Fuels authorised in France](https://www.ecologie.gouv.fr/politiques-publiques/carburants-combustibles-autorises-france)

**[S4] Légifrance, consolidated order of 28 December 2006 on superethanol specifications.** Article 3: permitted uses; annexes I and II: alcohols and seasons. Displayed last update: 1 February 2026; annexes amended on 18 April 2025.

[Consolidated superethanol order](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000245613/)

**[S5] Knoll et al., DOE / NREL / ORNL, February 2009.** Effects of Intermediate Ethanol Blends on Legacy Vehicles and Small Non-Road Engines, Report 1 - Updated. NREL/TP-540-43543, ORNL/TM-2008/117. PDF pages 37 and 41–43; internal pages 3-2 and 3-6 to 3-8.

[DOE / NREL / ORNL experimental study](https://www.energy.gov/sites/prod/files/2014/03/f14/pub_int_blends_rpt1_updated.pdf)

**[S6] Ickes and Wallner, Argonne National Laboratory, DEER 2011.** Cold-Start Performance and Emissions Behavior of Alcohol Fuels in an SIDI Engine Using Transient Hardware-In-Loop Test Methods. Slide 3, PDF page 3: reference properties.

[Argonne / DOE fuel properties](https://www.energy.gov/sites/default/files/2014/03/f8/deer11_ickes.pdf)

**[S7] Google and Apple, native technology documentation.** Prototype build references; no automotive conclusions are inferred from them.

[Android Gradle Plugin 8.13 compatibility](https://developer.android.com/build/releases/agp-8-13-0-release-notes)
[SwiftUI documentation](https://developer.apple.com/documentation/swiftui)

The 2009 and 2011 studies explain mechanisms and experimental limits. They are not presented as tests of your 2014 Aygo. Source documents may be in French; all labels and explanations in this project are in English.
