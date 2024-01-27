-- Show all counties ordered by their total
-- number of employees across all industries
-- Tie-break with the county id in ascending order.
-- 1.1 marks: <6 operators
-- 1.0 marks: <7 operators
-- 0.8 marks: correct answer

SELECT fips, name, state, sq_km, precip, snow, temp, life_expectancy, avg_income
FROM CountyIndustries
JOIN County ON CountyIndustries.county = County.fips
GROUP BY CountyIndustries.county
ORDER BY SUM(CountyIndustries.employees), fips