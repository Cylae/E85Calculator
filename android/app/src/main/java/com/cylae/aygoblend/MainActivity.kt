package com.cylae.aygoblend

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import java.util.Locale

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme(colorScheme = lightColorScheme(primary = Color(0xFF00685C),
                surface = Color(0xFFF6F8F7), secondary = Color(0xFF52655E))) {
                Surface(modifier = Modifier.fillMaxSize()) { BlendScreen() }
            }
        }
    }

    @Composable
    private fun BlendScreen() {
        val prefs = remember { getSharedPreferences("blend-v1", MODE_PRIVATE) }
        var finalVolume by rememberSaveable { mutableStateOf(prefs.getString("final", "35") ?: "35") }
        var remaining by rememberSaveable { mutableStateOf(prefs.getString("remaining", "11,67") ?: "11,67") }
        var residualLow by rememberSaveable { mutableStateOf(prefs.getString("rLow", "0") ?: "0") }
        var residualHigh by rememberSaveable { mutableStateOf(prefs.getString("rHigh", "85") ?: "85") }
        var pumpLow by rememberSaveable { mutableStateOf(prefs.getString("pLow", "54") ?: "54") }
        var pumpHigh by rememberSaveable { mutableStateOf(prefs.getString("pHigh", "85") ?: "85") }
        var target by rememberSaveable { mutableStateOf(prefs.getString("target", "10") ?: "10") }
        var estimated by rememberSaveable { mutableStateOf(prefs.getBoolean("estimated", true)) }
        var confirmed by rememberSaveable { mutableStateOf(false) }
        fun number(text: String) = BlendEngine.parseDecimal(text) ?: error("Renseignez tous les champs avec un nombre valide.")
        val computation = runCatching {
            BlendEngine.calculate(BlendInput(number(finalVolume), number(remaining),
                FractionRange(number(residualLow)/100, number(residualHigh)/100),
                FractionRange(number(pumpLow)/100, number(pumpHigh)/100), FractionRange(0.0, .05), number(target)/100))
        }
        val result = computation.getOrNull()
        fun format(value: Double) = String.format(Locale.FRANCE, "%.2f", value)
        val summary = when {
            result == null -> computation.exceptionOrNull()?.message ?: "Entrées invalides."
            !result.feasible -> "Plafond non garanti : même avec uniquement du SP98 ajouté, la borne haute est ${format(result.minimumUpper*100)} %. Aucun volume E85 calculé."
            else -> "Simulation : E85 ${format(result.e85Liters ?: 0.0)} L ; SP98 ${format(result.sp98Liters ?: 0.0)} L ; teneur finale entre ${format(result.final.low*100)} et ${format(result.final.high*100)} %."
        }
        Column(Modifier.fillMaxSize().safeDrawingPadding().verticalScroll(rememberScrollState()).imePadding()
            .padding(horizontal = 20.dp, vertical = 32.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text("Aygo Blend", style = MaterialTheme.typography.headlineLarge)
            Text("Calcul de mélange • simulation", style = MaterialTheme.typography.titleMedium)
            Card {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Aucun ratio sans voyant moteur n’est établi.", style = MaterialTheme.typography.titleMedium)
                    Text("Ce résultat décrit un mélange. Il ne valide ni la compatibilité de votre véhicule, ni sa calibration moteur.")
                }
            }
            Button(onClick = {
                finalVolume = "35"; remaining = "11,67"; residualLow = "0"; residualHigh = "85"
                target = "10"; estimated = true; confirmed = false
            }, modifier = Modifier.fillMaxWidth()) { Text("Scénario : 2 crans sur 6 (estimation)") }
            NumericField("Volume final simulé (L)", finalVolume) { finalVolume = it; confirmed = false }
            NumericField("Volume restant (L)", remaining) { remaining = it; confirmed = false }
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                NumericField("Restant min. (%)", residualLow, Modifier.weight(1f)) { residualLow = it; confirmed = false }
                NumericField("Restant max. (%)", residualHigh, Modifier.weight(1f)) { residualHigh = it; confirmed = false }
            }
            TextButton(onClick = { residualLow = "0"; residualHigh = "5"; confirmed = false }) {
                Text("Restant composé uniquement de carburant E5")
            }
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                NumericField("Pompe E85 min. (%)", pumpLow, Modifier.weight(1f)) { pumpLow = it; confirmed = false }
                NumericField("Pompe E85 max. (%)", pumpHigh, Modifier.weight(1f)) { pumpHigh = it; confirmed = false }
            }
            Text("54 % est une borne théorique prudente pour l’éthanol pur : l’annexe réglementaire borne la somme éthanol + alcools supérieurs, ces derniers pouvant atteindre 6 %. SP98 modélisé entre 0 et 5 %.", style = MaterialTheme.typography.bodySmall)
            NumericField("Plafond d’éthanol choisi (%)", target) { target = it; confirmed = false }
            Row {
                Checkbox(estimated, onCheckedChange = { estimated = it; confirmed = false })
                Text("Le volume restant est estimé", Modifier.padding(top = 12.dp))
            }
            Text(if (estimated) "Les crans ne mesurent pas les litres. Le calcul reste conditionnel."
                else "Le volume final saisi doit correspondre au volume réel retenu pour le calcul.")
            if ((BlendEngine.parseDecimal(target) ?: 0.0) > 10) Text("Objectif au-delà de l’E10 : validation spécifique du véhicule nécessaire.", color = MaterialTheme.colorScheme.error)
            Button(onClick = { confirmed = true }, modifier = Modifier.fillMaxWidth()) { Text("Calculer la simulation") }
            if (confirmed) {
                Card {
                    Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(summary, style = MaterialTheme.typography.titleMedium)
                        if (result != null) {
                            Text("Volume à compléter dans ce scénario : ${format(result.additionLiters)} L.")
                            if (result.feasible) Text("E85 arrondi vers le bas au centilitre. Le SP98 est le complément ; affichage arrondi. Ne dépassez pas le premier arrêt automatique de la pompe.")
                            if (result.limitedBySpace) Text("Le volume disponible limite l’ajout : le plafond choisi n’est pas nécessairement atteint.")
                        }
                    }
                }
                OutlinedButton(onClick = {
                    startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).apply {
                        type = "text/plain"; putExtra(Intent.EXTRA_TEXT, summary + "\nCalcul conditionnel, aucune garantie d’absence de voyant moteur.")
                    }, "Partager la simulation"))
                }, modifier = Modifier.fillMaxWidth()) { Text("Partager") }
            }
            OutlinedButton(onClick = {
                prefs.edit().putString("final", finalVolume).putString("remaining", remaining)
                    .putString("rLow", residualLow).putString("rHigh", residualHigh)
                    .putString("pLow", pumpLow).putString("pHigh", pumpHigh)
                    .putString("target", target).putBoolean("estimated", estimated).apply()
            }, modifier = Modifier.fillMaxWidth()) { Text("Mémoriser les hypothèses sur cet appareil") }
            Text("Sources : Toyota (Aygo 2014, 35 L), ministère chargé de l’écologie (E5/E10), arrêté du 28 décembre 2006 consolidé au 4 octobre 2026. Voir le rapport pour les liens et limites.", style = MaterialTheme.typography.bodySmall)
        }
    }
}

@Composable
private fun NumericField(label: String, value: String, modifier: Modifier = Modifier, onChange: (String) -> Unit) {
    OutlinedTextField(value = value, onValueChange = onChange, label = { Text(label) },
        modifier = modifier.fillMaxWidth(), singleLine = true,
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal))
}
