import Foundation

struct FractionRange {
    let low: Double
    let high: Double
}
struct BlendInput {
    let finalLiters: Double
    let remainingLiters: Double
    let residual: FractionRange
    let e85: FractionRange
    let sp98: FractionRange
    let target: Double
}
struct BlendOutput {
    let feasible: Bool
    let additionLiters: Double
    let exactE85Liters: Double?
    let e85Liters: Double?
    let sp98Liters: Double?
    let final: FractionRange
    let minimumUpper: Double
    let limitedBySpace: Bool
}
enum BlendError: LocalizedError {
    case invalid(String)
    var errorDescription: String? {
        switch self { case .invalid(let message): return message }
    }
}
enum BlendEngine {
    static func parseDecimal(_ text: String) -> Double? {
        let s = text.trimmingCharacters(in: .whitespacesAndNewlines).replacingOccurrences(of: ",", with: ".")
        guard s.range(of: #"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$"#, options: .regularExpression) != nil,
              let value = Double(s), value.isFinite else { return nil }
        return value
    }
    static func calculate(_ input: BlendInput) throws -> BlendOutput {
        let c = input.finalLiters, r = input.remainingLiters, t = input.target
        guard c.isFinite, r.isFinite, t.isFinite, c > 0, r >= 0, r <= c, t >= 0, t <= 1 else {
            throw BlendError.invalid("Invalid volumes or ceiling.")
        }
        for (range, name) in [(input.residual, "Remaining fuel"), (input.e85, "E85"), (input.sp98, "SP98")] {
            guard range.low.isFinite, range.high.isFinite, range.low >= 0,
                  range.high <= 1, range.low <= range.high else {
                throw BlendError.invalid("\(name): invalid bounds.")
            }
        }
        guard input.e85.low >= input.sp98.high, input.e85.high > input.sp98.high else {
            throw BlendError.invalid("The E85 interval must be above the SP98 interval.")
        }
        let addition = c - r
        func interval(_ x: Double) -> FractionRange {
            let y = addition - x
            return FractionRange(
                low: (r * input.residual.low + x * input.e85.low + y * input.sp98.low) / c,
                high: (r * input.residual.high + x * input.e85.high + y * input.sp98.high) / c)
        }
        let baseline = interval(0)
        guard baseline.high <= t + 1e-12 else {
            return BlendOutput(feasible: false, additionLiters: addition, exactE85Liters: nil,
                e85Liters: nil, sp98Liters: nil, final: baseline, minimumUpper: baseline.high, limitedBySpace: false)
        }
        let theoretical = (c * t - r * input.residual.high - addition * input.sp98.high) /
            (input.e85.high - input.sp98.high)
        let exact = max(0, min(addition, theoretical))
        var x = min(addition, floor(exact * 100 + 1e-9) / 100)
        if interval(x).high > t + 1e-12 { x = max(0, x - 0.01) }
        return BlendOutput(feasible: true, additionLiters: addition, exactE85Liters: exact,
            e85Liters: x, sp98Liters: addition - x, final: interval(x),
            minimumUpper: baseline.high, limitedBySpace: theoretical >= addition - 1e-12)
    }
}
