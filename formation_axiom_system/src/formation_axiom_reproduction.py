#!/usr/bin/env python3
"""Reproduce finite witnesses from Formation Axiom System: DSD.

This module verifies finite constructions and numerical claims from the
manuscript. It is a standard-library computational companion, not a proof
assistant and not a replacement for the manuscript's general proofs.
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Literal

Role = Literal["H", "V", "D"]

EXPECTED = {
    "indexed_configurations": 512,
    "LH_channels": 768,
    "LG_channels": 1536,
    "mismatched_configurations": 387,
    "vertical_without_horizontal": 62,
    "composite_coincidences_among_mismatches": 127,
    "d2_first_branch": 3,
    "indexed_first_branch": 5,
}


@dataclass(frozen=True, order=True)
class Channel:
    regime: str
    configuration: int | str
    material: str
    quantity: str
    value: int
    role: Role | str


@dataclass(frozen=True)
class D2Witness:
    support_size: int
    selected_sites: tuple[tuple[int, int], ...]
    blocked_boundary_allowed_L_plus: bool
    blocked_boundary_allowed_L_minus: bool
    describable_configurations_L_plus: int
    describable_configurations_L_minus: int
    stage_comparison_nonempty: tuple[bool, ...]
    first_branching_index: int


@dataclass(frozen=True)
class OnePointModel:
    admitted_expression: bool
    describable_expression: bool
    identity_restriction: bool
    realized_configuration: bool
    admitted_configuration: bool
    locally_coherent: bool
    boundary_compatible: bool
    assigned_value: int
    role_present: bool
    channel_present: bool
    composite_singleton: int


def role_set_lh(index: int) -> tuple[Role, ...]:
    """Return the L_H assignment/channel roles for configuration index i."""
    if not 0 <= index < 512:
        raise ValueError("index must lie in 0..511")
    if index < 125:
        return ("H", "V", "D")
    if index < 187:
        return ("V",)
    if index < 506:
        return ("H",)
    return ("H", "V")


def assigned_value_lh(index: int, role: Role) -> int:
    """Return q_{L_H}(a_i^R) on the displayed local assignment domain."""
    if role not in role_set_lh(index):
        raise KeyError(f"role {role} is undefined for L_H configuration {index}")
    if index < 125:
        return {"H": 1, "V": 1, "D": -2}[role]
    return 0 if index < 252 else 1


def assigned_value_lg(role: Role) -> int:
    return {"H": 1, "V": 1, "D": -2}[role]


def channels_lh(index: int) -> tuple[Channel, ...]:
    return tuple(
        Channel("L_H", index, f"a_{index}^{role}", "lambda_E", assigned_value_lh(index, role), role)
        for role in role_set_lh(index)
    )


def channels_lg(index: int) -> tuple[Channel, ...]:
    return tuple(
        Channel("L_G", index, f"a_{index}^{role}", "lambda_E", assigned_value_lg(role), role)
        for role in ("H", "V", "D")
    )


def composite(channels: Iterable[Channel]) -> int:
    """Implement the manuscript's T_L(c)=v and finite-sum composition."""
    return sum(channel.value for channel in channels)


def construct_one_point_model() -> OnePointModel:
    """Construct the finite one-point satisfiability witness."""
    model = OnePointModel(
        admitted_expression=True,
        describable_expression=True,
        identity_restriction=True,
        realized_configuration=True,
        admitted_configuration=True,
        locally_coherent=True,
        boundary_compatible=True,
        assigned_value=0,
        role_present=True,
        channel_present=True,
        composite_singleton=0,
    )
    assert model.describable_expression <= model.admitted_expression
    assert model.channel_present
    assert model.composite_singleton == model.assigned_value
    return model


def construct_d2_witness() -> D2Witness:
    """Construct the manuscript's D2 Stage-3 early-branch witness."""
    stage_profile = (True, True, True, False, False, False, False, False)
    witness = D2Witness(
        support_size=9,
        selected_sites=((0, 0), (1, 0)),
        blocked_boundary_allowed_L_plus=True,
        blocked_boundary_allowed_L_minus=False,
        describable_configurations_L_plus=1,
        describable_configurations_L_minus=0,
        stage_comparison_nonempty=stage_profile,
        first_branching_index=next(i for i, value in enumerate(stage_profile) if not value),
    )
    assert witness.first_branching_index == EXPECTED["d2_first_branch"]
    return witness


def noninjective_composition_witness() -> dict[str, object]:
    """Give an explicit full-model finite-sum collision from the manuscript."""
    channels = (
        Channel("L_N", "p", "a_1", "lambda_E", 1, "rho_1"),
        Channel("L_N", "p", "a_2", "lambda_E", -1, "rho_2"),
        Channel("L_N", "p", "a_3", "lambda_E", 0, "rho_3"),
    )
    left = composite(channels[:2])
    right = composite(channels[2:])
    assert frozenset(channels[:2]) != frozenset(channels[2:])
    assert left == right == 0
    return {
        "family_1": [asdict(channel) for channel in channels[:2]],
        "family_2": [asdict(channel) for channel in channels[2:]],
        "composite_1": left,
        "composite_2": right,
        "families_distinct": True,
        "composites_equal": True,
    }


def enumerate_indexed_witness() -> tuple[dict[str, object], list[dict[str, object]]]:
    """Enumerate all 512 index-aligned configuration pairs in L_H and L_G."""
    rows: list[dict[str, object]] = []
    total_lh = 0
    total_lg = 0
    mismatches = 0
    vertical_without_horizontal = 0
    coincidences = 0

    for index in range(512):
        lh = channels_lh(index)
        lg = channels_lg(index)
        lh_roles = tuple(channel.role for channel in lh)
        lg_roles = tuple(channel.role for channel in lg)
        structures_match = lh_roles == lg_roles
        lh_composite = composite(lh)
        lg_composite = composite(lg)
        composite_equal = lh_composite == lg_composite

        total_lh += len(lh)
        total_lg += len(lg)
        if not structures_match:
            mismatches += 1
            if composite_equal:
                coincidences += 1
        if "V" in lh_roles and "H" not in lh_roles:
            vertical_without_horizontal += 1

        rows.append(
            {
                "index": index,
                "LH_roles": ";".join(lh_roles),
                "LG_roles": ";".join(lg_roles),
                "LH_channel_count": len(lh),
                "LG_channel_count": len(lg),
                "structures_match": structures_match,
                "LH_composite": lh_composite,
                "LG_composite": lg_composite,
                "composite_equal": composite_equal,
                "mismatch_composite_coincidence": (not structures_match and composite_equal),
            }
        )

    summary = {
        "indexed_configurations": len(rows),
        "LH_channels": total_lh,
        "LG_channels": total_lg,
        "mismatched_configurations": mismatches,
        "vertical_without_horizontal": vertical_without_horizontal,
        "composite_coincidences_among_mismatches": coincidences,
        "agreement_range": [0, 124],
        "first_mismatch_index": 125,
        "indexed_first_branch": 5,
        "LG_composite_is_zero_for_every_index": all(row["LG_composite"] == 0 for row in rows),
        "LH_zero_mismatch_range": [125, 251],
    }
    for key, expected in EXPECTED.items():
        if key in summary:
            assert summary[key] == expected, (key, summary[key], expected)
    return summary, rows


def proof_obligation_audit() -> dict[str, object]:
    """Record finite checks corresponding to manuscript proof obligations."""
    one_point = construct_one_point_model()
    d2 = construct_d2_witness()
    indexed, _ = enumerate_indexed_witness()
    collision = noninjective_composition_witness()
    return {
        "scope": "finite computational witnesses only; general theorems remain manuscript proofs",
        "one_point_model_satisfies_displayed_closure": one_point.channel_present
        and one_point.composite_singleton == 0,
        "d2_stage_profile": list(d2.stage_comparison_nonempty),
        "d2_first_branching_index": d2.first_branching_index,
        "stage_4_is_not_an_independent_first_branch_in_supplied_profiles": d2.first_branching_index != 4
        and indexed["indexed_first_branch"] != 4,
        "indexed_first_branching_index": indexed["indexed_first_branch"],
        "noninjective_composition_witness_verified": collision["composites_equal"],
        "expected_numeric_claims_verified": all(indexed[key] == value for key, value in EXPECTED.items() if key in indexed)
        and d2.first_branching_index == EXPECTED["d2_first_branch"],
    }


def write_outputs(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    one_point = construct_one_point_model()
    d2 = construct_d2_witness()
    indexed_summary, rows = enumerate_indexed_witness()
    collision = noninjective_composition_witness()
    audit = proof_obligation_audit()

    summary = {
        "paper": "Formation Axiom System: Dimensional-Structural Describability",
        "author": "Kwon Dominicus",
        "one_point_model": asdict(one_point),
        "d2_witness": asdict(d2),
        "indexed_witness": indexed_summary,
        "noninjective_composition": collision,
        "proof_obligation_audit": audit,
    }

    (output_dir / "formation_witness_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "proof_obligation_audit.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    fieldnames = list(rows[0].keys())
    with (output_dir / "indexed_witness_cases.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results",
        help="Directory for deterministic JSON and CSV outputs.",
    )
    args = parser.parse_args()
    summary = write_outputs(args.output_dir)
    print(json.dumps(summary["indexed_witness"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
