# Reproducibility protocol

## Environment

- Python 3.10+
- standard library only
- no random seeds, network access, external datasets, or platform-specific numerical libraries

## Procedure

1. Run `formation_axiom_reproduction.py` to reconstruct all deterministic outputs.
2. Run `verify_formation_axiom_results.py` to compare outputs with the manuscript values.
3. Run the unit tests.
4. Confirm the final message reports:

```text
D2 first branch 3
indexed first branch 5
channel counts 768/1536
mismatches 387
vertical-only 62
coincidences 127
```

## Expected files

The generated JSON files are written with sorted keys and fixed indentation. The CSV rows are ordered by configuration index `0` through `511`, so identical Python versions produce semantically identical outputs.

## Failure policy

Any assertion failure indicates that the executable reconstruction no longer matches the finite definitions or reported values in the manuscript. The code must not silently update expected constants to fit new output.
