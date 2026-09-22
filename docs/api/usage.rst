Usage guide
===========

Development installation
------------------------

Use Python 3.11 or newer in an isolated environment and install the checked-out
snapshot from the repository root:

.. code-block:: console

   python -m pip install .

This installs a development snapshot, not a public release.

Complete calibration example
----------------------------

Run the deterministic complete route with:

.. code-block:: console

   python examples/basic_selection_aware_calibration.py

The script resolves the request, performs complete surrogate reselection, verifies
the result, and prints machine-readable JSON. For its fixed synthetic input it
selects candidate 2 and reports ``p_value=0.2``. That number is an example-specific
contract result, not scientific validation or evidence for a domain claim.

.. literalinclude:: ../../examples/basic_selection_aware_calibration.py
   :language: python
   :linenos:
   :caption: examples/basic_selection_aware_calibration.py

Interpret a complete result only after ``verify_calibration_result`` succeeds.
The ``scientific_plan_sha256`` binds the result to the resolved plan;
``planned_replicates`` states the requested Monte Carlo count; and
``failure_count`` records retained replicate failures rather than silently
shortening the denominator.

Binned NetTE and block shuffle
------------------------------

The third example covers the other registered statistic/null combination:
equal-width binned NetTE with strict block shuffling.

.. code-block:: console

   python examples/binned_nette_block_shuffle.py

The fixed input has length 10, three bins, candidate lags 1 and 2, block length
2, and nine planned replicates. The verified output selects candidate 1 and
reports ``p_value=0.4``. This broadens executable feature coverage; the example
does not compare SelCal with another package or establish an M6 result.

.. literalinclude:: ../../examples/binned_nette_block_shuffle.py
   :language: python
   :linenos:
   :caption: examples/binned_nette_block_shuffle.py

Fail-closed example
-------------------

Run the deliberately non-evaluable route with:

.. code-block:: console

   python examples/fail_closed_not_evaluable.py

The fixed request has no admissible circular shift. SelCal returns
``status="not_evaluable"``, ``failure_stage="null_bind"``, no p-value, no reject
decision, and no surrogate replicates. ``NOT_EVALUABLE`` is not evidence of no
effect or non-significance.

.. literalinclude:: ../../examples/fail_closed_not_evaluable.py
   :language: python
   :linenos:
   :caption: examples/fail_closed_not_evaluable.py

Save and read complete result content
--------------------------------------

The following commands execute in separate processes. The first calculates the
small synthetic basic example and writes every observed candidate, replicate,
transformation token, failure field and decision. The second strictly reads the
saved record; it does **not** rerun the calibration.

.. code-block:: console

   python examples/save_and_read_result.py save result.json --max-bytes 65536
   python examples/save_and_read_result.py read result.json --max-bytes 65536

The output file must not already exist. The example cap of 65,536 bytes is a
caller-selected budget for this small record, not a tested peak-memory bound or
a scientific threshold. Oversized or malformed input is rejected, not truncated.
An I/O failure is reported as an operation failure, never as a scientific result;
an interrupted write can leave a partial file, which must not be treated as a
completed record. The example is not an atomic evidence-bundle publisher.

The wire uses schema ``selcal.calibration-result-wire.v1``, UTF-8 JSON, exact
hexadecimal float tags and one terminal newline. Duplicate, missing and extra
fields, non-finite numbers and noncanonical encodings are rejected. Null values
and analytical failures are retained. The API returns a restored
``CalibrationResult`` whose content is internally checked, not authenticated
historical execution. A fresh resolver and ``verify_calibration_result`` can
check the documented result/plan consistency; neither substitutes for checking
the real input or executing a replay. No checkpoint/resume or full evidence
bundle is supplied by this example.

.. literalinclude:: ../../examples/save_and_read_result.py
   :language: python
   :linenos:
   :caption: examples/save_and_read_result.py

File-driven workflow
---------------------

For the actual file workflow, use these commands after installation:

.. code-block:: console

   selcal validate examples/workflow/series.csv examples/workflow/pearson.json
   selcal run examples/workflow/series.csv examples/workflow/pearson.json run.sqlite --max-bytes 1048576
   selcal verify run.sqlite --max-bytes 1048576 --replay
   selcal report run.sqlite report.html --max-bytes 1048576

The CSV/config fixtures are synthetic demonstrations. ``python -m selcal`` is an
equivalent entrypoint. Ordinary verification and reports do not recompute; only
explicit ``--replay`` performs a full calibration and exact-byte comparison.
Records capture their own input and request, without relying on original paths.
Reading captured terminal data is not checkpoint/resume or historical execution
authentication. Output paths must not exist. Scientific NE exits with code 7;
invalid requests use 2 and operation/integrity failures 4, with no invented p-value.

Reading the output
-------------------

``selected_candidate`` is the reported lag label; ``tied_candidates`` preserves
the tolerance-defined tie set. The family decision statistic is distinct from
the lag label. It does not identify a causal edge. Every surrogate rescans the
declared candidate family; the result is not a test performed only at the lag
chosen from the observed data.

``planned_replicates`` is B, not the number of successful replicates. When the
result is complete, the implemented Monte Carlo tail is (1 + E) / (B + 1), where
E is the recorded exceedance count. For a replicate-stage failure, p and the
decision remain null and the retained diagnostics/bounds are not a replacement
p-value. Pre-replicate NE retains its distinct failure stage and no invented
replicate outcomes. Increasing B cannot repair an inappropriate null model.

The example parameters are explicit test-fixture choices, not recommended
defaults for arbitrary research data. Statistical/null-model operating conditions
and task-specific parameter guidance require the still-open scientific studies.

Current claim boundary
----------------------

These examples demonstrate executable API and failure contracts. They do not
establish null-model exchangeability, Type-I-error control, statistical power,
workflow superiority, independent reuse, or SoftwareX readiness. Those claims
remain subject to the prospective M6 and release gates.
