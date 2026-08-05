from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formation_axiom_reproduction import (  # noqa: E402
    EXPECTED,
    construct_d2_witness,
    construct_one_point_model,
    enumerate_indexed_witness,
    noninjective_composition_witness,
    role_set_lh,
    write_outputs,
)


class FormationAxiomReproductionTests(unittest.TestCase):
    def test_one_point_model(self) -> None:
        model = construct_one_point_model()
        self.assertTrue(model.channel_present)
        self.assertEqual(model.composite_singleton, 0)

    def test_d2_first_branch(self) -> None:
        witness = construct_d2_witness()
        self.assertEqual(witness.first_branching_index, 3)
        self.assertEqual(witness.stage_comparison_nonempty[:3], (True, True, True))
        self.assertFalse(witness.stage_comparison_nonempty[3])

    def test_indexed_counts(self) -> None:
        summary, rows = enumerate_indexed_witness()
        self.assertEqual(len(rows), 512)
        for key, expected in EXPECTED.items():
            if key in summary:
                self.assertEqual(summary[key], expected)

    def test_partition_boundaries(self) -> None:
        self.assertEqual(role_set_lh(124), ("H", "V", "D"))
        self.assertEqual(role_set_lh(125), ("V",))
        self.assertEqual(role_set_lh(186), ("V",))
        self.assertEqual(role_set_lh(187), ("H",))
        self.assertEqual(role_set_lh(505), ("H",))
        self.assertEqual(role_set_lh(506), ("H", "V"))

    def test_noninjective_composition(self) -> None:
        witness = noninjective_composition_witness()
        self.assertTrue(witness["families_distinct"])
        self.assertTrue(witness["composites_equal"])
        self.assertEqual(witness["composite_1"], 0)

    def test_outputs_are_created(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            write_outputs(output)
            self.assertTrue((output / "formation_witness_summary.json").exists())
            self.assertTrue((output / "proof_obligation_audit.json").exists())
            self.assertTrue((output / "indexed_witness_cases.csv").exists())


if __name__ == "__main__":
    unittest.main()
