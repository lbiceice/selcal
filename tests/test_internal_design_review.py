"""Checkout-only review of the internal design; excluded explicitly from sdist."""

from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def test_correction_design_has_clean_whitespace_and_documents_final_trust_scope() -> None:
    design_path = (
        REPOSITORY_ROOT / "docs/superpowers/specs/2026-08-28-task10-trusted-call-boundary-design.md"
    )
    design = design_path.read_text(encoding="utf-8")

    assert all(line.rstrip() == line for line in design.splitlines())
    assert "behavior-critical module globals" in design
    assert "captured module globals mapping" in design
    assert "public verifier hook" in design
    assert "selector identity check" in design
    assert "import origins through straightforward assignments and containers" in design
