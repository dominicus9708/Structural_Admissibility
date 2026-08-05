# Structural Admissibility and Formation Axiom System — reproducibility repository

This repository contains standard-library Python packages for two connected finite-audit layers of Dimensional-Structural Describability (DSD), authored by Kwon Dominicus.

## Packages

### 1. Structural-admissibility square-lattice enumeration

The original root package exhaustively examines all `2^9 = 512` selected domains of the finite `3 x 3` square lattice and reproduces the induced-relation distribution, the total of `21,799` admissible configurations, and the finite failure witnesses stated in the structural-admissibility manuscript.

Run from the repository root:

```powershell
python src\enumerate_square_lattice.py --output-dir results
python src\verify_enumeration.py --results-dir results
python -m unittest discover -s tests -v
```

### 2. Formation Axiom System finite witnesses

The [`formation_axiom_system`](formation_axiom_system/) package accompanies:

> *Formation Axiom System: Dimensional-Structural Describability*

It reproduces the one-point, D2, non-injective-composition, and synthetic indexed finite witnesses, including the reported values `768`, `1536`, `387`, `62`, and `127`.

Run from the repository root:

```powershell
python formation_axiom_system\src\formation_axiom_reproduction.py --output-dir formation_axiom_system\results
python formation_axiom_system\src\verify_formation_axiom_results.py --results-dir formation_axiom_system\results
python -m unittest discover -s formation_axiom_system\tests -v
```

## Scope

These programs reproduce explicitly finite constructions and numerical claims. They do not replace the general proofs in the manuscripts and do not claim empirical validation, syntactic completeness, categoricity, or decidability.

## Requirements

- Python 3.10 or later
- No third-party dependencies
