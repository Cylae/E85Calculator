import SwiftUI

struct ContentView: View {
    @AppStorage("final") private var finalVolume = "35"
    @AppStorage("remaining") private var remaining = "11.67"
    @AppStorage("rLow") private var residualLow = "0"
    @AppStorage("rHigh") private var residualHigh = "85"
    @AppStorage("pLow") private var pumpLow = "54"
    @AppStorage("pHigh") private var pumpHigh = "85"
    @AppStorage("target") private var target = "10"
    @AppStorage("estimated") private var estimated = true
    @State private var confirmed = false
    @FocusState private var editing: Bool
    private func number(_ text: String) throws -> Double {
        guard let n = BlendEngine.parseDecimal(text) else {
            throw BlendError.invalid("Enter a valid number in every field.")
        }
        return n
    }
    private var calculation: Result<BlendOutput, Error> {
        Result {
            try BlendEngine.calculate(BlendInput(finalLiters: number(finalVolume), remainingLiters: number(remaining),
                residual: FractionRange(low: number(residualLow)/100, high: number(residualHigh)/100),
                e85: FractionRange(low: number(pumpLow)/100, high: number(pumpHigh)/100),
                sp98: FractionRange(low: 0, high: 0.05), target: number(target)/100))
        }
    }
    private func format(_ value: Double) -> String { String(format: "%.2f", locale: Locale(identifier: "en_US"), value) }
    private var summary: String {
        switch calculation {
        case .failure(let error): return error.localizedDescription
        case .success(let result):
            if !result.feasible {
                return "Ceiling cannot be guaranteed: even after adding only SP98, the upper bound is \(format(result.minimumUpper*100))%. No E85 volume calculated."
            }
            return "Simulation : E85 \(format(result.e85Liters ?? 0)) L ; SP98 \(format(result.sp98Liters ?? 0)) L ; final ethanol between \(format(result.final.low*100)) and \(format(result.final.high*100)) %."
        }
    }
    var body: some View {
        NavigationStack {
            Form {
                Section {
                    Text("Blend calculation • simulation").font(.headline)
                    Text("No blend guaranteeing no engine warning light is established.").fontWeight(.semibold)
                    Text("This calculation describes a blend. It does not validate vehicle compatibility or ECU calibration.")
                }
                Section("Volumes") {
                    Button("Scenario: 2 bars out of 6 (estimate)") {
                        finalVolume = "35"; remaining = "11.67"; residualLow = "0"; residualHigh = "85"
                        target = "10"; estimated = true; confirmed = false
                    }
                    field("Simulated final volume (L)", $finalVolume)
                    field("Remaining volume (L)", $remaining)
                    Toggle("The remaining volume is estimated", isOn: $estimated)
                    Text(estimated ? "Gauge bars do not measure litres. The calculation remains conditional."
                        : "The final volume must match the actual volume used for the calculation.").font(.footnote)
                }
                Section("Remaining fuel") {
                    field("Minimum ethanol (%)", $residualLow)
                    field("Maximum ethanol (%)", $residualHigh)
                    Button("Remaining fuel consists only of E5") {
                        residualLow = "0"; residualHigh = "5"; confirmed = false
                    }
                }
                Section("Added fuels") {
                    field("Pump E85 min. (%)", $pumpLow)
                    field("Pump E85 max. (%)", $pumpHigh)
                    Text("54% is a conservative theoretical pure-ethanol lower bound: the annex bounds ethanol plus higher alcohols, which may reach 6%. SP98 is modelled at 0–5%.").font(.footnote)
                }
                Section("Selected ceiling") {
                    field("Maximum final ethanol (%)", $target)
                    if (BlendEngine.parseDecimal(target) ?? 0) > 10 {
                        Text("Target above E10: vehicle-specific validation is required.").foregroundStyle(.red)
                    }
                    Button("Calculate the simulation") { editing = false; confirmed = true }
                }
                if confirmed {
                    Section("Conditional result") {
                        Text(summary).font(.headline)
                        if case .success(let result) = calculation {
                            Text("Additional volume in this scenario : \(format(result.additionLiters)) L.")
                            if result.feasible {
                                Text("E85 is rounded down to 0.01 L. SP98 is the remainder; its display is rounded. Do not exceed the first automatic pump shut-off.").font(.footnote)
                            }
                            if result.limitedBySpace { Text("Available space limits the addition.") }
                        }
                        ShareLink(item: summary + "\nCalcul conditionnel, aucune garantie d’absence de voyant moteur.") {
                            Label("Share", systemImage: "square.and.arrow.up")
                        }
                    }
                }
                Section("Data and sources") {
                    Text("Assumptions are saved on this device. No account or OBD connection. Report checked on 4 October 2026.").font(.footnote)
                    Link("Fuels: French ecology ministry", destination: URL(string: "https://www.ecologie.gouv.fr/politiques-publiques/carburants-combustibles-autorises-france")!)
                    Link("E85 specifications: Legifrance", destination: URL(string: "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000245613/")!)
                }
            }
            .navigationTitle("Aygo Blend")
            .tint(Color(red: 0, green: 0.41, blue: 0.36))
            .toolbar { ToolbarItemGroup(placement: .keyboard) { Spacer(); Button("Done") { editing = false } } }
        }
    }
    private func field(_ label: String, _ value: Binding<String>) -> some View {
        VStack(alignment: .leading, spacing: 5) {
            Text(label).font(.caption).foregroundStyle(.secondary)
            TextField(label, text: value).keyboardType(.decimalPad).focused($editing)
        }
        .onChange(of: value.wrappedValue) { _ in confirmed = false }
    }
}
