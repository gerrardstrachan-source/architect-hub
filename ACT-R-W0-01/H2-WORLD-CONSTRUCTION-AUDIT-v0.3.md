# H2 World Construction Audit v0.3

## Status
**Candidate v0.3 — action-marginal repair complete — NOT FROZEN — NOT EXECUTABLE**

## Defect resolved

The v0.2 candidate incorrectly declared equal training action marginals. Under the locked contingencies and v0.2 six-state training set, H-S produced 128 A0 / 64 A1 while H-C produced 96 A0 / 96 A1. This was a genuine world-level confound.

v0.3 repairs the defect by the smallest state-set substitution found: training states `010` and `101` are removed, and `001` and `100` are introduced.

Active training states:
`000, 001, 011, 100, 110, 111`

Held-out A states:
`010, 101`

Each training state occurs exactly 32 times.

## Training contingency audit

H-S:
`A0 iff x XOR y = 1`

H-C:
`A0 iff c XOR x = 1`

Across the active six training states, both histories produce exactly:
- A0: 2 states × 32 = 64 trials
- A1: 4 states × 32 = 128 trials

Therefore training action-frequency marginals are exactly identical.

Feature marginals are also balanced and identical:
- c: 96 zeros / 96 ones
- x: 96 zeros / 96 ones
- y: 96 zeros / 96 ones

The ordered observable input sequence is identical across H-S and H-C.

## Why this repair is preferable

The repair changes only which two joint states are withheld. It retains:
- three binary learner-facing variables;
- two actions;
- six training states;
- 32 repetitions per training state;
- 192 training trials;
- identical observable order across histories;
- legitimate distinct relational contingencies;
- A as a held-out joint-state extension.

It does not alter ACT-R parameters or use sequence manipulation to compensate for a contingency imbalance.

## A novelty

Training completely omits `010` and `101`. A is the first condition in which those exact joint conjunctions occur.

All primitive values 0/1 for c, x, and y have already occurred during training. Thus A novelty remains joint-state novelty rather than new-symbol novelty.

## Adversarial results

Identity: PASS
State exposure matching: PASS
Order matching: PASS
Trial-count matching: PASS
Training action-marginal equality: PASS
Training feature-marginal equality: PASS
A-condition novelty: PASS
Accessibility: PASS
Reproducibility: PASS
Neutrality: PASS at world level
H-S/H-C interpretation: LOCKED as matched relational-history transfer

Immediate-performance matching: NOT TESTED
ACT-R prediction: NOT AUTHORIZED
Fixture freeze: NOT AUTHORIZED
H2 implementation: NOT AUTHORIZED
H2 execution: NOT AUTHORIZED

## Fixture

The canonical ordered state sequences are committed in:
`ACT-R-W0-01/H2-W0.3-STATE-SEQUENCES.json`

An exact local CSV materialization containing all 1,152 H-S/H-C training and A/B/C/D future rows was independently validated.

Combined local CSV SHA-256:
`75db87c5c0d3ec8fca8033ea7ff348d4ded602347612cce9fe6e6ac0343b7941`

Training source-state sequence SHA-256:
`5fb17bee3cca914261cd2fb6db6e5cf0411b63425aca9aec4db0639343e3d9e3`

Future source-state sequence SHA-256:
`285809022276e6f2789a8b94f79f6a0245238fba6c6960213254ac24dd951451`

## Current frontier

The action-frequency confound is RESOLVED at the world level.

The world therefore clears the specifically challenged gate, but this does **not** establish immediate-performance matching. Matching remains a model-level question and cannot be solved retrospectively by parameter tuning.

No ACT-R forward prediction is authorized by this audit.
