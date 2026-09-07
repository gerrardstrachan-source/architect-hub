;;; H1 held-out-state ACT-R model.
;;; Training exposes S0/S1/S2 only. S3 is held out and receives no feedback.

(clear-all)

(define-model ACT-R-W0-H1
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

  (chunk-type w0-goal x y)

  (define-chunks
    (g-s0 isa w0-goal x 0 y 0)
    (g-s1 isa w0-goal x 0 y 1)
    (g-s2 isa w0-goal x 1 y 0)
    (g-s3 isa w0-goal x 1 y 1))

  (p S0-A0 =goal> isa w0-goal x 0 y 0 ==>
     !eval! (h1-action 'S0 'A0 'S0-A0)
     -goal>)
  (p S0-A1 =goal> isa w0-goal x 0 y 0 ==>
     !eval! (h1-action 'S0 'A1 'S0-A1)
     -goal>)
  (p S1-A0 =goal> isa w0-goal x 0 y 1 ==>
     !eval! (h1-action 'S1 'A0 'S1-A0)
     -goal>)
  (p S1-A1 =goal> isa w0-goal x 0 y 1 ==>
     !eval! (h1-action 'S1 'A1 'S1-A1)
     -goal>)
  (p S2-A0 =goal> isa w0-goal x 1 y 0 ==>
     !eval! (h1-action 'S2 'A0 'S2-A0)
     -goal>)
  (p S2-A1 =goal> isa w0-goal x 1 y 0 ==>
     !eval! (h1-action 'S2 'A1 'S2-A1)
     -goal>)
  (p S3-A0 =goal> isa w0-goal x 1 y 1 ==>
     !eval! (h1-action 'S3 'A0 'S3-A0)
     -goal>)
  (p S3-A1 =goal> isa w0-goal x 1 y 1 ==>
     !eval! (h1-action 'S3 'A1 'S3-A1)
     -goal>))
