# H2 — Forward-Model Readiness Audit

**Status:** FORWARD-MODEL CONSTRUCTION BLOCKED FROM QUANTITATIVE PREDICTION

**H2:** prospective only; no empirical H2 data exist.

**H1:** frozen and closed.

## 1. Objective

Construct the prospective ACT-R account required by H2 v0.2 and determine whether its A–D predictions can be generated without importing post hoc assumptions.

## 2. Surviving baseline available

The existing calibrated World-0 ACT-R model establishes a valid starting architectural pattern:

- observable binary feature representation through goal chunks;
- competing productions for action selection;
- utility learning enabled;
- subsymbolic processing enabled;
- utility noise and stochasticity explicitly controllable;
- production compilation explicitly disabled in the H1 calibration model.

H2, however, explicitly requires a broader capability envelope to be declared rather than automatically inheriting H1's constrained implementation.

## 3. Candidate H2 ACT-R architecture

The forward model must be constructed from the following declared layers, with each mechanism explicitly enabled or disabled before empirical execution:

1. **Perceptual / task interface:** receives only the observable context token and binary features supplied by the formal world.
2. **Goal representation:** encodes current task information without a precomputed relational feature such as XOR.
3. **Procedural system:** competing action procedures selected from the current ACT-R state.
4. **Utility learning:** updates action/production preferences from stipulated feedback.
5. **Declarative memory:** available only if explicitly required by the task and model account.
6. **Chunk construction:** available only under declared ACT-R learning rules; no experimenter-supplied relation chunk.
7. **Production compilation:** must be explicitly decided and parameterized rather than silently inherited from H1.
8. **Retrieval/activation mechanisms:** must be declared only where they participate in the intended explanation.
9. **Stochasticity:** fixed primary and replication seed sets must be declared before prediction generation.

This is a model specification boundary, not permission to implement or execute H2.

## 4. Critical construction result

Quantitative forward prediction is **not yet scientifically identifiable** from H2 v0.2.

The v0.2 document defines classes of training histories and future conditions, but it does not yet provide the exact objects required to run the forward model deterministically:

- exact H-S training contingency table;
- exact H-C training contingency table;
- exact trial order for H-S;
- exact trial order for H-C;
- exact performance-matching algorithm and admissibility window values;
- exact response-time matching rule;
- exact future-task fixture for A;
- exact future-task fixture for B;
- exact future-task fixture for C;
- exact future-task fixture for D;
- exact criterion definition and thresholds;
- exact retention interval, if used;
- exact ACT-R mechanism set and parameter values for the final H2 realization.

Therefore a numerical prediction made now would necessarily choose values that the scientific specification has not yet locked.

That would create a post hoc model specification rather than a prospective prediction.

## 5. Why this is a scientific blocker

The requested chain is:

**formal world → exact training history → ACT-R internal state → future condition → predicted trajectory**

Without the exact training history, the ACT-R state at the future-block boundary is not uniquely determined.

Without exact future fixtures, the input sequence driving the predicted trajectory is not uniquely determined.

Without the exact capability envelope and parameters, the transition dynamics are not uniquely determined.

Accordingly, there is currently no single defensible numerical A–D prediction to freeze.

## 6. No numerical predictions generated

No A–D percentage, trial-to-criterion estimate, error curve, interference cost, or transfer distribution is being promoted as a prospective prediction at this stage.

Any such number generated before the missing locks are fixed would be exploratory analysis, not preregistered prediction.

## 7. Required next construction step

Before quantitative prediction generation, the laboratory must construct and freeze:

### Lock F1 — Training contingencies

A complete H-S/H-C specification with equalized observable marginals, exact contingency tables, exact trial order, feedback schedule, and cryptographic hashes.

### Lock F2 — Matching protocol

A numerical admissibility rule for immediate-performance matching, including rejection rules and no post hoc selection.

### Lock F3 — Future fixtures

Exact A/B/C/D trial sequences, with mathematical declarations of manipulated and invariant variables and hashes.

### Lock F4 — Final ACT-R capability envelope

Exact enabled/disabled mechanisms, parameter values, initialization state, and seed policy.

### Lock F5 — Forward simulator

A non-empirical prediction runner that consumes only the frozen training and future fixtures plus the frozen ACT-R model specification.

### Lock F6 — Prediction freeze

Generate the complete A–D distributional prediction package before any H2 future-task runtime is executed.

## 8. Current verdict

**ACT-R architectural starting point:** READY

**H2 full capability envelope:** SPECIFICATION-LEVEL READY; exact mechanism decisions pending

**Training fixture:** NOT FROZEN

**Control fixture:** NOT FROZEN

**Future A–D fixtures:** NOT FROZEN

**Quantitative ACT-R predictions:** NOT GENERATED

**Prediction freeze:** NOT REACHED

**H2 implementation:** NOT AUTHORIZED

**H2 execution:** NOT AUTHORIZED

## Governing principle

> **A quantitative prediction is prospective only when the model, inputs, parameters, stochastic policy, and evaluation rule are fixed before the observation it is intended to predict.**

The absence of a numerical prediction at this stage is therefore not a failure of the developmental stream. It is the correct refusal to manufacture one from an underspecified experimental world.
