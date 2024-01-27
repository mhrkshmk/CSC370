-- Consider the industry with the most employees
-- nationwide. Retrieve alphabetically all counties
-- that have fewer than 10 employees in that industry
-- (ignoring those with no data on it).
-- 1.02 marks: <10 operators
-- 1.00 marks: <12 operators
-- 0.80 marks: correct answer

SELECT name AS County
FROM County, CountyIndustries, (
	SELECT industry, SUM(employees) AS Employee
	FROM CountyIndustries
	GROUP BY industry
	ORDER BY Employee DESC
	LIMIT 1
) AS bi
WHERE County.fips = CountyIndustries.county AND CountyIndustries.industry = bi.industry AND CountyIndustries.employees < 10
ORDER BY name