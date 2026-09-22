"""Read-only, same-team old/new regression; not independent scientific validation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

import selcal
from selcal import PlanRequestV2, calibrate_selected_family, resolve_plan_v2
from selcal.contracts import SeriesPair
from selcal.result_wire import encode_calibration_result


def cases():
    source = [0, 1, 0, 1, 2, 1, 2, 0, 2, 1, 4, 3]
    target = [1, 0, 1, 2, 1, 0, 2, 1, 2, 0, 3, 4]
    for statistic, parameters in (
        ("lagged_pearson_v1", {}),
        ("equal_width_binned_nette_v1", {"bins": 3}),
    ):
        for null, null_parameters in (
            ("circular_shift_v2", {"min_shift": 1}),
            ("block_shuffle_v2", {"block_length": 2}),
        ):
            for selection in ("max_absolute", "max_upper"):
                for values in (source, [0] * len(source)):
                    yield (
                        values,
                        target,
                        (1, 2),
                        statistic,
                        parameters,
                        null,
                        null_parameters,
                        selection,
                    )
    yield (
        [0, 1, 2, 3, 4],
        [4, 3, 2, 1, 0],
        (1, 3),
        "lagged_pearson_v1",
        {},
        "circular_shift_v2",
        {"min_shift": 3},
        "max_upper",
    )
    yield (
        [0, 0, 1, 2, 0, 0],
        [0, 1, 2, 3, 4, 5],
        (1, 2),
        "lagged_pearson_v1",
        {},
        "circular_shift_v2",
        {"min_shift": 1},
        "max_upper",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    args = parser.parse_args()
    baseline_files = sorted(args.baseline.glob("case-*.json"))
    if len(baseline_files) != 18:
        raise ValueError("requires the complete 18-case pre-refactor baseline")
    rows = []
    for index, case in enumerate(cases()):
        x, y, candidates, statistic, parameters, null, null_parameters, selection = case
        pair = SeriesPair(np.asarray(x, dtype=np.float64), np.asarray(y, dtype=np.float64))
        request = PlanRequestV2(
            candidates=candidates,
            statistic_name=statistic,
            statistic_params=parameters,
            selection_rule=selection,
            null_name=null,
            null_params=null_parameters,
            replicates=9,
            alpha=0.05,
            tie_tolerance=1e-12,
            root_seed=17,
        )
        result = calibrate_selected_family(pair, resolve_plan_v2(request))
        current = encode_calibration_result(result, max_bytes=1_000_000)
        baseline = (args.baseline / f"case-{index:02d}.json").read_bytes()
        old = json.loads(baseline)
        new = json.loads(current)
        rows.append(
            {
                "case": index,
                "status": result.status.value,
                "failure_stage": result.failure_stage.value if result.failure_stage else None,
                "baseline_sha256": hashlib.sha256(baseline).hexdigest(),
                "current_sha256": hashlib.sha256(current).hexdigest(),
                "match": current == baseline,
                "changed_top_level_fields": sorted(
                    key for key in old.keys() | new.keys() if old.get(key) != new.get(key)
                ),
            }
        )
    package_root = Path(selcal.__file__).resolve().parent
    identity = hashlib.sha256()
    source_files = sorted(package_root.rglob("*.py"))
    for path in source_files:
        relative = path.relative_to(package_root).as_posix().encode()
        content = path.read_bytes()
        identity.update(len(relative).to_bytes(8, "big"))
        identity.update(relative)
        identity.update(len(content).to_bytes(8, "big"))
        identity.update(content)
    print(
        json.dumps(
            {
                "scope": "SAME_TEAM_DETERMINISTIC_REGRESSION_NOT_EXTERNAL_OR_DOMAIN_VALIDATION",
                "source_identity": {
                    "scheme": "installed_python_sources_v1",
                    "file_count": len(source_files),
                    "sha256": identity.hexdigest(),
                },
                "matched": sum(row["match"] for row in rows),
                "total": len(rows),
                "cases": rows,
            },
            indent=2,
        )
    )
    return 0 if all(row["match"] for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
