-- Retrieve the name of all counties, ordered alphabetically,
-- that had a six-figure average income and voted Republican in 2020
-- 1.1 marks: < 5 operators
-- 1.0 marks: < 6 operators
-- 0.8 marks: correct answer

SELECT name
FROM County, ElectionResult
WHERE (year = 2020 AND gop > dem AND avg_income >= 100000 AND fips = county)
ORDER BY name ASC