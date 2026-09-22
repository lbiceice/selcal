# Final installed-sdist user-flow verification

Status: **PASS_LOCAL_INSTALLED_SDIST_USER_FLOWS**. This is a local installation and synthetic workflow result; it is not scientific validity, licence approval, public release, submission readiness, or full product-suite acceptance.

The final real sdist was rebuilt and installed non-editably into `/tmp/selcal-product-installed-20260908.dY3c0V/venv`. Only SelCal was replaced (`--no-deps --reinstall-package selcal`); the recorded dependency versions remained Python 3.11.12, NumPy 2.4.6, and SelCal 0.1.0.dev0. All commands ran outside the checkout, from the newly created empty workspace `/tmp/selcal-product-installed-20260908.GcAxF6`, with `PYTHONPATH` removed and user-site loading disabled. The observed import location was the new environment's `site-packages/selcal/__init__.py`; the checkout was absent from the isolated import probe's `sys.path`.

All **39 Python source files** in the installed package, actual sdist, sibling wheel, and current checkout were checked for identical paths and exact bytes. The combined `installed_python_sources_v1` identity was `73ccc9621719794645b23b18aa4457629f8f67b85b577f6bb68de976e142418c`, before and after user-flow execution.

| Actual operation | Exit | Observation |
|---|---:|---|
| Install final sdist | 0 | SelCal rebuilt and replaced; dependencies unchanged |
| Installed import/identity probe | 0 | Installed package path; no PYTHONPATH |
| README validate | 0 | PASS |
| README run | 0 | COMPLETE; p=0.2; 9 retained replicates |
| README verify | 0 | COMPLETE; replay NOT_PERFORMED |
| README verify --replay | 0 | COMPLETE; replay MATCH |
| README report | 0 | COMPLETE; report retained |
| README doctor | 0 | PASS; scientific_validation NOT_EXECUTED |
| basic_selection_aware_calibration.py | 0 | complete; p=0.2 |
| fail_closed_not_evaluable.py | 0 | not_evaluable; null_bind; p=null |
| binned_nette_block_shuffle.py | 0 | complete; p=0.4 |
| save_and_read_result.py save | 0 | complete; p=0.2; content_only_not_replay |
| save_and_read_result.py read | 0 | complete; p=0.2; content_only_not_replay |
| NOT_EVALUABLE run | 7 | NOT_EVALUABLE; null_bind; p/decision=null; 0 retained replicates |
| NOT_EVALUABLE verify | 7 | NOT_EVALUABLE; replay NOT_PERFORMED |
| NOT_EVALUABLE verify --replay | 7 | NOT_EVALUABLE; replay MATCH |
| NOT_EVALUABLE report | 7 | NOT_EVALUABLE; report retained |

The NOT_EVALUABLE CSV/config uses the same arrays and plan parameters as the shipped fail-closed Python example. Exit 7 is the documented scientific not-evaluable outcome, not an I/O failure and not evidence of no effect. Exact replay agreement checks stored/current result consistency for these fixed examples; it does not authenticate past execution or validate scientific claims.

## Bound evidence

- Actual stdout, stderr, command arguments, working directories, return codes, versions, source hashes, input hashes, and output hashes: `installed_check_final.json`, SHA-256 `24cb151db609a87e5efe50a5dcf10a66c5a7dc4e0a638f69739d588ef9929b22`.
- Exact final driver retained in `installed_verification_final.py.txt`, SHA-256 `f67edb472b4ef20fa3c4d9c33288ba8e70bc18d59bc9ece4fcaf57a9dd39144d`.
- Final sdist retained as `installed_final_source_sdist.tar.gz`, 875898 bytes, SHA-256 `bc69a294b4a5d7b397d4e599dc98ba784f8d3a774f5646b703729fe6e712c9f8`.
- Final sibling wheel retained as `installed_final_sibling_wheel.whl`, 173524 bytes, SHA-256 `dbf270e0cac37eae34e1f668ddae455cc72e1648f899c95ff12557508dd75c8e`.
- Complete and NOT_EVALUABLE SQLite records, HTML reports, result JSON and derived CSV/config are retained under the `installed_final_` prefix. All retained artifacts were rehashed against the final receipt after execution.
- `installed_check.json` and `installed_check_retry1.json` retained their original hashes. Their original driver bytes remain separately retained. No historical evidence was overwritten. The original `/tmp/selcal-file-workflow-installed.QMfe4R` environment was not modified.

The historical-code-audit binding was also rechecked after the descriptor repair: current contracts hash `85e201ad5efdf6f3a31064d69557d5dd641d43c14edf5f868ce682088e53961d` and primitive hash `314bd108c242bc19bf2cf4ccfbf6a311633e2577f3097e063ebcbb23cc064060` match its current-source fields, while the old audit remains hash-bound. This source linkage does not repeat or upgrade the historical whole-code audit.

No full pytest suite was run by this installation reviewer; final public-test-asset and complete product-suite acceptance remain separate root-owned checks.
