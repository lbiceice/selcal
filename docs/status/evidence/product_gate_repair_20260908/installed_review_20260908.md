# Independent installation and binding review

Observed on 2026-09-08, before the pending terminal descriptor repair.

## Evidence status

- `installed_check.json` (SHA-256 `679869027c49c1c45c896eb043ccdc2f4479f9df8e1be0d124fb9be24d6c0bb3`) preserves the first verification-driver failure. Installation and import succeeded, but the driver assumed uv's `direct_url.json` contained `archive_info.hashes`; uv actually returned `archive_info={}`. This is a driver assumption failure, not a measured SelCal product failure. The exact driver is retained as `installed_verification_initial.py.txt`, hash verified against that receipt.
- `installed_check_retry1.json` (SHA-256 `dd9099aec9c121c2861c51a13b9a605d7e4a569c32eaa59d8a54d849130dc6d2`) records six README commands, four Python example files across five processes, and four expected NOT_EVALUABLE exit-7 commands. Both complete and NOT_EVALUABLE explicit replays returned `MATCH`. All 39 installed Python sources equalled checkout, sdist, and sibling wheel bytes at source identity `4eca1dae0f0a261a5bf3bc2632ad261fd460a09de712ddf65e4c8bd6ddff205e`. The exact driver is retained as `installed_verification_retry1.py.txt`, hash verified against that receipt.
- These successful user-flow observations are now **PRE-DESCRIPTOR-FIX HISTORICAL EVIDENCE**, following the separate core review's discovery of a terminal-descriptor bypass. They do not establish acceptance of the corrected source or final distribution test assets. The original receipts and copied outputs remain unchanged.
- Environment `/tmp/selcal-product-installed-20260908.dY3c0V/venv` was newly created from the real sdist, with Python 3.11.12 and NumPy 2.4.6. The original `/tmp/selcal-file-workflow-installed.QMfe4R` environment was read only for historical byte comparison and was not modified. The new environment can receive a non-editable SelCal reinstall from the final sdist, without reinstalling dependencies; final workflows must use new output paths and a new receipt.

## Two root-owned binding fixes: bounded review PASS

1. `tests/test_documentation.py` differs from the pre-fix build snapshot only by changing `in_memory_standard_20260831_figure.svg` to `in_memory_standard_20260908_figure.svg`. The new referenced figure exists. Other Sphinx/public-API assertions are unchanged.
2. `docs/status/scientific_code_smell_audit_20260831_v3.json` is byte-identical to the pre-fix build snapshot, SHA-256 `2f61dbce8c41cf8a0298407d61478936925d54c2a47716fa6b3c38de85d4dccc`. Its 13 source records differ from the reviewed checkout in exactly `src/selcal/contracts_v2.py`; all other 12 source hashes still match.
3. `contracts_v2.pre-extraction-20260908.py.txt` equals the retained historical installed file byte-for-byte, SHA-256 `9e4cb4a945602c3ca8e299aefa73b01e753d3b90bdaa465b849d81bcc2b80ef5`. The new binding links this prior identity to the current contracts and extracted primitive hashes. It explicitly says the full code-smell audit was not rerun, findings were not promoted, scientific validation is false, and release approval is false.
4. Fresh focused execution of the source-binding check and its five evidence-byte negative cases returned **6 passed, 9 deselected in 0.01s**. No historical audit bytes were changed by this reviewer. The current-source hashes must be refreshed after any descriptor repair; this review does not grant stale bindings continuing authority.

Scope is local installation, synthetic user-flow observation, and historical/current source identity linkage. No science, licence, public release, or submission approval is inferred.
