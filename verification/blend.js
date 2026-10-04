(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.FuelBlend = api;
})(typeof globalThis === 'object' ? globalThis : this, function () {
  'use strict';
  function parseDecimal(text) {
    const s = String(text).trim().replace(',', '.');
    if (!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(s)) return null;
    const n = Number(s);
    return Number.isFinite(n) ? n : null;
  }
  function validateRange(r, name) {
    if (!r || !Number.isFinite(r.low) || !Number.isFinite(r.high) ||
        r.low < 0 || r.high > 1 || r.low > r.high) {
      throw new Error(name + ' : bornes attendues entre 0 et 100 %, dans cet ordre.');
    }
  }
  function calculate(input) {
    const { finalLiters: c, remainingLiters: r, residual, e85, sp98, target } = input;
    if (![c, r, target].every(Number.isFinite) || c <= 0 || r < 0 || r > c || target < 0 || target > 1)
      throw new Error('Volumes ou plafond invalides. Le volume final doit être positif et supérieur ou égal au restant.');
    validateRange(residual, 'Carburant restant');
    validateRange(e85, 'E85');
    validateRange(sp98, 'SP98');
    if (e85.low < sp98.high || e85.high <= sp98.high)
      throw new Error('La plage E85 doit être au-dessus de la plage SP98.');
    const addition = c - r;
    function interval(x) {
      const y = addition - x;
      return {
        low: (r * residual.low + x * e85.low + y * sp98.low) / c,
        high: (r * residual.high + x * e85.high + y * sp98.high) / c
      };
    }
    const baseline = interval(0);
    if (baseline.high > target + 1e-12) {
      return { feasible: false, additionLiters: addition, exactE85Liters: null,
        e85Liters: null, sp98Liters: null, final: baseline,
        minimumUpper: baseline.high, limitedBySpace: false };
    }
    const theoretical = (c * target - r * residual.high - addition * sp98.high) /
      (e85.high - sp98.high);
    const exact = Math.max(0, Math.min(addition, theoretical));
    let x = Math.min(addition, Math.floor(exact * 100 + 1e-9) / 100);
    // Numerical rounding must never increase the modeled upper bound above the ceiling.
    if (interval(x).high > target + 1e-12) x = Math.max(0, x - 0.01);
    const y = addition - x;
    return { feasible: true, additionLiters: addition, exactE85Liters: exact,
      e85Liters: x, sp98Liters: y, final: interval(x), minimumUpper: baseline.high,
      limitedBySpace: theoretical >= addition - 1e-12 };
  }
  return { calculate, parseDecimal };
});
