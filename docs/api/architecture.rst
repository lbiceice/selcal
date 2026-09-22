Architecture
============

Scope and status
----------------

SelCal currently implements an in-memory M0--M2 core. It resolves an immutable
scientific plan, evaluates a candidate family on observed data, applies an owned
null transformation, repeats the complete candidate-selection operation, and
returns a result bound to the resolved plan. Terminal persistence and a thin CLI
are implemented through a shared application service. Resumable execution, full
evidence bundles, scientific validation, a user interface, and a public release
remain unfinished.

Component boundaries
--------------------

.. list-table::
   :header-rows: 1
   :widths: 18 33 49

   * - Layer
     - Modules
     - Responsibility
   * - M0 contracts
     - ``selcal.contracts_v2``, ``selcal.canonical_v2``
     - Validate request fields, freeze plan identity, and provide canonical
       serialization for scientific hashes.
   * - M0 resolution
     - ``selcal.resolution_v2``, ``selcal.migration_v1_to_v2``
     - Resolve named statistics, selection rules, and null models without
       silently changing historical v1 identities.
   * - M1 statistics
     - ``selcal.statistics``
     - Evaluate binned NetTE or lagged Pearson on explicitly constructed common
       support.
   * - M1 null models
     - ``selcal.nulls``
     - Bind circular-shift or strict block-shuffle transformations to immutable
       observed inputs and SelCal-owned random tokens.
   * - M2 selection
     - ``selcal.selection_v2``
     - Select one candidate using the plan's rule and tie contract.
   * - M2 calibration
     - ``selcal.calibration_v2``
     - Recompute and reselect the complete candidate family for exactly the
       planned number of surrogates, then create a verifiable result.
   * - Internal oracle
     - ``selcal.exact_oracle_v0``
     - Check finite-state algorithm behavior independently of the production
       calibration path. It is not a domain-validity oracle.
   * - File application
     - ``selcal.workflow``, ``selcal.workflow_config``
     - Run actual CSV/NPZ requests through the core; bind captured input, config
       and complete result; separate read-only consistency from explicit replay.
   * - Terminal store
     - ``selcal.workflow_store``, ``selcal.result_wire``
     - Strict complete byte records in SQLite with exclusive writes and bounded
       read-only snapshots; no per-replicate recovery yet.
   * - User entrypoint
     - ``selcal.cli``
     - Thin validate/run/verify/report/doctor commands sharing the application API.

Execution sequence
------------------

.. code-block:: text

   PlanRequestV2 + immutable SeriesPair
                |
                v
        resolve_plan_v2
                |
                v
   ResolvedScientificPlanV2 -- scientific_plan_sha256
                |
                v
   bind statistic + bind null transformation
                |
                v
   observed candidate scan -> observed selection
                |
                v
   for each planned replicate:
       transform full source -> rebuild support
       -> rescan all candidates -> reselect
                |
                v
   CalibrationResultV2 -> verify_calibration_result

Identity and determinism
------------------------

Plan serialization is canonical and versioned. The resolved plan hash identifies
scientific choices; it is not a hash of runtime outputs or a claim of correctness.
Randomness is derived from the frozen root seed and owned replicate tokens. The
examples therefore emit byte-identical JSON for their fixed inputs on the
currently verified environment. Cross-platform reproducibility remains a release
gate until a supported-platform CI matrix is executed.

Failure boundary
----------------

Invalid contracts fail during resolution. A scientifically impossible bound null
configuration returns a verified ``NOT_EVALUABLE`` result with null decision
fields. Integrity failures and execution defects are not converted into evidence
of no effect. The in-memory resource budget is checked before replicate
allocation.

Planned downstream layers
-------------------------

Terminal persistence and a thin CLI are implemented, but M3/M4/M5 are not fully
accepted modules. M3 still needs transactionally tested incremental execution and
recovery; M4 needs its full export/manifest scope; M5 needs final compatibility
testing. M6 must test calibration, comparators, negative controls and a real case.
UI, CI, containers, release and the SoftwareX manuscript remain unfinished.
