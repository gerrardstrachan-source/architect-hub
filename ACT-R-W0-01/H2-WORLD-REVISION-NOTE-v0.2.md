# H2 World Revision Note v0.2

## Authority
This note governs the active H2 world construction and supersedes conflicting world-level wording in the earlier `H2-PROSPECTIVE-DESIGN.md` candidate specification. It does not authorize ACT-R implementation or execution.

## H-S / H-C interpretation
H-S and H-C are matched relational histories:

- H-S: `A0 iff x XOR y = 1`
- H-C: `A0 iff c XOR x = 1`

H-C is **not** a no-structure, random, or absence-of-regularity control. The scientific contrast is relational-history transfer between matched-complexity contingencies.

## Active training construction
The binary state space is all eight `(c,x,y)` states. Training exposes six states only, each 32 times:

`000, 010, 011, 101, 110, 111`

The states `001` and `100` are completely withheld from training. H-S and H-C use the identical ordered observable input sequence and the same exposure counts.

## Active A condition
A presents all eight states in the fixed future sequence, 12 times each, while retaining the source relation for the relevant history.

The novelty is not a reorder, renamed token, or unseen primitive value. It is the first learner exposure to the exact joint states `001` and `100`.

Therefore A is defined as a **held-out recombinative extension**.

## Active B/C/D conditions
B changes the future contingency to `A0 iff c XOR y = 1`.

C applies the fixed surface bijection `c' = 1-c`, `x' = 1-x`, `y' = 1-y`, which preserves both source parity relations.

D complements the source correct action mapping `A0 <-> A1`.

The same future source-state order is used across A, B, C, and D; C alone changes the presented state codes.

## Fixture authority
The complete ordered state sequences are stored in:

`ACT-R-W0-01/H2-W0.2-STATE-SEQUENCES.json`

The active world manifest is:

`ACT-R-W0-01/H2-WORLD-CANDIDATE-v0.2.json`

The construction audit is:

`ACT-R-W0-01/H2-WORLD-CONSTRUCTION-AUDIT-v0.2.md`

## Boundary
World-level identity, isolation, accessibility, reproducibility, and neutrality are established for this candidate construction. Immediate-performance matching remains unresolved because it requires model execution.

Accordingly:

**ACT-R prediction: NOT AUTHORIZED**

**H2 fixture freeze: NOT AUTHORIZED**

**H2 implementation: NOT AUTHORIZED**

**H2 execution: NOT AUTHORIZED**
