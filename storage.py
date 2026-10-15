"""JSON persistence for the project entities."""

import json
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Any, TypeVar

from models import Participant, Project, Role, Team

T = TypeVar("T")


class StorageError(Exception):
    """Raised when project data cannot be read or written safely."""


class JSONRepository:
    def __init__(self, data_dir: str | Path = "data") -> None:
        self.data_dir = Path(data_dir)

    def _read(self, filename: str) -> list[dict[str, Any]]:
        path = self.data_dir / filename
        if not path.exists():
            return []
        try:
            with path.open(encoding="utf-8") as stream:
                rows = json.load(stream)
        except (OSError, json.JSONDecodeError) as error:
            raise StorageError(f"Could not read {path.name}") from error
        if not isinstance(rows, list):
            raise StorageError(f"Expected a list in {path.name}")
        return rows

    def _write(self, filename: str, rows: list[dict[str, Any]]) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        try:
            with (self.data_dir / filename).open("w", encoding="utf-8") as stream:
                json.dump(rows, stream, ensure_ascii=False, indent=2)
        except OSError as error:
            raise StorageError(f"Could not write {filename}") from error

    def list_projects(self) -> list[Project]:
        projects = []
        for row in self._read("projects.json"):
            projects.append(Project(**{
                **row,
                "deadline": date.fromisoformat(row["deadline"]),
            }))
        return projects

    def list_teams(self) -> list[Team]:
        return [Team(**row) for row in self._read("teams.json")]

    def list_participants(self) -> list[Participant]:
        return [Participant(**row) for row in self._read("participants.json")]

    def list_roles(self) -> list[Role]:
        return [Role(**row) for row in self._read("roles.json")]

    def get(self, entity: type[T], object_id: int) -> T | None:
        readers = {
            Project: self.list_projects,
            Team: self.list_teams,
            Participant: self.list_participants,
            Role: self.list_roles,
        }
        return next((item for item in readers[entity]() if item.id == object_id), None)

    def save(self, entity: Project | Team | Participant | Role) -> None:
        files = {
            Project: "projects.json",
            Team: "teams.json",
            Participant: "participants.json",
            Role: "roles.json",
        }
        rows = self._read(files[type(entity)])
        row = asdict(entity)
        if isinstance(entity, Project):
            row["deadline"] = entity.deadline.isoformat()
        for index, current in enumerate(rows):
            if current["id"] == entity.id:
                rows[index] = row
                break
        else:
            rows.append(row)
        self._write(files[type(entity)], rows)
