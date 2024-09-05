-- select m.weekNumber, t1.manager, t2.manager, t3.manager
-- from matchup m
-- join team t1 ON  t1.teamId = m.team1Id
-- join team t2 ON  t2.teamId = m.team2Id
-- join team t3 ON  t3.teamId = m.team3Id
-- ORDER BY m.weekNumber


select * from team;