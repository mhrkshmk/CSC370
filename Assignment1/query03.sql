-- Retrieve the names of all counties, ordered by id,
-- that had either less than USD $1M of total payroll in "Real Estate"
-- or no data on that industry altogether.
-- 1.1 marks: <9 operators
-- 1.0 marks: <11 operators
-- 0.8 marks: correct answer

SELECT *
	FROM County
	LEFT JOIN CountyIndustries ON County.fips = CountyIndustries.county AND CountyIndustries.industry = 7
	WHERE payroll < 1000000 OR payroll IS NULL
	ORDER BY COALESCE(payroll) ASC