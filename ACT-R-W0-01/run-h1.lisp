;;; H1 held-out-state external controller.
;;; Training: 75 trials containing S0/S1/S2 only, with feedback.
;;; Holdout: 25 S3 trials, explicitly no feedback/reward.

(defparameter *h1-truth*
  '((S0 . A0) (S1 . A1) (S2 . A1) (S3 . A0)))

(defparameter *h1-sequence*
  '(S1 S0 S2 S3 S2 S2 S1 S0 S0 S3 S2 S0 S1 S3 S0 S3 S1 S1 S1 S0
    S3 S0 S0 S2 S1 S2 S1 S1 S3 S2 S0 S1 S3 S2 S1 S3 S3 S3 S0 S1
    S3 S3 S1 S2 S3 S3 S0 S2 S1 S1 S2 S1 S3 S2 S2 S1 S3 S2 S2 S0
    S1 S2 S3 S3 S3 S0 S3 S1 S3 S2 S0 S2 S1 S2 S0 S2 S0 S1 S3 S2
    S2 S1 S3 S0 S0 S2 S0 S1 S1 S3 S0 S0 S0 S3 S2 S1 S2 S0 S0 S0
    S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3 S3))

(defparameter *h1-trial-index* 0)
(defparameter *h1-current-trial* nil)
(defparameter *h1-log* nil)
(defparameter *h1-seed* nil)
(defparameter *h1-output-file* nil)
(defparameter *h1-training-trials* 75)

(defun h1-lookup-truth (state) (cdr (assoc state *h1-truth*)))
(defun h1-rng-state () (no-output (sgp :seed)))

(defun h1-write-log ()
  (with-open-file (stream *h1-output-file* :direction :output
                          :if-exists :supersede :if-does-not-exist :create)
    (format stream "trial,phase,state,production,action,correctness,feedback,rng_state~%")
    (dolist (entry (reverse *h1-log*))
      (format stream "~D,~A,~A,~A,~A,~D,~D,~S~%"
              (getf entry :trial) (getf entry :phase) (getf entry :state)
              (getf entry :production) (getf entry :action) (getf entry :correctness)
              (getf entry :feedback) (getf entry :rng-state)))))

(defun h1-action (state action production)
  (unless *h1-current-trial* (error "H1 action occurred without active trial."))
  (let* ((feedback (= *h1-current-trial* 1))
         (truth (h1-lookup-truth state))
         (correctness (if (eql action truth) 1 0)))
    ;; Phase boundary: trials <= training-trials receive feedback; holdout does not.
    (setf feedback (<= *h1-current-trial* *h1-training-trials*))
    (push (list :trial *h1-current-trial*
                :phase (if feedback 'TRAIN 'HOLDOUT)
                :state state :production production :action action
                :correctness correctness :feedback (if feedback 1 0)
                :rng-state (h1-rng-state))
          *h1-log*)
    (when feedback
      (trigger-reward (if (= correctness 1) 1 0)))
    (schedule-event-relative 0.001 'h1-finish-trial :maintenance t :priority :min)))

(defun h1-present-state (state)
  (goal-focus-fct
   (ecase state
     (S0 'G-S0) (S1 'G-S1) (S2 'G-S2) (S3 'G-S3))))

(defun h1-finish-trial ()
  (if (< *h1-trial-index* (length *h1-sequence*))
      (progn
        (incf *h1-trial-index*)
        (setf *h1-current-trial* *h1-trial-index*)
        (h1-present-state (nth (1- *h1-trial-index*) *h1-sequence*)))
      (progn
        (setf *h1-current-trial* nil)
        (h1-write-log)
        (format t "H1-COMPLETE trials=~D training=~D holdout=~D seed=~D production-count=~D~%"
                (length *h1-sequence*) *h1-training-trials*
                (- (length *h1-sequence*) *h1-training-trials*) *h1-seed*
                (length (all-productions))))))

(defun run-h1 (&optional (seed 20260907) (output-file "h1-results.csv"))
  (reset)
  (sgp-fct (list :seed (list seed 0)))
  (setf *h1-seed* seed *h1-output-file* output-file
        *h1-trial-index* 1 *h1-current-trial* 1 *h1-log* nil)
  (format t "H1-CONFIG seed=~D trials=~D training=~D holdout=~D~%"
          seed (length *h1-sequence*) *h1-training-trials*
          (- (length *h1-sequence*) *h1-training-trials*))
  (h1-present-state (first *h1-sequence*))
  (run 1000)
  (unless (null *h1-current-trial*)
    (error "H1 run ended before all planned trials completed.")))
