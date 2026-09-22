Public API
==========

The following objects form the intentionally exported pre-release API.

Contracts
---------

.. autoclass:: selcal.contracts.PlanRequest
   :members:

.. autoclass:: selcal.contracts_v2.PlanRequestV2
   :members:

.. autoclass:: selcal.contracts.ResolvedScientificPlan
   :members:

.. autoclass:: selcal.contracts_v2.ResolvedScientificPlanV2
   :members:

Resolution and migration
------------------------

.. autoclass:: selcal.resolution.PlanResolution
   :members:

.. autoclass:: selcal.resolution_v2.PlanResolutionV2
   :members:

.. autoclass:: selcal.migration_v1_to_v2.PlanMigrationV1ToV2
   :members:

.. autofunction:: selcal.resolution.resolve_plan

.. autofunction:: selcal.resolution_v2.resolve_plan_v2

.. autofunction:: selcal.migration_v1_to_v2.migrate_plan_v1_to_v2

Calibration and verification
----------------------------

.. autofunction:: selcal.calibration_v2.calibrate_selected_family

.. autofunction:: selcal.calibration_v2.verify_calibration_result

Result record serialization (development API)
----------------------------------------------

These functions retain complete result content. Decoding does not authenticate
the input pair or historical execution and does not resume or replay a run.
The caller supplies an explicit per-record byte limit; it is not a process-memory
guarantee or a universal dataset limit.

.. autofunction:: selcal.result_wire.encode_calibration_result

.. autofunction:: selcal.result_wire.decode_calibration_result

.. autoclass:: selcal.result_wire.ResultWireError

File workflow (development API)
--------------------------------

These entrypoints share the same service as the installed ``selcal`` command.
Terminal reading and reporting do not imply checkpoint recovery or authentication.

.. autoclass:: selcal.workflow_config.WorkflowConfig
   :members:

.. autofunction:: selcal.workflow_config.decode_workflow_config

.. autofunction:: selcal.workflow_config.encode_workflow_config

.. autofunction:: selcal.workflow.validate_files

.. autofunction:: selcal.workflow.run_files

.. autofunction:: selcal.workflow.read_workflow

.. autofunction:: selcal.workflow.verify_record

.. autofunction:: selcal.workflow.report_record

.. autofunction:: selcal.workflow.doctor
