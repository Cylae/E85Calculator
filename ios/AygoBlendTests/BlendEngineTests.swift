import XCTest
@testable import AygoBlend

final class BlendEngineTests: XCTestCase {
    func testCase00() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 11.666666666666666, residual: FractionRange(low: 0.05, high: 0.05), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.3)
        let result = try BlendEngine.calculate(input)
        XCTAssertEqual(result.feasible, true)
        XCTAssertEqual(try XCTUnwrap(result.exactE85Liters), 10.9375, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.e85Liters), 10.93, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.sp98Liters), 12.403333333333332, accuracy: 1e-8)
        XCTAssertEqual(result.minimumUpper, 0.05, accuracy: 1e-8)
    }
    func testCase01() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 11.666666666666666, residual: FractionRange(low: 0.5, high: 0.5), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.3)
        let result = try BlendEngine.calculate(input)
        XCTAssertEqual(result.feasible, true)
        XCTAssertEqual(try XCTUnwrap(result.exactE85Liters), 4.375, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.e85Liters), 4.37, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.sp98Liters), 18.96333333333333, accuracy: 1e-8)
        XCTAssertEqual(result.minimumUpper, 0.2, accuracy: 1e-8)
    }
    func testCase02() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 11.666666666666666, residual: FractionRange(low: 0.85, high: 0.85), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.3)
        let result = try BlendEngine.calculate(input)
        XCTAssertEqual(result.feasible, false)
        XCTAssertNil(result.exactE85Liters)
        XCTAssertNil(result.e85Liters)
        XCTAssertNil(result.sp98Liters)
        XCTAssertEqual(result.minimumUpper, 0.31666666666666665, accuracy: 1e-8)
    }
    func testCase03() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 11.666666666666666, residual: FractionRange(low: 0, high: 0.85), e85: FractionRange(low: 0.54, high: 0.85), sp98: FractionRange(low: 0, high: 0.05), target: 0.1)
        let result = try BlendEngine.calculate(input)
        XCTAssertEqual(result.feasible, false)
        XCTAssertNil(result.exactE85Liters)
        XCTAssertNil(result.e85Liters)
        XCTAssertNil(result.sp98Liters)
        XCTAssertEqual(result.minimumUpper, 0.31666666666666665, accuracy: 1e-8)
    }
    func testCase04() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 11.666666666666666, residual: FractionRange(low: 0.05, high: 0.05), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.1)
        let result = try BlendEngine.calculate(input)
        XCTAssertEqual(result.feasible, true)
        XCTAssertEqual(try XCTUnwrap(result.exactE85Liters), 2.1875, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.e85Liters), 2.18, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.sp98Liters), 21.153333333333332, accuracy: 1e-8)
        XCTAssertEqual(result.minimumUpper, 0.05, accuracy: 1e-8)
    }
    func testCase05() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 0, residual: FractionRange(low: 0.05, high: 0.05), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.3)
        let result = try BlendEngine.calculate(input)
        XCTAssertEqual(result.feasible, true)
        XCTAssertEqual(try XCTUnwrap(result.exactE85Liters), 10.9375, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.e85Liters), 10.93, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.sp98Liters), 24.07, accuracy: 1e-8)
        XCTAssertEqual(result.minimumUpper, 0.05, accuracy: 1e-8)
    }
    func testCase06() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 0, residual: FractionRange(low: 0.05, high: 0.05), e85: FractionRange(low: 0.54, high: 0.85), sp98: FractionRange(low: 0, high: 0.05), target: 1)
        let result = try BlendEngine.calculate(input)
        XCTAssertEqual(result.feasible, true)
        XCTAssertEqual(try XCTUnwrap(result.exactE85Liters), 35, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.e85Liters), 35, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.sp98Liters), 0, accuracy: 1e-8)
        XCTAssertEqual(result.minimumUpper, 0.05, accuracy: 1e-8)
    }
    func testCase07() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 35, residual: FractionRange(low: 0.05, high: 0.05), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.1)
        let result = try BlendEngine.calculate(input)
        XCTAssertEqual(result.feasible, true)
        XCTAssertEqual(try XCTUnwrap(result.exactE85Liters), 0, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.e85Liters), 0, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.sp98Liters), 0, accuracy: 1e-8)
        XCTAssertEqual(result.minimumUpper, 0.05, accuracy: 1e-8)
    }
    func testCase08() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 11.666666666666666, residual: FractionRange(low: 0.05, high: 0.05), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.05)
        let result = try BlendEngine.calculate(input)
        XCTAssertEqual(result.feasible, true)
        XCTAssertEqual(try XCTUnwrap(result.exactE85Liters), 0, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.e85Liters), 0, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.sp98Liters), 23.333333333333332, accuracy: 1e-8)
        XCTAssertEqual(result.minimumUpper, 0.05, accuracy: 1e-8)
    }
    func testCase09() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 0, residual: FractionRange(low: 0, high: 0), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0, high: 0), target: 0)
        let result = try BlendEngine.calculate(input)
        XCTAssertEqual(result.feasible, true)
        XCTAssertEqual(try XCTUnwrap(result.exactE85Liters), 0, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.e85Liters), 0, accuracy: 1e-8)
        XCTAssertEqual(try XCTUnwrap(result.sp98Liters), 35, accuracy: 1e-8)
        XCTAssertEqual(result.minimumUpper, 0, accuracy: 1e-8)
    }
    func testCase10() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 36, residual: FractionRange(low: 0.05, high: 0.05), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.3)
        XCTAssertThrowsError(try BlendEngine.calculate(input))
    }
    func testCase11() throws {
        let input = BlendInput(finalLiters: 0, remainingLiters: 0, residual: FractionRange(low: 0.05, high: 0.05), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.3)
        XCTAssertThrowsError(try BlendEngine.calculate(input))
    }
    func testCase12() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: -1, residual: FractionRange(low: 0.05, high: 0.05), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.3)
        XCTAssertThrowsError(try BlendEngine.calculate(input))
    }
    func testCase13() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 11.666666666666666, residual: FractionRange(low: 0.5, high: 0.4), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.3)
        XCTAssertThrowsError(try BlendEngine.calculate(input))
    }
    func testCase14() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 11.666666666666666, residual: FractionRange(low: 0.05, high: 1.1), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.3)
        XCTAssertThrowsError(try BlendEngine.calculate(input))
    }
    func testCase15() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 11.666666666666666, residual: FractionRange(low: 0.05, high: 0.05), e85: FractionRange(low: 0.05, high: 0.05), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.3)
        XCTAssertThrowsError(try BlendEngine.calculate(input))
    }
    func testCase16() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 11.666666666666666, residual: FractionRange(low: 0.05, high: 0.05), e85: FractionRange(low: 0.01, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: 0.3)
        XCTAssertThrowsError(try BlendEngine.calculate(input))
    }
    func testCase17() throws {
        let input = BlendInput(finalLiters: 35, remainingLiters: 11.666666666666666, residual: FractionRange(low: 0.05, high: 0.05), e85: FractionRange(low: 0.85, high: 0.85), sp98: FractionRange(low: 0.05, high: 0.05), target: -0.1)
        XCTAssertThrowsError(try BlendEngine.calculate(input))
    }
    func testDecimalParsing() {
        XCTAssertEqual(BlendEngine.parseDecimal("1,25"), 1.25)
        for s in ["", "NaN", "Infinity", "1e4", "1,2.3", "0x10"] { XCTAssertNil(BlendEngine.parseDecimal(s)) }
    }
    func testNonFinite() {
        let bad = BlendInput(finalLiters: .nan, remainingLiters: 0, residual: FractionRange(low:0,high:0),
            e85: FractionRange(low:0.54,high:0.85), sp98: FractionRange(low:0,high:0.05), target:0.1)
        XCTAssertThrowsError(try BlendEngine.calculate(bad))
    }
}
