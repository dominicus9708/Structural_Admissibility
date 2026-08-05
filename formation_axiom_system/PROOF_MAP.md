# Computational proof map

This map states what each executable check supports and what remains a manuscript proof.

| Manuscript result or construction | Executable support | Scope |
|---|---|---|
| One-point model and ZFC realizability witness | `construct_one_point_model()` | Checks the displayed finite instance, not the metatheoretic ZFC statement |
| Formation-trace/channel closure in the finite witness | one-point and witness constructors | Checks the instantiated closure data |
| Non-injectivity of finite-sum composition | `noninjective_composition_witness()` | Constructs two distinct finite channel families with equal composite `0` |
| D2 early boundary obstruction | `construct_d2_witness()` | Reproduces Stage-3 first branching for the displayed pair |
| Synthetic `3 x 3` indexed witness | `enumerate_indexed_witness()` | Exhaustively checks all `512` index-aligned pairs |
| Channel counts | deterministic enumeration | Reproduces `768` and `1536` |
| Channel-structure mismatches | deterministic enumeration | Reproduces `387` |
| Vertical without horizontal | deterministic enumeration | Reproduces `62` |
| Full-family composite coincidences | deterministic enumeration | Reproduces `127` among mismatched pairs |
| Primitive-axiom independence | none | General countermodel proofs remain in the manuscript |
| Unique relative closure | none | General extensional set-theoretic proof remains in the manuscript |
| Identity/composition closure of maps and embeddings | none | General proofs remain in the manuscript |
| Symmetry and strict-isomorphism invariance of first branching | finite profiles only | General theorem remains in the manuscript |

The executable package is therefore a reproducibility and proof-audit companion, not an automated formalization of the entire axiom system.
