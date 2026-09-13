# H2 World Construction Audit v0.1

## Status

**Candidate construction — NOT FROZEN — NOT EXECUTABLE**

## Purpose

This audit evaluates a candidate H2 world construction before ACT-R forward prediction. It does not authorize implementation or execution.

## Candidate construction

The candidate uses three observable binary variables `(c,x,y)` and two response actions `{A0,A1}`.

### Training history H-S

Correct action is `A0 iff x XOR y = 1`.

### Training history H-C

Correct action is `A0 iff c XOR x = 1`.

Both histories use the same ordered observable input sequence, with all eight observable states represented equally. Each history therefore contains 192 training trials and balanced action contingencies (96 A0, 96 A1) at the world level.

Candidate training fixture hashes:

- H-S: `72fc6345f2fb58eb2957b23531f01d72c4b042c0b3c96bdf7c5e1637d40bbbc1`
- H-C: `070f5b91e8939058de8087f4b49ca5b3c43006fdef2f24b4d8e2220e2ca5e0a2`

## Candidate future conditions

- A: retain each history's source relation under a new frozen presentation order.
- B: recombine the feature dimensions as `c XOR y`.
- C: invert all binary feature symbols at presentation while preserving the source relation under inverse decoding.
- D: complement the source action mapping.

Each future fixture contains 96 trials and preserves the full three-bit state distribution.

Candidate hashes:

| History | A | B | C | D |
|---|---|---|---|---|
| H-S | `dd4e7ebbde70efdfafdb4f69a75037a6f910a974c4d0e8612b0cb359def360a0` | `63e52a8b937fb572117776a86e20a3e5a931cd224d452275dc71b0816a57da55` | `8d5ac57edb0226fcee1ed79eecd2e6aec110657fd655bfda20ef083318fddc79` | `165e02f9179a674fba419277d0b6746234b1c0ec00458436b64dcd437be77758` |
| H-C | `4d7f768671910828cd327a2921edbcd7f186400b8200de63d75bceccf8044f25` | `63e52a8b937fb572117776a86e20a3e5a931cd224d452275dc71b0816a57da55` | `418ff116fbc99b87aab9d34b15d268690ec80c496095d3953ae8cf33ad6874ca` | `f7d0140ea29834af797df8be8cd01783ddc2ca8c892c62c0e455ddc9b43d58ba` |

## Gate assessment

### Identity — PARTIAL PASS

The state space, action space, training counts, and candidate hashes are explicitly defined. The complete ordered fixture materialization is not yet committed as a final frozen artifact.

### Isolation — CONDITIONAL PASS

A–D have explicit transformations. However, A is currently a continuation/reordering condition rather than a true novel-instance extension because every observable state is already experienced during training. This must be resolved before freeze.

### Accessibility — PASS AT WORLD LEVEL

The environmental input contains only observable `c`, `x`, `y`, action outcomes, and feedback. No relation label or precomputed XOR feature is supplied.

### Reproducibility — PASS AT GENERATOR LEVEL

The candidate construction is deterministically reconstructible from the declared state set, seeds, and rules. A final frozen artifact should still contain the realized ordered trials and hashes rather than relying solely on generator instructions.

### Neutrality — PASS AT WORLD LEVEL, SUBJECT TO MODEL AUDIT

The world defines explicit environmental contingencies. It does not assert that the learner represents them as relations. That interpretation remains a property to be tested by the model and subsequent analysis.

## Critical methodological finding

H-C is not a “no-structure” control. It contains its own explicit parity regularity (`c XOR x`). This is not inherently a defect; it changes the interpretation of H2.

The candidate is therefore best understood as testing:

> **Does learning one observable relational contingency alter future-learning consequences relative to learning a matched-complexity alternative relational contingency?**

It should NOT be described as testing “structural learning versus absence of structural learning.”

This distinction prevents the control from becoming a straw-man learner environment.

## Immediate-performance status

World construction alone cannot establish ACT-R performance matching or equivalent internal state.

The candidate worlds are deliberately symmetric at the world level (same state counts, same trial count, same action marginal, same observable complexity), but actual ACT-R training trajectories must still be computed before matching can be certified.

No post hoc history selection is permitted to manufacture a match.

## Current decision

**World identity:** partial
**World isolation:** conditional
**Accessibility:** pass
**Reproducibility:** pass at generator level
**Neutrality:** pass at world level
**A-condition novelty:** unresolved
**Immediate-performance matching:** unresolved
**H-S/H-C semantic framing:** requires explicit relational-history interpretation
**ACT-R prediction generation:** NOT AUTHORIZED
**Fixture freeze:** NOT AUTHORIZED
**Implementation:** NOT AUTHORIZED
**Execution:** NOT AUTHORIZED

## Next operation

Resolve the A-condition novelty problem and decide whether the intended H2 contrast is explicitly **relation-family transfer** (H-S versus H-C) rather than structure-versus-no-structure. Then materialize and audit the complete ordered fixtures. Only after the world passes those checks should the ACT-R capability envelope be instantiated.
