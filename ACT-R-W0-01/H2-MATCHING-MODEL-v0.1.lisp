;;; H2 Matching Learner v0.1
;;; Purpose: immediate-performance matching only.
;;; Frozen boundary: h2-goal(c,x,y); utility learning + subsymbolic processing.
;;; Exactly the frozen learner-visible representation.

(clear-all)

(define-model H2-MATCHING
  (sgp
    :v t
    :trace-detail high
    :ult t
    :esc t
    :ul t
    :alpha 0.2
    :iu 0
    :egs 0
    :er t
    :epl nil)

  (chunk-type h2-goal c x y)

  (define-chunks
    (G-000 isa h2-goal c 0 x 0 y 0)
    (G-001 isa h2-goal c 0 x 0 y 1)
    (G-011 isa h2-goal c 0 x 1 y 1)
    (G-100 isa h2-goal c 1 x 0 y 0)
    (G-110 isa h2-goal c 1 x 1 y 0)
    (G-111 isa h2-goal c 1 x 1 y 1))

  (p P-000-A0 =goal> isa h2-goal c 0 x 0 y 0 ==> !eval! (h2-action 0 :A0 'P-000-A0) -goal>)
  (p P-000-A1 =goal> isa h2-goal c 0 x 0 y 0 ==> !eval! (h2-action 0 :A1 'P-000-A1) -goal>)
  (p P-001-A0 =goal> isa h2-goal c 0 x 0 y 1 ==> !eval! (h2-action 1 :A0 'P-001-A0) -goal>)
  (p P-001-A1 =goal> isa h2-goal c 0 x 0 y 1 ==> !eval! (h2-action 1 :A1 'P-001-A1) -goal>)
  (p P-011-A0 =goal> isa h2-goal c 0 x 1 y 1 ==> !eval! (h2-action 3 :A0 'P-011-A0) -goal>)
  (p P-011-A1 =goal> isa h2-goal c 0 x 1 y 1 ==> !eval! (h2-action 3 :A1 'P-011-A1) -goal>)
  (p P-100-A0 =goal> isa h2-goal c 1 x 0 y 0 ==> !eval! (h2-action 4 :A0 'P-100-A0) -goal>)
  (p P-100-A1 =goal> isa h2-goal c 1 x 0 y 0 ==> !eval! (h2-action 4 :A1 'P-100-A1) -goal>)
  (p P-110-A0 =goal> isa h2-goal c 1 x 1 y 0 ==> !eval! (h2-action 6 :A0 'P-110-A0) -goal>)
  (p P-110-A1 =goal> isa h2-goal c 1 x 1 y 0 ==> !eval! (h2-action 6 :A1 'P-110-A1) -goal>)
  (p P-111-A0 =goal> isa h2-goal c 1 x 1 y 1 ==> !eval! (h2-action 7 :A0 'P-111-A0) -goal>)
  (p P-111-A1 =goal> isa h2-goal c 1 x 1 y 1 ==> !eval! (h2-action 7 :A1 'P-111-A1) -goal>))
