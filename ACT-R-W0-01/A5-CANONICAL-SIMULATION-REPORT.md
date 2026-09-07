# XVII-N.23.3-A.5 — Exact ACT-R Mechanism Simulation

## Status
**CANONICAL SIMULATION ESTABLISHED / RUNTIME MATCH VERIFIED**

## Frozen World-0 input
- 100 trials
- 25 occurrences each of S0, S1, S2, S3
- Fixture ID: `WORLD-0-FIXTURE-20260907-BALANCED-100`
- Fixture SHA256: `687236f1a958549fe6a80cee95e91b922b24398219c6ffbc9a2e5bee55149de4`
- Ground truth remains external to the learner: S0->A0, S1->A1, S2->A1, S3->A0

## Recovered ACT-R mechanisms
- Initial production utility U=0
- Utility learning alpha=0.20
- Utility noise egs=0
- Production compilation disabled
- Tie resolution enabled (`:er t`)
- Tie selection uses ACT-R `permute-list` -> `act-r-random` -> MT19937
- ACT-R `permute-list` consumes one random draw for every iteration, including the final length-1 iteration
- Returned permutation order is the reverse of random-removal order because selected items are consed onto the result
- Random seed = 20260907, offset = 0
- Default ACT-R production action time = 0.05 s
- Effective reward for this task is environment reward minus elapsed selection-to-reward time
- Runtime reward trace confirms +0.95 for correct and -0.05 for incorrect trials

## Exact deterministic simulation result
- Correct: **99/100**
- Accuracy: **99%**
- Incorrect trial: **2 (S0 -> A1)**
- Final 20 trials: 20/20 correct

## ACT-R runtime calibration
Runtime run: `34168859563`
Commit: `0317e9f92469497337092354c148b8d7a661ef65`
Runtime: `7.31.4-<3489.c:2026-06-10>`

The runtime completed all 100 trials on the frozen balanced fixture.

Observed runtime result:
- 99/100 correct
- one error at trial 2: S0 -> A1
- state counts 25/25/25/25

## Simulation/runtime equivalence
The exact simulator reproduces the ACT-R runtime's selected action on **all 100 trials**.

- State/action matches: **100/100**
- Accuracy match: **99/100**
- Final utility state agrees with the runtime trace to reported precision
- RNG count trajectory agrees with the recovered `permute-list` semantics

The earlier 97/100 figure is therefore retained only as a historical, incomplete benchmark. It omitted exact ACT-R permutation/RNG-consumption semantics and is no longer canonical.

Historical chain:

`94% withdrawn`
-> `96% non-canonical`
-> `97% incomplete ACT-R-compatible benchmark`
-> **`99% exact runtime-matched simulation`**

## Secondary multi-seed sensitivity
Using the exact recovered ACT-R mechanisms and the same frozen fixture, seeds 1..1000 give:

- mean accuracy = **98.012%**
- median = **98%**
- range = **96% to 100%**
- 96%: 67 seeds
- 97%: 234 seeds
- 98%: 373 seeds
- 99%: 272 seeds
- 100%: 54 seeds

This remains a secondary sensitivity analysis. The canonical fixed-seed result is 99/100.

## Provenance corrections preserved
- Earlier 101-entry controller defect: one extra trailing S1 was removed.
- Subsequent 25/24/26/25 balance defect: replaced by the formally frozen 25/25/25/25 fixture.
- TLS acquisition incompatibility: resolved without disabling certificate verification.
- Read-only ACT-R source loading: resolved by copying the official source into a writable container path before loading.
- Runtime evidence-directory permission defect: corrected.
- Simulation RNG mismatch: resolved by reproducing the complete ACT-R `permute-list` draw consumption and ordering.

## Epistemic boundary
This calibration establishes behavioral equivalence between the exact simulator and the specified ACT-R 7.31.4 runtime under World 0. It is evidence about the implementation's behavior in this controlled computational environment.

It is **not** evidence that ACT-R uniquely explains human learning, and it is **not** evidence that ACT-R has captured psychological understanding.

The laboratory can now move to prospective **model competition** using the frozen World-0 environment and held-out future conditions.
