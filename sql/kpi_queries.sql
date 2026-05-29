-- Appointment volume by department
SELECT
    department,
    COUNT(*) AS appointment_volume
FROM healthcare_operations
GROUP BY department
ORDER BY appointment_volume DESC;

-- Monthly operational KPI trend
SELECT
    DATE_TRUNC('month', encounter_date) AS month,
    COUNT(*) AS appointment_volume,
    AVG(wait_time_minutes) AS average_wait_time,
    AVG(readmitted_30_days) * 100 AS readmission_rate,
    AVG(CASE WHEN claim_status = 'Denied' THEN 1 ELSE 0 END) * 100 AS claim_denial_rate,
    AVG(satisfaction_score) AS average_satisfaction
FROM healthcare_operations
GROUP BY DATE_TRUNC('month', encounter_date)
ORDER BY month;

-- Claim denial rate by payer
SELECT
    payer,
    COUNT(*) AS total_claims,
    SUM(CASE WHEN claim_status = 'Denied' THEN 1 ELSE 0 END) AS denied_claims,
    100.0 * SUM(CASE WHEN claim_status = 'Denied' THEN 1 ELSE 0 END) / COUNT(*) AS denial_rate
FROM healthcare_operations
GROUP BY payer
ORDER BY denial_rate DESC;

-- Departments with wait times above the overall average
SELECT
    department,
    AVG(wait_time_minutes) AS average_wait_time
FROM healthcare_operations
GROUP BY department
HAVING AVG(wait_time_minutes) > (
    SELECT AVG(wait_time_minutes)
    FROM healthcare_operations
)
ORDER BY average_wait_time DESC;

