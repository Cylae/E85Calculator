import SwiftUI

struct ContentView: View {
    @AppStorage("final") private var finalVolume = "35"
    @AppStorage("remaining") private var remaining = "11,67"
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
            throw BlendError.invalid("Renseignez tous les champs avec un nombre valide.")
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
    private func format(_ value: Double) -> String { String(format: "%.2f", locale: Locale(identifier: "fr_FR"), value) }
    private var summary: String {
        switch calculation {
        case .failure(let error): return error.localizedDescription
        case .success(let result):
            if !result.feasible {
                return "Plafond non garanti : même avec uniquement du SP98 ajouté, la borne haute est \(format(result.minimumUpper*100)) %. Aucun volume E85 calculé."
            }
            return "Simulation : E85 \(format(result.e85Liters ?? 0)) L ; SP98 \(format(result.sp98Liters ?? 0)) L ; teneur finale entre \(format(result.final.low*100)) et \(format(result.final.high*100)) %."
        }
    }
    var body: some View {
        NavigationStack {
            Form {
                Section {
                    Text("Calcul de mélange • simulation").font(.headline)
                    Text("Aucun ratio sans voyant moteur n’est établi.").fontWeight(.semibold)
                    Text("Le calcul décrit un mélange. Il ne valide ni la compatibilité du véhicule, ni sa calibration moteur.")
                }
                Section("Volumes") {
                    Button("Scénario : 2 crans sur 6 (estimation)") {
                        finalVolume = "35"; remaining = "11,67"; residualLow = "0"; residualHigh = "85"
                        target = "10"; estimated = true; confirmed = false
                    }
                    field("Volume final simulé (L)", $finalVolume)
                    field("Volume restant (L)", $remaining)
                    Toggle("Le volume restant est estimé", isOn: $estimated)
                    Text(estimated ? "Les crans ne mesurent pas les litres. Le calcul reste conditionnel."
                        : "Le volume final saisi doit correspondre au volume réel retenu pour le calcul.").font(.footnote)
                }
                Section("Carburant restant") {
                    field("Éthanol minimum (%)", $residualLow)
                    field("Éthanol maximum (%)", $residualHigh)
                    Button("Restant composé uniquement de carburant E5") {
                        residualLow = "0"; residualHigh = "5"; confirmed = false
                    }
                }
                Section("Carburants ajoutés") {
                    field("Pompe E85 min. (%)", $pumpLow)
                    field("Pompe E85 max. (%)", $pumpHigh)
                    Text("54 % est une borne théorique prudente d’éthanol pur : l’annexe borne éthanol + alcools supérieurs, ces derniers pouvant atteindre 6 %. SP98 modélisé entre 0 et 5 %.").font(.footnote)
                }
                Section("Plafond choisi") {
                    field("Éthanol final maximum (%)", $target)
                    if (BlendEngine.parseDecimal(target) ?? 0) > 10 {
                        Text("Objectif au-delà de l’E10 : validation spécifique du véhicule nécessaire.").foregroundStyle(.red)
                    }
                    Button("Calculer la simulation") { editing = false; confirmed = true }
                }
                if confirmed {
                    Section("Résultat conditionnel") {
                        Text(summary).font(.headline)
                        if case .success(let result) = calculation {
                            Text("Volume à compléter dans ce scénario : \(format(result.additionLiters)) L.")
                            if result.feasible {
                                Text("E85 arrondi vers le bas au centilitre. Le SP98 est le complément ; affichage arrondi. Ne dépassez pas le premier arrêt automatique de la pompe.").font(.footnote)
                            }
                            if result.limitedBySpace { Text("Le volume disponible limite l’ajout.") }
                        }
                        ShareLink(item: summary + "\nCalcul conditionnel, aucune garantie d’absence de voyant moteur.") {
                            Label("Partager", systemImage: "square.and.arrow.up")
                        }
                    }
                }
                Section("Données et sources") {
                    Text("Hypothèses mémorisées sur cet appareil. Aucun compte et aucune connexion OBD. Rapport vérifié au 4 octobre 2026.").font(.footnote)
                    Link("Carburants : ministère chargé de l’écologie", destination: URL(string: "https://www.ecologie.gouv.fr/politiques-publiques/carburants-combustibles-autorises-france")!)
                    Link("Spécifications E85 : Légifrance", destination: URL(string: "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000245613/")!)
                }
            }
            .navigationTitle("Aygo Blend")
            .tint(Color(red: 0, green: 0.41, blue: 0.36))
            .toolbar { ToolbarItemGroup(placement: .keyboard) { Spacer(); Button("Terminé") { editing = false } } }
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
