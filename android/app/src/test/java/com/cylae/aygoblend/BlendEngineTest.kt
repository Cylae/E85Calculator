package com.cylae.aygoblend
import org.junit.Assert.*
import org.junit.Test

class BlendEngineTest {
    @Test fun case00() {
        val input = BlendInput(35.0, 11.666666666666666, FractionRange(0.05, 0.05), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), 0.3)
        val result = BlendEngine.calculate(input)
        assertEquals(true, result.feasible)
        assertEquals(10.9375, result.exactE85Liters!!, 1e-8)
        assertEquals(10.93, result.e85Liters!!, 1e-8)
        assertEquals(12.403333333333332, result.sp98Liters!!, 1e-8)
        assertEquals(0.05, result.minimumUpper, 1e-8)
    }
    @Test fun case01() {
        val input = BlendInput(35.0, 11.666666666666666, FractionRange(0.5, 0.5), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), 0.3)
        val result = BlendEngine.calculate(input)
        assertEquals(true, result.feasible)
        assertEquals(4.375, result.exactE85Liters!!, 1e-8)
        assertEquals(4.37, result.e85Liters!!, 1e-8)
        assertEquals(18.96333333333333, result.sp98Liters!!, 1e-8)
        assertEquals(0.2, result.minimumUpper, 1e-8)
    }
    @Test fun case02() {
        val input = BlendInput(35.0, 11.666666666666666, FractionRange(0.85, 0.85), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), 0.3)
        val result = BlendEngine.calculate(input)
        assertEquals(false, result.feasible)
        assertNull(result.exactE85Liters)
        assertNull(result.e85Liters)
        assertNull(result.sp98Liters)
        assertEquals(0.31666666666666665, result.minimumUpper, 1e-8)
    }
    @Test fun case03() {
        val input = BlendInput(35.0, 11.666666666666666, FractionRange(0.0, 0.85), FractionRange(0.54, 0.85), FractionRange(0.0, 0.05), 0.1)
        val result = BlendEngine.calculate(input)
        assertEquals(false, result.feasible)
        assertNull(result.exactE85Liters)
        assertNull(result.e85Liters)
        assertNull(result.sp98Liters)
        assertEquals(0.31666666666666665, result.minimumUpper, 1e-8)
    }
    @Test fun case04() {
        val input = BlendInput(35.0, 11.666666666666666, FractionRange(0.05, 0.05), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), 0.1)
        val result = BlendEngine.calculate(input)
        assertEquals(true, result.feasible)
        assertEquals(2.1875, result.exactE85Liters!!, 1e-8)
        assertEquals(2.18, result.e85Liters!!, 1e-8)
        assertEquals(21.153333333333332, result.sp98Liters!!, 1e-8)
        assertEquals(0.05, result.minimumUpper, 1e-8)
    }
    @Test fun case05() {
        val input = BlendInput(35.0, 0.0, FractionRange(0.05, 0.05), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), 0.3)
        val result = BlendEngine.calculate(input)
        assertEquals(true, result.feasible)
        assertEquals(10.9375, result.exactE85Liters!!, 1e-8)
        assertEquals(10.93, result.e85Liters!!, 1e-8)
        assertEquals(24.07, result.sp98Liters!!, 1e-8)
        assertEquals(0.05, result.minimumUpper, 1e-8)
    }
    @Test fun case06() {
        val input = BlendInput(35.0, 0.0, FractionRange(0.05, 0.05), FractionRange(0.54, 0.85), FractionRange(0.0, 0.05), 1.0)
        val result = BlendEngine.calculate(input)
        assertEquals(true, result.feasible)
        assertEquals(35.0, result.exactE85Liters!!, 1e-8)
        assertEquals(35.0, result.e85Liters!!, 1e-8)
        assertEquals(0.0, result.sp98Liters!!, 1e-8)
        assertEquals(0.05, result.minimumUpper, 1e-8)
    }
    @Test fun case07() {
        val input = BlendInput(35.0, 35.0, FractionRange(0.05, 0.05), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), 0.1)
        val result = BlendEngine.calculate(input)
        assertEquals(true, result.feasible)
        assertEquals(0.0, result.exactE85Liters!!, 1e-8)
        assertEquals(0.0, result.e85Liters!!, 1e-8)
        assertEquals(0.0, result.sp98Liters!!, 1e-8)
        assertEquals(0.05, result.minimumUpper, 1e-8)
    }
    @Test fun case08() {
        val input = BlendInput(35.0, 11.666666666666666, FractionRange(0.05, 0.05), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), 0.05)
        val result = BlendEngine.calculate(input)
        assertEquals(true, result.feasible)
        assertEquals(0.0, result.exactE85Liters!!, 1e-8)
        assertEquals(0.0, result.e85Liters!!, 1e-8)
        assertEquals(23.333333333333332, result.sp98Liters!!, 1e-8)
        assertEquals(0.05, result.minimumUpper, 1e-8)
    }
    @Test fun case09() {
        val input = BlendInput(35.0, 0.0, FractionRange(0.0, 0.0), FractionRange(0.85, 0.85), FractionRange(0.0, 0.0), 0.0)
        val result = BlendEngine.calculate(input)
        assertEquals(true, result.feasible)
        assertEquals(0.0, result.exactE85Liters!!, 1e-8)
        assertEquals(0.0, result.e85Liters!!, 1e-8)
        assertEquals(35.0, result.sp98Liters!!, 1e-8)
        assertEquals(0.0, result.minimumUpper, 1e-8)
    }
    @Test fun case10() {
        val input = BlendInput(35.0, 36.0, FractionRange(0.05, 0.05), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), 0.3)
        assertThrows(IllegalArgumentException::class.java) { BlendEngine.calculate(input) }
    }
    @Test fun case11() {
        val input = BlendInput(0.0, 0.0, FractionRange(0.05, 0.05), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), 0.3)
        assertThrows(IllegalArgumentException::class.java) { BlendEngine.calculate(input) }
    }
    @Test fun case12() {
        val input = BlendInput(35.0, -1.0, FractionRange(0.05, 0.05), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), 0.3)
        assertThrows(IllegalArgumentException::class.java) { BlendEngine.calculate(input) }
    }
    @Test fun case13() {
        val input = BlendInput(35.0, 11.666666666666666, FractionRange(0.5, 0.4), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), 0.3)
        assertThrows(IllegalArgumentException::class.java) { BlendEngine.calculate(input) }
    }
    @Test fun case14() {
        val input = BlendInput(35.0, 11.666666666666666, FractionRange(0.05, 1.1), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), 0.3)
        assertThrows(IllegalArgumentException::class.java) { BlendEngine.calculate(input) }
    }
    @Test fun case15() {
        val input = BlendInput(35.0, 11.666666666666666, FractionRange(0.05, 0.05), FractionRange(0.05, 0.05), FractionRange(0.05, 0.05), 0.3)
        assertThrows(IllegalArgumentException::class.java) { BlendEngine.calculate(input) }
    }
    @Test fun case16() {
        val input = BlendInput(35.0, 11.666666666666666, FractionRange(0.05, 0.05), FractionRange(0.01, 0.85), FractionRange(0.05, 0.05), 0.3)
        assertThrows(IllegalArgumentException::class.java) { BlendEngine.calculate(input) }
    }
    @Test fun case17() {
        val input = BlendInput(35.0, 11.666666666666666, FractionRange(0.05, 0.05), FractionRange(0.85, 0.85), FractionRange(0.05, 0.05), -0.1)
        assertThrows(IllegalArgumentException::class.java) { BlendEngine.calculate(input) }
    }
    @Test fun decimalParsing() {
        assertEquals(1.25, BlendEngine.parseDecimal("1,25")!!, 1e-12)
        for (s in listOf("", "NaN", "Infinity", "1e4", "1,2.3", "0x10")) assertNull(BlendEngine.parseDecimal(s))
    }
    @Test fun rejectsNonFinite() {
        val bad = BlendInput(Double.NaN, 0.0, FractionRange(0.0,0.0), FractionRange(.54,.85), FractionRange(0.0,.05), .1)
        assertThrows(IllegalArgumentException::class.java) { BlendEngine.calculate(bad) }
    }
}
