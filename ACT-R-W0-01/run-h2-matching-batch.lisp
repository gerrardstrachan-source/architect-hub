;;; H2 matching batch launcher v0.1
;;; Execution-only helper. It uses the frozen seed lists exactly.
;;; It does not consume any future-condition fixture.

(defun h2-run-seed-list (history seeds input-file output-dir label)
  (dolist (seed seeds)
    (run-h2-history-seed history seed input-file
                         (format nil "~A/~A-~A-~D.csv" output-dir history label seed))))

(defun run-h2-matching-primary (input-file output-dir)
  (ensure-directories-exist (pathname (format nil "~A/" output-dir)))
  (h2-run-seed-list 'H-S *h2-seeds-primary* input-file output-dir "primary")
  (h2-run-seed-list 'H-C *h2-seeds-primary* input-file output-dir "primary")
  (format t "H2-PRIMARY-BATCH-COMPLETE~%"))

(defun run-h2-matching-replication (input-file output-dir)
  (ensure-directories-exist (pathname (format nil "~A/" output-dir)))
  (h2-run-seed-list 'H-S *h2-seeds-replication* input-file output-dir "replication")
  (h2-run-seed-list 'H-C *h2-seeds-replication* input-file output-dir "replication")
  (format t "H2-REPLICATION-BATCH-COMPLETE~%"))
