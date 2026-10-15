-- 1. List all projects
SELECT id, name, deadline FROM projects ORDER BY deadline;

-- 2. List active projects (WHERE)
SELECT id, name FROM projects WHERE is_active = 1 ORDER BY name;

-- 3. Teams for a project (parameter: project id)
SELECT id, name, max_size FROM teams WHERE project_id = ? ORDER BY name;

-- 4. Participants with a minimum experience (WHERE, parameter)
SELECT id, name, experience FROM participants WHERE experience >= ?;

-- 5. List role catalogue
SELECT id, name, required_skill FROM roles ORDER BY name;

-- 6. Roles requiring a selected skill (WHERE, parameter)
SELECT id, name FROM roles WHERE required_skill = ? ORDER BY name;

-- 7. Participants with their assigned role (JOIN)
SELECT p.name, r.name AS role FROM participants p
LEFT JOIN roles r ON r.id = p.assigned_role_id ORDER BY p.name;

-- 8. Team roster with project and participant names (JOIN)
SELECT t.name AS team, pr.name AS project, p.name AS participant
FROM teams t JOIN projects pr ON pr.id = t.project_id
JOIN team_participants tp ON tp.team_id = t.id
JOIN participants p ON p.id = tp.participant_id ORDER BY t.name, p.name;

-- 9. Number of participants in the database (COUNT)
SELECT COUNT(*) AS participant_count FROM participants;

-- 10. Participants assigned to each role (COUNT, GROUP BY)
SELECT r.name, COUNT(p.id) AS assigned_count
FROM roles r LEFT JOIN participants p ON p.assigned_role_id = r.id
GROUP BY r.id, r.name ORDER BY assigned_count DESC, r.name;

-- 11. Team occupancy (JOIN, COUNT, GROUP BY)
SELECT t.id, t.name, t.max_size, COUNT(tp.participant_id) AS member_count
FROM teams t LEFT JOIN team_participants tp ON tp.team_id = t.id
GROUP BY t.id, t.name, t.max_size ORDER BY t.name;

-- 12. Teams with available seats for a selected project
SELECT t.id, t.name, t.max_size - COUNT(tp.participant_id) AS free_slots
FROM teams t LEFT JOIN team_participants tp ON tp.team_id = t.id
WHERE t.project_id = ? GROUP BY t.id, t.name, t.max_size
HAVING t.max_size - COUNT(tp.participant_id) > 0 ORDER BY t.name;

-- 13. Average participant experience by assigned role (AVG, GROUP BY)
SELECT r.name, AVG(p.experience) AS average_experience
FROM roles r JOIN participants p ON p.assigned_role_id = r.id
GROUP BY r.id, r.name ORDER BY average_experience DESC;
