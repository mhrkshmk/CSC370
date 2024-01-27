-- Retrieve the name of all counties, ordered alphabetically, in Texas
-- that have seen at least 2.5% population growth every year on record
-- 1.02 marks: <9 operators
-- 1.00 marks: <12 operators
-- 0.80 marks: correct answer

SELECT name AS County
FROM CountyPopulation cp1
JOIN County ON County.fips = cp1.county AND County.state = 4
JOIN CountyPopulation cp2 ON cp1.county = cp2.county AND cp1.year = cp2.year + 1
WHERE (cp1.population - cp2.population) / cp2.population >= 0.025
GROUP BY cp1.county
HAVING COUNT(*) = 9
ORDER BY name ASC;