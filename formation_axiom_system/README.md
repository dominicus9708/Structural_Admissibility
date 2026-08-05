# Formation Axiom System reproducibility package

This directory is the standard-library Python companion to:

> Kwon Dominicus, *Formation Axiom System: Dimensional-Structural Describability*.

It reproduces the manuscript's explicit finite constructions and numerical witness claims. It does **not** replace the manuscript's general set-theoretic proofs of primitive-axiom independence, unique relative closure, formation-trace characterization, morphism closure, strict-equivalence properties, or first-branching invariance.

## Reproduced claims

The package deterministically verifies:

- the one-point full-model satisfiability witness;
- the D2 early boundary obstruction with first branching index `3`;
- the synthetic indexed witness with first branching index `5`;
- `768` admitted channels in `L_H`;
- `1536` admitted channels in `L_G`;
- `387` index-aligned channel-structure mismatches;
- `62` vertical-without-horizontal cases in `L_H`;
- `127` full-family composite coincidences among the mismatched pairs;
- a fully constructed finite witness that finite-sum composition need not be injective.

## Requirements

- Python 3.10 or later
- No third-party dependencies

## Run on Windows

From the repository root:

```powershell
python formation_axiom_system\src\formation_axiom_reproduction.py --output-dir formation_axiom_system\results
python formation_axiom_system\src\verify_formation_axiom_results.py --results-dir formation_axiom_system\results
python -m unittest discover -s formation_axiom_system\tests -v
```

## Run on Linux or macOS

```bash
python3 formation_axiom_system/src/formation_axiom_reproduction.py --output-dir formation_axiom_system/results
python3 formation_axiom_system/src/verify_formation_axiom_results.py --results-dir formation_axiom_system/results
python3 -m unittest discover -s formation_axiom_system/tests -v
```

## Deterministic outputs

- `formation_axiom_system/results/formation_witness_summary.json`
- `formation_axiom_system/results/proof_obligation_audit.json`
- `formation_axiom_system/results/indexed_witness_cases.csv`

## Interpretation boundary

The D2 and indexed constructions are formation-finite formal witnesses. The `3 x 3` index partition is part of the model definition and is not claimed to be a geometric invariant. The computational audit checks the explicitly finite consequences stated in the manuscript; it does not establish syntactic completeness, categoricity, decidability, or empirical validity.
