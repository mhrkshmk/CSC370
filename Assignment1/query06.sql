-- Retrieve alphabetically all pairs of counties (along with their ids)
-- that have the same name but voted for different parties
-- in 2020. Break any ties with the first county's id and
-- then the second county's id
-- 1.02 marks: <12 operators
-- 1.00 marks: <13 operators
-- 0.90 marks: <14 operators
-- 0.80 marks: correct answer

SELECT ce1.fips, ce1.name, ce2.fips, ce2.name
FROM (
	SELECT *
	FROM ElectionResult e1
	JOIN County ON year = 2020 AND e1.county = County.fips
) AS ce1,
(
	SELECT *
    FROM ElectionResult e2
    JOIN County ON year = 2020 AND e2.county = County.fips
) AS ce2
WHERE ce1.name = ce2.name AND ce1.county < ce2.county AND ((ce1.dem > ce1.gop AND ce2.dem < ce2.gop) OR (ce1.gop > ce1.dem AND ce2.gop < ce2.dem))
ORDER BY ce1.name, ce1.fips, ce2.fips ASC;