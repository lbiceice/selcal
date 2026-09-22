# Amendment 1 to protocol.md (2026-09-19, after the run, before interpreting arm tables)

Gate result as frozen: FAIL, 8/1,200 observed maxima exceed 64 relative ulp (max 66,206 ulp).
Diagnosis: all 8 have |r| < 0.0035; absolute differences are 2.9e-18 to 4.9e-17 (below one ulp of 1.0,
2.2e-16); the selected lag matches SelCal in all 8 and in all 1,200 inputs. Relative ulp near zero was a
mis-specified criterion in protocol.md, not an implementation disagreement.

Amended gate: selected lag identical for all 1,200 AND |mine - sealed| <= 64 * 2^-52 (unit-scale ulp).
Result: PASS (1,200/1,200).

Disclosure: the run printed the D2 paired A0-vs-A2 counts before this amendment was written; the
full arm table had not been read. Arm computations do not depend on the gate, so no arm result was
changed. The amendment is recorded rather than silently replacing the original gate.
