package com.cylae.aygoblend

import kotlin.math.floor
import kotlin.math.max
import kotlin.math.min

data class FractionRange(val low: Double, val high: Double)
data class BlendInput(
    val finalLiters: Double,
    val remainingLiters: Double,
    val residual: FractionRange,
    val e85: FractionRange,
    val sp98: FractionRange,
    val target: Double,
)
data class BlendOutput(
    val feasible: Boolean,
    val additionLiters: Double,
    val exactE85Liters: Double?,
    val e85Liters: Double?,
    val sp98Liters: Double?,
    val final: FractionRange,
    val minimumUpper: Double,
    val limitedBySpace: Boolean,
)

object BlendEngine {
    fun parseDecimal(text: String): Double? {
        val value = text.trim().replace(',', '.')
        if (!Regex("^[+-]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)$").matches(value)) return null
        return value.toDoubleOrNull()?.takeIf { it.isFinite() }
    }
    fun calculate(input: BlendInput): BlendOutput {
        val c = input.finalLiters
        val r = input.remainingLiters
        val target = input.target
        require(c.isFinite() && r.isFinite() && target.isFinite() && c > 0 &&
            r >= 0 && r <= c && target >= 0 && target <= 1) { "Volumes ou plafond invalides." }
        for ((range, name) in listOf(input.residual to "Restant", input.e85 to "E85", input.sp98 to "SP98")) {
            require(range.low.isFinite() && range.high.isFinite() && range.low >= 0 &&
                range.high <= 1 && range.low <= range.high) { "$name : bornes invalides." }
        }
        require(input.e85.low >= input.sp98.high && input.e85.high > input.sp98.high) {
            "La plage E85 doit être au-dessus de la plage SP98."
        }
        val addition = c - r
        fun interval(x: Double): FractionRange {
            val y = addition - x
            return FractionRange(
                (r * input.residual.low + x * input.e85.low + y * input.sp98.low) / c,
                (r * input.residual.high + x * input.e85.high + y * input.sp98.high) / c,
            )
        }
        val baseline = interval(0.0)
        if (baseline.high > target + 1e-12) {
            return BlendOutput(false, addition, null, null, null, baseline, baseline.high, false)
        }
        val theoretical = (c * target - r * input.residual.high - addition * input.sp98.high) /
            (input.e85.high - input.sp98.high)
        val exact = max(0.0, min(addition, theoretical))
        var x = min(addition, floor(exact * 100 + 1e-9) / 100)
        if (interval(x).high > target + 1e-12) x = max(0.0, x - 0.01)
        return BlendOutput(true, addition, exact, x, addition - x, interval(x),
            baseline.high, theoretical >= addition - 1e-12)
    }
}
