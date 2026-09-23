# Windows check

`records/` holds the shipped example (`examples/workflow`, sampling null and exact enumeration) run by
SelCal 0.1.0 on macOS arm64 (Python 3.11.12), Linux aarch64 (3.11.16) and Linux x86_64 (3.12.14),
all with NumPy 2.4.6 and the code of commit `7ac842c`. On macOS each Linux record decision-replays
as `DECISION_MATCH` (largest statistic difference 1 unit; p = 0.015 and 0.03).

On Windows, from the repository root:

```console
powershell -ExecutionPolicy Bypass -File scripts\windows_check.ps1
```

The script builds a locked environment, runs the full test suite and the file workflow, replays these
records (byte replay is expected to report `environment_mismatch`; decision replay should report
`DECISION_MATCH`), and writes `windows_check_results.zip`.
