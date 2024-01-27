-- Retrieve alphabetically the abbreviations of the states
-- in which one can find the ten counties that had the
-- largest (absolute) increase in employed persons
-- between 2008 and 2016.
-- 1.02 marks: <11 operators
-- 1.00 marks: <12 operators
-- 0.90 marks: <14 operators
-- 0.80 marks: correct answer

SELECT DISTINCT abbr
FROM
(	
	SELECT abbr
	FROM CountyLabourStats cls1, CountyLabourStats cls2, County, State
    WHERE (cls1.county = cls2.county AND cls1.year = 2008 AND cls2.year = 2016)
		AND cls1.county = County.fips
		AND State.id = County.state
	ORDER BY (cls2.employed - cls1.employed) DESC
    LIMIT 10
) AS tb
ORDER BY abbr