-- Order by total payroll all states
-- that have fewer than 50 counties with payroll data
-- and at least ten industries of payroll data
-- 1.02 marks: <14 operators
-- 1.00 marks: <15 operators
-- 0.90 marks: <17 operators
-- 0.80 marks: correct answer

SELECT abbr, SUM(payroll)
FROM CountyIndustries
JOIN County ON CountyIndustries.county = County.fips
JOIN State ON County.state = State.id
GROUP BY state
HAVING COUNT(DISTINCT county) < 50 AND COUNT(DISTINCT industry) >= 10
ORDER BY SUM(payroll) DESC