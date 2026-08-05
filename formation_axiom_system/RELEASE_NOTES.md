# Release notes — v2.2.0

Release date: 2026-08-06

## Formation Axiom System reproducibility package

This release adds an executable companion to:

> Kwon Dominicus, *Formation Axiom System: Dimensional-Structural Describability*.

### Included checks

- one-point full-model satisfiability witness;
- D2 boundary-obstruction witness with first branching index `3`;
- synthetic indexed witness with first branching index `5`;
- admitted-channel totals `768` and `1536`;
- `387` channel-structure mismatches;
- `62` vertical-without-horizontal cases;
- `127` full-family composite coincidences among mismatched pairs;
- explicit non-injectivity witness for finite-sum composition.

### Reproducibility

The package uses Python 3.10 or later and has no third-party dependencies. GitHub Actions runs the original structural-admissibility enumeration and the Formation Axiom System package under Python 3.10 and 3.12.

### Scope

The software reproduces finite constructions and numerical claims. It does not replace the manuscript's general proofs of independence, closure, embedding, strict equivalence, or first-branching invariance.

### Suggested Git tag

```text
v2.2.0
```

The GitHub tag is the software release identifier. The manuscript version history remains managed by Zenodo.
