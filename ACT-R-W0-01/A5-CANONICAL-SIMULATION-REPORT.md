# XVII-N.23.3-A.5 — Canonical ACT-R-Compatible Simulation

## Status
CANONICAL SIMULATION ESTABLISHED / RUNTIME COMPARISON PENDING

## Frozen World-0 input
- 100 trials
- 25 occurrences each of S0, S1, S2, S3
- Sequence generated deterministically from seed 20260907 and preserved in the corrected controller
- Ground truth remains external to the learner: S0->A0, S1->A1, S2->A1, S3->A0

## Frozen ACT-R-compatible mechanisms
- Initial production utility U=0
- Utility learning alpha=0.20
- Utility noise egs=0
- Production compilation disabled
- Tie resolution enabled (:er t)
- Tie selection uses ACT-R permute-list -> act-r-random -> MT19937 stream
- Random seed = 20260907, offset = 0
- Default ACT-R production action time = 0.05 s
- Utility propagation uses effective reward R = environment reward - elapsed selection-to-reward time
- For this deterministic task, the 0.05 s action-time assumption yields effective reward +0.95 on correct trials and -0.05 on incorrect trials

## Canonical deterministic simulation result
- Correct: 97/100
- Accuracy: 97%
- Final 20 trials: 20/20 correct
- State accuracies: S0 24/25, S1 24/25, S2 24/25, S3 25/25
- Incorrect trials: 5, 8, 1 (one each for S1, S0, S2)

## Final production utilities
- S0-A0 = 0.945513751841
- S0-A1 = -0.010000000000
- S1-A0 = -0.010000000000
- S1-A1 = 0.945513751841
- S2-A0 = -0.010000000000
- S2-A1 = 0.945513751841
- S3-A0 = 0.946411001473
- S3-A1 = 0

## Secondary multi-seed sensitivity
For seeds 1..1000 with the same fixed World-0 sequence and ACT-R-compatible mechanisms:
- mean accuracy = 97.988%
- median = 98%
- range = 96% to 100%
- 96%: 54 seeds
- 97%: 272 seeds
- 98%: 373 seeds
- 99%: 234 seeds
- 100%: 67 seeds

This multi-seed analysis is secondary sensitivity analysis only. It is not the canonical fixed-seed prediction.

## Historical corrections
- 94% result: WITHDRAWN because the stochastic simulation procedure was under-specified.
- 96% result: NON-CANONICAL; generated under a different simulation procedure.
- Previous GitHub controller copy containing 101 trials: CORRECTED; one extra trailing S1 removed.

## Epistemic boundary
This artifact is a reproducible simulation of recovered ACT-R mechanisms. It is NOT ACT-R runtime execution and is NOT empirical evidence about human understanding. The next empirical test is execution with ACT-R 7.31.4 followed by direct trace comparison.