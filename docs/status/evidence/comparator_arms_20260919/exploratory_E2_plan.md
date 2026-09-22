# Exploratory E2 (post hoc, written after seeing E1; NEVER a primary or confirmatory result)

Observation: in E1 the circular+reselection re-implementation (A5, min_shift=1, 64 states incl. identity)
rejects 7/400 (L=4) and 0/400 (L=8) under the nulls, i.e. it looks over-conservative with a power ceiling.

Hypothesis H-floor: a circular shift s with |s| < L maps searched lag l to lag l+s, which is also in the
searched set, so null states s = 0..(L - lag*) reproduce the observed maximum exactly. The exact p then has a
floor of about (L - lag* + 1)/64, which already exceeds .05 at L=4 when lag*=1 and always does at L=8.

Checks (re-implementation only; SelCal production not executed):
1. Exact 64-state enumeration at L in {2,4,8} under min_shift=1: fraction of inputs whose exact p can
   never be <= .05, plus the minimum attainable p.
2. Variant V: null shifts uniform on [L, 64-L] (excludes identity and all colliding shifts), B=199,
   p=(1+E)/200, full reselection. Report null-cell size and alternative-cell power at L in {2,4,8},
   next to Bonferroni-parametric (A2) and A5.
Seeds: tag "SelCal/comparator-arms-v1|{cell}|{index}|E2-L{L}".
Any conclusion is a candidate for a SelCal default change that needs its own frozen confirmation run.
