-- Synthetic only
INSERT INTO cg_patients(patient_id, synthetic_name) VALUES ('PAT-1001', 'Jordan Lee');

INSERT INTO cg_encounters(encounter_id, patient_id, encounter_type, status)
VALUES ('ENC-240817', 'PAT-1001', 'Synthetic knee-replacement encounter', 'DISCHARGE_COORDINATION');

INSERT INTO cg_care_tasks(task_id, patient_id, encounter_id, task_type, task_status)
VALUES ('TASK-001', 'PAT-1001', 'ENC-240817', 'MEDICATION_RECONCILIATION', 'COMPLETE');

INSERT INTO cg_care_tasks(task_id, patient_id, encounter_id, task_type, task_status)
VALUES ('TASK-002', 'PAT-1001', 'ENC-240817', 'FOLLOW_UP', 'SCHEDULED');

INSERT INTO cg_care_tasks(task_id, patient_id, encounter_id, task_type, task_status)
VALUES ('TASK-003', 'PAT-1001', 'ENC-240817', 'HOME_OXYGEN_VENDOR', 'PENDING');

INSERT INTO cg_care_tasks(task_id, patient_id, encounter_id, task_type, task_status)
VALUES ('TASK-004', 'PAT-1001', 'ENC-240817', 'TRANSPORTATION', 'PENDING');

COMMIT;
