
import json
from pathlib import Path

from db.database import BASE_DIR, get_connection, initialize_database


def read_json(filename: str) -> list[dict]:
    path = BASE_DIR / "data" / filename
    return json.loads(path.read_text(encoding="utf-8"))


def import_json() -> None:
    projects = read_json("projects.json")
    roles = read_json("roles.json")
    participants = read_json("participants.json")
    teams = read_json("teams.json")
    initialize_database()

    with get_connection() as connection:
        connection.execute("DELETE FROM participant_preferences")
        connection.execute("DELETE FROM team_participants")
        connection.execute("DELETE FROM teams")
        connection.execute("DELETE FROM participants")
        connection.execute("DELETE FROM roles")
        connection.execute("DELETE FROM projects")
        connection.executemany(
            "INSERT INTO projects VALUES (?, ?, ?, ?, ?)",
            [(p["id"], p["name"], p["description"], p["deadline"],
              int(p["is_active"])) for p in projects],
        )
        connection.executemany(
            "INSERT INTO roles VALUES (?, ?, ?, ?, ?)",
            [(r["id"], r["name"], r["description"], r["required_skill"],
              r["min_experience"]) for r in roles],
        )
        connection.executemany(
            "INSERT INTO participants VALUES (?, ?, ?, ?, ?, ?)",
            [(p["id"], p["name"], p["email"], json.dumps(p["skills"],
              ensure_ascii=False), p["experience"], p["assigned_role_id"])
             for p in participants],
        )
        connection.executemany(
            "INSERT INTO teams VALUES (?, ?, ?, ?)",
            [(t["id"], t["name"], t["project_id"], t["max_size"])
             for t in teams],
        )
        connection.executemany(
            "INSERT INTO team_participants VALUES (?, ?)",
            [(t["id"], pid) for t in teams for pid in t["participant_ids"]],
        )
        connection.executemany(
            "INSERT INTO participant_preferences VALUES (?, ?)",
            [(p["id"], rid) for p in participants
             for rid in p["preferred_role_ids"]],
        )


if __name__ == "__main__":
    import_json()
    print(f"Imported JSON data into {Path('data/yourrole.sqlite3')}")
