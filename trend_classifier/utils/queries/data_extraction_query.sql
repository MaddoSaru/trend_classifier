SELECT
    *
FROM
    DEV_ANALYTICS_DB.STREAMLIT_SCHEMA.TREND_CLASSIFIER_TEST

;
/*
SELECT
    DATE(te.milestone_300_utc_ts) AS received_at_origin_processing_date_utc,
    s.brand_name,
    s.merchant_id,
    s.x_3pl_name,
    s.client_id,
    sf.account_lifecycle_stage_c,
    COUNT(*) AS shipment_volume
FROM
    {{ ref('int_common__shipment_enhanced') }} AS s
LEFT JOIN 
    {{ ref('int_common__summary_salesforce_account') }} AS sf 
    ON sf.account_id = s.salesforce_account_id
LEFT JOIN 
    {{ ref('int_common__tracking_events') }} AS te
    ON s.shipment_id = te.shipment_id
WHERE 
    te.milestone_300_utc_ts IS NOT NULL
    AND year(te.milestone_300_utc_ts) >=2022
    AND te.milestone_300_utc_ts < date_trunc('quarter', dateadd('quarter',-1,current_date))
    AND origin_processing_center_state in ('IL','NJ','CA')
    --and (s.brand_name is null or s.x_3pl_name is null)
    --and sf.churn_date_c is null
GROUP BY
    ALL
*/