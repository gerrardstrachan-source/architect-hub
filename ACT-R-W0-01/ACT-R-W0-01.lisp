;;; ACT-R-W0-01 learner model
;;; Target: official ACT-R 7.31.4 release.
;;; Scientific status: calibration model; no World-0 ground-truth mapping is encoded.

(clear-all)

(define-model ACT-R-W0-01
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

  ;; Explicitly represented observable states only.
  (define-chunks
    (g-s0 isa w0-goal x 0 y 0)
    (g-s1 isa w0-goal x 0 y 1)
    (g-s2 isa w0-goal x 1 y 0)
    (g-s3 isa w0-goal x 1 y 1))

  ;; Two competing action candidates per represented state.
  ;; The correct action is NOT encoded here.
  (p S0-A0
     =goal> isa w0-goal x 0 y 0
     ==>
     !eval! (w0-action 'S0 'A0 'S0-A0)
     -goal>)

  (p S0-A1
     =goal> isa w0-goal x 0 y 0
     ==>
     !eval! (w0-action 'S0 'A1 'S0-A1)
     -goal>)

  (p S1-A0
     =goal> isa w0-goal x 0 y 1
     ==>
     !eval! (w0-action 'S1 'A0 'S1-A0)
     -goal>)

  (p S1-A1
     =goal> isa w0-goal x 0 y 1
     ==>
     !eval! (w0-action 'S1 'A1 'S1-A1)
     -goal>)

  (p S2-A0
     =goal> isa w0-goal x 1 y 0
     ==>
     !eval! (w0-action 'S2 'A0 'S2-A0)
     -goal>)

  (p S2-A1
     =goal> isa w0-goal x 1 y 0
     ==>
     !eval! (w0-action 'S2 'A1 'S2-A1)
     -goal>)

  (p S3-A0
     =goal> isa w0-goal x 1 y 1
     ==>
     !eval! (w0-action 'S3 'A0 'S3-A0)
     -goal>)

  (p S3-A1
     =goal> isa w0-goal x 1 y 1
     ==>
     !eval! (w0-action 'S3 'A1 'S3-A1)
     -goal>)
)
