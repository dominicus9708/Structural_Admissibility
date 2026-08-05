#!/usr/bin/env python3
"""Verify generated Formation Axiom System reproduction outputs."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from formation_axiom_reproduction import EXPECTED, proof_obligation_audit


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results",
    )
    args = parser.parse_args()

    summary_path = args.results_dir / "formation_witness_summary.json"
    audit_path = args.results_dir / "proof_obligation_audit.json"
    cases_path = args.results_dir / "indexed_witness_cases.csv"
    for path in (summary_path, audit_path, cases_path):
        if not path.exists():
            raise SystemExit(f"Missing output: {path}. Run formation_axiom_reproduction.py first.")

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    indexed = summary["indexed_witness"]

    assert summary["d2_witness"]["first_branching_index"] == EXPECTED["d2_first_branch"]
    for key, expected in EXPECTED.items():
        if key in indexed:
            assert indexed[key] == expected, (key, indexed[key], expected)
    assert audit == proof_obligation_audit()
    assert all(
        value is True
        for key, value in audit.items()
        if key.endswith("_verified") or key.startswith("one_point") or key.startswith("stage_4")
    )

    with cases_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == EXPECTED["indexed_configurations"]
    mismatch_rows = [row for row in rows if row["structures_match"] == "False"]
    coincidence_rows = [row for row in rows if row["mismatch_composite_coincidence"] == "True"]
    vertical_only_rows = [
        row for row in rows if "V" in row["LH_roles"].split(";") and "H" not in row["LH_roles"].split(";")
    ]
    assert len(mismatch_rows) == EXPECTED["mismatched_configurations"]
    assert len(coincidence_rows) == EXPECTED["composite_coincidences_among_mismatches"]
    assert len(vertical_only_rows) == EXPECTED["vertical_without_horizontal"]

    print(
        "Verification passed: D2 first branch 3; indexed first branch 5; "
        "channel counts 768/1536; mismatches 387; vertical-only 62; coincidences 127."
    )


if __name__ == "__main__":
    main()
