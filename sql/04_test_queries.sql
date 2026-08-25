-- These are review queries, not application raw-SQL tools.

SELECT patient_id, encounter_id, task_type, task_status
FROM cg_care_tasks
WHERE patient_id = 'PAT-1001'
  AND encounter_id = 'ENC-240817';

-- Authorization-before-ranking pattern:
SELECT doc_id, title, classification
FROM cg_document_chunks
WHERE approval_status = 'APPROVED'
  AND allowed_role = 'CARE_COORDINATOR'
  AND allowed_purpose = 'CARE_COORDINATION';

-- Verify stale content cannot enter eligible retrieval set.
SELECT COUNT(*) AS retired_in_eligible_set
FROM cg_document_chunks
WHERE approval_status = 'APPROVED'
  AND doc_id = 'STALE-01';
