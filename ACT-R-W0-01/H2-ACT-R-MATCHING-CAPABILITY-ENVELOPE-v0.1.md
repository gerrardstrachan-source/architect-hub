# H2 — ACT-R Matching-Stage Capability Envelope

## Status

**CAPABILITY ENVELOPE v0.1 — MATCHING-STAGE LOCK CANDIDATE**

**No H2 execution is authorized by this document alone.**

## Purpose

This document fixes the ACT-R representational and mechanistic boundary to be used for the immediate-performance matching stage.

The objective of the matching stage is narrow:

> Determine whether the already-fixed H-S and H-C training histories produce comparable observable immediate performance under one predeclared ACT-R realization, without selecting seeds, histories, parameters, or mechanisms after observing results.

The existing H1 model is not copied unchanged because H1 represents only `x,y`, whereas H2 makes `c,x,y` learner-visible. The existing H1 model used utility learning, subsymbolic processing, and explicitly disabled production compilation. citeturn123file0turn124file0

ACT-R's procedural system is composed of procedural, utility, and production-compilation components; production compilation is therefore treated as an explicit architectural choice rather than an implicit inheritance from H1. citeturn182280search1

---

## 1. Frozen learner interface

For every H2 training trial the active ACT-R model receives only:

- context token `c ∈ {0,1}`;
- observable feature `x ∈ {0,1}`;
- observable feature `y ∈ {0,1}`;
- action alternatives `{A0,A1}`;
- environmental feedback after the selected action.

The model is not supplied with:

- the relation name;
- an XOR feature;
- a relation chunk supplied by the experimenter;
- the correct action before selection;
- the identity of H-S or H-C;
- future-condition labels;
- any hidden structural variable.

The world-level relation remains an environmental contingency, not a learner-side representation. The v0.3 world and fixture package define this interface. fileciteturn88file0turn89file0

---

## 2. Active representation

### Goal chunk

The current observable trial is represented in one goal chunk type:

`h2-goal(c,x,y)`

with exactly three binary slots:

- `c`
- `x`
- `y`

No slot for `xor`, `relation`, `rule`, `structure`, or `correct-action` is permitted.

### Action representation

The two response alternatives are represented as the symbolic actions:

`A0`

`A1`

The correct action is not encoded in the action-production conditions.

### Initial state

At the beginning of each seed realization:

- all model buffers are cleared;
- no task-specific relation chunk is preloaded;
- no task-specific production derived from H-S or H-C is preloaded;
- declarative and procedural memory begin from the fixed initialization specified below.

---

## 3. Active matching realization

The following settings are fixed for the immediate-performance matching stage.

### Enabled

**Procedural production matching:** enabled.

**Utility learning:** enabled.

**Subsymbolic processing:** enabled.

**Utility noise / stochastic conflict resolution:** retained under the fixed ACT-R stochastic policy below.

**Goal-buffer representation:** enabled for `c,x,y`.

### Disabled

**Production compilation:** disabled.

**Declarative-memory retrieval:** disabled for the matching realization.

**Imaginal buffer:** disabled / unused.

**Partial matching:** disabled.

**Spreading activation:** disabled because no declarative retrieval explanation is used in this matching realization.

**Visual, auditory, manual, vocal and other perceptual/motor modules:** not part of the task implementation; no unmodeled perceptual or motor timing is included in the primary latency measure.

These exclusions are deliberate model-definition choices, not post hoc simplifications. They keep the matching test focused on observable task-state representation, procedural competition, and learned action preference while preventing an experimenter-supplied declarative relation representation.

The broader H2 adjudication remains aware that declarative memory, chunk construction, and production compilation are legitimate ACT-R mechanisms that may matter to a later architectural adequacy audit. The current matching run cannot activate them after seeing a mismatch. ACT-R's reference manual explicitly treats production compilation as a distinct learning component. citeturn182280search1

---

## 4. Exact general parameters

The active realization inherits the calibrated World-0 parameter family where it remains applicable:

- `:ult t`
- `:esc t`
- `:ul t`
- `:alpha 0.2`
- `:iu 0`
- `:egs 0`
- `:er t`
- `:epl nil`

The existing repository model records these values explicitly. fileciteturn123file0

No parameter may be changed during matching to improve equivalence.

Before the first matching run, the implementation must print and archive the complete ACT-R `sgp` parameter state so that all relevant defaults and module parameters are observable rather than assumed. The ACT-R reference manual specifies that calling `sgp` with no arguments reports the current parameters, including their defaults and documentation. citeturn212961search12

---

## 5. Parameter-freeze rule

The values above constitute the initial fixed parameter set.

Any additional ACT-R module parameter required by the implementation must be explicitly declared in the final machine-readable model manifest **before matching execution**.

No parameter is to be discovered, optimized, widened, narrowed, or selected after inspecting H-S/H-C matching results.

Sensitivity analysis, if later authorized, is a separate adjudication exercise and does not retroactively redefine the primary matching realization.

---

## 6. Stochastic policy

The matching stage uses paired fixed seeds.

### Primary seed set

32 seeds:

`1001–1032`

### Independent replication seed set

32 seeds:

`2001–2032`

For each seed `s`, H-S and H-C are run under the same declared seed value `s`.

Seed identity is assigned before any ACT-R matching result is observed.

No seed may be removed because it produces a poor match.

No new seed may be introduced because it produces a better match.

The full primary and replication seed sets remain part of the analysis regardless of outcome.

The seed policy controls all ACT-R stochastic processes exposed by the implementation. The implementation must record the seed at the start and end of each history realization and record the exact ACT-R random-state configuration used.

---

## 7. Training initialization and independence

Each seed/history realization begins from the same clean ACT-R initialization state.

H-S and H-C therefore differ only through their stipulated training feedback contingencies and the resulting internal history accumulated during training.

The model may not carry state from an H-S run into an H-C run or vice versa.

A matching result is therefore a property of the independently initialized paired realizations, not a result of sequential contamination.

---

## 8. Timing implementation

The primary timing measure is **ACT-R model decision latency**, not human perceptual-motor latency.

For each trial:

`RT_model = t(action-selection-event) - t(stimulus-ready-event)`

where both timestamps are generated from the ACT-R event schedule.

Unmodeled external presentation, motor execution, keyboard, display, or network delays are excluded from the primary latency measure.

The exact event hooks used to establish `stimulus-ready-event` and `action-selection-event` must be fixed in the implementation before matching execution.

If the final implementation cannot produce these two timestamps consistently for every completed trial, latency is marked **NOT AVAILABLE** for the matching decision rather than retroactively reconstructed.

The accuracy and TTC components remain evaluable independently.

---

## 9. Training fixture input

The model consumes the fixed v0.3 repository fixture:

`ACT-R-W0-01/H2-W0.3-COMPLETE-FIXTURES.csv`

The v0.3 world defines:

- 192 training trials per history;
- six training states, each repeated 32 times;
- equal H-S/H-C action marginal of 64 A0 and 128 A1 world-level correct actions;
- fixed A held-out states `010` and `101`;
- fixed future-state schedule for A–D.

The canonical complete-CSV digest is:

`10dc5cfb8a14774d77e951e106c575e289c15bf5503c611ec420c997ae33d32d`

The matching model may read only the training rows during the matching stage. Future-condition rows must not be consumed before the prospective forward-model lock.

---

## 10. Observable outputs for matching

For every seed/history realization the implementation must record:

1. trial-level selected action;
2. trial-level correctness;
3. cumulative accuracy;
4. criterion status;
5. criterion trial when reached;
6. model decision latency when available;
7. ACT-R simulated time;
8. declared model seed;
9. final ACT-R buffer/chunk state required for later audit;
10. complete ACT-R parameter state.

The model is not permitted to expose future-task outcomes to the training process.

---

## 11. Matching protocol dependency

The matching-stage model is evaluated against the previously frozen H2 Immediate-Performance Matching Protocol.

That protocol specifies, before observation:

- full-training accuracy tolerance: ±5 percentage points;
- terminal 32-trial accuracy tolerance: ±5 percentage points;
- TTC tolerance: ±20 trials when both reach criterion;
- `NO-CRITERION` versus `NO-CRITERION` as categorical agreement with no numerical TTC difference;
- one-sided `NO-CRITERION` mismatch as failure;
- median latency tolerance: ±10% when latency is available;
- at least 90% of paired seeds satisfying each applicable component;
- independent primary and replication seed-set confirmation;
- no favorable-seed selection and no post hoc tolerance changes.

The protocol is the decision rule; this document is the model boundary. Neither may silently rewrite the other.

---

## 12. Match-failure consequence

If either the primary or independent replication seed set fails the predeclared matching rule:

**H2 does not advance to the future-learning comparison in its current form.**

The developmental stream may then investigate the failure as a model/design finding, but may not modify the primary model after seeing the failure and retroactively declare the modified model to be the preregistered realization.

---

## 13. Capability-envelope interpretation

The matching realization above is the **primary fixed ACT-R realization**.

The broader legitimate ACT-R capability envelope acknowledges mechanisms that are standard components of ACT-R, including declarative memory, chunk construction, and production compilation, but those mechanisms are not silently introduced if the primary realization fails matching.

Any later mechanism audit must be separately predeclared and must occur before any claim that ACT-R as an architectural account has failed.

This preserves the adjudication hierarchy:

1. data/implementation integrity;
2. representation integrity;
3. parameter integrity;
4. stochastic adequacy;
5. legitimate ACT-R mechanism audit;
6. replication/trajectory stability;
7. architectural adequacy.

---

## 14. Lock status

**Representation:** LOCKED

**Enabled mechanisms:** LOCKED

**Disabled mechanisms:** LOCKED

**Initial parameter family:** LOCKED

**Required complete parameter dump before run:** LOCKED

**Initialization policy:** LOCKED

**Primary seed set:** LOCKED

**Replication seed set:** LOCKED

**Timing definition:** LOCKED

**Future fixture access during matching:** PROHIBITED

**Post-observation tuning:** PROHIBITED

**Favorable-seed selection:** PROHIBITED

**Tolerance changes:** PROHIBITED

**Quantitative A–D forward prediction:** NOT AUTHORIZED BY THIS DOCUMENT

**H2 empirical execution:** NOT AUTHORIZED BY THIS DOCUMENT

---

## Governing principle

> **The model must be fixed before the match is observed. A mismatch is evidence about the fixed model and fixed world; it is never a license to redefine either one.**
