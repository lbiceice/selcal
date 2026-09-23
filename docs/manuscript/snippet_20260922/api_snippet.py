import csv

import numpy as np

from selcal import PlanRequestV2, calibrate_selected_family, resolve_plan_v2
from selcal.contracts import SeriesPair
from selcal.workflow import preflight

rows = list(csv.DictReader(open("examples/workflow/series.csv")))
pair = SeriesPair(source=np.array([float(r["x"]) for r in rows]),
                  target=np.array([float(r["y"]) for r in rows]))
request = PlanRequestV2(
    candidates=(1, 2, 3), statistic_name="lagged_pearson_v1", statistic_params={},
    selection_rule="max_absolute", null_name="circular_shift_exact_v1",
    null_params={"min_shift": 1}, replicates=99, alpha=0.05, tie_tolerance=0.0,
    root_seed=17)
check = preflight(request, sample_count=len(rows))
print(check["plan"]["status"], check["plan"]["attainability"]["status"])
result = calibrate_selected_family(pair, resolve_plan_v2(request))
sel = result.observed_selection
print(result.status.value, sel.selected_candidate, round(sel.decision_statistic, 3),
      result.exceedance_count, result.p_value, result.reject_null)
