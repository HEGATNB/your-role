PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    deadline TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
);

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    required_skill TEXT NOT NULL,
    min_experience INTEGER NOT NULL DEFAULT 0 CHECK (min_experience >= 0)
);

CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    skills TEXT NOT NULL DEFAULT '[]',
    experience INTEGER NOT NULL DEFAULT 0 CHECK (experience >= 0),
    assigned_role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    max_size INTEGER NOT NULL CHECK (max_size > 0)
);

CREATE TABLE IF NOT EXISTS team_participants (
    team_id INTEGER NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    participant_id INTEGER NOT NULL REFERENCES participants(id) ON DELETE CASCADE,
    PRIMARY KEY (team_id, participant_id)
);

CREATE TABLE IF NOT EXISTS participant_preferences (
    participant_id INTEGER NOT NULL REFERENCES participants(id) ON DELETE CASCADE,
    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (participant_id, role_id)
);
