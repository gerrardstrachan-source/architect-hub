# H2 — ACT-R Matching-Stage Lock Record v0.1

## Status

**MATCHING MODEL BOUNDARY — FROZEN**

This record freezes the ACT-R realization used for the immediate-performance matching gate. It does not authorize future-condition execution or final A–D prediction generation.

## Frozen components

- learner-visible representation: `h2-goal(c,x,y)` with exactly three binary slots;
- action set: `{A0,A1}`;
- procedural matching: enabled;
- utility learning: enabled;
- subsymbolic processing: enabled;
- production compilation: disabled;
- declarative retrieval: disabled;
- imaginal: disabled/unused;
- partial matching: disabled;
- spreading activation: disabled;
- perceptual/motor modules: not part of the task realization;
- fixed general parameters from the calibrated World-0 family;
- clean initialization before every history/seed realization;
- paired primary seeds `1001–1032`;
- paired independent replication seeds `2001–2032`;
- ACT-R random-module seed form `[integer,0]`;
- primary timing definition: model decision latency between stimulus-ready and action-selection events;
- future-condition rows inaccessible during matching.

The current model boundary intentionally does not inherit H1's `x,y`-only representation because H2 makes `c,x,y` learner-visible. The H1 implementation is therefore preserved as historical calibration, not as the H2 representation. fileciteturn123file0turn124file0

## Prospective boundary

The model is now fixed **before matching outcomes are observed**.

A matching failure therefore cannot trigger parameter tuning, seed replacement, mechanism activation, tolerance changes, or history substitution within the primary matching realization.

The matching protocol remains the independent decision rule and requires both primary and replication seed sets to pass. No individual favorable realization may be selected.

## ACT-R randomization basis

The ACT-R reference manual defines a dedicated random module using a Mersenne Twister generator and an explicit `:seed` parameter represented as a two-number seed/offset value. citeturn204424search12

The frozen H2 policy uses an offset of zero for each declared initialization integer.

## Current authorization boundary

**Capability envelope:** FROZEN

**Immediate-performance matching implementation:** MAY NOW BE CONSTRUCTED AND VALIDATED AGAINST THE LOCK

**Matching execution:** NOT YET AUTHORIZED by this record alone

**A–D quantitative forward prediction:** NOT AUTHORIZED

**H2 empirical future-task execution:** NOT AUTHORIZED

**Residual claim:** NOT ESTABLISHED

## Governing principle

> **The matching model is fixed first. The observed match or mismatch belongs to the model; the model is not rewritten to belong to the observed match.**
