-- Retrieve for each state the average payroll
-- in the "mining" sector (total vs number of counties),
-- ordered by that average payroll
-- Hint: you may need the COALESCE function
-- 1.02 marks: <19 operators
-- 1.00 marks: <22 operators
-- 0.80 marks: correct answer

SELECT tb1.abbr, COALESCE(ROUND(tb2.`Payroll` / tb1.`Number of County`), 0) AS AvgPayroll
FROM (
	SELECT COUNT(fips) AS 'Number of County', abbr
    FROM County
    JOIN State ON County.state = State.id
    GROUP BY State
) tb1
LEFT JOIN
(
	SELECT abbr, SUM(payroll) AS 'Payroll'
	FROM CountyIndustries
	JOIN Industry ON CountyIndustries.industry = Industry.id and (Industry.name LIKE '%Mining%')
	JOIN County ON CountyIndustries.county = County.fips
	JOIN State ON County.state = State.id
	GROUP BY State
	ORDER BY 'AVG Payroll' DESC
) tb2 ON tb1.abbr = tb2.abbr
ORDER BY AVGPayroll DESC