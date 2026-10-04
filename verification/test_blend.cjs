'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { calculate, parseDecimal } = require('./blend.js');
const vectors = JSON.parse(fs.readFileSync(path.join(__dirname, 'test_vectors.json'), 'utf8'));
let checked = 0;
for (const v of vectors) {
  if (v.error) { assert.throws(() => calculate(v.input)); checked++; continue; }
  const result = calculate(v.input);
  assert.equal(result.feasible, v.expected.feasible, v.name);
  for (const key of ['exactE85Liters', 'e85Liters', 'sp98Liters', 'minimumUpper']) {
    const e = v.expected[key];
    if (e === null) assert.equal(result[key], null, v.name + '/' + key);
    else if (e !== undefined) assert.ok(Math.abs(result[key] - e) < 1e-8, v.name + '/' + key);
  }
  checked++;
}
for (const [text, value] of [['1,25',1.25],[' 1.25 ',1.25],['0',0],['',null],['NaN',null],['Infinity',null],['1,2.3',null],['1e4',null],['0x10',null]]) {
  assert.equal(parseDecimal(text), value);
}
let seed = 20261004;
function random() { seed = (1664525 * seed + 1013904223) >>> 0; return seed / 2**32; }
for (let n = 0; n < 10000; n++) {
  const c = 5 + random()*75, r = random()*c;
  const a = random()*.85, b = a + random()*(.85-a);
  const input = {finalLiters:c, remainingLiters:r, residual:{low:a,high:b},
    e85:{low:.54,high:.85},sp98:{low:0,high:.05},target:random()};
  const result = calculate(input);
  if (!result.feasible) {
    const minimum = (r*b + (c-r)*.05)/c;
    assert.ok(minimum > input.target);
    assert.equal(result.e85Liters, null);
    continue;
  }
  const x = result.e85Liters, y = result.sp98Liters;
  assert.ok(x >= 0 && y >= -1e-9);
  assert.ok(Math.abs(r+x+y-c) < 1e-9);
  assert.ok(result.final.high <= input.target + 1e-10);
  // Verify the interval independently through its eight corners and an interior mixture.
  for (const er of [a,b]) for (const ep of [.54,.85]) for (const es of [0,.05]) {
    const mixed = (r*er+x*ep+y*es)/c;
    assert.ok(mixed >= result.final.low-1e-10 && mixed <= result.final.high+1e-10);
  }
  const interior = (r*(a+(b-a)*random()) + x*(.54+.31*random()) + y*.05*random())/c;
  assert.ok(interior >= result.final.low-1e-10 && interior <= result.final.high+1e-10);
  // Independent binary search for the greatest feasible continuous volume.
  let lo=0, hi=c-r;
  for(let j=0;j<60;j++) {
    const mid=(lo+hi)/2;
    if ((r*b+mid*.85+(c-r-mid)*.05)/c <= input.target) lo=mid; else hi=mid;
  }
  assert.ok(Math.abs(result.exactE85Liters-lo) < 1e-8);
  if(x+.01 <= c-r+1e-10) {
    assert.ok((r*b+(x+.01)*.85+(c-r-x-.01)*.05)/c > input.target-1e-10);
  }
}
console.log(JSON.stringify({vectors:checked, randomizedCases:10000, decimalParsingCases:9, status:'passed'}));
