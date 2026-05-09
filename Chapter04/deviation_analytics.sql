-- deviation_analytics.sql
-- Identify patterns in golden path deviations

WITH deviation_summary AS (
  SELECT 
    deviation_type,
    domain,
    COUNT(*) as deviation_count,
    COUNT(DISTINCT team_name) as affected_teams,
    AVG(CASE WHEN approved THEN 1 ELSE 0 END) as approval_rate
  FROM deviations
  WHERE requested_at >= CURRENT_DATE - INTERVAL '90 days'
  GROUP BY deviation_type, domain
)
SELECT 
  deviation_type,
  domain,
  deviation_count,
  affected_teams,
  ROUND(approval_rate * 100, 1) as approval_pct,
  CASE 
    WHEN affected_teams >= 3 AND approval_rate > 0.8 
    THEN 'Consider adding to golden path'
    WHEN approval_rate < 0.2 
    THEN 'Review deviation category'
    ELSE 'Monitor'
  END as recommendation
FROM deviation_summary
ORDER BY deviation_count DESC;
