-- Retrieve the five states
-- that had the largest (relative) increase in
-- votes for the democrat party from 2016 to 2020
-- 1.02 marks: <9 operators
-- 1.00 marks: <11 operators
-- 0.80 marks: correct answer

SELECT abbr AS State, (SUM(er2.dem) - SUM(er1.dem)) / SUM(er1.dem) AS VoteChange
FROM ElectionResult er1, ElectionResult er2, County, State
WHERE er1.county = er2.county
  AND er1.county = County.fips
  AND County.state = State.id
  AND er1.year = 2016
  AND er2.year = 2020
GROUP BY abbr
ORDER BY VoteChange DESC
LIMIT 5;