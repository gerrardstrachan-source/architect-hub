# H1 Evidence / Discrimination Record

**Test ID:** WORLD-0-H1-HELDOUT-S3-20260907  
**Repository:** gerrardstrachan-source/architect-hub  
**Validated implementation commit:** `19f0306a014bf0d6fcbbeb6c4c0577a72508f730`  
**H1 workflow run:** `34749280915`  
**H1 runtime job:** `103702741389`  
**Runtime evidence artifact:** `actr-w0-h1-runtime-evidence`  
**Artifact ID:** `10314963135`  
**Artifact SHA-256:** `8224cb680b8c40a879f09a33d69ed4ebbfdd747ca98106700c0a086ba5c62e78`

## Frozen experimental contract

- 100 total trials
- 75 training trials
- 25 holdout trials
- Training counts: S0=25, S1=25, S2=25, S3=0
- Holdout: 25 × S3
- No holdout feedback/reward
- ACT-R seed: 20260907
- Frozen H1 sequence SHA-256: `b734491084c3c41dcf100bb57f1ba09e3b17eb2e16721d336d6aeb92e44ebe46`
- ACT-R release verified at runtime: 7.31.4-<3489.c:2026-06-10>

## Runtime verification

The post-correction H1 workflow completed successfully. The runtime executed all 100 planned trials and uploaded the preserved evidence artifact.

The trial-level CSV was independently inspected and contains exactly 100 records. Training and holdout phases conform to the frozen contract. All holdout records have `feedback=0`.

## Observed H1 runtime

Training action counts:

| State | A0 | A1 |
|---|---:|---:|
| S0 | 24 | 1 |
| S1 | 0 | 25 |
| S2 | 0 | 25 |

Holdout S3 action counts:

- A0 = 14
- A1 = 11
- Accuracy = 14/25 = 56%

## Locked model predictions

### State-specific ACT-R

S3 is absent from training, so the S3-A0 and S3-A1 alternatives remain without differential learned utility. The locked prediction is stochastic A0/A1 selection, approximately 50/50 in the stated test condition.

### Bayesian Boolean learner

The training cases S0→A0, S1→A1, S2→A1 select XOR within the locked hypothesis class, giving the deterministic prediction S3→A0.

## Model discrimination

The observed runtime outcome differs from the deterministic Bayesian/XOR prediction: 11 of 25 S3 trials selected A1, whereas Bayesian/XOR predicts A0 on every S3 trial.

The observed ACT-R distribution, 14 A0 / 11 A1, is compatible with the locked stochastic state-specific ACT-R prediction. Under an exact p=0.5 binomial model, the probability of exactly 14 A0 selections in 25 trials is approximately 0.13284. This is not evidence that p=0.5 is proven; it establishes that the observed count is not unusual under the locked stochastic account.

For the deterministic Bayesian prediction, the observed A1 count directly contradicts the locked 25/25 A0 prediction.

**H1 model discrimination: PASS.**

## Epistemic boundaries

This record establishes a model-discriminating empirical result. It does **not** establish that the learner understands XOR, that an internal understanding state has been observed, or that an architectural residual has been found.

The next scientific question is whether the observed phenomenon requires an explanatory mechanism absent from the surviving account(s), or whether existing ACT-R mechanisms already explain it.

## Provenance boundary

- Historical/clean simulation observation: **14/25**
- First post-repair attempt: **105-state validation failure; zero H1 trials executed**
- Corrected implementation: **19f0306a014bf0d6fcbbeb6c4c0577a72508f730**
- First valid H1 ACT-R 7.31.4 runtime: **14/25 (56%)**

The runtime result is independent evidence from the preserved ACT-R execution artifact and must not be conflated with the prior simulation result.
