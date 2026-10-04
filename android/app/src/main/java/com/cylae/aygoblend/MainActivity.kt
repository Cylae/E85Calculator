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
        var remaining by rememberSaveable { mutableStateOf(prefs.getString("remaining", "11.67") ?: "11.67") }
        var residualLow by rememberSaveable { mutableStateOf(prefs.getString("rLow", "0") ?: "0") }
        var residualHigh by rememberSaveable { mutableStateOf(prefs.getString("rHigh", "85") ?: "85") }
        var pumpLow by rememberSaveable { mutableStateOf(prefs.getString("pLow", "54") ?: "54") }
        var pumpHigh by rememberSaveable { mutableStateOf(prefs.getString("pHigh", "85") ?: "85") }
        var target by rememberSaveable { mutableStateOf(prefs.getString("target", "10") ?: "10") }
        var estimated by rememberSaveable { mutableStateOf(prefs.getBoolean("estimated", true)) }
        var confirmed by rememberSaveable { mutableStateOf(false) }
        fun number(text: String) = BlendEngine.parseDecimal(text) ?: error("Enter a valid number in every field.")
        val computation = runCatching {
            BlendEngine.calculate(BlendInput(number(finalVolume), number(remaining),
                FractionRange(number(residualLow)/100, number(residualHigh)/100),
                FractionRange(number(pumpLow)/100, number(pumpHigh)/100), FractionRange(0.0, .05), number(target)/100))
        }
        val result = computation.getOrNull()
        fun format(value: Double) = String.format(Locale.US, "%.2f", value)
        val summary = when {
            result == null -> computation.exceptionOrNull()?.message ?: "Invalid input."
            !result.feasible -> "Ceiling cannot be guaranteed: even after adding only SP98, the upper bound is ${format(result.minimumUpper*100)}%. No E85 volume calculated."
            else -> "Simulation : E85 ${format(result.e85Liters ?: 0.0)} L ; SP98 ${format(result.sp98Liters ?: 0.0)} L ; final ethanol between ${format(result.final.low*100)} and ${format(result.final.high*100)} %."
        }
        Column(Modifier.fillMaxSize().safeDrawingPadding().verticalScroll(rememberScrollState()).imePadding()
            .padding(horizontal = 20.dp, vertical = 32.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text("Aygo Blend", style = MaterialTheme.typography.headlineLarge)
            Text("Blend calculation • simulation", style = MaterialTheme.typography.titleMedium)
            Card {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("No blend guaranteeing no engine warning light is established.", style = MaterialTheme.typography.titleMedium)
                    Text("This result describes a blend. It does not validate vehicle compatibility or ECU calibration.")
                }
            }
            Button(onClick = {
                finalVolume = "35"; remaining = "11.67"; residualLow = "0"; residualHigh = "85"
                target = "10"; estimated = true; confirmed = false
            }, modifier = Modifier.fillMaxWidth()) { Text("Scenario: 2 bars out of 6 (estimate)") }
            NumericField("Simulated final volume (L)", finalVolume) { finalVolume = it; confirmed = false }
            NumericField("Remaining volume (L)", remaining) { remaining = it; confirmed = false }
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                NumericField("Remaining fuel min. (%)", residualLow, Modifier.weight(1f)) { residualLow = it; confirmed = false }
                NumericField("Remaining fuel max. (%)", residualHigh, Modifier.weight(1f)) { residualHigh = it; confirmed = false }
            }
            TextButton(onClick = { residualLow = "0"; residualHigh = "5"; confirmed = false }) {
                Text("Remaining fuel consists only of E5")
            }
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                NumericField("Pump E85 min. (%)", pumpLow, Modifier.weight(1f)) { pumpLow = it; confirmed = false }
                NumericField("Pump E85 max. (%)", pumpHigh, Modifier.weight(1f)) { pumpHigh = it; confirmed = false }
            }
            Text("54% is a conservative theoretical pure-ethanol lower bound: the regulatory annex bounds ethanol plus higher alcohols, which may reach 6%. SP98 is modelled at 0–5%.", style = MaterialTheme.typography.bodySmall)
            NumericField("Selected ethanol ceiling (%)", target) { target = it; confirmed = false }
            Row {
                Checkbox(estimated, onCheckedChange = { estimated = it; confirmed = false })
                Text("The remaining volume is estimated", Modifier.padding(top = 12.dp))
            }
            Text(if (estimated) "Gauge bars do not measure litres. The calculation remains conditional."
                else "The final volume must match the actual volume used for the calculation.")
            if ((BlendEngine.parseDecimal(target) ?: 0.0) > 10) Text("Target above E10: vehicle-specific validation is required.", color = MaterialTheme.colorScheme.error)
            Button(onClick = { confirmed = true }, modifier = Modifier.fillMaxWidth()) { Text("Calculate the simulation") }
            if (confirmed) {
                Card {
                    Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(summary, style = MaterialTheme.typography.titleMedium)
                        if (result != null) {
                            Text("Additional volume in this scenario : ${format(result.additionLiters)} L.")
                            if (result.feasible) Text("E85 is rounded down to 0.01 L. SP98 is the remainder; its display is rounded. Do not exceed the first automatic pump shut-off.")
                            if (result.limitedBySpace) Text("Available space limits the addition: the selected ceiling may not be reached.")
                        }
                    }
                }
                OutlinedButton(onClick = {
                    startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).apply {
                        type = "text/plain"; putExtra(Intent.EXTRA_TEXT, summary + "\nCalcul conditionnel, aucune garantie d’absence de voyant moteur.")
                    }, "Share simulation"))
                }, modifier = Modifier.fillMaxWidth()) { Text("Share") }
            }
            OutlinedButton(onClick = {
                prefs.edit().putString("final", finalVolume).putString("remaining", remaining)
                    .putString("rLow", residualLow).putString("rHigh", residualHigh)
                    .putString("pLow", pumpLow).putString("pHigh", pumpHigh)
                    .putString("target", target).putBoolean("estimated", estimated).apply()
            }, modifier = Modifier.fillMaxWidth()) { Text("Save assumptions on this device") }
            Text("Sources: Toyota (2014 Aygo, 35 L), French ecology ministry (E5/E10), fuel order of 28 December 2006 consolidated on 4 October 2026. See the report for links and limitations.", style = MaterialTheme.typography.bodySmall)
        }
    }
}

@Composable
private fun NumericField(label: String, value: String, modifier: Modifier = Modifier, onChange: (String) -> Unit) {
    OutlinedTextField(value = value, onValueChange = onChange, label = { Text(label) },
        modifier = modifier.fillMaxWidth(), singleLine = true,
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal))
}
