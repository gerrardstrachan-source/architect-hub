;;; ACT-R-W0-01 external World-0 controller.
;;; Ground truth is intentionally outside the learner model.

(defparameter *w0-truth*
  '((S0 . A0) (S1 . A1) (S2 . A1) (S3 . A0)))

;; FORMALLY FROZEN WORLD-0 FIXTURE.
;; 100 trials; exactly 25 occurrences of each state.
;; Fixture ID: WORLD-0-FIXTURE-20260907-BALANCED-100
;; Sequence SHA256: 687236f1a958549fe6a80cee95e91b922b24398219c6ffbc9a2e5bee55149de4
;; The fixture order is a separate provenance object from the ACT-R learner RNG.
(defparameter *w0-sequence*
  '(S1 S0 S2 S3 S2 S2 S1 S0 S0 S3 S2 S0 S1 S3 S0 S3 S1 S1 S1 S0
    S3 S0 S0 S2 S1 S2 S1 S1 S3 S2 S0 S1 S3 S2 S1 S3 S3 S3 S0 S1
    S3 S3 S1 S2 S3 S3 S0 S2 S1 S1 S2 S1 S3 S2 S2 S1 S3 S2 S2 S0
    S1 S2 S3 S3 S3 S0 S3 S1 S3 S2 S0 S2 S1 S2 S0 S2 S0 S1 S3 S2
    S2 S1 S3 S0 S0 S2 S0 S1 S1 S3 S0 S0 S0 S3 S2 S1 S2 S0 S0 S0))

(defparameter *w0-trial-index* 0)
(defparameter *w0-current-trial* nil)
(defparameter *w0-log* nil)
(defparameter *w0-seed* nil)
(defparameter *w0-output-file* nil)
(defparameter *w0-selection-counts* (make-hash-table :test #'equal))

(defun w0-lookup-truth (state)
  (cdr (assoc state *w0-truth*)))

(defun w0-productions ()
  '(S0-A0 S0-A1 S1-A0 S1-A1 S2-A0 S2-A1 S3-A0 S3-A1))

(defun w0-current-utilities ()
  (mapcar (lambda (p)
            (list p (caar (spp-fct (list p :utility :u)))))
          (w0-productions)))

(defun w0-production-count ()
  (length (all-productions)))

(defun w0-rng-state ()
  (no-output (sgp :seed)))

(defun w0-write-row (stream entry)
  (format stream "~D,~A,~A,~A,~D,~D,~A,~S,~S,~A,~A~%"
          (getf entry :trial) (getf entry :state)
          (getf entry :selected-production) (getf entry :action)
          (getf entry :correctness) (getf entry :environment-reward)
          (or (getf entry :actr-time-action) 0)
          (getf entry :utility-before) (getf entry :utility-after)
          (getf entry :seed) (getf entry :production-count-after)))

(defun w0-write-log ()
  (with-open-file (stream *w0-output-file* :direction :output
                          :if-exists :supersede :if-does-not-exist :create)
    (format stream "trial,state,production,action,correctness,environment_reward,actr_time_action,utility_before,utility_after,seed,production_count_after~%")
    (dolist (entry (reverse *w0-log*)) (w0-write-row stream entry))))

(defun w0-record-trial (state production action env-reward correctness before-utils rng-before)
  (let ((entry (list :trial *w0-current-trial* :state state
                     :selected-production production :action action
                     :correctness correctness :environment-reward env-reward
                     :utility-before before-utils :utility-after nil
                     :actr-time-action (mp-time-ms) :actr-time-reward nil
                     :seed *w0-seed* :production-count-after nil
                     :rng-before rng-before)))
    (push entry *w0-log*)
    (incf (gethash (list state action) *w0-selection-counts* 0))
    (format t "W0-TRIAL trial=~D state=~A production=~A action=~A correct=~D env_reward=~D time_ms=~D rng_state=~S~%"
            *w0-current-trial* state production action correctness env-reward (mp-time-ms) rng-before)))

(defun w0-action (state action production)
  (unless *w0-current-trial* (error "W0 action occurred without an active trial."))
  (let* ((rng-before (w0-rng-state))
         (before-utils (w0-current-utilities))
         (truth (w0-lookup-truth state))
         (correctness (if (eql action truth) 1 0))
         (env-reward (if (= correctness 1) 1 0)))
    (w0-record-trial state production action env-reward correctness before-utils rng-before)
    (trigger-reward env-reward)
    (schedule-event-relative 0.001 'w0-finish-trial :maintenance t :priority :min)))

(defun w0-present-state (state)
  ;; Use the function form because the macro form does not evaluate STATE here.
  (goal-focus-fct
   (ecase state
     (S0 'G-S0)
     (S1 'G-S1)
     (S2 'G-S2)
     (S3 'G-S3))))

(defun w0-finish-trial ()
  (let ((entry (car *w0-log*)))
    (when entry
      (setf (getf entry :utility-after) (w0-current-utilities))
      (setf (getf entry :actr-time-reward) (mp-time-ms))
      (setf (getf entry :production-count-after) (w0-production-count))))
  (if (< *w0-trial-index* (length *w0-sequence*))
      (progn (incf *w0-trial-index*)
             (setf *w0-current-trial* *w0-trial-index*)
             (w0-present-state (nth (1- *w0-trial-index*) *w0-sequence*)))
      (progn (setf *w0-current-trial* nil) (w0-stop))))

(defun w0-stop ()
  (w0-write-log)
  (format t "W0-COMPLETE trials=~D seed=~D production-count=~D~%"
          (length *w0-log*) *w0-seed* (w0-production-count))
  (format t "W0-FINAL-UTILITIES ~S~%" (w0-current-utilities))
  (format t "W0-SELECTION-COUNTS ~S~%"
          (loop for k being the hash-keys of *w0-selection-counts* using (hash-value v)
                collect (list k v)))
  nil)

(defun run-w0 (&optional (seed 20260907) (output-file "w0-results.csv"))
  (reset)
  (sgp-fct (list :seed (list seed 0)))
  (setf *w0-seed* seed *w0-output-file* output-file
        *w0-trial-index* 1 *w0-current-trial* 1 *w0-log* nil
        *w0-selection-counts* (make-hash-table :test #'equal))
  (format t "W0-CONFIG seed=~D productions=~D~%" seed (w0-production-count))
  (format t "W0-INITIAL-RNG-STATE ~S~%" (w0-rng-state))
  (format t "W0-INITIAL-UTILITIES ~S~%" (w0-current-utilities))
  (w0-present-state (first *w0-sequence*))
  (run 1000)
  (unless (null *w0-current-trial*)
    (error "W0 run ended before all planned trials completed.")))
