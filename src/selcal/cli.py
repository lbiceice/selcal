"""Thin command-line consumer of the public file workflow."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from selcal import __version__
from selcal.contracts_v2 import ResourceLimitError, SelCalV2Error
from selcal.result_wire import ResultWireError
from selcal.workflow import (
    WorkflowError,
    doctor,
    report_record,
    result_summary,
    run_files,
    validate_files,
    verify_record,
)
from selcal.workflow_config import WorkflowConfigError
from selcal.workflow_store import RecordStoreError


def _positive(value: str) -> int:
    try:
        limit = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("max-bytes must be a positive integer") from error
    if limit < 1:
        raise argparse.ArgumentTypeError("max-bytes must be a positive integer")
    return limit


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="selcal", description="Selection-aware calibration")
    parser.add_argument("--version", action="version", version=f"SelCal {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "run"):
        command = commands.add_parser(name)
        command.add_argument("input")
        command.add_argument("config")
        if name == "run":
            command.add_argument("output")
            command.add_argument("--max-bytes", type=_positive, required=True)
            command.add_argument(
                "--allow-unattainable-plan",
                action="store_true",
                help="run a plan whose smallest attainable p-value exceeds alpha",
            )
    for name in ("verify", "report"):
        command = commands.add_parser(name)
        command.add_argument("record")
        command.add_argument("--max-bytes", type=_positive, required=True)
        if name == "verify":
            command.add_argument(
                "--replay",
                action="store_true",
                help="recompute and compare the complete saved result",
            )
        else:
            command.add_argument("output")
    commands.add_parser("doctor")
    return parser


def _execute(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "validate":
        return validate_files(args.input, args.config)
    if args.command == "run":
        return result_summary(
            run_files(
                args.input,
                args.config,
                args.output,
                max_bytes=args.max_bytes,
                allow_unattainable=args.allow_unattainable_plan,
            )
        )
    if args.command == "verify":
        return verify_record(args.record, max_bytes=args.max_bytes, replay=args.replay)
    if args.command == "report":
        return report_record(args.record, args.output, max_bytes=args.max_bytes)
    return doctor()


def main(argv: list[str] | None = None) -> int:
    """Emit one JSON operation result; scientific NE uses exit 7, not an I/O failure."""
    args = _parser().parse_args(argv)
    code, outcome, error_code = 0, "PASS", None
    data: dict[str, Any] | None = None
    try:
        data = _execute(args)
        plan = data.get("preflight", {}).get("plan") if args.command == "validate" else None
        if plan is not None and plan["status"] != "EXECUTABLE":
            code, outcome, error_code = 2, "PLAN_NOT_EXECUTABLE", plan["reasons"][0]
        elif data.get("status") == "not_evaluable":
            code, outcome = 7, "NOT_EVALUABLE"
        elif data.get("status") == "complete":
            outcome = "COMPLETE"
    except (WorkflowError, RecordStoreError, ResultWireError) as error:
        code, outcome, error_code = 4, "FAIL", error.code
    except (WorkflowConfigError, ResourceLimitError, TypeError, ValueError) as error:
        code, outcome = 2, "INVALID_REQUEST"
        error_code = error.code if isinstance(error, WorkflowConfigError) else "invalid_request"
    except (OSError, SelCalV2Error):
        code, outcome, error_code = 4, "FAIL", "io_or_integrity_failure"
    except KeyboardInterrupt:
        code, outcome, error_code = 130, "CANCELLED", "interrupted_no_resume_claim"
    terminal = {
        "schema": "selcal.cli.v1",
        "command": args.command,
        "outcome": outcome,
        "exit_code": code,
        "error": error_code,
        "data": data,
    }
    try:
        if error_code is not None:
            sys.stderr.write(f"SelCal: {error_code}\n")
        sys.stdout.write(json.dumps(terminal, allow_nan=False, sort_keys=True) + "\n")
        sys.stdout.flush()
    except OSError:
        return 4
    return code
